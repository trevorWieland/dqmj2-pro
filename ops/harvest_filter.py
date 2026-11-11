#!/usr/bin/env python3
"""Filter ov006 Thumb families by the seven-condition harvest rule.

The rule is docs/authoring/harvest-prediction.md. Families are clusters of
unmatched rows in a byte band that share their first eight mnemonics.

Rules 1-4 are read mechanically: call count, reload/branch-on-result after the
last call, callee-saved registers in the prologue, stack stores, record chain.

Rules 5-7 read the branch bodies and operand idioms that the experiment showed
are the real discriminator:
  5. branch-merged pointer/literal select (two paths load different address
     constants that feed a dereference);
  6. mask-equality comparison (`ands` whose two operands are then compared,
     which C may emit as `bics` instead);
  7. byte bit-test implemented as a shift-extract (`lsls`+`lsrs` pair feeding
     a conditional branch).

Exit status is 0 when at least one family passes, 1 when none does; in the
latter case every family's failure reasons are printed.
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
except ImportError:  # pragma: no cover
    sys.exit("capstone is required (run from the repo's Python environment)")

PARKED = {
    0x21F7ED8, 0x21FB384, 0x21FC1C8, 0x21FE4DC, 0x21FF6B4, 0x2200950,
    0x220383C, 0x22038E8, 0x2204218, 0x2204268, 0x220428C, 0x2204364,
    0x2204974, 0x21ECF68, 0x21EDA84, 0x21F1EF0, 0x21F2370, 0x21F5418,
    0x21F5428, 0x220490C, 0x2201AF8,
}
BRANCHES = {"b", "beq", "bne", "bgt", "bge", "blt", "ble", "bhi", "bls", "bcs", "bcc", "bmi", "bpl", "bvs", "bvc", "cbz", "cbnz"}
LOADS = {"ldr", "ldrb", "ldrh", "ldrsb", "ldrsh"}


def address_value(root, text):
    return int(text, 0)


def load_ledger(root):
    path = root / "ledger/functions.jsonl"
    rows = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            rows.append(json.loads(line))
    return rows


def defined_addresses(root):
    defined = set()
    for p in (root / "src").rglob("*"):
        if p.is_file():
            m = re.search(r"([0-9a-f]{8})", p.name)
            if m:
                defined.add(int(m.group(1), 16))
    for p in (root / "src").rglob("*.c"):
        text = p.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"0x0?([0-9a-fA-F]{8})", text):
            defined.add(int(m.group(1), 16))
    return defined


def pc_literal(insn, image, base):
    m = re.search(r"#(-?0x[0-9a-f]+)", insn.op_str)
    if not m:
        return None
    lit = ((insn.address + 4) & ~3) + int(m.group(1), 16)
    if not (0 <= lit - base <= len(image) - 4):
        return None
    return int.from_bytes(image[lit - base:lit - base + 4], "little")


def is_address_like(value):
    return 0x02000000 <= value < 0x05000000 and value % 2 == 0 and value >= 0x02000000


def is_mask_like(value):
    return value < 0x02000000 and value not in (0, 1)


def analyse(insns, image, base):
    calls = [i for i, x in enumerate(insns) if x.mnemonic in ("bl", "blx")]
    last_call = calls[-1] if calls else -1
    reload_after = False
    branch_on_result = False
    if last_call >= 0:
        for insn in insns[last_call + 1:]:
            if insn.mnemonic in LOADS and ("[pc" in insn.op_str or "[sp" in insn.op_str):
                reload_after = True
            if insn.mnemonic in ("cmp", "tst") and re.search(r"\br0\b", insn.op_str):
                branch_on_result = True
    push = next((x for x in insns if x.mnemonic == "push"), None)
    saved = 0
    if push:
        saved = len([r for r in re.findall(r"r(\d+)", push.op_str) if int(r) >= 4])
    stack_stores = sum(1 for x in insns if x.mnemonic in ("str", "strh", "strb") and "[sp" in x.op_str)
    chain = any(insns[k].mnemonic == "ldr" and "[pc" in insns[k].op_str and
                insns[k + 1].mnemonic == "ldr" and insns[k + 1].op_str.endswith("]")
                for k in range(len(insns) - 1))

    select_merge = False
    for k, insn in enumerate(insns):
        if insn.mnemonic not in BRANCHES:
            continue
        falthrough = insns[k + 1] if k + 1 < len(insns) else None
        target = re.search(r"#(0x[0-9a-f]+)", insn.op_str)
        if not target or falthrough is None:
            continue
        first = [falthrough]
        second = None
        for j, cand in enumerate(insns):
            if cand.address == int(target.group(1), 16):
                second = cand
                break
        if second is None:
            continue
        def address_of(seq):
            if not seq:
                return None
            if seq[0].mnemonic == "ldr" and "[pc" in seq[0].op_str:
                return pc_literal(seq[0], image, base)
            if seq[0].mnemonic == "movs" and len(seq) > 1 and seq[1].mnemonic == "lsls":
                m = re.search(r"#(?:0x)?([0-9a-f]+)", seq[0].op_str)
                n = re.search(r"#(?:0x)?([0-9a-f]+)", seq[1].op_str)
                if m and n:
                    return int(m.group(1), 16) << int(n.group(1), 16)
            return None

        path_a = insns[k + 1:k + 4]
        path_b = []
        for j, cand in enumerate(insns):
            if cand.address == int(target.group(1), 16):
                path_b = insns[j:j + 3]
                break
        va, vb = address_of(path_a), address_of(path_b)
        if va is not None and vb is not None and is_address_like(va) and is_address_like(vb):
            select_merge = True

    mask_equality = False
    for k in range(len(insns) - 3):
        a = insns[k]
        if a.mnemonic != "ands":
            continue
        regs = [r for r in re.findall(r"r(\d+)", a.op_str)]
        if len(regs) < 2:
            continue
        ra = "r" + regs[0]
        rb = "r" + regs[1]
        for cand in insns[k + 1:k + 5]:
            if cand.mnemonic == "cmp" and ra in cand.op_str and rb in cand.op_str:
                mask_equality = True
                break
        if mask_equality:
            break

    shift_extract = False
    for k in range(len(insns) - 2):
        a, b = insns[k], insns[k + 1]
        if a.mnemonic != "lsls" or b.mnemonic != "lsrs":
            continue
        ma = re.search(r"r(\d+), r\d+, #0x([0-9a-f]+)", a.op_str)
        mb = re.search(r"r(\d+), r\d+, #0x([0-9a-f]+)", b.op_str)
        if not ma or not mb or ma.group(1) != mb.group(1):
            continue
        if int(ma.group(2), 16) + int(mb.group(2), 16) == 32:
            for cand in insns[k + 2:k + 4]:
                if cand.mnemonic in BRANCHES:
                    shift_extract = True
                    break

    reasons = []
    if reload_after:
        reasons.append("rule1 post-call reload")
    if branch_on_result:
        reasons.append("rule1 branch on call result")
    if saved > 1:
        reasons.append("rule2 saved=%d" % saved)
    if stack_stores:
        reasons.append("rule3 stack=%d" % stack_stores)
    if chain:
        reasons.append("rule4 record chain")
    if select_merge:
        reasons.append("rule5 branch-merged address select")
    if mask_equality:
        reasons.append("rule6 mask-equality idiom")
    if shift_extract:
        reasons.append("rule7 byte shift-extract")
    return dict(calls=len(calls), reload_after=int(reload_after), branch_result=int(branch_on_result),
                saved=saved, stack=stack_stores, chain=int(chain), select=int(select_merge),
                mask_eq=int(mask_equality), shift=int(shift_extract), reasons=reasons)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--module", default="ov006")
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--min-bytes", type=int, default=40)
    ap.add_argument("--max-bytes", type=int, default=80)
    ap.add_argument("--prefix-len", type=int, default=8)
    ap.add_argument("--limit-families", type=int, default=0, help="only print the first N families")
    args = ap.parse_args()
    root = args.root.resolve()

    cfg = json.loads((root / "config/source_units.json").read_text(encoding="utf-8-sig"))
    modules = cfg["modules"]
    rows = load_ledger(root)
    defined = defined_addresses(root)
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    cache = {}

    def image_for(module):
        if module not in cache:
            info = modules[module]
            blob = (root / info["originalImage"]).read_bytes()
            base = int(info["loadAddressBase"], 0)
            cache[module] = (blob, base)
        return cache[module]

    candidates = []
    for r in rows:
        if r.get("processor") != "arm9" or r.get("module") != args.module or r.get("mode") != "thumb":
            continue
        addr = int(r["address"], 16)
        size = r.get("bytes")
        if r["states"]["functionMatched"] or not isinstance(size, int):
            continue
        if not (args.min_bytes <= size <= args.max_bytes):
            continue
        if addr in defined or addr in PARKED:
            continue
        candidates.append((addr, size))
    candidates.sort()

    families = defaultdict(list)
    for addr, size in candidates:
        image, base = image_for(args.module)
        insns = list(md.disasm(image[addr - base:addr - base + size], addr))
        families[tuple(x.mnemonic for x in insns[:args.prefix_len])].append((addr, size))

    passing = 0
    failed = 0
    print("module %s, band %d-%d B, %d rows, %d families" % (
        args.module, args.min_bytes, args.max_bytes, len(candidates), len(families)))
    print("%-56s %5s %6s  %s" % ("family prefix", "rows", "bytes", "result"))
    shown = 0
    for prefix, members in sorted(families.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        if len(members) < 2:
            continue
        if args.limit_families and shown >= args.limit_families:
            break
        shown += 1
        image, base = image_for(args.module)
        addr, size = sorted(members)[0]
        insns = list(md.disasm(image[addr - base:addr - base + size], addr))
        result = analyse(insns, image, base)
        ok = not result["reasons"]
        passing += int(ok)
        failed += int(not ok)
        print("%-56s %5d %6d  %s%s" % (
            " ".join(prefix), len(members), sum(s for _, s in members),
            "PASS" if ok else "FAIL " + "; ".join(result["reasons"]),
            "" if ok else "  [" + " ".join("%08x" % a for a, _ in sorted(members)) + "]"))

    print("\n%d families scanned, %d pass all seven, %d fail" % (shown, passing, failed))
    if passing == 0:
        print("no family passes; nothing to author", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
