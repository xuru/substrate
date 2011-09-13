substrate
======

Substrate is a base application and set of libraries for making Google
App Engine development easier. It includes a base app, management
script, testing framework with unittest2 and gaetestbed, a set of
common helper functions (agar), and a serialization library
(restler). It also comes with webapp2 and pytz.

Substrate is based on best practices for Google App Engine learned in
developing several real-world applications with many users.

For more documentation see: http://substrate-docs.appspot.com

Installation
---------

TODO: actually deploy packages.

To install, run:

   easy_install substrate

or

   pip install substrate

or download the package, and run:

   python setup.py install

Creating a new application
---------------------

To create a new application, run:

   substrate new app_name

This will create a new directory "app_name" and unpack the substrate
application libraries in it. The application name in app.yaml will be
set to "app_name".

Upgrading an existing application
---------------------------

If you have an existing application, you can upgrade it to the latest
substrate code by updating the substrate package (see "Installation",
above) and then running:

   substrate new app_name

Where app_name is the name of the directory. (For example, you could
run this in the current directory with .)

This command will NOT touch any of your application's files. Only
substrate files in the local/ and lib/ directories will be
overwritten. You can add new files to those directories, but do not
edit existing files.

