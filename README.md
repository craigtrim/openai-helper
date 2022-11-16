# OpenAI-Helper
OpenAI Helper for Easy I/O

## Github
https://github.com/craigtrim/openai-helper

## Usage

###  Set the OpenAI credentials
```python
import os
os.environ['OPENAI_KEY'] = "<encrypted key>"
os.environ['OPENAI_ORG'] = "<encrypted key>"
```

Use `CryptoBase.encrypt_str("...")` from https://pypi.org/project/baseblock/

###  Initialize the OpenAI Helper:
```python
run = OpenAICompletion().run
```
This will connect to OpenAI and establish performant callbacks.

### Call OpenAI:
```python
run(input_prompt="Generate a one random number between 1 and 5000")
```

or
```python
run(engine="text-ada-001",
    temperature=1.0,
    max_tokens=256,
    input_prompt="Rewrite the input in grammatical English:\n\nInput: You believe I can help you understand what trust yourself? don't you?\nOutput:\n\n")
```

The output will contain both the input and output values:
```json
{
   "input":{
      "best_of":1,
      "engine":"text-davinci-002",
      "frequency_penalty":0.0,
      "input_prompt":"Rewrite the input in grammatical English:\n\nInput: You believe I can help you understand what trust yourself? don't you?\nOutput:\n\n",
      "max_tokens":256,
      "presence_penalty":2,
      "temperature":1.0,
      "timeout":5,
      "top_p":1.0
   },
   "output":{
      "choices":[
         {
            "finish_reason":"stop",
            "index":0,
            "logprobs":"None",
            "text":"Don't you believe that I can help you understand trust in yourself?"
         }
      ],
      "created":1659051242,
      "id":"cmpl-5Z7IwXM5bCwWj8IuHaGnOLn6bCvHz",
      "model":"text-ada-001",
      "object":"text_completion",
      "usage":{
         "completion_tokens":17,
         "prompt_tokens":32,
         "total_tokens":49
      }
   }
}
```

## Supported Parameters and Defaults
This method signature describes support:
```python
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
```
