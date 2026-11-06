# Parallel nonmatching recovery, 2026-10-29

Broad source recovery now runs independently from exact tuning. Three agents pursue encounter predicates, save/preparation context and overlay/RNG/birth context, while separate compiler processes materialize and compile large ordinary C batches. A completed research pass supplies decompilation/validation and native Android gates. No approximate function is registered as an exact match.

The measured initial summary is `evidence/nonmatching/progress-20261029.json`:

| Module | Authored draft functions | Freshly compileable | Unique native bytes represented by compileable drafts |
| --- | ---: | ---: | ---: |
| main | 1,660 | 1,660 | 245,464 |
| overlay0 | 794 | 643 | 147,052 |
| overlay1, first batch | 512 | 512 | 144,040 |
| overlay6 | 439 | 439 | 63,656 |
| Total | 3,405 | 3,254 | 600,212 |

These are nonmatching hypotheses, often materially different in compiler bytes. Compilability and proximity do not establish correct ABI, state effects or gameplay behavior. Later overlay1/5 batches and repaired menu drafts have separate reports and must not be silently added twice. The summary is a dated scope, not an automatic whole-game completion percentage. Verified source coverage remains the independently measured accepted-build ledger.

Sources live under `nonmatching/`; compiler objects and scratch outputs remain under `work/`. Root batch reports under `evidence/nonmatching/` retain build/CPU/module/mode/address identity, source/native hashes, compiler/flags, compile status, comparison scope and limitations. Large standalone C drafts use bounded `.inc` fragments; every authored file remains comment-free and at most 500 lines. New workspace policy checks include these drafts. Raw/untranslated/generated failures remain separate evidence.

The item-queue reader demonstrates why functional evidence outranks a byte score. The retained legacy m2c source compiles but returns 255 instead of native FFFFFFFF for an absent item and omits an explicit helper argument. Its source hash and executable counterexample are retained. The preferred typed 104-byte hypothesis passes 1,103 native/source cases but remains 98/104 bytes; it receives zero exact credit. `evidence/nonmatching/preferred-implementations.json` records this distinction. See [the hypothesis and negative evidence](2026-10-29-item-queue-reader-hypothesis.md).

Next tuning order: correct known semantic defects and call signatures first; expand independent native fixtures; then tune compiler/types/expression shape and perform genuine linking. Exact function and affected-module comparisons precede accepted source credit. Whole-ROM exactness with original gaps remains scaffolding.

The later measured draft ledger now records 3,560 freshly compileable functions covering 638,920 unique native bytes across main and overlays 0/1/5/6. `ledger/drafts.jsonl` keeps analyzed, drafted and compiled states independent, with no function/module/ROM-match credit. Preferred semantic implementations are explicit. These metrics remain distinct from the unchanged accepted-source percentage.

A follow-up fixed-source SP1p5 sweep across close main/overlay1/overlay6 hypotheses yielded no exact source candidates. Of 516 same-size object variants inspected, all remaining differences included bytes outside relocations. Native opcode inspection identified byte-versus-word/halfword loads and stores, byte-versus-element pointer arithmetic, and accumulator-shape differences. Explicit global scalar-width hypotheses now yield 58 function candidates/3,392 native bytes; local dereference-width hypotheses yield 15/2,238. Their genuine module comparisons passed in accepted cohort 33, and only those promoted source bodies receive the measured source credit. The transformations preserve pointer declarations and byte-address arithmetic while making the scalar dereference width explicit; the compiler compares the entire native function span.

The indexed-array width follow-up selected 16 currently close C hypotheses (main 10,overlay1 two,overlay6 four). Natural widened-element and byte-offset-preserving scalar access forms were freshly compiled under recorded/default profiles; none matched completely. The zero-result reports remain under evidence/attempts and evidence/matches with root-array-widths-20261029a identities. No source credit or broad semantic claim follows from those experiments. The previously accepted global/local scalar fixes are not generalized to arbitrary indexed tables.

The new sequential-state shape sweep follows the demonstrated reward/entry selector fixes: it converts only side-effect-free identifier/member switches with terminating cases into ordinary if/else chains. It excludes all registered functions and active worker intervals. Across 220 additional compiled ARM drafts (64 +156), fresh per-unit O2 and O2/speed comparisons found nine exact candidates/2,968 native bytes. They receive zero source credit until genuine linking, fresh return/state fixtures and module acceptance. The matcher, original source hashes, complete profiles and rejected comparisons are retained in `evidence/attempts/root-linear-20261029a.json` and `root-linear-20261029b.json`; `sequential_state_shapes.py` also reproduces the independently demonstrated 976-byte selector shape. Two harness failures are preserved: a missing byte measurement was incorrectly assumed numeric, and a shifted private-helper relocation correctly failed native-branch validation. The revised harness skips absent measurements and records each helper rejection as a failed comparison without relaxing compiler/linker checks. Versioned harness snapshots retain the failed implementations.
