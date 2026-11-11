"""Regression tests for ops/harvest_filter.py rule 1 (every call's result use)."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harvest_filter


class FakeInsn:
    def __init__(self, mnemonic, op_str, address=0):
        self.mnemonic = mnemonic
        self.op_str = op_str
        self.address = address


def branch_on_result(insns):
    result = harvest_filter.analyse(insns, b"", 0)
    return any(reason.startswith("rule1 branch on call result") for reason in result["reasons"])


class Rule1Test(unittest.TestCase):
    def test_branch_on_intermediate_call_result_is_flagged(self):
        # bl 0x21ff0bc; adds r3, r0, #0; cmp r3, #2; bgt -> result copied then compared
        insns = [
            FakeInsn("bl", "#0x21ff0bc"),
            FakeInsn("adds", "r3, r0, #0"),
            FakeInsn("cmp", "r3, #2"),
            FakeInsn("bgt", "#0x20"),
            FakeInsn("bx", "lr"),
        ]
        self.assertTrue(branch_on_result(insns))

    def test_last_call_only_used_to_pass(self):
        # the pre-fix implementation looked only after the last call; this shape
        # (branch on the FIRST call's result) must now fail.
        insns = [
            FakeInsn("bl", "#0x21ff0bc"),
            FakeInsn("cmp", "r0, #3"),
            FakeInsn("beq", "#0x40"),
            FakeInsn("bl", "#0x2202e50"),
            FakeInsn("bx", "lr"),
        ]
        self.assertTrue(branch_on_result(insns))

    def test_clean_call_is_not_flagged(self):
        insns = [
            FakeInsn("bl", "#0x21f2390"),
            FakeInsn("ldr", "r0, [pc, #0x10]"),
            FakeInsn("bl", "#0x21f52cc"),
            FakeInsn("pop", "{r3, pc}"),
        ]
        self.assertFalse(branch_on_result(insns))

    def test_real_family_0x21fd0a4_now_fails(self):
        root = Path(__file__).resolve().parent.parent
        ledger = root / "ledger/functions.jsonl"
        image = root / "extract/arm9_overlays/ov006.bin"
        if not ledger.is_file() or not image.is_file():
            self.skipTest("repo data not present")
        from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
        import json
        cfg = json.loads((root / "config/source_units.json").read_text(encoding="utf-8-sig"))
        base = int(cfg["modules"]["ov006"]["loadAddressBase"], 0)
        blob = image.read_bytes()
        row = None
        for line in ledger.read_text(encoding="utf-8").splitlines():
            candidate = json.loads(line)
            if int(candidate["address"], 16) == 0x21FD0A4:
                row = candidate
                break
        self.assertIsNotNone(row)
        md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
        addr = 0x21FD0A4
        insns = list(md.disasm(blob[addr - base:addr - base + row["bytes"]], addr))
        result = harvest_filter.analyse(insns, blob, base)
        self.assertIn("rule1 branch on call result", result["reasons"])


if __name__ == "__main__":
    unittest.main()
