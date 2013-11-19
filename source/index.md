---
title: Orchestrate.io 	API Reference

language_tabs:
  - shell: curl
  - go

toc_footers:
 - <a href='https://dashboard.orchestrate.io'>Dashboard</a>
---

# API Version

```
/v0/:collection/:key
```

The current version of the Orchestrate API is v0. All URLs will start with the current API version.

# Request Headers

```shell
# With GETs a Accepts header must be set
curl "api_endpoint_here" \
	-u "$api_key:" \
	-H "Accepts: */*""

# With PUTs a Content-Type header must be set
curl -XPUT "api_endpoint_here" \
	-u "$api_key:" \
	-H "Content-Type: application/json" \
	-d '$json'
```

Clients must use request headers accordingly:

* All `GET` requests must accept the `Content-Type` as `application/json` or `*/*`.
* All `PUT` requests are expected to set the `Content-Type` header to `application/json`.

# Authentication

> Make sure to replace `$api_key` with your API key.

```go
// Create a new Orchestrate.io client with your API key
c := client.NewClient("$api_key")
```

```shell
# With curl, pass in your API key as the basic auth username and no password
curl "api_endpoint_here" \
	-u "$api_key:"
```

Orchestrate.io uses HTTP Basic Authentication over SSL. Authenticate with an API key as the username and no password.

# Keys

## Get

> Make sure to replace `$collection` and `$key` with the appropriate collection and key.

```shell
curl -i "https://api.orchestrate.io/v0/$collection/$key" \
	-u "$api_key:"
```

```go
domain_object := new(DomainObject)
err := c.Get("$collection", "$key", domain_object)
```

Returns value with content-location (ref) header.

### HTTP Request

> The returns a response headers like so:

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

### Query Parameters

Parameter  | Description
---------- | -----------
collection | the collection to query.
key        | the primary key for a value.

## Put

> Make sure to replace `$collection` and `$key` with the appropriate collection and key.

```shell
curl -i "https://api.orchestrate.io/v0/$collection/$key" \
	-XPUT \
	-H "Content-Type: application/json' -d'$json" \
	-u "$api_key:" \
	-d '$json'
```

```go
err := c.Put("$collection", "$key", domain_object)
```

Stores a value for key, returning the location (ref) header.

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

### Request Headers

Conditional headers can be used to specify a pre-condition that determines whether the store operation happens. The _If-Match_ header specifies that the store operation will succeed if and only if the _ref_ value matches current stored _ref_. The _If-None-Match_ header specifies that the store operation will succeed if and only if the key doesn't already exist. 

Header        | Description
------------- | -----------
If-Match      | Stores the value for the key if the value for this header matches the current `ref` value.
If-None-Match | Stores the value for the key if no key/value already exists, the only valid value for this header is `*`.

_If-Match_ and _If-None-Match_ headers cannot be supplied together.

### Query Parameters

Parameter  | Description
---------- | -----------
collection | the collection to query.
key        | the primary key for a value.

## Delete

> Make sure to replace `$collection` and `$key` with the appropriate collection and key.

```shell
curl -i "https://api.orchestrate.io/v0/$collection/$key" \
	-XDELETE \
	-u "$api_key:" \
	-H'Content-Type: application/json' -d'$json'
```

```go
err := c.Delete("$collection", "$key")
```

Deletes the value for a key.

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

### Query Parameters

Parameter  | Description
---------- | -----------
collection | the collection to query.
key        | the primary key for a value.

# Refs

## Get

> Make sure to replace the variables with the appropriate values.

```shell
curl -i "https://api.orchestrate.io/v0/$collection/$key/refs/$ref" \
	-u "$api_key:"
```

Returns value.

### HTTP Request

> The returns a response headers like so:

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

### Query Parameters

Parameter  | Description
---------- | -----------
collection | the collection to query.
key        | the primary key for a value.
ref        | an opaque identifier for a value.

# Collections

## Delete

> Make sure to replace `$collection` with the appropriate collection.

```shell
curl -i "https://api.orchestrate.io/v0/$collection?force=true" \
	-XDELETE \
	-u "$api_key:" \
```

Deletes an entire collection.

Delete operations cannot be undone, as a result, to avoid accidental deletions when experimenting with the API the query parameter `force=true` is necessary.

> Example response headers 

```http
HTTP/1.1 204 No Content
Content-Type: application/json
Date: Thu, 24 Oct 2013 15:20:42 GMT
X-ORCHESTRATE-REQ-ID: d88d0ef1-3cbf-11e3-be54-22000ae8057a
Connection: keep-alive
```

### Query Parameters

Parameter  | Description
---------- | -----------
collection | the collection to query.

# Search

## Collection

```shell
curl -i "https://api.orchestrate.io/v0/$collection?query=$query&limit=$limit&offset=$offset" \
	-XDELETE \
	-u "$api_key:" \
	-H'Content-Type: application/json' -d'$json'
```

```go
results, err := c.Search("$collection", "$query")
```

Returns list of collection, key, ref, and values.

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

`GET https://api.orchestrate.io/v0/$collection/$key`

### Parameters

Parameter  | Description
---------- | -----------
collection | the collection to query.
query      | a [Lucene](http://lucene.apache.org/core/4_3_0/queryparser/org/apache/lucene/queryparser/classic/package-summary.html#Overview) query string.
limit      | the number of results to return. (default: 10, max: 100)
offset     | the starting position of the results. (default: 0)

# Events

## Get

> Make sure to replace all the parameters with the appropriate values.

```shell
curl -i "https://api.orchestrate.io/v0/$collection/$key/events/$type?start=$start&end=$end" \
	-u "$api_key:"
```

```go
events, err := c.GetEvents("$collection", "$key", "$type")
```

Returns a list of events, optionally limited to specified time range.

### HTTP Request

> Returns response headers like so:

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Connection: Keep-Alive
Content-Length: 81
```

> And a response body like so:

```json
{
	"results": [
		{
			"timestamp": 1369832019085,
			"value": {
				"msg": "hello world"
			}
		}
	],
	"count": 1
}
```

### Query Parameters

Parameter  | Description
---------- | -----------
collection | the collection to query.
key        | the primary key for a value.
type       | the category for an event, e.g. "update" or "tweet" etc.
start      | the inclusive start of a time range to query. (optional)
end        | the exclusive end of a time range to query. (optional)

## Put

> Make sure to replace all the parameters with the appropriate values.

```shell
curl -i "https://api.orchestrate.io/v0/$collection/$key/events/$type?timestamp=$timestamp" \
	-XPUT \
	-H 'Content-Type: application/json' \
	-u "$api_key:" \
	-d '{"msg":"hello"}'
```

```go
err := c.PutEvent("$collection", "$key", "$type", strings.NewReader(`{"msg":"hello"}`))
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

### Query Parameters

Parameter  | Description
---------- | -----------
collection | the collection to query.
key        | the primary key for a value.
kind       | the category for an event, e.g. "update" or "tweet" etc.
timestamp  | the timestamp to associate with the event.

# Graph

## Get

> Make sure to replace all the parameters with the appropriate values.

```shell
# One hop
curl -i "https://api.orchestrate.io/v0/$collection/$key/relations/$kind" \
	-u "$api_key:"

# Two hops
curl -i "https://api.orchestrate.io/v0/$collection/$key/relations/$kind1/$kind2" \
	-u "$api_key:"
```

```go
// One hop
results, err := c.GetRelations("$collection", "$key", []string{"$kind"})

// Two hops
results, err := c.GetRelations("$collection", "$key", []string{"$kind1", "kind2"})
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

```GET /v0/$collection/$key/relation/$kind1/$kind2 ...```

### Query Parameters

Parameter  | Description
---------- | -----------
collection | the collection to query.
key        | the primary key for a value.
kind       | the relationship kind to query, e.g. "follows" or "friend" etc.

## Put

> Make sure to replace all the parameters with the appropriate values.

```shell
curl -i "https://api.orchestrate.io/v0/$collection/$key/relation/$kind/$toCollection/$toKey" \
	-XPUT \
	-u "$api_key:" \
```

```go
err := c.PutRelation("$collection", "$key", "$kind", "$toCollection", "toKey")
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

```PUT /v0/$collection/$key/relation/$kind/$toCollection/$fromCollection```

### Query Parameters

Parameter  | Description
---------- | -----------
collection | the collection from which the relationship originates.
key        | the key from which the relationship originates.
kind       | the category for an event, e.g. "update" or "tweet" etc.
toCollection | the collection to which the relationship goes.
toKey      | the key to which the relationship goes.

# Errors

Orchestrate.io uses the following error codes:

Code | Identifier | Meaning
-----| ---------- | -------
400 | API_BAD_REQUEST | The API request is malformed
500 | SECURITY_AUTHENTICATION | An error occurred while trying to authenticate
401 | SECURITY_UNAUTHORIZED | Valid credentials are required
400 | SEARCH_PARAM_INVALID | A provided search query param is invalid.
500 | SEARCH_INDEX_NOT_FOUND | Index could not be queried for this application
500 | INTERNAL_ERROR | Internal Error
404 | ITEMS_NOT_FOUND | The requested items could not be found
412 | ITEM_VERSION_MISMATCH | The version of the item does not match
412 | ITEM_ALREADY_PRESENT | The item is already present
400 | ITEM_REF_MALFORMED | The provided Item Ref is malformed
409 | INDEXING_CONFLICT | The item has been stored but conflicts were detected when indexing. Conflicting fields have not been indexed.
