---
title: Orchestrate.io API Reference

language_tabs:
  - shell: curl
  - java
  - go

toc_footers:
 - <a href='https://dashboard.orchestrate.io'>Dashboard</a>
---

# API Version

```
/v0/$collection/$key
```

All request URIs must be prefixed with the current version of the Orchestrate API. The current version is `v0`.

# Request Headers

```shell
# With PUTs a Content-Type header must be set
curl -XPUT "https://api.orchestrate.io/v0/$collection/$key" \
	-u "$api_key:" \
	-H "Content-Type: application/json" \
	-d "$json"
```

Clients must use request headers accordingly:

* All `GET` requests return JSON and thus must set compatible accept headers, either `application/json` or `*/*`.
* All `PUT` requests must contain a valid JSON body with the `Content-Type` header set to `application/json`.

# Authentication

> Example authenticated GET for a collection/key

```shell
# Pass in your API key as the basic auth username and no password
curl "https://api.orchestrate.io/v0/$collection/$key" \
	-u "$api_key:"
```

```java
Client client = new OrchestrateClient("your api key");
```

```go
// Create a new Orchestrate.io client with your API key
c := gorc.NewClient(apiKey)
```

Authentication for Orchestrate.io applications is provided by HTTP Basic Authentication over SSL. Authenticate with an API key as the username and no password. API keys can be created or revoked from the [Orchestrate.io Dashboard](https://dashboard.orchestrate.io) on a per-application basis.

## Ping

If you wish to validate your API key, you can make an authenticated HEAD request to the /v0 endpoint (no collection name necessary). These requests do not count towards your API usage.

> Example API key validation via HEAD request

```shell
# Pass in your API key as the basic auth username and no password
curl --head "https://api.orchestrate.io/v0" \
	-u "$api_key:"
```

```java
client.ping();
```

```go
c.Ping()
```

> If the key is VALID, you will receive a HTTP 200 response

```http
HTTP/1.1 200 OK
Content-Type: application/json
Date: Thu, 24 Apr 2014 15:17:53 GMT
X-ORCHESTRATE-REQ-ID: 9b2dfb30-cbc3-11e3-a9ec-12313d2f7cdc
Connection: keep-alive
```

> If the key is INVALID, you will receive a HTTP 401 response

```http
HTTP/1.1 401 Unauthorized
Cache-Control: must-revalidate,no-cache,no-store
Content-length: 1327
Content-Type: text/html;charset=ISO-8859-1
Date: Thu, 24 Apr 2014 15:15:11 GMT
WWW-Authenticate: Basic realm="orchestrate.io"
X-ORCHESTRATE-REQ-ID: 3ac61c50-cbc3-11e3-a70a-12313d2f50f8
Connection: keep-alive
```

# Applications

Applications in Orchestrate represent the highest level of your project. Users who are members of an Application are able to view, create, and revoke API keys and use those keys to access the Application’s data. Applications are created from the [Orchestrate.io Dashboard](https://dashboard.orchestrate.io).

<aside class="warning">
Application names must be globally unique. It is good practice to prefix application names with your username or organization name.
</aside>

# Collections

Collections are groupings of the JSON objects. Collections are analogous to tables in a relational database.

## Create

You can create collections either from the Orchestrate.io Dashboard or by performing a Key/Value PUT to the collection.

## Delete

> Make sure to replace the collection variable with the appropriate collection name.


```shell
curl -i "https://api.orchestrate.io/v0/$collection?force=true" \
	-XDELETE \
	-u "$api_key:"
```

```java
boolean result =
        client.deleteCollection(collection)
              .get();
```

```go
err := c.DeleteCollection(collection)
```

Deletes an entire collection.

<aside class="notice">
To prevent accidental deletions, `force=true` must be provided in the query string.
</aside>

> Returns response headers like so:

```http
HTTP/1.1 204 No Content
Content-Type: application/json
Date: Thu, 24 Oct 2013 15:20:42 GMT
X-ORCHESTRATE-REQ-ID: d88d0ef1-3cbf-11e3-be54-22000ae8057a
Connection: keep-alive
```

`DELETE https://api.orchestrate.io/v0/$collection?force=true`

### Parameters

Parameter  | Description
---------- | -----------
collection | the collection to delete.
force      | must be set to `true` for the delete to succeed.

# Key/Value

Key/Value is core to Orchestrate.io. All other query types are built around this data type. Key/Value pairs are pieces of data identified by a unique key for a collection and have corresponding value.

## Get

> Make sure to replace the collection and key variables with the appropriate collection and key.

```shell
curl -i "https://api.orchestrate.io/v0/$collection/$key" \
	-u "$api_key:"
```

```java
KvObject<DomainObject> object =
        client.kv("someCollection", "someKey")
              .get(DomainObject.class)
              .get();
```

```go
domainObject := new(DomainObject)
result, err := c.Get(collection, key)
err = result.Value(domainObject)
```

Get the latest value assigned to a key.

<aside class="notice">
Previous versions can be retrieved by performing a GET on the fully qualified value of a GET's `Content-Location` header or a PUT's `Location` header.
</aside>

### HTTP Request

> Returns response headers like so:

```http
HTTP/1.1 200 OK
Content-Location: /v0/collection/key/refs/ad39c0f8f807bf40
Content-Type: application/json
Date: Mon, 18 Nov 2013 12:39:44 GMT
ETag: "ad39c0f8f807bf40"
X-ORCHESTRATE-REQ-ID: 80caeaa0-504e-11e3-93d8-22000a1c9574
transfer-encoding: chunked
Connection: keep-alive
```

`GET https://api.orchestrate.io/v0/$collection/$key`

### Parameters

Parameter  | Description
---------- | -----------
collection | the collection from which to get the value.
key        | the key for a value to be retrieved.

## Put (Create/Update)

> Make sure to replace the variables with the appropriate values.

```shell
curl -i "https://api.orchestrate.io/v0/$collection/$key" \
	-XPUT \
	-H "Content-Type: application/json" \
	-u "$api_key:" \
	-d "$json"
```

```java
DomainObject obj = new DomainObject(); // a POJO
final KvMetadata kvMetadata =
        client.kv("someCollection", "someKey")
              .put(obj)
              .get();
```

```go
// Put a domain object
path, err := c.Put(collection, key, domainObject)
```

Creates or updates the value at the collection/key specified. The new value will have its own unique version and that value will always be retrievable at its fully qualified 'ref' location.  That location is made available in the 'Location' response header.

<aside class="warning">
All values must be valid JSON.
</aside>

### HTTP Request

> Returns response headers like so:

```http
HTTP/1.1 201 Created
Content-Type: application/json
Date: Tue, 19 Nov 2013 15:51:04 GMT
ETag: "cbb48f9464612f20"
Location: /v0/collection/key/refs/cbb48f9464612f20
X-ORCHESTRATE-REQ-ID: 65bc9800-5132-11e3-b722-22000ab79fbb
transfer-encoding: chunked
Connection: keep-alive
```

`PUT https://api.orchestrate.io/v0/$collection/$key`

### Conditional PUTs

```shell
# An If-Match PUT
curl -i "https://api.orchestrate.io/v0/$collection/$key" \
	-XPUT \
	-H "Content-Type: application/json" \
	-H "If-Match: \"cbb48f9464612f20\"" \
	-u "$api_key:" \
	-d "$json"

# An If-None-Match PUT
curl -i "https://api.orchestrate.io/v0/$collection/$key" \
	-XPUT \
	-H "Content-Type: application/json" \
	-H "If-None-Match: \"*\" \
	-u "$api_key:" \
	-d "$json"
```

```java
// An If-Match PUT
DomainObject obj = new DomainObject(); // a POJO
KvMetadata kvMetadata =
        client.kv("someCollection", "someKey")
              .ifMatch("someRef")
              .put(obj)
              .get();

// An If-None-Match PUT
DomainObject obj = new DomainObject(); // a POJO
KvMetadata kvMetadata =
        client.kv("someCollection", "someKey")
              .ifAbsent()
              .put(obj)
              .get();
```

```go
// If-Match PUT. Takes the path of the last seen version.
path, err := c.PutIfUnmodified(path, domainObject)

// If-None-Match PUT.
path, err := c.PutIfAbsent(collection, key, domainObject)
```

Conditional headers can be used to specify a pre-condition that determines whether the store operation happens. The `If-Match` header specifies that the store operation will succeed if and only if the _ref_ value matches current stored ref. The `If-None-Match` header specifies that the store operation will succeed if and only if the key doesn't already exist.

<aside class="notice">
Conditional headers must provide a double-quoted `ETag` value returned by either a GET or PUT.
</aside>

Header        | Description
------------- | -----------
<nobr>If-Match</nobr> | Stores the value for the key if the value for this header matches the current `ref` value.
<nobr>If-None-Match</nobr> | Stores the value for the key if no key/value already exists, the only valid value for this header is `"*"`.

*If-Match* and *If-None-Match* headers cannot be supplied together.

### Parameters

Parameter  | Description
---------- | -----------
collection | the collection to which to put the value.
key        | the primary key for the value.

## Delete

> Make sure to replace the collection and key variables with the correct collection and key.

```shell
curl -i "https://api.orchestrate.io/v0/$collection/$key" \
	-XDELETE \
	-u "$api_key:"

# permanently delete KV object and all history
curl -i "https://api.orchestrate.io/v0/$collection/$key?purge=true" \
    -XDELETE \
    -u "$api_key:"
```

```java
boolean result =
        client.kv("someCollection", "someKey")
              .delete()
              .get();
```

```go
err := c.Delete(collection, key)
```

Deletes set the value of a key to a null object. Previous versions of an object are retrievable at its fully qualified 'ref' location. If the `purge` parameter is supplied the object and its `ref` history will be permanently deleted.

### HTTP Request

> Returns response headers like so:

```http
HTTP/1.1 204 No Content
Content-Type: application/json
Date: Tue, 19 Nov 2013 15:53:04 GMT
X-ORCHESTRATE-REQ-ID: ad131350-5132-11e3-b722-22000ab79fbb
Connection: keep-alive
```

`DELETE https://api.orchestrate.io/v0/$collection/$key`

### Conditional DELETEs

```shell
curl -i "https://api.orchestrate.io/v0/$collection/$key" \
	-XDELETE \
	-H "If-Match: \"cbb48f9464612f20\"" \
	-u "$api_key:"
```

```java
boolean result =
        client.kv("someCollection", "someKey")
              .ifMatch("someRef")
              .delete()
              .get();
```

```go
// If-Match Delete
err := c.DeleteIfUnmodified(path)
```

Conditional headers can be used to specify a pre-condition that determines whether the delete operation happens. The `If-Match` header specifies that the delete operation will succeed if and only if the _ref_ value matches current stored ref.

<aside class="notice">
Conditional headers must provide a double-quoted `ETag` value returned by either a GET or PUT.
</aside>

Header        | Description
------------- | -----------
<nobr>If-Match</nobr> | Deletes the value for the key if the value for this header matches the current `ref` value.

### Parameters

Parameter  | Description
---------- | -----------
collection | the collection to delete from.
key        | the key to delete.
purge      | If `true` the KV object and all of its `ref` history will be permanently deleted. This operation cannot be undone.

## List

> Make sure to replace all the variables with the appropriate values.

```shell
# Inclusive start key
curl -i "https://api.orchestrate.io/v0/$collection?startKey=$startKey&limit=$limit" \
	-u "$api_key:"

# Exclusive after key
curl -i "https://api.orchestrate.io/v0/$collection?afterKey=$afterKey&limit=$limit" \
	-u "$api_key:"

# Inclusive start key up to an exclusive end key
curl -i "https://api.orchestrate.io/v0/$collection?startKey=$startKey&beforeKey=$beforeKey&limit=$limit" \
    -u "$api_key:"
```

```java
KvList<DomainObject> kvList =
        client.listCollection("someCollection")
              .limit(20)
              .get(DomainObject.class)
              .get();
```

```go
// List from beginning
results, err := c.List(collection, limit)

// List after key
results, err := c.ListAfter(collection, afterKey, limit)

//List starting with key
results, err := c.ListStart(collection, startKey, limit)

// Get next page
if results.HasNext() {
	nextResults, err := c.ListGetNext(results)
}
```

Returns a paginated, lexicographically ordered list of items contained in a
collection. The next page of results URL is specified by both the `next` field
in the JSON response and the `Link` header value. If no `next` field or `Link`
header is returned, there are no additional pages.

### HTTP Request

> Returns response headers like so:

```http
HTTP/1.1 200 OK
Content-Type: application/json
Date: Wed, 22 Jan 2014 14:16:08 GMT
Link: </v0/collection?limit=2&afterKey=002>; rel="next"
X-ORCHESTRATE-REQ-ID: bce1f3e0-836f-11e3-abae-12313d2f7cdc
transfer-encoding: chunked
Connection: keep-alive
```

> Returns a response body like so:

```json
{
    "count": 2,
    "next": "/v0/collection?limit=2&afterKey=002",
    "results": [
        {
            "path": {
                "collection": "collection",
                "key": "001",
                "ref": "20c14e8965d6cbb0"
            },
            "value": {
                "msg": "test"
            }
        },
        {
            "path": {
                "collection": "collection",
                "key": "002",
                "ref": "20c14e8965d6cbb0"
            },
            "value": {
                "msg": "test"
            }
        }
    ]
}
```

`GET https://api.orchestrate.io/v0/$collection?limit=$limit&afterKey=$afterKey`

### Parameters

Parameter  | Description
---------- | -----------
collection | the collection to list from.
limit      | the number of results to return. (default: 10, max: 100)
startKey   | the start of the key range to paginate from including the specified value if it exists.
afterKey   | the start of the key range to paginate from excluding the specified value if it exists.
beforeKey  | the end of the key range to paginate to excluding the specified value if it exists.
endKey     | the end of the key range to paginate to including the specified value if it exists.

<aside class="notice">
To include all keys in a collection, do not provide any "Key" parmeters (`startKey`, `afterKey`, `beforeKey`, `endKey`).
</aside>

# Refs

Refs are used to identify specific immutable values that have been assigned to keys.

## Get

> Make sure to replace the variables with the appropriate values.

```shell
curl -i "https://api.orchestrate.io/v0/$collection/$key/refs/$ref" \
	-u "$api_key:"
```

```java
KvObject<DomainObject> object =
        client.kv("someCollection", "someKey")
              .get(DomainObject.class, "someRef")
              .get();
```

```go
domainObject := new(DomainObject)
result, err := c.GetPath(path)
err = result.Value(domainObject)
```

Returns the specified version of a value.

### HTTP Request

> Returns response headers like so:

```http
HTTP/1.1 200 OK
Content-Location: /v0/collection/key/refs/ad39c0f8f807bf40
Content-Type: application/json
Date: Mon, 18 Nov 2013 12:39:44 GMT
ETag: "ad39c0f8f807bf40"
X-ORCHESTRATE-REQ-ID: 80caeaa0-504e-11e3-93d8-22000a1c9574
transfer-encoding: chunked
Connection: keep-alive
```

`GET https://api.orchestrate.io/v0/$collection/$key/ref/$ref`

### Parameters

Parameter  | Description
---------- | -----------
collection | the collection from which to get the value.
key        | the primary key of the value.
ref        | an opaque version identifier for the value.

# Search

Search allows collections to be queried using [Lucene Query Parser Syntax](http://lucene.apache.org/core/4_3_0/queryparser/org/apache/lucene/queryparser/classic/package-summary.html#Overview).

## Collection

> Make sure to replace all the variables with the appropriate values.

```shell
curl -i "https://api.orchestrate.io/v0/$collection?query=$query&limit=$limit&offset=$offset" \
	-u "$api_key:"
```

```java
String luceneQuery = "*";
SearchResults<DomainObject> results =
        client.searchCollection("someCollection")
              .limit(20)
              .get(DomainObject.class, luceneQuery)
              .get();
```

```go
results, err := c.Search(collection, query, offset, limit)

// Get next page
if results.HasNext() {
	nextResults, err := c.SearchGetNext(results)
}

// Get previous page
if results.HasPrev() {
	nextResults, err := c.SearchGetPrev(results)
}
```

Returns list of items matching the lucene query. The next page of results URL is specified by both the `next` field in the JSON response and the `Link` header value with a rel=`next`. If no `next` field or `Link` header is returned, there are no additional pages. The same is true for a previous page. If there are preceding results, then there will be a URL specified by both the `prev` field in the JSON response and a `Link` header with rel=`prev`. 

### HTTP Request

> Returns response headers like so:

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Date: Tue, 05 Nov 2013 14:32:00 GMT
Link: </v0/collection?limit=10&query=test&offset=20>; rel="next"
Link: </v0/collection?limit=10&query=test&offset=0>; rel="prev"
X-ORCHESTRATE-REQ-ID: 082a5df0-4627-11e3-9f5a-22000ae8057a
Transfer-Encoding: chunked
Connection: Keep-Alive
```

> Returns a response body like so (some `results` ommitted for clarity):

```json
{
    "count": 10,
    "next": "/v0/collection?limit=10&query=test&offset=20",
    "prev": "/v0/collection?limit=10&query=test&offset=0",
    "results": [
        {
            "path": {
                "collection": "collection",
                "key": "key",
                "ref": "20c14e8965d6cbb0"
            },
            "score": 1.0,
            "value": {
                "msg": "test"
            }
        }
    ],
    "total_count": 1
}
```

`GET https://api.orchestrate.io/v0/$collection?query=$query&limit=$limit&offset=$offset`

### Parameters

Parameter  | Description
---------- | -----------
collection | the collection to search.
query      | a [Lucene](http://lucene.apache.org/core/4_3_0/queryparser/org/apache/lucene/queryparser/classic/package-summary.html#Overview) query string.
limit      | the number of results to return. (default: 10, max: 100)
offset     | the starting position of the results. (default: 0)

# Events

Events are a way to associate time-ordered data with a key.

## Get

> Make sure to replace all the variables with the appropriate values.

```shell
curl -i "https://api.orchestrate.io/v0/$collection/$key/events/$type/$timestamp/$ordinal" \
	-u "$api_key:"
```

```java
/*
NOT CURRENTLY SUPPORTED

To get a single event, use the 'List' api with the start and end timestamps,
and then loop through them. The results will only contain Events with the
specified timestamp milliseconds.
*/
Iterable<Event<DomainObject>> results =
        client.event("someCollection", "someKey")
              .type("eventType")
              .start(someTimestamp)
              .end(someTimestamp + 1)
              .get(DomainObject.class)
              .get();
```

```go
/*
NOT CURRENTLY SUPPORTED

To get a single event, use the 'List' api with the start and end timestamps,
and then loop through them. The results will only contain Events with the
specified timestamp milliseconds.
*/
events, err := c.GetEventsInRange(collection, key, typ, timestamp, timestamp + 1)
```

Returns an individual event.

### HTTP Request

> Returns response headers like so:

```http
HTTP/1.1 200 OK
Date: Wed, 11 Dec 2013 14:47:11 GMT
Content-Type: application/json
Connection: keep-alive
X-ORCHESTRATE-REQ-ID: cd3965d0-cb2b-11e3-b13e-0e490195c851
ETag: "ae3dfa4325abe21e"
```

> And a response body like so:

```json
{
    "path": {
        "collection": "asdf",
        "key": "key",
        "ref": "ae3dfa4325abe21e",
        "type": "played",
        "timestamp": 1369832019085,
        "ordinal": 9
    },
    "value": {
      "msg": "hello world, again"
    },
    "timestamp": 1369832019085,
    "ordinal": 9
}
```

`GET https://api.orchestrate.io/v0/$collection/$key/events/$type/$timestamp/$ordinal`

### Parameters

Parameter  | Description
---------- | -----------
collection | the collection from which to get the event.
key        | the primary key associated with the event.
type       | the category for the event, e.g. "update" or "tweet" etc.
timestamp  | the event timestamp.
ordinal    | the event ordinal.

<aside class="notice">
The timestamp value should be formatted as described in [Timestamps](#timestamps).
</aside>

## Post (Create)
> Make sure to replace all the variables with the appropriate values.

```shell
# With timestamp
curl -i "https://api.orchestrate.io/v0/$collection/$key/events/$type/$timestamp" \
  -XPOST \
  -H "Content-Type: application/json" \
  -u "$api_key:" \
  -d "{\"msg\":\"hello\"}"

# Without timestamp (the event timestamp will be set to the current time in Orchestrate)
curl -i "https://api.orchestrate.io/v0/$collection/$key/events/$type" \
  -XPOST \
  -H "Content-Type: application/json" \
  -u "$api_key:" \
  -d "{\"msg\":\"hello\"}"

```

```java
/*
NOT CURRENTLY SUPPORTED

To create an Event, use the 'Put' api (which is now deprecated).
*/
DomainObject obj = new DomainObject(); // a POJO
boolean result =
        client.event("someCollection", "someKey")
              .type("eventType")
              .put(obj)
              .get();
```

```go
/*
NOT CURRENTLY SUPPORTED

To create an Event, use the 'Put' api (which is now deprecated).
*/
err := c.PutEvent(collection, key, typ, domainObject)
```

Creates an event with an optional user defined timestamp.

### HTTP Request

> Returns response headers like so:

```http
HTTP/1.1 201 Created
Date: Tue, 19 Nov 2013 13:51:54 GMT
Content-Type: application/json
Connection: keep-alive
X-ORCHESTRATE-REQ-ID: 93a94ad0-cb29-11e3-b13e-0e490195c851
Location: /v0/collection/key/events/type/1398286518286/6
ETag: "f8a86a25029a907b"
```

```POST /v0/$collection/$key/events/$type/$timestamp```

### Parameters

Parameter  | Description
---------- | -----------
collection | the collection to which to put the event.
key        | the primary key associated with the event.
type       | the category for an event, e.g. "update" or "tweet" etc.
timestamp  | the timestamp to associate with the event. (optional) 

<aside class="notice">
The timestamp value should be formatted as described in [Timestamps](#timestamps).
</aside>

<aside class="warning">
Previously, a PUT to the $type would create and Event. This is now deprecated, and will be removed in the next version.
</aside>


## Put (Update)

> Make sure to replace all the variables with the appropriate values.

```shell
curl -i "https://api.orchestrate.io/v0/$collection/$key/events/$type/$timestamp/$ordinal" \
	-XPUT \
	-H "Content-Type: application/json" \
	-u "$api_key:" \
	-d "{\"msg\":\"hello2\"}"
```

```java
// NOT CURRENTLY SUPPORTED
```

```go
// NOT CURRENTLY SUPPORTED
```

Updates an existing event.

### HTTP Request

> Returns response headers like so:

```http
HTTP/1.1 204 No Content
Date: Tue, 19 Nov 2013 13:51:54 GMT
Content-Type: application/json
Connection: keep-alive
X-ORCHESTRATE-REQ-ID: 7fa4d260-cb2a-11e3-b13e-0e490195c851
Location: /v0/collection/key/events/type/1398286914202/9
ETag: "ae3dfa4325abe21e"
```

```PUT /v0/$collection/$key/events/$type/$timestamp/$ordinal```
### Conditional PUTs

```shell
# An If-Match PUT
curl -i "https://api.orchestrate.io/v0/$collection/$key/events/$type/$timestamp/$ordinal" \
  -XPUT \
  -H "Content-Type: application/json" \
  -H "If-Match: \"ae3dfa4325abe21e\"" \
  -u "$api_key:" \
  -d "$json"
```

```java
// NOT CURRENTLY SUPPORTED
```

```go
// NOT CURRENTLY SUPPORTED
```

Conditional headers can be used to specify a pre-condition that determines whether the update operation happens. The `If-Match` header specifies that the update will succeed if and only if the _ref_ value matches current stored ref for the Event.

<aside class="notice">
Conditional headers must provide a double-quoted `ETag` value returned by other api calls or the "path.ref" value of an event.
</aside>

Header        | Description
------------- | -----------
<nobr>If-Match</nobr> | Stores the value for the event if the value for this header matches the current `ref` value.

### Parameters

Parameter  | Description
---------- | -----------
collection | the collection the event is in.
key        | the primary key associated with the event.
type       | the category for the event, e.g. "update" or "tweet" etc.
timestamp  | the event's timestamp.
ordinal    | the event's ordinal value.

<aside class="notice">
The timestamp value should be formatted as described in [Timestamps](#timestamps).
</aside>

## Delete

> Make sure to replace all the variables with the appropriate values.

```shell
curl -i "https://api.orchestrate.io/v0/$collection/$key/events/$type/$timestamp/$ordinal?purge=true" \
  -u "$api_key:"
  -XDELETE
```

```java
// NOT CURRENTLY SUPPORTED
```

```go
// NOT CURRENTLY SUPPORTED
```

Deletes an individual event.

### HTTP Request

> Returns response headers like so:

```http
HTTP/1.1 204 No Content
Date: Wed, 11 Dec 2013 14:47:11 GMT
Content-Type: application/json
Connection: keep-alive
X-ORCHESTRATE-REQ-ID: cd3965d0-cb2b-11e3-b13e-0e490195c851
```

`DELETE https://api.orchestrate.io/v0/$collection/$key/events/$type/$timestamp/$ordinal?purge=true`

### Conditional DELETEs

```shell
curl -i "https://api.orchestrate.io/v0/$collection/$key/events/$type/$timestamp/$ordinal" \
  -XDELETE \
  -H "If-Match: \"ae3dfa4325abe21e\"" \
  -u "$api_key:"
```

```java
// NOT CURRENTLY SUPPORTED
```

```go
// NOT CURRENTLY SUPPORTED
```

Conditional headers can be used to specify a pre-condition that determines whether the delete operation happens. The `If-Match` header specifies that the delete operation will succeed if and only if the _ref_ value matches current stored ref.

<aside class="notice">
Conditional headers must provide a double-quoted `ETag` value returned by either a GET or PUT.
</aside>

Header        | Description
------------- | -----------
<nobr>If-Match</nobr> | Deletes the value for the Event if the value for this header matches the current `ref` value.

### Parameters

Parameter  | Description
---------- | -----------
collection | the collection from which to get the event.
key        | the primary key associated with the event.
type       | the category for the event, e.g. "update" or "tweet" etc.
timestamp  | the event timestamp.
ordinal    | the event ordinal.
purge      | indicates that all versions will be deleted (currently required for events).

<aside class="notice">
The timestamp value should be formatted as described in [Timestamps](#timestamps).
</aside>

## List

> Make sure to replace all the variables with the appropriate values.

```shell
curl -i "https://api.orchestrate.io/v0/$collection/$key/events/$type?startEvent=$startEvent&endEvent=$endEvent" \
  -u "$api_key:"
```

```java
Iterable<Event<DomainObject>> results =
        client.event("someCollection", "someKey")
              .type("eventType")
              .get(DomainObject.class)
              .get();
```

```go
// Get most recent events
events, err := c.GetEvents(collection, key, typ)

// Get events in range
events, err := c.GetEventsInRange(collection, key, typ, start, end)
```

Returns a paginated list of events, optionally limited to specified time range in reverse chronological order. The next page of results URL is specified by both the next field in the JSON response and the Link header value. If no next field or Link header is returned, there are no additional pages.

### HTTP Request

> Returns response headers like so:

```http
HTTP/1.1 200 OK
Content-Type: application/json
Date: Wed, 11 Dec 2013 14:47:11 GMT
X-ORCHESTRATE-REQ-ID: 1db50310-6273-11e3-9fbc-12313d2f7cdc
Link: </v0/collection/key/events/type/?limit=2&beforeEvent=1369832019080/7>; rel="next"
```

> And a response body like so:

```json
{
  "results": [
    {
      "path": {
        "collection": "collection",
        "key": "key",
        "type": "type",
        "timestamp": 1369832019085,
        "ordinal": 9,
        "ref": "ae3dfa4325abe21e"
      },
      "value": {
        "msg": "hello world, again"
      },
      "timestamp": 1369832019085,
      "ordinal": 9
    },
    {
      "path": {
        "collection": "collection",
        "key": "key",
        "type": "type",
        "timestamp": 1369832019080,
        "ordinal": 7,
        "ref": "f8a86a25029a907b"
      },
      "value": {
        "msg": "hello world"
      },
      "timestamp": 1369832019080,
      "ordinal": 7
    }
  ],
  "count": 2,
  "next": "/v0/collection/key/events/type/?limit=2&beforeEvent=1369832019080/7"
}
```

`GET https://api.orchestrate.io/v0/$collection/$key/events/$type?startEvent=$startEvent&endEvent=$endEvent`

### Parameters

Parameter   | Description
----------- | -----------
collection  | the collection from which to get the events.
key         | the primary key associated with the events.
type        | the category for an event, e.g. "update" or "tweet" etc.
limit       | the number of results to return. (default: 10, max: 100)
start       | [DEPRECATED] the inclusive start of a time range to query. (optional)
end         | [DEPRECATED] the exclusive end of a time range to query. (optional)
startEvent  | the inclusive start of a range to query. (optional)
afterEvent  | the non-inclusive start of a range to query. (optional)
beforeEvent | the non-inclusive end of a range to query. (optional)
endEvent    | the inclusive end of a range to query. (optional)

<aside class="notice">
The range parameters are formatted as "$timestamp/$ordinal" where $ordinal is optional.
The timestamp value should be formatted as described in [Timestamps](#timestamps).
</aside>
## Timestamps


There are several event api calls that take a "timestamp" as a parameter (either as a url path parm or a query param).

Wherever a timestamp is expected in the events api calls, the value can be in any of the following formats:

- A Long that is the milliseconds since epoch
  - 784111777000
  - 784111777221
- ISO8601 Basic with or without the milliseconds portion
  - 19941106T084937Z
  - 19941106T084937.221Z
  - 19941106T014937-0700
  - 19941106T014937.221-0700
- ISO8601 Extended with or without the milliseconds portion
  - 1994-11-06T08:49:37Z
  - 1994-11-06T08:49:37.221Z
  - 1994-11-06T01:49:37-07:00
  - 1994-11-06T01:49:37.221-07:00
- RFC2616 Compatible Dates. This allows the following formats:
  - RFC1123
     - Sun, 06 Nov 1994 08:49:37 UTC
     - Sun, 06 Nov 1994 01:49:37 MST
     - Sun, 06 Nov 1994 01:49:37 -0700
  - RFC1036 (2-digit date supported and uses 2000 as start year)
     - Sunday, 06-Nov-1994 08:49:37 UTC
     - Sunday, 06-Nov-1994 01:49:37 MST
     - Sunday, 06-Nov-1994 01:49:37 -0700
  - ASCTIME (UTC Enforced)
     - Sun Nov 6 08:49:37 1994

<aside class="notice">
While the api will accept all these formats as input parameters, the event timestamp is always returned by the api as milliseconds since epoch.
</aside>


# Graph

The Graph functionality allows for directed relations to be created between collection/key pairs and for those relations to be traversed.

## Get

> Make sure to replace all the variables with the appropriate values.

```shell
# One hop
curl -i "https://api.orchestrate.io/v0/$collection/$key/relations/$kind" \
	-u "$api_key:"

# Two hops
curl -i "https://api.orchestrate.io/v0/$collection/$key/relations/$kind1/$kind2" \
	-u "$api_key:"
```

```java
// One hop
Iterable<KvObject<DomainObject>> results =
        client.relation("someCollection", "someKey")
              .get(DomainObject.class, "someKind")
              .get();

// Two hops
Iterable<KvObject<DomainObject>> results =
        client.relation("someCollection", "someKey")
              .get(DomainObject.class, "someKind", "someKind")
              .get();
```

```go
// One hop
results, err := c.GetRelations(collection, key, []string{kind})

// Two hops
results, err := c.GetRelations(collection, key, []string{kind1, kind2})
```

Returns relation's collection, key, ref, and values. The "kind" parameter(s) indicate which relations to walk and the depth to walk.

e.g. Get users that are friends of John's family members.

### HTTP Request

> Returns response headers like so:

```http
HTTP/1.1 200 OK
Content-Type: application/json
Date: Tue, 19 Nov 2013 15:33:58 GMT
X-ORCHESTRATE-REQ-ID: 01c318d0-5130-11e3-b722-22000ab79fbb
transfer-encoding: chunked
Connection: keep-alive
```

> And a response body like so:

```json
{
    "count": 1,
    "results": [
        {
            "path": {
                "collection": "users",
                "key": "matt",
                "ref": "0acfe7843316529f"
            },
            "value": {
                "age": 23,
                "name": "Matthew Jones"
            }
        }
    ]
}
```

```GET /v0/$collection/$key/relations/$kind1/$kind2 ...```

### Parameters

Parameter  | Description
---------- | -----------
collection | the collection to query.
key        | the primary key for a value.
kind       | the relationship kind to query, e.g. "follows" or "friend" etc.

## Put

> Make sure to replace all the variables with the appropriate values.

```shell
curl -i "https://api.orchestrate.io/v0/$collection/$key/relation/$kind/$to_collection/$to_key" \
	-XPUT \
	-u "$api_key:"
```

```java
boolean result =
        client.relation("sourceCollection", "sourceKey")
              .to("destCollection", "destKey")
              .put("someKind")
              .get();
```

```go
err := c.PutRelation(collection, key, kind, toCollection, toKey)
```

Creates a relationship between two objects. Relations can span collections.

<aside class="notice">
Both ends of the relation must exist.
</aside>

### HTTP Request

> Returns response headers like so:

```http
HTTP/1.1 204 No Content
Content-Type: application/json
Date: Tue, 19 Nov 2013 13:51:54 GMT
X-ORCHESTRATE-REQ-ID: bfc4e750-5121-11e3-be8f-22000ab58c12
Connection: keep-alive
```

```PUT /v0/$collection/$key/relation/$kind/$toCollection/$toKey```

### Parameters

Parameter  | Description
---------- | -----------
collection | the collection from which the relation originates.
key        | the key from which the relation originates.
kind       | the relationship kind to query, e.g. "follows" or "friend" etc.
toCollection | the collection to which the relation goes.
toKey      | the key to which the relation goes.

## Delete

> Make sure to replace all the variables with the appropriate values.

```shell
curl -i "https://api.orchestrate.io/v0/$collection/$key/relation/$kind/$to_collection/$to_key?purge=true" \
    -XDELETE \
    -u "$api_key:"
```

```java
boolean result =
        client.relation("sourceCollection", "sourceKey")
              .to("destCollection", "destKey")
              .purge("someKind")
              .get();
```

```go
err := c.DeleteRelation(sourceCollection, sourceKey, kind, destCollection, destKey)
```

Deletes a relationship between two objects.

<aside class="notice">
You must supply the `purge` parameter to delete a relationship. This parameter is not optional.
</aside>

### HTTP Request

> Returns response headers like so:

```http
HTTP/1.1 204 No Content
Content-Type: application/json
Date: Tue, 19 Nov 2013 13:51:54 GMT
X-ORCHESTRATE-REQ-ID: bfc4e750-5121-11e3-be8f-22000ab58c12
Connection: keep-alive
```

```DELETE /v0/$collection/$key/relation/$kind/$toCollection/$toKey?purge=true```

### Parameters

Parameter  | Description
---------- | -----------
collection | the collection from which the relation originates.
key        | the key from which the relation originates.
kind       | the relationship kind to query, e.g. "follows" or "friend" etc.
toCollection | the collection to which the relation goes.
toKey      | the key to which the relation goes.
purge      | This parameter is required to delete a relationship. This operation cannot be undone.

# Errors

Orchestrate.io uses the following error codes:

Status | Error Code | Description
------ | ---------- | -----------
400 | api_bad_request | The API request is malformed.
500 | security_authentication | An error occurred while trying to authenticate.
401 | security_unauthorized | Valid credentials are required.
400 | search_param_invalid | A provided search query param is invalid.
500 | search_index_not_found | Index could not be queried for this application.
500 | internal_error | Internal Error.
404 | items_not_found | The requested items could not be found.
412 | item_version_mismatch | The version of the item does not match.
412 | item_already_present | The item is already present.
400 | item_ref_malformed | The provided Item Ref is malformed.
409 | indexing_conflict | The item has been stored but conflicts were detected when indexing. Conflicting fields have not been indexed.
