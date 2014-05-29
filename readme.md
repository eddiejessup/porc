# Porc

An effortless, asynchronous Python client for [orchestrate.io][].

## Install

    pip install porc

Don't have [pip][]? [Get it!](http://pip.readthedocs.org/en/latest/installing.html) It's neat :D

## Usage

Let's create an authenticated client, which we'll use to make requests:

    from porc import Client

    YOUR_API_KEY = '...'
    client = Client(YOUR_API_KEY)

By default, porc makes asynchronous requests. To make synchronous requests instead, initialize your client with `async=False`, like this:

    client = Client(YOUR_API_KEY, async=False)

Synchronous requests, rather than returning futures, will block until they complete, before returning the same response objects as resolved promises.

Now then, how's about we create a key, yeah?

    collection = client.collection('newcollection')
    key = collection.key('derp')
    future = key.put({"hello": "world"})
    response = future.result()
    print response.status_code
    # 201

The synchronous equivalent:

    collection = client.collection('newcollection')
    key = collection.key('derp')
    response = key.put({"hello": "world"})
    print response.status_code
    # 201

## Features

### Get some REST

As much as possible, porc is a convenience layer to orchestrate's RESTful API, handling authentication, headers, inheritance, URLs, etc. so you can focus on moving data and building apps.

Just like the API, porc presents objects in a hierarchy of resources, like so:

    client = Client(API_KEY)
    collection = client.collection(COLLECTION_NAME)
    key = collection.key(KEY_NAME)
    ref = key.ref(REF_NAME)

Each resource, then, can execute methods corresponding to HTTP verbs, like so:

    future = ref.get()

...which is analogous to `GET https://API_KEY:@api.orchestrate.io/v0/COLLECTION_NAME/KEY_NAME/refs/REF_NAME`. The name of the collection, key, etc., are inherited from the resource's ancestors, along with any other options. 

If you're feeling sassy, you can do it all in one line:

    future = Client(API_KEY).collection(COLLECTION_NAME).key(KEY_NAME).ref(REF_NAME).get()

Here's the hierarchy flattened out:

    client
      collection
        list
        search
        key
          ref
          event
          relation

For more details, see porc's [API Reference][api-reference].

### Make a Request

Under the hood, porc leverages [requests-futures](https://github.com/ross/requests-futures) to deliver asynchronous execution. It works like this:

    client = porc.Client(API_KEY)
    future = client.ping()
    response = future.result()

That `response` object is just a [response object](http://docs.python-requests.org/en/latest/api/#requests.Response) from [Python Requests](http://docs.python-requests.org/en/latest/).

To disable asynchronous execution, initialize your client with `async=False`:

    client = porc.Client(API_KEY, async=False)
    response = client.ping()

Synchronous requests will block code execution until they complete.

### Saving URL Parameters

For your convenience and sanity, URL parameters like the current collection are attached to each object under the `path` attribute. For example:

    client = Client(API_KEY)
    collection = client.collection('hello')
    key = collection.key('world')
    print key.path
    # {"collection": "hello", "key": "world"}

The same is done for responses, specifically for values contained in headers like refs and ordinals, like so:

    future = ref.get()
    response = future.result()
    print response.path
    # {"collection": "hello", "key": "world", "ref": "cbb48f9464612f20"}

### Auto-quoting Headers

Headers like `If-Match` need to have their values wrapped in quotes, which can be a pain, so porc can do it for you. For example:

    ref = 'cbb48f9464612f20'
    future = self.key.put(dict(goodbye='world'), **{"If-Match": ref})
    # in the response, the `If-Match` value becomes `"cbb48f9464612f20"` 
    # rather than just `cbb48f9464612f20`
    response = future.result()
    print response.status_code
    # 201

If you wrap the value in quotes on your own, porc will leave it alone.

## API Reference

Annotated source code, thanks to [slate](https://github.com/tripit/slate), available [here][api-reference].

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
[api-reference]: http://orchestrate-io.github.io/porc/