#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @Author: Sun Xiaofan <sxf>
# @Date:   2016-11-15
# @Email:  sunxfancy@gmail.com
# @Last modified by:   sxf
# @Last modified time: 2016-11-15
# @License: MIT License

import sys, os
from . import utils

class ToolChains(object):
    """docstring for ToolChains."""
    def __init__(self):
        super(ToolChains, self).__init__()
        self.tools = ['git', 'cmake', 'conan', 'ninja']
    def check_tools(self):
        for tool in self.tools:
            if not self.find_tool(tool):
                self.download_tool(tool)

    def find_tool(self, name):
        sys.stdout.write("Found: ")
        if name == 'ninja':
            sys.stdout.write('ninja ')
        sys.stdout.flush()
        ws, msg = utils.run_limited(name, '--version')
        if ws != 0:
            print(name)
            return False
        print(msg)
        return True

    def download_tool(self, name):
        # TODO: add -y config
        str = input("Would you like to download tools automaticly? [y/N]")
        if str != '' and (str[0] == 'y' or str[0] == 'Y'):

            return
        print("Please install", name, "manually, and add it into PATH env.")
        sys.exit(3)
