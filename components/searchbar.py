import tkinter as tk
from tkinter import ttk


class SearchBar(tk.Frame):
    def __init__(self, parent, controller=None, *args, **kargs):
        tk.Frame.__init__(self, parent, *args, **kargs)

        self.searchbox = ttk.Entry(self)
        self.searchbox.pack(pady=5, fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.searchbox.bind("<KeyRelease>",lambda e: controller.handle_click_treeview_header_to_sort(event=e, order_by="id"))
        self.searchbox.bind("<Escape>", controller.handle_click_clear_searchbox)

        self.searchbtn = ttk.Button(
            self,
            text="Clear Search",
            command=controller.handle_click_clear_searchbox,
        )
        self.searchbtn.pack(pady=5, padx=15,fill=tk.BOTH, expand=True)
        
    def clear_search(self):
        self.searchbox.delete(0, 'end')

