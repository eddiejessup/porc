---
category: Graph Relations
path: '/v1/:collection/:key/relation/:kind'
title: 'Store graph relation'
type: 'PUT'

layout: nil
---

Stores a graph relation from one specified key to another specified key.

### Required parameters

* **collection**: the collection to query.
* **key**: the key for the graph query.
* **kind**: the relationship to query, e.g. "follows" or "friend" etc.

*The following parameters should be included in the URL as query strings.*

* **tocollection**: the collection in which to add the relationship to the key specified in the `tokey` parameter.
* **tokey**: the key in the collection specified in the `tocollection` parameter to add the relationship to.

### Example response headers

```HTTP/1.1 201 Created
Connection: Keep-Alive
Content-Length: 0```

