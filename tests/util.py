from credentials import API_KEY
from datetime import datetime
import vcr
import unittest
import porc

class TimestampTest(unittest.TestCase):

    def testTimestamp(self):
        datetime_obj = datetime.now()
        epoch = datetime.utcfromtimestamp(0)
        delta = datetime_obj - epoch
        seconds = delta.total_seconds()
        milliseconds = int(seconds * 1000)
        timestamp = porc.util.create_timestamp(datetime_obj)
        assert milliseconds == timestamp

class FutureTest(unittest.TestCase):

    def setUp(self):
        self.client = porc.Client(API_KEY)
        self.futures = [self.client.ping(), self.client.ping(), self.client.ping()]

    @vcr.use_cassette('fixtures/util/futures.yaml')
    def testResolveFutures(self):
        responses = porc.util.resolve_futures(self.futures)
        for response in responses:
            assert response.status_code == 200