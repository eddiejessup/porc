import vcr
import porc
import unittest
from .credentials import API_KEY

class ClientTest(unittest.TestCase):

    def setUp(self):
        self.api_key = API_KEY
        self.client = porc.Client(self.api_key)

    def test_ping(self):
        self.client.ping().raise_for_status()

    def test_get(self):
        raise NotImplementedError

    def test_post(self):
		raise NotImplementedError

    def test_put(self):
		raise NotImplementedError

    def test_delete(self):
		raise NotImplementedError

    def test_refs(self):
		raise NotImplementedError

    def test_list(self):
		raise NotImplementedError

    def test_search(self):
		raise NotImplementedError

    def test_get_relations(self):
		raise NotImplementedError

    def test_put_relation(self):
		raise NotImplementedError

    def test_delete_relation(self):
		raise NotImplementedError

    def test_get_event(self):
		raise NotImplementedError

    def test_post_event(self):
		raise NotImplementedError

    def test_put_event(self):
		raise NotImplementedError

    def test_delete_event(self):
		raise NotImplementedError

    def test_list_events(self):
		raise NotImplementedError
