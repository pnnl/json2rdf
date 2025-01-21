from pathlib import Path
from inspect import signature as sig
from . import json2rdf as j2r
args = sig(j2r).parameters
def _(
        i=Path('data.json'), imeta=None,
        asserted =          args['asserted']        .default,
        sort =              args['sort']            .default,
        # id interpretation
        subject_id_keys =   args['subject_id_keys'] .default,
        object_id_keys =    args['object_id_keys']  .default,
        # uri construction
        id_prefix =         args['id_prefix']       .default,
        key_prefix =        args['key_prefix']      .default,
        meta_prefix =       args['meta_prefix']     .default,
        o: Path|None=None,#Path('data.ttl'),
        ):
    from json import load
    data = load(open(i))
    meta = load(open(imeta)) if imeta else args['meta'].default
    _ = j2r(
            data, meta=meta,
            asserted=asserted,
            sort=sort,
            subject_id_keys=subject_id_keys,
            object_id_keys=object_id_keys,
            id_prefix=id_prefix,
            key_prefix=key_prefix,
            meta_prefix=meta_prefix,)
    if not o:
        return _
    else:
        open(o, 'w').write(_)
        return o
_.__doc__ = j2r.__doc__
from fire import Fire
_ = Fire(_)
exit(0)
