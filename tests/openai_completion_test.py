#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from openai_helper.bp import OpenAITextCompletion


def test_orchestrator():
    assert OpenAITextCompletion()


def main():
    test_orchestrator()


if __name__ == '__main__':
    main()
