import os
from string import Template
from distutils.dir_util import copy_tree
from shutil import copy2

from substrate import sanitize_app_id

def new(directory):
    target_dir = os.path.join(os.getcwd(), directory)

    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    
    package_dir, this_filename = os.path.split(__file__)
    data_dir = os.path.join(package_dir, "data")

    copy_tree(data_dir, target_dir)

    app_yaml = open(os.path.join(target_dir, "app.yaml")).read()
    app_yaml = app_yaml.replace("YOUR_APP_ID", sanitize_app_id(os.path.basename(os.path.abspath(target_dir))))

    file = open(os.path.join(target_dir, "app.yaml"), "w")
    file.write(app_yaml)
    file.close()

def update(directory):
    target_dir = os.path.join(os.getcwd(), directory)
    package_dir, this_filename = os.path.split(__file__)
    data_dir = os.path.join(package_dir, "data")

    copy_tree(os.path.join(data_dir, "local"), os.path.join(target_dir, "local"))
    copy_tree(os.path.join(data_dir, "lib"), os.path.join(target_dir, "lib"))
