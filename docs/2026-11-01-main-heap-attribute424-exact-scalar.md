# Exact scalar heap attribute source - 2026-11-01

`main:ARM0202AE9C/424` now rebuilds through the pinned compiler and real MW linker with all 424 bytes equal, including 416 instruction and eight literal bytes. The preferred ordinary C source is `src/main_sdk_aux/20261101_heap_attribute424/native_main_0202ae9c.c`, SHA-256 `0b5bc1dd7565b4983a350a589cd84c6107eb03d37be18c8134f1aa6c47861adf`. Shared registration, selection, module integration and whole-ROM acceptance remain the integrator's responsibility.

The old measured-view candidate was 422/424, differing only in one commuted ORR. Its source, fixtures and earlier trials remain untouched. This alternative uses plain `u16` attributes and a group-update block with ordinary `u32 maskBits` and `u32 newValue` temporaries. The demonstrated direction/alignment source lifetimes are preserved. Compiler and flags remain MWCC2.0/base, O2 and inline-off. There is no assembly, opcode manipulation, fixed register, fabricated alignment, added volatility or flag sweep. The generic zero shift in the group block comes from the reconstructed SDK field helper; it produces no padding instruction.

## Comparative SDK evidence

The pinned comparative repository is [RushRE/SonicRushAdventure-Decomp](https://github.com/RushRE/SonicRushAdventure-Decomp/tree/fb9b7e4dd9b5babbc114d6165f0279352bd11ecc). Commit `fb9b7e4dd9b5babbc114d6165f0279352bd11ecc` names tree `f3a9273c5ab90fb6acb452226f1518edd74da271`. Seven raw files are verified by Git blob identity, byte length and SHA-256 and retained unmodified under `deps/references/sonic-rush-adventure-fb9b7e4d-heap-20261101`.

Its [private foundation header](https://github.com/RushRE/SonicRushAdventure-Decomp/blob/fb9b7e4dd9b5babbc114d6165f0279352bd11ecc/lib/NitroSystem/src/fnd/include/heapcommoni.h) uses unsigned word mask/new-value temporaries before clear and OR assignments. Its block header uses a scalar `u16` attribute. These facts motivated the new source; the reference is not a compiler input, not assigned CC0 and not proof of the game's historical SDK revision. The reference allocator explicitly changes its minimum free-block size and has different fill behavior. The game's measured 20-byte split threshold, debug-fill behavior and original helper ABI remain authoritative. Neither public behavior difference was adopted.

A diagnostic volatile counterpart also matches 424 bytes. It is retained separately with zero additional definition or byte credit. Applying the public macro shape to all three fields instead left four alignment-related register-role differences; that failed trial is retained. Only the successful scalar group update is preferred.

## Independent execution

There are 560 fresh original/compiled-C pairs, 1,120 actual owned returns and 9,120 separately observed original-helper returns. All six lower routines execute without supplied outcomes. The original independent fixture `main_heap_commit_fixture_20261101.py`, SHA-256 `1255df3abda60dc1934320d195d3b3c5e8f766ec1ffd57149a1892192c2cda8b`, remains unchanged. A separately named instrumented copy preserves its heap model and adds full register/APSR, ordered read/write, helper-argument and complete mapped RAM/stack comparisons. Every caller instruction is visited. Both ARM and Thumb return sentinels are exercised.

The matrix uses one selected free block, zero/one pre-existing used node, requests `0/4/20/64/128`, measured gap boundaries, all four low flag combinations and deterministic full-u16 group/direction inputs. Valid bounded synthetic layouts are supported. Malformed/cyclic/concurrent heaps, scene feasibility and native 64-bit/Android portability are not established. The original 32-bit address/view ABI is explicit.

Four ordinary-C negative bodies are freshly compiled and genuinely linked, then executed against the independent model. Wrong used marker, group bit, fill mode and free-split threshold produce 2,240 actual returns and 1,151 model rejections. The fill mutation has a shorter linked body; its entire generated body is used and no original tail is credited. There are also 35 metadata, availability and exhaustion controls. Helper/data/assembly/extent and denominator credit remain zero.

## Reproduction and artifacts

Run `python validate_main_sdk_heap_attribute424_20261101.py` from any working directory. It regenerates the canonical match report and fresh C/object/ELF/linked products before validation, repeats the positive native/source proof and rebuilds all wrong-C controls. Source/runtime/tool/reference inputs are hash-gated by the final profile and 213-file pin set. Main native-symbol addresses are published as hex strings.

Supported and wrong-source traces are deterministic mtime-zero gzip with raw/compressed hashes. No cached objects, original executable compiler inputs or WORK products are required in transport. Repeated checks preserve the scalar source bytes. Full accepted-module and ROM construction stays pending until the integrator runs its complete regression gates.
