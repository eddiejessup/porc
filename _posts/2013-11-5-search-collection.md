---
category: Collections
path: '/v0/:collection?query=:query&limit=:limit&offset=:offset'
title: 'Search collection'
type: 'GET'

layout: nil
---

Returns list of collection, key, ref, and values.

### Parameters

* **collection**: the collection to query.
* **query**: a [Lucene](http://lucene.apache.org/core/4_3_0/queryparser/org/apache/lucene/queryparser/classic/package-summary.html#Overview) query string.
* **limit**: the number of results to return. (default: 10, max: 100)
* **offset**: the starting position of the results. (default: 0)

### Example response headers

```HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Date: Tue, 05 Nov 2013 14:32:00 GMT
X-ORCHESTRATE-REQ-ID: 082a5df0-4627-11e3-9f5a-22000ae8057a
Transfer-Encoding: chunked
Connection: Keep-Alive```

### Example response body

```{
    "results": [
        {
            "path": {
                "collection": "test",
                "key": "1",
                "ref": "20c14e8965d6cbb0"
            },
            "score": 1.0,
            "value": {
                "msg": "test"
            }
        }
    ],
    "count": 1,
    "total_count": 1
}```