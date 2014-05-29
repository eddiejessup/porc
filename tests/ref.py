import vcr
import porc
from credentials import API_KEY
import unittest

class RefTest(unittest.TestCase):

    @vcr.use_cassette('fixtures/ref/setup.yaml')
    def setUp(self):
        self.client = porc.Client(API_KEY, async=False)
        self.collection = self.client.collection('test')
        self.key = self.collection.key('test')
        # create first ref
        response = self.key.put(dict(hello='world'))
        ref_index = response.headers['location'].rfind('/') + 1
        ref = response.headers['location'][ref_index:]
        self.ref_a = self.key.ref(ref)
        # create second ref
        response = self.key.put(dict(goodbye='world'), **{"If-Match": ref})
        ref_index = response.headers['location'].rfind('/') + 1
        ref = response.headers['location'][ref_index:]
        self.ref_b = self.key.ref(ref)

    @vcr.use_cassette('fixtures/ref/teardown.yaml')
    def tearDown(self):
        self.collection.delete(dict(force=True)).raise_for_status()

    @vcr.use_cassette('fixtures/ref/crud.yaml')
    def testCrud(self):
        # read
        self.ref_a.get().raise_for_status()
        # delete the latest version
        self.key.delete().raise_for_status
        # read the older version
        self.ref_a.get().raise_for_status()