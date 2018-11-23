import math
import cv2
import numpy as np


from queue import Queue


class Tracklet:

    # TODO: pass anglular position to tracklet
    def __init__(self, initial_bbox, timestamp, tracklet_id):
        self.queue_length = 40
        self.bbox_queue: Queue = Queue(self.queue_length)
        self.bbox_queue.put(initial_bbox)
        self.timestamp_queue: Queue = Queue(self.queue_length)
        self.timestamp_queue.put(timestamp)
        self.gamma = 0
        self.tracklet_id = tracklet_id

    def push(self, q, item):
        if q.full():
            q.get()
            q.put(item)
        else:
            q.put(item)

    def update_tracklet(self, current_bbox, current_timestamp):

        self.push(self.bbox_queue, current_bbox)

        self.push(self.timestamp_queue, current_timestamp)

    def calc_iou_score(self, bbox):
        bbox_list = list(self.bbox_queue.queue)
        tracking_bbox = bbox_list[-1]
        detection_bbox = bbox
        xA = max(tracking_bbox[0], detection_bbox[0])
        yA = max(tracking_bbox[1], detection_bbox[1])
        xB = min(tracking_bbox[2], detection_bbox[2])
        yB = min(tracking_bbox[3], detection_bbox[3])

        # compute the area of intersection rectangle
        interArea = abs(max((xB - xA, 0)) * max((yB - yA), 0))
        if interArea == 0:
            return 0
        # compute the area of both the prediction and ground-truth rectangles
        tracking_bbox_area = abs((tracking_bbox[2] - tracking_bbox[0]) * (tracking_bbox[3] - tracking_bbox[1]))
        detection_bbox_area = abs((detection_bbox[2] - detection_bbox[0]) * (detection_bbox[3] - detection_bbox[1]))
        # compute the intersection over union by taking the intersection
        # area and dividing it by the sum of prediction + ground-truth
        # areas - the intersection area
        iou = interArea / float(tracking_bbox_area + detection_bbox_area - interArea)

        # return the intersection over union value

        return iou



    # TODO: take atgm_state
    def draw_tracking_bbox(self, frame, debug=False, box_thickness=2):
        """

        :param frame: one frame from video read using cv2
        :param box_thickness: (integer) number of pixels for thickness of box
        :return: None

        Drawing a tracking box on the frame provided using the lastest bbox_list value
        Marks the box with the tracklet id
        If it is a ghost box, its velocity is shown at the bottom left of the box
        """
        velocity = None

        bbox_list = list(self.bbox_queue.queue)

        bbox = bbox_list[-1]

        text = ''

        text += "ID: T{}".format(self.tracklet_id)

        cv2.putText(frame, text, (bbox[0] + 4, bbox[3] - 5)
                    , cv2.FONT_HERSHEY_SIMPLEX, 0.5, [255, 255, 255], 1, cv2.LINE_AA)
