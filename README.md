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
prefix meta:    <urn:example:meta:>

id:0 prefix:id 0.
id:0 prefix:list _:2432178001088.
id:0 prefix:nesting id:1.
id:1 prefix:id 1.
id:1 prefix:property "abc".
_:2432178001088 rdf:_0 1.
_:2432178001088 rdf:_1 2.
_:2432178001088 rdf:_2 3.
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


## Features

Optional:
**'meta triples'**: as RDF-star: `<<{data triple}>> {meta} <<{meta triple}>>`


## Development Philosophy
* **KISS**: It should only address converting (given) JSON to RDF.
Converting array data (above) is a special case.
Therefore, the code is expected to be feature complete (without need for adding more 'features').
* **Minimal dependencies**: follows from above.
Zero dependencies is possible and ideal.
(This would make it easier for a compiled Python version to be created for more performance.)
* List representation shall not be a [linked list](https://ontola.io/blog/ordered-data-in-rdf).
