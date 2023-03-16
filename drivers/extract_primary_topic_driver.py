#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Integration Test """


from openai_helper.svc import ExtractPrimaryTopic


def test_service():

    primary_topic = ExtractPrimaryTopic().process
    assert primary_topic

    result = primary_topic(
        "Our team has extensive experience and expertise in customizing Salesforce to meet unique business needs.")
    print(result)


def main():
    from drivers import IntegrationWrapper
    wrapper = IntegrationWrapper()

    wrapper.call(test_service)

    wrapper.deconstruct_env()


if __name__ == '__main__':
    main()
