import unittest
from lib.tldr_cli import update_cache as update_cache

class TestProgressBar(unittest.TestCase):
    def update_once(self):
        # setting gens
        update_gen = update_cache()
        progress_gen = progress_bar.progress_bar(4)

        # updating progress
        for i in range(5):
            cur_progress: str = next(progress_gen)
            cur_update: str = next(update_gen)
            self.assertIsNotNone(cur_progress)
            self.assertIsNotNone(cur_update)

if __name__ == '__main__':
    unittest.main()