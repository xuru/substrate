import os
import shutil

# TODO can we assume no user libs are in local/lib?
# TODO add user_lib for these?
# TODO use hg tags for releases?  major/minor/dev(default) options?
# TODO make substrate repo public

upgrade_items = ['manage.py', 'env_setup.py', 'local/commands', 'local/lib', 'lib/agar']


current_dir = os.path.abspath('.')
substrate_home_dir = os.path.expanduser('~/.substrate')
substrate_repo = os.path.expanduser('%s/substrate' % substrate_home_dir)


if not os.path.isdir(substrate_home_dir):
    os.mkdir(os.path.expanduser(substrate_home_dir))


if os.path.isdir(substrate_repo):
    os.chdir(substrate_repo)
    os.system('hg fetch')
    os.chdir(current_dir)
else:
    os.system('hg clone ssh://hg@bitbucket.org/garykoelling/substrate %s' % substrate_repo)


for item in upgrade_items:
    item_path = '%s/%s' % (substrate_repo, item)

    if os.path.isfile(item_path):
        shutil.copy(item_path, current_dir)
    
    if os.path.isdir(item_path):
        shutil.rmtree('%s/%s' % (current_dir, item))
        shutil.copytree(item_path, '%s/%s' % (current_dir, item))
