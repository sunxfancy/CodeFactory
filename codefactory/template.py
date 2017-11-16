#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Sun Xiaofan <sxf>
# @Date:   2016-11-15
# @Email:  sunxfancy@gmail.com
# @Last modified by:   sxf
# @Last modified time: 2016-11-15
# @License: MIT License

import os, re, io

pattern = re.compile(r'(?P<template>{=[a-zA-Z0-9_]+=})')


def template(str, context):
    m = pattern.search(str)

    def replace(matched):
        t = matched.group('template')
        name = t[2: len(t)-2]
        data = context[name]
        return data
    
    ans = pattern.sub(replace, str)
    return ans

def findFile(path, context):
    for root, dirs, files in os.walk(path):
        for file in files:
            arr = os.path.splitext(file)
            if arr[len(arr)-1] == '.tj':
                filepath = os.path.join(root, file)
                outpath = filepath[0:len(filepath)-3]
                with io.open(filepath, "r", encoding="utf-8") as f:
                    data = f.read()
                    data = template(data, context)
                    with io.open(outpath, "w", encoding="utf-8") as o:
                        o.write(data)
                os.remove(filepath)