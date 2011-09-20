"""Loading unittests."""

import os
import re
import sys
import traceback
import types
import unittest

from fnmatch import fnmatch

from unittest2 import case, suite, loader

try:
    from os.path import relpath
except ImportError:
    from unittest2.compatibility import relpath

__unittest = True

    

class TestLoader(loader.TestLoader):
    """
    This class is responsible for loading tests according to various criteria
    and returning them wrapped in a TestSuite
    """

    def _match_path(self, path, full_path, pattern):
        if fnmatch(full_path, '*/local/*') or fnmatch(full_path, '*/lib/*'):
            return False
        return fnmatch(path, pattern)
    


defaultTestLoader = TestLoader()
