#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from openai_helper.dmo import OpenAIConnector


def test_component():

    dmo = OpenAIConnector()
    assert dmo


def main():
    test_component()


if __name__ == '__main__':
    main()
