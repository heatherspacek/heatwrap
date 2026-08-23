import dearpygui.dearpygui as dpg

from .config import NiceListBoxConfig

# darks
NORD0 = (46, 52, 64)
NORD1 = (59, 66, 82)
NORD2 = (67, 76, 94)
NORD3 = (76, 86, 106)


class Dropdown: ...


class NiceListBox:
    def __init__(self, parent=None, tag=None, config: NiceListBoxConfig = None):
        if config is None:
            config = NiceListBoxConfig()
        self.config = config
        self.theme_base = ...
        self.theme_hovered = ...
        self.theme_active = ...

        self.focused_i = None
        self.children: list[NiceListItem] = []

        self.tag = tag or dpg.generate_uuid()
        self.parent = parent or None
        self.handler_registry = dpg.item_handler_registry()

        self._initial_layout()

    def _propagate_hover(self, _, item):
        print(dpg.get_item_info(item))

    def _propagate_click(self, _, item):
        print(dpg.get_item_info(item))

    def _initial_layout(self):
        with self.handler_registry:
            dpg.add_item_hover_handler(callback=self._propagate_hover)
            dpg.add_item_clicked_handler(callback=self._propagate_click)
        with dpg.child_window(
            parent=self.parent or 0,
            tag=self.tag,
            height=self.config.panel_h,
            width=self.config.panel_w,
        ):
            pass

    def _register_themes(self):
        with dpg.theme(tag="theme_base"), dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, NORD0)
        dpg.bind_theme("theme_base")  # global
        with dpg.theme(tag="theme_hovered"), dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, NORD2)


class NiceListItem:
    def selected_callback(): ...
