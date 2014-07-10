# Porc

[![Build Status](https://travis-ci.org/orchestrate-io/porc.svg?branch=master)](https://travis-ci.org/orchestrate-io/porc)
[![Coverage Status](https://coveralls.io/repos/orchestrate-io/porc/badge.png?branch=master)](https://coveralls.io/r/orchestrate-io/porc?branch=master)
[![PyPI version](https://badge.fury.io/py/porc.svg)](http://badge.fury.io/py/porc)
[![PyPi downloads](https://pypip.in/d/porc/badge.png)](https://crate.io/packages/porc/)

An effortless, asynchronous Python client for [orchestrate.io][].

## Install

    pip install porc

Don't have [pip][]? [Get it!](http://pip.readthedocs.org/en/latest/installing.html) It's neat :D


## Usage

Let's dive right in:

```python
from porc import Client

client = Client(YOUR_API_KEY)

# make sure our API key works
client.ping().raise_for_status()

# get and update an item
item = client.get(COLLECTION, KEY)
item['was_modified'] = True
client.put(item.collection, item.key, item.json, item.ref).raise_for_status()

pages = client.list(COLLECTION)
responses = pages.all()
print len(responses)
# prints number of pages in collection

# asynchronously get two items
with client.async() as c:
    futures = []
    futures.append(c.get(COLLECTION, KEY_1))
    futures.append(c.get(COLLECTION, KEY_2))
    responses = [future.result() for future in futures]
    [response.raise_for_status() for response in responses]

# iterate through search results
pages = client.search(COLLECTION, QUERY)
for page in pages:
    print page.status_code
    # prints 200
    print page['count']
    # prints number of items returned by page

# get every item in a collection
items = client.list(COLLECTION).all()
print len(items)
# prints number of items in collection
```

## Table of Contents

* [Client(api_key, custom_url=None, **options)](#client)
* [Client.get(collection, key, ref=None)](#clientget)
* [Client.post(collection, item)](#clientpost)
* [Client.put(collection, key, item, ref=None)](#clientput)
* [Client.delete(collection, key=None, ref=None)](#clientdelete)
* [Client.refs(collection, key, **params)](#clientrefs)
* [Client.list(collection, **params)](#clientlist)
* [Client.search(collection, query, **params)](#clientsearch)
* [Client.get_relations(collection, key, *relations)](#clientget_relations)
* [Client.put_relation(collection, key, relation, to_collection, to_key)](#clientput_relation)
* [Client.delete_relation(collection, key, relation, to_collection, to_key)](#clientdelete_relation)
* [Client.get_event(collection, key, event_type, timestamp, ordinal)](#clientget_event)
* [Client.post_event(collection, key, event_type, data, timestamp=None)](#clientpost_event)
* [Client.put_event(collection, key, event_type, timestamp, ordinal, data, ref=None)](#clientput_event)
* [Client.delete_event(collection, key, event_type, timestamp, ordinal, ref=None)](#clientdelete_event)
* [Client.list_events(collection, key, event_type, **params)](#clientlist_events)
* [Client.async()](#clientasync)
* [Pages](#page)
* [Pages.next(querydict={}, **headers)](#pagesnext)
* [Pages.prev(querydict={}, **headers)](#pagesprev)
* [Pages.reset()](#pagesreset)
* [Pages.all()](#pagesall)
* [Response](#response)

## API Reference

### Client

```python
from porc import Client

client = Client(API_KEY)
```

The thing you'll use to make requests. It's the only object you'll need to invoke directly.

By default, the client makes requests to <https://api.orchestrate.io/v0>. If you need to make requests against a different URL, you can pass it as an argument to the constructor:

```python
client = Client(API_KEY, "https://your_domain.com")
```

By default, the client makes synchronous requests. To make asynchronous requests, see [Client.async](#clientasync).

### Client.get

```python
item = client.get('a_collection', 'a_key')
# make sure the request succeeded
item.raise_for_status()
# prints your item's ref value
print item.ref
# prints your item's fields and values as a dict
print item.json
# prints a given field from the item's json
print item[FIELD]
```

Returns the item associated with a given key from a given collection.
The optional `ref` argument can retrieve a specific version of an item, like so:

```python
item = client.get('a_collection', 'a_key', 'a_ref')
```

This method returns a [Response](#response) object.

### Client.post

```python
response = client.post('a_collection', {
  "derp": True
})
# make sure the request succeeded
response.raise_for_status()
# prints the item's generated key
print response.key
# prints the item version's ref
print response.ref
```

Inserts an item into a collection, allowing the server to generate a key for it.

This method returns a [Response](#response) object.

### Client.put

```python
response = client.put('a_collection', 'a_key', {
  "derp": True
})
# make sure the request succeeded
response.raise_for_status()
# prints the item's key
print response.key
# prints the item version's ref
print response.ref
```

Inserts an item into a collection at a given key, or updates the value previously at that key.

The optional `ref` argument can be used to perform conditional updates.
To update only if your `ref` matches the latest version's, provide it to the method:

```python
response = client.put('a_collection', 'a_key', {
  "derp": True
}, 'a_ref')
```

To insert only if there is no item associated with a key, provide `False` instead:

```python
response = client.put('a_collection', 'a_key', {
  "derp": True
}, False)
```

This method returns a [Response](#response) object.

### Client.delete

```python
# delete an item version
client.delete('a_collection', 'a_key', 'a_ref')
# delete an item and all its versions
client.delete('a_collection', 'a_key')
# delete a collection and all its items
client.delete('a_collection')
```

Deletes a collection, item, or item version, depending on how many arguments you provide.

This method returns a [Response](#response) object.

### Client.refs

```python
refs = client.refs('a_collection', 'a_key')
# make sure the request succeeded
refs.raise_for_status()
# prints the number of versions for this item
print refs['count']
# prints every item version as a list of dicts
print refs['results']
```

Lists every version of an item.

To control which versions are passed back, you can use these keyword arguments:

* limit: the number of results to return. (default: 10, max: 100)
* offset: the starting position of the results. (default: 0)
* values: whether to return the value for each ref in the history. (default: false)

```python
refs = client.refs('a_collection', 'a_key', limit=5, values=True, offset=10)
```

This method returns a [Response](#response) object.

### Client.list

```python
pages = client.list('a_collection')
# get the first page of items in the collection
page = pages.next()
# ensure the request succeeded
page.raise_for_status()
# get all items in the collection
items = pages.all()
# print all items in the collection
print items['results']
# iterate over the pages of items in the collection
for
```

### Client.search
### Client.get_relations
### Client.put_relation
### Client.delete_relation
### Client.get_event
### Client.post_event
### Client.put_event
### Client.delete_event
### Client.list_events
### Client.async
### Pages
### Pages.next
### Pages.prev
### Pages.reset
### Pages.all
### Response

## Tests

To run tests, get the source code and use `setup.py`:

    git clone git@github.com:orchestrate-io/porc.git
    cd porc
    python setup.py test

## License

[MIT][], yo.

[orchestrate.io]: http://orchestrate.io/
[pip]: https://pypi.python.org/pypi/pip
[MIT]: http://opensource.org/licenses/MIT
