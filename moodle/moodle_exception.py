from collections.abc import Mapping

class MoodleException(Exception):
    def __init__(self, data:Mapping):
        self._message = data.get('message', '')
        self._exception = data.get('exception', '')
        self._errorcode = data.get('errorcode', '')
        self._debuginfo = data.get('debuginfo', '')
        super().__init__(self._message)
