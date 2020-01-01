# coding=utf-8
"""Test."""

import os
import sys
import unittest

TEST_DIR = os.path.dirname(__file__)
SRC_DIR = '../Source'
sys.path.insert(0, os.path.abspath(os.path.join(TEST_DIR, SRC_DIR)))

import Example


class TestSuite(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(4, Example.add(1, 3))


if __name__ == '__main__':
    unittest.main()
