#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Remove any Characters that Indicate List Delimitation """


from baseblock.common_utils import odds_of

from baseblock import BaseObject


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

        return input_text
