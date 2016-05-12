# -*- coding: utf-8 -*-
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath('..'))
from beam_carbon.beam import BEAMCarbon


class BEAMCarbonTest(unittest.TestCase):

    def setUp(self):
        self.fixture = BEAMCarbon()

    def tearDown(self):
        del self.fixture

    def test_n(self):
        p = self.fixture.n
        self.failUnlessEqual(100, p)


if __name__ == '__main__':
    unittest.main()
