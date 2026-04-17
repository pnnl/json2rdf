![PyPI - Status](https://img.shields.io/pypi/v/json2rdf)

# JSON2RDF

Converts JSON to RDF

```python
>>> from json2rdf.json2rdf import j2r
>>> j = {'id':0, 'list': [1,2,3], 'nesting': {'id':1, 'property': 'abc' }}
>>> print(j2r(j))
```
```turtle
prefix rdf:                   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix id:      <urn:example:id:>
prefix prefix:     <urn:example:prefix:>

id:0 prefix:id 0.
id:0 prefix:list _:2432178001088.
id:0 prefix:nesting id:1.
id:1 prefix:id 1.
id:1 prefix:property "abc".
_:2432178001088 rdf:_0 1.
_:2432178001088 rdf:_1 2.
_:2432178001088 rdf:_2 3.
```

```
Help on function json2rdf in module json2rdf.json2rdf:

json2rdf(
    data: str | dict,
    *,
    sort=True,
    subject_id_keys=('id',),
    deanon: bool = False,
    object_id_keys={'idref', 'refid'},
    id_prefix=('id', 'urn:example:id:'),
    key_prefix=('prefix', 'urn:example:prefix:')
)
    sort: the triples
    subject_keys: set of keys to create a uri out of in for the *subject*.
        the first key will be used to create a predicate if one does not exist.
        example: {"id": 1, "key":"abc" } ->
            prefix:1 prefix:key "abc".
            prefix:1 prefix:id prefix:1.
        example: case when no id key in data or no id key is set: {"key: "abc"} ->
            prefix:generated prefix:key "abc".
            prefix:generated prefix:id prefix:generated.
    object_keys: set of keys to interpret as a uri out of as an *object*.
        example: {"id": 1, "refid": 2,} ->
            prefix:1 prefix:refid prefix:2.
    deanon: can be set to True to use id_prefix when no id key is present.
        otherwise, a blank/anon node will be used.


```

## Why?

Motivation: This was developed as part of [BIM2RDF](https://github.com/PNNL/BIM2RDF)
where the main implementation language is Python
and the data sizes from [Speckle](https://www.speckle.systems/) are not small.

* [Prior implementation](https://github.com/AtomGraph/JSON2RDF)  is in java.
* Don't want to use [JSON-LD](https://json-ld.org/playground/)
(mentioned in above [documentation](https://github.com/AtomGraph/JSON2RDF/blob/master/README.md)  ).
Furthermore, the [Python JSON-LD implementation](https://github.com/digitalbazaar/pyld) was found to be too slow.


## How?

Traversing the (nested) JSON, a conversion is applied to 
'expand' data containers, lists and mappings, as triples.



## Behavior

is 'entity-driven': data containers must have identifiers.

When no identifier is given, an anoymous/blank node is used.
This is close to the 'spirit' of the semantic web.
However, this makes the conversion non-deterministic.
Reprecussions must be handled by the user.

`deanon=True` can be passed as an argument
which will use `id_prefix` instead of a blank node.
While reading of the rdf will be deterministic,
the conversion cannot be considered so.
(It's only deterministic per Python session
if the same `dict` data instance is read.)

[Nulls are preserved](https://github.com/w3c/json-ld-syntax/issues/258)
as it would be the 'least surprising' behviour.


## Features
none. zilch. nada.


## Development Philosophy
* **KISS**: It should only address converting (given) JSON to RDF.
Therefore, the code is expected to be feature complete (without need for adding more 'features').
* **Minimal dependencies**: follows from above.
Zero dependencies is possible and ideal.
(This would make it easier for a compiled Python version to be created for more performance.)
* List representation shall not be a [linked list](https://ontola.io/blog/ordered-data-in-rdf).
