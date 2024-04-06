import pprint
import unittest

from contents_reader import ContentsReader


class MyTestCase(unittest.TestCase):
    def setUp(self):
        root_folder = '../maildir'
        self.reader = ContentsReader(root_folder)

    def test_read_all_files(self):
        contents = self.reader .read_all_files()
        for content in contents:
            word_count = len(content.split())
            pprint.pp(f"{word_count}: {content}")
            print()

        self.assertNotEqual(contents, None)


if __name__ == '__main__':
    unittest.main()
