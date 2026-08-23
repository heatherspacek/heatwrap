from dataclasses import dataclass


@dataclass
class NiceListBoxConfig:
    base_color: tuple[int] = (46, 52, 64)
    hover_color: tuple[int] = (59, 66, 82)
    active_color: tuple[int] = (67, 76, 94)
    border_color: tuple[int] = (76, 86, 106)
    panel_w: int = 250
    panel_h: int = -1
    item_w: int = -1
    item_h: int = 60
