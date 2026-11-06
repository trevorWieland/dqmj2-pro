# First high-level C to SCR source rebuild, 2026-10-29

One complete interpreted routine now rebuilds from ordinary high-level C to its exact 240 original SCR bytes: entry 129 of `s07e04.e`, at code-relative `0x12F84..0x13074`. The candidate source clears primary flags 281 through 284. Their story, quest, map and encounter meanings remain unnamed. This is one reconstructed routine in one unique decoded image, pending integrator acceptance; the earlier frozen inventory's zero-source figures remain historical measurements.

The authored source is `src/scripts/20261029/s07e04_reset_flags.c`:

```c
#include "scr_flags.h"
void clear_primary_flags_281_through_284(void)
{
    for (int flag = 281; flag < 285; ++flag) {
        set_primary_flag(flag, false);
    }
}
```

This source expresses a bounded loop, an induction variable, arithmetic increment and an ordinary named API call. It contains no opcodes, program-counter labels, executable byte arrays or per-instruction macros. The API header declares a Boolean enum and `void set_primary_flag(int index, bool enabled)`.

## Reproduction and compiler scope

```text
python C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\match_scr_flags_20261029.py
```

The compiler can also rebuild just the routine:

```text
python scr_c_compiler_20261029.py --source src/scripts/20261029/s07e04_reset_flags.c --base 0x12F84 --output work/script-source/20261029/s07e04_reset_flags.scrfunc --report work/script-source/20261029/s07e04_reset_flags.build.json
```

Both tools resolve repository-relative paths from their own location. The matcher additionally copies only the compiler, C source and header into a separate source-only build directory and invokes the compiler there. The compiler reads no original ROM, SCR, disassembly or extracted executable input. Python 3.13.5 and its standard library perform this build; the build report records the Python executable hash. Original game data enters the matcher only for comparison and fixture scaffolding.

`scr_c_compiler_20261029.py` is an explicitly restricted C99 backend, not a general C/C++ compiler. It tokenizes and parses a single `void name(void)` function, validates its ABI declarations and identifiers, builds an AST, evaluates supported signed32 expressions with decimal/hexadecimal integer literals, and lowers named calls. Local declarations, `if`/`else` and bounded constant `for` loops are supported through compile-time evaluation. The loops are unrolled; runtime inputs, runtime variables or branches, parameters, arbitrary external APIs, full preprocessing and general C/C++ remain unsupported. Compile-time evaluation, unrolling and emitted-call bounds reject unsupported or nonterminating source. Unknown APIs, including ones in dead branches, are rejected.

The backend emits the measured SCR function-entry trampoline, marshals each named call's arguments and emits its return. The placement base is an explicit link parameter. The four calls share the same lowering rule; their flag IDs come from evaluating the C loop. Changing the source or placement changes the generated output. Generated SCR bytes are outputs, never authored source.

## Float ABI and function boundary

For this API, the native VM reads argument cells 0 and 1 as IEEE754 binary32 values, converts the flag index to a native integer and treats a nonzero Boolean argument as set. The backend supports flag indices 0 through 1535 and Boolean values 0/1, all exactly representable in binary32. It marshals each argument through the measured immediate-to-argument-cell assignment form before calling SYS42. The returned previous flag value clobbers a scratch argument cell and is discarded by the declared void API. Later calls prepare their arguments again. This profile does not generalize floating arithmetic or invalid conversion behavior.

The complete function consists of fourteen records: one entry trampoline, four three-record named-call lowerings and a private return. All 240 bytes are contiguous. The input entry table maps only slot 129 to this root. Full linear instruction partitioning establishes both endpoints; no record crosses an endpoint, embedded payload/data is absent, and no other entry or decoded direct call/fork/jump enters the routine interior. The only direct interior transfer is its own trampoline to the first statement at `0x12F90`. No shared tail is detected. The setters' native behavior is exercised; they do not redirect the function's PC in the supported domain.

This certifies the stated complete entry in the measured valid-input VM context. It does not exhaustively rule out an opaque native SYS elsewhere modifying a PC, and does not certify the rest of the image's control flow.

## Exact bytes and provenance

| Artifact | SHA-256 |
| --- | --- |
| C source | `2c430637c1bfa51fbc34d55c6a4204c004b1821ec6f883242e3f67e9160556bf` |
| ABI header | `8f0e2b3942eb2760b8fff0031849b4738c5e16c96cfd27e2e4a269bbddc9f7fe` |
| Restricted compiler | `8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935` |
| Matcher | `b24e7262a7a42ccd7954d68d366be2644e662e7aa24ac7528462bc5fd21ca6b7` |
| Native fixture generator | `d876d7d61fa35f379c1ead45a474f7a5f13e498a33f81421860fa38af684395d` |
| Emitted and original 240-byte routine | `58c94f200124dba9227f4d21d3359bab5da54dafd2e0c1f5af362b9aaae6a741` |
| Report `evidence/matches/scripts-20261029-flags.json` | `8db50bfbae1517ff4e0eb3f0488f8fc733bb94500c815b6a0d07103084b53a56` |

The original archive hash is `7444b8bd3eb9765f29ef3dffa2d924927a41f53f869539418a1201fbc714bc4f`, and the decoded script hash is `a3f0cd628f46485f8e4fdfcf3912b4c53457839e91f074eeb4ede2cb7bb2180e`. The matcher checks the archive against its allocation interval in the pinned ROM. All eight archive members decode to the same image and are verified individually; they give one unique source unit, without eightfold credit.

The emitted range replaces only its original 240 bytes. The rebuilt decoded image consequently equals all 82,508 original bytes, but **82,268 bytes remain original scaffolding with zero source credit**, including the 4,100-byte header/entry table and 78,168 other code-container bytes. No full image, archive compression, executable module or whole-ROM source match is claimed. No native executable bytes receive credit from this work.

## Independent native execution and compiler controls

Fresh original-versus-rebuilt testing passes **2,242 actual returning native calls per implementation, 4,484 total**, using 129 separately initialized machines per implementation. The complete routine terminates for all sixteen starting flag combinations on all four VM threads, with two independent randomized machine/context/save-state seeds per combination. Neighboring flag bits and every other persistent byte remain unchanged. Flags 281 through 284 occupy mask `0x1E` in the primary-plane byte at RAM `021C0E43`; their serialized mapping follows the separately established primary-plane context, without choosing a real save bank.

Initialization, entry selection and secondary-thread creation execute the original native helpers. Controlled scheduler selection chooses the tested thread; no routine PC is forced past an unsupported path. The native return ends the selected depth-zero thread after all fourteen records. Thread-zero completion sets the main completion state; secondary completion preserves it. A negative entry is rejected through the native start API without executing the reconstructed routine.

Every counted native call reaches its return sentinel within 20,000 instructions and one second and preserves SP/R4-R11. The fixture compares R0 through R12, SP, LR, PC and CPSR, ordered CPU store addresses/sizes/values, full persistent state, the VM context and the global VM context. Fresh scenarios have independent memory/register/CPSR state. Native VM and setter routines execute without stubs and receive no new source credit.

Eleven invalid-source controls reject before output: invalid flag index, non-Boolean argument, unknown API, undeclared runtime value, unbounded loop, signed overflow, escaping include, a dead unknown API, unsupported octal notation, shadowing the runtime API and a keyword used as an entry name. A failed CLI build preserves existing output/report sentinels. Relocating the same C source changes only the trampoline target. Reducing the loop bound emits 184 bytes. A separate ordinary C `if` variant sets flag 282 instead of clearing it and passes independent native expected-state checks on four threads. These controls demonstrate active source compilation; none receives extra original-source credit.

The initial 297-image interpreted backlog therefore gains only this one 240-byte candidate routine. Remaining interpreted logic, ordinary native logic, platforms, rendering and whole-ROM source reconstruction retain their separate unfinished gates. No access, story/quest eligibility or encounter-renewability conclusion follows from these four unnamed flag resets.
