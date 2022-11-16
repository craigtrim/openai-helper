#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Connect to OpenAI """


from typing import Any
from typing import Optional

import openai

from baseblock import EnvIO
from baseblock import CryptoBase
from baseblock import BaseObject


class OpenAIConnector(BaseObject):
    """ Connect to OpenAI """

    def __init__(self):
        """ Change Log

        Created:
            28-Jul-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)

    @classmethod
    def _openai_key(cls) -> Optional[str]:
        """ Retrieve OpenAI Key

        Use the encrypted key within the environment

        Returns:
            str: the decrypted OpenAI key
        """
        try:
            return CryptoBase().decrypt_str(EnvIO.str_or_exception('OPENAI_KEY'))
        except ValueError:
            return None

    @classmethod
    def _openai_org(cls) -> Optional[str]:
        """ Retrieve OpenAI org

        Use the encrypted key within the environment

        Returns:
            str: the decrypted OpenAI org
        """
        try:
            return CryptoBase().decrypt_str(EnvIO.str_or_exception('OPENAI_ORG'))
        except ValueError:
            return None

    def _process(self) -> Any:
        """ Connect to OpenAI

        Returns:
            object: an instantiated remote instance
        """

        openai.api_key = self._openai_key()
        openai.organization = self._openai_org()

        return openai

    def process(self) -> Any:
        """ Connect to OpenAI

        Returns:
            object: an instantiated remote instance
        """
        return self._process()
