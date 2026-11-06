# Parallel source cohort 120 — 2026-11-01

This packet proposes seven ordinary C functions and 1,584 initialized module bytes. The integration specification, current validation reports and committed closure determine acceptance. Research and exact byte hypotheses alone have zero accepted source credit. Earlier accepted source and object identities must remain unchanged.

| Processor/module/mode | Address | Initialized bytes | Measured behavior and scope |
|---|---:|---:|---|
| ARM9/main/ARM | 02039F2C | 120 | Forwards complete nonnegative incoming words to a ten-word callee; negative values select record bytes. Explicit word prototypes replace accidental byte truncation. |
| ARM9/main/ARM | 020193F8 | 36 | Preserves the incoming word across the IRQ helper call. The bounded mismatch-return path executes the original IPC wrapper and IRQ restoration; deeper IPC contexts remain unsupported. |
| ARM9/main/ARM | 0203A4FC | 88 | Preserves the incoming object pointer on the direct branch and tests the flag using an unsigned shift. Interfaces agree with selected pointer-taking callees. |
| ARM7/arm7-main/ARM | 027EA584 | 76 | Reads the qualified state fields with zero owned writes or calls. Producer setup and boundary controls are separate evidence. |
| ARM9/ov005/ARM | 021E6704 | 1000 | Converts the bounded synthetic record contexts, preserving full registers, flags, RAM, ordered writes and supplied-call words. Actual surrounding helpers execute where qualified. |
| ARM9/main/ARM | 020445E4 | 180 | Builds the resource output using explicitly supplied formatter and loader boundaries. Path naming and application meaning remain qualified only by evidence. |
| ARM9/main/ARM | 0205C448 | 84 | Finds the first zero slot marker and executes the actual 43-word clear over the selected 0xAC-byte record. The caller's semantic cache ownership remains unknown. |

The superseded Root244 raw-word candidate is not selected. Its earlier byte match did not establish a coherent C interface with the selected pointer-taking callees. The replacement preserves explicit compatible prototypes and separately reproduces the full machine comparisons from an unrelated working directory with Python `-I -S`.

Before sealing, Root244 passed 1,152 actual top returns, 480 actual native helper returns, 1,056 supplied calls and 384 returning wrong-source executions, producing 153 model rejects and 231 positive controls. ARM7 state76 passed 352 actual top returns plus 352 separate producer-fill returns. Overlay record682 passed 64 top returns, 6,848 native helper returns and 2,174 supplied calls. Save resource/slot passed 1,740 top returns, 1,392 native helper returns and 4,032 supplied calls; its 16 wrong-source returns contain four model rejects and four positive controls. These are bounded fixture results rather than general game execution claims.

## Research retained with zero source credit

The previous private ov005 record670 C body is a functional hypothesis with explicit physical scratch differences. Its later record682 replacement achieves canonical linked bytes; the old failed heap-context experiment remains recorded. The save row-builder research uses the measured full-word field access and actual helper execution. The variadic context research retains the previously omitted argument under narrow input pins; the three pointer-to-word source variants remain nonmatching. ARM7 helper128 preserves a private functional comparison, with the recorded scratch-register and read-order limitations and no canonical source credit.

The repository-local decomp-permuter dependency is the unmodified public commit `8556c81d80d1c1af98a858c8f4dc951357f29139` from https://github.com/simonlindholm/decomp-permuter. Its archive SHA-256 is `46866946297f37e1f81c9ba1933d4406fe1c5660264a7c9b5771bbfa0b73ef27`. All 255 source files were independently checked against Git tree/blob identities. Only the local AST API is used; no distributed worker or upstream compiler/scorer is used. Its pinned dependency, restricted adapters, acquisition and smoke reports are retained. The first 192 local trials produced 162 genuine linked outputs and zero exact matches; the best residual still has an extra conditional-read difference. It receives no source credit.

## Coordination and reproduction

Three workers own independent ARM7, overlay and save/core repositories and output directories. The integrator owns the primary ARM9 lane, shared registry, ledger and accepted builds. Broad drafting and compiler jobs run within lanes; shared acceptance remains serialized. Drafted, compiled, byte-exact, native-validated and module-linked stages are separate measurements.

Run `python prepare_cohort120_parallel_20261101.py --save-manifest evidence/lanes/save-core/resource-slot198-ready-v2-20261101.json --save-report evidence/matches/mechanics-save-20261101-lane-resource-slot.json --save-producer match_mechanics_save_20261101_lane_resource_slot.py --save-archive save-resource-slot198-20261101`, then use the versioned continuation driver with `cohort120-parallel-specification-20261101.json` and `stage_cohort120_parallel_20261101.py`. Packet-specific commands and immutable original worker evidence are retained in the package and provenance archives. `python reproduce.py` remains the checksum regression entry point.

All twenty module comparisons, both checksum matches, 144 isolated checksum returns, 5,117 getter comparisons and the exact original-length/SHA ROM must pass before acceptance. The ROM still includes explicitly marked original executable scaffolding. No full source-only ROM, full Windows game, Android device execution or dual-screen game UI is proved here. The application's independent edits remain visible in the strict workspace audit; this work does not modify application adapters or UI. All 40,560 semantically unknown save bytes remain unknown.
