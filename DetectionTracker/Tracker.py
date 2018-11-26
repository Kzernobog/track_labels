import glob
import operator

import numpy as np
import tqdm
import os
import sys

import DetectionTracker.Tracklet
import time
import math
import pdb
import pandas as pd
import cv2


class Tracker:
    def __init__(self, log=True):
        self.tracklet_list = []
        self.id_iterator = _IdIterator()
        self.frame_iterator = None
        self.score_threshold = 0.5
        self.frame_score = ""
        self.gamma_threshold = 5


    def update_frame(self, current_detected_list, labels_list):
        for idx,current_detection in enumerate(current_detected_list):
            self.tracklet_list += [DetectionTracker.Tracklet.Tracklet
                                   (current_detection,labels_list[idx])]


    def get_labels(self,current_detected_list):

        tracklet_id_list = []

        self._update_tracklets_with_detections(current_detected_list.copy(), None)

        for idx, detection in enumerate(current_detected_list):
            detection_match = False
            for tracklet in self.tracklet_list:
                bbox_list = list(tracklet.bbox_queue.queue)

                if (bbox_list[-1] == detection):
                    detection_index = idx
                    detection_match = True
                    tracklet_id_list.append(tracklet.tracklet_id)
                    break
            if detection_match==False:
                tracklet_id_list.append(None)

        # if(len(current_detected_list)>0):
        #     tracklet_id_list = [i[0] for i in tracklet_id_list]
        # if len(self.selected_tracklet.bbox_queue == None

        return tracklet_id_list


    def _create_frame_iterator(self, path):
        if os.path.isdir(path):  # is a folder (containing images)
            images_paths = glob.glob(path)

            if len(images_paths) == 0:  # the directory is empty

                raise Exception("Directory provided is empty")

            self.frame_iterator = iter(_TimedImageIterator(path))

        else:  # is a video file
            self.frame_iterator = iter(_TimedVideoIterator(path))

    def _update_tracklets_with_detections(self, current_detected_list, confidence_list, debug=False):
        """
        Using the provided detected list, the existing tracklets are updated. Any new tracklets that need to be
        made are also made.

        :param current_detected_list: (list) list of bboxes
        :param confidence_list: (list) corresponding list of confidences
        :param debug: (bool) make true while debugging (internal use only)
        :return: (None)
        """

        # Split the tracklet list into two groups based on high and low gamma value
        low_gamma_tracklet_list = []
        high_gamma_tracklet_list = []
        for tracklet in self.tracklet_list:
            # if tracklet.gamma >= 150:
            #     if self.selected_tracklet == tracklet:
            #         self.selected_tracklet = None
            #     self.tracklet_list.remove(tracklet)
            if tracklet.gamma <= self.gamma_threshold:
                low_gamma_tracklet_list.append(tracklet)
            else:
                high_gamma_tracklet_list.append(tracklet)

        self._make_associations(low_gamma_tracklet_list, current_detected_list, confidence_list)
        self._make_associations(high_gamma_tracklet_list, current_detected_list, confidence_list)

        # all unassigned detection boxes are used to make new tracklets
        # TODO add a confidence threshold to make a new tracklet
        # for current_detection in current_detected_list:
        #     # TODO Look at the Nuns
        #     if current_detection != None:
        #         self.tracklet_list.append(
        #             DetectionTracker.Tracklet.Tracklet(current_detection, next(self.id_iterator)))

    def _make_associations(self, tracklet_list, current_detected_list, confidence_list):

        # a matrix containing scores of all tracklets against all detections
        scores_mat = self._create_score_matrix(tracklet_list, current_detected_list)

        while ((scores_mat.shape[0] != 0 and scores_mat.shape[1] != 0) and (np.max(scores_mat) > self.score_threshold)):
            # get index of tracker and index of detection box which have the highest score
            t_idx, d_idx = np.unravel_index(np.argmax(scores_mat), scores_mat.shape)

            tracklet_to_update = tracklet_list[t_idx]
            associated_detection_box = current_detected_list[d_idx]

            # update tracklet with associated detection box

            # Writing azimuth and elevation angles to file for  debugging

            tracklet_to_update.update_tracklet(associated_detection_box)

            # delete the row and column from scores_mat
            scores_mat = np.delete(scores_mat, t_idx, 0)
            scores_mat = np.delete(scores_mat, d_idx, 1)

            # remove the tracklet and detection box from the corresponding lists
            tracklet_list.remove(tracklet_list[t_idx])
            current_detected_list.remove(current_detected_list[d_idx])

        else:
            # do ghost update for left over tracklets

            for tracklet in tracklet_list:
                tracklet.tracklet_id = None
                self.tracklet_list.remove(tracklet)


    def _create_score_matrix(self, tracklet_list, current_detected_list):

        score_matrix = np.array([[tracklet.calc_iou_score(current_detection)
                                  for current_detection in current_detected_list] for tracklet in tracklet_list])

        return score_matrix

    def _draw_detection_bboxes(self, frame, bbox_list, scores=None, confidences_list=None, colour=(0, 0, 255),
                               box_thickness=1):
        """

        :param frame: one frame from video read using cv2
        :param bbox_list: a list of bboxes (each of which is a list of 4 elements)
        :param confidences_list: (list) list of confidences of the detections
        :param colour: (tuple) specify colour of bounding box in (B, G, R) format
        :param box_thickness: (integer) number of pixels for thickness of bbox
        :return: None (modifies frame)

        Receives a frame along with auxiliary info and draws a bbox around all the tanks detected.
        The frame is modified.

        """

        for i in range(len(bbox_list)):
            text = ''
            bbox = bbox_list[i]

            assert len(bbox) == 4

            # display id for detection box
            dbox_id = i + 1
            text += "D{} ".format(dbox_id)

            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]),
                          colour, box_thickness)

            if (scores != None):
                text += "score: " + str(round(scores[i], 2)) + " "

            # show confidence for detection if confidence list is present
            if confidences_list != None:
                confidence = confidences_list[i]
                text += "Confidence: {0}".format(str(round(confidence, 2)))

            cv2.putText(frame, text, (bbox[0], bbox[1] - 5)
                        , cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour, 1, cv2.LINE_AA)

    def _draw_all_scores(self, scores_list_of_all_tracklets, frame):
        if len(scores_list_of_all_tracklets) > 0:
            data = [item[1] for item in scores_list_of_all_tracklets]
            index = ["T{}".format(item[0]) for item in scores_list_of_all_tracklets]
            columns = ["D{}".format(i) for i in range(1, len(scores_list_of_all_tracklets[0][1]) + 1)]

            df = pd.DataFrame(data=data, index=index, columns=columns)
            scores_txt = str(df.round(2))
        else:
            scores_txt = 'No detections made in this frame'

        y0, dy = 50, 20
        for i, line in enumerate(scores_txt.split('\n')):
            y = y0 + i * dy
            cv2.putText(frame, line, (100, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        [255, 0, 0], 1, cv2.LINE_AA)


class _TimedVideoIterator:
    """
    Class which creates an iterator for a video file
    The iterator returns video frames with timestamps
    """

    def __init__(self, vid_path):
        self.cap = cv2.VideoCapture(vid_path)

    def __iter__(self):
        return self

    def __next__(self):
        ret, frame = self.cap.read()
        if ret:
            return frame, time.time()
        else:
            raise StopIteration

    def __len__(self):
        return int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def get_frame_shape(self):
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return width, height


class _TimedImageIterator:
    """
    Class which creates an iterator for a folder containing images
    The iterator returns images with timestamps
    """

    def __init__(self, image_folder_path):
        # the iterator works only for images genereated by tank application
        sorted_image_paths = sorted(glob.glob(os.path.join(image_folder_path, "*.*")),
                                    key=lambda path: int(os.path.split(path)[1][7:-4]))
        self.image_paths = sorted_image_paths
        self.image_path_iterator = iter(self.image_paths)

    def __iter__(self):
        return self

    def __next__(self):
        image_path = next(self.image_path_iterator)
        image = cv2.imread(image_path)
        return image, time.time()

    def __len__(self):
        return len(self.image_paths)

    def get_frame_shape(self):
        frame_size = cv2.imread(self.image_paths[0]).shape[:-1][::-1]
        return frame_size


class _IdIterator:
    """
    Class which creates an iterator which runs forever and generates ids
    Ids are natural numbers
    """

    def __init__(self):
        self.n = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.n += 1
        return self.n
