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

## `unclaimed.py` — source-first screening (and `--check-addresses` gate)

The ledger's `functionMatched` flag is not a duplicate screen: a source can land in
`src/` before the ledger absorbs it. `unclaimed.py` answers "is this row claimed?" from
the source tree first and the ledger only as a confidence modifier.

```bash
python ops/unclaimed.py --module ov000
python ops/unclaimed.py --all --json work/unclaimed.json
python ops/unclaimed.py --check-addresses 0x021FBB04 main:0x020685bc --address-file work/batch.txt
```

A claim is a **symbol** definition whose identifier encodes the address, an
**address-named source file** (`native_main_020685bc.c`, whatever the symbol inside is
called), or a **data** definition named after the address. Extern declarations,
prototypes, call sites and comments are *mentions*: they lower confidence to `medium`
but never claim a row. Claims are **module-scoped**, because every overlay loads at
`0x021d7240`; `src/ov000/...` cannot claim an `ov004` row at the same address.
`--check-addresses` exits 1 when any address in the batch is already defined, so a
packet build can gate on it.

`python -m unittest ops.test_unclaimed` covers the evidence rules. The measured
correction, bucket counts and ledger hashes are in
[docs/authoring/2026-11-11-unclaimed-tool.md](../docs/authoring/2026-11-11-unclaimed-tool.md).

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

`decomp-permuter` is now driven for real by `ops/permuter.py` (see the section below and
`docs/authoring/permuter.md`); the loop here is the deterministic subset that runs inside
the packet harness with no extra state, and stays the right tool when the row's edit is
one of the eight shapes above.

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

## `form_search_thumb.py` — the three Thumb layout dimensions

`form_search.py` enumerates a literal text grid. The remaining main-module
Thumb rows fail because of three layout dimensions that grid cannot express,
so `form_search_thumb.py` drives one spec file per row through `WRITEBACK`,
`HOIST` and `LOOP`:

```bash
python ops/form_search_thumb.py --spec ops/form_specs/thumb/020b5890.json --time-budget 300
python ops/form_search_thumb.py --rank --json build/thumb-form2/ranked.json
python ops/form_search_thumb.py --spec ... --keep src/main/t1_main_thumb/native_main_020b5890.c
```

The spec is `{address, bytes, module, template, dimensions}`; each dimension
is a list of alternatives or a `{"library": ..., "params": ...}` call into
`writeback_forms`, `hoist_forms` or `loop_forms`. A missing dimension is one
empty alternative — the control that must leave the template byte-identical.
The tool compiles through the resolved `src/main/t1_main_thumb/**` lane rule
(module main, mode thumb, p032, mwccarm 2.0/base), patches relocations with
`form_search.relocate`, scores against the module image and stops at the
per-row time budget.

The batch-4 note (`docs/authoring/2026-11-11-main-thumb-2.md`) records the
measured result: seven rows, 236 bytes, and the finding that the pool-load
difference is argument liveness (a live third argument delays the load past
the store). `ops/test_form_search_thumb.py` pins one observable difference per
dimension and the two controls (absent dimension, equivalent spellings).

## `permuter.py` — real decomp-permuter workspaces, runs and acceptance

The deterministic catalogue above cannot reach "the same instructions with a different
register allocation" when the fix is an AST-level rewrite. `permuter.py` generates a
complete [decomp-permuter] workspace for one ledger address — `base.c`, a `target.o`
built from the module image with its relocation slots zeroed, `compile.sh` with the row's
exact mwccarm flags, and `settings.toml` — runs the search for a bounded time, and hands
the best candidate to `verify_permuter.py`, which is the only thing allowed to accept it.

```bash
git clone https://github.com/simonlindholm/decomp-permuter.git work/decomp-permuter
git -C work/decomp-permuter checkout 8556c81d80d1c1af98a858c8f4dc951357f29139

python ops/permuter.py build --module ov006 --address 0x02203EBC \
    --src ops/compiler_specs/02203ebc.c
python ops/permuter.py probe work/permuter/ov006_02203ebc
python ops/permuter.py run   work/permuter/ov006_02203ebc --timeout 300
python ops/verify_permuter.py work/permuter/ov006_02203ebc --source best.c
```

`build --rule` takes the compiler, flag profile and mode from `config/source_units.json`
for `--src`, which is what the repository build uses; without it the tool falls back to
the ledger row or the processor profile. `ops/permuter_candidates.py` finds the rows
worth running at all: it resolves and compiles every source unit in a module, keeps the
exact-size ones whose difference survives the shim's normal form, and separates the
relocation-only rows (link problem, invisible to the permuter) from ledger-stale rows
(already exact, `ops/reconcile_ledger.py` work).

The permuter is never vendored: it is a pinned clone under `work/` (ignored) or the
pinned import under `tools/` (ignored), and every workspace and receipt records the
commit. `mwcc_objdump.py` is the Capstone `objdump -drz` shim the permuter parses, because
no GNU-style ARM objdump exists in this tree.

**Score 0 is not acceptance.** `verify_permuter.py` recompiles the candidate with the
row's compiler and compares bytes and relocations against the module image, then requires
two negative controls (the base source must fail; the shifted slices must fail) and
relocation identity with the base object. Worked example, the build-selection trap, and
the honest limits are in [`docs/authoring/permuter.md`](../docs/authoring/permuter.md).

[decomp-permuter]: https://github.com/simonlindholm/decomp-permuter

## `accessor_pool.py` — pool-cluster measurement (and its negative result)

Measures whether a module's ready rows cluster by **pool word**, and emits an
ordered worklist (no-call rows first, then 3+ cluster members, then ascending size).

```bash
python ops/screen_candidates.py --module ov006 --json build/screen/ov006.json
python ops/accessor_pool.py --module ov006
```

**Measured conclusion, 2026-11: pool-word clustering does not predict tractability,
and the lane should not be re-opened on that basis.** On ov006 (570 ready rows, 450
Thumb analysed, 763 distinct pool words, 123 clusters of three or more) the busiest
words are memory-mapped registers (`0x04001008` x35, `0x04000008` x26,
`0x01ff0000` x21) that every row touches. A row joins a cluster because it reads the
same hardware, not because its C resembles its cluster-mates', so cluster membership
carries no authoring information: four cluster rows were attempted and none matched
(`0x02203EBC`, `0x02203EEC`, `0x02203F1C` at 48/48 with one halfword off; `0x021F6BCC`
at 60/60 with one register off), while grouping by **body shape** in the 40-80 B band
gives 11 families over 31 rows and a 75% first-try rate on the family template.
Group by body, not by pool word.

## Parked: ov006 `0x021F4C80` quartet (deliberate template design)

The four rows `0x021F4C80`, `0x021F4CC4`, `0x021F4D08`, `0x021F4D4C` (68 B each) are
a call chain: each member reads `*(0x0221C060) + 0x34`, extracts a channel field and
an offset, calls `0x021F4944(3, offset)` and, when `offset >= 0xC0`, calls
`0x02204970(arg, <next member>|1)` with the next member's address as a Thumb function
pointer (`0x021F4CC5`, `0x021F4D09`, `0x021F4D4D`, `0x021F4D91`).

**Status: parked.** The leader does not converge; four source forms were tried and the
closest is 64 of 68 bytes with the first difference at byte 0. The blocker is
**allocation, not mechanism** — the record read, the mask shift and the two calls are
all understood; what the source cannot express is the original's combination of a
volatile-like dead store of the channel field (`str r0, [sp, #4]`, never read) with the
offset kept in a register and spilled around the first call:

```
image: 10b5 82b0 041c 0c48 0068 406b 0168 0b48 0840 000c 0190 0806 010e 0091 0c31 0091 0320 ...
form : 10b5 82b0 041c 0e48 0068 0068 406b 0168 0c48 0840 000c 0190 0806 000e 0090 0098 ...
                                            ^^^^ extra load                    ^^^^^^^^^^ volatile offset
```

Forms tried: a stack struct with two fields (mwcc promotes and drops the dead store);
a pointer to that struct (72 B); `volatile` on the channel only (64 B, closest); and
`volatile` on both fields (76 B, frame right but the offset gains a load/store pair).
The image's `ldr r0,[pool] / ldr r0,[r0] / ldr r0,[r0,#0x34]` chain is also emitted as
`ldr / ldr / ldr #0x34` by every form here, one load longer than the image's two.

A future pass should start from the frame shape (`push {r4,lr}; sub sp,#8` with the
channel at `[sp, #4]`) rather than from the field arithmetic.
