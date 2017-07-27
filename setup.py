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
from distutils.command.build_py import build_py as _build_py

import zipfile, os

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

class ZipFile(_build_py):
    def run(self):
        old_cur = os.getcwd()
        for dir in os.listdir(os.path.join(old_cur, 'templates')):
            now = os.path.join(old_cur, 'templates', dir)
            if os.path.isdir(now) and dir != '.DS_Store':
                os.chdir(now)
                target_file = os.path.join('..', dir + '.zip')
                with zipfile.ZipFile(target_file, 'w') as myzip:
                    zipdir('.', myzip)
                print("Zip finished!")
                os.chdir(old_cur)
                _build_py.run(self)

setup(
    name='codefactory',   #名称
    version='0.5.0',  #版本
    description="a native code builder using git, github service and cmake", #描述
    keywords='codef code factory builder cmake github',
    author='sunxfancy',  #作者
    author_email='sunxfancy@gmail.com', #作者邮箱
    url='https://github.com/sunxfancy', #作者链接
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'autotest']),
    zip_safe=True,
    data_files=[('share/codefactory/templates/', ['templates/CPPTemplate.zip'])],
    install_requires=[      #需求的第三方模块
    ],
    entry_points={
        'console_scripts':[
            'codef = codefactory.codef:cli'
        ]
    },
    cmdclass={
        # 'install':ZipFile,
        'zip':ZipFile,
    }
)
