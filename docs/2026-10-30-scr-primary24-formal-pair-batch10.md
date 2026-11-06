# Complete primary24 formal-argument decisions - 2026-10-30

Two complete routines now rebuild from ordinary C with an exact source-only byte match: `s02e04.e` entry102 `[63992,64344)`,352 bytes, and `s02e01.e` entry102 `[65228,65892)`,664 bytes. They are two authored definitions/two qualified instances totaling 1,016 bytes. All other script/native/asset bytes remain zero-credit scaffolding; neither image is completely reconstructed.

Sources are `src/scripts/20261030/batch10/enable_primary_24_from_argument.c` and `clear_primary_24_from_argument.c`, with the common `scr_formal_decision.h` and separate named bindings. Both use ordinary float formal arguments, variables, named numeric/flag APIs and nested structured conditions. There are no source PC constants, opcodes, executable arrays or per-opcode macros. The source compiler is separately versioned `scr_c_compiler_20261030_v8.py`; v1-v7 and all earlier proof closures stay frozen.

## Raw measured behavior

- The 352-byte routine sets primary24 true when argument0 equals5, numeric0 equals2 and numeric3 equals6.
- The 664-byte routine clears primary24 when argument0 equals8, numeric0 equals2 and numeric3 equals6; otherwise, argument0 equals15, numeric0 equals2 and numeric3 equals8 also clear it.

These are raw input/state predicates. They complement the earlier separately qualified `s02e10.e` context0==12/numeric0==2/numeric3==1 setter without proving that the three scripts represent particular areas, story stages or encounter access. Formal argument0 and direct context0 are distinct ABI inputs. Supported reentry may invoke the same word setter again even after the stored value agrees. No once-ever or renewal claim follows.

The native primary setter performs an aligned 32-bit read/modify/write at RAM021C0E20, affecting bit24 and preserving all neighboring bits. Numeric reads use RAM021C0DC8 and 021C0DCB. The previously qualified serializer maps the primary plane to bank0x3994, so bit24 corresponds to bank0x3997 bit0; these fixtures exercise RAM state, not bank selection or serialization. The captured-save current-world state is not asserted.

## Source and storage qualification

The 352-byte routine copies argument0 to slot 102 and uses slot 103 for successive numeric reads. The 664-byte routine copies argument0 to slot 101 and reuses102 within its mutually exclusive branches. Every known encoded reference to each pair of slots is inside its own routine. Every known mode0 operand in each complete image is checked for a finite integral index0..255. Opaque/native/computed references remain unresolved; absence of known references is not a general private-lifetime assertion.

V8 adds a float formal binding and uninitialized automatic declarations to the frozen scalar backend. The formal copy preserves raw IEEE754 binary32 bits. An uninitialized declaration emits no store and defines no value. Every local read requires initialization on that source path; a definition inside one conditional branch is not assumed after that branch. A separate forward CFG analysis of the current original routine intersects predecessor definition sets and proves an actual VM assignment dominates every read. Both source and decoded CFG controls reject an uninitialized read.

The 664-byte source therefore declares `float state;` without manufacturing an initialization. Each relevant branch writes numeric0 before comparing it and conditionally writes numeric3 before its comparison. When the request is neither8 nor15, the VM state slot retains its prior poisoned word. That preservation, all other slots and both complete register files are tested explicitly.

## Native validation and caller prefixes

The full matcher, invoked from the repository's parent directory, passed 2,496 complete owned entry executions, 28,656 paired actual native VM/helper returns and 256 separately counted prefix native returns. There are 240 standalone cases for the setter and 384 for the clearer per implementation, two serialized invocations per case, and two implementations. These native-return counts are not counts of complete script executions. Prefix callee returns are additional separately scoped facts; outer-prefix return/source credit remains zero.

The fixtures cover all 4 threads, each conditional branch with both outcomes, every own instruction, set/clear initial primary24, numeric byte extremes, unequal requests, adjacent binary32 values, positive/negative zero, infinities and signed quiet NaNs. Direct tests set context0 to a distinct 99 while supplying formal argument0 independently. Comparisons include registers/CPSR, ordered CPU stores, full persistent state, full 256-word VM register files, previous setter/getter values and real private returns. Native calls must actually reach the sentinel within 20,000 instructions / 1,000,000 microseconds; each routine has a 48-step cap.

Actual original caller prefixes independently start entry129 through the native entry API. They copy synthetic context0 into a caller slot, execute original helper49684 completely, copy the preserved caller slot to argument0, CALL entry102 and observe its real return to the caller. The supported target calls are119112 in `s02e04.e` and101768 in `s02e01.e`; tested requests are5 and8/15 respectively. The prefix stops after the target return, leaving entry129 active. This qualifies the script-level producer and ordering in that synthetic context, not the outer entry's termination or a natural native launcher/scene producer. Helper49684 receives zero source credit.

Seventeen negative source/profile controls reject before output, including aliased/missing formal slots, wrong parameter/getter types, out-of-range API indices, shadowing and three uninitialized/dominance controls. Malformed native records, resource errors or arbitrary outer-entry paths are not claimed as supported outcomes. Post-fault state contributes no evidence.

## Acceptance and reproduction

`python match_scr_primary24_pair_20261030_batch10.py` reconstructs both ranges from source-only inputs, compares the current ROM-derived images and runs fresh original-versus-rebuilt native machines. `python validate_scr_primary24_pair_20261030_batch10.py` independently re-emits both source products, checks hashes/products/current ROM intervals, recomputes direct/private boundaries and all assignment dominance, verifies the complete native populations and expected full-state effects, and rechecks negative controls and caller-prefix scope. Missing products withhold credit. Root owns registry and ledger updates.

Original ROM SHA256 is `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`, 175,959,612 bytes. Python3.13.5 and Unicorn2.1.4 remain pinned. The report records source/include/profile/compiler/native input identities and actual argv/CWD. Source bodies and proof generators are private repository files. No application adapter/UI, device deployment or emulator was changed or used.
