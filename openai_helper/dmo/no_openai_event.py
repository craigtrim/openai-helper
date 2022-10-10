#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Return a Null OpenAI Event """


from baseblock import Stopwatch
from baseblock import BaseObject
from baseblock import ServiceEventGenerator


class NoOpenAIEvent(BaseObject):
    """ Return a Null OpenAI Event """

    def __init__(self):
        """ Change Log

        Created:
            29-Sept-2022
            craigtrim@gmail.com
            *   refactored out of business process
        """
        BaseObject.__init__(self, __name__)
        self._generate_event = ServiceEventGenerator().process

    def process(self,
                input_text: str,
                search_model: str) -> dict:

        sw = Stopwatch()
        output_events = []

        output_events.append(self._generate_event(
            service_name=self.component_name(),
            event_name="openai",
            stopwatch=sw,
            data={
                'input_text': input_text,
                'search_model': search_model,
                'output_text': "*** OPENAI DISABLED ***"}))

        return {
            'text': None,
            'events': output_events
        }
