#!/usr/bin/env python
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
        self.tools = ['git', 'cmake', 'conan']
        self.options = ['ninja', 'make', 'nmake']
    def check_tools(self):
        for tool in self.tools:
            if not self.find_tool(tool):
                self.download_tool(tool)
        for tool in self.options:
            if self.find_tool(tool, option=True):
                return tool

    def find_tool(self, name, option=False):
        ws, msg = utils.run_limited(name, '--version')
        if ws != 0:
            if not option:
                sys.stdout.write("Not Found: ")
                if name == 'ninja':
                    print('ninja')
            return False
        sys.stdout.write("Found: ")
        sys.stdout.flush()
        if name == 'ninja':
            sys.stdout.write('ninja ')
            sys.stdout.flush()
        print(msg)
        return True

    def download_tool(self, name):
        # TODO: add -y config
        # str = input("Would you like to download tools automaticly? [y/N]")
        # if str != '' and (str[0] == 'y' or str[0] == 'Y'):
        #     return
        print("Please install", name, "manually, and add it into PATH env.")
        sys.exit(3)
