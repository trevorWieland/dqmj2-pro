# Harvest density and the filter's role

Measured with `ops/harvest_filter.py` (PR #134) on ov006 and the untouched modules, 2026-11-11.

| module | band (B) | families with >=2 members | families passing all seven | pass density |
| --- | --- | --- | --- | --- |
| ov006 | 40-80 | 10 | 1 | 10% |
| ov006 | 81-120 | 8 | 1 | 12.5% |
| ov006 | 121-200 | 7 | 0 | 0% |
| main | 40-80 | 2 | 0 | 0% |
| ov000 / ov001 / ov003 | 40-80 | 0 | 0 | n/a (no unmatched rows) |
| **total** | | **27** | **2** | **~7%** |

Rows covered by the two passing families: 288 B + 228 B = 516 B.

## Outcome of authoring the passing set

The two rows of the 81-120 B passing family were attempted first:

- `0x21FB800` (108 B): best source 92/108 — the measured copy of the 4-byte pattern is unrolled
  with two stack pointers and the compare loop reloads the record byte every iteration; the C forms
  tried kept the pattern pointer in a register and fused the copy.
- `0x21FD0A4` (120 B): best source 108/120 — closes, but the measured row forwards the slot through
  an intermediate record and clamps before the final call; the C form emitted two fewer instructions
  around the call.

Both are parked; no source was committed. The 40-80 B passing family (5 rows) was not reached.

## Filter correction this run exposed

`rule1` checks only the *last* call for a reload or branch on its result. `0x21FD0A4` branches on
the result of an earlier call (`bl 0x21ff0bc; cmp r0,#3; beq`), which the filter did not see, so the
family passed. The rule needs to scan every call's result use, not just the last one. Until that is
fixed the filter has a known false-positive class: rows with multiple calls that branch on an
intermediate result.

## Strategy

Pass density is ~7% across 27 multi-member families and 516 B of shape-determined rows. That is too
thin to drive authoring capacity: the filter's real product is the **queue for the permuter lane**,
not a supply of manual packets. It separates families whose bytes are shape-determined (harvestable
by hand) from families whose residual is allocation or expression-idiom choice (need the permuter or
a compiler-model fix). Planning should use it that way: run the filter first, author from PASS, and
send everything else with its reasons to the permuter queue instead of re-scanning bands for bytes.
