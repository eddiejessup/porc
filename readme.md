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
    # prints number of records returned by page
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
### Client.get
### Client.post
### Client.put
### Client.delete
### Client.refs
### Client.list
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
### Pages]
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
