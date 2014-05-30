import vcr
import unittest
import porc

class BaseTest(unittest.TestCase):

    def setUp(self):
        self.uri = 'http://httpbin.org'

    def testExistingSession(self):
        resource_a = porc.Resource(self.uri)
        resource_b = porc.Resource(self.uri, session=resource_a._session)
        assert resource_a._session is resource_b._session

    def testUpdateOptions(self):
        resource = porc.Resource(self.uri, headers={"hello": "world"})
        assert resource.opts['headers'].get('hello') == 'world'

    def testSetPath(self):
        resource = porc.Resource("https://api.orchestrate.io/v0/$collection/$key/relations/$kind1/$kind2")
        assert 'kinds' in resource.path
        assert resource.path['kinds'] == ['$kind1', '$kind2']

class AsyncTest(BaseTest):

    @vcr.use_cassette('fixtures/resource/async/head.yaml')
    def testHead(self):
        uri = '/'.join([self.uri, 'get'])
        resource = porc.Resource(uri)
        future = resource.head({"hello": "world"})
        response = future.result()
        response.raise_for_status()

    @vcr.use_cassette('fixtures/resource/async/get.yaml')
    def testGet(self):
        uri = '/'.join([self.uri, 'get'])
        resource = porc.Resource(uri)
        future = resource.get({"hello": "world"})
        response = future.result()
        response.raise_for_status()

    @vcr.use_cassette('fixtures/resource/async/put.yaml')
    def testPut(self):
        uri = '/'.join([self.uri, 'put'])
        resource = porc.Resource(uri)
        future = resource.put({"hello": "world"})
        response = future.result()
        response.raise_for_status()

    @vcr.use_cassette('fixtures/resource/async/post.yaml')
    def testPost(self):
        uri = '/'.join([self.uri, 'post'])
        resource = porc.Resource(uri)
        future = resource.post({"hello": "world"})
        response = future.result()
        response.raise_for_status()

    @vcr.use_cassette('fixtures/resource/async/delete.yaml')
    def testDelete(self):
        uri = '/'.join([self.uri, 'delete'])
        resource = porc.Resource(uri)
        future = resource.delete({"hello": "world"})
        response = future.result()
        response.raise_for_status()

    @vcr.use_cassette('fixtures/resource/async/truefalse.yaml')
    def testTrueFalseCorrection(self):
        uri = '/'.join([self.uri, 'get'])
        resource = porc.Resource(uri)
        future = resource.get({"hello": True, "goodbye": False})
        response = future.result()
        response.raise_for_status()
        assert "hello=true" in response.url
        assert "goodbye=false" in response.url

    @vcr.use_cassette('fixtures/resource/async/handle_response.yaml')
    def testHandleResponse(self):
        location = "/v0/$collection/$key/refs/$ref"
        # get response object
        uri = '/'.join([self.uri, 'get'])
        resource = porc.Resource(uri)
        future = resource.get()
        response = future.result()
        response.raise_for_status()
        # set location header
        response.headers['location'] = location
        # check location header
        resource._handle_response(None, response)
        assert 'ref' in response.path
        assert response.path['ref'] == '$ref'
        del response.headers['location']
        # set content-location header
        response.headers['content-location'] = location
        # check content-location header
        resource._handle_response(None, response)
        assert 'ref' in response.path
        assert response.path['ref'] == '$ref'
        del response.headers['content-location']
        # check etag header
        response.headers['ETag'] = '"$ref-gzip"'
        # check content-location header
        resource._handle_response(None, response)
        assert 'ref' in response.path
        assert response.path['ref'] == '$ref'
        del response.headers['ETag']

    @vcr.use_cassette('fixtures/resource/async/multiple_callbacks.yaml')
    def testMultipleCallbacks(self):
        self.callback_ran = False
        def callback (session, response):
            self.callback_ran = True

        uri = '/'.join([self.uri, 'get'])
        resource = porc.Resource(uri, background_callback=callback)
        future = resource.get()
        response = future.result()
        response.raise_for_status()
        assert self.callback_ran is True

class SyncTest(BaseTest):

    @vcr.use_cassette('fixtures/resource/sync/head.yaml')
    def testHead(self):
        uri = '/'.join([self.uri, 'get'])
        resource = porc.Resource(uri, async=False)
        response = resource.head({"hello": "world"})
        response.raise_for_status()

    @vcr.use_cassette('fixtures/resource/sync/get.yaml')
    def testGet(self):
        uri = '/'.join([self.uri, 'get'])
        resource = porc.Resource(uri, async=False)
        response = resource.get({"hello": "world"})
        response.raise_for_status()

    @vcr.use_cassette('fixtures/resource/sync/put.yaml')
    def testPut(self):
        uri = '/'.join([self.uri, 'put'])
        resource = porc.Resource(uri, async=False)
        response = resource.put({"hello": "world"})
        response.raise_for_status()

    @vcr.use_cassette('fixtures/resource/sync/post.yaml')
    def testPost(self):
        uri = '/'.join([self.uri, 'post'])
        resource = porc.Resource(uri, async=False)
        response = resource.post({"hello": "world"})
        response.raise_for_status()

    @vcr.use_cassette('fixtures/resource/sync/delete.yaml')
    def testDelete(self):
        uri = '/'.join([self.uri, 'delete'])
        resource = porc.Resource(uri, async=False)
        response = resource.delete({"hello": "world"})
        response.raise_for_status()

    @vcr.use_cassette('fixtures/resource/sync/truefalse.yaml')
    def testTrueFalseCorrection(self):
        uri = '/'.join([self.uri, 'get'])
        resource = porc.Resource(uri, async=False)
        response = resource.get({"hello": True, "goodbye": False})
        response.raise_for_status()
        assert "hello=true" in response.url
        assert "goodbye=false" in response.url

    @vcr.use_cassette('fixtures/resource/sync/handle_response.yaml')
    def testHandleResponse(self):
        location = "/v0/$collection/$key/refs/$ref"
        # get response object
        uri = '/'.join([self.uri, 'get'])
        resource = porc.Resource(uri, async=False)
        response = resource.get()
        response.raise_for_status()
        # set location header
        response.headers['location'] = location
        # check location header
        resource._handle_response(None, response)
        assert 'ref' in response.path
        assert response.path['ref'] == '$ref'
        del response.headers['location']
        # set content-location header
        response.headers['content-location'] = location
        # check content-location header
        resource._handle_response(None, response)
        assert 'ref' in response.path
        assert response.path['ref'] == '$ref'
        del response.headers['content-location']