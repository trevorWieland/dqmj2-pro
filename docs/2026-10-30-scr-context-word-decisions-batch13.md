# Complete numeric/primary context-word decisions — 2026-10-30

World entry272, code `[43972,45252)`, now has a complete ordinary C source reconstruction in `src/scripts/20261030/batch13/refresh_context_words.c`. The independently emitted 1,280 bytes equal the measured original code range. This closes the original-only dependency called `refresh_shared_context` in the frozen source proof for entry32. That older proof and its dependency manifest remain unchanged.

The source resets sixteen native context words, makes structured numeric0/3 decisions, checks primary209/210/212/211, and makes a numeric20 threshold decision. Its two local scalar variables occupy qualified VM slots67/68. No other encoded read/write of those slots, public interior entry, or external direct interior edge appears in the current world image. The function has one private RET at45248, and all its records are reachable and executed. Opaque/native/computed references and global program control remain unproved; qualification is for serialized entry-domain calls.

## Compiler and native contracts

Separately versioned `scr_c_compiler_20261030_v11.py` extends the pinned scalar-state backend with typed `reset_context_words(void)` and `set_context_word(int,int)` APIs, numeric-byte `<=` comparisons, and ordinary compound statements. An explicit lexical compound statement in the nested else lowers to a VM no-op header plus generated entry/exit branches. Original native `0204BF1C` only advances the PC and clears the per-thread pending byte; it does not modify scalar variables, persistent state, or the native context-word table. The generated labels come entirely from source lengths. Source contains neither PC constants nor opcodes, executable arrays, assembly, or per-opcode macro calls.

The compiler is a documented restricted C99 backend. It rejects unsupported statements/ABI/type/index/value/storage profiles and does not claim general C support. Ordered comparisons require definitely assigned numeric-byte getter provenance. Setter indices are restricted to0..15 and constant values to exact nonnegative binary32 integers0..16777216 before native integer conversion. The actual source uses only0 and10800. This source/API domain restriction is not a claimed native error path.

Actual SYS162 dispatch at `main:ARM0205B734` calls `02054E6C`, which reads the raw persistent word at`021B9EB8` through `0205BF4C/02063E80` and invokes `020725C8` for all sixteen indices. SYS161 at`0205B740` calls `02054ED0`, converts its two VM arguments, and calls the same setter. `020725C8` writes `021C51D0[index]`. These original native dependencies remain zero new source credit. Reset copies the full raw counter word; it does not initialize the table to zero universally or convert that value to a float.

## Source-only and native proof

The matcher constructs an isolated source-only directory containing four pinned Python compiler modules plus C/header/allocation profile. No original bytecode is supplied to that compiler process. Its generated product matches the entire original range, and the reconstructed script is identical to the original current script. Everything outside this function remains zero-credit scaffolding for this proof.

There are320 fresh scenarios per implementation: all four VM threads, all16 primary-bit combinations, and five numeric tuples covering both threshold outcomes and the outer numeric0 alternatives. Each scenario completes twice by native entry/fork APIs and serialized reentry. Both original and source-recompiled runs pass, giving1,280 complete entry executions and66,624 actual returning native VM/helper calls. All eight branch sites take both outcomes; all original records execute. Bounds remain200 script steps and20,000 native instructions/1,000,000 microseconds per call.

The fixtures retain raw reset words0,1,10800,FFFFFFFF; all sixteen word values and ordered stores; adjacent guard words; complete persistent state; all256 VM variable words; native registers/CPSR and ordered CPU-store observations; and real private-return/depth/termination. Only slots67/68 change in the variable bank. Reentry resets/reapplies the same writes and retains the same final table; that observation does not establish game renewability.

Ten source/profile errors are rejected before a product returns. A separately compiled zero-credit C control tests both `<=6` and `<=28` for every byte value0..255 through the actual native VM. These256 cases contribute2,960 actual returns, counted separately. No provider, source function stub, emulator, application edit, or deployment is involved.

## Reproduction and acceptance access

```powershell
& 'C:\Users\trevo\AppData\Local\Programs\Python\Python313\python.exe' 'C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\match_scr_context_words_20261030_batch13.py'
& 'C:\Users\trevo\AppData\Local\Programs\Python\Python313\python.exe' 'C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\validate_scr_context_words_20261030_batch13.py'
& 'C:\Users\trevo\AppData\Local\Programs\Python\Python313\python.exe' 'C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\verify_scr_context_words_20261030_batch13.py'
```

The full matcher completed successfully. The standalone accessor passed from both the repository and its parent directory, including another fresh source-only build in a temporary directory. It pins the source closure/native namespace/current ROM/image, re-audits direct/private/slot bounds and native contracts, checks every supported trace/read/branch/reset/set/store/state/return, source controls, and zero excess credit. It returns one qualified `(codeSha,startPc)` unit. Seventeen meaningful altered-proof controls and a positive accessor check passed. Missing products withhold credit. Root owns registry and source-ledger acceptance.

| Frozen artifact | SHA-256 |
| --- | --- |
| v11 compiler | `c30f671b25323f474b5aebd9a0b6fcd8a02055a5914ab850a51d430291d59af3` |
| batch13 matcher | `347259ba0f56beff89b083d020e233a9acc0dbe44f4d82629573489b3e627b44` |
| batch13 standalone accessor | `4351288dcde12aaabb0fcd38b8b56d04b7d3703215cfd1950a8e69725b23ea7c` |
| batch13 altered-proof controls | `79d77fcdd743553947145bb2b0648c60c4d66feecc3dee1308cc6af3f2a390b2` |
| `evidence/matches/scripts-20261030-context-words.json` | `295ac6ec9ac26987fbbda863a694b85c8c726f115c721b0bd3f3a380b5d934a8` |

Original ROM SHA-256 remains `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`. Only this complete SCR function gains a source hypothesis/proof here; no native bytes, complete image, or whole-ROM source match is claimed. Raw context words, counters, numeric IDs and primary IDs retain measured meanings without assigned area/story/access/timing/renewal labels.
