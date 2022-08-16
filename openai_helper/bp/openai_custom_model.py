#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Query a Custom Model in OpenAI """


from random import sample
from functools import lru_cache
from openai.error import InvalidRequestError

from baseblock import EnvIO
from baseblock import Stopwatch
from baseblock import BaseObject
from baseblock import Enforcer
from baseblock import ServiceEventGenerator

from openai_helper.dmo import OpenAIConnector


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

        Args:
            openai (object): an instantiation of openAI
            model_name (str): the name of the custom model to query
        """
        BaseObject.__init__(self, __name__)
        self._conn = OpenAIConnector().process()
        self._model_name = model_name
        self._generate_event = ServiceEventGenerator().process

    def _query(self,
               input_text: str,
               search_model: str) -> object or None:
        try:
            return self._conn.Answer.create(
                search_model=search_model,
                model="curie",
                question=input_text,
                return_metadata=True,
                file=self._model_name,
                examples_context="In 2017, U.S. life expectancy was 78.6 years.",
                examples=[
                    ["What is human life expectancy in the United States?", "78 years."]],
                max_rerank=10,
                max_tokens=5,
                stop=["\n", "<|endoftext|>"]
            )
        except InvalidRequestError:
            # GRAFFL-350; not necessarily a defect, just didn't find similar documents
            if self.isEnabledForInfo:
                self.logger.info('\n'.join([
                    "No Similar Documents Were Found",
                    f"\tInput Text: {input_text}",
                    f"\tTrained Model: {self._model_name}",
                    f"\tSearch Model: {search_model}"]))
            return None

    def _top_response(self,
                      results: list,
                      threshold: float) -> str:
        """ Return the Top Response

        In the case of multiple responses, and if the top responses are within a few % points of eachother
        then choose a top response at random; GRAFFL-371

        Args:
            results (list): the OpenAI search results
            threshold (float): the accuracy threshold to filter out results at. Defaults to 25.0.

        Returns:
            str: a single output result
        """

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

    @lru_cache
    def process(self,
                input_text: str,
                search_model: str = 'text-davinci-002',
                threshold: float = 25.0) -> tuple or None:
        """ Call the OpenAI Text Summarizer

        Args:
            input_text (str): the input text to send to OpenAI
            search_model (str): the model used to interpret the query and search
            threshold (float): the accuracy threshold for filtering results

        Returns:
            dict: the complete openAI event
        """

        if not EnvIO.is_true("USE_OPENAI"):
            return "*** OPENAI DISABLED ***", None

        sw = Stopwatch()
        if self.isEnabledForDebug:
            Enforcer.is_str(input_text)

        response = self._query(
            input_text=input_text,
            search_model=search_model)

        if not response:
            return None, None

        output_text = self._top_response(response['selected_documents'],
                                         threshold=threshold)
        if not output_text:
            return None, None

        # COR-80; Generate an Event Record
        d_event = self._generate_event(
            service_name=self.component_name(),
            event_name="openai",
            stopwatch=sw,
            data={
                'input_text': input_text,
                'output_text': output_text,
                'search_model': search_model,
                'd_response': dict(response)
            })

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                f"OpenAI Service Completed ({d_event['service']})",
                f"\tTotal Time: {str(sw)}",
                f"\tInput Text: {input_text.strip()}",
                f"\tOutput Text: {output_text}"]))

        return output_text, d_event
