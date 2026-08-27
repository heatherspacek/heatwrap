from __future__ import annotations

from enum import IntEnum

import dearpygui.dearpygui as dpg

from .config import NiceListBoxConfig

# darks
NORD0 = (46, 52, 64)
NORD1 = (59, 66, 82)
NORD2 = (67, 76, 94)
NORD3 = (76, 86, 106)


class SelectionState(IntEnum):
    BASE = 0
    HOVER = 1
    PRIMED = 2
    ACTIVE = 3


class Dropdown: ...


class NiceListBox:
    def __init__(self, parent=None, tag=None, config: NiceListBoxConfig = None):
        if config is None:
            config = NiceListBoxConfig()
        self.config = config
        self.theme_base, self.theme_hovered, self.theme_active = self._setup_themes(
            config
        )

        self.children: list[NiceListItem] = []

        self.tag = tag or dpg.generate_uuid()
        self.parent = parent or None
        self.handler_registry = dpg.add_item_handler_registry()
        self.registry2 = dpg.add_handler_registry()

        self._initial_layout()

    def set_title(self, new_title):
        dpg.set_value("title_text", new_title)

    def register_and_move_child(self, child: NiceListItem):
        self.children.append(child)
        dpg.bind_item_handler_registry(child.tag, self.handler_registry)
        dpg.move_item(child.tag, parent=self.tag)
        self.apply_state_to_child(child, SelectionState.BASE)

    def apply_state_to_child(self, child: NiceListItem, state: SelectionState):
        child.state = state
        dpg.configure_item(child.tag, indent=2 if state==SelectionState.PRIMED else 0)
        match state:
            case SelectionState.BASE:
                dpg.bind_item_theme(child.tag, self.theme_base)
            case SelectionState.HOVER:
                dpg.bind_item_theme(child.tag, self.theme_hovered)
            case SelectionState.ACTIVE | SelectionState.PRIMED:
                dpg.bind_item_theme(child.tag, self.theme_active)

    def _mouse_down(self):
        click_pos = dpg.get_mouse_pos(local=False)
        for c in self.children:
            # TODO: cache these for perf! cache invalidation is the hard part.
            base, size = c.global_extents()
            if (
                base[0] < click_pos[0]
                and base[0] + size[0] >= click_pos[0]
                and base[1] < click_pos[1]
                and base[1] + size[1] >= click_pos[1]
            ):
                for c_other in self.children:
                    self.apply_state_to_child(c_other, SelectionState.BASE)
                self.apply_state_to_child(c, SelectionState.PRIMED)
                break

    def _mouse_move(self):
        mouse = dpg.get_mouse_pos(local=False)
        for c in self.children:
            # TODO: cache these for perf! cache invalidation is the hard part.
            base, size = c.global_extents()
            if (
                base[0] < mouse[0]
                and base[0] + size[0] >= mouse[0]
                and base[1] < mouse[1]
                and base[1] + size[1] >= mouse[1]
            ):
                for c_other in self.children:
                    if c_other.state not in [
                        SelectionState.ACTIVE,
                        SelectionState.PRIMED,
                    ]:
                        self.apply_state_to_child(c_other, SelectionState.BASE)
                if c.state not in [
                    SelectionState.ACTIVE,
                    SelectionState.PRIMED,
                ]:
                    self.apply_state_to_child(c, SelectionState.HOVER)
                break

    def _mouse_up(self):
        mouse = dpg.get_mouse_pos(local=False)
        for c in self.children:
            # TODO: cache these for perf! cache invalidation is the hard part.
            base, size = c.global_extents()
            if (
                base[0] < mouse[0]
                and base[0] + size[0] >= mouse[0]
                and base[1] < mouse[1]
                and base[1] + size[1] >= mouse[1]
            ):
                if c.state == SelectionState.PRIMED:
                    self.apply_state_to_child(c, SelectionState.ACTIVE)
                break

    def _initial_layout(self):
        # dpg.add_item_hover_handler(
        #     parent=self.handler_registry, callback=self._hover_cbk
        # )
        dpg.add_mouse_down_handler(parent=self.registry2, callback=self._mouse_down)
        dpg.add_mouse_release_handler(parent=self.registry2, callback=self._mouse_up)
        dpg.add_mouse_move_handler(parent=self.registry2, callback=self._mouse_move)
        # dpg.add_mouse_drag_handler(parent=self.registry2, callback=None)

        with (
            dpg.child_window(
                parent=self.parent or 0,
                tag=self.tag,
                height=self.config.panel_h,
                width=self.config.panel_w,
                resizable_x=True,
            ),
            dpg.group(horizontal=True),
        ):
            dpg.add_text("[Placeholder Title]", tag="title_text")

    def _setup_themes(self, config: NiceListBoxConfig):
        with dpg.theme() as theme_base, dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, config.base_color)
            dpg.add_theme_color(dpg.mvThemeCol_Border, config.border_color)
        with dpg.theme() as theme_hovered, dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, config.hover_color)
            dpg.add_theme_color(dpg.mvThemeCol_Border, config.border_color)
        with dpg.theme() as theme_active, dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, config.active_color)
            dpg.add_theme_color(dpg.mvThemeCol_Border, config.border_color)
        return theme_base, theme_hovered, theme_active


class NiceListItem:
    """
    Parentless and staged so they can be registered with
    NiceListBox.register_and_move_child.

    ** FOR REUSABILITY, can we make the layout of this generic or
    externally-supplied?
    """

    def __init__(self, tag=None, config: NiceListBoxConfig = None):
        self.tag = tag or dpg.generate_uuid()
        self.config = config or NiceListBoxConfig()
        self.state = SelectionState(0)
        self._initial_layout()

    def _initial_layout(self):
        with dpg.stage():
            with dpg.child_window(
                tag=self.tag, width=self.config.item_w, height=self.config.item_h
            ):
                with dpg.group(horizontal=True):
                    with dpg.group():
                        dpg.add_text("Item description")
                        dpg.add_text("Item date-time")
                    dpg.add_button(label="share...")
                    dpg.add_button(label="X")

    def extents(self):
        base_pos = dpg.get_item_pos(self.tag)
        shape = dpg.get_item_rect_size(self.tag)
        return base_pos, shape

    def global_extents(self):
        shape = dpg.get_item_rect_size(self.tag)

        global_pos = dpg.get_item_pos(self.tag)
        level = self.tag
        while True:
            level = dpg.get_item_parent(level)
            if level is None:
                break
            additional_pos = dpg.get_item_pos(level)
            global_pos = (
                global_pos[0] + additional_pos[0],
                global_pos[1] + additional_pos[1],
            )
        return global_pos, shape

    def selected_callback(): ...
