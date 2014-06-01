from .credentials import API_KEY
from datetime import datetime
import vcr
import unittest
import porc

class TimestampTest(unittest.TestCase):

    def testTimestamp(self):
        datetime_obj = datetime.now()
        epoch = datetime.utcfromtimestamp(0)
        delta = datetime_obj - epoch
        if hasattr(delta, 'total_seconds'):
            seconds = delta.total_seconds()
        else:
            seconds = (delta.microseconds + (delta.seconds + delta.days * 24 * 3600) * 10**6) / 10.0**6
        milliseconds = int(seconds * 1000)
        timestamp = porc.util.create_timestamp(datetime_obj)
        assert milliseconds == timestamp
