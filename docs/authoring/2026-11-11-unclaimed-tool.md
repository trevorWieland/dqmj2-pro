# Screening debt: `ops/unclaimed.py` and the 2026-11-11 ledger correction

The ledger's `states.functionMatched` flag is the input to the duplicate check, the
harvest filter and the permuter queue. On 2026-11-11 it was stale enough to tax every
authoring lane:

* `ov000` pass 3 drafted 9 rows that were already defined under `src/` (8 of them in
  `src/ov000/pass1_20261111`);
* `ov001` pass 3 had to skip 11 of its own family members because the family address
  was already taken;
* the main lane's duplicate screen could not be trusted to answer a yes/no question.

`ops/reconcile_ledger.py` already existed, but its definition scan only recognised
symbols that end in the address. That misses two shapes that are already in the tree:

1. **an address-named file with a semantically named symbol** — `src/main/r1_main_small/native_main_020685bc.c`
   defines `saved_identity_profile_pointer`;
2. **a header that wraps before the body opens** — `s32 native_ov000_021e02b0(Actor *actor, ...`
   on one line, `ParameterBlock *third)` on the next, `{` on the third.

It was also address-global, which is wrong for overlays: every overlay loads at
`0x021d7240`, so a definition in `src/ov000` was being counted as a claim on an `ov004`
row at the same address.

## The tool

`ops/unclaimed.py` builds one evidence index from `src/` and answers two questions.

**Claims** (strongest first):

| kind | evidence |
| --- | --- |
| `symbol` | a definition whose identifier encodes the address (`native_ov000_021e0478`), in C, C++ or assembly |
| `file` | a source file whose stem encodes the address, whatever the symbol inside is called |
| `data` | a data definition named after the address; claims the bytes, not a function body |

A *mention* — an `extern` declaration, a prototype, a call site, a comment, an
immediate — is never a claim. Claims are **module-scoped** from the symbol tokens and
every path component, so `src/ov000/...` cannot claim an `ov004` row that shares the
address. A claim whose module cannot be inferred is reported as `unscoped` and still
counts, because being conservative is the point of a duplicate screen.

**Ledger state is secondary.** A row is genuinely unclaimed when the tree has no claim
for it; `functionMatched` then only moves the confidence:

* `high` — unmatched and no mention anywhere in `src/`;
* `medium` — unmatched but the address is mentioned (a caller or a leftover
  declaration exists, so something may still surface);
* `low` — the ledger says matched while nothing claims the row (an *inverse* row; not
  unclaimed by definition, only listed with `--include-inverse`).

```bash
python ops/unclaimed.py --module ov000                 # address, module, bytes, mode, confidence
python ops/unclaimed.py --all --json work/unclaimed.json
python ops/unclaimed.py --check-addresses 0x021FBB04 main:0x020685bc \
    --address-file work/batch.txt                       # exits 1 if any is defined
```

`--check-addresses` is the batch gate that replaces hand screening: `module:ADDR` is
checked against that module plus unscoped claims, a bare `ADDR` against every module.
The exit status is 1 when any address in the batch is already defined, so a packet
build can refuse before drafting.

`ops/reconcile_ledger.py` now imports the same evidence model, so the two tools cannot
drift apart, and it reports four buckets with counts and bytes instead of three counts.

## Measured on 2026-11-11 (16,073 ledger rows, 15,308 with bytes)

Before the tool, the old address-global, symbol-only reconcile reported:

| bucket | rows | bytes |
| --- | --- | --- |
| stale | 202 | 11,668 |
| inverse | 504 | 81,968 |
| genuinely unmatched | 3,081 | 900,086 |
| consistent | 11,521 | — |

With the module-scoped evidence index:

| bucket | rows | bytes |
| --- | --- | --- |
| stale | 204 | 12,000 |
| inverse | 472 | 74,590 |
| genuinely unmatched | 3,079 | 900,086 |
| consistent | 11,553 | 1,144,504 |

The moves are each explainable: **+5** stale rows only an address-named *file* catches
(one of them `0x020685bc`), **-3** rows the old scan falsely claimed from another
overlay, **-74** rows that leave the inverse set because wrapped-header parsing finds
their definition, and **+42** rows that enter the inverse set because module scope
refuses their cross-overlay "claim". Net: stale +2, inverse -32, unmatched -2,
consistent +32.

## The ledger correction

`ops/reconcile_ledger.py --patch` proposed 204 rows (12,000 bytes) across `ov000` 60,
`ov001` 53, `ov006` 52 and `main` 39. Every claim sits in the row's own module source
root (`src/ov000`, `src/ov001`, `src/ov006`, `src/main`, plus one `src/runtime` file
whose symbol is `native_main_...`). The guarded applier wrote it:

| | |
| --- | --- |
| backup | `work/ledger-backup-f3330f8eade90521.jsonl` |
| before sha256 | `f3330f8eade90521e3ead7ef4e23a36a844b60f7020418c7d520a74826ed91e8` (32,723,744 B, 16,073 rows) |
| patch | `work/ledger-proposed.jsonl`, 204 rows (`functionMatched=true`, `sourceUnit`, `sourceLanguage`) |
| after sha256 | `751f366138a3a9ac7ed2b4e2113cadd36a0b80697bcfd89e598aa46e8a9760fb` (16,073 rows) |

Re-reconciling the live ledger reports **stale 0**, inverse 471 / 74,046 bytes,
genuinely unmatched 3,079 / 900,086 bytes, consistent 11,758 / 1,157,048 bytes. The one
inverse-to-consistent move is the scanner fix (`address in the file stem only`), not
the write. No compiler pin, source file or configuration was changed.

The 471 inverse rows are not lost sources: every one still carries a `sourceUnit` that
exists on disk, which is the renamed-source bookkeeping
[docs/acceptance/inverse-504.md](../acceptance/inverse-504.md) describes. They are the
next naming job, not a screening problem.

## Verification

`python public_tools/repo_build.py --root . --private-root . --compile-only` over ten
of the newly flagged rows — both overlays, both modes, the wrapped-header file and the
semantic-symbol file — reports 10 selected, 10 compiled, 0 failed. The sources were
already committed; only the ledger changed, so this is the expected result and it
confirms the correction did not disturb any unit rule.

## What this replaces, and what it does not

* `ops/check_duplicate.py` remains the single-address interactive check, but
  `ops/unclaimed.py --check-addresses` is the batch gate and knows about module scope
  and address-named files.
* `ops/screen_candidates.py` still does the disassembly screen (size, call count, BLX
  mode, boot floor). `unclaimed.py` answers only "is it claimed?" and does not replace
  candidate ranking.
* `ops/reconcile_ledger.py` and `ops/unclaimed.py` share one evidence index; run both
  after every wave and gate the packet on `stale 0`.

Limits worth knowing: a claim is attributed to every module named by symbol tokens or
path components (a shared `src/runtime` file can legitimately claim two modules); data
symbols are counted separately and never flip `functionMatched`; `.h` files can define
symbols but a header stem never claims an address by itself.
