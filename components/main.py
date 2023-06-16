import tkinter as tk
from tkinter import messagebox, ttk


class Main(tk.Frame):
    def __init__(self, parent, controller=None, *args, **kargs):
        tk.Frame.__init__(self, parent, *args, **kargs)

        columns = ("name", "ip_address", "subnet_mask", "gateway", "id")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        self.tree.column("name", width=160, minwidth=60)
        self.tree.column("ip_address", width=90, minwidth=90)
        self.tree.column("subnet_mask", width=90, minwidth=90)
        self.tree.column("gateway", width=90, minwidth=90)
        self.tree.column("id", width=30, minwidth=30, anchor="center")

        self.tree.heading(
            "name",
            text="NAME",
            command=lambda: controller.handle_click_treeview_header_to_sort(order_by="name"),
        )
        self.tree.heading(
            "ip_address",
            text="IP",
            command=lambda: controller.handle_click_treeview_header_to_sort(
                order_by="ip_address"
            ),
        )
        self.tree.heading(
            "subnet_mask",
            text="MASK",
            command=lambda: controller.handle_click_treeview_header_to_sort(
                order_by="subnet_mask"
            ),
        )
        self.tree.heading(
            "gateway",
            text="GATEWAY",
            command=lambda: controller.handle_click_treeview_header_to_sort(order_by="gateway"),
        )
        self.tree.heading(
            "id",
            text="ID",
            command=lambda: controller.handle_click_treeview_header_to_sort(order_by="id"),
        )

        self.tree.pack(side="left")
        self.tree.bind(
            "<Double-Button-1>", controller.handle_populate_entrybox_from_tree
        )

        verscrlbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        verscrlbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=verscrlbar.set)

    def populate(self, values):
        self.tree.delete(*self.tree.get_children())
        for value in values:
            self.tree.insert("", tk.END, values=value)

    def get_selected_item_from_tree(self, action_name=None, all_row_data=False):
        selected_item = None
        item_id = None

        if all_row_data:
            selected_item = self.tree.focus()
            selected_item = self.tree.item(selected_item, "values")
            return selected_item

        try:
            selected_item = self.tree.selection()[0]
            item_id = str(self.tree.item(selected_item)["values"][4])
            return (item_id, selected_item)

        except IndexError:
            messagebox.showerror(
                "Something went wrong!",
                f"Error: while trying to {action_name} data!\nYou must select a row to {action_name}.",
            )
            return ("", False)

    def delete_from_tree(self, item):
        self.tree.delete(item)

    def clear_all_tree(self):
        self.tree.delete(*self.tree.get_children())
