# ARM7 buffer fields, 2026-10-29

The 252-byte ordinary C body at ARM7 main address `0x027F1584` now matches every native instruction and literal-pool byte. It constructs buffer fields from a shared pointer, prefix/length words, flag bits, payload bytes, and a shared halfword; it optionally writes two marker halfwords and clears a state field. Packet and marker interpretations remain structural inferences.

## Reproduction and the final type correction

Run `python verify_arm7_20261029_packet.py`, including by absolute path from a different working directory. The frozen source is `src/arm7/20261029packet32/native_arm7_main_027f1584.c`; the report is `evidence/matches/arm7-20261029packet32.json`.

The initial draft matched 250/252 bytes. Its signed halfword store of `0xB6B8` caused a sign-extended constant in the literal pool. The native literal is zero-extended. Changing that store's pointee type to unsigned 16-bit retains the measured two-byte write and reproduces the complete native pool. There is no assembly, instruction patch, or embedded executable byte array.

The pinned MW compiler freshly builds this unit with ARM7TDMI, `-O2`, and `-inline off`. The real pinned `mwldarm` resolves the original code/data relocations at qualified ARM7 function addresses and the two measured shared-RAM locations. Actual linked caller bytes and symbol boundaries must match. Uninitialized mode anchors supply zero executable callee bytes and zero callee source credit.

## Independent bounded execution

There are 576 paired fixtures and 1,152 actual returning executions, each in a fresh native or source Unicorn machine. Eight payload lengths include zero, odd/even lengths, and `255`; six prefix lengths exercise both alignment branches; marker presence, three shared halfwords, and both ARM/Thumb returns are covered. Every caller instruction executes across these fixtures.

All three measured native helper bodies execute directly: the rounded-copy wrapper at `0x027EAC88`, the halfword-preserving byte writer at `0x027EAD30`, and its copy-loop target at `0x037FDF9C`. They are runtime scaffolding with zero new source credit. No synthetic callee return contract is used.

The independent model checks rounded-even payload copies, unchanged neighboring bytes during byte writes, header length, byte truncation, aligned marker placement, the final state reset, all ordered halfword stores and call arguments, complete 4 KiB buffer/record RAM, an unchanged complete 4 KiB shared-word page, return R0, preserved R4–R11/SP, and return modes. Full register/NZCV state and native stack writes additionally agree between native and compiled machines.

Fixture lengths keep all aligned payload copies and fields inside valid bounded RAM. Arbitrary overlapping/unmapped pointers and physical wireless-memory effects are unsupported. No external transmission occurs. This caller proof remains distinct from a reconstructed module or whole-ROM source build.

## Discovery

All 485 previously unmatched ARM7 candidates were rotated with corrected scalar/ABI/stack hypotheses. Ranking rejected near matches exposed this constant-pool type discrepancy. Other rejected drafts remain failures; their assembly and successful compilation are not decompiled-source credit. The integrator owns shared registration and accepted module builds.
