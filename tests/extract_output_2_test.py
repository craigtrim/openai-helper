#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from openai_helper.dmo import OutputExtractorText


def test_extract_output():

    extract = OutputExtractorText().process
    assert extract

    # test null inputs
    # https://github.com/craigtrim/openai-helper/issues/4

    assert not extract(
        input_text=None,
        d_result=None)

    assert not extract(
        input_text='this is a test',
        d_result=None)

    assert not extract(
        input_text=None,
        d_result={})

    assert not extract(
        input_text='this is a test',
        d_result={'input': 'this is a test'})

    assert not extract(
        input_text='this is a test',
        d_result={'input': 'this is a test',
                  'output': None})

    assert not extract(
        input_text='this is a test',
        d_result={'input': 'this is a test',
                  'output': {}})

    assert not extract(
        input_text='this is a test',
        d_result={'input': 'this is a test',
                  'output': {
                      'choices': None
                  }})

    assert not extract(
        input_text='this is a test',
        d_result={'input': 'this is a test',
                  'output': {
                      'choices': []
                  }})

    assert not extract(
        input_text='this is a test',
        d_result={'input': 'this is a test',
                  'output': {
                      'choices': [{
                          'text': None
                      }]
                  }})


def main():
    test_extract_output()


if __name__ == '__main__':
    main()
