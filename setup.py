#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @Author: Sun Xiaofan <sxf>
# @Date:   2016-11-14
# @Email:  sunxfancy@gmail.com
# @Last modified by:   sxf
# @Last modified time: 2016-11-15
# @License: MIT License

from setuptools import setup, find_packages

setup(
    name='codefactory',   #名称
    version='0.3.1',  #版本
    description="a native code builder using git, github service and cmake", #描述
    keywords='codef code factory builder cmake github',
    author='sxf',  #作者
    author_email='sunxfancy@gmail.com', #作者邮箱
    url='https://github.com/sunxfancy', #作者链接
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'autotest']),
    zip_safe=True,
    data_files=[('share/codefactory/templates/', ['templates/CPPTemplate.zip'])],
    install_requires=[      #需求的第三方模块
        'click'
    ],
    entry_points={
        'console_scripts':[
            'codef = codefactory.codef:cli'
        ]
    }
)
