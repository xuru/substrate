import os
import sys

def setup():
    '''
    Adds <project_root>/lib to the python path.  
    Starts in current working directory and traverses up until found.
    Assumes app.yaml is in project root.
    '''
    curdir = os.path.abspath('.')
    paths_to_search = os.path.abspath('.').split(os.path.sep)

    for path in paths_to_search:
        if os.path.exists('app.yaml'):
            lib_path = os.path.join(os.path.abspath('.'), 'lib')

            if lib_path not in sys.path:
                sys.path.insert(0, lib_path)
            
            os.chdir(curdir)
            break
        
        os.chdir('..')
    else:
        raise Exception('app.yaml not found for env_setup.setup()')
