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
        Updated:
            14-Sept-2022
            craigtrim@gmail.com
            *   make text pipeline dynamic via incoming parameters
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

                # TODO: if line breaks become an issue, then parameterize this feature
                output_text = output_text.replace('\n', ' CUSTOMLINEBREAK ')
                while '\n\n' in output_text:
                    output_text = output_text.replace('\n\n', '\n')

                output_text = output_text.split('\n')[-1].strip()

                output_text = output_text.replace(' CUSTOMLINEBREAK ', '\n')
                while '  ' in output_text:
                    output_text = output_text.replace('  ', ' ')

                return output_text

        return None

    def process(self,
                input_text: str,
                d_result: dict,
                replace_duplicated_input: bool = True,
                handle_text_completions: bool = True,
                remove_indicators: bool = True,
                replace_cliched_text: bool = True) -> str or None:

        sw = Stopwatch()

        if not input_text:
            return None

        if not d_result:
            return None

        def create_pipeline() -> list:
            text_pipeline = []

            if replace_duplicated_input:
                text_pipeline.append(self._replace_duplicated_input)

            if handle_text_completions:
                text_pipeline.append(self._handle_text_completions)

            if remove_indicators:
                text_pipeline.append(self._remove_indicators)

            if replace_cliched_text:
                text_pipeline.append(self._replace_cliched_text)

            return text_pipeline

        output_text = self._output_text(d_result)
        if not output_text or not len(output_text):
            return None

        for text_handler in create_pipeline():
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
