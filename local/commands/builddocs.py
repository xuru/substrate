import os, sys

cur_dir = os.path.abspath(".")
os.chdir(os.path.join('docs', 'static'))
os.system('make %s' % " ".join(sys.argv[2:]))
os.chdir(cur_dir)

