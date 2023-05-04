from typing import List
from typing import Union
from typing import Optional
from baseblock import EnvIO
from baseblock import Enforcer
from .bp import *
from .svc.extract_primary_topic import ExtractPrimaryTopic
from .svc import *
from .dmo import *
from .bp.openai_text_completion import OpenAITextCompletion
from .bp.openai_chat_completion import OpenAIChatCompletion
from .dmo import OutputExtractorText
from .dmo import OutputExtractorChat
from .dmo import InputTokenCounter
import logging
logger = logging.getLogger(__name__)

token_counter = InputTokenCounter().process


def num_of_tokens(messages: List[str] or str,
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
    return token_counter(messages=messages, model=model)


def chat(input_prompt: str,
         messages: Optional[Union[List[str], str]] = None,
         remove_emojis: bool = True,
         model: Optional[str] = 'gpt-3.5-turbo') -> Optional[str]:
    """ Call OpenAI Chat Completion

    Args:
        input_prompt (str): a defined input prompt

            Sample Input Prompt:
                "You are a helpful assistant."

        messages (Optional[Union[List[str], str]]): The optional messages to execute the chat completion upon

            Sample Messages (Dialog):
                [
                    "Who won the world series in 2020?",
                    "The Los Angeles Dodgers won the World Series in 2020.",
                    "Where was it played?"
                ]

                There should be an odd-number of messages in the list, with
                    odd-numbered entries as user questions
                    even-numbered entries as system responses

            Sample Messages
                [
                    "Who won the world series in 2020?",
                ]

                A single entry means this model can be used as a text completion, much like 'text-davinci-003'


            Sample Messages
                None

                The system will respond entirely based on the prompt if no input is provided.


        remove_emojis (bool, optional): remove any emojis OpenAI might provide. Defaults to True.
            Reference:
                https://github.com/craigtrim/openai-helper/issues/8

        model (str, optional): The model name to use.  Defaults to 'gpt-3.5-turbo'

    Returns:
        Optional[str]: the result (if any)
    """
    try:

        if not EnvIO.exists_as_true('USE_OPENAI'):
            return None

        if messages is None:
            messages = ['']
        elif type(messages) == str:
            messages = [messages]

        if logger.isEnabledFor(logging.DEBUG):
            Enforcer.is_list_of_str(messages)

        bp = OpenAIChatCompletion()

        d_result = bp.run(
            model=model,
            messages=messages,
            input_prompt=input_prompt,
        )

        if not d_result or not d_result['output']:
            return None

        result = OutputExtractorChat().process(
            input_text=input_prompt,
            d_result=d_result,
            remove_emojis=remove_emojis)

        if logger.isEnabledFor(logging.DEBUG):
            logging.getLogger(__name__).debug('\n'.join([
                'OpenAI Call Completed',
                f'\tInput Prompt: {input_prompt}',
                f'\tMessages: {messages}',
                f'\tResult: {result}']))

        return result

    except Exception as e:
        print(e)


# def call(input_prompt: str,
#          max_tokens: int = 256,
#          temperature: float = 0.7,
#          remove_emojis: bool = True,
#          engine: str = 'text-davinci-003') -> Optional[str]:
#     """ Call OpenAI Text Completion

#     Args:
#         input_prompt (str): a defined input prompt
#         max_tokens (int, optional): max tokens to use. Defaults to 256.
#         temperature (float, optional): the temperature. Defaults to 0.7.
#         remove_emojis (bool, optional): remove any emojis OpenAI might provide. Defaults to True.
#         engine (str, optional): the LLM engine. Defaults to 'text-davinci-003'.

#     Returns:
#         Optional[str]: the result (if any)
#     """

#     if not EnvIO.exists_as_true('USE_OPENAI'):
#         return None

#     bp = OpenAITextCompletion()

#     d_result = bp.run(
#         input_prompt=input_prompt,
#         engine=engine,
#         temperature=temperature,
#         max_tokens=max_tokens)

#     if not d_result or not d_result['output']:
#         return None

#     return OutputExtractorText().process(
#         input_text=input_prompt,
#         d_result=d_result,
#         remove_emojis=remove_emojis)


def call2(input_prompt: str,
          remove_emojis: Optional[bool] = True,
          engine: Optional[str] = 'text-davinci-003',
          temperature: Optional[float] = 1.0) -> Optional[str]:
    """ Call OpenAI

    Not a very creative function name, but basically 'full-auto' call

    Args:
        input_prompt (str): a defined input prompt
        remove_emojis (bool, optional): remove any emojis OpenAI might provide. Defaults to True.
            Reference:
                https://github.com/craigtrim/openai-helper/issues/8
        engine (str, optional): the LLM engine. Defaults to 'text-davinci-003'.
        temperature (float, optional): the temperature. Defaults to 1.0.

    Returns:
        Optional[str]: the result (if any)
    """

    try:

        bp = OpenAITextCompletion()

        d_result = bp.run(
            input_prompt=input_prompt,
            engine=engine,
            temperature=temperature)

        result = OutputExtractorText().process(
            input_text=input_prompt,
            d_result=d_result,
            remove_emojis=remove_emojis)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('\n'.join([
                'OpenAI Call Completed',
                f'\tInput Prompt: {input_prompt}',
                f'\tEngine: {engine}',
                f'\tTemperature: {temperature}',
                f'\tResult: {result}']))

        return result

    except Exception:
        pass
