#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Format Chat Message Input """


from typing import List

from baseblock import Enforcer
from baseblock import BaseObject


class ChatMessageFormatter(BaseObject):
    """ Format Chat Message Input """

    def __init__(self):
        """ Change Log

        Created:
            1-Mar-2023
            craigtrim@gmail.com
            *   https://github.com/craigtrim/openai-helper/issues/9
            *   Official Documentation:
                https://platform.openai.com/docs/guides/chat/introduction
        """
        BaseObject.__init__(self, __name__)

    def process(self,
                input_prompt: str,
                messages: List[str]) -> List[str]:

        if self.isEnabledForDebug:
            Enforcer.is_str(input_prompt)
            Enforcer.is_list_of_str(messages)

        if len(messages) % 2 != 1:
            self.logger.error('\n'.join([
                "Expect Interaction Sequences in Odd-Numbered Multiples",
                f"\tActual Messages:\n{messages}"]))
            raise ValueError

        outputs = [
            {"role": "system", "content": input_prompt},
        ]

        for i in range(len(messages)):

            def get_role() -> str:
                if i % 2 == 0:
                    return "user"
                return "assistant"

            outputs.append({
                "role": get_role(),
                "content": messages[i]
            })

        return outputs
