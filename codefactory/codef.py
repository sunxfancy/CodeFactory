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
import multiprocessing

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    version = pkg_resources.require("codefactory")[0].version
    click.echo('Version '+version)
    ctx.exit()

yes_choose = False
default_tool = 'ninja'

@click.group()
@click.option('-y', '--yes', default=False, is_flag=True,
              help='Auto-agree Yes/No choose')
@click.option('-v', '--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True,
              help='Show codef version')
def cli(yes=False):
    """A native code auto build tool."""
    global yes_choose
    global default_tool
    yes_choose = yes
    tools = toolchains.ToolChains()
    default_tool = tools.check_tools()

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
    
def setup_sub_dir(system, debug, build_dir):
    if system[0:2] != 'vs':
        sub_dir = system +'-'+ ('debug' if debug else 'release')
    else:
        sub_dir = system
    try:
        os.makedirs( build_dir+'/'+sub_dir )
    except OSError:
        pass
    return sub_dir

@cli.command('build', short_help='build the code with CMake')
@click.option('-s', '--system', default='default',
                type=click.Choice(utils.get_allowed_buildsystem()),
                help='Avaliable build system')
@click.option('-t', '--target', default='',
                help='Select the build target')
@click.option('-d/-r', '--debug/--release', default=True,
                help='Select the build type')
@click.option('-n', '--native', is_flag=True, default=False,
                help='Using native build mode to directly call cmake build')
@click.option('-j', '--threads', default=1,
                help='Threads Number for parallel building')
@click.option('-p', '--profile', default='default',
                help='Conan profile file name (invalid in native mode)')
def build(system, target, debug, native, threads, profile):
    """Build the code with selected build system"""
    if system == 'default':
        system = default_tool
        print("Default build system:", system)
    build_dir = 'build'

    try:
        find_conan = os.access("conanfile.txt", os.R_OK) or os.access("conanfile.py", os.R_OK)

        if (not find_conan) or native:
            # native build mode
            sub_dir = setup_sub_dir(system, debug, build_dir)
            os.chdir(build_dir)
            os.chdir(sub_dir)
            mt = str(threads)

            if find_conan:
                utils.run('conan', 'install', '../..', '--build=missing')
            if system[0:2] != 'vs':
                mode = '-DCMAKE_BUILD_TYPE=Debug' if debug else '-DCMAKE_BUILD_TYPE=Release'
                utils.run('cmake', '-G', utils.map_buildsystem(system), mode, '../..')
                if target=='':
                    utils.run('cmake', '--build', '.', '-j', mt)
                else:
                    utils.run('cmake', '--build', '.', '--target', target, '-j', mt)
            else:
                # vs can change debug or release in one configure
                mode = 'Debug' if debug else 'Release'
                utils.run('cmake', '-G', utils.map_buildsystem(system), '../..')
                if target=='':
                    utils.run('cmake', '--build', '.', '--config', mode, '-j', mt)
                else:
                    utils.run('cmake', '--build', '.', '--target', target, '--config', mode, '-j', mt)
        else:
            # conan build
            sub_dir = setup_sub_dir(profile, debug, build_dir)
            mode = 'Debug' if debug else 'Release'
            utils.run('conan', 'install', '.', '-if', build_dir+'/'+sub_dir, '-pr', profile, '-s', 'build_type='+mode, '--build=missing')
            utils.run('conan', 'build', '.', '-bf', build_dir+'/'+sub_dir)

        print('Build Succeed')
    except Exception as ex:
        print('Build Failed')
        # print(ex)

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
