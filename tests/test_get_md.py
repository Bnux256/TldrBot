import unittest
import sys
import os
sys.path.append(os.getcwd())
from tldr.tldr import get_md

class getMd(unittest.TestCase):
    def get_en_common(self):
        self.assertIsNotNone(tldr.get_md('cd'))
    def get_fr_common(self):
        self.assertIsNotNone(tldr.get_md('cd', language='fr'))
    def get_fr_linux(self):
        self.assertIsNotNone(tldr.get_md('cd', 'linux', 'fr'))
    def get_not_exist(self):
        self.assertIsNone(tldr.get_md('aaa','linux', 'fr'))


if __name__ == '__main__':
    unittest.main()
