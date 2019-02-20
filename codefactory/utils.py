#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Sun Xiaofan <sxf>
# @Date:   2016-11-15
# @Email:  sunxfancy@gmail.com
# @Last modified by:   sxf
# @Last modified time: 2016-11-15
# @License: MIT License

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
           'make': 'Unix Makefiles',
           'msys': 'MSYS Makefiles',
           'mingw': 'MinGW Makefiles',
           'nmake': 'NMake Makefiles',
           'vs2008': 'Visual Studio 9 2008 Win64',
           'vs2010': 'Visual Studio 10 2010 Win64',
           'vs2012': 'Visual Studio 11 2012 Win64',
           'vs2013': 'Visual Studio 12 2013 Win64',
           'vs2015': 'Visual Studio 14 2015 Win64',
           'vs2017': 'Visual Studio 15 2017 Win64',
           'vs2008-x86': 'Visual Studio 9 2008',
           'vs2010-x86': 'Visual Studio 10 2010',
           'vs2012-x86': 'Visual Studio 11 2012',
           'vs2013-x86': 'Visual Studio 12 2013',
           'vs2015-x86': 'Visual Studio 14 2015',
           'vs2017-x86': 'Visual Studio 15 2017',
           'vs2008-arm': 'Visual Studio 9 2008 ARM',
           'vs2010-arm': 'Visual Studio 10 2010 ARM',
           'vs2012-arm': 'Visual Studio 11 2012 ARM',
           'vs2013-arm': 'Visual Studio 12 2013 ARM',
           'vs2015-arm': 'Visual Studio 14 2015 ARM',
           'vs2017-arm': 'Visual Studio 15 2017 ARM'}
    return opt[name]

def get_allowed_buildsystem():
    if platform.system() == 'Windows':
        return ['default', 'ninja', 'msys', 'mingw', 'nmake',
                'vs2008', 'vs2010', 'vs2012', 'vs2013', 'vs2015']
    if platform.system() == 'Linux':
        return ['default', 'ninja', 'make']
    if platform.system() == 'Darwin':
        return ['default', 'ninja', 'xcode', 'make']
    return []

def run(*args):
    print(*args)
    return subprocess.check_call(list(args))

def run_limited(*args):
    try:
        msg = subprocess.check_output(list(args))
        return 0, msg.split(b'\n')[0].decode(sys.stdout.encoding)
    except subprocess.CalledProcessError as e:
        print("CalledProcessError")
        return e.returncode, e.output.decode(sys.stdout.encoding)
    except FileNotFoundError as e:
        return e.errno, e.strerror

import zipfile, os
def Unzip(target_file, output_dir, name):
    zipfiles=zipfile.ZipFile(target_file, 'r')
    zipfiles.extractall(os.path.join(output_dir,
                        name))
    zipfiles.close()
    print("Unzip finished!")
