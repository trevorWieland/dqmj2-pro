# Thumb branch mode: resolve the target, never the placeholder

Status: fixed and re-measured 2026-11-11. The bug was a comparison-pipeline
artifact, not a compiler mismatch. A Thumb branch's instruction set must be
resolved from the **target**, never assumed from the bytes the compiler left at
the call site.

## 1. The bug

mwccarm emits one `R_ARM_THM_CALL` for both a Thumb `BL` and an ARM `BLX`. The
object always contains the `BL` placeholder (`F8xx` second halfword). The
linker — or a relocation patcher standing in for it — chooses `BL` or `BLX` from
the callee's mode.

`ops/form_search.py:relocate` read the mode from the **candidate object**:

```python
marker = int.from_bytes(text[offset + 2:offset + 4], 'little')
arm = (marker & 0xF800) == 0xE800 if kind == 10 else False
```

The placeholder is always `0xF800`-class, so `arm` was always false. Every
Thumb call to an ARM function was patched as `BL`, and the row scored a phantom
2-byte mismatch at the second halfword. `ops/compiler_matrix.py` and
`ops/link_compare.py` called the same patcher; the public
`public_tools/repo_build.py` path already carried a partial target-aware rule,
but its BLX marker test also missed `J1 == 0` sites (`0xC8xx`).

## 2. The evidence

`ops/link_compare.py` on branch `codex/compiler-source-test` (963883e2)
encoded the same relocation both ways:

| row | call site | target | image | `arm=False` (old) | `arm=True` (fix) |
| --- | --- | --- | --- | --- | --- |
| `0x021FB384` | `+0xA` | `0x02002480` ARM | `07 F6 78 E8` | `07 F6 77 F8` | `07 F6 78 E8` |
| `0x021FF02C` | `+0x1A` | `0x0200616C` ARM | `07 F6 92 E8` | `07 F6 91 F8` | `07 F6 92 E8` |
| `0x02203EBC` | — | Thumb row | (no call) | 1-byte mask-idiom diff | same 1-byte diff |

`0x02203EBC` is the negative control: its target is Thumb and a `BLX` there
would be wrong. The two remaining rows are byte-exact once the second halfword
and the BLX base are correct.

The two encodings differ in two ways:

* base: `BL` is relative to `PC + 4`; `BLX` is relative to `Align(PC + 4, 4)`;
* marker: `BL` leaves second-halfword bit 12 set (`F8xx`); `BLX` clears it
  (`E8xx` when `J1 == 1`, `C8xx` when `J1 == 0`).

`0xE800` is therefore not a reliable marker test. The discriminating test is
`(second & 0xD000) == 0xC000`.

## 3. The fix

One rule, applied in every patcher:

1. an explicit caller hint (`arm=True/False`) wins;
2. the ledger row at the target address (`mode`);
3. a ledger extent containing the target (mid-function ARM entry);
4. the ledger row for the target symbol;
5. the target module's mode when every ledger row in it agrees;
6. the existing accepted source file's mode (`config/source_units.json`
   profile, `-thumb` or not);
7. no evidence: fall back to `BL`, and say so.

BLX is encoded with base `Align(PC + 4, 4)`; BL with base `PC + 4`. The
compiler's `-4` addend is applied once, as before.

Changed:

* `ops/thumb_branch.py` — architectural `is_blx`/`marker_mode`, `mode=` override;
* `ops/form_search.py` — `TargetModes` evidence resolver; `relocate(..., modes=)`;
* `ops/compiler_matrix.py`, `ops/link_compare.py` — pass the resolver;
* `public_tools/repo_build.py` — ledger-row-first `target_mode`, module-mode
  fallback, bit-12 BLX decode;
* `ops/test_form_search.py` (new), `ops/test_thumb_branch.py`,
  `public_tools/test_thumb_branches.py` — pinned rows and negative controls.

## 4. Re-measurement

Screening set: 629 unmatched arm9 Thumb rows in ov006 + main. **274 (43.6%)**
contain a BLX immediate: 168 ov006, 106 main, 1,068 sites, 179 distinct ARM
targets. Every one of those targets now resolves; zero are unresolved.

| classification (274 BLX rows) | rows |
| --- | --- |
| exact after the fix (all were a 2-byte miss) | 4 |
| compiled best-known source, still a shape mismatch | 2 |
| no best-known source, BLX-reachable | 268 |
| BLX target unresolved | 0 |

The other 355 of the 629 rows contain no BLX and are outside this blocker.
Of the 6 BLX rows that already had a candidate source, 4 became exact and 2
improved but did not match: `0208BA68` 44 -> 42 differing bytes and `02094208`
26 -> 25. Nothing regressed.

The fix cannot create source. What it proves is narrower and useful: for 268
rows the branch encoding was the only *measured* blocker we could remove
without a source, and for 4 rows an existing form was already correct. TU
grouping is not an axis for the remainder: independently confirmed on 2,147 of
2,147 Thumb rows, every pc-literal lies inside its own extent, MWCC does not
inline ordinary callees, and compiling a TU alone equals compiling it in a
group. The remaining work on those rows is the ordinary form search.

## 5. Shipped

Four ordinary C files in `src/ov006/p5_ov006_blx_mode/`, one per function:

* `0x021FB384` (24 B), call `+0xA` -> ARM `0x02002480`, BLX `07 F6 78 E8`;
* `0x021FF02C` (48 B), call `+0x1A` -> ARM `0x0200616C`, BLX `07 F6 92 E8`;
* `0x021FF05C` (48 B), same call, BLX `07 F6 7A E8`;
* `0x021FF08C` (48 B), same call, BLX `07 F6 62 E8`.

All four are byte-exact under the real `config/source_units.json` rule
(`src/ov006/p5_ov006_blx_mode/**`, profile p004, module ov006, mode thumb) and
have one whole-C negative control each. `python ops/verify_blx_mode_fix.py`
prints the pass/fail table; `ops/check_duplicate.py` reported all four clear
before authoring.

## 6. Reproduce

```
python ops/link_compare.py --module ov006 --rows ops/compiler_specs/rows.json \
    --names 02203ebc,021fb384,021ff02c
python ops/blx_rescreen.py --candidates "work/tu-grouping/parked/*.c" \
    --candidates "work/permuter-candidates/**/*.c" --json build/blx-rescreen.json
python ops/verify_blx_mode_fix.py
python -m unittest ops.test_form_search ops.test_thumb_branch \
    public_tools.test_thumb_branches
```

Historical context: [Thumb BLX-immediate blocker](../platform/thumb-blx.md)
recorded the relocation-rule hypothesis on 179 rows. This note replaces its
"recommended next step" with the implemented rule and the 274-row measurement.

Follow-up: the ledger evidence in this note was not module-scoped. A
base-colliding host row could win over the child image (ten
`utility-child-arm7-wram` rows). The resolver now reads the measured call site
first and scopes the ledger fallback to the containing module; see
`docs/authoring/2026-11-11-scanner-module-mode.md`.
