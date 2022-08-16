#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Query a Custom Model in OpenAI """


from random import sample

from baseblock import Stopwatch
from baseblock import BaseObject
from baseblock import ServiceEventGenerator


class ExtractTopResponse(BaseObject):
    """ Query a Custom Model in OpenAI """

    def __init__(self):
        """ Change Log

        Created:
            4-Aug-2022
            craigtrim@gmail.com
            *   refactored out of 'openai-custom-model' in pursuit of
                https://bast-ai.atlassian.net/browse/COR-94
        """
        BaseObject.__init__(self, __name__)
        self._generate_event = ServiceEventGenerator().process

    def _process(self,
                 results: list,
                 threshold: float) -> str:
        d_results = {}
        for result in results:
            if result['score'] >= threshold:
                d_results[result['score']] = result['text']

        if not len(d_results):
            return None

        if len(d_results) == 1:
            return list(d_results.values())[0]

        spread = max(d_results) - 10
        d_results = {score: d_results[score] for score in d_results
                     if score >= spread}

        results = list(d_results.values())
        if len(results) == 1:
            return results[0]

        return sample(results, 1)[0]

    def process(self,
                results: list,
                threshold: float):
        """ Return the Top Response

        In the case of multiple responses, and if the top responses are within a few % points of eachother
        then choose a top response at random; GRAFFL-371

        Args:
            results (list): the OpenAI search results
            threshold (float): the accuracy threshold to filter out results at. Defaults to 25.0.

        Returns:
            dict: the result
        """

        sw = Stopwatch()
        output_events = []

        output_text = self._process(results=results,
                                    threshold=threshold)

        output_events.append(self._generate_event(
            service_name=self.component_name(),
            event_name="extract-top-response",
            stopwatch=sw,
            data={
                'input_text': results,
                'threshold': threshold,
                'output_text': output_text,
            }))

        return {
            'text': output_text,
            'events': output_events
        }
