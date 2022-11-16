#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from openai_helper.bp import OpenAICompletion


def test_orchestrator():
    assert OpenAICompletion()


def main():
    test_orchestrator()


if __name__ == '__main__':
    main()
