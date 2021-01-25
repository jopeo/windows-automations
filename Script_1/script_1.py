#! /usr/bin/env python

import sys
import datetime as dt
import getpass
import pytz
from os import path
from winevt import EventLog
from collections import OrderedDict
from maint_funcs import sloppy_copy
from consts import *


def cpy_dot_ankiaddon_to_g(nm_path):
    # fixme: copies but the printout isnt quite right?
    head, tail = path.split(nm_path)
    dest = path.join(f'F://yourpath', tail)
    x = dest.find('~')
    if x == -1:
        sloppy_copy(f'{nm_path}', dest)
    else:
        popped = dest[:(x)] + dest[x+1:]
    return


def cpy_addon_to_anki():
    sloppy_copy(r"F://yourpath", r'F://yourpath',
                ignore_glob={'*.json', '*.yourfile'})
    return


def cpy_addon_to_g():
    sfx = dt.datetime.strftime(dt.datetime.today(), (' %m.%d.%Y-%I-%M-%S%p'))
    prfx = r"F://yourpath"
    dest = prfx + sfx
    sloppy_copy(r"F://yourpath", f"{dest}")
    return


def GUIs_to_g():
    #fixme: copied correctly but .ui files show up as 'folders ignored' even when copied
    sloppy_copy(r'F://yourpath', r'F://yourpath')
    return


def fx_to_g():
    sloppy_copy(r"F://yourpath", r"F://yourpath",
                ignore_glob={'__pycache__*', '*.idea'})
    return


def cpy_Script_1_to_g():
    sloppy_copy('F://yourpath', 'F://yourpath',
                ignore_glob={'__pycache__*'})
    return


def check_times(evt_tm: dt.time, s: int):
    now = dt.datetime.now(dt.timezone.utc)  # should be UTC
    if now - evt_tm < dt.timedelta(seconds=s):
        return True
    else:
        return False


def untangle_2_dict(event):

    def join_attis(evnt):
        lst = [(getattr(evnt.System, atri), atri) for atri in dir(evnt.System)]
        return lst  # returns list of tuples

    edic = dict()
    edat = list(tuple())
    edat.extend([('EventID', event.EventID), ('Level', event.Level), ('LevelStr', event.LevelStr)])

    first = join_attis(event)  # 'first' is a list of tuples
    for x in first:
        elem = x[0]
        nm = x[1]
        cdat = None
        try:
            cdat = x[0].cdata
            if len(cdat) > 0:
                edat.append((f"{nm}", cdat))

            elif len(cdat) == 0 and elem.__dict__['_attributes'].items():
                sfx = True
                for (k, v) in elem.__dict__['_attributes'].items():
                    if sfx:
                        edat.append((f'{nm} {k}', v))
                        sfx = False
                    else:
                        edat.append((f'{k}', v))
                else:
                    cdat = 'None'
                    edat.append((f"{nm}", cdat))
        except Exception as ep:
            print(f'Exception raised:\n{ep}')

    edat.extend([(f"{item['Name']}", item.cdata) for item in event.EventData.Data])

    tm_str = event.System.TimeCreated['SystemTime']
    tm_str = tm_str[:-2] + tm_str[-1:]
    tm_obj = dt.datetime.strptime(tm_str, ('%Y-%m-%dT%H:%M:%S.%f%z'))
    tz = pytz.timezone('US/central')
    tm_cst = tm_obj.astimezone(tz)
    edic = dict(edat)
    edic['TimeCreated SystemTime'] = tm_obj
    edic['Time as local CTime'] = dt.datetime.ctime(tm_cst)

    return edic


if __name__ == '__main__':

    try:
        query = EventLog.Query(log_path, xpath, direction="backward")
        event = next(query, None)
        ed = untangle_2_dict(event)
    except Exception as exc:
        print(exc)

    if check_times(ed['TimeCreated SystemTime'], 2):  # event must be within in %d seconds

        ef = ed['ObjectName']

        if r'F://yourpath' in ef and r'F://yourpath' in ef and r'F://yourpath' in ef:
            cpy_dot_ankiaddon_to_g(ef)
        elif r'F://yourpath' in ef:
            cpy_addon_to_anki()
            cpy_addon_to_g()
        elif r'F://yourpath' in ef:
            GUIs_to_g()
        elif r'F://yourpath' in ef:
            fx_to_g()
        elif r'F://yourpath' in ef:
            cpy_Script_1_to_g()
