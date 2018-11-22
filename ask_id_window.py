import tkinter as tk
from tkinter import messagebox


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


def launch_top_level():
    id_window = IdWindow()
    id_window.wait_window()
    print("The entered number is {}.".format(id_window.entered_number))
    return id_window.entered_number

win = tk.Tk()
tk.Button(win, text="Click Me", command = launch_top_level).pack()
win.mainloop()