from sys import argv

import lenovo_y27q20.constants
import lenovo_y27q20.helpers
from common.helpers import destroy_physical_monitor, get_all_physical_monitors


if __name__ == '__main__':
    if len(argv[1:]) == 0:
        print('error: missing argument')
    elif len(argv[1:]) > 1:
        print('error: more than one argument')
    elif argv[1] == 'lenovo_y27q20_report_osd_status':
        for pm in get_all_physical_monitors():
            if pm.szPhysicalMonitorDescription == lenovo_y27q20.constants.PHYSICAL_MONITOR_DESCRIPTION:
                lenovo_y27q20.helpers.report_osd_status(pm.hPhysicalMonitor)
            destroy_physical_monitor(pm)
    elif argv[1] == 'lenovo_y27q20_set_day_mode':
        for pm in get_all_physical_monitors():
            if pm.szPhysicalMonitorDescription == lenovo_y27q20.constants.PHYSICAL_MONITOR_DESCRIPTION:
                lenovo_y27q20.helpers.set_day_mode(pm.hPhysicalMonitor)
            destroy_physical_monitor(pm)
    elif argv[1] == 'lenovo_y27q20_set_night_mode':
        for pm in get_all_physical_monitors():
            if pm.szPhysicalMonitorDescription == lenovo_y27q20.constants.PHYSICAL_MONITOR_DESCRIPTION:
                lenovo_y27q20.helpers.set_night_mode(pm.hPhysicalMonitor)
            destroy_physical_monitor(pm)
    else:
        print(f'error: invalid argument: {argv[1]}')
