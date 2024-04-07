import unittest
import pprint
from contents_reader import ContentsReader
from pegasus_contents_summarization import PegasusContentsSummarization

#
# UserWarning: `huggingface_hub` cache-system uses symlinks by default to efficiently store duplicated files but your machine does not support them in C:\Users\WishCoder\.cache\huggingface\hub\models--google--pegasus-xsum. Caching files will still work but in a degraded version that might require more space on your disk. This warning can be disabled by setting the `HF_HUB_DISABLE_SYMLINKS_WARNING` environment variable. For more details, see https://huggingface.co/docs/huggingface_hub/how-to-cache#limitations.
# To support symlinks on Windows, you either need to activate Developer Mode or to run Python as an administrator. In order to see activate developer mode, see this article: https://docs.microsoft.com/en-us/windows/apps/get-started/enable-your-device-for-development
# warnings.warn(message)
#

import os

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"


# download model
# transformers-cli download google/pegasus-xsum
# from transformers.file_utils import cached_path, HF_DATASETS_CACHE, TRANSFORMERS_CACHE
#
# print("Transformers cache directory:", TRANSFORMERS_CACHE)
# print("Datasets cache directory:", HF_DATASETS_CACHE)

class TestPegasusContentsSummarization(unittest.TestCase):
    def setUp(self):
        root_folder = '../maildir'
        self.reader = ContentsReader(root_folder)
        self.contents = self.reader.read_all_files()
        self.contentsSummarization = PegasusContentsSummarization(cache_dir='../model/')

    def test_summarize(self):
        self.assertNotEqual(self.contents, None)
        self.assertNotEqual(self.contentsSummarization, None)
        summary = self.contentsSummarization.summarize(''.join(self.contents[:1]))
        pprint.pp(f"{summary}")
        self.assertNotEqual(summary, None)

    def test_summarize_bullet_points(self):
        self.assertNotEqual(self.contents, None)
        self.assertNotEqual(self.contentsSummarization, None)
        summary = self.contentsSummarization.summarize_bullet_points(''.join(self.contents[:1]))
        pprint.pp(f"{summary}")
        self.assertNotEqual(summary, None)


if __name__ == '__main__':
    unittest.main()
