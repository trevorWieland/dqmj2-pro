# BLX authoring, batch 3: seventeen more ov006 Thumb rows

Status: authored and verified 2026-11-11. Third batch of source for the
**BLX-reachable rows** measured in
[Thumb branch mode](2026-11-11-blx-mode-fix.md), after
[batch 1](2026-11-11-blx-authoring-1.md) and
[batch 2](2026-11-11-blx-authoring-2.md). Branch mode is not the blocker for
these rows any more; they need source.

## Selection

`build/blx-rescreen.json` still lists 165 ov006 `needs-source-blx-reachable`
rows (the rescreen predates all three authoring packets). Excluded before
authoring:

* the thirty-five rows already shipped by
  `src/ov006/p5_ov006_blx_mode`, `src/ov006/p6_ov006_blx_auth` and
  `src/ov006/p7_ov006_blx_auth2`;
* the nine parked rows: `021EF078`, `021F27D4`, `021EDA50`, `02202A48`,
  `021EF0A0`, `021EDFAC`, `02203114`, `021FEC00`, `0220134C`;
* everything `ops/check_duplicate.py` flags. It reports **0 already defined**
  for all twenty-three addresses attempted here (only *mentions* of the same
  addresses in older `src/runtime` and `src/overlays` drafts).

The smallest remaining rows after those exclusions start at 68 bytes, so
candidates were taken smallest-first from 76 to 136 bytes. Rows were preferred
when their shape already had an authored sibling, and the sibling was read
first:

* `022041A0` pairs with p6 `022041F0` on the two-word `0221C1A4` descriptor
  (one shuts the subsystem down, this one brings it up);
* `02203644` and `022035D8` reuse the p6 record-release shape over the
  `0221C184` resource state (special record at +0x67C, release handles at
  +0x28/+0x2C, clear buffers at +0x638/+0x668);
* `0220491C` reuses the p6 linked-list shape (`02005D50`/`02005D20` lock pair,
  insert through `0220428C`);
* `021F8050` reuses the p7 `0221C0D8` display-state struct and its
  `02002480`/`020024BC` ARM scale helpers;
* `022019D0` and `02201C84` reuse the p7 `0221C164` mode descriptor and the
  `0x08000000` callback shape;
* `021EDB00` reuses the authored `021EDC50` byte-swap helper and the
  `0220D3DC` network block.

Twenty-three candidates were attempted; seventeen reached exact.

## Rows shipped

One file per function in `src/ov006/p8_ov006_blx_auth3/`, compiled under the
p004 profile (module ov006, mode thumb) via the source-unit rule added for that
directory in `config/source_units.json`. No `context.h` is shared with any
earlier lane.

| address | bytes | shape | ARM calls |
| --- | --- | --- | --- |
| `021EDB00` | 88 | byte-swap three network parameters, start the link, wait for completion | 1 |
| `021F56D8` | 76 | allocate the 0x0C/-4 resource, register three callbacks, fail loudly | 2 |
| `021F6984` | 92 | step the current entry and dispatch its four interleaved columns | 2 |
| `021F8050` | 116 | derive record height, pick palette selector, scale and blit | 1 |
| `021FB474` | 88 | rebuild both background control words when the record is pending | 2 |
| `021FEB5C` | 104 | start the transfer, poll the counter to 2, check completion | 4 |
| `021FE86C` | 100 | re-fade to a target brightness through two setters | 2 |
| `022019D0` | 80 | re-select the mode entry and hand the table to the callback | 1 |
| `02201C84` | 112 | run the mode evaluator and classify its answer | 1 |
| `02201F54` | 104 | queue one frame: latch counter, copy staging block, advance | 2 |
| `022029AC` | 96 | tear the scene down: three helpers, release handle and slot | 5 |
| `022035D8` | 108 | release one resource record with the size that matches it | 4 |
| `02203644` | 76 | release one resource record and clear its buffer | 4 |
| `02204150` | 80 | keep the mode byte in step with bit 15 of 0x027FFFA8 | 2 |
| `022041A0` | 80 | bring the subsystem up opposite to `022041F0` | 6 |
| `022042C4` | 108 | allocate the page block, build both pages, arm the callback | 1 |
| `0220491C` | 84 | allocate a list node and link it before the first greater key | 2 |

Seventeen functions, 1,592 bytes. Each file states what the function does and
what remains unknown (callee semantics, data-field names, constants' meaning).

## Verification

`python ops/verify_blx_authoring_3.py` recompiles every unit with the real
source-unit rule and the pinned mwccarm, patches the object's relocations with
the mode-aware `TargetModes` rule, and requires, per row:

* the patched text is byte-identical to the measured extent;
* the object's relocation table is exactly the pinned one — same offsets, same
  kinds, same externals — so a match cannot come from a literal that happens to
  equal an address;
* at least one `R_ARM_THM_CALL` resolves to an ARM target, that site is a Thumb
  call in the image, and its second halfword is a BLX immediate;
* every `R_ARM_ABS32` slot has addend 0 or 1; a +1 addend (a Thumb-tagged
  function address) must resolve to a Thumb function in the ledger, and a plain
  data address needs no mode evidence (this batch points at nineteen data words
  that have no ledger row);
* the old placeholder-mode patcher is **not** exact, and every byte it gets
  wrong lies in the second halfword of one of those ARM call sites;
* one whole-C negative control per function compiles and fails at the pinned
  offsets.

Current result: seventeen exact, seventeen controls failed as expected, every
old-patcher diff confined to ARM call halfwords. Run `--pin` to reprint the
relocation/control table rather than trusting this paragraph.

`python public_tools/source_units.py --root . --check` stays at unresolved 0
with the new `src/ov006/p8_ov006_blx_auth3/**` rule.

## Addend-1 ABS32 sites

This batch takes six Thumb function addresses as data, and the +1 addend is
what folds the Thumb bit in — the same finding batch 2 documented. The new
lanes use it for the three `021F57CC`/`021F57E0`/`021F57EC` callbacks handed to
`021F1FA8`, the `02204218` callback stored in the `0221C1A4` descriptor, the
`02204330` callback registered with `0220490C`, and the `021FEC00` transfer
registered with the two ARM helpers. Declaring the target as `u8 name[]` and
passing `name + 1` emits `R_ARM_ABS32` with addend 1; the relocation still
names the function's own address, so the identity check above stays meaningful.

## Not shipped

| address | bytes | reason |
| --- | --- | --- |
| `02200C0C` | 96 | exact size, 25 bytes off: the base pointer lands in r0 where the image keeps it in r1 (the image leaves the `(u16)~bit << 16` shift leftover in r0). `ops/permuter_candidates.py` reports score 25 against its default `--max-score 24`, so the row is deliberately outside the near-miss class; not permuter work. Two hand forms (u16 mask, u32 mask with `& 0xFFFF`) compiled identically. Parked as an allocation mismatch. |
| `02202FF0` | 76 | exact size, 20 bytes off: the staging-buffer address is cached in r4, the destination in r5 and the count in r1 where the image uses r6/r7, and the buffer clear is scheduled before the entry's count is read. `permuter_candidates` puts it in the far bucket at `textDiff=35`; two hand forms (struct entry, raw pointer entry) compiled identically. Parked. |
| `0220003C` | 92 | four control-flow forms (switch, if/else chain, early returns, inverted guard). The closest is 92 bytes with 29 bytes off (case-4 body layout), and the inverted guard merges the image's two `021FFF6C` call sites into one (88 bytes). Parked as a control-flow-form mismatch. |
| `021EDCE4` | 112 | 116 bytes: mwcc keeps the three-word buffer address in a callee-saved r5 (`push {r4,r5,lr}` plus copies) where the image pushes only `{r3,r4,lr}` and recomputes `add r0,sp,#0` per call. Two hand forms (u32[3] and u8[12] buffer) compiled identically. Parked. |
| `021F98D0` | 100 | 92 bytes: the buffer address is cached in r4 and the limit moved into an extra callee-saved r5, while the image allocates a four-byte frame with the limit in r4 and recomputes the buffer address. Parked. |
| `021F8800` | 104 | 100 bytes: mwcc derives `first + index` on the fly (three callee-saved registers) where the image materialises an incrementing copy per loop (five callee-saved: `{r3,r4,r5,r6,r7,lr}`). Parked. |

The six parked rows stay `needs-source-blx-reachable`; none has a draft under
`src/`.

## Reproduce

```
python ops/verify_blx_authoring_3.py
python ops/verify_blx_authoring_3.py --pin        # reprint the pinned table
python public_tools/source_units.py --root . --check
python ops/check_duplicate.py --root . --address 0x22041a0   # one per authored address
```

The verification needs a private checkout with `manifest.json`, `extract/` and
the pinned toolchain, like the other `ops/` tools.
