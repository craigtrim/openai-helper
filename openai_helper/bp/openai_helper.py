#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Run a Completion against openAI """


from baseblock import BaseObject

from openai_helper.dmo import OpenAIConnector
from openai_helper.svc import RunOpenAIEvent


class OpenAIHelper(BaseObject):
    """ Run a Completion against openAI """

    def __init__(self):
        """ Change Log

        Created:
            28-Jul-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)
        conn = OpenAIConnector().process()
        self._run = RunOpenAIEvent(conn).process

    def run(self,
            input_prompt: str,
            engine: str = None,
            best_of: int = None,
            temperature: float = None,
            max_tokens: int = None,
            top_p: float = None,
            frequency_penalty: int = None,
            presence_penalty: int = None) -> dict:
        """ Run an OpenAI event

        Args:
            input_prompt (str): The Input Prompt to execute against OpenAI
            engine (str, optional): The OpenAI model (engine) to run against. Defaults to None.
                Options as of July, 2022 are:
                    'text-davinci-002'
                    'text-curie-001',
                    'text-babbage-001'
                    'text-ada-001'
            best_of (int, optional): Generates Multiple Server-Side Combinations and only selects the best. Defaults to None.
                This can really eat up OpenAI tokens so use with caution!
            temperature (float, optional): Control Randomness; Scale is 0.0 - 1.0. Defaults to None.
                Scale is 0.0 - 1.0
                Lower values approach predictable outputs and determinate behavior
                Higher values are more engaging but also less predictable
                Use High Values cautiously
            max_tokens (int, optional): The Maximum Number of tokens to generate. Defaults to None.
                Requests can use up to 4,000 tokens (this takes the length of the input prompt into account)
                The higher this value, the more each request will cost.            
            top_p (float, optional): Controls Diversity via Nucleus Sampling. Defaults to None.
                no idea what this means
            frequency_penalty (int, optional): How much to penalize new tokens based on their frequency in the text so far. Defaults to None.
                Scale: 0.0 - 2.0.
            presence_penalty (int, optional): Seems similar to frequency penalty. Defaults to None.

        Returns:
            dict: an output dictionary with two keys:
                input: the input dictionary with validated parameters and default values where appropriate
                output: the output event from OpenAI
        """
        return self._run(input_prompt=input_prompt,
                         engine=engine,
                         best_of=best_of,
                         temperature=temperature,
                         max_tokens=max_tokens,
                         top_p=top_p,
                         frequency_penalty=frequency_penalty,
                         presence_penalty=presence_penalty)
