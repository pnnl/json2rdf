# class Remapping
# composition  would involve composing terminals
# which are somehow the last thing in matching functions.

# this /might/ be done faster using parsing like Lark

def classes():
    # just to create a copy of the following.
    # too lazy to convert them to be able to be instantiated.
    class Termination:
        """ 'pre'-processing """
        terminals = {
            int, float,
            str,
            bool,
            type(None), # weird
            # does json have datetime?
            }
        terminals = tuple(terminals)
        @classmethod
        def visit(cls, p, k, v):
            return True

        @classmethod
        def map(cls, d):
            from boltons.iterutils import remap
            return remap(d, visit=cls.visit)


    class Identification:
        types = (int, str)

        from dataclasses import dataclass
        @dataclass(frozen=True)
        class ID:
            value: int | str # usually. types above
            def __str__(self) -> str:
                return str(self.value)
        class anonID(ID): ...
        
        terminals = {Termination.terminals}|{ID, anonID}
        terminals = tuple(terminals)

        subject_keys = ('id',)
        # cant do 
        # subject_key = subject_keys[0] 
        # @classproperty 'deprecated'
        # def subject_key
        object_keys = {'refid',}

        class list:
            key =   '__rdftype__'
            value = '__rdfseq__'
            
        @classmethod
        def enter(cls, p, k, v):
            subject_key = cls.subject_keys[0]
            def dicthasid(v):
                for id in cls.subject_keys:
                    if id in v:
                        yield id
            if type(v) is dict:
                dids = dicthasid(v)
                dids = tuple(dids)
                return (
                    #        wrap in ID
                    {sk: cls.ID(v[sk]) for sk in dids}
                    or {subject_key: cls.anonID(id(v))},
                    #       ..the rest of the data
                    ((k,v) for k,v in  v.items() if k not in dids ) )
            elif type(v) is list:
                # id(lst) is not deterministic. don't think it's a 'problem'
                return ({
                        subject_key: cls.anonID(id(v)),
                        cls.list.key: cls.list.value
                        },
                        enumerate(v))
            else:
                assert(isinstance(v, cls.terminals))
                return k, False
        
        @classmethod
        def visit(cls, p, k, v):
            # interpret object identifier cases
            # no anon. it's there.
            if k in cls.object_keys:
                if isinstance(v, cls.types):
                    return k, cls.ID(v)
            if p: # example connectedIds: [id1,id2,id3]
                if any(k in cls.object_keys for k in p):
                    if isinstance(v, cls.types):
                        return k, cls.ID(v)
            return True

        @classmethod
        def map(cls, d):
            from boltons.iterutils import remap
            return remap(d, enter=cls.enter, visit=cls.visit)
    

    class Tripling:
        """
        (identified) data -> triples
        """
        from dataclasses import dataclass
        @dataclass(frozen=True)
        class Triple:
            subject: 's'
            predicate: 'p'
            object: 'o'

            def __str__(self) -> str:
                return f"{self.subject} {self.predicate} {self.object}"
            
        class list(list):  #ordered set? TODO

            def __str__(self) -> str:
                _ = '\n'.join([str(i) for i in self])
                return _
        
        @classmethod
        def enter(cls, p, k, v):
            subject_key = Identification.subject_keys[0]
            if isinstance(v, dict):
                assert(subject_key in v)
                def _(v):
                    for ik, iv in v.items():
                        if isinstance(iv, dict):
                            yield from (
                                cls.Triple(v[subject_key] , ik, iv[subject_key] ),
                                iv, )
                        else:
                            assert(isinstance(iv, Identification.terminals ))
                            if not ((ik in Identification.subject_keys) and (type(iv) is Identification.anonID)):
                                yield cls.Triple(v[subject_key], ik, iv)
                return cls.list(), enumerate(_(v))
            else:
                assert(isinstance(v, cls.Triple))
                # no nesting. no need to 'enter'
                return None, False
        
        @classmethod
        def visit(cls, p, k, v):
            if isinstance(v, cls.Triple):
                if v.predicate in Identification.subject_keys:
                    if isinstance(v.object, Identification.ID):
                        return k, cls.Triple(v.subject, v.predicate, v.object.value)
            return True

        
        @classmethod
        def map(cls, d, flatten=True):
            from boltons.iterutils import remap
            _ = remap(d, enter=cls.enter, visit=cls.visit)
            if not flatten:
                return _
            else:
                _ = cls.flatten(_, seqtypes=(cls.list))
                _ = frozenset(_)
                _ = cls.list(_)
                return _
        
        @classmethod
        def flatten(cls, items, seqtypes=(list, tuple)):
            def flatten(items, seqtypes=seqtypes):
                #https://stackoverflow.com/questions/10823877/what-is-the-fastest-way-to-flatten-arbitrarily-nested-lists-in-python
                try:
                    for i, x in enumerate(items):
                        while isinstance(x, seqtypes):
                            items[i:i+1] = x
                            x = items[i]
                except IndexError:
                    pass
                return items
            return flatten(items, seqtypes=seqtypes)


    class RDFing:

        class Triple(Tripling.Triple):
            def __str__(self) -> str:
                if isinstance(self.subject, Tripling.Triple):
                    #                     but take out the dot
                    s = f"<<{str(self.subject)[:-1]}>>"
                else:
                    s = str(self.subject)
                if isinstance(self.object, Tripling.Triple):
                    o = f"<<{str(self.object)[:-1]}>>"
                else:
                    o = str(self.object)
                return f"{s} {self.predicate} {o}."
        class list(Tripling.list):
            id_prefix =                 'id'
            id_uri =                    f"urn:example:{id_prefix}:"
            key_prefix =                'prefix'
            key_uri =                   f"urn:example:{key_prefix}:"
            meta_prefix =               'meta'
            meta_uri =                  "urn:example:meta:"

            def __str__(self) -> str:
                _ =     f'prefix rdf:                   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \n'
                _ = _ + f'prefix {self.id_prefix}:      <{self.id_uri}>     \n'
                _ = _ + f'prefix {self.key_prefix}:     <{self.key_uri}>    \n'
                _ = _ + f'prefix {self.meta_prefix}:    <{self.meta_uri}>   \n\n'
                _ = _ + super().__str__()
                return _
        
        @classmethod
        def triple(cls, s, p, o):
            m = {True: 'true', False:'false', None: '\"null\"'} # not rdf:nil which is specific to a rdf:List
            from types import NoneType
            # SUBJECT
            assert(isinstance(s, Identification.ID))
            if type(s) is Identification.ID:
                s = f'{cls.list.id_prefix}:{s}'
            else:
                assert(type(s) is Identification.anonID)
                s = f'_:{s}'
            # special list/seq handling
            if p == Identification.list.key and o == Identification.list.value:
                return cls.Triple(s, "rdf:type", "rdf:Seq")

            # PREDICATE
            # just need to take care of int predicates
            if isinstance(p, int):
                p = f'rdf:_{p}'
            else:
                assert(isinstance(p, str))
                p = p.replace(' ', '_')
                # create legal by dropping non alpha num
                # url encodeing?
                p = ''.join(c for c in p if c.isalnum() or c == '_')
                p = f'{cls.list.key_prefix}:{p}'
            
            # OBJECT
            #      need to escape quotes
            if isinstance(o, str):
                # dont want to encode('unicode_escape').decode()
                # to not lose unicode chars
                # escape all the backslashes, first..
                o = o.replace("\\", "\\\\")
                # /then/ ...
                # escape spacing things
                o = o.replace('\n', '\\n')
                o = o.replace('\r', '\\r')
                o = o.replace('\f', '\\f')
                o = o.replace('\t', '\\t')
                # inner quotes
                o = o.replace('"', '\\"')
                # outer quote
                o = '"'+o+'"'
            elif isinstance(o, (bool, NoneType)): # https://github.com/w3c/json-ld-syntax/issues/258
                o = m[o]
            elif isinstance(o, Identification.ID):
                if type(o) is Identification.ID:
                    o = f'{cls.list.id_prefix}:{o}'
                else:
                    assert(type(o) is Identification.anonID)
                    o = f'_:{o}'
            else:
                o = str(o)
            return cls.Triple(s,p,o)

        @classmethod
        def visit(cls, v):
            assert(isinstance(v, Tripling.Triple))
            # meta tripling
            # just do one-level in
            if isinstance(v.subject, Tripling.Triple):
                s = cls.triple(v.subject.subject,
                            v.subject.predicate,
                            v.subject.object)
            else:
                s = v.subject
            p = v.predicate
            if isinstance(v.object, Tripling.Triple):
                o = cls.triple(v.object.subject,
                            v.object.predicate,
                            v.object.object)
            else:
                o = v.object
            if p == cls.list.meta_uri:
                p = f"{cls.list.meta_prefix}:"
                return cls.Triple(s, p, o)
            else:
                return cls.triple(s,p,o)

        @classmethod
        def map(cls, d, meta=[], ):
            if meta:
                from itertools import product
                d = product(d, meta)
                d = map(lambda mt: Tripling.Triple(mt[0], cls.list.meta_uri, mt[1]), d)
            _ = map(cls.visit, d)
            _ = cls.list(_)
            return _

    _ = locals()
    from inspect import isclass
    for n,c in _.items(): assert(isclass(c))
    from types import SimpleNamespace as NS
    return NS(**_)

defaults = classes()
def json2rdf(
        data: str | dict,
        meta: str | dict = {},
        *,
        asserted =          True,
        sort =              True, # (attempt to) make conversion deterministic
        # id interpretation
        subject_id_keys =   defaults.Identification.subject_keys,
        object_id_keys =    defaults.Identification.object_keys,
        # # uri construction
        id_prefix =         (defaults.RDFing.list.id_prefix,
                             defaults.RDFing.list.id_uri),
        key_prefix =        (defaults.RDFing.list.key_prefix,
                             defaults.RDFing.list.key_uri),
        meta_prefix =       (defaults.RDFing.list.meta_prefix,
                             defaults.RDFing.list.meta_uri)
        ):
    """
    meta: meta triples to associate with data triples:
        <<data triple>> {meta_uri} <<meta triple n>>.
    asserted: in the case of meta triples, should the data triples be separate?
          data.subject data.predicate data.object.                                # include this?
        <<data.subject data.predicate data.object>> {meta_uri} <<meta triple n>>. # ..in addition to this?
    sort: the triples
    subject_keys: set of keys to create a uri out of in for the *subject*.
        the first key will be used to create a predicate if one does not exist.
        example: {"id": 1, "key":"abc" } ->
            prefix:1 prefix:key "abc".
            prefix:1 prefix:id prefix:1.
        example: case when no id key: {"key: "abc"} ->
            prefix:generated prefix:key "abc".
            prefix:generated prefix:id prefix:generated.
    object_keys: set of keys to interpret as a uri out of as an *object*.
        example: {"id": 1, "refid": 2,} ->
            prefix:1 prefix:refid prefix:2.
    """
    f = classes()
    f.Identification.subject_keys = [k for k in subject_id_keys if k in frozenset(subject_id_keys)]
    f.Identification.object_keys = frozenset(object_id_keys)

    f.RDFing.list.id_prefix,      f.RDFing.list.id_uri =    id_prefix
    f.RDFing.list.key_prefix,     f.RDFing.list.key_uri =   key_prefix
    f.RDFing.list.meta_prefix,    f.RDFing.list.meta_uri =  meta_prefix

    d = data
    m = meta
    def triples(data):
        _ = data
        _ = f.Termination.map(_)
        _ = f.Identification.map(_)
        _ = f.Tripling.map(_)
        return _
    if isinstance(d, str):
        from json import loads
        d = loads(d)
    if m:
        if isinstance(m, str):
            from json import loads
            m = loads(m)

    d = triples(d)
    if m:
        m = triples(m)
        m = f.RDFing.map(d, meta=m)
        if asserted:
            # just pull rdfed
            d = frozenset([t.subject for t in m])
        else:
            d = frozenset()
        # asserted 'data' triples + meta triples
        _ = frozenset(m) | d  # set->list source of indeterminism
        if sort:
            _ = sorted(_, key=str)
        d = f.RDFing.list(_)
    else:
        if sort:
            d = sorted(d, key=str)
        d = f.RDFing.map(d)
    d = str(d)
    return d

j2r = json2rdf

if __name__ == '__main__':
    from .cli import _
