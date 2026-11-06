# ARM7 coordination callers, 2026-10-29

Three new ordinary C callers match 384 complete native bytes in the canonical ARM7 WRAM module:

| ARM entry | Bytes | Measured structure |
| --- | ---: | --- |
| `0x037FBA94` | 116 | Select an interrupt-mask pair, call a two-word test, optionally invoke a callback and write a halfword on zero result, restore the mask, and return the test result. |
| `0x037FC888` | 132 | Inspect a global owner pointer, increment a nesting word, append an unowned object, or wait through an owner-change loop. |
| `0x037FD5C0` | 136 | Guard an inactive record, unlink active neighbor fields/global endpoints, optionally call a next-record handler, and clear three record words. |

Mutex, scheduler, and alarm interpretations are hypotheses based on these operations. Native API names, declarations, and full lifecycle invariants are not established by this report.

## Reproduction and linking

Run `python verify_arm7_20261029_coordination.py`, or invoke that script by absolute path from another working directory. It writes `evidence/matches/arm7-20261029rotated29.json` after every gate passes. The three frozen sources are under `src/arm7/20261029rotated29/`.

The verifier pins the source hashes and MW compiler/linker hashes, regenerates canonical ARM7 boundaries, removes prior mutable compiler outputs, and compiles all caller bodies targeting ARM7TDMI. Every byte must match after the original declared relocations. The actual MW linker then resolves those relocations at measured caller/callee/data addresses and produces the same complete caller bytes and symbol spans.

Function bindings use canonical ARM entries represented by zero-sized function symbols in uninitialized mode-anchor sections. These anchors emit no initialized executable bytes and receive no callee source credit. Data assignments retain the exact measured relocation targets. No original executable object contributes to the caller link. A source-only isolated caller link remains distinct from a reconstructed module link.

## Bounded execution

There are 472 paired cases and 944 actual returning executions. Each native and compiled run starts in a fresh Unicorn instance with its own deterministic RAM, registers, globals, stack, and privileged CPU state. All four incoming IRQ/FIQ-mask combinations and both ARM/Thumb return modes are exercised. Every caller instruction is covered; literal pools are excluded from instruction coverage.

The independent sequential model checks complete 4 KiB object RAM and a complete 4 KiB synthetic global page, ordered modeled stores, call arguments and ordering, result R0, preserved R4–R11/SP/LR, and restoration of original IRQ/FIQ control bits. Other register/flag state and native stack writes additionally agree between native and compiled executions.

The measured native IRQ helpers at `0x037FDD00`, `0x037FDD14`, `0x037FDD2C`, and `0x037FDD40` execute directly, as does the measured append helper at `0x037FC9A4` when reached. Their original bytes are runtime scaffolding and contribute zero new decompilation credit. Reports derive actually reached native helper sets per caller.

Remaining callees are explicit bounded contracts: the test at `0x037FE2AC` returns each selected zero/nonzero word; callbacks exercise null, ARM, and Thumb entries with deterministic volatile-register/NZCV clobbers; the wait at `0x037FC290` follows finite one- or two-wake owner plans; and `0x037FD2C0` records its next-record argument. Native implementations of those callees, actual context switching, physical interrupt delivery, and timer timing are not established.

The first caller covers both interrupt-mask pairs, zero/nonzero results, callbacks, and truncating halfword stores. The second covers free ownership, recursive ownership, one/two waits, transition to free or current ownership, zero/wrapping nesting words, and empty/nonempty append tails. The third covers inactive/active records and all four null/non-null neighbor endpoint topologies. Arbitrary unmapped or unaligned pointers remain unsupported inputs.

## Discovery and acceptance

The preceding 64-candidate rotation produced no full match; its failed attempts remain in `evidence/attempts/arm7-20261029rotated28.json`. This rotation researched 128 additional previously unmatched candidates and admitted three complete matches. All 125 rejected results remain in `evidence/attempts/arm7-20261029rotated29.json`.

No partial match or synthetic callee contract counts as recovered callee source. Shared ledgers and accepted module builds remain the integrator's responsibility; this report makes no whole-module or whole-ROM source-completion claim.
