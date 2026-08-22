import dearpygui.dearpygui as dpg

_n_apps = 0


class WrApp:
    def __init__(self):
        global _n_apps
        _n_apps += 1
        if _n_apps > 1:
            raise RuntimeError("Only one app instance is supported.")


def init():
    dpg.create_context()
    dpg.create_viewport()
    dpg.setup_dearpygui()


def app_loop(user_frame_fcn):
    dpg.show_viewport()
    try:
        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()
            user_frame_fcn()
    finally:
        dpg.destroy_context()
        dpg.stop_dearpygui()
