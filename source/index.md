---
title: Porc API Reference

language_tabs:
  - python

toc_footers:
  - <a href='#'>Porc Source</a>
  - <a href='http://github.com/tripit/slate'>Documentation Powered by Slate</a>
  - <a href="http://orchestrate.io/docs/api/">Orchestrate Documentation</a>

---

# Porc

The effortless, asynchronous Python client for [orchestrate.io](http://orchestrate.io/).


# | Resource


```python
    def __init__(self, uri, **kwargs):
        self.uri = uri

        # if given an existing session, use it
        if kwargs.get('session'):
            self._session = kwargs['session']
            del kwargs['session']
        # set the resource's session as either sync or async
        # according to keyword arguments
        elif kwargs.get('async') == False:
            self._session = requests.Session()
            del kwargs['async']
        # default to async
        else:
            self._session = FuturesSession()

        # set path parameters according to given url
        self._set_path()

        # pass remaining kwargs as defaults to requests
        self._set_options(**kwargs)

```



Ancestor for all Orchestrate resources.
Handles storing URL state, headers, sessions, etc.

If you create an object, like a `Client`, then use that to
create a `Collection` object, the `Collection` will inherit any options
from the `Client` object, such as auth settings.

Likewise, all objects inheriting from Resource can make HTTP requests
using the methods `head`, `get`, `put`, `post`, and `delete`,
even if Orchestrate would only return a `405 Method Not Allowed`
for a given method.




## get


```python
    def get(self, querydict={}, **headers):
        
        return self._make_request('get', querydict, **headers)

```



Make a GET request against the object's URI.
`querydict` is a mapping object, like a dict, 
that is serialized into the querystring.
Any keyword arguments are passed along as headers.




## head


```python
    def head(self, querydict={}, **headers):
        
        return self._make_request('head', querydict, **headers)

```



Make a HEAD request against the object's URI.
`querydict` is a mapping object, like a dict, 
that is serialized into the querystring.
Any keyword arguments are passed along as headers.




## put


```python
    def put(self, body={}, **headers):
        
        return self._make_request('put', body, **headers)

```



Make a PUT request against the object's URI.
`querydict` is a mapping object, like a dict, 
that is serialized into the querystring.
Any keyword arguments are passed along as headers.




## post


```python
    def post(self, body={}, **headers):
        
        return self._make_request('post', body, **headers)

```



Make a POST request against the object's URI.
`querydict` is a mapping object, like a dict, 
that is serialized into the querystring.
Any keyword arguments are passed along as headers.




## delete


```python
    def delete(self, querydict={}, **headers):
        
        return self._make_request('delete', querydict, **headers)

```



Make a DELETE request against the object's URI.
`querydict` is a mapping object, like a dict, 
that is serialized into the querystring.
Any keyword arguments are passed along as headers.





# | Client


```python
    def __init__(self, api_key, api_version=0, **kwargs):
        uri = 'https://%s:@api.orchestrate.io/v%d' % (api_key, api_version)
        super(Client, self).__init__(uri, **kwargs)

```



The top-level resource for interacting with Orchestrate.
Handles authentication, spawns collections.

```
client = porc.Client(API_KEY)
client.ping().result().raise_for_status()
# if it throws an error, you're not authenticated
```




## ping


```python
    def ping(self):
        
        return self.head()

```



Sends Orchestrate a HEAD request to determine
connectivity and authentication.




## collection


```python
    def collection(self, name, **kwargs):
        
        return self._init_child(collection.Collection, name, **kwargs)

```



Spawns a collection object, inheriting options from the client object.
Note that this does not create a collection in Orchestrate.





# | Collection




From the Orchestrate docs:

"Collections are groupings of the JSON objects. 
Collections are analogous to tables in a relational database."

The collection object performs searches over the JSON objects stored in a collection, 
and can spawn key objects representing JSON objects.

```python
collection = porc.Client(API_KEY).collection(NAME)
for page in collection.search({"query": "cool_*"}):
    print page.json()
    # {
    #     "count": 1,
    #     "next": "/v0/collection?limit=10&query=test&offset=1",
    #     "prev": "/v0/collection?limit=10&query=test&offset=0",
    #     "results": [
    #         {
    #             "path": {
    #                 "collection": "neat_stuff",
    #                 "key": "cool_beans",
    #                 "ref": "20c14e8965d6cbb0"
    #             },
    #             "score": 1.0,
    #             "value": {
    #                 "coolness": 999
    #             }
    #         }
    #     ],
    #     "total_count": 100
    # }
```




## search


```python
    def search(self, **kwargs):
        
        return self.list(**kwargs)

```



Returns a page object to page through search results.

Alias to `self.list`.




## key


```python
    def key(self, name, **kwargs):
        
        return self._init_child(key.Key, name, **kwargs)

```



Spawns a key object, inheriting options from the collection object.
Note that this does not create a key in Orchestrate.




## delete


```python
    def delete(self, querydict={}, **headers):
        
        querydict['force'] = True
        return super(Collection, self).delete(querydict, **headers)

```



Deletes a collection and all the keys it contains.
Automatically sets `?force=true` in the querystring.




## list


```python
    def list(self, **kwargs):
        
        return page.Page(self.uri, kwargs, session=self._session, **self.opts)

```



Returns a page object to page through list results.





# | Page


```python
    def __init__(self, uri, querydict={}, **kwargs):
        opts = dict(kwargs, params=querydict)
        # if async, create a callback that stores current page state after each request
        if 'session' in kwargs and type(kwargs['session']) == FuturesSession:
            opts['background_callback'] = self._handle_res
        super(Page, self).__init__(uri, **opts)
        self._url_root = self.uri[:self.uri.find('/v0')]
        self.response = None

```



Class used for paging through search results.

Can be used as an iterator, ex: `for page in Page`,
or by using the methods `next` and `prev` explicitly
to page through results.

Used in searching collections and events.




## reset


```python
    def reset(self):
        
        self.response = None

```



Clear the page's current place.

    page_1 = page.next().result()
    page_2 = page.next().result()
    page.reset()
    page_x = page.next().result()
    assert page_x.url == page_1.url




## next


```python
    def next(self, querydict={}, **headers):
        
        return self._handle_page(querydict, **headers)

```



Gets the next page of results.
Raises `StopIteration` when there are no more results.




## prev


```python
    def prev(self, querydict={}, **headers):
        
        return self._handle_page(querydict, 'prev', **headers)        

```



Gets the previous page of results.
Raises `StopIteration` when there are no more results.

Note: Only collection searches provide a `prev` value.
For all others, `prev` will always return `StopIteration`.





# | Key




From the Orchestrate docs:

"Key/Value is core to Orchestrate.io. 
All other query types are built around this data type. 
Key/Value pairs are pieces of data
identified by a unique key for a collection
and have corresponding value."

The key object represents a single key/value in Orchestrate,
and provides methods for working with refs, events, and relations,
as well as creating, reading, updating, and destroying key/values.

```python
key = collection.key(NAME)
# create
response = key.put({"hello": "world"}).result()
response.raise_for_status()
# create a ref to work with this version of the key/value
ref_value = response.path['ref']
ref = key.ref(ref_value)
# read
response = key.get().result()
print response.json()
# {"hello": "world"}
# update
response = key.put({"goodnight": "moon"}, **{"If-Match": ref_value}).result()
response.raise_for_status()
ref_value = response.path['ref']
# delete
response = key.delete(**{"If-Match": ref_value}).result()
response.raise_for_status()
```




## relation


```python
    def relation(self, **kwargs):
        
        return self._init_child(Relation, **kwargs)

```



Returns an object for creating and querying relations.
See `Relation` for more info.




## graph


```python
    def graph(self, **kwargs):
        
        return self.relation(**kwargs)

```



Alias to `relation`




## ref


```python
    def ref(self, name, **kwargs):
        
        return self._init_child(Ref, 'refs', name, **kwargs)

```



Returns an object for dealing with a given Ref value.
See `Ref` for more info.




## event


```python
    def event(self, event_type, **kwargs):
        
        return self._init_child(Event, 'events', event_type, **kwargs)

```



Returns an object for creating and querying events.
See `Event` for more info.





# | Ref




From the Orchestrate docs:

"Refs are used to identify specific immutable values that have been assigned to keys."

Ref objects allow you to work with specific versions of a doc,
particularly past versions.

```python
ref = key.ref(ref_value)
response = ref.get().result()
print response.json()
# {"hello": "world"}
```





# | Event




From the Orchestrate docs:

"Events are a way to associate time-ordered data with a key."

The event object allows you to create, read, update, and delete
different events, and to perform queries over events associated
with a key.

```python
event = key.event(TYPE)
# create
response = event.post({"msg": "hello world, again"}).result()
timestamp = response.path['timestamp']
ordinal = response.path['ordinal']
response.raise_for_status()
# read
response = event.get(timestamp, ordinal).result()
response.raise_for_status()
print response.json()
# {
#     "path": {
#         "collection": "asdf",
#         "key": "key",
#         "ref": "ae3dfa4325abe21e",
#         "type": "played",
#         "timestamp": 1369832019085,
#         "ordinal": 9
#     },
#     "value": {
#       "msg": "hello world, again"
#     },
#     "timestamp": 1369832019085,
#     "ordinal": 9
# }
# update
response = event.put(timestamp, ordinal, {"msg": "goodnight moon"}).result()
response.raise_for_status()
# query
for page in event.list():
    print page.json()
    # {
    #   "results": [
    #     {
    #       "path": {
    #         "collection": "collection",
    #         "key": "key",
    #         "type": "type",
    #         "timestamp": 1369832019085,
    #         "ordinal": 9,
    #         "ref": "ae3dfa4325abe21e"
    #       },
    #       "value": {
    #         "msg": "goodnight moon"
    #       },
    #       "timestamp": 1369832019085,
    #       "ordinal": 9
    #     }
    #   "count": 1
    # }
# delete
response = event.delete(timestamp, ordinal).result()
response.raise_for_status()
```




## get


```python
    def get(self, timestamp=None, ordinal=None, querydict={}, **headers):
        
        if not timestamp and not ordinal:
            return self.list(querydict, **headers)
        else:
            if type(timestamp) == datetime:
                timestamp = create_timestamp(timestamp)
            resource = self._init_child(Resource, str(timestamp), ordinal)
            return resource.get(**headers)

```



Retrieves a given event. 
If timestamp is a datetime object, 
it will be converted to milliseconds since epoch.




## put


```python
    def put(self, timestamp, ordinal, body, **headers):
        
        if type(timestamp) == datetime:
            timestamp = create_timestamp(timestamp)
        resource = self._init_child(Resource, str(timestamp), ordinal)
        return resource.put(body, **headers)

```



Updates a given event.
If timestamp is a datetime object, 
it will be converted to milliseconds since epoch.




## post


```python
    def post(self, body, timestamp=None, **headers):
        
        if timestamp:
            if type(timestamp) == datetime:
                timestamp = create_timestamp(timestamp)
            resource = self._init_child(Resource, str(timestamp))
        else:
            resource = self._init_child(Resource)

        return resource.post(body, **headers)

```



Creates a new event.
If timestamp is not provided, Orchestrate will give it one.




## list


```python
    def list(self, querydict, **headers):
        
        return Page(self.uri, querydict, session=self._session, headers=headers)

```



Returns a page representing a given query of events.
See `Page` for more details on the page object.




## delete


```python
    def delete(self, timestamp, ordinal, querydict={}, **headers):
        
        if type(timestamp) == datetime:
            timestamp = create_timestamp(timestamp)
        resource = self._init_child(Resource, str(timestamp), ordinal)
        querydict['purge'] = True
        return resource.delete(querydict, **headers)

```



Deletes a given event.
Automatically sets `?purge=true` in the querystring.





# | Relation


```python
    def __init__(self, uri, **kwargs):
        self._root_url = uri
        super(Relation, self).__init__(uri, **kwargs)

```



From the Orchestrate docs:

"The Graph functionality allows for directed relations 
to be created between collection/key pairs 
and for those relations to be traversed."

A relation object allows you to create, delete, and query
relations associated with a key.

```python
relation = key.relation()
# create
response = relation.put('loves', 'people', 'David Bowie').result()
response.raise_for_status()
# query
response = relation.get('loves')
response.raise_for_status()
print response.json()
# {
#     "count": 1,
#     "results": [
#         {
#             "path": {
#                 "collection": "people",
#                 "key": "David Bowie",
#                 "ref": "0acfe7843316529f"
#             },
#             "value": {
#                 "age": 67,
#                 "name": "David Bowie"
#             }
#         }
#     ]
# }
# delete
response = relation.delete('loves', 'people', 'David Bowie').result()
response.raise_for_status()
```




## get


```python
    def get(self, *relations, **headers):
        
        resource = self._init_child(Resource, 'relations', *relations)
        return resource.get(**headers)

```



Queries all relations specified in `relations`, ex:

    relation.get('friend', 'friend')

...would return all friends of friends.

N.B.: Graph query results are not currently paginated.




## put


```python
    def put(self, relation, collection, key, **headers):
        
        resource = self._init_child(Resource, 'relation', relation, collection, key)
        return resource.put(**headers)

```



Creates a relationship between two objects.
Relations can span collections.




## delete


```python
    def delete(self, relation, collection, key, querydict={}, **headers):
        
        resource = self._init_child(Resource, 'relation', relation, collection, key)
        querydict['purge'] = True
        return resource.delete(querydict, **headers)

```



Deletes a relationship between two objects.
Automatically sets `?purge=true` in the querystring.




