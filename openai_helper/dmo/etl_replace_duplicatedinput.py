#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Replace any Input that is Quoted in the Output Text """


from baseblock.common_utils import odds_of

from baseblock import BaseObject


class EtlReplaceDuplicatedInput(BaseObject):
    """ Replace any Input that is Quoted in the Output Text """

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
