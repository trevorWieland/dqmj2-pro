# BLX reachability: nineteen authored ov006 Thumb rows

Status: authored and verified 2026-11-11. This packet is the first batch of source
for the **268 BLX-reachable rows** measured in
[Thumb branch mode](2026-11-11-blx-mode-fix.md): unmatched arm9 Thumb functions in
ov006/main that contain an immediate BLX and previously could not match because the
comparison pipeline always patched `R_ARM_THM_CALL` as a Thumb `BL`.

Branch mode is no longer a blocker for these rows; they need source. This packet
supplies nineteen of them, smallest-first, all in ov006.

## Selection

`build/blx-rescreen.json` lists the 268 `needs-source-blx-reachable` rows (164
ov006, 104 main) with their measured sizes. Candidates were taken from the smallest
end of that list (28-52 bytes) so each form is small enough to recover exactly.
Every address was checked with `ops/check_duplicate.py --address` before authoring
(all clear, no definition under `src/`).

## Rows shipped

One file per function in `src/ov006/p6_ov006_blx_auth/`, compiled under the p004
profile (module ov006, mode thumb) via the source-unit rule for that directory.

| address | bytes | shape | ARM calls |
| --- | --- | --- | --- |
| `021EF050` | 40 | guarded buffer flush through a table callback | 2 |
| `02204268` | 34 | remove a node from the global list under a lock | 2 |
| `0220428C` | 30 | append a node at the list tail under a lock | 2 |
| `021F1EF0` | 28 | 64-bit value shifted by six, dispatched to a helper | 2 |
| `021F2B3C` | 40 | clear/release the shared 0xC0-byte buffer | 2 |
| `021FEA78` | 40 | poll a main-side state slot until 0x8000, then dispatch | 1 |
| `021FFF6C` | 40 | classify a fixed record against a byte pattern | 1 |
| `02203C4C` | 40 | store a non-zero value into the main slot under a lock | 3 |
| `021FEE00` | 40 | copy a 0x20-byte record and clear its status byte | 1 |
| `021FF440` | 40 | reset a record payload and stamp its status byte | 1 |
| `022041F0` | 40 | mask interrupts, shut the descriptor down | 2 |
| `021FEFD4` | 44 | render the record at base+0x4C0 | 1 |
| `02203720` | 44 | forward six arguments with a row-selected table pointer | 1 |
| `02203B94` | 44 | clear + allocate 0x40000 bytes, fail loudly | 3 |
| `02203C20` | 44 | release the main slot for a handle under a lock | 3 |
| `02203148` | 48 | allocate a palette entry, program both engines | 2 |
| `02203BD8` | 48 | allocate under a lock, fail loudly, return the result | 4 |
| `022026A8` | 48 | reset a 0x100-byte buffer pair and self-pointer | 2 |
| `021FE510` | 52 | copy `count` 0x40-byte records from a table | 1 |

Nineteen functions, 784 bytes. Each file states what the function does and what
remains unknown (callee semantics, data-field names, constants' meaning).

## Verification

`python ops/verify_blx_authoring_1.py` recompiles every unit with the real
source-unit rule and the pinned mwccarm, patches the object's relocations with the
mode-aware `TargetModes` rule, and requires, per row:

* the patched text is byte-identical to the measured extent;
* at least one `R_ARM_THM_CALL` resolves to an ARM target, and the image word at
  that site is a BLX immediate (`(second & 0xD000) == 0xC000`);
* the old placeholder-mode patcher is **not** exact, and every byte it gets wrong
  lies in the second halfword of one of those ARM call sites;
* one whole-C negative control compiles and fails at the recorded offsets.

Current result: nineteen exact, nineteen controls failed as expected. The
verification needs a private checkout with `manifest.json`, `extract/` and the
pinned toolchain, like the other `ops/` tools.

`python public_tools/source_units.py --root . --check` stays at unresolved 0 with
the new `src/ov006/p6_ov006_blx_auth/**` rule.

## Not shipped

* `021EF078` (40 B, two ARM calls) compiles to the exact size but stays fifteen
  bytes off: mwcc puts the four-entry table pointer in r1 and stores the loop
  index directly, while the image uses r3 for the table and a copied value in r1.
  Six loop/pointer/while forms were searched through `ops/form_search`-style
  enumeration; none moved the allocation. Parked as an allocation-form mismatch.
* `021F27D4`, `021EDA50`, `02202A48` were decoded but not written: the first needs
  a callback plus stack-record form, the second's loop stores zero before reading
  the same byte back (mechanism not understood well enough to claim a match), and
  the third passes three stack arguments plus an uninitialised r3. They remain
  BLX-reachable and need a dedicated form pass.

## Reproduce

```
python ops/verify_blx_authoring_1.py
python public_tools/source_units.py --root . --check
python ops/check_duplicate.py --address 0x21ef050   # one per authored address
```
