from ctypes.wintypes import BYTE
from typing import Type, Union

PHYSICAL_MONITOR_DESCRIPTION: str = 'LEN Y27q-20'

# For some bizarre reason, the monitor reports entirely different values than what you write to it.
# Note that sRGB mode is a toggle, and it doesn't change the actively-reported color preset. As a
# result it's impossible to know when sRGB is enabled via the reported color preset EVEN THOUGH you
# activate it by writing a color preset value. *shrugs*
SELECT_COLOR_PRESET_READ_VALUES: dict[str, Type[BYTE]] = {
    'User or sRGB': 0x04,
    'Cool or sRGB': 0x05,
    'Normal or sRGB': 0x06,
    'Warm or sRGB': 0x08,
}

# Values specific to the Lenovo Y27q-20 monitor. It does not follow the MCCS color preset codes.
# (See VESA Monitor Control Command Set Standard: Table 8-4: Image Adjustment VCP Codes.)
# @see https://support.lenovo.com/us/en/solutions/pd500310-lenovo-y27q-20-monitor-overview
SELECT_COLOR_PRESET_WRITE_VALUES: dict[str, Type[BYTE]] = {
    'sRGB': 0x01, # minimum value
    # 0x02 and 0x03 close the OSD, but they don't appear to apply any changes
    'Warm': 0x04,
    'Normal': 0x06, # 0x05, 0x06, and 0x07 apply Normal
    'Cool': 0x09, # 0x08, 0x09, 0x0A apply Cool
    'User': 0x0B, # maximum value
}

# Displayed as 20/100 on monitor. This is the ideal value.
VIDEO_GAIN_DRIVE_NIGHT_MODE_BLUE: int = 19

# Displayed as 99/100 on monitor. Ideal value is 100/100, but it isn't programmatically possible.
VIDEO_GAIN_DRIVE_NIGHT_MODE_GREEN: int = 50

# Displayed as 99/100 on monitor. Ideal value is 100/100, but it isn't programmatically possible.
VIDEO_GAIN_DRIVE_NIGHT_MODE_RED: int = 50
