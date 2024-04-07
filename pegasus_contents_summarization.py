from nltk import sent_tokenize
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch
import pprint
import os
from transformers.file_utils import TRANSFORMERS_CACHE


class PegasusContentsSummarization:
    def __init__(self, model_name="google/pegasus-xsum", cache_dir=None):
        if cache_dir is not None:
            # Set TRANSFORMERS_CACHE environment variable to the specified cache directory
            os.environ["TRANSFORMERS_CACHE"] = cache_dir

        pprint.pp(f"Transformers cache directory: {TRANSFORMERS_CACHE}")

        """
        Initializes the PegasusContentsSummarization class with a specified model.

        :param model_name: Name of the model to use.
        :param cache_dir: Directory where the model & tokenizer are cached. If None, defaults to the transformers cache.
        """
        self.tokenizer = PegasusTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
        self.model = PegasusForConditionalGeneration.from_pretrained(model_name, cache_dir=cache_dir)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.to(self.device)

    def summarize(self, text, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True):
        """
        Summarizes the given text using the PEGASUS model.

        :param text: Text to summarize.
        :param max_length: The maximum length of the summary.
        :param min_length: The minimum length of the summary.
        :param length_penalty: Penalty for length.
        :param num_beams: Number of beams for beam search.
        :param early_stopping: Whether to stop when at least num_beams sentences are finished per batch.

        :return: The summarized text.
        """
        cleaned_text = self.preprocess_text(text)
        encoded_input = self.tokenizer(cleaned_text, return_tensors="pt", max_length=1024, truncation=True).to(self.device)
        summarized = self.model.generate(**encoded_input, max_length=max_length, min_length=min_length,
                                         length_penalty=length_penalty, num_beams=num_beams,
                                         early_stopping=early_stopping)
        summary_text = self.tokenizer.decode(summarized[0], skip_special_tokens=True)
        return summary_text

    def summarize_bullet_points(self, text, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True):
        """
        Summarizes the given text using the PEGASUS model and formats the summary as bullet points.

        :param text: Text to summarize.
        :param max_length: The maximum length of the summary.
        :param min_length: The minimum length of the summary.
        :param length_penalty: Penalty for length.
        :param num_beams: Number of beams for beam search.
        :param early_stopping: Whether to stop when at least num_beams sentences are finished per batch.

        :return: The summarized text formatted as bullet points.
        """
        cleaned_text = self.preprocess_text(text)
        encoded_input = self.tokenizer(cleaned_text, return_tensors="pt", max_length=1024, truncation=True).to(self.device)
        summarized = self.model.generate(**encoded_input, max_length=max_length, min_length=min_length,
                                         length_penalty=length_penalty, num_beams=num_beams,
                                         early_stopping=early_stopping)
        summary_text = self.tokenizer.decode(summarized[0], skip_special_tokens=True)

        # Split the summary into sentences and format as bullet points
        sentences = sent_tokenize(summary_text)
        bullet_points = '\n'.join([f"- {sentence}" for sentence in sentences])
        return bullet_points

    def preprocess_text(self, text):
        # Implement your logic here to clean and preprocess email text
        # This might involve removing headers, footers, HTML tags, attachments, etc.
        # You can use libraries like BeautifulSoup for HTML parsing
        cleaned_text = text
        return cleaned_text
