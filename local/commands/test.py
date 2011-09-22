""" Run tests using 'nose' for discovery """

import logging
import tempfile

from google.appengine.api import yaml_errors
from google.appengine.tools import dev_appserver
from google.appengine.tools import dev_appserver_main

from nose.core import main
from nosegae import NoseGAE
from nose_exclude import NoseExclude
from nose.plugins.logcapture import LogCapture

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
args[dev_appserver_main.ARG_PROSPECTIVE_SEARCH_PATH] = os.path.join(
        tempfile.gettempdir(), 'dev_appserver.test.matcher')
args[dev_appserver_main.ARG_HISTORY_PATH] = os.path.join(
        tempfile.gettempdir(), 'dev_appserver.test.datastore.history')

from google.appengine.api import app_identity
dev_appserver.SetupStubs(config.application, **args)
os.environ['APPLICATION_ID'] = 'dev~%s' % app_identity.get_application_id()

# ie python manage.py test tests/my_tests.py
import sys
# Would like to get the log capture working sometime...
# main(plugins=[NoseGAE(), NoseExclude(), LogCapture()])
if __name__ == "__main__":
    if len (sys.argv) < 2:
        print "No tests specified.  Running everything..."
        sys.argv[0] = "."
    else:
        print "Testing: %s"% sys.argv[1]
        sys.argv[0] = sys.argv[1]
        del sys.argv[1]
    main(plugins=[NoseGAE(), NoseExclude()])

