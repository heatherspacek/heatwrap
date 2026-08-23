import dearpygui.dearpygui as dpg

from .config import NiceListBoxConfig


class Dropdown: ...


class NiceListBox:
    def __init__(self, parent, tag, config: NiceListBoxConfig = None):
        if config is None:
            config = NiceListBoxConfig()
        self.theme_base = ...
        self.theme_hovered = ...
        self.theme_active = ...
