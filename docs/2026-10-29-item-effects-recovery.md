# Native item effects and record wrapper - 2026-10-29

The authoritative input is the private 175,959,612-byte ROM with SHA-256 `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`. Tests use disposable Unicorn memory. The original ROM/save, baseline and application are preserved. Overlay identities remain distinct despite overlapping load ranges.

## Exact wrapper candidate

`src/mechanics_save/20261029_item_effect_wrapper.c` reconstructs overlay0:ARM `022140C0-02214120`, 96 bytes. Its source SHA-256 is `50eac63ad9aa3466d7b7839f1abd627a71ff653b95ae313f9daef048b82a90b1`. The real-linked binary equals native span SHA-256 `9c18cd58dc040ac0aa3998410e754e5739b42ada4aa0db365e4912b4bdaab62c`.

The pinned MW 2.0/base compiler with recorded ABI flags and O2/speed produces the complete match. Declaring species before the block/bonus pointers resolved register allocation. The promoted source is byte-identical to the successful hypothesis. No assembly, executable byte array or opcode substitution is used.

Run `python match_mechanics_save_20261029_item_effect_wrapper.py`, optionally passing a repository-relative `--source`. It emits `evidence/matches/mechanics-save-20261029-item-effect-wrapper.json` with source/object/link pins and native symbol dependencies. Only 96 bytes are candidates for coordinator acceptance. This worker performs no registration or shared build mutation.

The wrapper takes a nullable saved-record pointer, feature pointer and 32-bit item index. A nonnull record forwards record+0x20, record+0x40, signed halfword record+0x18, unsigned byte record+0x1A, features, item, null live-entity pointer and final word 1 into main:ARM `02066358`. Null-record forwarding supplies zero for the first four words. Separate ABI-only provider tests check all eight words; no null-record effect safety is established.

## Larger core hypothesis

Main:ARM `02066358-02066A6C` remains nonmatching. The preferred explicit-ABI source `nonmatching/save-core/20261029-preparation/effect_explicit_abi.c` has SHA-256 `f30ca37e0a21fdd882211e5eba3e814b32245d7af5dcb9750640e6a381cc67ed`. It compiles and really links to 1812 bytes with 1666 same-offset bytes. A separate declaration hypothesis reaches 1676/1812, but receives no semantic priority merely for its higher score. No exact core source credit is claimed.

The core accepts mutable 32-byte state, optional bonus data, species, variant, features, item index, live entity and an eligibility-enforcement word. The first four arguments occupy registers and the final four occupy the caller stack. A nonzero final word invokes main:ARM `02065E44` and returns full-word -1 if rejected. Its native getters may first clamp over-max signed resource fields at block+4/+6. A zero final word bypasses eligibility and still mutates state. It is not a preview mode.

The item kind comes from table byte 0x28, with parameters at 0x2A/0x2B. Kinds 1/2 update signed fields +4/+6. A lower parameter 0xFF fills to the native maximum and returns 255. Other amounts draw an inclusive RNG range, store with 16-bit wrapping, then compare the stored signed value to its cap.

Kind 3 can call native percentage setter `0207C844`. Its signed division truncates toward zero, and it clears block+0x13, corresponding to saved record+0x33. A positive current value bypasses the chance draw. Failed chance can leave the percentage parameter as the returned word, so a return value alone does not universally identify applied gain.

Kind 12 changes signed block+0x1C with wrapping, then invokes `02063C00(19,1)`. A previously clear secondary 19 also sets auxiliary 83 and primary 76. The 999 cap is checked after the signed-halfword store, with excess subtracted from the returned delta. Kinds 13-18 modify six signed fields; kinds 13/14 also modify their corresponding current-resource field. Their result accounts for post-store cap excess. Kind 48 computes the full signed 32-bit difference block+0x18 minus block+0x14 minus 1, updating block+0x14 only when positive.

Other groups return full-word -2, zero or -1. The preserved legacy m2c input incorrectly narrows the common result to unsigned byte, losing sentinels and larger experience deltas. These measured effects do not establish named health/status/ownership or progression meanings. Inventory ownership, paid-operation gates and consumption remain caller responsibilities. The earlier measured caller `020731AC` performs separate consumption.

## Execution evidence

Run `python evidence/application/effect_fixtures_20261029.py`. The report `evidence/application/effect-fixtures-20261029.json` passes 3180 cases and 6360 actual routine returns plus 40 original native leaf controls, totaling 6400. The source-hash-pinned hypothesis receives zero exact credit.

An independent Python model checks the complete modeled saved region, RNG seed/draws, signed halfword wrapping, caps, full-word returns and secondary flag coupling. Native and compiled C also agree on observed writes, division transactions and watched callee arguments/results. Each case uses a fresh machine, explicit stacked arguments, bounded instructions, actual return, stack balance and preserved-register checks.

The suite covers 253 measured ItemTbl rows outside three scene-specific kind-24 rows, six saved-block profiles, both enforcement settings and 12 explicitly synthetic descriptors. Physical reserved table rows are included; usable-item legality is not implied. Profiles include captured, zero, one, maximum, 32767 and -1 fields, plus an unequal experience gap. Synthetic descriptors cover full-resource parameters, chance extremes and sentinel kinds in disposable memory. The independently checked RNG update is `(seed * 1103515245 + 12345) mod 2^32`, followed by the upper-half remainder for a positive bound.

The exact wrapper report `evidence/application/effect-wrapper-fixtures-20261029.json` passes 1012 connected cases and 2024 routine returns across four block profiles, plus 30 native controls and four separately counted ABI-only returns, totaling 2058. Connected cases execute the complete original 1812-byte core, predicate, RNG, resource helpers and flag writers with no callee substitutions. Only the four ABI-only tests replace the effect entry, including null-record forwarding; they do not prove null-record safety.

The only device provider is bounded hardware division with a nonnegative 64-bit numerator and positive 32-bit denominator. The tested context is species 1, variant 0, neutral 64-byte features and null live entity. Core optional bonus is null; wrapper bonus fields are zero. Arbitrary species/features, nonzero bonus, live-entity effects, kind-24 transitions, physical overlay loading, ordinary scene access and native bank selection remain unsupported. Leaf maxima and caps are measured native controls, not independent re-proofs of growth formulas.

## Negative experiments and reproducibility

Compiler, width, declaration and structural hypotheses remain separate under `nonmatching/save-core/20261029-preparation/`, with JSON attempt records. All eight original compiler/goal profiles fail the larger core byte gate. The 2.0 speed families reach the correct extent; declaration changes leave register differences. These experiments never count as accepted source.

The independent model exposed two Python errors: kind-14 current-resource offset mapping and floor division instead of truncating signed percentage division. Both were corrected in the model; native code and the frozen C hypothesis were unchanged. A C90 declaration-placement experiment also failed compilation and was not adopted.

The exact wrapper replay succeeds from the repository root and an unrelated working directory. It verifies the source, object, pinned linker artifacts and qualified main-core relocation before publication. Earlier accepted record, selection and 1300-byte eligibility sources remain frozen. Coordinator registration, module/whole-ROM regressions and isolation gates remain separate.
