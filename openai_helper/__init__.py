from .bp import *
from .svc import *
from .dmo import *

from .bp.openai_completion import OpenAICompletion
from .bp.extract_output import ExtractOutput


def call(input_prompt: str,
         max_tokens: int = 256,
         temperature: float = 0.7) -> str:

    bp = OpenAICompletion()

    d_result = bp.run(
        input_prompt=input_prompt,
        engine="text-davinci-002",
        temperature=temperature,
        max_tokens=max_tokens)

    return ExtractOutput().process(
        input_text=input_prompt,
        d_result=d_result)
