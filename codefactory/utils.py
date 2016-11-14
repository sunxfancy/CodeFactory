#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess, platform, sys

def askYesNo(message, no_default=True):
    ask = no_default if "[y/N]:" else "[Y/n]:"
    msg = input(message, ask)
    if no_default:
        if (msg[0] == 'y' or msg[0] == 'Y'):
            return True
        return False
    else:
        if (msg[0] == 'n' or msg[0] == 'N'):
            return False
        return True

def askDefault(message, default):
    msg = input(message + '[' + default + ']:')
    if msg == '':
        return default
    return msg

def map_buildsystem(name):
    opt = {'ninja': 'Ninja',
           'xcode': 'Xcode',
           'makefile': 'Unix Makefiles',
           'makefile-msys': 'MSYS Makefiles',
           'makefile-mingw': 'MinGW Makefiles',
           'makefile-nmake': 'NMake Makefiles',
           'vs2008': 'Visual Studio 9 2008',
           'vs2010': 'Visual Studio 10 2010',
           'vs2012': 'Visual Studio 11 2012',
           'vs2013': 'Visual Studio 12 2013',
           'vs2015': 'Visual Studio 14 2015'}
    return opt[name]

def get_allowed_buildsystem():
    if platform.system() == 'Windows':
        return ['ninja', 'makefile-msys', 'makefile-mingw', 'makefile-nmake',
                'vs2008', 'vs2010', 'vs2012', 'vs2013', 'vs2015']
    if platform.system() == 'Linux':
        return ['ninja', 'makefile']
    if platform.system() == 'Darwin':
        return ['ninja', 'xcode', 'makefile']
    return []

def run(*args):
    # print(*args)
    return subprocess.check_call(list(args))

def run_limited(*args):
    try:
        msg = subprocess.check_output(list(args))
        return 0, msg.split(b'\n')[0].decode(sys.stdout.encoding)
    except subprocess.CalledProcessError as e:
        return e.returncode, e.output.decode(sys.stdout.encoding)
