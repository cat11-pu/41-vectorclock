"""vectorclock.py：因果时钟（基线：只比总计数）。"""
from __future__ import annotations


class VClock:
    def __init__(self, name: str = "n1"):
        self.name = name
        self.clock = {}
        self.merges = 0

    def tick(self, node: str = None) -> dict:
        node = node or self.name
        self.clock[node] = self.clock.get(node, 0) + 1
        return dict(self.clock)

    def merge(self, other) -> dict:
        for node, value in other.clock.items():
            self.clock[node] = max(self.clock.get(node, 0), value)
        self.merges += 1
        return dict(self.clock)

    def compare(self, other) -> str:
        """基线：只比总大小，并发一律说 before/after。"""
        mine = sum(self.clock.values())
        theirs = sum(other.clock.values())
        if mine == theirs:
            return "equal"
        return "before" if mine < theirs else "after"

    def concurrent_with(self, others) -> list:
        raise NotImplementedError("并发集合还没实现")

    def persist(self) -> bytes:
        raise NotImplementedError("快照还没实现")

    def restore(self, blob: bytes = None) -> dict:
        raise NotImplementedError("重启恢复还没实现")

    def stats(self) -> dict:
        return {"clock": dict(self.clock), "merges": self.merges}
