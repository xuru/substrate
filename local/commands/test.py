import logging
import tempfile

from google.appengine.tools import dev_appserver
from google.appengine.tools import dev_appserver_main

from nose.core import main
from nosegae import NoseGAE
from nose_exclude import NoseExclude
from nose.plugins.logcapture import LogCapture
import re

import os

os.environ['NOSE_WITH_NOSEEXCLUDE'] = "--exclude-dir=lib"
os.environ['NOSEEXCLUDE_DIRS'] = "./lib ./local"
os.environ['NOSE_WHERE'] = "."
os.environ['NOSE_ALL_MODULES'] = "false"
os.environ['NOSE_LOGGING_CLEAR_HANDLERS'] = "true"

config = matcher = None

try:
    config, matcher = dev_appserver.LoadAppConfig(".", {})
except yaml_errors.EventListenerError, e:
    logging.error('Fatal error when loading application configuration:\n' +
                                    str(e))
except dev_appserver.InvalidAppConfigError, e:
    logging.error('Application configuration file invalid:\n%s', e)

#Configure our dev_appserver setup args
args = dev_appserver_main.DEFAULT_ARGS.copy()
args[dev_appserver_main.ARG_CLEAR_DATASTORE] = True
args[dev_appserver_main.ARG_BLOBSTORE_PATH] = os.path.join(
        tempfile.gettempdir(), 'dev_appserver.test.blobstore')
args[dev_appserver_main.ARG_DATASTORE_PATH] = os.path.join(
        tempfile.gettempdir(), 'dev_appserver.test.datastore')
args[dev_appserver_main.ARG_MATCHER_PATH] = os.path.join(
        tempfile.gettempdir(), 'dev_appserver.test.matcher')
args[dev_appserver_main.ARG_HISTORY_PATH] = os.path.join(
        tempfile.gettempdir(), 'dev_appserver.test.datastore.history')

dev_appserver.SetupStubs(config.application, **args)
os.environ['APPLICATION_ID'] = config.application

# Run the test on the current directory
# import sys
# sys.argv[1] = "."

# Run the test on the current directory if no other test is passed in as an option.
# ie python manage.py test tests/my_tests.py
import sys
if len (sys.argv) < 3:
    print "No tests specified.  Running everything..."
    sys.argv[1] = "."
else:
    print "Testing: %s"% sys.argv[2]
    sys.argv[1] = sys.argv[2]
    del sys.argv[2]

main(plugins=[NoseGAE(), NoseExclude()])
# main(plugins=[NoseGAE(), NoseExclude(), LogCapture()])

