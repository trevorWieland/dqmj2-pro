# Reproducibility status and preserved failures — 2026-11-02

This consolidates and supersedes the historical replay narrative previously embedded in README. Machine receipts and logs remain authoritative; failed evidence is preserved.

## Current status

The current accepted cohort is identified by README and its committed finalized receipt/expanded source closure. Starting cohort 146 had 9,517 functions and 780,507 initialized source bytes. Subsequent accepted cohorts are identified by their committed shared acceptance and closure receipts; 148 combined the original unpublished 148–150 inputs with parallel worker packets. Neither static committed closure nor a prepared live manifest proves a current complete independent replay. See the [execution plan](2026-11-02-parallel-execution-plan.md) and [aggregate record](2026-11-02-parallel-wave-acceptance.md).

Latest successful recorded fresh build/oracle replay: checkout P, revision `eb923c71b12abe5a5f69c5e694138cc8dcce28ac`, 2026-10-30, 8,668 functions / 588,101 bytes, 595 completed commands. The separate strict workspace audit reports concurrent changes in the parallel application. This is build/oracle success, not aggregate audit success.

Latest historical failed fresh replay: checkout Z, revision `7b49e810a532206970ab4627e7c43dd661cc687e`, 2026-10-31, command 854 `validate_arm7_channel_parameters_20261030_67.py`: `Complete channel-parameter generator closure differs`. A repair is already committed in `reproduce_channel_parameters_closure_v2_20261101.py` and selected by the recovery registry. The independent cold component replay below verifies that repair without adding a duplicate.

Inspect `evidence/verification/clean-checkout.json`, dated `clean-checkout-*.json`, `evidence/verification/cohort146-expanded-source-closure-20261101.json`, and new wave-specific validation receipts under `evidence/verification/parallel-wave20261102/`. Passing static source/input closure does not establish dynamic replay success.

## Active parallel-wave findings

The existing channel 67 repair passed a cold isolated wrapper replay followed by the unchanged validator: three positive units / 296 bytes, 3,080 actual original/compiled returns and 41 rejected negative controls. The original 214 generator entries remain unchanged; three supplemental replay sources are recorded separately. Historical Z's extra sealer entry is independently rejected. This is zero new source credit and a component replay proof, not a full clean checkout. Receipt: `evidence/verification/channel67-parallel-wave20261102/cold2.json`.

A new materialization attempt exposed ten intentionally committed MSL reference-source/license paths under `deps/`, which the older blanket source-snapshot rule rejected. Commit `b35aaddb` permits only the exact four provenance manifests' ten C/H/license files, verifies committed blob hashes and rejects changed local dependency copies. Sixteen negative controls cover other dependency/executable/cache paths, traversal, absolute paths, incorrect upstream identity and nonzero source credit. Receipt: `evidence/verification/parallel-wave20261102/clean-reference-policy.json`.

`run_clean_parallel_wave20261102.py` attempted a genuine independent replay of that immutable commit in the separate sibling `j2p-clean-parallel-wave20261102` directory. Only final report publication was redirected into a wave-specific namespace to avoid collision with shared acceptance. Its failed result remains independent of the component and policy tests.

That immutable run subsequently failed before accepted reconstruction: source verification required four pinned native ARM7 runtime images before the runtime extraction commands had generated them. The committed bootstrap fix derives only those exact original runtime inputs and then performs the full source-hash gate. Cold-input and tamper controls pass. A separate patched diagnostic completed 31 replay commands, including channel67, before it was deliberately stopped; it does not convert the original failed run into success. Source-root compatibility was checked by executing the original launch/timeout/registry-mutation test statements unchanged against disposable output fixtures.

The runner now stops after a command changes the native registry, source preferences or interpreted registry. A detected violation cannot be cleared by restoring bytes before final hashing. Qualified controls retain true source/hash checks, reject changed/removed/restored scope and preserve the original negative tests. The registry-mutation test now stops after one invalid command instead of executing 1,296 otherwise-successful mocked commands and repeatedly rewriting 6.4 MB of registry data. This strengthens failure handling; it does not skip any valid replay command. Source-complete fixtures regenerate the exact adopted implementation from pinned Git input, without old work-directory dependencies. See `runner-scope-failfast-reproducible.json` and `runner-scope-restoration-reproducible.json` in the wave verification directory.

The restarted patched146 diagnostic was deliberately bounded and stopped after 145 of 1,313 planned commands completed successfully. The next command is separately recorded as interrupted; no result is credited for it. Original B35 failures and all completed command/log hashes remain preserved in `continued-diagnostic-v2-bounded-termination.json`. Verified process ownership and repeated descendant checks left no running diagnostic processes. This is neither a complete fresh replay nor a replay of the later accepted cohort.

A two-content-sweep source-pin optimization remains unadopted. Seven actual mutation/restore controls passed in a separate current-epoch private snapshot, but full 14-case validator equivalence is unrun and that snapshot still lacks identified baseline and object/link closure. Timing is not correctness proof. The exact blockers and first private check are preserved under `evidence/lanes/parallel-wave20261102/scope-pin-private-qualification/`; no persistent cache replaces content checks.

Cohort149 passed all module/ROM and 14 regression gates, then retained strict source-policy and packaging failures for generated research placement. Byte-preserving relocation, explicit opaque diagnostic archives and generated snapshots resolved packaging without changing accepted C, frozen READY, native source pins or the staging/finisher policy. Its committed source/input and 17,609-path oracle-closure checks pass. Cohort150 is the separately frozen 95-function / 27,280-byte union; README and its committed closure receipt determine its shared acceptance state.

## Historical milestones and failures

- Checkout M, revision `db72691e1cb9a2aa98ad3c90ca05a2e8e7bce622`, cohort 46: 8,623 native functions / 580,337 bytes and 1,235 script instances / 29,056 physical bytes. Source/build/oracle/tool/module/exact-ROM checks passed, including explicit source-primary selections; isolation findings retained outside application changes.
- Checkout N, cohort 47: generated-golden ordering and root-dependent verifier metadata failed. Later portable-behavior and cross-directory diagnostics did not substitute for a full replay. [Repair](2026-10-30-clean-replay-golden-dependencies.md).
- Checkout O: 507 successful commands before the 600-second outer deadline on interpreted world-source batch09. Its failure and separately bounded timing diagnostic remain evidence. P subsequently passed the older full fresh-build/oracle scope.
- Q/R: committed source-selection receipts missing. [Repair](2026-10-30-clean-source-selection-closure-repair.md).
- S/T: auxiliary oracle script absent. Systematic source packaging and entrypoint preflight followed. [Repair](2026-10-31-oracle-source-closure-repair.md).
- U: 690 successful commands before a missing frozen nonmatching C input. Nested profile/pin closure was expanded. [Repair](2026-10-31-static-oracle-input-closure-repair.md).
- W: 224 successful commands before a batch-only static input omission. [Batch/oracle root and static-read repair](2026-10-31-batch-and-oracle-input-closure-repair.md).
- Z: exact generator-closure disagreement described above. The existing repair keeps the original generator list frozen and records supplemental replay code separately.

The cohort94 package audit separately classifies the ROM-derived ARM7 physical input. Its original strict audit failure remains preserved; no executable blob receives source credit. [Derived-input audit](2026-10-31-derived-arm7-source-package-audit.md).

## Reporting rules

Separate source compilation/matching, connected behavior, module links, exact packaging, committed closure and independent replay. Keep `allChecksPassed` distinct from `freshBuildAndOracleChecksPassed` when isolation observes unrelated application changes. Preserve failed receipts and exact inputs.

Clean replay uses committed source plus explicitly identified private inputs/tools/dependencies. It cannot borrow cached work, generated extraction, dependency links or untracked research producers. Supplemental verification identifies its hashes/scope without silently changing frozen historical generator lists.
