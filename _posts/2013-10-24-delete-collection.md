---
category: Collections
path: '/v0/:collection/?force=true'
title: 'Delete collection'
type: 'DELETE'

layout: nil
---

Deletes an entire collection.

Delete operations cannot be undone, as a result, to avoid accidental deletions when experimenting with the API the query parameter _force=true_ is necessary.

### Parameters

* **collection**: the collection to delete.

### Example response headers

```HTTP/1.1 204 No Content
Content-Type: application/json
Date: Thu, 24 Oct 2013 15:20:42 GMT
X-ORCHESTRATE-REQ-ID: d88d0ef1-3cbf-11e3-be54-22000ae8057a
Connection: keep-alive```
