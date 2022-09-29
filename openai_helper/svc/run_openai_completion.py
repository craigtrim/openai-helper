#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Run a Completion against openAI """


from pprint import pformat

from baseblock import EnvIO
from baseblock import Enforcer
from baseblock import Stopwatch
from baseblock import BaseObject

from openai_helper.dmo import CompletionEventExtractor


class RunOpenAICompletion(BaseObject):
    """ Run a Completion against openAI """

    def __init__(self,
                 conn: object,
                 timeout: int = 5):
        """ Change Log

        Created:
            28-Jul-2022
            craigtrim@gmail.com

        Args:
            conn (object): a connected instance of OpenAI
            timeout (int, optional): the timeout for the API call. Defaults to 15.
        """
        BaseObject.__init__(self, __name__)
        self._completion = conn.Completion.create
        self._extract_event = CompletionEventExtractor().process
        self._timeout = EnvIO.int_or_default(
            'OPENAI_CREATE_TIMEOUT', timeout)  # GRAFFL-380

    def _process(self,
                 d_event: dict) -> dict:

        response = self._completion(
            engine=d_event['engine'],
            prompt=d_event['input_prompt'],
            temperature=d_event['temperature'],
            max_tokens=d_event['max_tokens'],
            top_p=d_event['top_p'],
            best_of=d_event['best_of'],
            frequency_penalty=d_event['frequency_penalty'],
            presence_penalty=d_event['presence_penalty'],
            timeout=self._timeout  # GRAFFL-380
        )

        d_result = dict(response)
        if self.isEnabledForDebug:
            Enforcer.is_dict(d_event)
            self.logger.debug('\n'.join([
                "OpenAI Call Completed",
                pformat(d_result)]))

        return {
            'input': d_event,
            'output': d_result
        }

    def process(self,
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

        sw = Stopwatch()

        d_params = self._extract_event(
            input_prompt=input_prompt,
            engine=engine,
            best_of=best_of,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty)

        d_result = self._process(d_params)

        self.logger.debug('\n'.join([
            "OpenAI Event Execution Completed",
            f"\tTotal Time: {str(sw)}",
            f"\tInput Params:\n{pformat(d_params)}",
            f"\tOutput Result:\n{pformat(d_result)}"]))

        return d_result
