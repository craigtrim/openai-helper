#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Extract and Validate Input Parameters """


from baseblock import EnvIO
from baseblock import Enforcer
from baseblock import BaseObject


class CompletionEventExtractor(BaseObject):
    """ Extract and Validate Input Parameters for an OpenAI Completion """

    def __init__(self,
                 timeout: int = 5):
        """ Change Log

        Created:
            28-Jul-2022
            craigtrim@gmail.com

        Args:
            timeout (int, optional): the timeout for the API call. Defaults to 15.
        """
        BaseObject.__init__(self, __name__)
        self._timeout = EnvIO.int_or_default(
            'OPENAI_CREATE_TIMEOUT', timeout)  # GRAFFL-380

    def process(self,
                input_prompt: str,
                engine: str = None,
                best_of: int = None,
                temperature: float = None,
                max_tokens: int = None,
                top_p: float = None,
                frequency_penalty: int = None,
                presence_penalty: int = None) -> dict:
        """ Extract and Validate the Inputs into a single dictionary

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
            dict: a dictinoary of validated inputs with default values (where appropriate)
        """

        def _input_prompt() -> str:
            """ The Input Prompt to execute against OpenAI

            Raises:
                ValueError: input prompt not given

            Returns:
                str: the input prompt to execute
            """
            if not 'input_prompt' or not len(input_prompt):
                raise ValueError('Prompt Input Required')

            if self.isEnabledForDebug:
                Enforcer.is_str(input_prompt)

            return input_prompt

        def _engine() -> str:
            """ The OpenAI model (engine) to run against

            Options as of July, 2022 are:
                'text-davinci-002'
                'text-curie-001',
                'text-babbage-001'
                'text-ada-001'

            Returns:
                str: the openAI engine
            """
            if engine and len(engine):
                if self.isEnabledForDebug:
                    Enforcer.is_str(engine)
                return engine

            # the best all-around engine as of July, 2022
            # but also the most expensive
            return 'text-davinci-002'

        def _best_of() -> int:
            """ Generates Multiple Server-Side Combinations and only selects the best
            This can really eat up OpenAI tokens so use with caution!

            Returns:
                int: the number of server-side combinations to generate
            """
            if best_of:
                if self.isEnabledForDebug:
                    Enforcer.is_int(best_of)
                return int(best_of)

            return 1

        def _temperature() -> float:
            """ Control Randomness; Scale is 0.0 - 1.0

            Lower values approach predictable outputs and determinate behavior
            Higher values are more engaging but also less predictable
            Use High Values cautiously

            Returns:
                float: the temperature
            """
            if temperature:
                if self.isEnabledForDebug:
                    Enforcer.is_float(temperature)
                    assert temperature >= 0.0
                    assert temperature <= 1.0
                return temperature

            # this seems to be a reasonable default
            return 0.7

        def _max_tokens() -> int:
            """ The Maximum Number of tokens to generate
            Requests can use up to 4,000 tokens (this takes the length of the input prompt into account)
            The higher this value, the more each request will cost

            Returns:
                int: the max tokens to generate
            """
            if max_tokens:
                if self.isEnabledForDebug:
                    Enforcer.is_int(max_tokens)
                return max_tokens

            # whether this is reasonable depends entirely on the input prompt
            return 256

        def _top_p() -> float:
            """ Controls Diversity via Nucleus Sampling; no idea what this means

            Returns:
                float: the top-p result
            """
            if top_p:
                return top_p

            # I rarely change this setting
            return 1.0

        def _frequency_penalty() -> int:
            """ How much to penalize new tokens based on their frequency in the text so far
            Scale: 0.0 - 2.0

            Returns:
                int: the frequency penalty
            """
            if frequency_penalty:
                return frequency_penalty
            return 0.0

        def _presence_penalty() -> int:
            """ Seems similar to frequency penalty

            Returns:
                int: the presence penalty
            """
            if presence_penalty:
                return presence_penalty
            return 2

        return {
            'engine': _engine(),
            'input_prompt': _input_prompt(),
            'temperature': _temperature(),
            'max_tokens': _max_tokens(),
            'top_p': _top_p(),
            'best_of': _best_of(),
            'frequency_penalty': _frequency_penalty(),
            'presence_penalty': _presence_penalty(),
            'timeout': self._timeout
        }
