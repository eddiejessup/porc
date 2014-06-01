import vcr
import porc
import unittest
import time
from .credentials import API_KEY

class PageTest(unittest.TestCase):

    @vcr.use_cassette('fixtures/page/setup.yaml')
    def setUp(self):
        self.client = porc.Client(API_KEY)
        self.collection = self.client.collection('test')
        self.key_names = ['omg', 'wut', 'bbq']
        for name in self.key_names:
            response = self.collection.key(name).put(dict(hello='world')).result()
            response.raise_for_status()

    @vcr.use_cassette('fixtures/page/teardown.yaml')
    def tearDown(self):
        self.collection.delete(dict(force=True)).result().raise_for_status()

    @vcr.use_cassette('fixtures/page/next.yaml')
    def testNext(self):
        pages = self.collection.list(limit=len(self.key_names))
        response = next(pages)
        try: 
            next(pages)
        except StopIteration:
            # good. this is expected
            pass
        else:
            raise AssertionError("Should have thrown StopIteration")

    @vcr.use_cassette('fixtures/page/prev.yaml')
    def testPrev(self):
        page = self.collection.search(query="*", limit=1)
        # proceed two pages
        next(page)
        next(page)
        # go back one
        page.prev()
        # going back one more should raise StopIteration
        try: 
            page.prev()
        except StopIteration:
            # good. this is expected
            pass
        else:
            raise AssertionError("Should have thrown StopIteration")

    @vcr.use_cassette('fixtures/page/reset.yaml')
    def testReset(self):
        page = self.collection.list(limit=len(self.key_names))
        response = next(page).result()
        response.raise_for_status()
        page.reset()
        # now, nexting should work
        response = next(page).result()
        response.raise_for_status()

    @vcr.use_cassette('fixtures/page/iter.yaml')
    def testIter(self):
        pages = self.collection.list(limit=1)
        pages_responses = [page for page in pages]
        assert len(pages_responses) == 3

    @vcr.use_cassette('fixtures/page/next_function_identity.yaml')
    def testNextFunctionIdentity(self):
        # ensure next and __next__ do the same thing
        page1 = self.collection.list().next().result()
        page2 = self.collection.list().__next__().result()
        assert page1.text == page2.text
