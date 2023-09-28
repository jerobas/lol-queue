import tkinter as tk
from tkinter import ttk
import os
from script import main
import multiprocessing


class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)

        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        self.ban = tk.BooleanVar()
        self.pick = tk.BooleanVar()

        self.setup_widgets()

    def startScript(self):
        if self.ban.get():
            arg1 = self.entry.get()
        else:
            arg1 = "None"

        if self.pick.get():
            arg2 = self.entry_pick.get()
        else:
            arg2 = "None"
        processo = multiprocessing.Process(target=main, args=(arg2, arg1))
        processo.start()

    def setup_widgets(self):
        self.widgets_frame = ttk.Frame(self, padding=(0, 0, 0, 10))
        self.widgets_frame.grid(
            row=0, column=1, padx=10, pady=(30, 10), sticky="nsew", rowspan=3
        )
        self.widgets_frame.columnconfigure(index=0, weight=1)

        self.label = ttk.Label(self.widgets_frame, text="Ban champion")
        self.label.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="w")

        self.check_1 = ttk.Checkbutton(
            self.widgets_frame, text="Auto Ban", variable=self.ban
        )
        self.check_1.grid(row=1, column=0, sticky="nsew")

        self.entry = ttk.Entry(self.widgets_frame)
        self.entry.insert(0, "")
        self.entry.grid(row=2, column=0, padx=5, pady=(0, 10), sticky="ew")

        self.label = ttk.Label(self.widgets_frame, text="Pick champion")
        self.label.grid(row=3, column=0, padx=5, pady=(0, 5), sticky="w")

        self.check_2 = ttk.Checkbutton(
            self.widgets_frame, text="Auto Pick", variable=self.pick
        )
        self.check_2.grid(row=4, column=0, sticky="nsew")

        self.entry_pick = ttk.Entry(self.widgets_frame)
        self.entry_pick.insert(0, "")
        self.entry_pick.grid(row=5, column=0, padx=5,
                             pady=(0, 10), sticky="ew")

        self.button = ttk.Button(
            self.widgets_frame, text="Run", command=self.startScript)
        self.button.grid(row=8, column=0, padx=5, pady=10, sticky="nsew")

        footer_label = ttk.Label(
            self.widgets_frame,
            text="Created by flaviozno and jaonolo",
            anchor="center"
        )
        footer_label.grid(row=9, column=0, padx=5, pady=(10, 0), sticky="nsew")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("LOL - QUEUE")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    azure_tcl_path = os.path.join(script_dir, "interface", "azure.tcl")
    root.tk.call("source", azure_tcl_path)
    root.tk.call("set_theme", "dark")

    app = App(root)
    app.pack(fill="both", expand=True)

    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) -
                      (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) -
                      (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

    root.mainloop()
