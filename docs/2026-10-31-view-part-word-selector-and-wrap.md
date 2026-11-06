# Full-word view selection and wrapped range predicates

The new ordinary C source `src/mechanics_save/20261031_lane_view_parts/native_main_02074764.c`, SHA-256 `7396b60857571c2ec765a6fd5e74205164efbb24aa39b92126b9ca11abaf428c`, reconstructs main ARM9 ARM `0x02074764..0x0207483C`, 216 bytes. All code and literals genuinely compile/link to the measured input with pinned MW2.0 base and the explicit flags in the report. This packet proposes 216 new native bytes, pending integrator module/ROM acceptance. It makes no central registry or source-preference changes.

Run `python match_mechanics_save_20261031_lane_view_parts.py`. Canonical report `evidence/matches/mechanics-save-20261031-lane-view-parts.json` is SHA-256 `fd67824a0135ec718efdbeec89622460d834934b4c10e2dd556e58011deae036`, reproduced from both the repository and its parent working directory. Native vector digest is `efa14d7d9783ee0e9e034f0a7ae5895118d5a8d100221c4a012ac37c9938e7a7`. Current source/object/native/real-link identities are checked each run; old-root debug/object bytes are not assumed reproducible identities. The canonical command produces its own fixture and control reports without consuming unmaterialized generated goldens.

## Two source-type corrections

The original instruction at `0x02074774` loads a complete word from `0x021C5A24`. The broad m2c draft instead declared a byte array and loaded its first byte, matching 215 of 216 bytes after genuine linking. The corrected source declares this particular selector as an unsigned word. This evidence does not justify blanket width changes to other globals. Values 1 and 3 select views `0x021C5A30` and `0x021C5B20`; all other full words select no view. Synthetic values `0x101`, `0x103`, and `0x01000001` expose the first-byte hypothesis's different behavior.

The second predicate adds a signed word at view `+4` to an unsigned halfword at `+0x0C`, wraps to 32 bits, interprets that word as signed, and compares it with the unsigned halfword at `+0x0E`. A promoted signed addition in C can overflow before its outside cast. The new source casts the first operand to unsigned before adding, then uses the target's signed-word conversion. This matches the native wrap and signed comparison without signed-overflow arithmetic. The separate first predicate is simply signed offset greater than zero. Negative/extreme offsets are bounded synthetic tests, not assertions about legal ordinary menu state or unconditional navigation restrictions.

Both natural type corrections preserve all 216 native bytes. The raw draft, its compiler/link receipts, and the specific one-byte load mismatch are retained at `evidence/attempts/save-core-view-parts-byte-global-hypothesis-20261031.json`. That older draft receives no source credit and is not the preferred hypothesis.

## Actual helper effects and dependency limits

Original overlay-0 getter `ov000:ARM 0x02215698` returns context address `0x022459B4`; byte `+0x494` must be 3, 4, 9, or 10 for the update path. The overlay is explicitly loaded from its measured module mapping; no other overlapping overlay is inferred. The chosen view's word `+0xC4` is the actual part-array base used by the native helper, not merely a guessed boolean guard.

With a nonzero part-array pointer, original main `0x0204B138` executes twice with container `view+0xA8`, indices 0/1, and the two measured predicates. Original `0x0205F98C` performs the 144-byte part stride. Each part's word `+0x7C` has mask `0x2` set or cleared. Setting an already set bit makes no write; clearing always stores the resulting word. All other bits are preserved.

Original `0x020496B0` then visits both parts, calling `0x02048A44(part+8,1)`. The latter tailcalls `0x0203515C` with second word 8192, which actually calls `0x02034D68`. These helpers execute originally with zero providers. The fixture explicitly sets each animation controller word `+0x0C` to 0, 2, or `0xFFFFFFFF`, so the actual tick takes its native inactive branch and returns zero. No active-animation result is simulated. State 1 reaches a declared unsupported boundary in each engine; partial part writes before that stop are excluded. Active frame application, callbacks, resource use, and ordinary visible behavior remain unresolved.

The helper mask writes are concrete transient state mutations. They are not called presentation-only or used to infer persistence, ownership, or scene eligibility. The routine always returns physical zero in this corpus; no success-status meaning is assigned.

## Returning matrix and rejection control

The matrix crosses seven full selector words, seven context bytes, null/non-null part arrays, five signed offset boundaries, three heights, and three totals. It has 4,410 original/compiled pairs and 8,820 actual top-level returns. Native helper entry completions total 18,180; distinct native return boundaries total 16,740, with the tailcall distinction retained. The two engines perform 1,120 checked data-word writes and use zero providers. Two active-controller stops are unsupported and contribute no return or post-fault credit.

The independent model checks full-word gating, each predicate's signedness and wrap, exact conditional mask writes and preserved bits, exact helper arguments and returns, full disposable part/view snapshots, registers/CPSR, stack hashes, restored SP, and actual bounded termination. All original and complete-C observations agree.

Run `python evidence/application/save_core_view_parts_controls_20261031.py`. Its report SHA-256 is `99cc1e4dfdebd2454d5d1effff08fe1c09a1f29478fb590795e446df2b12e95f`. A complete 216-byte wrong C function changes only the selector back to a byte-array view while retaining defined wrapping arithmetic and all original SDK helpers. It genuinely compiles and links. Three high-word contexts wrongly mutate actual part words and fail the independent memory model; three low-word controls preserve memory. All six original and six wrong-C runs return zero, so the control does not mistake a return value for evidence of correct effects.

Original ROM/save inputs, earlier accepted source, baseline, and application remain untouched. The 40,560 semantically unknown save bytes remain preserved and unclassified. No original executable or generated assembly is credited as reconstructed source. Complete module closure, earlier regressions, and repeated whole-ROM acceptance remain the integrator's responsibility after this source-only packet is imported.
