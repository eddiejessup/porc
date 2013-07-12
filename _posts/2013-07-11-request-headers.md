---
title: 'Request headers'

layout: nil
---

Clients must use request headers accordingly:

* All `PUT` requests are expected to set the `Content-Type` header to `application/json`.
* All `GET` requests must accept the `Content-Type` as `application/json` or `*/*`.