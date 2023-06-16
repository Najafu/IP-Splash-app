import tkinter as tk


class Temp(tk.Frame):
    def __init__(self, parent, controller=None, *args, **kargs):
        tk.Frame.__init__(self, parent, *args, **kargs)

        tk.Label(self, text="Testing New Method", font=("Halvetica", 14)).pack()



root = tk.Tk()
app = Temp(root)
app.pack()
tk.mainloop()
