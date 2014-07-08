import json
import requests
from .response import Response
from requests_futures.sessions import FuturesSession
import copy
try:
    # python 2
    from urllib import quote
except ImportError:
    # python 3
    from urllib.parse import quote

class Resource(object):
    def __init__(self, uri, **kwargs):
        self.uri = uri
        self.opts = kwargs
        self.session = requests.Session()
        for key, value in kwargs.iteritems():
            setattr(self.session, key, value)

    def init_child(self, child_obj, path, **kwargs):
        uri = self._merge_paths(path)
        opts = copy.copy(self.opts)
        opts.update(kwargs)
        return child_obj(uri, **opts)

    def _merge_paths(self, path):
        if path:
            if isinstance(path, list):
                path = '/'.join([quote(elem) for elem in path])
            return '/'.join([self.uri, quote(path)])
        else:
            return self.uri

    def _make_request(self, method, path='', body={}, headers={}):
        """
        Executes the request based on the given body and headers
        along with options set on the object.
        """
        uri = self._merge_paths(path)
        opts = dict(headers=headers)

        # normalize body according to method and type
        if body:
            if method in ['head', 'get', 'delete']:
                if type(body) == dict:
                    # convert True and False to true and false
                    for key, value in list(body.items()):
                        if value == True:
                            body[key] = 'true'
                        elif value == False:
                            body[key] = 'false'
                opts['params'] = body
            else:
                opts['data'] = json.dumps(body)

        return self.session.request(method, uri, **opts)

    def async(self):
        return Async(self.uri, self.opts)

class Async(object):
    def __init__(self, uri, opts):
        self.client = Resource(self.uri, **self.opts)
        
        if 'background_callback' in self.client.opts:
            self.client.opts['background_callback'] = self._merge_callbacks(self.client.opts['background_callback'])
        else:
            self.client.opts['background_callback'] = self._handle_response

        self.client.session = FuturesSession(**self.client.opts)

    def _merge_callbacks(self, callback):
        def merger(session, response):
            callback(session, response)
            self._handle_response(session, response)

        return merger

    def _handle_response(session, response):
        response = Response(response)

    def __enter__(self):
        return self.client

    def __exit__(self, type, value, traceback):
        return True
