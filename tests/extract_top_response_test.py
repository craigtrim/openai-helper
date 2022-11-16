#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from openai_helper.svc import ExtractTopResponse


def test_service():

    svc = ExtractTopResponse()
    assert svc


def main():
    test_service()


if __name__ == '__main__':
    main()
