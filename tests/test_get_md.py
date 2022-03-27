import unittest
import sys
import os
import lib.tldr_cli as tldr


class TestGetMd(unittest.TestCase):
    def test_get_en_common(self):
        self.assertIsNotNone(tldr.get_md('cd'), "en_common failed")

    def test_get_fr_common(self):
        self.assertIsNotNone(tldr.get_md('cd', language='fr'), "fr_common failed")

    def test_get_fr_linux(self):
        self.assertIsNotNone(tldr.get_md('ip', 'linux', 'fr'), "fr_linux failed")

    def test_get_not_exist(self):
        self.assertIsNone(tldr.get_md('aaa', 'linux', 'fr'), "shouldn't have failed")


if __name__ == '__main__':
    unittest.main()
