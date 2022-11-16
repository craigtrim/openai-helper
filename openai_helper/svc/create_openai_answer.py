#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Craft an Answer from OpenAI """


from openai.error import InvalidRequestError

from baseblock import Stopwatch
from baseblock import BaseObject
from baseblock import ServiceEventGenerator

from openai_helper.dmo import OpenAIConnector


class CreateOpenAIAnswer(BaseObject):
    """ Craft an Answer from OpenAI """

    def __init__(self,
                 model_name: str):
        """ Change Log

        Created:
            16-Aug-2022
            craigtrim@gmail.com
            *   refactored out of 'openai-custom-model' in pursuit of
                https://bast-ai.atlassian.net/browse/COR-94

        Args:
            openai (object): an instantiation of openAI
            model_name (str): the name of the custom model to query
        """
        BaseObject.__init__(self, __name__)
        self._model_name = model_name
        self._conn = OpenAIConnector().process()
        self._generate_event = ServiceEventGenerator().process

    def _process(self,
                 input_text: str,
                 search_model: str) -> object or None:
        try:

            return self._conn.Answer.create(
                search_model=search_model,
                model='curie',
                question=input_text,
                return_metadata=True,
                file=self._model_name,
                examples_context='In 2017, U.S. life expectancy was 78.6 years.',
                examples=[
                    ['What is human life expectancy in the United States?', '78 years.']],
                max_rerank=10,
                max_tokens=5,
                stop=['\n', '<|endoftext|>']
            )

        except InvalidRequestError:
            # GRAFFL-350; not necessarily a defect, just didn't find similar documents
            if self.isEnabledForInfo:
                self.logger.info('\n'.join([
                    'No Similar Documents Were Found',
                    f'\tInput Text: {input_text}',
                    f'\tTrained Model: {self._model_name}',
                    f'\tSearch Model: {search_model}']))

            return None

    def process(self,
                input_text: str,
                search_model: str) -> dict:

        sw = Stopwatch()
        output_events = []

        response = self._process(input_text=input_text,
                                 search_model=search_model)

        response = dict(response)

        output_events.append(self._generate_event(
            service_name=self.component_name(),
            event_name='create-openai-answer',
            stopwatch=sw,
            data={
                'input_text': input_text,
                'search_model': search_model,
                'response': response
            }))

        return {
            'results': response,
            'events': output_events
        }
