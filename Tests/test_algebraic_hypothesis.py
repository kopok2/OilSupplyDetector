# coding=utf-8
"""Test."""

import os
import sys
import unittest

TEST_DIR = os.path.dirname(__file__)
SRC_DIR = '../Source'
sys.path.insert(0, os.path.abspath(os.path.join(TEST_DIR, SRC_DIR)))

# import Module


class TestSuite(unittest.TestCase):
    def test_empty(self):
        pass


if __name__ == '__main__':
    unittest.main()
