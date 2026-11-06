# Card common initializer, 2026-10-29

The reconstructed ordinary C at `src/mechanics_save/20261029_card_common_initialize.c` matches main ARM9 ARM function `020100E4–020101F4` completely: 272 bytes, including seven literal words. The pinned MW2.0 base compiler and actual pinned MW linker produce native span SHA-256 `61244f0430532069b1279a3b9e3c0a226b7eab537234c8fd2707202aa038a893` without executable blobs, assembly, relocation rewriting or binary correction.

The measured input ROM is 175,959,612 bytes with SHA-256 `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`. The source SHA-256 is `0da0581a4a5de50528577e13349a9934e9fd39f782df815c53e1af1d854c9ff9`; its object SHA-256 is `c05be8883a12c3f54a9e293b190a859a41f77a6d43ba960557dec4c50b28f134`.

Reproduce with `python match_mechanics_save_20261029_card_common.py`. Absolute-script invocation from `C:/Users/trevo/Documents/Codex` also passes with the same object identity. Logs are `work/mechanics-save/20261029-common/accepted-run.txt` and `different-cwd.txt`. The complete current machine-readable result is `evidence/matches/mechanics-save-20261029-card-common.json`.

## Compiler and source boundaries

This unit uses MW2.0/base SHA-256 `7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880`, ARM946E, O2 speed, inline functions enabled and the existing private license-file setup. The measured common object at `020E5500` has an explicitly declared 32-byte alignment. That declaration removes a redundant pointer move and changes register scheduling; O2 speed supplies the native conditional return. Neither setting establishes other source units' settings.

The reference `ntrtwl/NitroSDK` commit `1958e1ef5547b076c793047b0fc0e39e79b416c7` preserves `CARDi_InitCommon` and related card, thread, memory and multiboot interfaces. Its common object declaration explicitly requests 32-byte alignment. Hashes, URLs and local immutable reference snapshots are indexed by `evidence/save/20261029-card-common-source-reference.json`. This is qualified third-party preservation, with no authenticated vendor archive or proof of the exact game SDK version. It supplies no assembly exception or build dependency. Reconstructed types, opaque thread storage and two volatile 16-bit boot observations remain constrained by measured native instructions and the full-byte match.

The earlier unsuccessful experiments and their diagnostic partial-byte scores remain zero-credit evidence. The original attempt index is retained; subsequent SDK-interface/alignment attempts have a separate `evidence/attempts/20261029-backend-common/sdk-shape-and-alignment/index.json`. Only the full current matched report qualifies these 272 bytes.

## Bounded execution evidence

The independent oracle runs 917 deterministic cases as 1,834 fresh Unicorn machine executions. It executes only the newly linked 272-byte initializer and the already accepted, independently relinked 16-byte enable setter at `0201021C`. No native callee bodies are retained in the recovered-source execution and the setter earns no additional credit. All 61 initializer instruction addresses are visited. Each execution must actually return within 2,000 instructions; execution of literal pools or undeclared callees, writes outside the explicit state windows and failures to restore preserved registers/SP are rejected.

An independent state/call model checks the entire 4 KiB common arena and 4 KiB shared-header page. Native/source comparison also checks the complete 32 KiB stack, ordered memory writes, register results, CPSR and call order. Fixtures cover all low-byte boot values and selected full 16-bit boundaries, independently change the boot mode during callback registration, and repeat initialization over previous output state.

Measured observations include descriptor pointer/96-byte clearing, lock value `FFFFFFFD`, zero reference/target, both zeroed queues, priority four, two `FFFFFFFF` thresholds, conditional 352-byte header copying, and thread creation with the measured six arguments: thread address `020E5544`, task `02011244`, null argument, stack endpoint `020E5B20`, stack size 1024 and priority four. FS FIFO registration uses channel 11 and callback `02011210`. The second full halfword read independently controls the accepted enable setter at `0201021C`.

Clear/copy/cache, thread creation/wake and FIFO registration are six explicit synthetic platform boundaries. Their argument contracts and controlled effects are tested; physical cache behavior, scheduler operation, IRQ safety, task/callback execution, FIFO timing, backup-device protocol and concurrent initialization remain unsupported by this isolated proof. The declared void interface makes no semantic return-value promise, although all final architectural result registers are compared.

The earlier frozen backup boot, backend initializer and accepted helpers remain unchanged. These are function-level source/link/effect results; the integrator owns shared-ledger acceptance and full module/ROM regression.
