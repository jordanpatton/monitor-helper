from ctypes import byref, Structure, WinError, WINFUNCTYPE, windll
from ctypes.wintypes import BOOL, BYTE, DWORD, HANDLE, HDC, HMONITOR, LPARAM, LPRECT, WCHAR
from typing import Any, Tuple, Type, Union


# @see https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumdisplaymonitors
_MONITORENUMPROC = WINFUNCTYPE(BOOL, HMONITOR, HDC, LPRECT, LPARAM)

# @see https://learn.microsoft.com/en-us/windows/win32/api/physicalmonitorenumerationapi/ns-physicalmonitorenumerationapi-physical_monitor
class _PHYSICAL_MONITOR(Structure):
    _fields_ = [('hPhysicalMonitor', HANDLE), ('szPhysicalMonitorDescription', WCHAR * 128)]

# Destroys a physical monitor.
# @see https://learn.microsoft.com/en-us/windows/win32/api/physicalmonitorenumerationapi/nf-physicalmonitorenumerationapi-destroyphysicalmonitor
def destroy_physical_monitor(physical_monitor: Type[_PHYSICAL_MONITOR]) -> None:
    if not windll.dxva2.DestroyPhysicalMonitor(physical_monitor.hPhysicalMonitor):
        raise WinError()

# Returns a list of all physical monitors. Every item in the list should be destroyed after use.
# @see https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumdisplaymonitors
# @see https://learn.microsoft.com/en-us/windows/win32/api/physicalmonitorenumerationapi/nf-physicalmonitorenumerationapi-getnumberofphysicalmonitorsfromhmonitor
# @see https://learn.microsoft.com/en-us/windows/win32/api/physicalmonitorenumerationapi/nf-physicalmonitorenumerationapi-getphysicalmonitorsfromhmonitor
def get_all_physical_monitors() -> list[Type[_PHYSICAL_MONITOR]]:
    display_monitors = []
    def callback(hmonitor, hdc, lprect, lparam):
        display_monitors.append(HMONITOR(hmonitor))
        return True
    if not windll.user32.EnumDisplayMonitors(None, None, _MONITORENUMPROC(callback), None):
        raise WinError()
    all_physical_monitors = []
    for dm in display_monitors:
        number_of_physical_monitors = DWORD()
        if not windll.dxva2.GetNumberOfPhysicalMonitorsFromHMONITOR(dm, byref(number_of_physical_monitors)):
            raise WinError()
        physical_monitors = (_PHYSICAL_MONITOR * number_of_physical_monitors.value)()
        if not windll.dxva2.GetPhysicalMonitorsFromHMONITOR(dm, number_of_physical_monitors.value, byref(physical_monitors)):
            raise WinError()
        for pm in physical_monitors:
            all_physical_monitors.append(pm)
    return all_physical_monitors

# Returns the first matching key for a given value in a dictionary. (Ignores subsequent matches.)
def get_dict_key_for_value(dictionary: dict[str, Any], value: Any) -> str:
    return list(dictionary.keys())[list(dictionary.values()).index(value)]

# Returns the current value and maximum value of a VCP feature.
# @see https://learn.microsoft.com/en-us/windows/win32/api/lowlevelmonitorconfigurationapi/nf-lowlevelmonitorconfigurationapi-getvcpfeatureandvcpfeaturereply
def get_vcp_feature(physical_monitor_handle: Type[HANDLE], vcp_code: Type[BYTE]) -> Tuple[int, int]:
    current_value = DWORD()
    maximum_value = DWORD()
    if not windll.dxva2.GetVCPFeatureAndVCPFeatureReply(
        physical_monitor_handle,
        vcp_code,
        None,
        byref(current_value),
        byref(maximum_value)
    ):
        raise WinError()
    return current_value.value, maximum_value.value

# Sets the value of a VCP feature.
# @see https://learn.microsoft.com/en-us/windows/win32/api/lowlevelmonitorconfigurationapi/nf-lowlevelmonitorconfigurationapi-setvcpfeature
def set_vcp_feature(physical_monitor_handle: Type[HANDLE], vcp_code: Type[BYTE], value: Union[int, Type[BYTE]]) -> None:
    if not windll.dxva2.SetVCPFeature(physical_monitor_handle, vcp_code, DWORD(value)):
        raise WinError()
