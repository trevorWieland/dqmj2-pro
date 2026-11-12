# decomp-permuter: generate, run, accept

`ops/permute.py` is a deterministic edit catalogue over one row's C. `ops/form_search.py`
enumerates a hand-written template grid. Both stop at the same wall: the search space
that matters when only register allocation differs is the space of *semantically
equivalent C*, and hand-writing that space does not scale.

This is the adapter for the real engine: [decomp-permuter] by Simon Lindholm, using its
`compiler_type = "mwcc"` path with a Capstone-based `objdump_command`. It generates a
complete permuter workspace from a ledger address, runs the search for a bounded time,
and — the part that matters — refuses to ship anything until `ops/verify_permuter.py`
reproduces the row through the project's own compile + relocation + byte comparison.

[decomp-permuter]: https://github.com/simonlindholm/decomp-permuter

| tool | job |
| --- | --- |
| `ops/permuter.py build` | generate `work/permuter/<module>_<addr>/` |
| `ops/permuter.py probe` | run the permuter's own setup + score once (parse check) |
| `ops/permuter.py run` | drive the search for N seconds, collect the best candidate |
| `ops/permuter_candidates.py` | rank permuter-ready rows from the source tree + ledger |
| `ops/mwcc_objdump.py` | Capstone `objdump -drz` shim the permuter parses |
| `ops/verify_permuter.py` | the only acceptance gate: byte + reloc + negative controls |

## 1. The engine is acquired, never vendored

The permuter is a Python program that reads a directory. It must not live in git (its
licence and its size are the wrong shape for this repo, and a vendored copy drifts from
the pin). Two supported locations, both already ignored:

```bash
# outside git, the normal way to run it (work/ is ignored)
git clone https://github.com/simonlindholm/decomp-permuter.git work/decomp-permuter
git -C work/decomp-permuter checkout 8556c81d80d1c1af98a858c8f4dc951357f29139

# or the project's pinned import (tools/ is ignored), same commit
python acquire_decomp_permuter_20261101.py
```

**Pin: `8556c81d80d1c1af98a858c8f4dc951357f29139`.** `ops/permuter.py` checks
`git rev-parse HEAD` on a clone and refuses to run off-pin; the pin is also recorded in
every `row.json` and in every acceptance receipt. If you move the pin, change
`PERMUTER_PIN` in `ops/permuter.py` and regenerate workspaces.

## 2. The interface, exactly as the permuter defines it

A directory with `base.c`, `target.o`, `compile.sh` and `settings.toml`:

* `compile.sh` is invoked as `bash compile.sh <input.c> -o <output.o>` — `$1` and `$3`,
  absolute temp paths. So the tool writes a `compile.sh` that calls the pinned mwccarm
  with the row's flags and `-thumb` **before** `-c` (mwcc reads the mode flag before the
  compile action; appending it after silently fails).
* `settings.toml` carries `func_name` (must be the function definition in `base.c`),
  `compiler_type = "mwcc"`, and `objdump_command`. Weights go under
  `[weight_overrides]`.
* `objdump_command` is a **string**, split with `shlex`, then executed as
  `<argv...> <object.o>` and parsed as `objdump -drz` output. Two consequences:
  forward slashes only (shlex eats backslashes), and the interpreter must be an absolute
  path — a bare `python` resolves to the WindowsApps alias stub on some machines and
  fails with `WinError 193`.
* Two host requirements the permuter does not let you configure: it shells out to
  `cpp -P -nostdinc -DPERMUTER base.c` and it invokes `compile.sh` through `bash`
  (`shutil.which("bash")`). On this machine `which bash` finds the WSL launcher, which
  cannot open a `C:\` path, and there is no `cpp` at all. `ops/permuter.py` fixes both
  for the child process only: it prepends Git's `bin` (a real POSIX bash) and a private
  `work/permuter/.bin` holding a hardlink of the pinned NDK `clang.exe` named `cpp.exe`
  (LLVM's driver behaves as a preprocessor under that program name). Nothing global is
  modified.

## 3. Generating a workspace

```bash
python ops/permuter.py build --module ov006 --address 0x02203EBC \
    --src ops/compiler_specs/02203ebc.c
# -> work/permuter/ov006_02203ebc/
#    base.c  target.o  compile.sh  settings.toml  row.json  README.md
```

`--src` is the current best-known source: an existing file anywhere in the tree, a
`src/<module>/...` packet source, or a `ops/compiler_specs/*.c` draft. Everything else
comes from the ledger and the build config: `bytes` and `mode` from
`ledger/functions.jsonl`, flags from the ledger row when it has them and otherwise from
the processor's flag profile in `config/source_units.json` (`p001` for arm9, `p000` for
arm7), and the image slice from the module's `originalImage`.

The function name is auto-detected as the last definition in the file (override with
`--symbol`); a mismatch between `func_name` and `base.c` is the most common first-run
error, which is why `probe` exists.

### `target.o`: image bytes, base object's relocation table

`target.o` is not built from scratch and it is not "the image bytes in an ELF". It is
**`base.o` with `.text` rewritten to the image slice, every relocation slot zeroed**:

```
target.o = copy(base.o); target.o.text = image[address : address+bytes]; slots := 0
```

Why this shape:

* The relocation table of the base compile names the externals exactly as the source
  names them, at the offsets the original uses — the premise of a permuter row is that
  the skeleton already matches. Keeping that table means the target and every candidate
  render *the same* `bl`/`.word` relocation text, so a score of 0 is about the
  instructions, not about symbol spelling.
* Zeroing the slots is what a fresh, unlinked candidate contains (mwccarm leaves an
  unresolved slot at its addend, 0 for a data pointer). Without it, the target's literal
  pool would hold the *linked* address while every candidate holds 0, and no candidate
  could ever reach 0.
* `build` refuses to run when `base.c` is not exactly `bytes` long. That is the honest
  precondition: fix the size with `ops/form_search.py` first, then permute.

`row.json` records the image slice hash, the zeroed slot offsets, the compiler, flags,
mode, weights and the permuter pin, so a workspace is auditable on its own.

### The shim

`ops/mwcc_objdump.py <object.o>` prints exactly what `arm-none-eabi-objdump -drz` prints
for a relocatable object: `<addr>:\t<raw bytes>\t<mnemonic>\t<operands>` rows plus
`<offset>: R_ARM_<kind> <symbol>` relocation rows, with a first line the permuter skips.
It honours mwcc's ARM ELF mapping symbols (`$a`/`$t`/`$d`), so a Thumb literal pool is
rendered as `.word` data instead of being decoded into plausible instructions
(`--mode arm|thumb` overrides the inference). Relocation kinds are limited to the three
the permuter's ARM parser accepts (`R_ARM_ABS32`, `R_ARM_THM_CALL`, `R_ARM_CALL`); an
object carrying anything else is rejected with a message rather than silently mis-parsed.

Both sides of every comparison go through this shim, which is what makes the diff
meaningful — it is not an oracle for "the real objdump", it is a consistent normal form.

## 4. Run it

```bash
python ops/permuter.py probe work/permuter/ov006_02203ebc_sp1     # parse + base score
python ops/permuter.py run   work/permuter/ov006_02203ebc_sp1 --timeout 240
```

`probe` runs the permuter with `--debug`: it builds the scorer, compiles and scores the
base, then exits. If the shim, `cpp`, `bash`, `func_name` or `settings.toml` are wrong,
this fails in seconds instead of ten minutes into a run. Always probe first.

`run` starts `permuter.py <dir> --stop-on-zero` with the environment described above,
enforces the wall-clock timeout itself (the pinned permuter has **no** `--timeout`
flag), then reads the `output-<score>-<counter>/` directories it wrote, copies the best
`source.c` to `best.c` and the diff to `best.diff`, and records `run.json`
(base score, best score, iteration count, elapsed, timeout flag, the exact command).
`run.log` keeps the raw status stream.

Numbers for this machine (Windows, single-threaded): **~0.7 permutations/s** measured
across runs (0.52-0.84), so a 240 s budget is 170-200 candidates. `-j` is not usable
here: the pinned permuter relies on fork and says so in `src/main.py` ("make
multiprocessing work on Linux... break on Windows").

Weights: the default profile in `REGALLOC_WEIGHTS` (`ops/permuter.py`) is tuned for the
row class this tool exists for — same instructions, different registers. It keeps the
`mwcc` defaults and raises the passes that reorder operands, declarations and typing
(`perm_commutative`, `perm_reorder_decls`, `perm_reorder_stmts`, `perm_cast_simple`,
`perm_refer_to_var`) above the structural rewrites that would change instruction count.
Override per row with `--weight name=value` at build time.

## 5. Accept it — score 0 is not acceptance

```bash
python ops/verify_permuter.py work/permuter/ov006_02203ebc_sp1 --source best.c \
    --emit src/ov006/permuter_20261111/native_ov006_02203ebc.c
```

The permuter's score is a diff of two objdump streams. The project's acceptance rule is
different: compile with the row's mwccarm, apply the branch and absolute relocations,
compare with the module image. `ops/verify_permuter.py` performs that comparison
independently of anything the permuter reported, and additionally requires:

0. **the fixed branch-mode path** — it relocates through
   `form_search.relocate(..., modes=form_search.TargetModes(root, module))`, i.e. `BL`
   vs `BLX` is read from the measured instruction at the call site, then from
   module-scoped ledger evidence as in
   `docs/authoring/2026-11-11-scanner-module-mode.md`. Calling `relocate` without
   `modes` falls back to `BL` and invents a 2-byte mismatch on every Thumb call to an
   ARM function; that is how `0x021FB384` and `0x021FF02C` were "failing" before that
   fix;
1. **workspace integrity** — the image still hashes to `row.json`'s value and
   `target.o`'s `.text` is the recorded slice with the recorded slots zeroed;
2. **negative control, base source** — `base.c` must *not* reproduce the row;
3. **positive, byte + relocation exactness** — score `(0, 0)` through
   `ops/form_search.py`'s compile/relocate/score path, the same path
   `ops/compiler_matrix.py` and the packet verifiers use;
4. **absolute text equality** — candidate `.text` with slots zeroed equals `target.o`'s
   `.text`;
5. **relocation identity** — the candidate references the same symbols at the same
   offsets as the base object (this is the anti-cheat: a candidate that quietly dropped a
   call cannot pass on bytes alone);
6. **negative controls, shifted slices** — the candidate must not also reproduce the
   image 2 bytes (Thumb) or 4 bytes (ARM) before or after the row.

Every check must pass. The receipt (`<workspace>/receipt.json`, or `--json`) records the
candidate hash, the compiler hash, the permuter pin, the flags, every check and the
measured scores. It contains no ROM bytes. Run the gate on `--source base.c` too: it
must fail, and if it passes, the run proved nothing.

Two of the five rows in `ops/compiler_specs/rows.json` are worth knowing about before
queuing anything: `0x021FB384` and `0x021FF02C` score 0 with their existing sources once
`TargetModes` is in play — they were the phantom `BL`/`BLX` mismatch fixed in
`docs/authoring/2026-11-11-blx-mode-fix.md`, not permuter rows. `0x02203EBC` was
re-measured after that fix and still fails on its own one-byte diff, which is why it is
the worked example below.

## 6. The proof row: `ov006 0x02203ebc`

Row: 48 B, Thumb, `native_ov006_02203ebc`; the image ends `cmp r0, r1` where the
best-known source compiled to `cmp r1, r0` — one differing halfword, same size, no
structural difference. Exactly the row class in the title of this document.

```
build    python ops/permuter.py build --module ov006 --address 0x02203EBC \
             --src ops/compiler_specs/02203ebc.c \
             --compiler tools/mwccarm/mwccarm/2.0/sp1/mwccarm.exe
probe    permuter accepted the workspace: base score 10
run #1   240 s budget -> score 0 at iteration 132, 157 s
run #2   300 s budget -> score 0 at iteration 115, 160 s, exited on --stop-on-zero
winning  return field == mask;  ->  return mask == field;
verify   8/8 checks passed, score (0, 0), 48 B, relocations identical (2)
```

Reproduced twice from the same workspace with the same weights: the winning mutation is
the commutative swap of the final comparison. The first run also carried a semantically
empty `new_var = 15` temp; the second run's diff is the swap alone. The shipped source
drops even that and was re-verified after dropping it.
`src/ov006/permuter_20261111/native_ov006_02203ebc.c` is that file, and
`docs/authoring/permuter-02203ebc-receipt.json` is the receipt for it.

**The build dependency is the interesting part, and it is not optional reading.** With
the project's pinned build, `2.0/base`, the same mutation scores **2**, not 0: `2.0/base`
folds `mask == (field & mask)` into the BIC idiom (`bics r1, r0`) and no source form
tried reaches `cmp r0, r1`. A sweep of every installed mwccarm (25 builds, the
`ops/compiler_matrix.py` question, run without the manifest dependency) gives:

| source | 2.0/base | 2.0/sp1 … 2.0/sp2p4 | dsi/1.1 … dsi/1.6sp2 | 1.2/*, 2004/b56 |
| --- | --- | --- | --- | --- |
| previous draft (`field == mask`) | 1 (size 48) | 1 (48) | 1 (48) | 18 (size 52) |
| permuted (`mask == field`) | 2 | **0** | **0** | 17 (52) |

So `0x02203ebc` is a **compiler-selection row, not a source row**: the permuter found
the right source, but the row only reproduces under `2.0/sp1` or later. This is the
first honest limit of the tool and the reason `--compiler` exists at build time. The same
workspace under `2.0/base` with the same weights, 181 s: 94 permutations, no score below
10, no output — the expected result, not a tool failure.

### The rule this establishes

**When a permuter zero requires a different build than the row's pin, that is a
compiler-selection finding — record the sweep, promote the row to the lowest exact
build, and never silently change the global pin.** Concretely, in this order:

1. **Do not touch the global compiler.** `config/source_units.json:compiler` re-measures
   every accepted row; a per-row change does not.
2. **Sweep, do not guess.** Compile the candidate source with every installed build (the
   `ops/compiler_matrix.py` question) and record the matrix in the row's evidence. The
   proof row's matrix is the table above.
3. **Promote to the lowest exact build**, not the highest: `2.0/sp1` before `2.0/sp1p2`,
   before any `dsi` build. The lowest exact build is the smallest deviation from the
   project's 2.0/base choice that reproduces the row.
4. **Register the identity.** `source_units.resolve()` rejects a `compilerSha256` that is
   not in the `compilers` map, so add the build there first.
5. **Add a row-level rule, not a profile change.** `src/ov006/**` resolves to `p004`; the
   row rule for `src/ov006/permuter_20261111/native_ov006_02203ebc.c` keeps `p004` and
   only overrides `compilerSha256`. The rest of the tree keeps the profile.
6. **Prove it through the real build path, then patch the ledger.** Source-unit
   resolution, `public_tools/repo_build.py`, and only then the ledger row's
   `compilerSha256`/`compilerFlags`/`sourceUnit`/`object`/`matchingBytes`. The permuter
   score is never the evidence here.

For `0x02203ebc` that gave: rule `{glob: src/ov006/permuter_20261111/native_ov006_02203ebc.c,
module: ov006, compilerFlags: p004, compilerSha256: e76c86fa…, mode: thumb}`,
`2.0/sp1` registered in `compilers`, `repo_build --source` compiling the row (object
`.text` byte-identical to a direct `2.0/sp1` compile, relocated bytes equal to the image,
score `(0, 0)`), and a ledger row carrying `matchingBytes: 48` with the same source hash.
Note the profile matters as much as the build: `p001` (the tool's fallback) produces a
60-byte body for this row where the config's `p004` produces 48, which is why
`ops/permuter.py build --rule` and `ops/verify_permuter.py` read the rule instead of
guessing.

### Promotion record, `0x02203ebc` (2026-11-11)

| step | value |
| --- | --- |
| ledger before | `18219454ecf39081b4cd155f83c913cdbe3c09071b9746fd1cb3621283840158` (16,073 rows) |
| backup | `work/ledger-backup-18219454ecf39081.jsonl` (32,739,058 bytes) |
| patch plan | `work/ledger-proposed-02203ebc.jsonl` (1 row, matched by ledger `id`) |
| ledger after | `f3330f8eade90521e3ead7ef4e23a36a844b60f7020418c7d520a74826ed91e8` (16,073 rows) |
| row fields | `compilerSha256` = `2.0/sp1`, `compilerFlags` = p004 (32 entries), `sourceUnit`, `sourceSha256`, `object` + `objectSha256`, `matchingBytes` = 48, `functionMatched`/`moduleLinked` = true |
| config | `compilers` + `2.0/sp1`; row rule `{glob, ov006, p004, e76c86fa…, thumb}` |
| real build | `repo_build --source` → `source-compilation-passed`; object `.text` byte-identical to a direct `2.0/sp1` compile; relocated bytes `(0, 0)`, 48 B |
| permuter | base score 10 → score 0 at iteration 1 in 6.1 s with `perm_commutative=200` (172 s with the default weights) |
| gate | 8/8 checks (`docs/authoring/permuter-02203ebc-receipt.json`) |
| reconcile after | stale 4 (all `src/ov006/p5_ov006_blx_mode/**`, pre-existing), inverse 504, unmatched 3,279 |

The four remaining stale rows are the `p5_ov006_blx_mode` sources from
`docs/authoring/2026-11-11-blx-mode-fix.md`; they are a separate reconciliation batch and
were deliberately not folded into this promotion.

## 7. Honest limits

* **Throughput.** ~0.85 permutations/s on this machine, single-threaded. A row whose
  fix needs a 4-mutation chain is out of reach in a 5-minute budget; run longer, or use
  `PERM_GENERAL`/`PERM_ONCE` macros in `base.c` to make the suspected variation
  exhaustive instead of random. Manual macros are decomp-permuter's intended mode for
  "I know which knob it is".
* **The scorer is not the acceptance rule.** It diffs objdump text, ignores stack
  offsets unless `--stack-diffs`, and rewards shapes that are not semantically sensible.
  Score 0 with a nonsense source still has to pass `ops/verify_permuter.py`, including
  the relocation-identity check.
* **It cannot fix build selection.** As `0x02203ebc` shows, a plateau at a small score
  can mean "wrong mwccarm", not "wrong source". Sweep the builds
  (`ops/compiler_matrix.py`) before spending a long permuter run.
* **It cannot fix structure.** `target.o` inherits `base.o`'s relocation table, so a
  candidate whose calls or data references change shape is rejected by check 5 even if
  its bytes look right. Missing/extra calls, wrong function boundaries, a different
  literal-pool layout, or a wrong callee are not permuter problems.
* **Same-size requirement.** `build` refuses a `base.c` that is not exactly the measured
  size. Permuting a size-mismatched draft wastes the budget: the search space is
  dominated by length differences.
* **ARM rows are implemented but under-exercised.** The shim's ARM path (`$a` mapping,
  32-bit bytes, `--mode arm`) is unit-tested but no ARM row has been permuted yet; the
  worked example above is Thumb.
* **Windows quirks are handled, not solved.** `bash` and `cpp` are provisioned per
  process; `-j` is unavailable; a killed run can leave one `mwccarm.exe` behind for a
  second. None of that affects acceptance, because acceptance recompiles from scratch.

## 8. Queuing a row

A row is permuter-ready when all of these hold:

1. it is unmatched (`states.functionMatched` false) and has a measured `bytes`;
2. there is a `base.c` that compiles to exactly `bytes` bytes (check with
   `ops/compiler_matrix.py` or `ops/form_search.py`);
3. the remaining diff is instructional, not structural: same call/relocation skeleton,
   same literal-pool shape, same instruction count (`ops/permute.py` or a manual diff of
   `ops/disasm.py` output tells you this);
4. no build reproduces it: run the compiler sweep first. If a different build is exact,
   the row needs a compiler decision, not a permuter run.

`ops/permuter_queue.py` ranks candidate families from `ops/harvest_filter.py`; treat that
list as input, not as a promise — the build sweep and the exact-size check come first.
`ops/permuter_candidates.py` answers the mechanical half of the question: for every source
unit in a module it resolves the rule, compiles, measures, and buckets the result.

```bash
python ops/permuter_candidates.py --module ov006            # permuter-ready rows, ranked
python ops/permuter.py build --module ov006 --address 0x... --src <row source> --rule
python ops/permuter.py probe work/permuter/ov006_<addr>
python ops/permuter.py run   work/permuter/ov006_<addr> --timeout 600
python ops/verify_permuter.py work/permuter/ov006_<addr> --source best.c --emit src/ov006/<packet>/<symbol>.c
```

Three buckets come out of the scan, and only the first is permuter work:

* **permuter-ready** — exact compiled size, bytes differ, and the difference is *small in
  the shim's normal form* (`textDiff <= 3` instruction rows by default). Both tests are
  needed. The first full `src/runtime` scan (962 units) called **259 rows ready on the byte
  score alone**; the normalized diff showed 246 of them at roughly 70+ differing rows, i.e.
  one byte of encoding difference that desynchronizes the instruction stream or sits in a
  shape the randomizer cannot reach. Calibration on `src/runtime/ov006-thumb01` (358 units):
  95 already exact, 8 relocation-only, 246 large-diff, **0 true near-misses**. A run on three
  of the byte-level "ready" rows confirmed it — 90 s each, base scores 705-905, best 805, no
  zero, which is the expected outcome for a row that is not in the allocation class.
* **relocation-only** — exact size, byte diff, `textDiff == 0`. The diff sits in a
  relocation slot, both sides render `bl <target>`, the permuter reports score 0 and does
  nothing. Fix the link/relocation, not the source.
* **large normalized diff** — exact size and a small byte score but tens of differing rows.
  Not a near miss; byte score over-reports these badly.
* **already exact** — the source reproduces the row under its own rule. That is ledger
  reconciliation (`ops/reconcile_ledger.py`), not a permuter job.

`--rule` is not optional in practice: it takes the compiler, flag profile and mode from
`config/source_units.json` for the `--src` path. Without it the tool falls back to the
ledger row or the processor profile, and `p001` vs `p004` alone changes this row class's
codegen (see the rule above). The build also copies the source's quoted-include closure
into the workspace, because the permuter's hardcoded `cpp -P -nostdinc` has no include
path and its candidate files are written to a temp directory.

### The relocation-only bucket was a patcher bug, not dead rows

The first pass put ten accepted rows (156 B) in the relocation-only bucket:
`0x021edc3c`, `0x021ef108`, `0x021ef84c`, `0x021f4f30`, `0x021f57e0`, `0x021f69e0`,
`0x021fb7b0`, `0x021fd948`, `0x021fd954`, `0x022042ac`. Every one compiled to the exact
measured size and was one byte off, with the whole difference inside a single
`R_ARM_ABS32` relocation slot: the image stores a Thumb function's address **with bit 0
set**, and the patcher stored the even address.

`ops/form_search.py:relocate` now writes the measured `R_ARM_ABS32` word from the caller
image; when the site is outside the image it falls back to the function-symbol/Thumb
resolution that also decides `BL` vs `BLX` (module-scoped, see
`docs/authoring/2026-11-11-scanner-module-mode.md`). After the fix all ten rows measure
exact and the relocation-only bucket is empty in every module scanned so far. Two
consequences worth keeping straight:

* the public `bytematch` path compares relocation *contracts* rather than patching bytes,
  so these rows were already counted in the ledger; the bug was in the local measurement
  path (`ops/form_search.py`, `ops/compiler_matrix.py`, `ops/verify_permuter.py`), which
  would have rejected a correct source for any row holding a function pointer literal;
* `ops/test_form_search.py` pins the rule: Thumb function vs data vs ARM function, addend
  ordering, the no-`modes` fallback, and the BL/BLX marker bits.

The all-module queue scan (below) then found the second, different cause: `0x020337c4`
(main, 364 B, two source files) named its pivot table `native_data_020d9aac` while the
image's literal pool holds `0x020d90ac + {0,1,2,3}`. The shape was right and the pointer
was 0xA00 high, so every objdump-level diff called it a match; only the byte comparison
saw it. The corrected source is `src/main/permuter_20261111/native_main_020337c4.c`
(verified `(0, 0)`, 364 B under its own rule: `2.0/sp1p5`, ARM, `-opt speed`). Both causes
are recorded because they are the two ways a row lands in this bucket: the patcher
dropped information, or the source named the wrong address.

## The addressable market, measured (2026-11-11)

`ops/permuter_candidates.py --modules all` over the whole tree: **12,002 compiled units**.

| bucket | rows | bytes |
| --- | --- | --- |
| permuter-ready (textDiff <= 3) | **0** | **0** |
| relocation-only | 2 (one row, two files; both since fixed) | 728 |
| large normalized diff | 12 | 708 |
| already exact under a declared rule | 4,948 | 224,738 |
| skipped (no address in the file name, or no ledger row) | 7,011 | - |

The skipped bucket is structural, not a failure: a source file whose name carries no
`<8 hex>` address is either a data unit or a multi-function packet, and neither maps to a
single ledger row.

**So the true near-miss population is 0 rows / 0 bytes.** Every addressable source unit in
the tree either reproduces its measured row exactly under a rule the build already knows
(primary or alternate compiler/flag profile) or cannot be attributed to a row. The twelve
large-diff rows -- `utility-child-arm7-wram` translated07/13/15/16/20 drafts and two main
rows -- are the closest candidates, but they are not instruction-level near misses: a
probed run on `0x038029f4` put the permuter's own base score at 300, about thirty differing
instruction rows, which only looks close when counted in bytes (score 2).

What that means operationally: the permuter has no queue to work through today, and the
tool's value is now prospective -- it ranks new drafts. The scanner caches per
(source hash, compiler, flags) under `work/permuter/`, so re-running after new sources land
is minutes, not an hour. `docs/authoring/permuter-queue-v2.md` is the generated snapshot;
the JSON beside it carries every row with its address, size, score and normalized diff.
