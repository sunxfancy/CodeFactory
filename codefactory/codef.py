#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Sun Xiaofan <sxf>
# @Date:   2016-11-14
# @Email:  sunxfancy@gmail.com
# @Last modified by:   sxf
# @Last modified time: 2016-11-15
# @License: MIT License

import sys, os, shutil
from . import utils, toolchains
from . import template as tp
from . import click
import pkg_resources
from pkg_resources import Requirement

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    version = pkg_resources.require("codefactory")[0].version
    click.echo('Version '+version)
    ctx.exit()

yes_choose = False

@click.group()
@click.option('-y', '--yes', default=False, is_flag=True,
              help='Auto-agree Yes/No choose')
@click.option('-v', '--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True,
              help='Show codef version')
def cli(yes):
    """A native code auto build tool."""
    yes_choose = yes
    tools = toolchains.ToolChains()
    tools.check_tools()

@cli.command('init', short_help='init the repo')
@click.option('-t', '--template', default='cpp', help='Using template, (default cpp)')
@click.argument('name')
def init(template, name):
    """Initializes the repository."""
    print("Repository:", name)
    # my_data = os.path.dirname(os.path.realpath(__file__)) + '/templates/' + template +'.zip' # 这条作为临时测试使用
    # my_data = pkg_resources.resource_filename(
    #     Requirement.parse('codefactory'), 'share/codefactory/templates/'+ template +'.zip') # 这条是原版正确的，但现在wheel版有毛病，sdist又不给打包数据了，只能勉强修复
    if (os.name == 'nt'): # 非常无奈，Windows下无论是加--user还是不加，都比unix的少了一级
        my_data = pkg_resources.resource_filename(
            Requirement.parse('codefactory'), '../../share/codefactory/templates/'+ template +'.zip')
    else:
        my_data = pkg_resources.resource_filename(
            Requirement.parse('codefactory'), '../../../share/codefactory/templates/'+ template +'.zip')
    utils.Unzip(my_data, os.getcwd(), name)
    tp.findFile(os.path.join(os.getcwd(), name), {'name': name})
    utils.run('git', 'init', name)
    

@cli.command('build', short_help='build the code with CMake')
@click.option('-s', '--system', default='ninja',
              type=click.Choice(['ninja', 'xcode', 'makefile',
              'makefile-mingw', 'makefile-msys', 'makefile-nmake',
              'vs2008', 'vs2010', 'vs2012', 'vs2013', 'vs2015']))
@click.option('-t', '--target', default='',
                help='Select the build target')
@click.option('-d/-r', '--debug/--release', default=True,
                help='Select the build target')
def build(system, target, debug):
    """Build the code with selected build system, (default ninja)"""
    try:
        os.makedirs('build/'+system +'-'+ ('debug' if debug else 'release') )
    except OSError:
        pass
    try:
        find_conan = os.access("conanfile.txt", os.R_OK) or os.access("conanfile.py", os.R_OK)
        os.chdir('build')
        if find_conan:
            utils.run('conan', 'install', '..', '--build=missing')
        os.chdir(system +'-'+ ('debug' if debug else 'release'))

        mode = '-DCMAKE_BUILD_TYPE=Debug' if debug else '-DCMAKE_BUILD_TYPE=Release'
        utils.run('cmake', '-G', utils.map_buildsystem(system), mode, '../..')
        if target=='':
            utils.run('cmake', '--build', '.')
        else:
            utils.run('cmake', '--build', '.', '--target', target)
        print('Build Succeed')
    except:
        print('Build Failed')


@cli.command('clean', short_help='clean middle files in the repo')
def clean():
    """Clean the repository."""
    print(os.listdir('build'))
    for target in os.listdir('build'):
        print('Cleaning', target, 'dir')
        try:
            utils.run('cmake', '--build', 'build/'+target, '--target', 'clean')
        except:
            pass


@cli.command('depclean', short_help='clean all output files in the repo')
def depclean():
    """Clean all the repository with the release files."""
    shutil.rmtree('build')

if __name__ == "__main__":
   cli()
