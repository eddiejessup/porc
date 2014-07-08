from requests import Response as Requests_Response

URL_PATTERNS = [
    "/v0/(?P<collection>.+)/(?P<key>.+)/events/(?P<type>.+)/(?P<timestamp>\d+)/(?P<ordinal>\d+)",
    "/v0/(?P<collection>.+)/(?P<key>.+)/refs/(?P<ref>.+)"
]

class Response(dict):
    def __init__(self, resp):
        self.response = resp
        self.json = self.response.json()
        self._set_path()

    def _set_path(self):
        for regex in URL_PATTERNS:
            # check location
            location_match = re.match(
                regex, self.response.headers.get('location', ''))
            # if not in location, try content-location
            if not location_match:
                location_match = re.match(
                    regex, self.response.headers.get('content-location', ''))
            # else, try the etag
            if not location_match:
                location_match = re.match('"(?P<ref>.+)-gzip"', self.response.headers.get('ETag', ''))
            # if a match was found in either place, attach it to self
            if location_match:
                for key, value in location_match.groupdict().items():
                    setattr(self, key, value)
                break

    def __getattr__(self, name):
        return getattr(self.response, name)

    def __getitem__(self, key):
        return self.json.get(key)

    def __setitem__(self, key, value):
        self.json[key] = value