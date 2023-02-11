#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Remove any Characters that Indicate List Delimitation """


from baseblock.common_utils import odds_of

from baseblock import BaseObject


LINE_BREAK = '\n'


class EtlRemoveListIndicators(BaseObject):
    """ Remove any Characters that Indicate List Delimitation

        Sample Input:
            - item 1
            - item 2
            - item 3
        Sample Output:
            item 1
            item 2
            item 3

        Sample Input:
            1. item 1
            2. item 2
            3. item 3
        Sample Output:
            item 1
            item 2
            item 3

        Sample Input:
            1) item 1
            2) item 2
            3) item 3
        Sample Output:
            item 1
            item 2
            item 3

    Line breaks are still maintained
    """

    def __init__(self):
        """ Change Log

        Created:
            16-Nov-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/openai-helper/issues/2
        """
        BaseObject.__init__(self, __name__)

    @staticmethod
    def _strip_numbered_list(input_text: str) -> str:
        for i in range(1, 16):

            key = f'{i}:'
            if input_text.startswith(key):
                return input_text[len(key):].strip()

            key = f'{i}.'
            if input_text.startswith(key):
                return input_text[len(key):].strip()

            key = f'{i})'
            if input_text.startswith(key):
                return input_text[len(key):].strip()

            key = f'variation {i}:'
            if input_text.startswith(key):
                return input_text[len(key):].strip()

            key = f'variation {i}.'
            if input_text.startswith(key):
                return input_text[len(key):].strip()

            key = f'variation {i})'
            if input_text.startswith(key):
                return input_text[len(key):].strip()

        return input_text

    def process(self,
                input_text: str,
                output_text: str) -> str:
        """ Entry Point

        Args:
            input_text (str): the user input text
            output_text (str): the openAI response text

        Returns:
            str: the output text
        """

        if LINE_BREAK not in output_text:
            return output_text

        normalized = []

        lines = [x.strip() for x in output_text.split(LINE_BREAK)]
        for line in lines:

            if line.startswith('-'):
                normalized.append(line[1:].strip())
                continue

            if '.' in line:
                normalized.append(self._strip_numbered_list(line))
                continue

            normalized.append(line)

        normalized = [x.strip() for x in normalized if x and len(x.strip())]

        return LINE_BREAK.join(normalized)
