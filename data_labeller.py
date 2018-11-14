import sys
from PIL import Image
from PIL import ImageTk
from PIL.ImageTk import PhotoImage
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from tkinter import filedialog
from tkinter import scrolledtext as sct
import cv2

class Track_Label_GUI(object):

    def __init__(self):
        self._root = tk.Tk()
        self._root.title("Labeller")
        self._width = 720
        self._height = 480

        if self._root.tk.call('tk', 'windowingsystem') == 'aqua':
            s = ttk.Style()
            s.configure('TNotebook.Tab', padding=(12, 8, 12, 0))

        # class level attributes
        self._video_name = None
        self._vidcap = None

        # initialize a few UI features
        self._initialize_tab_control()
        self._initialize_labeller_tab()
        return None

    def _initialize_tab_control(self):
        self._tabcontrol = ttk.Notebook(self._root)
        self._track_label_tab = tk.Frame(self._tabcontrol)
        self._tabcontrol.add(self._track_label_tab, text="Track Labelling")
        self._tabcontrol.pack(expand=1,fill='both')
        return None

    def _initialize_labeller_tab(self):
        self._mainUIFrame = ttk.Labelframe(self._track_label_tab, width = self._width, height=self._height)
        self._mainUIFrame.grid(row=0, column=0)

        # main image label
        self._image_label = ttk.Label(self._mainUIFrame)
        self._image_label.grid(row=1, column=0, columnspan=5)

        # button to load video
        self._video_load_btn = ttk.Button(self._mainUIFrame, text="load video", command=self._load_video)
        self._video_load_btn.grid(row=0, column=0)

        # button to load next frame
        self._load_next_frame_btn = ttk.Button(self._mainUIFrame, text="Next", command=self._get_next_frame)
        self._load_next_frame_btn.grid(row=0, column=4)
        return None

    def _get_next_frame(self):
        ok, frame = self._vidcap.read()
        if not ok:
            print("frame retrieval not successfull")
            sys.exit()

        # switch to RGB format
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # make it PIL ImageTk compatible
        image = Image.fromarray(image)
        # crosshair overlay
        image = self._crosshair_overlay(image, self._crosshair_image)
        # make it imgtk compatible
        image = ImageTk.PhotoImage(image)
        # store the image in the label
        self._image_label.imgtk = image
        # configure the image to the corresponding size
        self._image_label.configure(image=image)
        # store the reference to the image so that Python's gc doesn't erase the image
        self._image_label.image = image
        return None

    def _detection_display(self, frame):
        pass

    def _load_video(self):
        self._video_name = tk.filedialog.askopenfilename()
        self._vidcap = cv2.VideoCapture(self._video_name)
        return None

    def run(self):
        self._root.mainloop()


if __name__ == "__main__":
    tracking = Track_Label_GUI()
    tracking.run()
