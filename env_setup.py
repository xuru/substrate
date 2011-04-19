import os
import sys

# env_setup_path = os.path.dirname(__file__)
# def alt_setup():
#     lib_path = os.path.join(env_setup_path, 'lib')
#     print 'lib_path: %s'% lib_path
#     if lib_path not in sys.path:
#         sys.path.insert(0, lib_path)

def setup():
    '''
    Adds <project_root>/lib to the python path.  
    Starts in current working directory and traverses up until found.
    Assumes app.yaml is in project root.
    '''
    start_path = os.path.abspath('.')
    search_path = start_path
    while search_path:
        app_yaml_path = os.path.join(search_path, 'app.yaml')
        
        if os.path.exists(app_yaml_path):
            lib_path = os.path.join(search_path, 'lib')

            if lib_path not in sys.path:
                sys.path.insert(0, lib_path)
            
            break
        search_path, last_dir = os.path.split(search_path)
    else:
        raise os.error('app.yaml not found for env_setup.setup().%sSearch started in: %s'% (os.linesep, start_path))
