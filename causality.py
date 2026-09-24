"""causality.py：对外门面（老接口 tick/merge/compare 不能改）。"""
from __future__ import annotations

from vectorclock import VClock


class Tracker:
    def __init__(self, name: str = "n1"):
        self.vclock = VClock(name)

    def tick(self, node: str = None) -> dict:
        return self.vclock.tick(node)

    def merge(self, other) -> dict:
        return self.vclock.merge(other.vclock if hasattr(other, "vclock") else other)

    def compare(self, other) -> str:
        return self.vclock.compare(other.vclock if hasattr(other, "vclock") else other)

    def snapshot(self) -> bytes:
        return self.vclock.persist()

    def rebuild(self, blob: bytes = None) -> dict:
        return self.vclock.restore(blob)
