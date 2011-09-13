import os
from string import Template
from distutils.dir_util import copy_tree

def new(directory):
    target_dir = os.path.join(os.getcwd(), directory)

    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    
    package_dir, this_filename = os.path.split(__file__)
    data_dir = os.path.join(package_dir, "data")

    copy_tree(data_dir, target_dir)

    app_yaml = open(os.path.join(target_dir, "app.yaml")).read()
    template = Template(app_yaml)
    result = template.substitute(app_name=os.path.basename(os.path.abspath(target_dir)))

    file = open(os.path.join(target_dir, "app.yaml"), "w")
    file.write(result)
    file.close()
    
    update(directory)

def update(directory):
    target_dir = os.path.join(os.getcwd(), directory)
    package_dir, this_filename = os.path.split(__file__)

    # TODO: figure out where to put local and lib

