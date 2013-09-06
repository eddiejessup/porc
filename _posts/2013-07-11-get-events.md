---
category: Events
path: '/v0/:collection/:key/events/:type'
title: 'Get events'
type: 'GET'

layout: nil
---

Returns a list of events, optionally limited to specified time range.

### Required parameters

* **collection**: the collection to query.
* **key**: the key for the event query.
* **type**: the category for an event, e.g. "update" or "tweet" etc.

### Optional paramaters

*To be provided as query parameters in the URL.*

* **start**: the start of a time range to query.
* **end**: the end of a time range to query.

### Example response headers

```HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Connection: Keep-Alive
Content-Length: 81```

### Example response body

```{"results":[{"timestamp":1369832019085,"value":{"msg":"hello world"}}],"count":1}```


