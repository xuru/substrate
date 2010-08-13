
from nose.core import main, run
from nose.config import Config
from nosegae import NoseGAE
from nose_exclude import NoseExclude
import re

import os

#os.environ['NOSE_EXCLUDE'] = "nose"
#os.environ['EXCLUDE_DIR'] = "lib"
os.environ['NOSE_WITH_NOSEEXCLUDE'] = "--exclude-dir=lib"
os.environ['NOSEEXCLUDE_DIRS'] = "./lib"
os.environ['NOSE_WHERE'] = "."
os.environ['NOSE_ALL_MODULES'] = "false"

#main(plugins=[NoseGAE(), NoseExclude()], Config(exclude="[^\/]*/lib\/.*"))))
#main(plugins=[NoseGAE(), NoseExclude()], config=Config(exclude=(re.compile(r".*lib.*"),)))
#main(plugins=[NoseGAE(), NoseExclude()], config=Config(exclude=r".*lib.*"))
#main(plugins=[NoseGAE()])
main(plugins=[NoseGAE(), NoseExclude()])

