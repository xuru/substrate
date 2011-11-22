#!/usr/bin/env python
""" Substrate management interface. Fixes up appengine and substrate paths and runs substrate commands."""

import os
import sys

# Only works for UNIXy style OSes.
# Find App Engine SDK
dev_appserver = None
DIR_PATH = ""
for d in os.environ["PATH"].split(":"):
    dev_appserver_path = os.path.join(d, "dev_appserver.py")
    if os.path.isfile(dev_appserver_path):
        DIR_PATH = os.path.abspath(os.path.dirname(os.path.realpath(dev_appserver_path)))
        sys.path.append(DIR_PATH)
        import dev_appserver
        sys.path.pop()


if not hasattr(sys, 'version_info'):
    sys.stderr.write('Very old versions of Python are not supported. Please '
                     'use version 2.5 or greater.\n')
    sys.exit(1)
version_tuple = tuple(sys.version_info[:2])

if version_tuple != (2, 5):
    sys.stderr.write('Warning: Python %d.%d is not supported. Please use '
                     'version 2.5.\n' % version_tuple)

if not DIR_PATH:
    sys.stderr.write("Could not find SDK path.  Make sure dev_appserver.py is in your PATH")
    sys.exit(1)

# local 'helper' scripts
SCRIPT_DIR = os.path.join(DIR_PATH, 'google', 'appengine', 'tools')

EXTRA_PATHS = dev_appserver.EXTRA_PATHS[:]
SUBSTRATE_PATHS = [
    os.path.join('.', 'lib', 'substrate'),
    os.path.join('.', 'local', 'substrate', 'lib'),
    os.path.join('.', 'local', 'substrate', 'manage'),
]
USR_PATHS = [
    os.path.join('.', 'lib', 'usr'),
    os.path.join('.', 'local', 'usr', 'lib'),
    os.path.join('.', 'local', 'usr', 'manage'),
]

def fix_sys_path():
    """Fix the sys.path to include our extra paths."""
    sys.path = EXTRA_PATHS + SUBSTRATE_PATHS + USR_PATHS + sys.path

def print_subcommand_overviews(sub_comms, usr_comms):
    import logging
    logging.basicConfig(level=logging.ERROR)
    print "manage.py built-in commands: "
    cmd_width = max(len(command) for command in sub_comms)
    for command in sub_comms:
        module = __import__("substrate_manage.commands", {}, {}, [command])
        doc = getattr(module, command).__doc__
        print "  ", command.ljust(cmd_width), "-" if doc else "" ,  doc or ""
    print "manage.py project commands: "
    cmd_width = max(len(command) for command in usr_comms)
    for command in usr_comms:
        module = __import__("substrate_manage_usr.commands", {}, {}, [command])
        doc = getattr(module, command).__doc__
        print "  ", command.ljust(cmd_width), "-" if doc else "" ,  doc or ""


def run_command(command, globals_, script_dir=SCRIPT_DIR):
    """Execute the file at the specified path with the passed-in globals."""
    fix_sys_path()
    import pkgutil
    from substrate_manage import commands as substrate_commands
    script_path = None
    pkgpath = os.path.dirname(substrate_commands.__file__)
    sub_comms = [name for _, name, _ in pkgutil.iter_modules([pkgpath])]
    for arg in sys.argv:
        if arg in sub_comms:
            script_path = './local/substrate/manage/substrate_manage/commands'
            break
    else:
        from substrate_manage_usr import commands as usr_commands
        pkgpath = os.path.dirname(usr_commands.__file__)
        usr_comms = [name for _, name, _ in pkgutil.iter_modules([pkgpath])]
        for arg in sys.argv:
            if arg in usr_comms:
                script_path = './local/usr/manage/substrate_manage_usr/commands'
                break
        else:
            print_subcommand_overviews(sub_comms, usr_comms)
            sys.exit(1)
    command_idx = sys.argv.index(arg)
    script_name = sys.argv[command_idx]
    management_args = sys.argv[:command_idx]

    command_args = sys.argv[command_idx:]
    sys.argv = command_args
    script_path = os.path.join(script_path, script_name + ".py")
    execfile(script_path, globals_)


if __name__ == '__main__':
    run_command(__file__, globals())

