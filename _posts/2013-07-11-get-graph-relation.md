---
category: Graph Relations
path: '/v1/:collection/:key/relation/:kind'
title: 'Get graph relation'
type: 'GET'

layout: nil
---

*Note: currently non-functional.*

Returns relation's collection, key, ref, and values.

### Required parameters

* **collection**: the collection to query.
* **key**: the key for the graph query.
* **kind**: the relationship to query, e.g. "follows" or "friend" etc.

### Example response headers

```HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Connection: Keep-Alive
Content-Length: 24```

### Example response body

```{"results":[],"count":0}```