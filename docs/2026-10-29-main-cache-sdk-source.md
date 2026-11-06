# Main cache SDK source recovery, 2026-10-29

Three previously unmatched ARM9/ARM routines now have frozen ordinary C, complete compiler/ELF-relocation equality, genuine pinned MW linker proofs and 1,028 actual-return native-versus-linked executions. They total 432 native bytes. The integrator owns whole-module and ROM acceptance. The adjacent 20-byte release routine `020485B4` was already accepted and remains unchanged; it earns no duplicate credit.

All evidence refers to ROM SHA256 `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`, main initialized-image SHA256 `ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f`, processor ARM9 and ARM mode.

| Entry | Bytes | Frozen source | Profile | Evidence |
|---|---:|---|---|---|
| 02048404 | 216 | `src/runtime/20261029_cache_sdk/lookup_8f132205fc42.c` | MW2.0 base, O2,p, inline off | `evidence/matches/main-20261029-cache-lookup01.json` |
| 020484DC | 112 | `src/runtime/20261029_cache_sdk/close_99508969fcf1.c` | MW2.0 base, O2, inline off | `evidence/matches/main-20261029-cache-close01.json` |
| 0204854C | 104 | `src/runtime/20261029_cache_sdk/acquire_22c90cbd192f.c` | MW2.0 base, O2, inline off | same lookup report |

The reports contain complete source/object/native-span hashes, precise flags, qualified function/data bindings, original ELF relocation rows, actual linker commands/control files and frozen linked artifacts. No assembly, opcode edits, absolute-address substitution for the data symbol, executable arrays or callee source credit is introduced. The global `data_020FBAE8` reference retains its ELF data relocation.

Canonical interval checks found no accepted overlap for the three new spans. Worker reservations also contained no matching address. The audit is retained at `work/main-cache-sdk/20261029/reservation-audit.json`. Source/fixture ownership is confined to the new cache SDK paths; no shared builder/ledger, accepted cache source or application file was edited.

## Recovered behavior and source choices

The lookup routine computes bank base `data_020FBAE8 + bank*0x3744`. Its first eight-record scan compares the embedded name at record+24, returning the matching index regardless of the later allocation scan. If no name matches, its second scan finds the first record whose flag bit0 is clear, calls the native length helper, forwards bank/base/index/name and both remaining arguments to `02048AA4`, sets the returned record's flag bit0 and returns the index. A full bank returns full-word 000000FF. The record stride is 100 bytes and its flag word is at+92; other opaque fields retain neutral names. Argument2/argument3 meanings are unclaimed. The otherwise unused length-helper call is preserved.

The candidate routine computes the same bank base, scans 128 eight-byte views starting at+0x320, and selects the first whose flags bit0 is clear. It stores `bankBase + recordIndex*100` modulo2^32 at candidate+4, sets bit0 without discarding the other flags and returns the candidate pointer. Exhaustion returns0. Unsigned address arithmetic preserves the measured full32-bit index behavior; invalid index vectors test pointer-word arithmetic without dereferencing the computed record pointer.

The close routine selects a 100-byte record by bank/index. An inactive low flag bit returns immediately. An active record calls the native length helper, clears that many name bytes, calls the native backing-record cleanup, clears flag bit0 and clears the complete 100-byte record. The execution fixture uses null backing pointers so real native cleanup can run without an initialized heap.

The literal-load order of lookup/acquire was initially reversed while all semantic operations agreed. Computing an explicit unsigned scaled-bank offset before adding the global base naturally reproduces the native load/pool order. Lookup uses the measured two do/while scans; candidate selection materializes the selected view before its flag test. These are ordinary readable C forms, with no pragmas or scheduling barriers in the frozen sources. The compiler profiles are demonstrated separately for these units and are not generalized to other functions.

The physical view overlap remains important: the 24-byte context initialized by `020489F0` at bankBase+0x520 overlaps scan candidates64..66. `evidence/abi/main-cache-view-alias-20261029.json` records the exact native arithmetic and writes. The 128-view scan is measured code behavior; high cells are not claimed to be independent valid lease objects or valid game-domain allocations.

## Native validation and limits

Lookup has90 vectors/180 executions covering both banks, all eight exact cached-name matches and full-bank/255 returns. Actual native name comparison runs; no host callee stubs are installed. Auxiliary arguments4/5 are fixed in these fixtures. Cache-miss filesystem loading remains unsupported dynamically, although the whole source body and its six-argument loader call match complete native bytes and genuine linking.

Candidate allocation has104 vectors/208 executions covering both banks, every valid record index, first/middle/last free scan cells0/63/127, exhaustion and raw record indices -1/0x100/0xFFFFFF00/0x7FFFFFFF/0x80000000. The independent model verifies full32-bit modulo pointer-word stores, preserved flag bits and complete RAM. Invalid pointers are not dereferenced; invalid bank IDs and live scene validity remain unsupported.

Close has320 vectors/640 executions covering both banks/all eight indices, ASCII name lengths0/1/5/31/63, flag words0/1/80000000/FFFFFFFF and randomized remaining record/stack/register bytes. Actual native length, name-clear, backing-record-clear and CPU-fill routines execute. An independent model requires exactly the selected active record to become zero while inactive records and all other RAM remain unchanged. Non-null backing allocation frees, malformed/unterminated names, invalid bank/index addressing and encoding meanings remain unsupported.

All supported executions start fresh, must actually return with restored SP/preserved registers, and compare every R0-R12 value, CPSR, full RAM, scratch/stack memory and instruction/write trace hashes. The fixture bounds are20,000 instructions for close and30,000 for lookup/acquire. The shared lookup/candidate fixture is the unchanged hash-qualified `ov007_constructor_fixture_20261029.py`; its measured ov007 image supplies synthetic fixture names only and receives no new source credit.

## Replay and retained experiments

```text
python match_main_20261029_cache_close.py
python match_main_20261029_cache_lookup.py
```

Use pinned Python3.13.5, Unicorn2.1.4 and the repository-local compiler/linker/license. Scripts derive repository paths from their own location. Source is under `src/runtime/20261029_cache_sdk/`, outputs are isolated under `work/main-cache-sdk/20261029/`, and every authored code file remains comment-free and below500 physical lines.

Earlier candidates and failures remain under `nonmatching/main/20261029-cache-sdk01/`. These include loop-shape, pointer-view, bounded declaration-order, compiler-family/symbol on/off, scheduling, aliasing and inline-accessor experiments. The near matches at94/104 and206/216 were not credited; only the separately frozen offset forms and their complete validation reports are proposed for acceptance.
