# ARM7 sampled-register records, 2026-10-29

The complete ARM7 WRAM callers at `0x037FD898` and `0x037FD928` now match ordinary C, 144 bytes each. They guard a null/in-use record, sample a halfword at `0x04000006`, obtain a counter-like word, conditionally advance it using a signed threshold comparison, populate record fields, call an insertion-like routine, and restore the interrupt mask. Their bodies differ in the word written at offset `0x1C`.

Scanline, counter, insertion, and periodic-state interpretations are structural hypotheses. Native API names, record types, and physical hardware timing remain unproven by this caller evidence.

## Reproduction and linking

Run `python verify_arm7_20261029_scanline_records.py`, including by absolute path from another working directory. The verifier pins the two sources under `src/arm7/20261029rotated30/`, the compiler, and the linker. It writes `evidence/matches/arm7-20261029rotated30.json` after every compiler, linker, and execution gate passes.

Fresh ARM7TDMI compilations must match every native byte after the original declared relocations. Actual `mwldarm` links resolve qualified canonical ARM function entries and the exact halfword hardware-data address. Linked bytes and function symbol boundaries must match. Zero-sized function symbols in uninitialized mode-anchor sections supply no initialized callee bytes or callee source credit. No original executable object contributes to either caller link.

## Returning fixtures and separate guard checks

The returning suite comprises 1,344 paired cases and 2,688 actual returns across both functions. Each run starts in a fresh Unicorn machine. It covers six sampled halfwords, seven signed thresholds, zero/maximum counter words, all four incoming IRQ/FIQ-mask combinations, and both ARM/Thumb returns. Additional inputs exercise signed halfword truncation, opaque handler/data words, and the fifth incoming stack argument.

The independent model checks the complete 4 KiB record arena, every typed store and its order, every call and argument, exactly one halfword hardware read, an unchanged complete 4 KiB synthetic hardware page, unsigned counter wrap, native R0, preserved R4–R11/SP, and interrupt/return modes. Full register/NZCV state and native stack writes additionally agree between native and compiled executions.

Null and in-use guards have a separate 16 paired cases/32 executions. They must reach canonical panic entry `0x037FDE70` before any object or hardware write. The verifier deliberately stops there. These guard-boundary checks make no actual-return or panic-body claim and are excluded from the returning suite. The union of returning and guard checks covers every caller instruction.

The measured native IRQ helpers execute as runtime scaffolding with zero new source credit. Counter and insertion implementations use explicit deterministic return/ABI-clobber contracts. Physical register timing, queue effects, panic behavior, and arbitrary malformed pointers remain unsupported.

## Discovery and acceptance

This rotation researched 128 further unmatched ARM7 candidates. The other 126 remain rejected in `evidence/attempts/arm7-20261029rotated30.json`. Generic unmapped-pointer failures prompted the dedicated fixture model; they are not treated as successful executions.

The integrator owns shared ledger registration and accepted module builds. These two caller matches make no whole-module or whole-ROM source-completion claim.
