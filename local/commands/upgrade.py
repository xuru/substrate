import os

have_dot_dir = os.path.isdir(os.path.expanduser('~/.substrate'))

if not have_dot_dir:
    os.mkdir(os.path.expanduser('~/.substrate'))

working_dir = os.path.expanduser('~/.substrate/substrate')
have_working_dir = os.path.isdir(working_dir)

if have_working_dir:
    cur_dir = os.path.abspath(".")
    os.chdir(working_dir)
    os.system('hg fetch')
    os.chdir(cur_dir)
else:
    os.system('hg clone ssh://hg@bitbucket.org/garykoelling/substrate %s' % working_dir)
