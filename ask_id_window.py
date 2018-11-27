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
        self.entry_box = tk.Entry(input_frame, width=8, textvariable=self.num_str)
        self.entry_box.grid(row=0, column=1)

        # label frame for radio buttons to mark occlusion and no-tank
        occ_frame = tk.LabelFrame(self)
        occ_frame.grid(row=1, column=0)
        self.rad_var = tk.IntVar()
        self.rad_var.set(0)  # normal mode is selected by default
        rad_1 = tk.Radiobutton(occ_frame, text='No Tank', variable=self.rad_var, value=-1, command=self.rad_call)
        rad_1.grid(row=0, column=0)
        rad_2 = tk.Radiobutton(occ_frame, text='Tank-Tank Occlusion', variable=self.rad_var, value=-2,
                               command=self.rad_call)
        rad_2.grid(row=0, column=1)
        rad_3 = tk.Radiobutton(occ_frame, text='Normal', variable=self.rad_var, value=0, command=self.rad_call)
        rad_3.grid(row=0, column=2)

        # label frame containing store button
        output_frame = tk.LabelFrame(self)
        output_frame.grid(row=2, column=0)
        ok_button = tk.Button(output_frame, text='Ok', command=self.on_press_ok)
        ok_button.grid(row=0, column=0)

        # bind enter key to the ok button
        self.bind('<Return>', self.on_press_ok)

        # keep focus on this window till destroyed
        self.grab_set()

        # set focus to the text field where id is entered
        self.entry_box.focus_set()

    def rad_call(self):
        rad_selected = self.rad_var.get()

        # TODO remove everything in textbox and disable it

        if rad_selected == -1 or rad_selected == -2:  # No tank in frame or occ
            self.num_str = ''  # empty the textbox
            self.entry_box.config(state = 'disabled')  # disable the text box which takes ids
        elif rad_selected == 0:  # normal mode
            self.entry_box.config(state = 'normal')

    def on_press_ok(self, event=None):
        """
        This is what happens when the ok button is pressed.
        If the value in the text field is an integer, it sets the corresponding
        class attribute with this number which can then be retrieved outside.
        Else, an error is displayed.
        :param event: A parameter that is passed by bind function (pressing enter here)
        :return: (None)
        """
        # check if textbox should be used (for eg, it should not if in occ mode)
        rad_selected = self.rad_var.get()

        if rad_selected == 0:  # normal mode
            label_string = self.num_str.get()

            if not label_string.isdigit() or int(label_string) < 1:
                messagebox.showerror("Bad Label", "Enter a positive integer for the label")
            else:
                self.entered_number = int(label_string)
        else:  # it is either in tank-tank occlusion or no-tank
            self.entered_number = rad_selected

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
