# ARM7 word packing, 2026-10-29

The 160-byte ARM7 WRAM caller at `0x03802A0C` now matches ordinary C. It reads a mode word from a pointed context, packs input bits differently for modes 1/2/3, and passes a four-byte stack word plus three other argument words to one helper. Original API names, the fixed fourth-argument address's meaning, and peripheral behavior remain unproven.

## Reproduction and matching

Run `python verify_arm7_20261029_pack.py`, including by absolute path from another working directory. The frozen source is `src/arm7/20261029pack33/native_arm7_wram_03802a0c.c`; the report is `evidence/matches/arm7-20261029pack33.json`.

The decompiler's `(u16)(arg0 << 8)` produced a 156/160-byte match. Expressing the same defined unsigned value as `((arg0 & 0xFFU) << 8)` produces the native register allocation and matches all 160 bytes with the pinned compiler's ARM7TDMI `-O2`, `-inline off` configuration. No assembly or instruction patch is used.

Fresh compiler outputs and actual MW linker outputs must reproduce the complete caller span and symbol boundary. The function binding has a qualified canonical ARM7 ARM entry; the two data/address words retain their measured targets. The uninitialized mode anchor emits zero executable callee bytes and contributes zero callee source credit. No original executable object participates in the caller link.

## Supported execution and explicit limits

There are 1,200 paired valid-mode cases and 2,400 actual returning executions, each using a fresh native/source Unicorn machine. Modes 1/2/3, input byte/bit boundaries, overlapping flag bits, four helper results, and both ARM/Thumb returns are exercised.

The independent model checks the complete four-byte packed stack value, every helper argument word, unchanged complete 4 KiB context and shared-pointer pages, result R0, preserved R4–R11/SP, and return modes. All native/source register and NZCV values, stack writes, and final stack hashes additionally agree. The helper itself is a deterministic return/ABI-clobber contract; it performs no physical device or external communication.

Modes outside 1/2/3 leave the native stack word uninitialized and remain unsupported. Three separate paired boundary probes for modes `-1`, `0`, and `4` stop at the canonical helper entry before interpreting that word. Their six executions make no return or packed-value claim. The union of valid-mode and boundary fixtures covers every caller instruction.

Shared ledger registration and accepted module builds remain the integrator's responsibility. These isolated caller results do not establish a complete module, peripheral implementation, or whole-ROM source build.
