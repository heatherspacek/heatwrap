import dearpygui.dearpygui as dpg


class Dropdown:
    def __init__(self, parent, tag):
        self.parent = parent
        self.tag = tag

        with dpg.popup(parent=parent, tag=tag):
            dpg.add_button(label="Share...")
            dpg.add_button(label="Copy P1 only")
            dpg.add_button(label="Copy P2 only")
            dpg.add_button(label="Copy both players")


# drop-down button, like for a kebab menu
def add_dropdown(parent, tag) -> Dropdown:
    dr = Dropdown(parent=parent, tag=tag)
    return dr


# better listbox
def add_biglistbox(tag):
    with dpg.group(tag=tag):
        ...
