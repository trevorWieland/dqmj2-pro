# Progression controller's two-byte skill input

This refines the still-unmatched main ARM controller at `020C61A4`, measured extent 3,744 bytes and native SHA-256 `fe089bff7da0dff307a7bca975cf70f9e51cc3e903efb31e1780ce2a92290aa1`. It adds no matched function or executable bytes. Accepted source, application code, ROM and saves remain unchanged.

The original case-zero prefix prepares two adjacent stack bytes, `8E 00`, before calling `02062E44(createdUID, 1, pointer)`. The independently accepted callee is `saved_record_skill_initialize` in `src/mechanics_save/record_update.c`, source SHA-256 `fa7fef97fe89b83cc446fc45bef3d1a22a98aff1c1adb5a1eee7b98349ec800f`. Its nonnull input contract is the two-byte `SavedSkill { u8 skill; u8 allocated; }`, copied into the selected record slot. This note uses those source field names as an existing ABI view; it does not establish ordinary progression reachability or additional skill meanings.

The earlier flat hypothesis declares separate signed-byte locals `sp0` and `sp1`, initializes both, then passes only `&sp0` through an empty helper prototype. That declaration gives the addressed C object one byte. Under the pinned compiler, the store to the separate, unescaped `sp1` disappears. The new `state` field-view hypothesis retains this problem and provides an executed counterexample. Its complete linked bytes are identical to the frozen original-local-order hypothesis; source and object provenance remain distinct.

The preferred `typed_skill` hypothesis uses a real two-byte unsigned structure and an explicit `02062E44(u32, s32, const ObservedSavedSkill *)` declaration. It assigns both members and passes the structure address. This preserves the original two-byte input in the measured prefix. It remains a nonmatching whole-controller hypothesis.

## Bounded measurements

`python prove_mechanics_save_20261101_lane_progression_skill_input.py` rebuilds both frozen hypotheses with the measured historical Metrowerks 2.0/base compiler and the original O2/inline-off/speed flags, performs genuine MWLD comparisons, then executes the original and both linked prefixes.

The matrix contains 1,536 contexts: all 256 numeric-byte inputs, primary flag-six clear/set, and stack poison `00`, `A5`, or `FF`. Across the three implementations this gives 4,608 explicit prefix completions, 6,912 actual original getter returns and 4,608 supplied calls. The original and corrected versions each reach 768 skill-input boundaries with `8E00`. The historical scalar variant produces 512 mismatches under nonzero poison and 256 coincidences under zero poison.

Every entry starts synthetically immediately before the measured primary-getter setup. Constant registers come from decoded preceding instructions. The original primary/numeric getter bodies execute. Creation and the first null-input skill initialization are supplied and legally clobber caller registers/flags. The later nonnull skill call is an observed, verified external BL boundary; its body does not execute in this probe. Every run stops explicitly at that boundary or the decoded skip branch. There are zero complete parent returns and zero skill-callee returns. Timeout is a failure.

Thus these measurements prove supplied pointer bytes and the narrow source correction. They do not prove record creation, actual saved-record mutation, startup/heap/UI initialization, bank selection, chronology, enclosing scene access, or complete controller semantics. No semantically unknown save-byte count changes.

## Bounded source experiments

Ten new whole-function hypotheses retain their complete source, compiler identity, object hashes, current real-link results and negative comparisons under `nonmatching/save-core/20261101-progression-fields139/` and `evidence/lanes/save-core/progression-fields139-20261101.json`.

| Hypothesis | Linked size | Same-offset bytes |
|---|---:|---:|
| Controller field view | 3748 | 935 |
| Context field view | 3748 | 921 |
| Both field views | 3748 | 921 |
| Signed contiguous payload | 3756 | 634 |
| Unsigned byte array | 3756 | 634 |
| Array with explicit case 14 | 3760 | 907 |
| Scoped array | 3756 | 634 |
| Scoped array with case 14 | 3760 | 907 |
| Typed SavedSkill input | 3756 | 634 |
| Scoped typed SavedSkill input | 3756 | 634 |

All ten compile and reach genuine real-link comparison; none matches. Size and byte-score improvements do not outrank the measured input contract. The preferred typed input is selected only for further research, not accepted module construction. Eight additional bytes relative to the scalar draft reflect its different generated body; no padding, fake arguments, forced registers, assembly or opcode edits were introduced.

The sweep replay is `python experiment_save_core_progression_fields139_20261101.py`. Its archived per-root object/link metadata documents this lane's experiment. The smaller proof entry point rebuilds its own two source objects and consumes no scratch result JSON or unmaterialized generated golden.

Full vectors remain in a deterministic gzip sidecar with declared compressed and uncompressed SHA-256 hashes. Canonical case identity excludes compiler/debug paths; fresh object/link provenance remains separate. The final normal and isolated alternate-working-directory replays must reproduce the same report within this repository.
