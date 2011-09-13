import os
from setuptools import setup, find_packages

def package_data():
    """
    package_data is incredibly stupid and no wildcard can match a
    directory or it will break. This provides a list of all files in
    the data directory to circumvent that.
    """
    
    this_dir, this_filename = os.path.split(os.path.abspath(__file__))
    data_dir = os.path.join(this_dir, "substrate", "data")
    data_dir_prefix = os.path.dirname(data_dir)
    
    data = []

    for root, dirs, files in os.walk(data_dir):
        for f in files:
            path_without_prefix = os.path.join(root, f)[len(data_dir_prefix)+1:]
            data.append(path_without_prefix)
    
    return data

setup(name='substrate',
      version='0.1',
      description='A set of libraries and a base application for making Google App Engine development easier.',
      author='Thomas Bombach, Jr.',
      author_email='thomasbohmbach@gmail.com',
      url='http://substrate-docs.appspot.com/',
      zip_safe=False,
      packages=find_packages(exclude=['tests', 'tests.*']),
      package_data={'': package_data()},
      scripts=['bin/substrate']
      )
