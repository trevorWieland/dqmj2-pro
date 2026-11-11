# ops/

Private-side operating tools. Everything here may read the private inputs
(`ledger/`, `manifest.json`, `extract/`, `inputs/`), so these scripts are not part
of `public_tools/` and are not run by CI's public build.

## `symbol_map.py` — generated symbol map (deliverable D1)

Emits the canonical address → symbol map from the address ledger.

```bash
python ops/symbol_map.py --root <private-checkout>            # write the map
python ops/symbol_map.py --root <private-checkout> --check    # verify naming only
```

Outputs (generated, **never committed**; default `build/symbol-map/`):

| file | contents |
| --- | --- |
| `symbols.txt` | one line per symbol: `<address> <size> <module> <mode> <name>` |
| `symbols.json` | the same rows plus `processor`, `source`, `nameSource`, `accepted` |

Rows are sorted by module then numeric address, so the output depends only on the
inputs. It reads `ledger/functions.jsonl` (one row per measured function) and
`manifest.json` (the module inventory); `--root` defaults to the current directory.

### Name resolution

The ledger symbol is used when it is a real name. When it is the
`func_XXXXXXXX` placeholder the name comes from, in order:

| `nameSource` | rule |
| --- | --- |
| `ledger` | the ledger already carries a real symbol |
| `source` | a function definition in the row's `sourceUnit` whose identifier contains the address, the only definition in that file, or the file stem when it encodes the address |
| `dependency` | another ledger row's relocation targets this address with a real symbol name (call sites name their callee) |
| `definition-order` | the row's file has exactly as many unclaimed definitions as unclaimed rows: paired in address order with definition order |
| `unresolved` | none of the above — kept at the address-derived ledger symbol |

Rows that stay unresolved are emitted with an **address-derived name** (the ledger's
`func_XXXXXXXX`, or the module-qualified `func_<module>_XXXXXXXX` for arm7 rows that
have no source at all) and `nameSource: "address-fallback"`, so a consumer can always
see which names were not resolved from evidence.

`--check` verifies naming only and writes nothing. It exits non-zero when an accepted
row (`states.functionMatched`) is unresolved. `--allow-unresolved [N]` relaxes that to
a ceiling: with the flag alone `N` is the documented baseline
(`UNRESOLVED_BASELINE = 151`), so CI gates on "no new unresolved rows" instead of
absolute zero; `--allow-unresolved 0` restores the strict check and a larger `N`
lowers the bar further.

Measured on the current private ledger: 16,073 rows over 18 modules, 11,660
accepted, with 9,485 names from the ledger, 5,102 from source definitions, 193 from
relocation evidence, 85 from definition order, and 1,208 rows on
`address-fallback`, of which 151 are accepted.

The 151 accepted residual is deliberate and must not be papered over with invented
names: each is a main-module function whose source defines a semantic name that
neither carries the address nor appears as any taken relocation target, and whose
file does not have a row-count to definition-count match that would allow an
unambiguous pairing. The only evidence that could name them — the original object
symbol tables (`row['object']`) and the match reports (`evidence/matches/*.json`) —
was pruned from the private tree, so recovering them needs either a re-run of the
link that produced them or a decision to accept the address-derived names. Until
then `--check --allow-unresolved` passes at the baseline and fails if the count
grows. The text map is stable across runs.

## `permute.py` — deterministic allocation-form permuter

Hand-matching stalls on one class of row: the C is reachable and compiles to the
exact ledger size, but mwcc `-O2` picks a different register, stack slot or branch
form. `permute.py` searches that shape space and accepts exactly one outcome:
byte-and-relocation exactness against the overlay image.

```bash
python ops/permute.py --candidate ops/candidates/ov001_021d8fa4.json
python ops/permute.py --module ov001 --address 0x021d8ff8 --size 120 \
    --symbol native_ov001_021d8ff8 --source work/p2/cd/f8ff8.c --budget 60
```

A candidate is a JSON file with `module`, `address`, `size`, `symbol` and `source`
(see `ops/candidates/`). No target bytes are stored: the expected bytes are read
from the overlay image at run time, so candidates carry no evidence artifact. The
compile and comparison path is the same one the packet verifiers use
(`work/p2/check.py`), so a hit is a real hit.

### Mutation set (deterministic order, then seeded composition)

| # | shape | why it matters here |
| --- | --- | --- |
| 1 | swap adjacent local declarations | flips register assignment order |
| 2 | hoist a local to the top of its block | changes live-range start |
| 3 | signedness flip (`s32` <-> `u32`, ...) | `bgt` vs `bhi`, sign-extension shape |
| 4 | `p[i]` <-> `*(p + i)` | index vs pointer addressing |
| 5 | hex literal <-> named local | a literal is folded, a local is not (reciprocal multiply) |
| 6 | swap `return 0` / `return 1` | if-conversion order of the two predicated moves |
| 7 | swap any two declarations | the allocator does not always follow textual order |
| 8 | split an inline call result into a local | produces the `mov r3, r0; cmp r3` tail shape |

After the single-step list, a seeded composition pass combines pairs of shapes
(`--seed`, default 0), which is the part of the space a hand search cannot reach
while staying reproducible.

`decomp-permuter` is vendored at
`tools/decomp-permuter-8556c81d80d1c1af98a858c8f4dc951357f29139` (pinned commit
`8556c81d80d1c1af98a858c8f4dc951357f29139`) and is the intended engine once the
search needs AST-level and randomised mutations; the loop here is the
deterministic subset that runs inside the packet harness with no extra state.

### Structural edits and hill climbing

The second layer rewrites a single statement's expression tree and keeps the
semantics fixed: split a condition operand into a named temporary, split an
addition operand into a temporary, reorder commutative operands, swap the sides of
a comparison, and insert an `(s32)` / `(u32)` cast around a condition operand.
These are the shapes that produce the `mov r3, r0; cmp r3, ...` tail and the
register-role swaps the hand search kept hitting.

Near-misses are scored (differing bytes plus length delta, compile failure worst)
and the best `--beam` texts are expanded again, so the search climbs instead of
restarting from the original every time. Exactness remains the only success
condition; the score only steers.

### Proof rows (40 s budget each, 2.0/base, seed 0, beam 4)

| row | bytes | mutants | wall time | diff start -> best | exact |
| --- | --- | --- | --- | --- | --- |
| `ov001 0x021d8ff8` | 120 | 581 | 40.1 s | 18 -> 18 | no |
| `ov001 0x021d8f08` | 128 | 555 | 40.0 s | 20 -> 20 | no |
| `ov001 0x021d8fa4` | 84 | 125 | 8.5 s | 14 -> 14 | no |

No row improved its diff and none reached exactness. The trajectory column is the
important number: the search is exploring, but the diff is flat, which says the
mutation set is the bottleneck rather than the scoring or the beam width. The
next step for this lane is richer structural edits (temporary introduction across
multi-statement spans, statement reordering inside a block), not a wider beam.

### Second corpus (Thumb, module `main`)

`C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\work\permuter-candidates\`
holds seven Thumb near-misses (56-68 B) with their own `README.md` and shared
`context.h`. `load_module('main')` points the comparison at
`extract/arm9/arm9.bin` with base `0x02000000` and inserts `-thumb` **before** `-c`
(appending it after `-c` silently fails the compile — that cost an hour).

The corpus is **not runnable yet**, and the remaining blocker is precise: Thumb
code relocates calls with `R_ARM_THM_CALL` (ELF type 10), which `check.relocate`
does not patch — it handles `R_ARM_PC24` (1) and `R_ARM_ABS32` (2) only, so a
Thumb row now gets past compile and image selection and then raises
`unsupported relocation type 10`. The encoder needed is the 32-bit Thumb `bl`:
split `delta = target - (place + 4)` into `S`, `J1`, `J2` and `imm11` across the
two halfwords (`11110 S imm10` / `11 J1 1 J2 imm11`). That is a ~15-line addition
to `check.relocate` with the formula above, and it unblocks all seven rows.

### Follow-up that changes the lane: compiler identity is confirmed per module

A separate audit (10 accepted 2.0/base functions per module, recompiled on all 24
installed mwccarm builds with each row's own flags) shows `2.0/base` is the best
match in every module:

| module | 1.2 (5 builds) | 2.0 (10 builds) | dsi (9 builds) |
| --- | --- | --- | --- |
| main | 4-5 | **8** | 4 |
| ov000 | 5-6 | **10** | 6 |
| ov001 | 3 | **10** | 6 |
| itcm | 0 | **5** | 2 |
| arm7-main | 1 | **8** | 4 |
| arm7-wram | 3 | **9** | 5 |

One row is a genuine anomaly: `main 0x02000d0c` (192 B) matches **only** on
`1.2/sp3` and `1.2/sp4`, never on any 2.0 build. Everything else either matches
2.0/base or matches no build at all (itcm 5 rows, arm7 3 rows, main 1), which
points at flags or missing asm units rather than a different compiler generation.
So the "some modules were built by an older MWCC" hypothesis is **not** supported,
with that one main-module exception worth a follow-up.

### Mechanism findings this lane produced

These are recorded here because they are the reusable part of the work:

1. `0x0202a954` takes **five** arguments; the fifth is a literal zero on the
   stack, which is why the name buffer sits at `sp + 4` in both ov001 loaders.
   A four-argument call is 4 bytes short and moves the buffer to `sp + 0`.
2. `0x0202a8e0` is the ov001 size probe and its result must be held in a `u32`:
   an `s32` comparison emits `bgt` where the overlay has `bhi`.
3. The ov001 name tables copy **7** and **9** byte-pairs (0x0222d9b6 and
   0x0222d9c4); the trailing character of the longer one is copied separately.
   mwcc rotates the do-while decrement in front of the body, so the counters are
   7 and 8 in source order.
4. The recorded-flag bitmap is byte indexed — `index / 8` for the byte and
   `index % 8` for the bit — and the divisor is proved by the signed-division
   bias shift (`ror #29`, not `#27`).
5. **Negative result:** do not extend the dsi/1.6sp2 compiler override to the
   0x021fexxx sound cluster. It merges the three identical release blocks into a
   loop (92 B against the original's unrolled 120 B), so 2.0/base is correct
   there even though the field-load idiom differs.
