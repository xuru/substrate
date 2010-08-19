
from google.appengine.tools import dev_appserver
from google.appengine.tools import dev_appserver_main

from nose.core import main, run
from nose.config import Config
from nosegae import NoseGAE
from nose_exclude import NoseExclude
import re

import os

os.environ['NOSE_WITH_NOSEEXCLUDE'] = "--exclude-dir=lib"
os.environ['NOSEEXCLUDE_DIRS'] = "./lib"
os.environ['NOSE_WHERE'] = "."
os.environ['NOSE_ALL_MODULES'] = "false"

config = matcher = None

try:
    config, matcher = dev_appserver.LoadAppConfig(".", {})
except yaml_errors.EventListenerError, e:
    logging.error('Fatal error when loading application configuration:\n' +
                                    str(e))
except dev_appserver.InvalidAppConfigError, e:
    logging.error('Application configuration file invalid:\n%s', e)

dev_appserver.SetupStubs(config.application, **dev_appserver_main.DEFAULT_ARGS)
os.environ['APPLICATION_ID'] = config.application

# Run the test on the current directory
import sys
sys.argv[1] = "."

main(plugins=[NoseGAE(), NoseExclude()])

