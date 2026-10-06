"""对象图上的标记清除。"""

GEN_YOUNG = 0
GEN_OLD = 1


class Counter:
    """记录本轮检查过的对象条数。"""

    def __init__(self):
        self.scanned = 0


def collect(objects, roots, gen_limit, counter):
    """回收一轮，返回本轮释放的对象 id。"""
    alive = set()
    stack = list(roots)
    while stack:
        oid = stack.pop()
        if oid in alive or oid not in objects:
            continue
        alive.add(oid)
        stack.extend(objects[oid].get("refs", []))
    freed = []
    for oid in list(objects):
        counter.scanned += 1
        if oid in alive:
            objects[oid]["gen"] = GEN_YOUNG
            continue
        objects[oid]["gen"] = objects[oid].get("gen", GEN_YOUNG) + 1
        freed.append(oid)
        if objects[oid]["gen"] > gen_limit:
            del objects[oid]
    return freed
