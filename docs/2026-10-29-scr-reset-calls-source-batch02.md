# Complete SCR reset callers and hooks, 2026-10-29

Two ordinary C definitions now rebuild four complete routine instances in `s07e05.e` and `s07e11.e`, totaling **536 qualified SCR bytes**. Each image contributes a 252-byte reset caller at entry 129 and a 16-byte empty hook at entry 102. The empty hooks are reported explicitly; they do not represent additional flag logic. There are two source definitions, four image-qualified function instances and three distinct emitted body hashes. Both archive members and identical hook-body copies are distinguished from independently authored logic.

The first unit's compiler, matcher, C source, header and native fixture remain unchanged and are pinned by the new matcher. The empty hooks use that frozen v1 backend. A separately named v2 compiler adds only an out-of-line, zero-argument named script call with an explicit linker binding. No first-unit file is modified.

```text
python C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\match_scr_resets_20261029_batch02.py
```

The final fresh replay passed from the parent DQM directory. Earlier repository-CWD testing also passed; the final report clarifies that the native filesystem loader is not exercised. The report is `evidence/matches/scripts-20261029-reset-calls.json`.

## High-level source and linking

Source lives under `src/scripts/20261029/batch02/`. The hook is an ordinary empty `void before_primary_flag_reset(void)` definition. The reset caller is:

```c
#include "scr_calls.h"
void clear_primary_flags_after_hook(void)
{
    before_primary_flag_reset();
    for (int flag = 281; flag < 285; ++flag) {
        set_primary_flag(flag, false);
    }
}
```

The two files are separately compiled. The v1 compiler emits the complete hook at the measured entry-102 placement. V2 emits the named call using a binding from `before_primary_flag_reset` to that source-built hook's entry, followed by the same high-level flag-call lowering used by v1. The linker-binding JSON is generated from the verified entry table and is a layout input, not authored executable source. The caller retains the out-of-line call; no cross-unit inlining is attempted.

`scr_c_compiler_20261029_v2.py` retains the restricted constant-evaluation C99 model, signed32 checks, exact binary32 flag argument ABI and bounded loop unrolling. Its new declaration has zero parameters and returns void. Runtime variables/branches, arbitrary APIs, general C/C++ and complete preprocessing remain unsupported. The compiler reads C, its explicit ABI header and named binding data; original bytecode is supplied only to the matcher. Source-only subprocess builds use copies of these declared inputs and the two pinned compilers.

## Exact ranges and provenance

| Image | Entry | Executable range | Bytes | SHA-256 |
| --- | --- | --- | --- | --- |
| `s07e05.e` | 102 | `0xCF48..0xCF58` | 16 | `616f68b9d53fd3b0275dee8fc46e94383398bfb9c48d13f88f47349be01c6edf` |
| `s07e05.e` | 129 | `0x16608..0x16704` | 252 | `ff9e7407d6f4fa5d2154b006c767fd0b44e28c94bcf76a7b00587a0f6d738bad` |
| `s07e11.e` | 102 | `0xCF48..0xCF58` | 16 | `616f68b9d53fd3b0275dee8fc46e94383398bfb9c48d13f88f47349be01c6edf` |
| `s07e11.e` | 129 | `0xE158..0xE254` | 252 | `e18315d9a997d85afffc31d657ce5041bdf5186ed6581647be5daf8c0889f3c0` |

| Input or proof | SHA-256 |
| --- | --- |
| v2 compiler | `e88ddd56f388e97852293942d7f49cc8fab2f89c8bd4d19683c33811de565f2e` |
| New matcher | `4761dc295ef8ddd5b66cab45c52a105548b397132535486d63da96bdd5a362ac` |
| Empty-hook C | `c6e2d8d816a96553043687a44c00d98f3c9c3c7d98db68a290c4e8a590e86d6d` |
| Reset-caller C | `4e4c6390073a68d904f0667bdd983bbebd69e4ed1a3df7ae7e24fa182be72d5e` |
| New calls header | `9ac1d6c5c6e50340b690e50f657fca26850c845e459ec6579cfb3123214a5599` |
| New native fixture | `5f1ef9f313c12ae39eee9ee731ca2036f1f5140ff23a71b3f877cd24da95df24` |
| Report | `102d25e495da0ac4858b5bfaf3e189de96ebaf3eaca1d2ac6448b5ac77908422` |

The matcher verifies both original archives against their allocation ranges in the pinned ROM, and all eight members of each archive decode to their expected image. The image hashes are `4a0af687456cdfd4297badecc8cb05578cc410adfcb152082361675939dbcc66` and `bb7bc3a54c93e3a774cb8c918b194eabbdf76b2aa92437fb3fc1b334f89dbda7`. Member aliases do not multiply source credit. The copied v1 header retains hash `8f0e2b3942eb2760b8fff0031849b4738c5e16c96cfd27e2e4a269bbddc9f7fe`.

Both complete executable ranges begin at their native entry-table roots and end at private returns. Full decoded-record partitioning finds no entry or external decoded direct transfer into either interior. The caller's only cross-function transfer is the named call to the hook root; no shared return tail is detected. The adjacent eight unexecuted original bytes after each return are separately hashed, remain outside the accepted executable ranges, and receive zero source credit. Their broader metadata/control role and outside opaque or indirect transfers remain unproved.

## Native execution and controls

The fresh original-versus-rebuilt suite passes **2,716 actual returning native calls per implementation, 5,432 total**, on 146 separately initialized machines per implementation. Each reset caller runs all sixteen initial flag patterns on all four threads in each image. Each hook also runs directly with clear/set patterns on all four threads. Negative native entry selection is rejected without executing an owned routine.

The caller's real VM CALL increases depth from zero to one and stores the return PC at caller base plus 24. The hook's real return restores depth zero and resumes that exact PC while keeping the thread active. The final caller return ends the depth-zero thread. Complete call trees terminate within 17 script records for callers or two for direct hooks, under a 24-step fixture bound. Every native call reaches its return sentinel within 20,000 instructions and one second, preserving SP/R4-R11. All general registers/CPSR, ordered CPU stores, full persistent state and VM contexts agree. Flag bits outside 281 through 284 are preserved. Native VM and callees execute unchanged, without stubs or new native-source credit.

Nineteen v2 source/link rejection controls cover the previous restricted-language failures plus absent, misaligned, negative, out-of-range, Boolean and unknown bindings, wrong script-call arity and excessive script calls. Changing an aligned binding changes only the call target word and fails the original-byte comparison; that mismatching control is not executed or credited. Frozen v1 rejects the broader ABI, demonstrating why a distinct compiler version is required.

All other decoded bytes, headers, adjacent metadata, native executables, archive compression and container bytes remain original scaffolding with zero source credit. No complete script image, scene, story/quest condition, access predicate, battle eligibility or encounter renewability is established. These are measured clears of four unnamed primary flags, preserving the complete source and boundary limitations of the first unit.
