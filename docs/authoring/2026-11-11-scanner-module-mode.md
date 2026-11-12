# Scanner measurement: image mode, module scope, reported relocation skips

Status: fixed and re-measured 2026-11-11. Two rules are now part of the measuring
path (`ops/form_search.py`, used by `ops/permuter_candidates.py`,
`ops/compiler_matrix.py` and `ops/link_compare.py`).

## Rule 1 — a target's mode comes from the image, and ledger fallback is module-scoped

`utility-child-arm7-wram` and `arm7-wram` both load at `0x037F8000`. Their images
overlap in address space but not in content: a child Thumb function at
`0x037FF3C4` sits inside host ARM row `0x037FF3AC` (948 B). An address is
therefore not a module identifier.

The old `TargetModes.resolve` checked the caller's exact and extent rows, then
fell back to a **global** address table. A child branch target with no child row
at that exact address matched the host's ARM extent, so `relocate` encoded `BLX`
where the child image has `BL`: a two-byte error per branch. Ten accepted
`utility-child-arm7-wram` rows scored 2-7 and were reported as regressions while
`public_tools/repo_build.py` measured all ten byte-exact (584 B).

The measurement rules, strongest first:

1. **Image at the call site.** Read the instruction from the caller's measured
   module image. In the second halfword, `(value & 0xD000) == 0xC000` is a
   `BLX` immediate (ARM target); otherwise it is a `BL` (Thumb target). This is
   the only module-local record of the original linker's choice.
2. **Module-scoped ledger.** Use it only when the image cannot decide (no image,
   site outside the image, or no Thumb-2 branch prefix). If the target lies in
   the caller's own image, only the caller's ledger rows may describe it; a base
   collision is intra-image by construction. An external target uses the smallest
   module range that contains it. Order: symbol, exact address, containing extent,
   module mode, accepted source rule. A module-qualified symbol name is stronger
   than an address two base-colliding images can share.
3. **No evidence.** Fall back to `BL` and say so. There is no global address table
   that can borrow another module's row.

`repo_build` already behaved this way: its ledger index is per module and its
branch decision reads the original image word. The scanner now shares the rule.

## Rule 2 — a scanner that silently skips a relocation kind must report the skip count

`form_search.relocate` now encodes:

| ELF kind | name | form |
| ---: | --- | --- |
| 1 | `R_ARM_PC24` | ARM `B`/`BL` word |
| 2 | `R_ARM_ABS32` | 32-bit pointer, Thumb bit on function symbols |
| 10 | `R_ARM_THM_CALL` | Thumb `BL` / `BLX` immediate |
| 30 | `R_ARM_THM_JUMP24` | Thumb `B.W` immediate |
| 43 | `R_ARM_MOVW_ABS_NC` | ARM `MOVW` |
| 44 | `R_ARM_MOVT_ABS` | ARM `MOVT` |
| 47 | `R_ARM_THM_MOVW_ABS_NC` | Thumb `MOVW` |
| 48 | `R_ARM_THM_MOVT_ABS` | Thumb `MOVT` |

MOVW/MOVT patch the `imm4:imm12` (ARM) or `imm4:i:imm3:imm8` (Thumb) fields and
leave the condition, register and opcode bits alone. A Thumb function pointer
gets its bit 0 through `MOVW`, exactly as through `ABS32`; `MOVT` takes the high
half and never sets it.

Any other kind raises `form_search.UnsupportedRelocation`. A caller that measures
many units passes `skip_counts=...`; `ops/permuter_candidates.py` records the
counter as `relocationSkips` in its JSON, prints it, and names the kind in the
skipped unit's reason. A skip is now a visible measurement hole, never "no variant
compiled".

`R_ARM_PC24` was the dominant hole: the baseline scan cache had **4,595 units**
failing on kind 1 alone, mostly ARM functions with a direct call. Encoding it
changed **4,261 rows / 539,904 B** from "not exact" to measured. No row in this
census was blocked only by MOVW/MOVT, and the repaired scan reports no remaining
relocation skips; the encodings are pinned by tests so a future profile that
emits them is measured rather than silently dropped.

## Census

Baseline and after are the same tree at `92f727ad3`, the same 12,110 compiled
units, scanned in eight shards. The census is row-level over the 15,308 sized
ledger rows.

| bucket | before rows | before bytes | after rows | after bytes | delta rows | delta bytes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| a exact + matched | 4,856 | 222,010 | 9,098 | 760,934 | +4,242 | +538,924 |
| b exact + unmatched | 103 | 5,384 | 132 | 6,948 | +29 | +1,564 |
| c not-exact + matched | 7,169 | 997,084 | 2,927 | 458,160 | -4,242 | -538,924 |
| d not-exact + unmatched | 3,180 | 906,702 | 3,151 | 905,138 | -29 | -1,564 |

**4,271 rows / 540,488 B** were previously "not exact" and are artifacts:

* **4,261 rows / 539,904 B** were `R_ARM_PC24` skips (kind 1);
* **10 rows / 584 B** were the base-collision BLX rows (`utility-child-arm7-wram`).

No baseline exact row was lost: all 4,959 previously exact rows are still exact.
The new true non-exact count is **6,078 rows / 1,363,298 B**, down from
10,349 rows / 1,903,786 B.

Twenty scanner-exact rows (the ten utility rows plus ten rows the baseline did
not call exact) were re-measured through `public_tools/repo_build.py`:
20/20 exact, 584 B of the ten, zero unresolved relocations. Run
`python ops/verify_scanner_module_fix.py --scan work/census2/after-*.json ...`.


## Reproduce

```
python -m unittest ops.test_form_search -v
python ops/verify_scanner_module_fix.py --scan work/census2/after-*.json \
    --baseline work/census/before-*.json
python ops/permuter_candidates.py --modules all --shard 0/8 \
    --json work/census2/after-0.json
python ops/scanner_census.py --scan work/census2/after-*.json \
    --baseline work/census/before-*.json \
    --out-md work/census2/census.md
```

The baseline is the same tree at `92f727ad3` before the patch, scanned in eight
shards; the after scan uses the same shards and unit set.
