---
category: Keys
path: '/v0/:collection/:key'
title: 'Delete value at key'
type: 'DELETE'

layout: nil
---

Deletes the value for a key.

### Parameters

* **collection**: the collection to access.
* **key**: the key whose value should be deleted.

### Example response headers

```HTTP/1.1 204 No Content
Content-Type: application/json
Date: Thu, 24 Oct 2013 15:20:42 GMT
X-ORCHESTRATE-REQ-ID: d88d0ef1-3cbf-11e3-be54-22000ae8057a
Connection: keep-alive```