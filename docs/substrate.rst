The ``substrate`` Command
=========================

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

   $ substrate update app_directory

Where ``app_directory`` is the name of the application directory to upgrade. (For example, you could
run this in the current directory with .)

This command will NOT touch any of your application's files. Only
substrate files in the ``local/`` and ``lib/`` directories will be
overwritten. You can add new files to those directories, but do not
edit existing files.

Management Console
------------------

``manage.py`` is a management console for your app. It can invoke several commands.

::

  $ ./manage.py shell

Runs a shell against your local application (requires `iPython`_)

::

  $ ./manage.py rshell

Runs a remote shell against your application on Google App
Engine. To specify a different application ID than what is in your
``app.yaml``, use ``-A``. If your remote API endpoint is not at
the default location, you can pass the path as an argument.

::

  $ ./manage.py test

Runs your application's tests.

Testing
-------

As noted above, ``manage.py`` has a ``test`` command. This runs all
the tests in the ``tests`` directory of your application using
unittest2. Included with the Substrate base app is a simple "hello
world" test that you can run to verify your installation. It is
located in ``tests/handlers/test_main.py``.

.. Links

.. _iPython: http://ipython.org/