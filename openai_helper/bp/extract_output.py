#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" A Generic Service to Extract Unstructured Output from an OpenAI response """


from cgitb import text
from pprint import pformat
from baseblock.common_utils import odds_of

from baseblock import Stopwatch
from baseblock import BaseObject


class ExtractOutput(BaseObject):
    """ A Generic Service to Extract Unstructured Output from an OpenAI response """

    def __init__(self):
        """
        Created:
            17-Mar-2022
            craig@bast.ai
            *   in pursuit of
                https://github.com/grafflr/graffl-core/issues/222
        Updated:
            18-Mar-2022
            craig@bast.ai
            *   handle text completions
                https://github.com/grafflr/graffl-core/issues/224
        Updated:
            4-Aug-2022
            craig@bast.ai
            *   migrated to 'openai-helper' in pursuit of
                https://bast-ai.atlassian.net/browse/COR-56
                https://github.com/craigtrim/openai-helper/issues/1
        """
        BaseObject.__init__(self, __name__)

    @staticmethod
    def _handle_text_completions(input_text: str,
                                 output_text: str) -> str:
        """ Handle Situations where OpenAI tries to complete a User Sentence
        These are not imperative to resolve, but resolution frequently results in cleaner output

        Args:
            input_text (str): the user input text
            output_text (str): the current state of the extracted text from OpenAI

        Returns:
            str: the potentially modified output text
        """

        # this represents openAI trying to complete a user sentence
        # openAI will generally do this if the user does not terminate their input with punctuation like .!?
        # graffl now adds ending punctuation where none exists, so this pattern rarely takes place ...
        if output_text.startswith(' ') and '\n\n' in output_text:
            response = output_text.split('\n\n')[-1].strip()
            if response and len(response):
                return response

        # this is more common and seems to represent another form of text completion
        # an example is "0\n\nI'm not sure what you're asking"
        # the text prior to the response tends to be brief
        if '\n\n' in output_text:
            lines = output_text.split('\n\n')
            lines = [x.strip() for x in lines if x]
            lines = [x for x in lines if len(x) > 5]
            output_text = ' '.join(lines)
            while '  ' in output_text:
                output_text = output_text.replace('  ', ' ')

        return output_text

    @staticmethod
    def _output_text(d_result: dict) -> str:
        if 'choices' in d_result['output']:
            choices = d_result['output']['choices']

            if len(choices):
                output_text = choices[0]['text'].strip()
                output_text = output_text.split('\n')[-1].strip()

                return output_text

        return None

    @staticmethod
    def _replace_input(input_text: str,
                       output_text: str) -> str:
        """ Sometimes the Input is Quoted in the Output Text

        Sample Input: 
            We are not put in this world for mere pleasure alone.

        Sample Output: 
            We are not put in this world for mere pleasure alone.  Sometimes, we must suffer through pain and hardship to grow and become stronger.

        Desired Output: 
            Sometimes, we must suffer through pain and hardship to grow and become stronger.

        Args:
            input_text (str): the user input text
            output_text (str): the openAI response text

        Returns:
            str: the output text
        """

        if input_text in output_text and input_text != output_text:
            if odds_of(90):
                output_text = output_text.replace(input_text, '')

        return output_text

    @staticmethod
    def _remove_indicators(input_text: str,
                           output_text: str) -> str:
        """ Eliminate Annoying Situations where OpenAI responds with something like
            'Human: blah blah' 
        or
            'Assistant: blah blah'

        Args:
            input_text (str): the user input text
            output_text (str): the current state of the extracted text from OpenAI

        Returns:
            str: the potentially modified output text
        """

        indicators = ['User:', 'Human:', 'Assistant:']

        for indicator in indicators:
            if indicator in output_text:
                output_text = output_text.split(indicator)[-1].strip()

        if 'User:' in output_text:
            output_text = output_text.replace('User:', '').strip()

        if 'Human:' in output_text:
            output_text = output_text.replace('Human:', '').strip()

        if 'Assistant:' in output_text:
            return output_text.replace('Assistant:', '').strip()

        if 'AI:' in output_text:
            return output_text.replace('AI:', '').strip()

        if 'Marv:' in output_text:
            output_text = output_text.replace('Marv:', '').strip()

        if "Marv's" in output_text:
            output_text = output_text.replace("Marv's", "its")

        if 'Two-Sentence Horror Story:' in output_text:
            output_text = output_text.replace(
                'Two-Sentence Horror Story:', '').strip()

        return output_text

    def _replace_cliched_text(self,
                              input_text: str,
                              output_text: str) -> str:
        """ Replace Cliched Responses, which just add noise to the output

        Args:
            input_text (str): the user input text
            output_text (str): the current state of the extracted text from OpenAI

        Returns:
            str: the potentially modified output text
        """

        long_texts = [
            "and that's where Loqi comes in.",
            "If you're looking for a chatbot that will give you sassy responses to your questions",
            "look no further than Loqi",
            "He may not be the most helpful chatbot out there, but he's definitely the funniest",
            "Loqi is a chatbot that reluctantly answers questions in a mocking tone"
            "is a chatbot that responds to questions with",
            "is a chatbot that reluctantly answers questions",
        ]

        for long_text in long_texts:
            if long_text in output_text:
                output_text = output_text.replace(long_text, "")

        return output_text

    def process(self,
                input_text: str,
                d_result: dict) -> str or None:

        sw = Stopwatch()

        text_pipeline = [
            self._replace_input,
            self._handle_text_completions,
            self._remove_indicators,
            self._replace_cliched_text
        ]

        output_text = self._output_text(d_result)
        if not output_text or not len(output_text):
            return None

        for text_handler in text_pipeline:
            output_text = text_handler(input_text=input_text,
                                       output_text=output_text)
            if not output_text or not len(output_text):
                return None

        if self.isEnabledForDebug:
            self.logger.debug('\n'.join([
                "OpenAI Output Extraction Completed",
                f"\tTotal Time: {str(sw)}",
                f"\tInput Text: {input_text}",
                f"\tOutput Text: {output_text}"]))

        return output_text
