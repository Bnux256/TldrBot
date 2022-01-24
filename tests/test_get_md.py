import unittest
import sys
import os
sys.path.append(os.getcwd())
from tldr.tldr import get_md

class getMd(unittest.TestCase):
    def get_en_common(self):
        self.assertIsNotNone(tldr.get_md('cd'), "en_common failed")
    def get_fr_common(self):
        self.assertIsNotNone(tldr.get_md('cd', language='fr'), "fr_common failed")
    def get_fr_linux(self):
        self.assertIsNotNone(tldr.get_md('cd', 'linux', 'fr'), "fr_linux failed")
    def get_not_exist(self):
        self.assertIsNone(tldr.get_md('aaa','linux', 'fr'), "shouldn't have failed")


if __name__ == '__main__':
    unittest.main()
