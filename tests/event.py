import vcr
import porc
import unittest
import time
from .credentials import API_KEY
from datetime import datetime

class EventTest(unittest.TestCase):

    def setUp(self):
        self.event = porc.Client(API_KEY).collection('derptest').key('testderp').event('created')

    def testList(self):
        page = self.event.list(dict(limit=100))
        assert type(page) == porc.Page

class CrudTest(unittest.TestCase):

    @vcr.use_cassette('fixtures/event/crud_setup.yaml')
    def setUp(self):
        self.client = porc.Client(API_KEY, async=False)
        self.collection = self.client.collection('derptest')
        self.key = self.collection.key('testderp')
        response = self.key.put(dict(hello='world'))
        response.raise_for_status()
        self.event = self.key.event('created')

    @vcr.use_cassette('fixtures/event/crud_teardown.yaml')
    def tearDown(self):
        self.collection.delete(dict(force=True)).raise_for_status()

    @vcr.use_cassette('fixtures/event/crud.yaml')
    def testCrud(self):
        responses = dict()
        # create
        responses['create'] = self.event.post(dict(hello='world'))
        responses['create'].raise_for_status()
        # create with timestamp
        timestamp = datetime(2014, 5, 2)
        responses['post'] = self.event.post(dict(hello='world'), timestamp)
        ordinal = responses['post'].path['ordinal']
        responses['post'].raise_for_status()
        # list
        responses['list'] = [response for response in self.event.get()]
        for response in responses['list']:
            assert response.json()['count'] == 2
            response.raise_for_status()
        # read
        responses['get'] = self.event.get(timestamp, ordinal)
        responses['get'].raise_for_status()
        assert responses['get'].json()['value']['hello'] == 'world'
        # update
        responses['update'] = self.event.put(timestamp, ordinal, dict(goodbye='world'))
        responses['update'].raise_for_status()
        # delete
        responses['delete'] = self.event.delete(timestamp, ordinal, dict(purge=True))
        responses['delete'].raise_for_status()
