import vcr
import porc
import unittest
from credentials import API_KEY

class RelationTest(unittest.TestCase):
    
    @vcr.use_cassette('fixtures/relation/setup.yaml')
    def setUp(self):
        self.client = porc.Client(API_KEY, async=False)
        self.collection = self.client.collection('test')
        self.key = self.collection.key('a')
        self.other_key = self.collection.key('b')
        self.key.put(dict(hello='world')).raise_for_status()
        self.other_key.put(dict(goodbye='world')).raise_for_status()
        self.relation = self.key.relation()

    @vcr.use_cassette('fixtures/relation/crud.yaml')
    def testCrud(self):
        self.relation.put('before', 'test', 'b').raise_for_status()
        response = self.relation.get('before')
        response.raise_for_status()
        assert response.json()['count'] == 1
        self.relation.delete('before', 'test', 'b', dict(purge=True)).raise_for_status()

    @vcr.use_cassette('fixtures/relation/teardown.yaml')
    def tearDown(self):
        self.collection.delete(dict(force=True)).raise_for_status()