import tkinter as tk


class StatusBar(tk.Frame):
    def __init__(self, parent, controller=None, *args, **kargs):
        tk.Frame.__init__(self, parent, *args, **kargs)

        self.statusbar = tk.Label(self, text="")
        self.statusbar.pack()

    def update(self, msg, error_flag=None):
        self.statusbar.configure(fg="SystemButtonText")
        if error_flag:
            self.statusbar.configure(fg="red")
        self.statusbar["text"] = msg + ""
