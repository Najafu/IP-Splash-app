import itertools

import network
from model import Model
from view import TkView

toggle_sorting_mode = itertools.cycle(["ASC", "DESC"]).__next__


class Controller:
    def __init__(self, model, view) -> None:
        self.model = model
        self.view = view

    def start(self):
        self.view.setup(self)
        self.view.start_main_loop()

    def handle_click_treeview_header_to_sort(self, order_by, event=None):
        search_value = self.view.searchbar.searchbox.get()
        if search_value and event:
            values = self.model.fetch_filtered_data((order_by, "ASC"), search_value)
        else:
            values = self.model.fetch_filtered_data(
                (order_by, toggle_sorting_mode()), search_value
            )
        if values:
            self.view.tree.populate(values)
        else:
            self.view.tree.clear_all_tree()

    def handle_click_clear_searchbox(self, e=None):
        self.view.searchbar.clear_search()
        self.handle_to_populate_treeview()

    def handle_to_populate_treeview(self):
        values = self.model.fetch_all_data()
        if values:
            self.view.tree.populate(values)

    def handle_populate_entrybox_from_tree(self, e):
        data = self.view.tree.get_selected_item_from_tree(all_row_data=True)
        self.view.populate_entrybox_from_tree(data)

    def handle_load_devices_on_compobox(self):
        values = network.find_net_device()
        self.view.tabmenu.actions.load_devices(values)

    def handle_click_save(self):
        values = self.view.insert_to_tree()
        if values:
            self.model.insert(values)
            self.view.clear_entrybox()
            self.view.statusbar.update("New entry created.")
            self.handle_to_populate_treeview()

    def handle_click_delete(self):
        item_id, selected_item = self.view.tree.get_selected_item_from_tree(
            action_name="delete"
        )
        if selected_item:
            self.view.tree.delete_from_tree(selected_item)
            self.model.delete(item_id)
            self.view.clear_entrybox()
            self.view.statusbar.update(f"Entry id:{item_id} deleted.")

    def handle_click_edit(self):
        item_id, selected_item = self.view.tree.get_selected_item_from_tree(
            action_name="edit"
        )
        if selected_item:
            values = self.view.update_from_tree()
            if values:
                values.append(item_id)
                self.model.update(values)
                self.view.clear_entrybox()
                self.view.statusbar.update(f"Entry id:{item_id} updated.")
                self.handle_to_populate_treeview()

    def handle_entry_box_switch(self):
        self.view.entry_box_switch()

    def handle_click_dns_static(self):
        values = self.view.change_dns(state=True)
        if not values:
            return
        is_executed = network.change_to_staticdns(*values)
        if is_executed:
            self.view.statusbar.update(f"DNS has change on adapter:{values[0]}.")
            self.handle_clear_dns_entry()
        else:
            self.view.statusbar.update(
                "Command error: DNS has not change!", error_flag=True
            )

    def handle_click_dns_dhcp(self):
        self.handle_clear_dns_entry()
        values = self.view.change_dns(state=False)
        if not values:
            return
        is_executed = network.change_dns_to_dhcp(values)
        if is_executed:
            self.view.statusbar.update(f"DNS for {values[0]} has change on DHCP.")
        else:
            self.view.statusbar.update(
                f"Command error: DNS for {values[0]} has not change on DHCP!",
                error_flag=True,
            )

    def handle_clear_dns_entry(self):
        self.view.tabmenu.dns.dns_ip_entry.select_range(0, "end")
        self.view.tabmenu.dns.dns_ip_entry.delete(0, "end")

    def handle_click_change(self):
        values = self.view.change_ip()
        if not values:
            return

        if self.view.tabmenu.actions.get_radiobutton_selection:
            is_executed = network.change_to_staticip(*values)
            if is_executed:
                self.view.statusbar.update(f"ip has change on adapter:{values[0]}.")
            else:
                self.view.statusbar.update(
                    "Command error: ip has not change!", error_flag=True
                )
        else:
            is_executed = network.change_to_dhcp(values)
            if is_executed:
                self.view.statusbar.update(f"{values[0]} has change on DHCP.")
            else:
                self.view.statusbar.update(
                    f"Command error: {values[0]} has not change on DHCP!",
                    error_flag=True,
                )
        self.view.clear_entrybox()

    def handle_click_renew(self):
        is_executed = network.renew_ip()
        if is_executed:
            self.view.statusbar.update("Renew was successful.")
        else:
            self.view.statusbar.update(
                "Command error: Renew failed!",
                error_flag=True,
            )
