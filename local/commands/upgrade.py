import os
import shutil

# TODO can we assume no user libs are in local/lib?
# TODO add user_lib for these?
upgrade_items = ['manage.py', 'env_setup.py', 'local/commands', 'local/lib']

have_dot_dir = os.path.isdir(os.path.expanduser('~/.substrate'))

if not have_dot_dir:
    os.mkdir(os.path.expanduser('~/.substrate'))


current_dir = os.path.abspath(".")
substrate_repo = os.path.expanduser('~/.substrate/substrate')
repo_exists = os.path.isdir(substrate_repo)


if repo_exists:
    os.chdir(substrate_repo)
    os.system('hg fetch')
    os.chdir(current_dir)
else:
    os.system('hg clone ssh://hg@bitbucket.org/garykoelling/substrate %s' % substrate_repo)


for item in upgrade_items:
    new_item = os.path.expanduser('%s/%s' % (substrate_repo, item))

    if os.path.isfile(new_item):
        shutil.copy(new_item, current_dir)
    
    if os.path.isdir(new_item):
        shutil.rmtree('%s/%s' % (current_dir, item))
        shutil.copytree(new_item, '%s/%s' % (current_dir, item))
