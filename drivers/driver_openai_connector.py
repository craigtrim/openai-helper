#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Integration Test """


from openai_helper.dmo import OpenAIConnector


def test_component():

    dmo = OpenAIConnector()
    assert dmo

    conn = dmo.process()
    assert conn


def main():
    from drivers import IntegrationWrapper
    wrapper = IntegrationWrapper()

    wrapper.call(test_component)

    wrapper.deconstruct_env()


if __name__ == "__main__":
    main()
