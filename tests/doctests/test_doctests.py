import os
import doctest
import unittest


DOCTEST_FILES = []

for root, dirs, files in os.walk("."):
    if ".hg%s" % os.path.sep not in root:
        for f in files:
            if f.endswith(".doctest"):
                DOCTEST_FILES.append(f)

DOCTEST_FILES = ["../../README.txt", "../../lib/restler/__init__.py"] + DOCTEST_FILES
print "Running ", DOCTEST_FILES

#DOCTEST_FILES = []
suite = unittest.TestSuite()
for f in DOCTEST_FILES:
    suite.addTest(doctest.DocFileSuite(f))
runner = unittest.TextTestRunner()
runner.run(suite)



