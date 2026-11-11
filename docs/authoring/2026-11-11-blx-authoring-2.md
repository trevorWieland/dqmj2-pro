# BLX authoring, batch 2: twelve more ov006 Thumb rows

Status: authored and verified 2026-11-11. Second batch of source for the
**268 BLX-reachable rows** measured in
[Thumb branch mode](2026-11-11-blx-mode-fix.md), after
[batch 1](2026-11-11-blx-authoring-1.md). Branch mode is not the blocker for
these rows any more; they need source.

## Selection

`build/blx-rescreen.json` (regenerated with
`ops/blx_rescreen.py --root . --candidates "../permuter-candidates/**/*.c"
--candidates "../tu-grouping/parked/*.c"`) still lists 165 ov006
`needs-source-blx-reachable` rows. Excluded before authoring:

* the nineteen rows of `src/ov006/p6_ov006_blx_auth` (batch 1) and the four of
  `src/ov006/p5_ov006_blx_mode` (the mode-fix packet);
* the four rows batch 1 documented as parked: `021EF078` (allocation),
  `021F27D4`, `021EDA50`, `02202A48` (mechanism);
* everything `ops/check_duplicate.py` flags. It reports **0 already defined**
  for all seventeen addresses attempted here (only *mentions* of the same
  addresses in older `src/runtime` drafts).

Seventeen candidates were taken smallest-first (52-72 B); twelve reached exact.

## Rows shipped

One file per function in `src/ov006/p7_ov006_blx_auth2/`, compiled under the
p004 profile (module ov006, mode thumb) via the source-unit rule added for that
directory in `config/source_units.json`.

| address | bytes | shape | ARM calls |
| --- | --- | --- | --- |
| `021FED84` | 52 | allocate resource 0x6F8, program the block at +0x4F8, release | 2 |
| `021FFE28` | 52 | reset the shared 0x600 block twice through two ARM helpers, notify | 2 |
| `02204330` | 52 | rebuild the shared 0x800 page block, then clear both 0x400 halves | 3 |
| `021F8B00` | 60 | "scroll pending": scale the mode, write BG0/BG1 VOFFS, clear the flag | 1 |
| `021FE544` | 60 | release the shared 0x608 block: clear the payload twice, drop the flag | 2 |
| `021FEBC4` | 60 | count how many of twenty 0x2A-byte records match a six-byte pattern | 1 |
| `022009C8` | 60 | raise the scene brightness level, hand the fade-out callback on | 1 |
| `02202A0C` | 60 | map a display-state selector to an answer code, reprogramming | 2 |
| `021F2AD4` | 64 | resolve a table entry into a handle, copy 0xC0, arm the frame callback | 1 |
| `021FE49C` | 64 | allocate the shared block, copy 0x600 in, arm the release callback | 1 |
| `02200598` | 64 | lower the scene brightness level, hand the fade-in callback on at -12 | 1 |
| `02200DF0` | 64 | probe every set bit of the 16-bit active-slot mask | 1 |

Twelve functions, 712 bytes. Each file states what the function does and what
remains unknown (callee semantics, data-field names, constants' meaning).

## Verification

`python ops/verify_blx_authoring_2.py` recompiles every unit with the real
source-unit rule and the pinned mwccarm, patches the object's relocations with
the mode-aware `TargetModes` rule, and requires, per row:

* the patched text is byte-identical to the measured extent;
* the object's relocation table is exactly the pinned one — same offsets, same
  kinds, same externals — so a match cannot come from a literal that happens to
  equal an address;
* at least one `R_ARM_THM_CALL` resolves to an ARM target, that site is a Thumb
  call in the image, and its second halfword is a BLX immediate;
* every `R_ARM_ABS32` target has mode evidence in the ledger and its addend is
  0 or 1 (1 = Thumb-tagged address);
* the old placeholder-mode patcher is **not** exact, and every byte it gets
  wrong lies in the second halfword of one of those ARM call sites;
* one whole-C negative control per function compiles and fails at the pinned
  offsets.

Current result: twelve exact, twelve controls failed as expected, twelve old
patcher diffs confined to ARM call halfwords. Run `--pin` to reprint the
relocation/control table rather than trusting this paragraph.

`python public_tools/source_units.py --root . --check` stays at unresolved 0
with the new `src/ov006/p7_ov006_blx_auth2/**` rule (14,781 resolved files,
1,566 in ov006).

### One recurring finding: a Thumb function pointer needs an addend

Three rows pass a Thumb callback address to the overlay that has to be
Thumb-tagged in the image word (`02200598`, `022009c8`, `021F2AD4` and
`021FE49C` — four call sites). mwccarm will not fold that bit from a function
designator: `(void *)native_ov006_02200a04` produces addend 0 and
`(u32)fn + 1` produces an `adds r1, #1` instruction. Declaring the address as
data and adding one *does* fold:

```c
extern u8 native_ov006_02200a04[];          /* not a function prototype */
native_ov006_02204970(arg, (void *)(native_ov006_02200a04 + 1));
```

That emits `R_ARM_ABS32` against `native_ov006_02200a04` with addend 1, which
patches to the image word. The relocation still names the function's own
address, so the identity check above stays meaningful.

## Not shipped

| address | bytes | reason |
| --- | --- | --- |
| `021EF0A0` | 56 | exact size, 14 bytes off: the cursor lands in r3 with `push {r4,lr}`, the image keeps it in r5 with `push {r3,r4,r5,lr}`. Two hand forms (nested if/else, both senses of the compare) did not move the allocation; `ops/permuter_candidates.py` reports `textdiff=29`, so it is not in the permuter's near-miss class either. Parked as an allocation-form mismatch. |
| `021EDFAC` | 56 | the image keeps a loop skeleton whose trip flag is cleared unconditionally in the body (`movs r0,#0` … `cmp r0,#0; bne`), so the poll runs once. Every equivalent source form (`do/while (0)`, a trip-flag `while`, `for (i < 1)`) is folded by -O4 into straight-line code 8-12 bytes shorter. Mechanism not understood well enough to claim a match; parked. |
| `02203114` | 52 | exact size, 4 bytes off (the count value sits in r1 where the image uses r2). Permuter: no exact candidate, see below. |
| `021FEC00` | 68 | exact size, 3 bytes off (the switch value in r0 where the image uses r1). Permuter: no exact candidate, see below. |
| `0220134C` | 72 | exact size, 7 bytes off (the state pointer and the 0x13C0 constant swap registers). Permuter: no exact candidate, see below. |

## Permuter rows

Four exact-size near misses were measured against the project's own readiness
tool before any run, and the tool says none of them is permuter work. The four
are the "Not shipped" rows above; they are deliberately absent from `src/`, so
this command prints nothing for the lane as merged — it was run while their
drafts were still in it, and each draft survives as the `base.c` of its permuter
workspace:

```
python ops/permuter_candidates.py --module ov006 --under src/ov006/p7_ov006_blx_auth2
  permuter-ready rows (0)
  exact-size but a large normalized diff (4) -- byte score is small, instruction
  stream is not: not a near miss
  0x021ef0a0    56    14 textdiff=29   ...
  0x021fec00    68     3 textdiff=21   ...
  0x0220134c    72     7 textdiff=37   ...
  0x02203114    52     4 textdiff=24   ...
```

Those rows *look* like allocation rows byte-wise (3-7 bytes, identical size,
identical instruction shape) but the normalized instruction-row diff is 21-37
against a threshold of 3, i.e. `docs/authoring/permuter.md` §8's "large
normalized diff" bucket: the byte score is the misleading number there, not the
normalized one. The three rows with the smallest byte diffs were run anyway, to
measure rather than assume, two bounded runs each on a workspace built from the
same source (`ops/permuter.py build`, `probe` clean; the permuter pin and the
pinned 2.0/base mwccarm in every `row.json`). Those workspaces predate the
`--rule` build on `main`, which now copies a source's quoted-include closure, so
`context.h` was copied into each one by hand — with the current tool the same
workspace is `build --rule` and needs no manual copy:

| row | budget | permutations | base score | best score | `verify_permuter.py` |
| --- | --- | --- | --- | --- | --- |
| `02203114` | 240 s | 419 | 930 | 920 | FAIL, 4 B — unchanged |
| `02203114` | 900 s | 1,647 | 930 | 920 | FAIL, 4 B — unchanged |
| `021FEC00` | 240 s | 411 | 1,215 | 1,125 | FAIL, (38, 4) at 64 B — worse |
| `021FEC00` | 900 s | 1,713 | 1,215 | 1,125 | FAIL, (38, 4) at 64 B — worse |
| `0220134C` | 240 s | 398 | 1,260 | none | no output |
| `0220134C` | 900 s | 1,543 | 1,260 | 1,090 | FAIL, (68, 4) at 76 B — worse |

Zero rows reached score 0; zero rows passed the gate (6,131 permutations,
3,422 s of search). Two rows' scores fell while their bytes got worse — the best
candidate's text came out 4 bytes *under* the row's own size for `021FEC00` and
4 bytes *over* for `0220134C`, each with its relocation table changed, which is
the sharpest local illustration of why `docs/authoring/permuter.md` §5 says
score 0 is not acceptance and why §8 asks for the normalized diff first. The
remaining work on these three rows is a source-form decision about which value
mwcc keeps in a callee-saved register, not a search.

## Reproduce

```
python ops/blx_rescreen.py --root . --candidates "../permuter-candidates/**/*.c" \
    --candidates "../tu-grouping/parked/*.c" --json build/blx-rescreen.json
python ops/verify_blx_authoring_2.py
python ops/verify_blx_authoring_2.py --pin        # reprint the pinned table
python public_tools/source_units.py --root . --check
python ops/check_duplicate.py --root . --address 0x21fed84   # one per authored address
```

The verification needs a private checkout with `manifest.json`, `extract/` and
the pinned toolchain, like the other `ops/` tools.
