import vcr
import porc
import unittest
from credentials import API_KEY

class ClientTest(unittest.TestCase):

    def setUp(self):
        self.api_key = API_KEY
        self.client = porc.Client(self.api_key)

    def testInit(self):
        assert self.client.uri == 'https://%s:@api.orchestrate.io/v0' % self.api_key

    def testCollection(self):
        collection = self.client.collection('hello')
        assert collection.uri == self.client.uri + '/' + 'hello'
        assert collection._session == self.client._session

    @vcr.use_cassette('fixtures/client/ping.yaml')
    def testPing(self):
        future = self.client.ping()
        response = future.result()
        response.raise_for_status()