#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from baseblock import Enforcer

from openai_helper.bp import ExtractOutput


def test_extract_output():

    input_text = 'Who are you?'

    d_result = {
        'output': {
            'choices': [
                {
                    'text': 'Marv: I am a friendly chatbot!'
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


def main():
    test_extract_output()


if __name__ == '__main__':
    main()
