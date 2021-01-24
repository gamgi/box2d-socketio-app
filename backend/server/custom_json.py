from dataclasses import fields, is_dataclass
import json
from Box2D import b2Vec2


def shallow_asdict(obj):
    if not is_dataclass(obj):
        raise TypeError("shallow_asdict() should be called on dataclass instances")

    # follows dataclasses.asdict() implementation
    result = []
    for f in fields(obj):
        value = getattr(obj, f.name)
        result.append((f.name, value))
    return dict(result)


class EnhancedJSONEncoder(json.JSONEncoder):
    # https://stackoverflow.com/questions/51286748/make-the-python-json-encoder-support-pythons-new-dataclasses
    def default(self, o):
        if is_dataclass(o):
            return shallow_asdict(o)
        elif isinstance(o, b2Vec2):
            return o.tuple
        return super().default(o)


def dumps(data, *args, **kwargs):
    return json.dumps(data, *args, cls=EnhancedJSONEncoder, **kwargs)


def loads(data, *args, **kwargs):
    return json.loads(data, *args, **kwargs)
