import ipaddress
from tkinter import Entry


class IPEntry(Entry):
    def __init__(self, parent, **kargs):
        default_kargs = {"justify": "center"}
        kargs = {**default_kargs, **kargs}
        Entry.__init__(self, parent, **kargs)

        vcmd = (parent.register(self.validate_input), "%P", "%d")

        self.config(
            highlightbackground="SystemButtonFace",
            highlightcolor="SystemWindowFrame",
            validate="key",
            validatecommand=vcmd,
            highlightthickness=1,
        )

        self.bind("<FocusOut>", self.is_valid_ip)

    def validate_input(self, chars, acttyp):
        if acttyp == "1":  # insert
            count = 0
            for char in chars:
                if char == ".":
                    count += 1
                if not chars[0].isdigit():
                    return False
                if len(chars) >= 16:
                    return False
                if not (char.isdigit() or (char == "." and count <= 3)):
                    return False
            return True
        else:
            self.after_idle(lambda: self.configure(validate="key"))
            if self.select_present():
                start_indx = self.index("sel.first")
                end_indx = self.index("sel.last")
                self.delete(start_indx, end_indx)
            else:
                self.delete(self.index("insert") - 1)

    def is_valid_ip(self, inc_event=None):
        if len(self.get()) == 0:
            self.config(
                highlightbackground="SystemButtonFace",
                highlightcolor="SystemWindowFrame",
            )
            return False
        else:
            try:
                _ = ipaddress.ip_address(self.get())
                self.config(
                    highlightbackground="SystemButtonFace",
                    highlightcolor="SystemWindowFrame",
                )
                return True
            except ValueError:
                self.config(highlightbackground="red", highlightcolor="red")
                return False
