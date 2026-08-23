import dearpygui.dearpygui as dpg

from ..scaffolding import app_init, app_loop, WrApp
from ..widgets import NiceListBox


def frame_loop():
    fxx = dpg.get_frame_count()
    if fxx % 60 == 0:
        print(fxx)


def highlight(_, item):
    dpg.configure_item(item, indent=10)
    dpg.bind_item_theme(item, "theme_hovered")


def layout():

    with dpg.item_handler_registry(tag="handler1"):
        dpg.add_item_hover_handler(callback=highlight)

    # darks
    NORD0 = (46, 52, 64)
    NORD1 = (59, 66, 82)
    NORD2 = (67, 76, 94)
    NORD3 = (76, 86, 106)

    def add_entry(tag):
        with dpg.child_window(tag=tag, height=55, width=235):
            with dpg.group(horizontal=True):
                # dpg.add_image("")
                dpg.add_text("Label... and ")
                dpg.add_button(label="dropdown...")

        dpg.bind_item_handler_registry(tag, "handler1")

    with dpg.window(tag="main_win"):
        dpg.add_menu_bar()
        NiceListBox()
    dpg.set_primary_window("main_win", True)


def demo_application():
    app_init()

    layout()

    app_loop(frame_loop)
