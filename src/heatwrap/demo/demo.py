import dearpygui.dearpygui as dpg

from ..scaffolding import app_init, app_loop, WrApp


def frame_loop():
    fxx = dpg.get_frame_count()
    if fxx % 60 == 0:
        print(fxx)


def layout():
    with dpg.window():
        dpg.add_text("hello world?!")


def demo_application():
    app_init()

    layout()

    app_loop(frame_loop)
