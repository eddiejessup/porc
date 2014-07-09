from datetime import datetime
import time
import vcr
import porc
import unittest
from .credentials import API_KEY

class ClientTest(unittest.TestCase):

    def setUp(self):
        self.api_key = API_KEY
        self.client = porc.Client(self.api_key)
        self.collections = ['COLLECTION_1', 'COLLECTION_2']
        self.keys = ['KEY_1', 'KEY_2']

    # N.B.: TESTS MUST CLEAN UP AFTER THEMSELVES

    @vcr.use_cassette('fixtures/client/ping.yaml')
    def test_ping(self):
        self.client.ping().raise_for_status()

    @vcr.use_cassette('fixtures/client/get.yaml')
    def test_get(self):
        # test 404
        resp = self.client.get(self.collections[0], self.keys[0])
        assert resp.status_code == 404
        # create item
        resp = self.client.put(self.collections[0], self.keys[0], {"derp": True})
        ref = resp.ref
        resp.raise_for_status()
        # wait; kv is eventually consistent (?!)
        time.sleep(1)
        # test 200
        resp = self.client.get(self.collections[0], self.keys[0])
        resp.raise_for_status()
        # test 200 with ref
        resp = self.client.get(self.collections[0], self.keys[0], ref)
        resp.raise_for_status()
        # cleanup
        self.client.delete(self.collections[0], self.keys[0]).raise_for_status()

    @vcr.use_cassette('fixtures/client/post.yaml')
    def test_post(self):
		# test creates
        resp = self.client.post(self.collections[0], {"derp": True})
        key = resp.key
        ref = resp.ref
        resp.raise_for_status()
        # test get with generated ref
        self.client.get(self.collections[0], key, ref).raise_for_status()
        # cleanup
        self.client.delete(self.collections[0], key, ref).raise_for_status()
        self.client.delete(self.collections[0], key).raise_for_status()

    @vcr.use_cassette('fixtures/client/put.yaml')
    def test_put(self):
        # test creates with If-None-Match
        resp = self.client.put(self.collections[0], self.keys[0], {"derp": True}, False)
        resp.raise_for_status()
        ref = resp.ref
        # test update with If-Match
        resp = self.client.put(self.collections[0], self.keys[0], {"derp": False}, ref)
        ref = resp.ref
        resp.raise_for_status()
        # test update with neither
        self.client.put(self.collections[0], self.keys[0], {"derp": True}).raise_for_status()
        # delete
        self.client.delete(self.collections[0], self.keys[0]).raise_for_status()

    @vcr.use_cassette('fixtures/client/delete.yaml')
    def test_delete(self):
		# create
        resp = self.client.post(self.collections[0], {"derp": True})
        resp.raise_for_status()
        # delete a ref
        self.client.delete(resp.collection, resp.key, resp.ref).raise_for_status()
        # delete purge
        self.client.delete(resp.collection, resp.key).raise_for_status()
        # delete collection
        self.client.delete(resp.collection).raise_for_status()

    @vcr.use_cassette('fixtures/client/refs.yaml')
    def test_refs(self):
        # create
        resp = self.client.post(self.collections[0], {"derp": True})
        resp.raise_for_status()
        # list
        ref_resp = self.client.refs(resp.collection, resp.key, values=False)
        ref_resp.raise_for_status()
        assert ref_resp['count'] == 1
        # delete
        self.client.delete(resp.collection, resp.key).raise_for_status()

    @vcr.use_cassette('fixtures/client/list.yaml')
    def test_list(self):
        # create
        resp = self.client.post(self.collections[0], {"derp": True})
        resp.raise_for_status()
        # list
        pages = self.client.list(resp.collection, limit=1)
        page = pages.next()
        page.raise_for_status()
        assert page['count'] == 1
        # delete
        self.client.delete(resp.collection, resp.key).raise_for_status()

    @vcr.use_cassette('fixtures/client/search.yaml')
    def test_search(self):
        # create
        resp = self.client.post(self.collections[0], {"herp": "hello"})
        resp.raise_for_status()
        # wait; search is eventually consistent
        time.sleep(3)
        # list
        pages = self.client.search(resp.collection, 'herp:hello', limit=1)
        page = pages.next()
        page.raise_for_status()
        assert page['count'] == 1
        # delete
        self.client.delete(resp.collection, resp.key).raise_for_status()

    @vcr.use_cassette('fixtures/client/relations.yaml')
    def test_crud_relations(self):
		# create two items
        responses = []
        for item in [{"herp": "hello"}, {"burp": "goodbye"}]:
            resp = self.client.post(self.collections[0], item)
            resp.raise_for_status()
            responses.append(resp)
        # get relation, 404 or 200 and count = 0
        resp = self.client.get_relations(self.collections[0], responses[0].key, 'friends')
        if resp.status_code == 200:
            assert resp['count'] == 0
        else:
            assert resp.status_code == 404
        # make relation, 201
        resp = self.client.put_relation(
            self.collections[0], 
            responses[0].key, 
            'friends', 
            self.collections[0], 
            responses[1].key
            )
        resp.raise_for_status()
        # get relation, 200
        resp = self.client.get_relations(self.collections[0], responses[0].key, 'friends')
        resp.raise_for_status()
        assert resp['count'] == 1
        # delete relation
        self.client.delete_relation(
            self.collections[0], 
            responses[0].key, 
            'friends', 
            self.collections[0], 
            responses[1].key
            )
        # delete collection
        self.client.delete(self.collections[0]).raise_for_status()

    @vcr.use_cassette('fixtures/client/events.yaml')
    def test_crud_events(self):
        # create an event
        resp = self.client.post_event(self.collections[0], self.keys[0], 'log', {'herp': 'derp'})
        resp.raise_for_status()
        # create an event with a timestamp
        timestamp = datetime.utcfromtimestamp(float(resp.timestamp) / 1000.0)
        resp = self.client.post_event(self.collections[0], self.keys[0], 'log', {'herp': 'derp'}, timestamp)
        resp.raise_for_status()
        # get an event
        timestamp = datetime.utcfromtimestamp(float(resp.timestamp) / 1000.0)
        resp = self.client.get_event(resp.collection, resp.key, resp.type, timestamp, resp.ordinal)
        resp.raise_for_status()
        # update an event
        timestamp = datetime.utcfromtimestamp(float(resp.timestamp) / 1000.0)
        resp = self.client.put_event(resp.collection, resp.key, resp.type, timestamp, resp.ordinal, {'herp': 'lol'})
        resp.raise_for_status()
        # update with ref
        resp = self.client.put_event(resp.collection, resp.key, resp.type, resp.timestamp, resp.ordinal, {'herp': 'rofl'}, resp.ref)
        resp.raise_for_status()
        # list all events
        pages = self.client.list_events(resp.collection, resp.key, resp.type, limit=1, afterEvent=datetime.utcfromtimestamp(0))
        page = pages.next()
        page.raise_for_status()
        assert page['count'] == 1
        # delete event with ref
        timestamp = datetime.utcfromtimestamp(float(resp.timestamp) / 1000.0)
        self.client.delete_event(resp.collection, resp.key, resp.type, timestamp, resp.ordinal, resp.ref).raise_for_status()
        # delete event without ref
        timestamp = datetime.utcfromtimestamp(float(resp.timestamp) / 1000.0)
        self.client.delete_event(resp.collection, resp.key, resp.type, timestamp, resp.ordinal).raise_for_status()

    @vcr.use_cassette('fixtures/client/async.yaml')
    def test_async(self):
        # add three items
        with self.client.async() as c:
            futures = [
                c.post(self.collections[1], {"holy gosh": True}),
                c.post(self.collections[1], {"holy gosh": True}),
                c.post(self.collections[1], {"holy gosh": True})
            ]
            responses = [future.result() for future in futures]
            [response.raise_for_status() for response in responses]
        # ensure they all exist
        with self.client.async() as c:
            futures = [
                c.get(self.collections[1], responses[0].key),
                c.get(self.collections[1], responses[1].key),
                c.get(self.collections[1], responses[2].key)
            ]
            responses = [future.result() for future in futures]
            [response.raise_for_status() for response in responses]
        # delete all three
        with self.client.async() as c:
            futures = [
                c.delete(self.collections[1], responses[0].key),
                c.delete(self.collections[1], responses[1].key),
                c.delete(self.collections[1], responses[2].key)
            ]
            responses = [future.result() for future in futures]
            [response.raise_for_status() for response in responses]
