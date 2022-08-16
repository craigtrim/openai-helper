#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" A Generic Service to Extract Unstructured Output from an OpenAI response """


from baseblock import Stopwatch
from baseblock import BaseObject

from openai_helper.dmo import EtlHandleTextCompletions
from openai_helper.dmo import EtlRemoveIndicators
from openai_helper.dmo import EtlReplaceCliches
from openai_helper.dmo import EtlReplaceDuplicatedInput


class ExtractOutput(BaseObject):
    """ A Generic Service to Extract Unstructured Output from an OpenAI response """

    def __init__(self):
        """
        Created:
            17-Mar-2022
            craigtrim@gmail.com
            *   in pursuit of
                https://github.com/grafflr/graffl-core/issues/222
        Updated:
            18-Mar-2022
            craigtrim@gmail.com
            *   handle text completions
                https://github.com/grafflr/graffl-core/issues/224
        Updated:
            4-Aug-2022
            craigtrim@gmail.com
            *   migrated to 'openai-helper' in pursuit of
                https://bast-ai.atlassian.net/browse/COR-56
                https://github.com/craigtrim/openai-helper/issues/1
        """
        BaseObject.__init__(self, __name__)
        self._replace_duplicated_input = EtlReplaceDuplicatedInput().process
        self._handle_text_completions = EtlHandleTextCompletions().process
        self._remove_indicators = EtlRemoveIndicators().process
        self._replace_cliched_text = EtlReplaceCliches().process

    @staticmethod
    def _output_text(d_result: dict) -> str:

        if 'choices' in d_result['output']:
            choices = d_result['output']['choices']

            if len(choices):
                output_text = choices[0]['text'].strip()
                output_text = output_text.split('\n')[-1].strip()

                return output_text

        return None

    def process(self,
                input_text: str,
                d_result: dict) -> str or None:

        sw = Stopwatch()

        text_pipeline = [
            self._replace_duplicated_input,
            self._handle_text_completions,
            self._remove_indicators,
            self._replace_cliched_text
        ]

        from pprint import pprint
        pprint(d_result)

        output_text = self._output_text(d_result)
        if not output_text or not len(output_text):
            return None

        for text_handler in text_pipeline:
            output_text = text_handler(input_text=input_text,
                                       output_text=output_text)
            if not output_text or not len(output_text):
                return None

        if self.isEnabledForDebug:
            self.logger.debug('\n'.join([
                "OpenAI Output Extraction Completed",
                f"\tTotal Time: {str(sw)}",
                f"\tInput Text: {input_text}",
                f"\tOutput Text: {output_text}"]))

        return output_text
