#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" A Generic Service to Extract Unstructured Output from an OpenAI response """


from baseblock import BaseObject


class EtlRemoveIndicators(BaseObject):
    """ A Generic Service to Extract Unstructured Output from an OpenAI response """

    def __init__(self):
        """ Change Log

        Created:
            4-Aug-2022
            craig@bast.ai
            *   https://bast-ai.atlassian.net/browse/COR-56
        """
        BaseObject.__init__(self, __name__)

    def process(self,
                input_text: str,
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
