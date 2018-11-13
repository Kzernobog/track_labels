import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from tkinter import filedialog
from tkinter import scrolledtext as sct

class Track_Label_GUI(object):

    def __init__(self):
        self._root = tk.Tk()
        self._root.title("Labeller")
        self._width = 720
        self._height = 480

        # initialize a few UI features
        self._initialize_tab_control()
        self._initialize_labeller_tab()
        return None

    def _initialize_tab_control(self):
        pass

    def _initialize_labeller_tab(self):
        pass


