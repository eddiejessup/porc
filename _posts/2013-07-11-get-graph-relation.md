---
category: Graph Relations
path: '/v0/:collection/:key/relation/?hop=:kind[&hop=:kind]*'
title: 'Get graph relation'
type: 'GET'

layout: nil
---

Returns relation's collection, key, ref, and values. The "hop" query parameter(s) indicate which relations to walk and the depth to walk.

e.g. Get users that are friends of John's family members.

```GET /v0/users/john/relation/?hop=family&hop=friend```

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
