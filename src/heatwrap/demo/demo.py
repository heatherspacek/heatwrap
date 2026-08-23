import dearpygui.dearpygui as dpg

from ..scaffolding import app_init, app_loop, WrApp
from ..widgets import NiceListBox, NiceListItem


def frame_loop():
    fxx = dpg.get_frame_count()
    if fxx % 60 == 0:
        print(fxx)


def layout():

    with dpg.viewport_menu_bar():
        dpg.add_text("could this be a status bar?")
    with dpg.window(tag="main_win"):
        dpg.add_menu_bar()
        N = NiceListBox()
        for _ in range(10):
            I = NiceListItem()
            N.register_and_move_child(I)
    dpg.set_primary_window("main_win", True)


def demo_application():
    app_init()

    layout()

    app_loop(frame_loop)
