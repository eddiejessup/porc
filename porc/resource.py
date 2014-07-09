from . import util
import json
import requests
from .response import Response
import copy
from requests_futures.sessions import FuturesSession
try:
    # python 2
    from urllib import quote
except ImportError:
    # python 3
    from urllib.parse import quote

class Resource(object):
    def __init__(self, uri, use_async=False, **kwargs):
        self.uri = uri
        self.opts = kwargs
        self.session = requests.Session()
        self.async = FuturesSession()
        self.use_async = use_async
        kwargs['hooks'] = {
            "response": self._handle_response
        }
        for obj in [self.session, self.async]:
            for key, value in kwargs.iteritems():
                setattr(obj, key, value)

    def init_child(self, child_obj, path, **kwargs):
        uri = self._merge_paths(path)
        opts = copy.copy(self.opts)
        opts.update(kwargs)
        return child_obj(uri, **opts)

    def _merge_paths(self, path):
        if path:
            if isinstance(path, list):
                path = '/'.join([quote(str(elem)) for elem in path])
            return '/'.join([self.uri, quote(str(path))])
        else:
            return self.uri

    def _make_request(self, method, path='', body={}, headers={}):
        """
        Executes the request based on the given body and headers
        along with options set on the object.
        """
        uri = self._merge_paths(path)
        opts = dict(headers=headers)
        session = self.async if self.use_async else self.session
        # normalize body according to method and type
        if body:
            if method.lower() in ['head', 'get', 'delete']:
                if type(body) == dict:
                    # convert True and False to true and false
                    for key, value in list(body.items()):
                        if value is True:
                            body[key] = 'true'
                        elif value is False:
                            body[key] = 'false'
                opts['params'] = body
            else:
                opts['data'] = json.dumps(body)

        return session.request(method, uri, **opts)

    def _handle_response(self, response, *args, **kwargs):
        return Response(response)
