import logging

from typing import List
from typing import Optional
from baseblock import EnvIO

from .bp import *
from .svc import *
from .dmo import *

from .bp.openai_text_completion import OpenAITextCompletion
from .bp.openai_chat_completion import OpenAIChatCompletion
from .dmo import OutputExtractorText
from .dmo import OutputExtractorChat


def chat(input_prompt: str,
         messages: List[str],
         remove_emojis: bool = True) -> Optional[str]:
    """ Call OpenAI Chat Completion

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

        remove_emojis (bool, optional): remove any emojis OpenAI might provide. Defaults to True.
            Reference:
                https://github.com/craigtrim/openai-helper/issues/8

    Returns:
        Optional[str]: the result (if any)
    """
    try:

        if not EnvIO.exists_as_true('USE_OPENAI'):
            return None

        bp = OpenAIChatCompletion()

        d_result = bp.run(
            input_prompt=input_prompt,
            messages=messages)

        if not d_result or not d_result['output']:
            return None

        result = OutputExtractorChat().process(
            input_text=input_prompt,
            d_result=d_result,
            remove_emojis=remove_emojis)

        logging.getLogger(__name__).debug('\n'.join([
            'OpenAI Call Completed',
            f'\tInput Prompt: {input_prompt}',
            f'\tMessages: {messages}',
            f'\tResult: {result}']))

        return result

    except Exception as e:
        print(e)


def call(input_prompt: str,
         max_tokens: int = 256,
         temperature: float = 0.7,
         remove_emojis: bool = True) -> Optional[str]:
    """ Call OpenAI Text Completion

    Args:
        input_prompt (str): a defined input prompt
        max_tokens (int, optional): max tokens to use. Defaults to 256.
        temperature (float, optional): the temperature. Defaults to 0.7.
        remove_emojis (bool, optional): remove any emojis OpenAI might provide. Defaults to True.
            Reference:
                https://github.com/craigtrim/openai-helper/issues/8

    Returns:
        Optional[str]: the result (if any)
    """

    if not EnvIO.exists_as_true('USE_OPENAI'):
        return None

    bp = OpenAITextCompletion()

    d_result = bp.run(
        input_prompt=input_prompt,
        engine='text-davinci-003',
        temperature=temperature,
        max_tokens=max_tokens)

    if not d_result or not d_result['output']:
        return None

    return OutputExtractorText().process(
        input_text=input_prompt,
        d_result=d_result,
        remove_emojis=remove_emojis)


def call2(input_prompt: str,
          remove_emojis: bool = True) -> Optional[str]:
    """ Call OpenAI

    Not a very creative function name, but basically 'full-auto' call

    Args:
        input_prompt (str): a defined input prompt
        remove_emojis (bool, optional): remove any emojis OpenAI might provide. Defaults to True.
            Reference:
                https://github.com/craigtrim/openai-helper/issues/8

    Returns:
        Optional[str]: the result (if any)
    """

    max_tokens = len(input_prompt) * 2
    if max_tokens > 4000:
        return None

    try:

        result = call(
            input_prompt=input_prompt,
            max_tokens=max_tokens,
            temperature=1.0,
            remove_emojis=remove_emojis)

        logging.getLogger(__name__).debug('\n'.join([
            'OpenAI Call Completed',
            f'\tInput Prompt: {input_prompt}',
            f'\tMax Tokens: {max_tokens}',
            f'\tResult: {result}']))

        return result

    except Exception:
        pass
