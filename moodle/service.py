"""
    Moodle webservice caller Main class
"""

from collections.abc import Iterable
import logging
from urllib.parse import quote_plus
import requests
from .moodle_exception import MoodleException

_logger = logging.getLogger(__name__)

class Moodle:
    def __init__(self, url:str, token:str, timeout:int=30):
        self._url = url
        self._token = token
        self._timeout = timeout

    def __call__(self, function:str, data=None):
        params = {
            'wstoken': self._token, 'wsfunction': function,
            'moodlewsrestformat': 'json',
        }

        _logger.debug('Call %s', function)

        if data is None:
            resp = requests.get(self._url, params=params, timeout=self._timeout)
        else:
            resp = requests.post(
                self._url, params=params,
                headers={'Content-type': 'application/x-www-form-urlencoded'},
                data=self._serialize(data),
                timeout=self._timeout,
            )

        _logger.debug('Response status code: %d', resp.status_code)

        if not resp.ok:
            _logger.error('Error on request, data: %s', resp.text)

        resp.raise_for_status()
       
        res = resp.json()

        if res is not None and 'exception' in res:
            raise MoodleException(res['message'])

        return res

    def _serialize(self, data):
        res = {}
        def _trace(data, path=''):
            if isinstance(data, dict):
                for k,v in data.items():
                    if path=='':
                        _trace(v, k)
                    else:
                        _trace(v, f'{path}[{k}]')
            elif isinstance(data, Iterable) and not isinstance(data, str):
                for i,v in enumerate(data):
                    _trace(v, f'{path}[{i}]')
            else:
                res[path] = str(data)

        _trace(data)
        return '&'.join([f'{k}={quote_plus(v)}' for k,v in res.items()])
