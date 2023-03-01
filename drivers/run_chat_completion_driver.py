#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Integration Test """


from pprint import pprint

from baseblock import Enforcer

from openai_helper.bp import OpenAIChatCompletion
from openai_helper import chat


def test_completion_1():

    bp = OpenAIChatCompletion()
    assert bp

    d_result = bp.run(
        input_prompt="You are a sarcastic assistant",
        messages=[
            "Who won the world series in 2020?",
            "The Los Angeles Dodgers won the World Series in 2020.",
            "Where was it played?",
        ])

    pprint(d_result)
    Enforcer.keys(d_result, 'input', 'output')


def test_completion_2():

    output = chat(
        input_prompt="You are a sarcastic assistant",
        messages=[
            "Who was the 42nd President of the United States?",
            "Bill Clinton was the 42nd President",
            "What did he have in common with Lisa Simpson?",
        ])

    pprint(output)
    Enforcer.is_str(output)


def main():
    from drivers import IntegrationWrapper
    wrapper = IntegrationWrapper()

    # wrapper.call(test_completion_1)
    wrapper.call(test_completion_2)

    wrapper.deconstruct_env()


if __name__ == '__main__':
    main()
