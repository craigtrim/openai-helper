#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Integration Test """


from pprint import pprint

from baseblock import Enforcer

from openai_helper.bp import OpenAICompletion


def test_completion():

    bp = OpenAICompletion()
    assert bp

    bp.run(input_prompt="Generate a one random number between 1 and 5000")

    d_result = bp.run(
        engine="text-davinci-002",
        temperature=1.0,
        max_tokens=256,
        input_prompt="Rewrite the input in grammatical English:\n\nInput: You believe I can help you understand what trust yourself? don't you?\nOutput:\n\n")

    pprint(d_result)
    Enforcer.keys(d_result, 'input', 'output')


def main():
    from drivers import IntegrationWrapper
    wrapper = IntegrationWrapper()

    wrapper.call(test_completion)

    wrapper.deconstruct_env()


if __name__ == "__main__":
    main()
