""" Pulls the latest version of substrate to ~/.substrate and replaces the project files."""

import os
import shutil

# TODO can we assume no user libs are in local/lib?
# TODO add user_lib for these?
# TODO use hg tags for releases?  major/minor/dev(default) options?
# TODO make substrate repo public
# TODO check to see if project to be upgraded has no uncommitted files


if __name__ == '__main__':
    upgrade_items = ['manage.py', 'env_setup.py', 'local/commands', 'local/lib', 'lib/agar']


    current_dir = os.path.abspath('.')
    substrate_home_dir = os.path.expanduser('~/.substrate')
    substrate_repo = os.path.expanduser('%s/substrate' % substrate_home_dir)

    confirm = raw_input('This will delete and copy substrate files/dirs, continue?(y/n) ')

    if confirm.upper() != 'Y':
        print 'Upgrade canceled.'
        import sys
        sys.exit(1)

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
            print 'Replacing project file: %s' % item
            shutil.copy(item_path, current_dir)
        
        if os.path.isdir(item_path):
            print 'Replacing project dir: %s' % item
            shutil.rmtree('%s/%s' % (current_dir, item))
            shutil.copytree(item_path, '%s/%s' % (current_dir, item))
