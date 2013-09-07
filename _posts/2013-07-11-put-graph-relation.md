---
category: Graph Relations
path: '/v0/:collection/:key/relations/:kind/:toCollection/:toKey'
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

* **toCollection**: the collection in which to add the relationship to the key specified in the `toKey` parameter.
* **toKey**: the key in the collection specified in the `toCollection` parameter to add the relationship to.

### Example response headers

```HTTP/1.1 201 Created
Connection: Keep-Alive
Content-Length: 0```

