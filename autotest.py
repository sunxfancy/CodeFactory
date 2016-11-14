#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @Author: Sun Xiaofan <sxf>
# @Date:   2016-11-13
# @Email:  sunxfancy@gmail.com
# @Last modified by:   sxf
# @Last modified time: 2016-11-14
# @License: MIT License

import unittest
from codefactory.toolchains import ToolChains

# 执行测试的类
class ToolChainsTestCase(unittest.TestCase):
    def testFindTool(self):
        toolchain = ToolChains()
        for tool in toolchain.tools:
            self.assertEqual(toolchain.find_tool(tool), True)

# 测试
if __name__ == "__main__":
    unittest.main()
