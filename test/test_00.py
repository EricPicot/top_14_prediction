# Test file created to manage the import problems due to
import sys
import os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import pytest
import unittest

class TestImportInitialisation(unittest.TestCase):

    def test_import_modules(self):
        assert True