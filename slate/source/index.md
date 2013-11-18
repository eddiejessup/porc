---
title: API Reference

language_tabs:
  - shell
  - go

toc_footers:
 - <a href='#'>Sign Up for a Developer Key</a>
 - <a href='http://github.com/tripit/slate'>Documentation Powered by Slate</a>
---

# Version

```
/v0/:collection/:key
```

The current version of the Orchestrate API is v0. All URLs will start with the current API version.

# Request Headers

```shell
# With GETs a Accepts header must be set
curl "api_endpoint_here" -u "$api_key:" -H'Accepts: */*'

# With PUTs a Content-Type header must be set
curl -XPUT "api_endpoint_here" -u "$api_key:" -H'Content-Type: application/json' -d'$json'
```

Clients must use request headers accordingly:

* All `GET` requests must accept the `Content-Type` as `application/json` or `*/*`.
* All `PUT` requests are expected to set the `Content-Type` header to `application/json`.

# Authentication

```go
// Create a new Orchestrate.io client with your API key
c := client.NewClient("$api_key")
```

```shell
# With curl, pass in your API key as the basic auth username and no password
curl "api_endpoint_here"
	-u "$api_key:"
```

> Make sure to replace `$api_key` with your API key.

Orchestrate.io uses HTTP Basic Authentication over SSL. Authenticate with an API key as the username and no password.

# Keys

## Get

```shell
curl -i "https://api.orchestrate.io/v0/$collection/$key"
	-u "$api_key:"
```

```go
err := c.Get("$collection", "$key", domain_object);
```

> Make sure to replace `$collection` with your API key.

Returns value with content-location (ref) header.

### HTTP Request

`GET https://api.orchestrate.io/v0/$collection/$key`

> The above request returns a response headers like so:

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

### Query Parameters

Parameter  | Description
---------- | -----------
collection | the collection to query.
key        | the key assigned to a value stored in the specified collection.


## Put

```shell
curl -i "https://api.orchestrate.io/v0/$collection/$key"
	-XPUT
	-u "$api_key:"
	-H'Content-Type: application/json' -d'$json'
```

```go
err := c.Put("$collection", "$key", domain_object);
```

Stores a value for key, returning the location (ref) header.

### Headers

Conditional headers can be used to specify a pre-condition that determines whether the store operation happens. The _If-Match_ header specifies that the store operation will succeed if and only if the _ref_ value matches current stored _ref_. The _If-None-Match_ header specifies that the store operation will succeed if and only if the key doesn't already exist. 

Header        | Description
------------- | -----------
If-Match      | Stores the value for the key if the value for this header matches the current `ref` value.
If-None-Match | Stores the value for the key if no key/value already exists, the only valid value for this header is `*`.

_If-Match_ and _If-None-Match_ headers cannot be supplied together.

### HTTP Request

`PUT https://api.orchestrate.io/v0/$collection/$key`

### Query Parameters

Parameter  | Description
---------- | -----------
collection | the collection to query.
key        | the key assigned to a value stored in the specified collection.


# Errors

The Kittn API uses the following error codes:


Error Code | Meaning
---------- | -------
400 | Bad Request -- Your request sucks
401 | Unauthorized -- Your API key is wrong
403 | Forbidden -- The kitten requested is hidden for administrators only
404 | Not Found -- The specified kitten could not be found
405 | Method Not Allowed -- You tried to access a kitten with an invalid method
406 | Not Acceptable -- You requested a format that isn't json
410 | Gone -- The kitten requested has been removed from our servers
418 | I'm a teapot
429 | Too Many Requests -- You're requesting too many kittens! Slown down!
500 | Internal Server Error -- We had a problem with our server. Try again later.
503 | Service Unavailable -- We're temporarially offline for maintanance. Please try again later.