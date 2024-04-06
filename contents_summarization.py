import os
import warnings

import backoff
import ratelimit
from google.api_core import exceptions
from vertexai.language_models import TextGenerationModel

warnings.filterwarnings("ignore")


class ContentsSummarization:
    def __init__(self, word_count_max=100, gac_path=None):
        if gac_path is not None:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = gac_path

        self.word_count_max = word_count_max
        self.generation_model = TextGenerationModel.from_pretrained("text-bison@001")
        self.CALL_LIMIT = 20  # Number of calls to allow within a period
        self.ONE_MINUTE = 60  # One minute in seconds
        self.FIVE_MINUTE = 5 * self.ONE_MINUTE

        self.initial_summary = []

        self.prompt_template = """
            Write a concise summary of the following text delimited by triple backquotes.
            Return your response in bullet points which covers the key points of the text.

            ```{text}```

            BULLET POINT SUMMARY:
        """

        self.initial_prompt_template = """
            Write a concise summary of the following text delimited by triple backquotes.

            ```{text}```

            CONCISE SUMMARY:
        """

        self.final_prompt_template = """
            Write a concise summary of the following text delimited by triple backquotes.
            Return your response in bullet points which covers the key points of the text.

            ```{text}```

            BULLET POINT SUMMARY:
        """

        # A function to print a message when the function is retrying
        def backoff_handler(details):
            print(
                "Backing off {} seconds after {} tries".format(
                    details["wait"], details["tries"]
                )
            )

        @backoff.on_exception(  # Retry with exponential backoff strategy when exceptions occur
            backoff.expo,
            (
                    exceptions.ResourceExhausted,
                    ratelimit.RateLimitException,
            ),  # Exceptions to retry on
            max_time=self.FIVE_MINUTE,
            on_backoff=backoff_handler,  # Function to call when retrying
        )
        @ratelimit.limits(  # Limit the number of calls to the model per minute
            calls=self.CALL_LIMIT, period=self.ONE_MINUTE
        )
        # This function will call the `generation_model.predict` function, but it will retry if defined exceptions occur.
        def model_with_limit_and_backoff(**kwargs):
            return self.generation_model.predict(**kwargs)

    def summarize(self, content_to_summarize, template=None):
        word_count = len(content_to_summarize.split())
        if word_count > self.word_count_max:
            return self.summarize_large_contents(content_to_summarize)

        # Define the prompt using the prompt template
        if template is None:
            prompt = self.prompt_template.format(text=content_to_summarize)
        else:
            prompt = template.format(text=content_to_summarize)

        # Use the model to summarize the text using the prompt
        summary = self.generation_model.predict(prompt=prompt, max_output_tokens=1024).text
        return summary

    def summarize_large_contents(self, content_to_summarize):
        """
        MapReduce
        :param content_to_summarize:
        :return:
        """

        # Map Part
        # Create an empty list to store the summaries
        initial_summary = []

        # Get chunks of words form large contents
        chunks = self.split_large_content(content_to_summarize)
        for chunk in chunks:
            # Generate a summary using the model and the prompt
            summary = self.summarize(chunk, template=self.initial_prompt_template)
            # Append the summary to the list of summaries
            initial_summary.append(summary)

        # Reduce Part
        # Concatenate the summaries from the initial step
        concat_summary = "\n".join(initial_summary)
        summary = self.summarize(concat_summary, template=self.final_prompt_template)
        return summary

    def split_large_content(self, large_content):
        # Split the content into words
        words = large_content.split()
        # Initialize an empty list to hold the chunks of words
        chunks = []

        # Iterate over the words in chunks of `words_per_chunk`
        for i in range(0, len(words), self.word_count_max):
            # Slice the words list to get a chunk and join it into a string
            chunk = ' '.join(words[i:i + self.word_count_max])
            # Add the string to the chunks list
            chunks.append(chunk)

        return chunks
