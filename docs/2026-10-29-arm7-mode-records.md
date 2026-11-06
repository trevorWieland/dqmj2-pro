# ARM7 mode records, 2026-10-29

The 248-byte ARM7 main caller at `0x027E54E8` now matches ordinary C. It truncates an input mode, chooses an enable word, copies or clears 80 bytes, stores a setting, calls a provider using a 512-byte stack buffer, optionally fills a status message, and always fills a final message header. Command, message, and enable names describe the measured structure rather than recovered original API meanings.

## Reproduction and source correction

Run `python verify_arm7_20261029_mode.py`, including by absolute path from another working directory. Its frozen source is `src/arm7/20261029mode34/native_arm7_main_027e54e8.c`; the report is `evidence/matches/arm7-20261029mode34.json`.

The draft matched 241/248 bytes. Moving the equivalent duplicated `default` switch block to the end reproduces the native branch-table/block order and matches every byte with pinned ARM7TDMI `-O2`, `-inline off`. No assembly or instruction patch is used.

The verifier removes previous mutable compiler outputs and independently links the compiled caller with the actual pinned MW linker. Qualified main/WRAM ARM function bindings and the original data relocation must resolve to exact native caller bytes and symbol bounds. Mode anchors emit zero initialized callee bytes and contribute zero source credit. No original executable object contributes to the caller link.

## Independent bounded execution

There are 1,728 paired cases and 3,456 actual returning executions in fresh native/source Unicorn machines. Nine raw mode words include default/enable modes and upper-word truncation; four response halfwords include zero and high-bit values; four source alignments, three final results, two response placements, and both ARM/Thumb returns are exercised. Every caller instruction is covered.

The measured native copy and clear helpers execute directly as runtime scaffolding with zero new source credit. The independent model checks complete 4 KiB request/context/payload/response/message RAM, an unchanged complete 4 KiB shared-pointer page, copy/clear effects, every ordered caller field store, every call argument, optional/final message headers, return R0, preserved R4–R11/SP, and return modes. Full register/NZCV state, native/helper stack writes, and final stack hashes additionally agree between native and source.

The provider contract fills all 512 scratch bytes after checking that the buffer stays below the saved frame, then returns either an independent response pointer or that stack buffer. Allocation/send providers supply valid message buffers and explicit return/ABI-clobber effects. These contracts do not execute physical command handling or communication. Invalid context/request/provider pointers and undisclosed provider side effects remain unsupported.

The integrator owns shared registration and accepted module builds. Caller equality and bounded execution remain distinct from complete module or whole-ROM source recovery.
