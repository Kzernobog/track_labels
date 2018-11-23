import os
import sys
from tkinter import messagebox as msg
from PIL import Image
from PIL import ImageTk
from PIL.ImageTk import PhotoImage
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from tkinter import filedialog
from tkinter import scrolledtext as sct
import cv2
from DetectionTracker import Tracker as tracker
import tiny_yolo.TinyYoloDetection as TY
from detection_list_class import DetectionList
from ask_id_window import ask_id


class TrackLabelGUI(object):

    def __init__(self):
        self._root = tk.Tk()
        self._child_root = None
        self._root.title("Track Label")
        self._width = 720
        self._height = 480

        # in case you use this GUI in an OSX environment
        if self._root.tk.call('tk', 'windowingsystem') == 'aqua':
            s = ttk.Style()
            s.configure('TNotebook.Tab', padding=(12, 8, 12, 0))

        # class level attributes
        self._video_name = None
        self._vidcap = None
        self.tracker_obj = tracker.Tracker(log=False)

        # the frame loaded from the video (this should always be unaltered)
        self.frame = None

        # initialize a few UI features
        self._initialize_tab_control()
        self._initialize_labeler_tab()

        # video related variables
        self._NUM_OF_VID_FRAMES = None
        self._frame_num = 0

        # detector related initializations
        self._config_path = "tiny_yolo/tiny-tank-yolo-mhm_31_Oct.cfg"
        self._weight_path = "tiny_yolo/tiny-tank-yolo-mhm_31_Oct_43400.weights"
        self._meta_path = "tiny_yolo/tank.data"

        self._detector = TY.YOLODetector(self._config_path, self._weight_path, self._meta_path)

        self.detection_list: DetectionList = None

        # certain label txt related variables
        self._label_folder = './Labels'
        self._videos_folder = './Videos'
        self._video_file_path = None

    def _initialize_tab_control(self):
        self._tabcontrol = ttk.Notebook(self._root)
        self._track_label_tab = tk.Frame(self._tabcontrol)
        self._tabcontrol.add(self._track_label_tab, text="Track Labelling")
        self._tabcontrol.pack(expand=1, fill='both')
        return None

    # initializes the main UI display
    def _initialize_labeler_tab(self):
        self._mainUIFrame = ttk.Labelframe(self._track_label_tab, width=self._width, height=self._height)
        self._mainUIFrame.grid(row=0, column=0)

        # main image label
        self._image_label = ttk.Label(self._mainUIFrame)
        self._image_label.grid(row=1, column=0, columnspan=5)
        self._image_label.bind("<Button-1>", self._leftclick)

        # label display

        # button to load video
        self._video_load_btn = ttk.Button(self._mainUIFrame, text="load video", command=self._load_video)
        self._video_load_btn.grid(row=0, column=0, sticky=tk.W)

        # button to load next frame
        self._load_next_frame_btn = ttk.Button(self._mainUIFrame, text="Next", command=self._get_next_frame)
        self._load_next_frame_btn.grid(row=0, column=4, sticky=tk.E)

        return None

    # retrieves the next frame, runs it through the detector, displays it 
    def _get_next_frame(self):
        if self.detection_list.all_marked():  # if all detections have been labelled
            self._write_into_file()

        else:  # if detections are left which are yet to be labelled
            msg.showinfo('Unfinished labelling', 'There are Detections yet to be labelled')
            return

        # checks if there are any valid frames
        if self._frame_num > self._NUM_OF_VID_FRAMES:
            msg.showinfo('Frame does not exist',
                         'This application has not been designed to rupture the space-time continuum')
            return None

        # retrieves the next frame
        self._frame_num += 1
        self._vidcap.set(cv2.CAP_PROP_POS_FRAMES, self._frame_num - 1)
        ok, self.frame = self._vidcap.read()

        confidence_list, boxes, frame = self._detector.detect(self.frame.copy(), draw=False)
        self.detection_list = DetectionList(boxes)
        current_detected_list = self.detection_list.get_bbox_list()

        tracklet_id = self.tracker_obj.update_frame(current_detected_list.copy(), None)

        for idx, detection in enumerate(self.detection_list.detections_list):
            detection.label = tracklet_id[idx]

        frame = self.detection_list.draw(frame)
        self._display_frame(frame)

        if not ok:
            print("frame retrieval unsuccessful")
            sys.exit()

        return None

    # function that writes into file
    def _write_into_file(self):
        bbox_list = self.detection_list.get_bbox_list()
        labels_list = self.detection_list.get_labels_list()
        text = "{},{},{}\n".format(self._frame_num, bbox_list, labels_list)
        with open(self._video_file_path, 'a') as f:
            f.write(text)

        return None

    # click event handler function
    def _leftclick(self, event):
        x = event.x
        y = event.y
        point = (x, y)

        # get the detection to which the point belongs
        target_detection = self.detection_list.get_detection_containing_point(point)

        if target_detection is not None:  # point belongs to a detection
            ask_id(target_detection)

            # redraw frame and show in GUI
            drawn_frame = self.detection_list.draw(self.frame)
            self._display_frame(drawn_frame)

        else:  # the click was outside a detection
            msg.showerror("Click outside detection box",
                          "Please click inside a detection box to enter its id.")

    # detects the tanks and display them
    def _display_frame(self, frame):
        """
        Displays the frame provided on the GUI.
        :param frame: image to be displayed
        :return: (None)
        """

        # switch to RGB format
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # make it PIL ImageTk compatible
        image = Image.fromarray(image)
        # make it imgtk compatible
        image = ImageTk.PhotoImage(image)
        # store the image in the label
        self._image_label.imgtk = image
        # configure the image to the corresponding size
        self._image_label.configure(image=image)
        # store the reference to the image so that Python's gc doesn't erase the image
        self._image_label.image = image
        return None

    def _load_video(self):
        self._video_name = tk.filedialog.askopenfilename()
        self._vidcap = cv2.VideoCapture(self._video_name)
        self._NUM_OF_VID_FRAMES = int(self._vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
        self._frame_num += 1
        self._vidcap.set(cv2.CAP_PROP_POS_FRAMES, self._frame_num - 1)
        ok, self.frame = self._vidcap.read()

        if not ok:
            print("frame retrieval not successful")
            sys.exit()
            #     self._write_into_file()

        current_detected_list = []

        confidence_list, boxes, frame = self._detector.detect(self.frame.copy(), draw=False)
        self.detection_list = DetectionList(boxes)

        for detection in self.detection_list.detections_list:
            current_detected_list.append(detection.bbox)

        tracklet_id = self.tracker_obj.start_tracking(current_detected_list.copy(), None)

        for idx, detection in enumerate(self.detection_list.detections_list):
            detection.label = tracklet_id[idx]

        frame = self.detection_list.draw(frame)
        self._display_frame(frame)

        # creates a .txt file for writing
        video_file = self._video_name.split('/')[-1].split('.')[0]
        if not os.path.exists(self._label_folder):
            os.makedirs(self._label_folder)
        if not os.path.exists(self._videos_folder):
            os.makedirs(self._videos_folder)
        self._video_file_path = os.path.join(self._label_folder, video_file + '_label.txt')
        with open(self._video_file_path, 'w') as f:
            text = "frameID, detection_list, label_list\n"
            f.write(text)
        return None

    def run(self):
        self._root.mainloop()
        return None

    def release(self):
        self._vidcap.release()


if __name__ == "__main__":
    tracking = TrackLabelGUI()
    tracking.run()
