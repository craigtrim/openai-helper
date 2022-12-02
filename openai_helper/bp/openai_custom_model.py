#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Query a Custom Model in OpenAI """


from typing import Optional

from functools import lru_cache

from baseblock import EnvIO
from baseblock import Stopwatch
from baseblock import BaseObject
from baseblock import Enforcer
from baseblock import ServiceEventGenerator

from openai_helper.svc import ExtractTopResponse
from openai_helper.svc import CreateOpenAIAnswer
from openai_helper.dmo import NoOpenAIEvent


class OpenAICustomModel(BaseObject):
    """ Query a Custom Model in OpenAI """

    def __init__(self,
                 model_name: str):
        """ Change Log

        Created:
            20-Apr-2022
            craigtrim@gmail.com
            *   https://github.com/grafflr/graffl-core/issues/303
        Updated:
            12-May-2022
            craigtrim@gmail.com
            *   https://github.com/grafflr/graffl-core/issues/371
        Updated:
            4-Aug-2022
            craigtrim@gmail.com
            *   refactored in pursuit of
                https://bast-ai.atlassian.net/browse/COR-57
        Updated:
            16-Aug-2022
            craigtrim@gmail.com
            *   refactor services into component parts in pursuit of
                https://bast-ai.atlassian.net/browse/COR-94

        Args:
            openai (object): an instantiation of openAI
            model_name (str): the name of the custom model to query
        """
        BaseObject.__init__(self, __name__)
        self._generate_event = ServiceEventGenerator().process
        self._query = CreateOpenAIAnswer(model_name).process
        self._extract_top_response = ExtractTopResponse().process

    @lru_cache
    def process(self,
                input_text: str,
                search_model: str = 'text-davinci-003',
                threshold: float = 25.0) -> Optional[tuple]:
        """ Call a custom OpenAI Model

        Args:
            input_text (str): the input text to send to OpenAI
            search_model (str): the model used to interpret the query and search
            threshold (float): the accuracy threshold for filtering results

        Returns:
            dict: the complete openAI event
        """

        if not EnvIO.is_true('USE_OPENAI'):
            return NoOpenAIEvent().process(input_text, search_model)

        if self.isEnabledForDebug:
            Enforcer.is_str(input_text)

        sw = Stopwatch()
        output_events = []

        d_query = self._query(
            input_text=input_text,
            search_model=search_model)

        [output_events.append(x) for x in d_query['events']]

        if not d_query['results']:
            return {
                'text': None,
                'events': output_events
            }

        d_top_response = self._extract_top_response(
            d_query['results']['selected_documents'],
            threshold=threshold)

        [output_events.append(x) for x in d_top_response['events']]

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                'OpenAI Service Completed',
                f'\tTotal Time: {str(sw)}',
                f'\tInput Text: {input_text.strip()}',
                f"\tOutput Text: {d_top_response['text']}"]))

        return {
            'text': d_top_response['text'],
            'events': output_events
        }
