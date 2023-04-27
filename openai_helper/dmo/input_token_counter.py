#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Count Tokens accurately with Tiktoken """


from typing import List

from tiktoken.core import Encoding
from tiktoken import encoding_for_model

from baseblock import BaseObject


class InputTokenCounter(BaseObject):
    """ Count Tokens accurately with Tiktoken

    Encoding Name       OpenAI Models
    cl100k_base	        gpt-4
                        gpt-3.5-turbo
                        text-embedding-ada-002
    p50k_base           Codex models
                        text-davinci-002
                        text-davinci-003
    r50k_base           GPT-3 models like davinci
    """

    __d_encoding = {}

    def __init__(self):
        """ Change Log

        Created:
            27-Mar-2023
            craigtrim@gmail.com
            *   https://github.com/craigtrim/openai-helper/issues/11
        """
        BaseObject.__init__(self, __name__)

    def _cached_model(self,
                      model: str) -> Encoding:
        if model not in self.__d_encoding:

            try:

                self.__d_encoding[model] = encoding_for_model(model)

            except KeyError:
                self.logger.error('\n'.join([
                    'Warning: model not found.',
                    f'\tUsing cl100k_base encoding.']))
                self.__d_encoding[model] = encoding_for_model(
                    'cl100k_base')

        return self.__d_encoding[model]

    def process(self,
                messages: List[str],
                model: str = 'gpt-3.5-turbo-0301') -> int:
        """ Count the Number of Tokens in an Input String

        Counting tokens is not the same as "tokenizing a string" and counting the result
        OpenAI has a different technique for arriving at this count and this varies by model

        Reference:
            https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb

        Args:
            messages (List[str] or str): a List of strings or simply an input string
            model (str, optional): the model to use for counting tokens. Defaults to "gpt-3.5-turbo-0301".
                token counting varies between models
                however, if you don't know your OpenAI model just leave this value at the default

        Returns:
            int: the total tokens
        """

        if type(messages) == str:
            messages = [messages]

        if not model or not len(model):
            model = 'gpt-3.5-turbo-0301'

        encoding = self._cached_model(model)

        if model == 'gpt-3.5-turbo':
            self.logger.warning(
                'Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.')
            return self.process(messages, model='gpt-3.5-turbo-0301')

        elif model == 'gpt-4':
            self.logger.warning(
                'Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.')
            return self.process(messages, model='gpt-4-0314')

        elif model == 'gpt-3.5-turbo-0301':
            # every message follows <|start|>{role/name}\n{content}<|end|>\n
            tokens_per_message = 4
            tokens_per_name = -1  # if there's a name, the role is omitted

        elif model == 'gpt-4-0314':
            tokens_per_message = 3
            tokens_per_name = 1

        else:
            # raise NotImplementedError(
            #     f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
            tokens_per_message = 4  # just some default ...

        num_tokens = 0
        for message in messages:
            num_tokens += tokens_per_message
            for message in messages:
                num_tokens += len(encoding.encode(message))

        num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
        return num_tokens
