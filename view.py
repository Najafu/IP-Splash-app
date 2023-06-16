import tkinter as tk
from tkinter import messagebox, ttk

import ico
from components import Center, Main, SearchBar, StatusBar, TabMenu
from components.IPEntry import IPEntry


class TkView:
    def setup(self, controller) -> None:
        # setup tkinter.
        self.master = tk.Tk()
        try:
            self.master.iconbitmap(default=ico.use_ico())
        except Exception:
            self.master.iconbitmap(default=None)
        self.master.title("IPSplash - ip manager by PHR")
        self.master.resizable(False, False)

        style = ttk.Style()
        current_theme = style.theme_use()
        style.theme_settings(
            current_theme, {"TNotebook.Tab": {"configure": {"padding": [20, 5]}}}
        )

        self.tree = Main(self.master, controller)
        self.center = Center(self.master, controller)
        self.tabmenu = TabMenu(self.master, controller)
        self.statusbar = StatusBar(self.master, controller)
        self.searchbar = SearchBar(self.master, controller)

        self.searchbar.pack(fill="x", padx=5)
        self.tree.pack()
        self.center.pack(pady=10)
        self.tabmenu.pack(fill="x", padx=5)
        self.statusbar.pack(side="right", padx="20")

        controller.handle_to_populate_treeview()
        #self.master.after_idle(controller.handle_load_devices_on_compobox)

    def start_main_loop(self):
        self.master.mainloop()

    def populate_entrybox_from_tree(self, current_item):
        self.clear_entrybox()
        wgs = [
            self.tabmenu.persistence.name_entrybox,
            self.center.ip_entrybox,
            self.center.mask_entrybox,
            self.center.gateway_entrybox,
        ]

        if current_item:
            for idx, wg in enumerate(wgs):
                wg.insert(0, current_item[idx])
                wg.focus()
        self.tree.focus_force()

    def clear_entrybox(self):
        wgs = [
            self.tabmenu.persistence.name_entrybox,
            self.center.ip_entrybox,
            self.center.mask_entrybox,
            self.center.gateway_entrybox,
        ]
        for wg in wgs:
            wg.select_range(0, "end")
            wg.delete(0, "end")

    def _validate_wgts_input(self, validation_info, wgts_list):
        valid_values = []
        for wgt in wgts_list:
            temp_wgt_data = wgt.get()
            wgt_name = str(wgt).split(".")[-1].replace("_", " ")
            if len(temp_wgt_data) == 0:
                messagebox.showwarning(
                    validation_info,
                    f"{wgt_name.capitalize()} field can not be empty!\nPlease enter a value.",
                )
                return False
            if isinstance(wgt, IPEntry):
                if not wgt.is_valid_ip():
                    messagebox.showwarning(
                        validation_info,
                        f"Please enter a valid {wgt_name}",
                    )
                    return False
            valid_values.append(temp_wgt_data)
        return valid_values

    def entry_box_switch(self):
        switch = "normal"

        if not self.tabmenu.actions.get_radiobutton_selection:
            self.clear_entrybox()
            switch = "disabled"

        self.center.ip_entrybox.config(state=switch)
        self.center.mask_entrybox.config(state=switch)
        self.center.gateway_entrybox.config(state=switch)

    def change_ip(self):
        # static
        if self.tabmenu.actions.get_radiobutton_selection:
            wigt_list = [
                self.tabmenu.actions.adapter_combo,
                self.center.ip_entrybox,
                self.center.mask_entrybox,
                self.center.gateway_entrybox,
            ]
        else:
            # dynamic
            wigt_list = [self.tabmenu.actions.adapter_combo]

        return self._validate_wgts_input(
            "IP: Something went wrong while changing ip!", wigt_list
        )

    def change_dns(self, state):
        # static
        if state:
            wigt_list = [
                self.tabmenu.dns.dns_combobox,
                self.tabmenu.dns.dns_ip_entry,
            ]
        else:
            # dynamic
            wigt_list = [self.tabmenu.dns.dns_combobox]

        return self._validate_wgts_input(
            "DNS: Something went wrong while changing DNS!", wigt_list
        )

    def insert_to_tree(self):
        return self._validate_wgts_input(
            "Something went wrong while saving data!",
            [
                self.tabmenu.persistence.name_entrybox,
                self.center.ip_entrybox,
                self.center.mask_entrybox,
                self.center.gateway_entrybox,
            ],
        )

    def update_from_tree(self):
        return self._validate_wgts_input(
            "Something went wrong while editing data!",
            [
                self.tabmenu.persistence.name_entrybox,
                self.center.ip_entrybox,
                self.center.mask_entrybox,
                self.center.gateway_entrybox,
            ],
        )
