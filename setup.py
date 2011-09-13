from setuptools import setup, find_packages

setup(name='substrate',
      version='0.1',
      description='A set of libraries and a base application for making Google App Engine development easier.',
      author='Thomas Bombach, Jr.',
      author_email='thomasbohmbach@gmail.com',
      url='http://substrate-docs.appspot.com/',
      zip_safe=False,
      packages=find_packages(exclude=['tests', 'tests.*']),
      package_data={'': ['data/*']},
      scripts=['bin/substrate']
      )
