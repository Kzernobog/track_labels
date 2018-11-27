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

        # bind enter key to the ok button
        self.bind('<Return>', self.on_press_ok)

        # keep focus on this window till destroyed
        self.grab_set()

        # set focus to the text field where id is entered
        entry_box.focus_set()

    def on_press_ok(self, event = None):
        """
        This is what happens when the ok button is pressed.
        If the value in the text field is an integer, it sets the corresponding
        class attribute with this number which can then be retrieved outside.
        Else, an error is displayed.
        :param event: A parameter that is passed by bind function (pressing enter here)
        :return: (None)
        """
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
