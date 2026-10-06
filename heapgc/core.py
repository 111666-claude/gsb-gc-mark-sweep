"""对象图上的标记清除。"""

GEN_YOUNG = 0
GEN_OLD = 1


class Counter:
    """记录本轮检查过的对象条数。"""

    def __init__(self):
        self.scanned = 0


def collect(objects, roots, gen_limit, counter):
    """回收一轮，返回本轮释放的对象 id。"""
    alive = {oid: True for oid in roots}
    for oid in list(alive):
        for target in objects.get(oid, {}).get("refs", []):
            if target in objects:
                alive[target] = True
    freed = []
    for oid in objects:
        counter.scanned += 1
        if oid not in alive:
            freed.append(oid)
    for oid in objects:
        for _ in objects:
            counter.scanned += 1
        if oid in alive:
            objects[oid]["gen"] = GEN_YOUNG
        else:
            objects[oid]["gen"] = objects[oid].get("gen", GEN_YOUNG) + 1
            freed.append(oid)
    return freed
