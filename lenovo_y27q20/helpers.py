from ctypes.wintypes import HANDLE
from typing import Type

from common.constants import VCP_CODES
from common.helpers import get_dict_key_for_value, get_vcp_feature, set_vcp_feature
from lenovo_y27q20.constants import (
    PHYSICAL_MONITOR_DESCRIPTION,
    SELECT_COLOR_PRESET_READ_VALUES,
    SELECT_COLOR_PRESET_WRITE_VALUES,
    VIDEO_GAIN_DRIVE_NIGHT_MODE_BLUE,
    VIDEO_GAIN_DRIVE_NIGHT_MODE_GREEN,
    VIDEO_GAIN_DRIVE_NIGHT_MODE_RED,
)


# Transforms the value read from the VESA MCCS API to the value shown on the OSD (on-screen display) for the red,
# green, and blue video gain drive channels. Uses a simple straight line function with rounding and boundaries. The
# numbers used in the straight line function were found by manipulating the API and observing the OSD.
def _transform_video_gain_drive_from_api_to_osd(value: int) -> int:
    result = round((2.5421052631578958 * value) - 28.16423751686913) # straight line function with rounding
    return 0 if result < 0 else 100 if result > 100 else result # boundaries

# Reports the status of the monitor in a way that matches the OSD (on-screen display).
def report_osd_status(physical_monitor_handle: Type[HANDLE]) -> None:
    print('=' * 40)
    print(PHYSICAL_MONITOR_DESCRIPTION)
    print('.' * 40)
    lum_cur, lum_max = get_vcp_feature(physical_monitor_handle, VCP_CODES['luminance'])
    print(f'Brightness: {lum_cur}/{lum_max}')
    scp_cur, _ = get_vcp_feature(physical_monitor_handle, VCP_CODES['select_color_preset'])
    scp_cur_key = get_dict_key_for_value(SELECT_COLOR_PRESET_READ_VALUES, scp_cur)
    cti_cur, _ = get_vcp_feature(physical_monitor_handle, VCP_CODES['color_temperature_increment']) # hidden from OSD
    ctr_cur, _ = get_vcp_feature(physical_monitor_handle, VCP_CODES['color_temperature_request']) # hidden from OSD
    print(f'Color Temp.: {scp_cur_key} ({3000 + (cti_cur * ctr_cur)}° K)')
    if scp_cur == SELECT_COLOR_PRESET_READ_VALUES['User or sRGB']:
        red_cur, _ = get_vcp_feature(physical_monitor_handle, VCP_CODES['video_gain_drive_red'])
        print(f'    Red:   {_transform_video_gain_drive_from_api_to_osd(red_cur)}/100')
        grn_cur, _ = get_vcp_feature(physical_monitor_handle, VCP_CODES['video_gain_drive_green'])
        print(f'    Green: {_transform_video_gain_drive_from_api_to_osd(grn_cur)}/100')
        blu_cur, _ = get_vcp_feature(physical_monitor_handle, VCP_CODES['video_gain_drive_blue'])
        print(f'    Blue:  {_transform_video_gain_drive_from_api_to_osd(blu_cur)}/100')
    print('=' * 40)

# Sets the monitor to day mode.
def set_day_mode(physical_monitor_handle: Type[HANDLE]) -> None:
    set_vcp_feature(physical_monitor_handle, VCP_CODES['luminance'], 30)
    set_vcp_feature(physical_monitor_handle, VCP_CODES['select_color_preset'], SELECT_COLOR_PRESET_WRITE_VALUES['Warm'])

# Sets the monitor to night mode.
def set_night_mode(physical_monitor_handle: Type[HANDLE]) -> None:
    set_vcp_feature(physical_monitor_handle, VCP_CODES['luminance'], 0)
    set_vcp_feature(physical_monitor_handle, VCP_CODES['select_color_preset'], SELECT_COLOR_PRESET_WRITE_VALUES['User'])
    set_vcp_feature(physical_monitor_handle, VCP_CODES['video_gain_drive_red'], VIDEO_GAIN_DRIVE_NIGHT_MODE_RED)
    set_vcp_feature(physical_monitor_handle, VCP_CODES['video_gain_drive_green'], VIDEO_GAIN_DRIVE_NIGHT_MODE_GREEN)
    set_vcp_feature(physical_monitor_handle, VCP_CODES['video_gain_drive_blue'], VIDEO_GAIN_DRIVE_NIGHT_MODE_BLUE)
