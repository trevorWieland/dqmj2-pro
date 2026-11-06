# Complete world reset caller source - 2026-10-30

`world.e` entry32, code `[60232,63972)`, is reconstructed as ordinary C in `src/scripts/20261030/batch09/reset_world_flags.c`. Its 3,740-byte source-only product exactly matches the measured image, SHA256 `e55fb5cbd177fcfdb25fbfd92fb5cfe1de4dd83fd3557a71e7532ffe021ee759`. This is one definition and one complete function instance. It is not a complete image or a native executable module.

## Source and contracts

The C source has a float formal argument, named state/counter/random APIs, constant flag-reset loops, typed locals and seven named script calls. It contains no source opcode constants, source PC constants, executable arrays or per-opcode assembly macros. Separate compiler `scr_c_compiler_20261030_v7.py` uses the frozen core/v4 parser infrastructure. Constant ordinary C loops are unrolled; this is explicit compiler behavior, not a claim that the original bytecode loops at those locations. The compiler is a restricted C99 backend, not a general C compiler.

The caller saves its incoming argument0 word in slot100, clears sixty specifically measured primary flags, samples positive-bound7 native randomness into slot101 and numeric52, and stores the threshold predicate in slot102 and primary145. Primary clears include346-349 and500-509. It resets a raw counter between the third and fourth primary clears. This ordering is preserved, including all aligned32-bit primary read/modify/write stores and previous-value returns.

Measured native dependencies are:

- SYS36 wrapper main:ARM02052840, bound7: state RAM020F6044 updates as `(state*0x41C64E6D+0x3039) mod 2^32`; the sampled integer is `(new_state>>16) mod7`, represented as binary32. The backend supports only positive byte-bounded samples here; its name does not grant unsupported negative-bound source behavior.
- SYS43 wrapper main:ARM02053B0C: the native wrapper scales its converted input by30; the supported source input is0. It writes zero words to RAM021B9ED4 and021B9ED0, corresponding to persistent-base offsets0x20 and0x1C, in that order.
- SYS48 wrapper main:ARM02053C68 uses native0205BFD4: unsigned persistent-base word+4 at least0x2A30 returns logical1, otherwise0, converted to binary32.
- Numeric52 uses the native numeric byte setter; primary145 uses the native primary word bit setter. No assembly or additional native source credit is assigned by this proof.

These are raw operations. Counter scale, threshold and resets are not given timing, story, area, acquisition or renewal meanings. A cleared flag and repeated caller execution do not establish encounter renewability.

The three slots100-102 have no known encoded reads/writes outside this caller in the complete current decoded image. Every known mode0 operand is checked for a finite integral index0..255. Opaque/native/computed accesses remain unproved. Direct entry/call/jump boundaries exclude interior entry or shared-tail credit. Each original callee must preserve the three caller slots in the supported native executions; the rest of its VM state remains shared rather than being treated as private C stack storage.

## Actual source linking

The linked test image contains three freshly emitted source products: caller32/3,740 bytes; frozen decision34/1,352 bytes; and frozen empty20/16 bytes. The last two reuse existing definitions and get zero new source credit. Their actual C/header/compiler closures are copied to isolated source-only directories, compiled and inserted into the image before native testing. A qualified-original binding alone does not qualify as a source-linked callee.

The other five callees remain qualified original dependencies with zero reconstructed-source credit: entry257 at1056, entry272 at43972, entry11 at50684, entry12 at52244 and entry17 at59076. The script shares its implicit VM argument/context state; only the explicit formal handoff to entry12 is emitted immediately before that call. No generic host-C ABI isolation of original callees is inferred.

The new caller passes its saved float argument to entry12 without numeric conversion. Positive/negative zero,1 and a quiet NaN payload are fixture inputs. The raw input word must survive slot100 and the named call's argument0. This is a VM binary32 bit-preservation contract, distinct from casting that word numerically to a native float.

## Native evidence and limits

The first full proof passed52,076 actual native VM/helper returns across original and rebuilt code. This means64 complete owned entry32 executions:16 scenarios per implementation, two serialized invocations each, two implementations. The much larger native-return total is not a count of complete script executions. Source-linked callee executions and the five original dependencies are separately scoped.

The cases cover all4 threads, the four formal bit patterns, threshold counters0/10799/10800/0xFFFFFFFF, varied RNG seeds, initially set/clear reset flags and both numeric20 threshold paths. Numeric0/1 are explicitly synthetic4/0. No natural launcher, current save bank or ordinary scene context is claimed. Every own instruction executes; this caller itself is straight-line after compile-time loop unrolling. Conditional behavior of original callees remains their zero-credit implementation.

Each native call must reach its sentinel within20,000 instructions and1,000,000 microseconds. Each complete invocation has a3,000-step SCR cap. The fixture verifies real CALL/RET targets, signed depth and all seven continuations. Original and rebuilt comparisons cover general registers/CPSR, ordered CPU stores, VM state and full persistent state. Own effects have an independent model, including all primary word stores, counter stores, bounded RNG, numeric byte stores and whole256-slot checks. Persistent/register-file boundary snapshots make serialized state carry independently checkable; post-fault state is not used.

Thirteen source/profile/link controls reject before output, including aliases, missing formal allocation, unbounded values passed to bool/byte setters, unqualified RNG bounds, nonzero counter reset, incorrect getter type, incomplete links, wrong callee ABI/arity, negative flags and runtime-dependent constant loops. A wrong but aligned link produces different bytes and fails current-image qualification. Unsupported native resource/error paths and other numeric0/1 contexts receive no return or source claim.

`validate_scr_world32_20261030_batch09.py` independently checks current source and product closure, ROM/archive identities, every actual source-linked emission, boundary/slot/link metadata, native API identities, first-phase semantic effects, complete nested trace/depth, raw caller locals, serialized state carry and control rejections. It freshly recompiles all three products. Missing products withhold credit. Root owns shared ledger and acceptance.

## Reproduction and preserved failure

Run `python match_scr_world32_20261030_batch09.py`, then `python validate_scr_world32_20261030_batch09.py`. The tools resolve paths from their own repository files and the reports record actual argv/CWD. Python3.13.5 and Unicorn2.1.4 remain pinned. Original ROM SHA256 is `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`; world decoded SCR SHA256 is `9c6c4a136b306126a83a8a749df18276aa2a9d328a4add073fc47f50ea0619f8`.

The first empty-callee attempt used frozen v2 with a header from the core-v1 ABI and was rejected. `work/script-source/20261030/batch09/failed-v2-empty-profile/failure.json` preserves its input hashes, command, exit1 and actual error. The corrected build uses the frozen core-v1 backend with the same original C/header bytes. It grants no extra source credit. Earlier accepted sources, reports and verifiers are unchanged. No application adapters/UI, device deployment or emulator were used.
