import os
import stat
from distutils.dir_util import copy_tree
from shutil import copy2, rmtree, move

from substrate import sanitize_app_id


def new(directory):
    target_dir = os.path.join(os.getcwd(), directory)

    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    
    package_dir, this_filename = os.path.split(__file__)
    data_dir = os.path.join(package_dir, "data")

    copy_tree(data_dir, target_dir)

    app_yaml = open(os.path.join(target_dir, "app.yaml")).read()
    app_yaml = app_yaml.replace("your-app-id", sanitize_app_id(os.path.basename(os.path.abspath(target_dir))))

    #noinspection Restricted_Python_calls
    file = open(os.path.join(target_dir, "app.yaml"), "w")
    file.write(app_yaml)
    file.close()

    # permissions don't get saved in zip files. Make manage.py executable.
    # chmod 755 manage.py
    os.chmod(os.path.join(target_dir, "manage.py"), stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

def update(directory):
    target_dir = os.path.join(os.getcwd(), directory)
    package_dir, this_filename = os.path.split(__file__)
    data_dir = os.path.join(package_dir, "data")

    target_lib_substrate = os.path.join(target_dir, "lib", "substrate")
    target_local_substrate = os.path.join(target_dir, "local", "substrate")

    target_lib_usr = os.path.join(target_dir, "lib", "usr")
    target_local_usr = os.path.join(target_dir, "local", "usr")

    create_lib_usr = False
    if not os.path.exists(target_lib_usr):
        create_lib_usr = True
    create_local_usr = False
    if not os.path.exists(target_local_usr):
        create_local_usr = True

    data_lib_substrate = os.path.join(data_dir, "lib", "substrate")
    data_local_substrate = os.path.join(data_dir, "local", "substrate")

    #Remove the lib/substrate and local/substrate dirs
    if os.path.exists(target_lib_substrate):
        rmtree(target_lib_substrate)
    if os.path.exists(target_local_substrate):
        rmtree(target_local_substrate)
    #Copy the new lib/substrate and local/substrate
    copy_tree(data_lib_substrate, target_lib_substrate)
    copy_tree(data_local_substrate, target_local_substrate)

    if create_lib_usr:
        os.mkdir(target_lib_usr)
        old_target_lib = os.path.join(target_dir, "lib")
        os.remove(os.path.join(old_target_lib, "__init__.py"))
        for filename in os.listdir(old_target_lib):
            if filename != "substrate" and filename != "usr":
                if not filename.endswith(".pyc") and filename not in os.listdir(target_lib_substrate):
                    move(os.path.join(old_target_lib, filename), target_lib_usr)
                else:
                    file_to_delete = os.path.join(old_target_lib, filename)
                    if os.path.isdir(file_to_delete):
                        rmtree(file_to_delete)
                    else:
                        os.remove(file_to_delete)

    if create_local_usr:
        os.mkdir(target_local_usr)
        new_target_usr_lib = os.path.join(target_local_usr, "lib")
        os.mkdir(new_target_usr_lib)
        new_target_usr_manage = os.path.join(target_local_usr, "manage")
        os.mkdir(new_target_usr_manage)
        old_target_local_lib = os.path.join(target_dir, "local", "lib")
        new_target_local_substrate_lib = os.path.join(target_local_substrate, "lib")
        for filename in os.listdir(old_target_local_lib):
            if not filename.endswith(".pyc") and filename != "__init__.py" and filename not in os.listdir(new_target_local_substrate_lib):
                move(os.path.join(old_target_local_lib, filename), new_target_usr_lib)
        rmtree(old_target_local_lib)
        rmtree(os.path.join(target_dir, "local", "commands"))
        if os.path.exists(os.path.join(target_dir, "local", "__init__.py")):
            os.remove(os.path.join(target_dir, "local", "__init__.py"))
        if os.path.exists(os.path.join(target_dir, "local", "__init__.pyc")):
            os.remove(os.path.join(target_dir, "local", "__init__.pyc"))

    copy2(os.path.join(data_dir, "env_setup.py"), os.path.join(target_dir, "env_setup.py"))
    copy2(os.path.join(data_dir, "manage.py"), os.path.join(target_dir, "manage.py"))
    # permissions don't get saved in zip files. Make manage.py executable.
    # chmod 755 manage.py
    os.chmod(os.path.join(target_dir, "manage.py"), stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
