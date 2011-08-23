Substrate Commands
==================

--------
overview
--------
|   >% python2.5 manage.py 
|   manage.py commands: 
|      builddocs -  Builds the documentation for substrate 
|      discover  -  Run tests using unittest2 'discover' 
|      rshell    -  Connect to a remote datastore through an interactive console. 
|      shell     -  Run an interactive console after including AppEngine and project libraries. 
|      test      -  Run tests using 'nose' for discovery 
|      upgrade   -  Pulls the latest version of substrate to ~/.substrate and replaces the project files.


---------
upgrade
---------
|   >% python2.5 manage.py upgrade --help 
|   usage: upgrade [-h] [--url URL] [--reset-url RESET_URL]
|                  [--local-only LOCAL_ONLY]
|   
|   optional arguments:
|     -h, --help            show this help message and exit
|     --url URL             The hg repository url to use for upgrading substrate.
|     --reset-url RESET_URL
|                           Uses the default repository for upgrades.
|     --local-only LOCAL_ONLY
|                           Substrate env files only (manage.py, local/\*, etc)

^^^^^^^^^^^^
Dependencies
^^^^^^^^^^^^

The mercurial binary (hg) is available on the system path.

On Mac OS X using the default easy_install to install mercurial will cause problems with the upgrade command.
 * The current fix is to use the python version specific easy_install, i.e. easy_install-2.6 -U mercurial.

