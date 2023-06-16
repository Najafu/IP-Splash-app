import tkinter as tk
from tkinter import ttk

import network
from components.IPEntry import IPEntry


class TabMenu(tk.Frame):
    def __init__(self, parent, controller=None, *args, **kargs):
        tk.Frame.__init__(self, parent, *args, **kargs)

        # GUI setup tab menu.
        self.tabcontrol = ttk.Notebook(self, height=120)
        # tab 1
        self.tab1 = ttk.Frame(self.tabcontrol, padding=10)
        self.tabcontrol.add(self.tab1, text="Actions", sticky="nsew")
        # tab 2
        self.tab2 = ttk.Frame(self.tabcontrol, padding=10)
        self.tabcontrol.add(self.tab2, text="Persistence")
        # tab 3
        self.tab3 = ttk.Frame(self.tabcontrol, padding=10)
        self.tabcontrol.add(self.tab3, text="DNS")
        # pack tabed menu
        self.tabcontrol.pack(expand=1, fill="both", padx=5, pady=5)

        self.actions = TabOne(self.tab1, controller)
        self.persistence = TabTwo(self.tab2, controller)
        self.dns = TabThree(self.tab3, controller)

        self.actions.pack(anchor="center")
        self.persistence.pack(anchor="center")
        self.dns.pack(anchor="center")


class TabOne(tk.Frame):
    """TAB 1 Menu area setup."""

    def __init__(self, parent, controller=None, *args, **kargs):
        tk.Frame.__init__(self, parent, *args, **kargs)

        # Combobox
        self.adapter_combo = DeviceWidget(self)
          
        # Radio button
        self.radio_var = tk.IntVar()
        self.radio_var.set(1)
        self.change_static_button = ttk.Radiobutton(
            self,
            text="Static",
            variable=self.radio_var,
            value=1,
            command=controller.handle_entry_box_switch,
        )
        self.change_dynamic_button = ttk.Radiobutton(
            self,
            text="Dynamic",
            variable=self.radio_var,
            value=0,
            command=controller.handle_entry_box_switch,
        )
        self.command_button = ttk.Button(
            self, text="Change", command=controller.handle_click_change
        )
        self.renew_button = ttk.Button(
            self, text="IP Renew", command=controller.handle_click_renew
        )

        self.adapter_combo.grid(row=0, column=1, columnspan=3)
        self.change_static_button.grid(row=1, column=1, sticky="w")
        self.change_dynamic_button.grid(row=2, column=1, sticky="w")
        self.command_button.grid(row=1, column=2, rowspan=2, ipadx=36, sticky=(tk.E,tk.N,tk.S))
        self.renew_button.grid(row=1, column=3, rowspan=2, sticky=(tk.N,tk.S))

    @property
    def get_radiobutton_selection(self):
        return bool(self.radio_var.get())


class TabTwo(tk.Frame):
    """TAB 2 Menu area setup."""

    def __init__(self, parent, controller=None, *args, **kargs):
        tk.Frame.__init__(self, parent, *args, **kargs)

        lbp = ttk.Label(self, text="Name:")
        self.name_entrybox = tk.Entry(self, name="description_name")
        self.savebutton = ttk.Button(
            self, text="Save", command=controller.handle_click_save
        )
        self.deletbutton = ttk.Button(
            self, text="Delete", command=controller.handle_click_delete
        )
        self.editbutton = ttk.Button(
            self, text="Edit", command=controller.handle_click_edit
        )

        lbp.grid(row=0, column=0)
        self.name_entrybox.grid(row=0, column=1, columnspan=2, pady=15, sticky=(tk.W, tk.E))
        self.savebutton.grid(row=1, column=0)
        self.deletbutton.grid(row=1, column=1, padx=5)
        self.editbutton.grid(row=1, column=2)


class TabThree(tk.Frame):
    """TAB 3 Menu area setup."""

    def __init__(self, parent, controller=None, *args, **kargs):
        tk.Frame.__init__(self, parent, *args, **kargs)

        self.dns_combobox = DeviceWidget(self)
        lb = tk.Label(self, text="DNS ip:")
        self.dns_ip_entry = IPEntry(self, name="dns_ip")
        self.dns_button = ttk.Button(self, text="SET", command=controller.handle_click_dns_static)
        self.dns_dhcp_button = ttk.Button(self, text="DHCP", command=controller.handle_click_dns_dhcp)
        
        self.dns_combobox.grid(row=0, column=1, columnspan=3, sticky="e")
        lb.grid(row=1, column=1, sticky="w")
        self.dns_ip_entry.grid(row=1, column=2, ipadx=25 ,padx=5, sticky=(tk.W, tk.E))
        self.dns_button.grid(row=1, column=3, sticky=(tk.W))
        self.dns_dhcp_button.grid(row=2, column=3, sticky=(tk.W), pady=5)



class DeviceWidget(tk.Frame):

    def __init__(self, parent, *args, **kargs):
        tk.Frame.__init__(self, parent, *args, **kargs)
   
        ttk.Label(self, text="Adapter device:").grid(row=0, column=0, ipadx=3)
        self.device_combobox = ttk.Combobox(self, name="adapter_name", values=["Loading..."])
        self.device_combobox.current(0)
        self.reload_combobox = ttk.Button(self,text="Reload", command=self.__load_devices)
        
        self.device_combobox.grid(row=0, column=1)
        self.reload_combobox.grid(row=0, column=2, padx=5, pady=10)

        self.__load_devices()

    def __load_devices(self):
        values = network.find_net_device()
        self.device_combobox["values"] = values
        self.device_combobox.current(0)

    def get(self):
        return self.device_combobox.get()

