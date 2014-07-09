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

TODO

## API Reference

### Client(api_key, custom_url=None, **options)
### Client.get(collection, key, ref=None)
### Client.post(collection, item)
### Client.put(collection, key, item, ref=None)
### Client.delete(collection, key=None, ref=None)
### Client.refs(collection, key, **params)
### Client.list(collection, **params)
### Client.search(collection, query, **params)
### Client.get_relations(collection, key, *relations)
### Client.put_relation(collection, key, relation, to_collection, to_key)
### Client.delete_relation(collection, key, relation, to_collection, to_key)
### Client.get_event(collection, key, event_type, timestamp, ordinal)
### Client.post_event(collection, key, event_type, data, timestamp=None)
### Client.put_event(collection, key, event_type, timestamp, ordinal, data, ref=None)
### Client.delete_event(collection, key, event_type, timestamp, ordinal, ref=None)
### Client.list_events(collection, key, event_type, **params)
### Client.async()

### Pages
### Pages.next(querydict={}, **headers)
### Pages.prev(querydict={}, **headers)
### Pages.reset()
### Pages.all()

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
