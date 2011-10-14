substrate
=========

Substrate is a base application and set of libraries for making Google
App Engine development easier. It includes a base app with management
script, testing already set up, a set of common helper functions
(agar), and a serialization library (restler). It also comes with
common libraries like webapp2 and pytz ready to go.

Substrate is based on best practices for Google App Engine learned in
developing several real-world applications with many users.

We are tired of seeing App Engine frameworks languish unsupported. For
that reason, Substrate is **NOT** a framework. It is a base
application with a set of libraries and helpers. No more, no less.

For more documentation see: http://packages.python.org/substrate/

Installation
------------

To install substrate, run::

  $ easy_install substrate

or::

  $ pip install substrate

or download the package, and run::

  $ python setup.py install

Creating a new application
--------------------------

To create a new application, run::

  $ substrate new app_name

This will create a new directory "app_name" and unpack the substrate
application libraries in it. The application name in app.yaml will be
set to "app_name".

Or, if you find installing a script to do this for you tedious, you
can clone the substrate repository and copy the ``app`` directory to
create your application.

Upgrading an existing application
---------------------------------

If you have an existing application, you can upgrade it to the latest
substrate code by updating the substrate package (see "Installation",
above) and then running::

   $ substrate new app_name

Where app_name is the name of the directory. (For example, you could
run this in the current directory with .)

This command will NOT touch any of your application's files. Only
substrate files in the ``local/`` and ``lib/`` directories will be
overwritten. You can add new files to those directories, but do not
edit existing files.

Management Console
------------------

``manage.py`` is a management console for your app.

It has the following commands:

  ``shell``
    Run a shell against your local application (requires iPython)

  ``rshell``
    Run a remote shell against your application on Google App
    Engine. To specify a different application ID than what is in your
    ``app.yaml``, use ``-A``. If your remote API endpoint is not at
    the default location, you can pass the path as an argument.

  ``test``
    Run your application's tests


Testing
-------

As noted above, ``manage.py`` has a ``test`` command. This runs all
the tests in the ``tests`` directory of your application using
unittest2. Included with the Substrate base app is a simple "hello
world" test that you can run to verify your installation. It is
located in ``tests/handlers/test_main.py``.

License
-------

Substrate is mostly a packaging of other libraries, which have their
own licenses. Original code in Substrate is under the MIT license.
