from ctypes.wintypes import BYTE
from typing import Type


# VESA Monitor Control Command Set Standard: Table 8-3: Image Adjustment VCP Code Cross-reference.
# @see https://milek7.pl/ddcbacklight/mccs.pdf
VCP_CODES: dict[str, Type[BYTE]] = {
    'color_temperature_increment': 0x0B,
    'color_temperature_request': 0x0C,
    'luminance': 0x10,
    'select_color_preset': 0x14,
    'video_gain_drive_red': 0x16,
    'video_gain_drive_green': 0x18,
    'video_gain_drive_blue': 0x1A,
}
