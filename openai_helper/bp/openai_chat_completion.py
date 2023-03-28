#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Run a Chat Completion against OpenAI """


from typing import List
from typing import Optional
from typing import Callable

from baseblock import EnvIO
from baseblock import Enforcer
from baseblock import BaseObject

from openai_helper.dmo import OpenAIConnector
from openai_helper.svc import RunChatCompletion
from openai_helper.dmo import NoOpenAIEvent


class OpenAIChatCompletion(BaseObject):
    """ Run a Chat Completion against OpenAI """

    __run = None

    def __init__(self):
        """ Change Log

        Created:
            1-Mar-2023
            craigtrim@gmail.com
            *   https://github.com/craigtrim/openai-helper/issues/9
        """
        BaseObject.__init__(self, __name__)

    def _run(self) -> Callable:
        if not self.__run:
            openai = OpenAIConnector().process()
            self.__run = RunChatCompletion(openai).process
        return self.__run

    def run(self,
            input_prompt: str,
            messages: List[str],
            model: Optional[str] = 'gpt-3.5-turbo') -> dict:
        """ Run an OpenAI event

        Args:
            input_prompt (str): a defined input prompt

                Sample Input Prompt:
                    "You are a helpful assistant."

            messages (List[str]): The messages to execute the chat completion upon

                Sample Messages:
                    [
                        "Who won the world series in 2020?",
                        "The Los Angeles Dodgers won the World Series in 2020.",
                        "Where was it played?"
                    ]

                There should be an odd-number of messages in the list, with
                    odd-numbered entries as user questions
                    even-numbered entries as system responses

            model (str): the model to use

        Returns:
            dict: an output dictionary with two keys:
                input: the input dictionary with validated parameters and default values where appropriate
                output: the output event from OpenAI
                    Unless RateLimitError, PermissionError, AuthenticationError, ServiceUnavailableError
                    -   each of these errors is gracefully handled, and a dictionary result is still returned with 'output:None'
                    This service will not catch Exception or Error classes generally
                    -   the door is still left open for these and other error types to be thrown
                        and the consumer must plan for this eventuality
        """

        if not EnvIO.is_true('USE_OPENAI'):
            return NoOpenAIEvent().process(input_prompt, None)

        if self.isEnabledForDebug:
            Enforcer.is_str(input_prompt)

        d_result = self._run()(
            model=model,
            messages=messages,
            input_prompt=input_prompt,
        )

        if self.isEnabledForDebug:
            Enforcer.keys(d_result, 'input', 'output')

        return d_result
