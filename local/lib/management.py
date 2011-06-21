#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Convenience wrapper for starting an appengine tool."""


import os
import sys

# Only works for UNIXy style OSes.
# Find App Engine SDK
SDKPATH_CFG = "sdkpath.cfg"
DIR_PATH = ""
if os.path.isfile(SDKPATH_CFG):
    DIR_PATH = open(SDKPATH_CFG).read()
else:
    sys.stderr.write('Scanning for App Engine SDK...\n')
    for d in os.environ["PATH"].split(":"):
        dev_appserver = os.path.join(d, "dev_appserver.py")
        if os.path.isfile(dev_appserver):
            DIR_PATH = os.path.abspath(os.path.dirname(os.path.realpath(dev_appserver)))
            open(SDKPATH_CFG, "w").write(DIR_PATH)
            sys.stderr.write('Found SDK Path: %s\n' % DIR_PATH)


if not hasattr(sys, 'version_info'):
    sys.stderr.write('Very old versions of Python are not supported. Please '
                     'use version 2.5 or greater.\n')
    sys.exit(1)
version_tuple = tuple(sys.version_info[:2])

if version_tuple != (2, 5):
    sys.stderr.write('Error: Python %d.%d is not supported. Please use '
                     'version 2.5.\n' % version_tuple)
    sys.exit(1)

#DIR_PATH = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

if not DIR_PATH:
    sys.stderr.write("Could not find SDK path.  Make sure dev_appserver.py is in your PATH")
    sys.exit(1)

# local 'helper' scripts
local_path = 'local'
SCRIPT_DIR = os.path.join(DIR_PATH, 'google', 'appengine', 'tools')

EXTRA_PATHS = [
    DIR_PATH,
    os.path.join(DIR_PATH, 'lib', 'antlr3'),
    os.path.join(DIR_PATH, 'lib', 'django_0_96'),
    os.path.join(DIR_PATH, 'lib', 'fancy_urllib'),
    os.path.join(DIR_PATH, 'lib', 'ipaddr'),
    os.path.join(DIR_PATH, 'lib', 'webob'),
    os.path.join(DIR_PATH, 'lib', 'yaml', 'lib'),
    os.path.join(DIR_PATH, 'lib', 'simplejson'),
    os.path.join(DIR_PATH, 'lib', 'graphy'),
    os.path.join(".", 'local', 'lib'),
    os.path.join(".", 'lib'),
]

def fix_sys_path():
    """Fix the sys.path to include our extra paths."""
    sys.path = EXTRA_PATHS + sys.path


def print_subcommand_overviews(commands):
    import logging
    logging.basicConfig(level=logging.ERROR)
    print "manage.py commands: "
    cmd_width = max(len(command) for command in commands)
    for command in commands:
        module = __import__("local.commands", {}, {}, [command])
        doc = getattr(module, command).__doc__
        print "  ", command.ljust(cmd_width), "-" if doc else "" ,  doc or ""

def run_command(command, globals_, script_dir=SCRIPT_DIR):
    """Execute the file at the specified path with the passed-in globals."""
    fix_sys_path()
    import pkgutil, local.commands
    pkgpath = os.path.dirname(local.commands.__file__)
    commands = [name for _, name, _ in pkgutil.iter_modules([pkgpath])]
    for arg in sys.argv:
        if arg in commands:
            break
    else:
        print_subcommand_overviews(commands)
        sys.exit(1)
    command_idx = sys.argv.index(arg)
    script_name = sys.argv[command_idx]
    management_args = sys.argv[:command_idx]
    command_args = sys.argv[command_idx:]
    sys.argv = command_args
    script_path = os.path.join('./%s/commands' % local_path, script_name + ".py")
    execfile(script_path, globals_)


if __name__ == '__main__':
    run_command(__file__, globals())

