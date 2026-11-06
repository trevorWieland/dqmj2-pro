# SDK animation drafts and original state effects — 2026-10-30

Main:ARM `02034F90..02034FF0` (96 bytes) and `02035018..02035108` (240 bytes) are two canonical unmatched functions reserved to this worker. The ownership audit found no accepted overlap. Both have complete ordinary C hypotheses with explicit animation/frame/sequence/cell-bank fields. They remain nonmatching and add zero functions/bytes to accepted coverage.

| Target | Preferred source | Source SHA-256 | Native / compiled / equal-offset bytes |
| --- | --- | --- | --- |
| `02034F90` | `nonmatching/save-core/20261030-sdk-animation/native_main_02034f90_typed.c` | `6343cd059dbe46f6b0eb454ee4b057cd940d407507183163f8d6ce35e8d2ee5e` | 96 / 92 / 71 |
| `02035018` | `nonmatching/save-core/20261030-sdk-animation/native_main_02035018_typed.c` | `dd1a82d7c81218b6ef9a68cd6004be2c79f54a970f85f408fd9910829d3e8ea9` | 240 / 208 / 177 |

The common measured field layout is `animation_types_v2.h`, SHA-256 `ea24e0db385b54a4d5dc8f0aacbf5ba363542a0dfcebd761bf8df7b2dd09f0c4`. The first source uses pinned 2.0/base O2/speed; the second uses O2/space. Both are genuinely MW-linked at their native addresses for byte comparison and again at isolated `026E0000`/`026F0000` for complete source execution. During each source test, reads/fetches of its original target body are forbidden and ARM/literal mappings are checked. No original executable tail, forced register, volatile field or assembly supplies missing source behavior.

## Reproduction and counts

Run `python evidence/application/sdk_animation_source_20261030.py`. The frozen report `evidence/application/sdk-animation-source-20261030.json` has SHA-256 `c9e47c701938b6cc435422965f178cceeb903bda3806579a56a0f985826a7103`; normal and unrelated-working-directory replays reproduce it exactly. The native-case payload digest is `66bd9d07c43dd00a268be899a8d126ef34c982079330a24be59d2a6c0005470e`, separate from current object/debug/link provenance.

There are 120 reset and 437 apply contexts, each run natively and from compiled C: 1,114 actual target returns. Each positive execution starts with one separately counted original constructor return, adding 1,114 setup returns. Four unsupported controls also complete their setup constructor before their target stops. Thus supported host returns total 2,228; including the four explicitly separate unsupported-setup returns, total actual host returns are 2,232. The report separately records 6,432 supported target helper returns and 18,938 supported setup helper returns. There are zero providers. No stopped target is counted as returned.

Each setup executes the original 124-byte initializer and original SDK chain against explicit synthetic sequence/cell data. Only after setup does a source run install its complete isolated candidate. This is not original target-code fallback during the measured source invocation. Full widget and RAM transfer buffers, exact ordered writes, readonly SDK inputs and copied-save invariance are independently modeled. Every call requires actual STOP, original SP and preserved callee-saved registers.

## Reset state and direction

The 96-byte routine compares signed speed with zero, combines that Boolean with the complete reverse word, and selects either sequence loop-start or count-minus-one. It stores current/active frame pointers, resets elapsed time and invokes original `02034D68` with delta zero. The source expresses the measured full-word XOR condition; reverse values2/FFFFFFFF are not silently normalized to Boolean. The matrix spans positive/zero/negative speed, reverse0/1/2/FFFFFFFF, running0/1 and several explicit count/loop-start pairs with positive frame durations. The original tick code executes without a substituted return.

The closest source retains correct state effects but its optimizer removes one redundant native current-frame reload. Source/control-flow and archive/profile experiments did not establish complete byte equality. No unjustified volatile field or generated assembly is used to force that load. Malformed sequences, nonzero tick deltas and arbitrary callback execution remain outside this proof.

## Cell, SRT and transfer state

The 240-byte routine returns immediately when the active frame duration is zero. Otherwise it obtains content through original `02034D5C`, looks up the cell through original `020349F4`, writes the selected cell pointer, initializes SRT through original `020372F8/02037308`, and applies transformation branches through original `02037294/020372D8/020372B8`. A cell index outside the synthetic bank's count produces a null cell pointer when no extension entry is accessed; that is measured behavior, not a claim of a valid resource.

Sequence type is masked to its low byte. Type0 preserves identity SRT, type2 reads the two signed halfwords at content+6/+4, and every other nonzero low byte uses scale words+4/+8, the rotation halfword+2 and translation halfwords+14/+12. Flags at SRT+12h accumulate masks2/4/8 for those operations. Tests include high type words, signed halfword limits and complete high-bit scale words. Cell-bank flag bit0 selects the original8/16-byte cell stride.

When extension data is nonnull and the complete handle differs from `FFFFFFFF`, original `02035518/02035500` update actual RAM transfer state. The explicit synthetic manager pointer at `020F0EF8+8` addresses four48-byte records; the selected record receives `FFFFFFFF` at+24h and the two extension words at+28h/+2Ch. These are real native stores, not supplied transfer effects. The four-record/entry-array bounds are fixture limits; the original arithmetic does not establish a global capacity or validate arbitrary handles. No physical graphics transfer is invoked or claimed.

The zero-duration early return is also tested with an otherwise out-of-range synthetic handle, proving that it bypasses transfer-state access. Separate controls stop before an extension-table overread or an out-of-range transfer-record store. All four targets exclude post-fault state and return credit; their already completed setup returns remain separately counted.

The direct apply interface is treated as void. Its original caller chain ultimately discards its machine R0 in the roster initializer. Direct C/native R0 differ in 252 contexts and are recorded separately rather than invented as a numeric API result. Small signed SDK rotation/translation parameters compare their relevant low16 bits, while both raw argument words remain in the report. Complete memory effects and preserved registers still must match. This is a qualified semantic draft, not a full ABI claim for every possible caller.

## Failed matching and provenance

Source, inline Boolean helpers, typed layouts, verified archive revisions and optimizer profiles remain preserved as zero-credit experiments. Earlier unadopted profile batches had two bookkeeping limitations: row flags referenced a mutable list, and nonmatching link directories omitted compiler identity. `sdk_animation_negative_profiles_v2_20261030.py` replays28 trials with immutable flag/compiler snapshots and source/compiler/profile-specific link directories, then rechecks every captured linked hash after all trials. Its correction report SHA-256 is `b07de72c3d1fed2b0e854d82b0fec30b1d603d9cf44fc39da180914df8df9029`. Original negative reports are retained as superseded evidence. No accepted source, canonical match, shared preference or registry was changed by that repair.
