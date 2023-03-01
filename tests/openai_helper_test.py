#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from openai_helper.bp import OpenAITextCompletion


def test_bp():

    bp = OpenAITextCompletion()
    assert bp


def main():
    test_bp()


if __name__ == '__main__':
    main()
