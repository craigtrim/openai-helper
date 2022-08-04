#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from baseblock import Enforcer

from openai_helper.bp import ExtractOutput


def extract_output(input_text: str):

    input_text = "Who are you?"

    d_result = {
        'output': {
            'choices': [
                {
                    'text': input_text
                }
            ]
        }
    }

    bp = ExtractOutput()
    assert bp

    result = bp.process(
        input_text=input_text,
        d_result=d_result)

    Enforcer.is_str(result)


def main(input_text):
    extract_output(input_text)


if __name__ == "__main__":
    import plac
    plac.call(main)
