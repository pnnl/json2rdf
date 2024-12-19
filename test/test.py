

def json():
    return {
        'k': [
            {'k': 3, 'kk': 'dil', 'kkk':True}
        ],
        'kk': { 'k': {'k': 'did'} },
        'ed': {}, 'el': [],
        'dwid': {
            'id': 33,
            'k': 'v'
        }
    }

def json():
    return {'k':'v', 'id':'id', 'l': [1,2,3, {'k':'v'}] }

def json():
    return {'id':'id', 'ID': 'ID', 'refid': 'id' }

def json():
    return {'id':'id', 'array': list(range(5))  }


def rdf():
    return """
    prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    _:2142013828288 _:id 2142013828288.
    _:2142013828288 _:k _:2142054851264.
    _:2142053379456 rdf:_0 _:2142054854336.
    _:2142053379456 _:id 2142053379456.
    _:2142054851264 _:id 2142054851264.
    _:2142054851264 _:k "asdf".
    _:2142054854336 _:id 2142054854336.
    _:2142054854336 _:k 3.
    _:2142054854336 _:kk "asdf".
    _:2142054860992 _:id 2142054860992.
    _:2142054860992 _:k _:2142053379456.
    _:2142054860992 _:kk _:2142013828288.
    """


from rdflib import Graph
def is_eq(g1: Graph|str, g2: Graph|str):
    from rdflib import Graph
    g1 = Graph().parse(data=g1, format='text/turtle') if isinstance(g1, str) else g1
    g2 = Graph().parse(data=g2, format='text/turtle') if isinstance(g2, str) else g2
    from rdflib.compare import isomorphic
    return isomorphic(g1, g2)


def test_iso():
    _ = json()
    from json2rdf.json2rdf import j2r
    r1 = j2r(_, )
    r2 = j2r(_,)
    assert(len(r2) == len(r2))
    assert(is_eq(r1, r2))



def test():
    # from rdflib import Graph
    # a = rdf()
    # a = Graph().parse(data=a, format='text/turtle')

    _ = json()
    from json2rdf.json2rdf import j2r
    f = j2r(_, array_keys = {'array',} )
    print(f)
    #f = Graph().parse(data=f, format='text/turtle')

    #from rdflib.compare import isomorphic
    #assert(isomorphic(f, a))
    
