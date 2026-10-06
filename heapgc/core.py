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
    stack = [oid for oid in roots if oid in objects]
    while stack:
        oid = stack.pop()
        if oid in alive:
            continue
        alive.add(oid)
        for target in objects[oid].get("refs", []):
            if target in objects and target not in alive:
                stack.append(target)
    freed = []
    for oid in list(objects):
        counter.scanned += 1
        if oid in alive:
            objects[oid]["gen"] = GEN_YOUNG
            continue
        objects[oid]["gen"] = objects[oid].get("gen", GEN_YOUNG) + 1
        if objects[oid]["gen"] <= gen_limit:
            freed.append(oid)
            del objects[oid]
    return freed
