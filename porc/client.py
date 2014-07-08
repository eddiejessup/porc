from .resource import Resource
from .version import VERSION
from .pages import Pages
from . import util

class Client(Resource):
    def __init__(self, api_key, custom_url=None):
        url = custom_url or 'https://api.orchestrate.io/v0'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'python-requests/1.2.0 porc/%s' % VERSION
        }
        super(Client, self).__init__(url, auth=(api_key, ''), headers=headers)

    def ping(self):
        return self._make_request('HEAD')

    def get(self, collection, key, ref=None):
        if ref:
            path = [collection, key]
        else:
            path = [collection, key, ref]
        return self._make_request('GET', path)

    def post(self, collection, body):
        return self._make_request('POST', collection, body)

    def put(self, collection, key, body, ref=None):
        opts = dict()
        if ref:
            opts['If-Match'] = ref.center(len(ref)+2, '"')
        elif ref == False:
            opts['If-None-Match'] = '*'
        return self._make_request('POST', [collection, key], body, **opts)

    def delete(self, collection, key=None, ref=None):
        if key:
            opts = dict()
            params = dict()
            if ref:
                opts['If-Match'] = ref.center(len(ref)+2, '"')
            else:
                params['purge'] = True
            return self._make_request('DELETE', [collection, key], params, **opts)
        else:
            return self._make_request('DELETE', collection, dict(force=True))

    def refs(self, collection, key, **params):
        return self._make_request('GET', [collection, key, 'refs'], params)

    def list(self, collection, **params):
        return Pages(self.opts, self.url, collection, params)

    def search(self, collection, query, **params):
        params['q'] = query
        return Pages(self.opts, self.url, collection, params)

    def get_relations(self, collection, key, *relations):
        path = [collection, key, 'relations'] + relations
        return self._make_request('GET', path)

    def put_relation(self, collection, key, relation, to_collection, to_key):
        path = [collection, key, 'relations', relation, to_collection, to_key]
        return self._make_request('PUT', path)

    def delete_relation(self, collection, key, relation, to_collection, to_key):
        path = [collection, key, 'relations', relation, to_collection, to_key]
        return self._make_request('DELETE', path, dict(purge=True))

    def get_event(self, collection, key, event_type, timestamp, ordinal):
        if isinstance(datetime, timestamp):
            timestamp = util.datetime_to_timestamp(timestamp)
        path = [collection, key, 'events', event_type, util.datetime(timestamp), ordinal]
        return self._make_request('GET', path)

    def post_event(self, collection, key, event_type, data, timestamp=None):
        path = [collection, key, 'events', event_type]
        if timestamp:
            if isinstance(datetime, timestamp):
                timestamp = util.datetime_to_timestamp(timestamp)
            path += timestamp
        return self._make_request('POST', path, data)

    def put_event(self, collection, key, event_type, timestamp, ordinal, data, ref=None):
        if isinstance(datetime, timestamp):
            timestamp = util.datetime_to_timestamp(timestamp)
        path = [collection, key, 'events', event_type, timestamp, ordinal]
        headers = dict()
        if ref:
            headers['If-Match'] = ref.center(len(ref)+2, '"')
        return self._make_request('PUT', path, data, headers=headers)

    def delete_event(self, collection, key, event_type, timestamp, ordinal, ref=None):
        if isinstance(datetime, timestamp):
            timestamp = util.datetime_to_timestamp(timestamp)
        path = [collection, key, 'events', event_type, timestamp, ordinal]
        headers = dict()
        if ref:
            headers['If-Match'] = ref.center(len(ref)+2, '"')
        return self._make_request('DELETE', path, headers=headers)

    def list_events(self, collection, key, event_type, **params): 
        path = [collection, key, 'events', event_type]
        for param in ['startEvent', 'afterEvent', 'beforeEvent', 'endEvent']:
            if param in params and isinstance(datetime, params[param]):
                params[param] = datetime_to_timestamp(params[param])
        return Pages(self.opts, self.url, path, params)
