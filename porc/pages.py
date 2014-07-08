from .resource import Resource
from collections import Iterator
import copy
try:
    # python 2
    from urllib import quote
except ImportError:
    # python 3
    from urllib.parse import quote

class Pages(Iterator):
    def __init__(self, opts, url, path, params):
        self.resource = Resource(url, **opts)
        if isinstance(list, path):
            self.resource.url = '/'.join([url] + [quote(elem) for elem in path])
        else:
            self.resource.url = '/'.join([url, quote(path)])
        self.params = params
        self._url_root = self.uri[:self.uri.find('/v0')]
        self.response = None

    def _handle_page(self, querydict={}, val='next', **headers):
        """
        Executes the request getting the next (or previous) page,
        incrementing (or decrementing) the current page.
        """
        params = copy.copy(self.params)
        params.update(querydict)
        # if async, wait for previous page to load
        if hasattr(self.response, 'result'):
            self.response.result()
        # update uri based on next page
        if self.response:
            self.response.raise_for_status()
            _next = self.response.links().get(val, False)
            if _next:
                self.uri = self._url_root + _next
            else:
                raise StopIteration
        # execute request
        response = self.resource._make_request('GET', '', params, **headers)
        self._handle_res(None, response)
        return response

    def _handle_res(self, session, response):
        """
        Stores the response, which we use for determining
        next and prev pages.
        """
        self.response = response

    def reset(self):
        """
        Clear the page's current place.

            page_1 = page.next().result()
            page_2 = page.next().result()
            page.reset()
            page_x = page.next().result()
            assert page_x.url == page_1.url
        """
        self.response = None

    def next(self, querydict={}, **headers):
        """
        Gets the next page of results.
        Raises `StopIteration` when there are no more results.
        """
        return self._handle_page(querydict, **headers)

    def __next__(self):
        return self.next()

    def prev(self, querydict={}, **headers):
        """
        Gets the previous page of results.
        Raises `StopIteration` when there are no more results.

        Note: Only collection searches provide a `prev` value.
        For all others, `prev` will always return `StopIteration`.
        """
        return self._handle_page(querydict, 'prev', **headers)        

    def all(self):
        return [response for response in self]