import pytest

@pytest.fixture
def json():
    return {
        'k': [
            {'k': 3, 'kk': 'dil', 'kkk': True}
        ],
        'kk': { 'k': {'k': 'did'} },
        'ed': {}, 'el': [], 'l': [1,2,3, 'a', 'b','c'],
        'dwid': {
            'id': 33,
            'k': 'v'
        }
    }


from rdflib import Graph
def is_eq(g1: Graph|str, g2: Graph|str):
    from rdflib import Graph
    g1 = Graph().parse(data=g1, format='text/turtle') if isinstance(g1, str) else g1
    g2 = Graph().parse(data=g2, format='text/turtle') if isinstance(g2, str) else g2
    from rdflib.compare import isomorphic
    return isomorphic(g1, g2)



def test(json, file_regression):
    j = json
    from json2rdf.json2rdf import j2r
    r = j2r(j)

    def check_fn(obtained_fn, expected_fn):
        o, e = map(lambda f: open(f).read(), (obtained_fn, expected_fn))
        if not is_eq(o, e): raise AssertionError
    file_regression.check(r, check_fn=check_fn, extension='.ttl')
    
