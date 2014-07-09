import vcr
import porc
import unittest
from .credentials import API_KEY

class PagesTest(unittest.TestCase):

    @vcr.use_cassette('fixtures/pages/setup.yaml')
    def setUp(self):
        self.api_key = API_KEY
        self.client = porc.Client(self.api_key)
        self.collections = ['COLLECTION_1', 'COLLECTION_2']
        self.keys = ['KEY_1', 'KEY_2']
        self.pages = self.client.search(self.collections[0], '*', limit=1)
        # add items
        with self.client.async() as c:
            futures = [
                c.post(self.collections[0], {'lol': True}),
                c.post(self.collections[0], {'lol': True}),
                c.post(self.collections[0], {'lol': True})
            ]
            [future.result().raise_for_status() for future in futures]

    @vcr.use_cassette('fixtures/pages/teardown.yaml')
    def tearDown(self):
        self.client.delete(self.collections[0]).raise_for_status()

    @vcr.use_cassette('fixtures/pages/reset.yaml')
    def test_reset(self):
        resp = self.pages.next()
        resp.raise_for_status()
        assert resp.links.get('prev', None) == None
        self.pages.reset()
        resp = self.pages.next()
        resp.raise_for_status()
        assert resp.links.get('prev', None) == None

    @vcr.use_cassette('fixtures/pages/next.yaml')
    def test_next(self):
        resp = self.pages.next()
        resp.raise_for_status()

    @vcr.use_cassette('fixtures/pages/prev.yaml')
    def test_prev(self):
        resp = self.pages.next()
        resp.raise_for_status()
        resp = self.pages.next()
        resp.raise_for_status()
        resp = self.pages.prev()
        resp.raise_for_status()

    @vcr.use_cassette('fixtures/pages/all.yaml')
    def test_all(self):
        pages = self.pages.all()
        [page.raise_for_status() for page in pages]

    @vcr.use_cassette('fixtures/pages/iter.yaml')
    def test_iter(self):
        pages = [page for page in self.pages]
        [page.raise_for_status() for page in pages]
