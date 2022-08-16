""" Integration Wrapper """


import os

from baseblock import FileIO
from baseblock import BaseObject


class IntegrationWrapper(BaseObject):
    """ Integration Wrapper """

    def __init__(self):
        file_path = os.path.normpath(os.path.join(
            os.getcwd(), 'drivers/test-keys.yaml'))
        FileIO.exists_or_error(file_path)
        self._keys = FileIO.read_yaml(file_path)

        os.environ['USE_OPENAI'] = str(True)
        for key in self._keys:
            os.environ[key] = self._keys[key]

    def deconstruct_env(self) -> None:
        os.environ['USE_OPENAI'] = str(False)
        for key in self._keys:
            del os.environ[key]

    def call(self, function, *args) -> None:
        if len(args):
            function(args)
        else:
            function()
