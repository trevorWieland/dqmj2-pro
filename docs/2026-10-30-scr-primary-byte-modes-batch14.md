# Complete primary-predicate byte-mode source — 2026-10-30

World entry12, code `[52244,53244)`, is reconstructed in `src/scripts/20261030/batch14/apply_primary_byte_modes.c`. A source-only rebuild emits all1,000 original bytes exactly. This is the original-only `apply_saved_world_argument` dependency in the frozen entry32 proof; that older proof/manifest remains unchanged.

The C function has one float formal, six primary getter/conditional branches and named `select_context_byte_mode` calls. The formal is copied into private VM slot81 before API arguments are reused, even though the function's own logic never reads it. The primary predicates use slot82. Current encoded-reference analysis finds no outside read/write of these slots, public interior entry, external direct interior branch or shared return tail. One private RET is at53240. Opaque/native/computed references and global program control remain unproved.

## Lowering and actual native effects

Separately versioned `scr_c_compiler_20261030_v12.py` preserves the frozen formal/definite-assignment scalar backend and adds the typed two-argument byte-mode API. The accepted source/profile namespace and closure are frozen; general C compilation is not claimed. Logical indices0..18 and modes0..3 are supported. These are compiler-supported domains, not native error checks.

Actual SYS103 dispatch at`main:ARM0205B6F8` calls`02054C1C`. It converts both arguments to integers, constructs four bytes with100 in the selected mode lane and zero in the other three, maps the logical index through actual`020725E8`, then calls actual`020C1FDC` to copy four bytes to`020E2CF4 + mappedRow*4`. Native helpers, initialized data outside the selected source range, and all remaining original code remain zero new source credit. The logical mapping is `[0,3,2,1,3,6,0,5,4,7,8,9,10,11,12,13,14,0,15]`; aliases/default row0 are measured without ownership or validity meanings.

The source tests primary207/208/209/210/212/211 in order. Each false predicate selects mode0 for logical2/3/4/5/8/7 respectively; a true predicate preserves that row. No story/area/access/renewability meaning is assigned to these raw flags, rows or byte values. Source contains ordinary named calls, variables and structured conditions; it contains no opcodes, PC constants, assembly or executable arrays.

## Complete proof and controls

The full original-versus-source-recompiled proof passes1,024 complete entry executions and48,384 actual native VM/helper returns. Each implementation uses256 fresh contexts: all64 flag patterns and all4 VM threads, with two serialized calls per context. All six branch sites take both outcomes and all own records execute. Bounds are128 script steps and20,000 instructions/1,000,000 microseconds per native call. No provider or source/native function stub is used.

The formal's raw32-bit representations include positive/negative zero, one, positive/negative infinity, quiet/signaling NaN payloads andFFFFFFFF. The second invocation changes the argument. Every captured word remains exact. This is the qualified SCR raw-binary32 copy ABI, not a promise that every host compiler preserves NaN payloads through arbitrary numerical float conversions. A native Android port must retain the raw-word bridge when these effects matter.

Each scenario randomizes all256 variable words and the guarded64-byte table. Only slots81/82 may change. Ordered four-byte stores, all table rows/neighbors, complete persistent state, VM state, general registers/CPSR and ordered CPU-store observations are compared. Reentry preserves the same final rows while still performing selected native writes; this does not prove game renewability.

Eight unsupported source/domain profiles reject before a product returns. Seventy-six separate zero-credit source-built controls execute all19 logical indices and all4 modes, including the last row and logical aliases, for608 actual native returns. Those counts remain separate from the original-function proof.

## Reproduction and ready acceptance

Run the following with pinned Python3.13.5/Unicorn2.1.4:

```powershell
python match_scr_byte_modes_20261030_batch14.py
python validate_scr_byte_modes_20261030_batch14.py
python verify_interpreted_byte_modes_sources.py
```

The matcher passed the full source-only/current-image and native proof. The standalone accessor performs another isolated source-only rebuild, validates current ROM/module/image/direct/private/slot/native-ABI identities and every supported action/trace/store/return/state record, then returns one qualified unit. It passes from the repository and its parent directory. The registry adapter invokes that frozen validator and separately tracks source, complete-entry, native and synthetic-control counts. Its22 meaningful mutation controls plus positive validation pass. Missing source products withhold credit. No shared registry/framework/ledger was edited; Root owns acceptance.

| Frozen artifact | SHA-256 |
| --- | --- |
| v12 compiler | `0452b7c010993dea523cf92fda01d72fc83a7a0aea318f33886fdc836c0bb271` |
| batch14 matcher | `f47a610f68ab4c3c1506fb264b5bef6fb0ca4548eb32d90525e01645db6bfbfb` |
| standalone accessor | `acd81055061cc7d9d76a8b095da4f713f3bee26f97a9f3188f4e69bda3c74ab6` |
| registry adapter | `6d7e98d3cf40acee5d8e9a261c0e431cecba2f55dc93ffd6a844c0d1eb54ec0c` |
| registry mutation suite | `a58bc7ec443b888871329690b2e738c90f5d669309757e78a2b2009279b35f0b` |
| `evidence/matches/scripts-20261030-byte-modes.json` | `31be6f51aa65b0787a5e159859f2b55ca50e88399ae5d37fe16cc1f14203230a` |
| mutation report | `bfa30d7dbc6abf4c3c6bc61c58c839d5ff2e14477065b0d71ec54b712d6f2815` |

Only the complete1,000-byte range is credited by this source proof. Original ROM SHA-256 remains`674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`; no native source bytes, complete image or whole-ROM source match is claimed. All earlier sources/proofs, ROM/save, baseline and application remain unchanged.
