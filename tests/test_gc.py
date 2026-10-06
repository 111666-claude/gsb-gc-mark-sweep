import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from heapgc import core


def obj(refs=None, gen=0):
    return {"refs": refs or [], "gen": gen}


class GcTest(unittest.TestCase):
    def test_root_is_alive(self):
        objects = {"a": obj()}
        freed = core.collect(objects, ["a"], 3, core.Counter())
        self.assertNotIn("a", freed)

    def test_unreachable_is_freed(self):
        objects = {"a": obj(), "b": obj()}
        freed = core.collect(objects, ["a"], 3, core.Counter())
        self.assertIn("b", freed)

    def test_direct_reference_is_alive(self):
        objects = {"a": obj(["b"]), "b": obj()}
        freed = core.collect(objects, ["a"], 3, core.Counter())
        self.assertEqual(freed, [])

    def test_empty_heap(self):
        self.assertEqual(core.collect({}, ["a"], 3, core.Counter()), [])

    def test_counting_happens(self):
        counter = core.Counter()
        core.collect({"a": obj()}, [], 3, counter)
        self.assertGreater(counter.scanned, 0)


if __name__ == "__main__":
    unittest.main()
