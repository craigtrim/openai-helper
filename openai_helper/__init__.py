import logging

from typing import Optional
from baseblock import EnvIO

from .bp import *
from .svc import *
from .dmo import *

from .bp.openai_completion import OpenAICompletion
from .bp.extract_output import ExtractOutput


def call(input_prompt: str,
         max_tokens: int = 256,
         temperature: float = 0.7) -> Optional[str]:
    """ Call OpenAI

    Args:
        input_prompt (str): a defined input prompt
        max_tokens (int, optional): max tokens to use. Defaults to 256.
        temperature (float, optional): the temperature. Defaults to 0.7.

    Returns:
        Optional[str]: the result (if any)
    """

    if not EnvIO.exists_as_true('USE_OPENAI'):
        return None

    bp = OpenAICompletion()

    d_result = bp.run(
        input_prompt=input_prompt,
        engine='text-davinci-003',
        temperature=temperature,
        max_tokens=max_tokens)

    if not d_result or not d_result['output']:
        return None

    return ExtractOutput().process(
        input_text=input_prompt,
        d_result=d_result)


def call2(input_prompt: str) -> Optional[str]:
    """ Call OpenAI

    Not a very creative function name, but basically 'full-auto' call

    Args:
        input_prompt (str): a defined input prompt

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
            temperature=1.0)

        logging.getLogger(__name__).debug('\n'.join([
            'OpenAI Call Completed',
            f'\tInput Prompt: {input_prompt}',
            f'\tMax Tokens: {max_tokens}',
            f'\tResult: {result}']))

        return result

    except Exception:
        pass
