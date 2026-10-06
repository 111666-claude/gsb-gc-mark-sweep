"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def _obj(oid, refs=None, gen=0):
    return {"refs": refs or [], "gen": gen}


def run(name):
    if name == "chain":
        objects = {"a": _obj("a", ["b"]), "b": _obj("b", ["c"]), "c": _obj("c")}
        freed = core.collect(objects, ["a"], 3, core.Counter())
        _line({"freed": sorted(freed)})
        return 0
    if name == "dup":
        objects = {"a": _obj("a"), "b": _obj("b")}
        freed = core.collect(objects, ["a"], 3, core.Counter())
        _line({"freed": sorted(freed)})
        return 0
    if name == "gen":
        objects = {"a": _obj("a")}
        core.collect(objects, [], 1, core.Counter())
        core.collect(objects, [], 1, core.Counter())
        freed = core.collect(objects, [], 1, core.Counter())
        _line({"freed": sorted(freed)})
        return 0
    if name == "work":
        objects = {}
        for i in range(2000):
            nxt = "o%04d" % (i + 1)
            objects["o%04d" % i] = _obj("o%04d" % i, [nxt] if i + 1 < 2000 else [])
        counter = core.Counter()
        core.collect(objects, ["o0000"], 3, counter)
        _line({"objects": 2000, "scanned": counter.scanned})
        return 0
    raise SystemExit("未知场景：" + name)
