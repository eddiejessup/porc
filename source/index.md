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

> Make sure to replace the API Key variable with your API key.

```shell
# Pass in your API key as the basic auth username and no password
curl "https://api.orchestrate.io/v0/$collection/$key" \
	-u "$api_key:"
```

```java
Client client = new Client("your api key");
```

```go
// Create a new Orchestrate.io client with your API key
c := client.NewClient(apiKey)
```

Authenication for Orchestrate.io applications is provided by HTTP Basic Authentication over SSL. Authenticate with an API key as the username and no password. API keys can be created or revoked from the [Orchestrate.io Dashboard](https://dashboard.orchestrate.io).

# Applications

Applications are the unit of tenancy in Orchestrate.io. Users who are members of an Application are able to view, create, and revoke API keys and use those keys to access the Application's data. Applications are created from the [Orchestrate.io Dashboard](https://dashboard.orchestrate.io).

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
DeleteOperation deleteOp = new DeleteOperation("collectionName");
Future<Boolean> future = client.execute(deleteOp);
Boolean result = future.get(3, TimeUnit.SECONDS);
if (result) {
    System.out.println("Successfully deleted the collection.");
}
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
KvFetchOperation<MyObject> kvFetchOp =
        new KvFetchOperation<MyObject>("collection", "key", MyObject.class);
Future<KvObject<MyObject>> future = client.execute(kvFetchOp);
KvObject<MyObject> result = future.get(3, TimeUnit.SECONDS);
MyObject domainObject = result.getValue();
```

```go
domainObject := new(DomainObject)
err := c.Get(collection, key, domainObject)
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
MyObject domainObject = new MyObject(...);
KvStoreOperation kvStoreOp =
        new KvStoreOperation("collection", "key", domainObject);
Future<Boolean> future = client.execute(kvStoreOp);
Boolean result = future.get(3, TimeUnit.SECONDS);
if (result) {
	System.out.println("Successfully stored the object.");
}
```

```go
err := c.Put(collection, key, domainObject)
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
```

```java
DeleteOperation deleteOp = new DeleteOperation("collection", "key");
Future<Boolean> future = client.execute(deleteOp);
Boolean result = future.get(3, TimeUnit.SECONDS);
if (result) {
	System.out.println("Successfully deleted the key.");
}
```

```go
err := c.Delete(collection, key)
```

Deletes set the value of a key to a null object. Previous versions of an object are retrievable at its fully qualified 'ref' location.

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

## List

> Make sure to replace all the variables with the appropriate values.

```shell
# Inclusive start key
curl -i "https://api.orchestrate.io/v0/$collection?startKey=$startKey&limit=$limit" \
	-u "$api_key:"

# Exclusive after key
curl -i "https://api.orchestrate.io/v0/$collection?afterKey=$afterKey&limit=$limit" \
	-u "$api_key:"
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
Link: </v0/collection?limit=100&afterKey=099>; rel="next"
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
afterKey   | the start of the key range to paginate from excluding the specified value.

<aside class="notice">
To include all keys in a collection, do not provide a `startKey` or `afterKey` value.
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
KvFetchOperation<MyObject> kvFetchOp =
        new KvFetchOperation<MyObject>(
        "collection", "key", "ref", MyObject.class);
Future<KvObject<MyObject>> future = client.execute(kvFetchOp);
KvObject<MyObject> result = future.get(3, TimeUnit.SECONDS);
MyObject domainObject = result.getValue();
```

```go
err := c.GetRef(collection, key, ref, domainObject)
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
SearchOperation<MyObject> searchOp = SearchOperation
        .builder("collection", MyObject.class)
        .query("*")
        .limit(10)
        .offset(0)
        .build();
Future<SearchResults<MyObject>> future = client.execute(searchOp);
SearchResults<MyObject> results = future.get(3, TimeUnit.SECONDS);
for (Result<MyObject> result : results) {
	System.out.println(result.getScore());
	System.out.println(result.getKvObject().getValue());
}
```

```go
results, err := c.Search(collection, query, offset, limit)
```

Returns list of items matching the lucene query.

### HTTP Request

> Returns response headers like so:

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Date: Tue, 05 Nov 2013 14:32:00 GMT
X-ORCHESTRATE-REQ-ID: 082a5df0-4627-11e3-9f5a-22000ae8057a
Transfer-Encoding: chunked
Connection: Keep-Alive
```

> Returns a response body like so:

```json
{
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
    "count": 1,
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
curl -i "https://api.orchestrate.io/v0/$collection/$key/events/$type?start=$start&end=$end" \
	-u "$api_key:"
```

```java
EventFetchOperation<MyObject> eventFetchOp =
        new EventFetchOperation<MyObject>(
        "collection", "key", "type", MyObject.class);
Future<Iterable<Event<MyObject>>> future = client.execute(eventFetchOp);
Iterable<Event<MyObject>> events = future.get(3, TimeUnit.SECONDS);
for (Event<MyObject> event : events) {
	System.out.println(event.getTimestamp());
	System.out.println(event.getValue());
}
```

```go
events, err := c.GetEvents(collection, key, typ, start, end)
```

Returns a list of events, optionally limited to specified time range in reverse chronological order.

### HTTP Request

> Returns response headers like so:

```http
HTTP/1.1 200 OK
Content-Type: application/json
Date: Wed, 11 Dec 2013 14:47:11 GMT
X-ORCHESTRATE-REQ-ID: 1db50310-6273-11e3-9fbc-12313d2f7cdc
Transfer-Encoding: chunked
Connection: keep-alive
```

> And a response body like so:

```json
{
	"results": [
		{
			"timestamp": 1369832019085,
			"value": {
				"msg": "hello world, again"
			}
		},
		{
			"timestamp": 1369832019080,
			"value": {
				"msg": "hello world"
			}
		}
	],
	"count": 2
}
```

`GET https://api.orchestrate.io/v0/$collection/$key/events/$type?start=$start&end=$end`

### Parameters

Parameter  | Description
---------- | -----------
collection | the collection from which to get the events.
key        | the primary key associated with the events.
type       | the category for an event, e.g. "update" or "tweet" etc.
start      | the inclusive start of a time range to query. (optional)
end        | the exclusive end of a time range to query. (optional)

<aside class="notice">
The start and end values are integers representing milliseconds since the Unix epoch.
</aside>

## Put

> Make sure to replace all the variables with the appropriate values.

```shell
curl -i "https://api.orchestrate.io/v0/$collection/$key/events/$type?timestamp=$timestamp" \
	-XPUT \
	-H "Content-Type: application/json" \
	-u "$api_key:" \
	-d "{\"msg\":\"hello\"}"
```

```java
MyObject domainObject = new MyObject(...);
EventStoreOperation eventStoreOp =
        new EventStoreOperation("collection", "key", "type", domainObject);
Future<Boolean> future = client.execute(eventStoreOp);
Boolean result = future.get(3, TimeUnit.SECONDS);
if (result) {
	System.out.println("Successfully stored the event.");
}
```

```go
err := c.PutEvent(collection, key, typ, strings.NewReader(`{"msg":"hello"}`))
```

Puts an event with an optional user defined timestamp.

### HTTP Request

> Returns response headers like so:

```http
HTTP/1.1 204 No Content
Content-Type: application/json
Date: Tue, 19 Nov 2013 13:51:54 GMT
X-ORCHESTRATE-REQ-ID: bfc4e750-5121-11e3-be8f-22000ab58c12
Connection: keep-alive
```

```PUT /v0/$collection/$key/events/$type```

### Parameters

Parameter  | Description
---------- | -----------
collection | the collection to which to put the event.
key        | the primary key associated with the event.
type       | the category for an event, e.g. "update" or "tweet" etc.
timestamp  | the timestamp to associate with the event.

<aside class="notice">
The timestamp value should be an integer representing millisecond since the Unix epoch.
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
RelationFetchOperation<MyObject> relationFetchOp =
        new RelationFetchOperation("collection", "key", "kind1", "kind2");
Future<Iterable<KvObject<String>>> future = client.execute(relationFetchOp);
Iterable<KvObject<String>> relatedObjects = futureResult.get();
for (KvObject<String> relatedObject : relatedObjects) {
	System.out.println(relatedObject.getValue());
}
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
RelationStoreOperation relationStoreOp = new RelationStoreOperation(
        "sourceCollection", "sourceKey", "kind", "toCollection", "toKey");
Future<Boolean> future = client.execute(relationStoreOp);
Boolean result = futureResult.get(3, TimeUnit.SECONDS);
if (result) {
	System.out.println("Successfully stored the relation.");
}
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
kind       | the category for an event, e.g. "update" or "tweet" etc.
toCollection | the collection to which the relation goes.
toKey      | the key to which the relation goes.

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
