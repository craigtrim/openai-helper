#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from openai_helper.bp import OpenAICompletion


def test_bp():

    bp = OpenAICompletion()
    assert bp


def main():
    test_bp()


if __name__ == '__main__':
    main()
