#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Integration Test """


from baseblock import Enforcer

from openai_helper.bp import OpenAICustomModel


def test_custom_model():

    johnkao_model_name = "file-N2QMp92F0kkETGSdknISails"

    bp = OpenAICustomModel(johnkao_model_name)
    assert bp

    d_result = bp.process("How can I be successful in business?")
    Enforcer.keys(d_result, 'events', 'text')


def main():
    from drivers import IntegrationWrapper
    wrapper = IntegrationWrapper()

    wrapper.call(test_custom_model)

    wrapper.deconstruct_env()


if __name__ == "__main__":
    main()
