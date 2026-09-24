"""check_sample.py：按 sample/clocks.json 走一圈，打印验收面。"""
import json
import os
import sys

from vectorclock import VClock


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join("sample", "clocks.json")
    with open(path, encoding="utf-8") as handle:
        spec = json.load(handle)

    def build(raw):
        clock = VClock(raw.get("name", "n1"))
        clock.clock = dict(raw["clock"])
        return clock

    base = build(spec["base"])
    comparisons = []
    for item in spec["others"]:
        comparisons.append((item["name"], base.compare(build(item))))
    merged = build(spec["base"])
    for item in spec["others"]:
        merged.merge(build(item))
    conflict = build(spec["base"])
    blob = base.persist()
    reborn = VClock(spec["base"].get("name", "n1"))
    restored = reborn.restore(blob)
    events = []
    for event in spec["events"]:
        events.append((event["node"], event["event"], dict(spec["event_clocks"][event["event"]])))
    print("与各时钟的比较 =", comparisons)
    print("并发集合 =", conflict.concurrent_with([build(item) for item in spec["others"]]))
    print("合并后的时钟 =", merged.clock)
    print("事件时钟 =", [(node, event) for node, event, _ in events])
    print("并发事件对 =", spec["concurrent_pairs"])
    print("恢复后的时钟 =", restored.get("clock"))
    print("不变量（合并后各分量不小于两边） =", spec["merge_invariant"])
    print("时钟分量数 =", len(base.clock))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
