#!/usr/bin/env python3
"""Build the permuter queue from the harvest filter's FAIL families.

Runs the seven-condition harvest filter over every unmatched Thumb row in every
arm9 module (all sizes), clusters rows into families by module + first eight
mnemonics, keeps families with at least two members, and ranks the failing
families by (member count descending, bytes descending). For each family the
smallest member is suggested as the first permute target.

Outputs:
  docs/authoring/permuter-queue.md   ranked markdown work list
  docs/authoring/permuter-queue.json machine-readable queue
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harvest_filter
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--prefix-len", type=int, default=8)
    ap.add_argument("--top", type=int, default=30)
    args = ap.parse_args()
    root = args.root.resolve()

    cfg = json.loads((root / "config/source_units.json").read_text(encoding="utf-8-sig"))
    modules = cfg["modules"]
    ledger = [json.loads(line) for line in (root / "ledger/functions.jsonl").read_text(encoding="utf-8").splitlines()]
    defined = harvest_filter.defined_addresses(root)
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)

    images = {}

    def image_for(module):
        if module not in images:
            info = modules[module]
            images[module] = ((root / info["originalImage"]).read_bytes(), int(info["loadAddressBase"], 0))
        return images[module]

    groups = defaultdict(list)
    rows = 0
    for r in ledger:
        if r.get("processor") != "arm9" or r.get("mode") != "thumb":
            continue
        module = r.get("module")
        if module not in modules or modules[module]["processor"] != "arm9":
            continue
        addr = int(r["address"], 16)
        size = r.get("bytes")
        if r["states"]["functionMatched"] or not isinstance(size, int):
            continue
        if addr in defined or addr in harvest_filter.PARKED:
            continue
        image, base = image_for(module)
        insns = list(md.disasm(image[addr - base:addr - base + size], addr))
        groups[(module, tuple(x.mnemonic for x in insns[:args.prefix_len]))].append((addr, size))
        rows += 1

    families = []
    passing = 0
    singletons = 0
    for (module, prefix), members in groups.items():
        if len(members) < 2:
            singletons += 1
            continue
        image, base = image_for(module)
        reasons = set()
        failing = []
        for addr, size in members:
            insns = list(md.disasm(image[addr - base:addr - base + size], addr))
            result = harvest_filter.analyse(insns, image, base)
            if result["reasons"]:
                reasons.update(result["reasons"])
                failing.append((addr, size))
        if not reasons:
            passing += 1
            continue
        first = min(failing, key=lambda pair: (pair[1], pair[0]))
        families.append(dict(
            module=module,
            prefix=" ".join(prefix),
            members=[dict(address="%08x" % a, bytes=s) for a, s in sorted(members)],
            rows=len(members),
            bytes=sum(s for _, s in members),
            first="%08x" % first[0],
            firstBytes=first[1],
            reasons=sorted(reasons),
        ))

    families.sort(key=lambda f: (-f["rows"], -f["bytes"], f["module"], f["prefix"]))
    summary = dict(
        generatedFrom=dict(filter="ops/harvest_filter.py", ledger="ledger/functions.jsonl", root="."),
        scannedRows=rows,
        families=len(families),
        familyRows=sum(f["rows"] for f in families),
        familyBytes=sum(f["bytes"] for f in families),
        passingFamilies=passing,
        singletonRows=singletons,
        top=families[:args.top],
    )

    docs = root / "docs/authoring"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "permuter-queue.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Permuter queue",
        "",
        "Generated from `ops/harvest_filter.py`. Every family below fails at least one of the seven",
        "harvest conditions, i.e. its bytes are not shape-determined by the current source model;",
        "the smallest member is the suggested first permute target.",
        "",
        "- scanned rows: %d" % summary["scannedRows"],
        "- failing families: %d (%d rows, %d bytes)" % (
            summary["families"], summary["familyRows"], summary["familyBytes"]),
        "- passing families (not queued): %d" % summary["passingFamilies"],
        "- singleton rows (not queued as families): %d" % summary["singletonRows"],
        "",
        "| # | module | family | rows | bytes | first row | reasons |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for index, family in enumerate(families[:args.top], 1):
        lines.append("| %d | %s | `%s` | %d | %d | `%s` (%d B) | %s |" % (
            index, family["module"], family["prefix"], family["rows"], family["bytes"],
            family["first"], family["firstBytes"], "; ".join(family["reasons"])))
    lines.append("")
    lines.append("Full queue (every family, with member addresses) is in `permuter-queue.json`.")
    (docs / "permuter-queue.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("scanned %d unmatched Thumb rows; %d failing families (%d rows, %d bytes); "
          "%d passing families; %d singleton rows" % (
              summary["scannedRows"], summary["families"], summary["familyRows"],
              summary["familyBytes"], summary["passingFamilies"], summary["singletonRows"]))
    for index, family in enumerate(families[:args.top], 1):
        print("%2d. %-8s %-6d %5d B  %s  %s" % (
            index, family["module"], family["rows"], family["bytes"],
            family["first"], "; ".join(family["reasons"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
