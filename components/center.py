import tkinter as tk
from tkinter import ttk

from components.IPEntry import IPEntry


class Center(tk.Frame):
    def __init__(self, parent, controller=None, *args, **kargs):
        tk.Frame.__init__(self, parent, *args, **kargs)

        lb1 = ttk.Label(self, text="IP Address:", anchor="w", width=17)
        lb2 = ttk.Label(self, text="Subnet mask:", anchor="w", width=17)
        lb3 = ttk.Label(self, text="Gateway:", anchor="w", width=17)

        self.ip_entrybox = IPEntry(self, name="ip_address")
        self.mask_entrybox = IPEntry(self, name="subnet_mask")
        self.gateway_entrybox = IPEntry(self, name="gateway")

        lb1.grid(row=0, column=0)
        lb2.grid(row=0, column=1)
        lb3.grid(row=0, column=2)
        self.ip_entrybox.grid(row=1, column=0)
        self.mask_entrybox.grid(row=1, column=1, padx=2)
        self.gateway_entrybox.grid(row=1, column=2)
