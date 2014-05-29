import vcr
import porc
import unittest
from credentials import API_KEY

class CollectionTest(unittest.TestCase):

    def setUp(self):
        self.collection = porc.Client(API_KEY).collection('derptest')

    def testKey(self):
        key = self.collection.key('omgwut')
        # assert it returns a Key object
        assert type(porc.Key('test')) == type(key) 

    def testList(self):
        page = self.collection.list(limit=100)
        # assert it returns a Page object
        assert type(porc.Page('test')) == type(page)

    def testSearch(self):
        page = self.collection.search(query='test*')
        # assert it returns a Page object
        assert type(porc.Page('test')) == type(page)

class CrudTest(unittest.TestCase):

    def setUp(self):
        self.collection = porc.Client(API_KEY, async=False).collection('derptest')
        self.key = self.collection.key('omgwut')

    @vcr.use_cassette('fixtures/collection/crud.yaml')
    def testCrud(self):
        # create
        self.key.put(dict(hello='world')).raise_for_status()
        # destroy
        self.collection.delete().raise_for_status()
