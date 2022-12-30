# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openai_helper', 'openai_helper.bp', 'openai_helper.dmo', 'openai_helper.svc']

package_data = \
{'': ['*']}

install_requires = \
['baseblock', 'openai>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'openai-helper',
    'version': '0.1.26',
    'description': 'OpenAI Helper for Easy I/O',
    'long_description': '# OpenAI-Helper\nOpenAI Helper for Easy I/O\n\n## Github\nhttps://github.com/craigtrim/openai-helper\n\n## Usage\n\n###  Set the OpenAI credentials\n```python\nimport os\nos.environ[\'OPENAI_KEY\'] = "<encrypted key>"\nos.environ[\'OPENAI_ORG\'] = "<encrypted key>"\n```\n\nUse `CryptoBase.encrypt_str("...")` from https://pypi.org/project/baseblock/\n\n###  Initialize the OpenAI Helper:\n```python\nrun = OpenAICompletion().run\n```\nThis will connect to OpenAI and establish performant callbacks.\n\n### Call OpenAI:\n```python\nrun(input_prompt="Generate a one random number between 1 and 5000")\n```\n\nor\n```python\nrun(engine="text-ada-001",\n    temperature=1.0,\n    max_tokens=256,\n    input_prompt="Rewrite the input in grammatical English:\\n\\nInput: You believe I can help you understand what trust yourself? don\'t you?\\nOutput:\\n\\n")\n```\n\nThe output will contain both the input and output values:\n```json\n{\n   "input":{\n      "best_of":1,\n      "engine":"text-davinci-003",\n      "frequency_penalty":0.0,\n      "input_prompt":"Rewrite the input in grammatical English:\\n\\nInput: You believe I can help you understand what trust yourself? don\'t you?\\nOutput:\\n\\n",\n      "max_tokens":256,\n      "presence_penalty":2,\n      "temperature":1.0,\n      "timeout":5,\n      "top_p":1.0\n   },\n   "output":{\n      "choices":[\n         {\n            "finish_reason":"stop",\n            "index":0,\n            "logprobs":"None",\n            "text":"Don\'t you believe that I can help you understand trust in yourself?"\n         }\n      ],\n      "created":1659051242,\n      "id":"cmpl-5Z7IwXM5bCwWj8IuHaGnOLn6bCvHz",\n      "model":"text-ada-001",\n      "object":"text_completion",\n      "usage":{\n         "completion_tokens":17,\n         "prompt_tokens":32,\n         "total_tokens":49\n      }\n   }\n}\n```\n\n## Supported Parameters and Defaults\nThis method signature describes support:\n```python\ndef process(self,\n            input_prompt: str,\n            engine: str = None,\n            best_of: int = None,\n            temperature: float = None,\n            max_tokens: int = None,\n            top_p: float = None,\n            frequency_penalty: int = None,\n            presence_penalty: int = None) -> dict:\n    """ Run an OpenAI event\n\n    Args:\n        input_prompt (str): The Input Prompt to execute against OpenAI\n        engine (str, optional): The OpenAI model (engine) to run against. Defaults to None.\n            Options as of July, 2022 are:\n                \'text-davinci-003\'\n                \'text-curie-001\',\n                \'text-babbage-001\'\n                \'text-ada-001\'\n        best_of (int, optional): Generates Multiple Server-Side Combinations and only selects the best. Defaults to None.\n            This can really eat up OpenAI tokens so use with caution!\n        temperature (float, optional): Control Randomness; Scale is 0.0 - 1.0. Defaults to None.\n            Scale is 0.0 - 1.0\n            Lower values approach predictable outputs and determinate behavior\n            Higher values are more engaging but also less predictable\n            Use High Values cautiously\n        max_tokens (int, optional): The Maximum Number of tokens to generate. Defaults to None.\n            Requests can use up to 4,000 tokens (this takes the length of the input prompt into account)\n            The higher this value, the more each request will cost.\n        top_p (float, optional): Controls Diversity via Nucleus Sampling. Defaults to None.\n            no idea what this means\n        frequency_penalty (int, optional): How much to penalize new tokens based on their frequency in the text so far. Defaults to None.\n            Scale: 0.0 - 2.0.\n        presence_penalty (int, optional): Seems similar to frequency penalty. Defaults to None.\n\n    Returns:\n        dict: an output dictionary with two keys:\n            input: the input dictionary with validated parameters and default values where appropriate\n            output: the output event from OpenAI\n    """\n```\n',
    'author': 'Craig Trim',
    'author_email': 'craigtrim@gmail.com',
    'maintainer': 'Craig Trim',
    'maintainer_email': 'craigtrim@gmail.com',
    'url': 'https://github.com/craigtrim/openai-helper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)
