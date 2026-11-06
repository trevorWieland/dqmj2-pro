# Complete world bounded selection source - 2026-10-30

`world.e` entry17, decoded code `[59076,60224)`, now rebuilds from ordinary C as a complete 1,148-byte function. The source is `src/scripts/20261030/batch11/select_numeric_thirty_one.c`, with `scr_random_decision.h` and `selection.bindings.json`. Exact body SHA256 is `184289f71a8612498fa98fad4bd347ad8b86a0bf669b238da81422f5ed24f140`. This is one definition/one qualified instance, not a complete image or ROM. It closes one previously original-only dependency of the independently recovered entry32; that older proof remains unchanged and receives no duplicate credit here.

## Measured behavior

The function returns early if primary93 is false or primary28 is true. Otherwise it reads numeric32. A value below4 causes numeric32=4; a value at least8 returns without sampling. Values below8 permit one genuine native bound6 random sample. Selections0/1/2/3/4/5 set numeric31 to6/19/31/43/49/59 respectively. The local state scalar retains its original numeric32 read even when the byte is clamped. On serialized reentry a clamped byte is read as4 and can sample again; an open gate repeats the random sample and numeric31 setter. These raw predicates and values have no assigned area, timing, story, acquisition or renewal meaning.

Native randomness is measured through SYS36/main:ARM02052840 and native0203D294. RAM020F6044 advances as `(state*0x41C64E6D+0x3039) mod 2^32`; the returned selection is `(new_state>>16) mod6`, represented as binary32. Fixtures select initial states by modular inversion of that real LCG. They execute the real native sampler; neither PC nor result is patched, and no out-of-domain result is injected.

## Source, storage and CFG

Separate compiler `scr_c_compiler_20261030_v9.py` extends the frozen scalar frontend with typed positive byte-bounded random reads, early void returns to a computed private RET, byte-proven variable-left `<` and constant-left `<=`. Ordered comparisons remain restricted to definitely initialized numeric-byte getter provenance. Arbitrary context floats, other operators, nonpositive/oversized random bounds and changed provenance are rejected. This restricted C99 backend is not a general compiler.

The source uses named getters/setters, variables, structured conditions and `return`; it contains no source PC constants, opcodes, executable arrays or per-opcode macros. Generated early-return targets are computed after lowering. Slots96/97/98 hold the numeric state, boolean gate and random selection. Every known mode0 operand across the whole image is a finite integral index0..255, and no known encoded reference to these slots occurs outside entry17. Opaque/native/computed references and global program coverage remain unresolved. The direct entry/call/branch audit excludes interior entry and shared-tail credit for this qualified entry domain.

Three original compiler-generated joins at59192/59308/59528 follow unconditional returns and have no path from the qualified entry in the current CFG. They account for 36 physical bytes. The source backend reproduces them exactly as compiler artifacts, but the report never claims they executed. No PC is forced to cover them.

The last `selection==5` false outcome is also excluded: the real native result domain is0..5; reaching that comparison requires earlier comparisons to0..4 all false, leaving only5. The verifier checks the current bound6 call, result slot, each equality, each false target and each successful arm's return join. This is an entry-domain/dataflow exclusion, not a complete assertion about opaque external control transfers.

## Native proof

The matcher passed 768 complete owned entry executions and 19,776 paired actual native VM/helper returns: 192 fresh scenarios per implementation, two serialized invocations each, two implementations. All 4 threads, all early exits, numeric32 values0/3/4/7/8/255, set/clear gates and all six real random choices are covered. Every reachable own instruction executes. Nine conditional sites have both outcomes; the final equality has only its feasible true outcome. Registers/CPSR, ordered CPU stores, full persistent state and VM state compare between original and rebuilt code.

An independent model checks the optional numeric32 byte clamp, numeric31 byte setter, complete 256-word register file, retained/untouched locals on early exits, previous native getter/setter values, RNG updates and serialized state carry. Calls must actually reach the sentinel within 20,000 instructions / 1,000,000 microseconds; an invocation has an 80-step cap. No native function stub or post-fault state is used.

A separate generated 280-byte ordinary-C control exhausts all 256 numeric-byte values for `<4` and `8<=value`, yielding 3,824 actual native returns. It has zero original-source credit and is separate from the paired routine return count. Ten negative source controls reject unsupported domains, types, operators, return values, indices and provenance before output. No arbitrary-float ordering, malformed-native-record or resource-error path is claimed.

## Acceptance and replay

Run `python match_scr_world17_20261030_batch11.py`, then `python validate_scr_world17_20261030_batch11.py`. Both work through absolute invocation from the parent directory. The verifier hashes current inputs/products, compares the ROM-derived image, recomputes direct/private bounds, slot references and unreachable CFG nodes, freshly emits the complete C product, verifies the real RNG/equality domain exclusion, every native trace and state effect, all byte controls and source rejections. Missing products withhold credit. Root owns shared ledger and acceptance updates.

Original ROM is 175,959,612 bytes, SHA256 `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`; decoded world SCR SHA256 is `9c6c4a136b306126a83a8a749df18276aa2a9d328a4add073fc47f50ea0619f8`. Python3.13.5 and Unicorn2.1.4 remain pinned. No application adapters/UI, save bank selection, device deployment or emulator execution were changed or used. Earlier proofs remain frozen.
