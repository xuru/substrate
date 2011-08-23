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

