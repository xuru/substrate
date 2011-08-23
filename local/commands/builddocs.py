""" Builds the documentation for substrate """

import os, sys

if __name__ == "__main__":
    cur_dir = os.path.abspath(".")
    os.chdir(os.path.join('docs', 'static'))
    # os.system('make %s' % " ".join(["epub", "html"]))
    os.system('make html')
    os.chdir(cur_dir)
