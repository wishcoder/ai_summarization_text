import pprint
import unittest
from contents_reader import ContentsReader
from contents_summarization import ContentsSummarization


class TestContentsSummarization(unittest.TestCase):
    def setUp(self):
        root_folder = '../maildir'
        self.reader = ContentsReader(root_folder)
        self.contents = self.reader.read_all_files()

        # Path to your service account key file
        service_account_key_path = '../key/wishcoder-ai-3f2a7eb7153a.json'
        self.contentsSummarization = ContentsSummarization(gac_path=service_account_key_path)

    def test_summarize(self):
        self.assertNotEqual(self.contents, None)
        self.assertNotEqual(self.contentsSummarization, None)
        summary = self.contentsSummarization.summarize(''.join(self.contents[:1]))
        pprint.pp(f"{summary}")
        self.assertNotEqual(summary, None)


if __name__ == '__main__':
    unittest.main()
