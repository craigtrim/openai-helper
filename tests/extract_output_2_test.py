#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from baseblock import Enforcer

from openai_helper.bp import ExtractOutput


def test_extract_output():

    # test null inputs
    # https://github.com/craigtrim/openai-helper/issues/4

    assert not ExtractOutput().process(
        input_text=None,
        d_result=None)

    assert not ExtractOutput().process(
        input_text="this is a test",
        d_result=None)

    assert not ExtractOutput().process(
        input_text=None,
        d_result={})

    assert not ExtractOutput().process(
        input_text="this is a test",
        d_result={"input": "this is a test"})

    assert not ExtractOutput().process(
        input_text="this is a test",
        d_result={"input": "this is a test",
                  "output": None})

    assert not ExtractOutput().process(
        input_text="this is a test",
        d_result={"input": "this is a test",
                  "output": {}})

    assert not ExtractOutput().process(
        input_text="this is a test",
        d_result={"input": "this is a test",
                  "output": {
                      "choices": None
                  }})

    assert not ExtractOutput().process(
        input_text="this is a test",
        d_result={"input": "this is a test",
                  "output": {
                      "choices": []
                  }})

    assert not ExtractOutput().process(
        input_text="this is a test",
        d_result={"input": "this is a test",
                  "output": {
                      "choices": [{
                          "text": None
                      }]
                  }})


def main():
    test_extract_output()


if __name__ == '__main__':
    main()
