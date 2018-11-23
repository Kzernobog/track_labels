import tkinter as tk
from tkinter import messagebox
from detection_class import Detection


class IdWindow(tk.Toplevel):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.title("Enter ID")

        self.num_str = tk.StringVar()
        self.entered_number = None

        # label frame containing textbox and a label
        input_frame = tk.LabelFrame(self)
        input_frame.grid(row=0, column=0)
        input_label = tk.Label(input_frame, text="Enter the label")
        input_label.grid(row=0, column=0)
        entry_box = tk.Entry(input_frame, width=8, textvariable=self.num_str)
        entry_box.grid(row=0, column=1)

        # label frame containing store button
        output_frame = tk.LabelFrame(self)
        output_frame.grid(row=1, column=0)
        ok_button = tk.Button(output_frame, text='Ok', command=self.on_press_ok)
        ok_button.grid(row=0, column=0)
        self.grab_set()

    def on_press_ok(self):
        # check if the label entered for detection is proper
        label_string = self.num_str.get()

        if not label_string.isdigit() or int(label_string) < 1:
            messagebox.showerror("Bad Label", "Enter a positive integer for the label")
        else:
            self.entered_number = int(label_string)
            self.destroy()


def ask_id(detection: Detection):
    """
    Used to update the label of a detection from user input.
    Causes a GUI to be displayed which ask for a positive integer.
    Uses this to update the label.

    If the GUI is closed, the detection's label is NOT changed.
    :return: (None)
    """
    id_window = IdWindow()
    id_window.wait_window()
    entered_id = id_window.entered_number

    # TODO DEBUG
    print("Value entered is: {}".format(entered_id))

    if entered_id is not None:
        detection.label = entered_id


def ask_id_test():
    detection = Detection([0, 0, 0, 0])
    detection.label = 1
    print("Initial label for the detection: {}".format(detection.label))
    ask_id(detection)
    print("Final value of the detection: {}".format(detection.label))


if __name__ == '__main__':
    win = tk.Tk()
    tk.Button(win, text="Click Me", command=ask_id_test).pack()
    win.mainloop()
