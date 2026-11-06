# Encounter VM operator C recovery — 2026-10-29

Five further ordinary-C bodies reproduce 884 native ARM9/main executable bytes with fresh compilation and genuine MWLD linking. Promoted copies are in `src/encounter/20261029-ops/`; the byte-identical original typed hypotheses are preserved in `nonmatching/encounter/20261029_ops06/`. The coordinator owns registration and the combined module build. The previously frozen five-context and eleven-thread batches remain unchanged.

Run `python nonmatching/encounter/verify_20261029_ops.py`, optionally supplying `--source-root src/encounter/20261029-ops`. The source argument resolves against the repository root. The full final run passed through an absolute script invocation from the parent DQM working directory. Results, source/header/object hashes, helper contracts and immutable source-only link artifacts are in `evidence/matches/encounter-20261029-ops.json`.

| ARM9/main ARM entry | Bytes | Measured operation | Exact SP1p5 profile |
| --- | ---: | --- | --- |
| 0204C094 | 292 | Float arithmetic and signed-integer remainder opcodes 1046–1050 | O2 |
| 0204C1B8 | 200 | Unsigned operand conversion, bitwise operations and raw destination bits | O2 |
| 0204C418 | 76 | Fork wrapper, preserving the third opaque argument to 0204BED0 | O2 |
| 0204C464 | 172 | Signed16 counter and pending/PC state machine | O2 |
| 0204C510 | 144 | Pop a return PC or end the selected thread | O4 |

All profiles use ARM946E, soft float and inline off. The verified compiler SHA-256 remains `89b2fc16c7f1f29ede1e52bdee5bc8ae4d63fe7e50d8074354dfd92c43d47aca`; separately pinned MWLD SHA-256 remains `bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74`. The complete new header hash is `6b0a4de328e3dd4289ffd0aaaa30f67e7faf3efe268287aad64df7db5f58b3f8`. Every selected source and its header are checked before compilation. No assembly, instruction patch, executable blob or initialized callee anchor is used for these bodies. The separately demonstrated O4 profile is specific to the return body; it is not generalized to unrelated source units.

## Cell representation and arithmetic

The destination cell is represented as a union of binary32 number and unsigned32 bits. Opcodes 1051/1052/1053 first convert numeric float operands with the native unsigned conversion helper, perform AND/OR/XOR, then store the raw integer result word. They do not numerically convert that result back to float. For example, `1 OR 0` stores word `0x00000001`, not the binary32 encoding of numeric `1.0`. This is a native byte-level property, not an inferred convenience representation.

Opcode 1050 converts each float operand to signed32, takes the signed integer remainder, and converts that remainder to float. Thus the operands 3.5 and 2.75 produce numeric 1.0. This is not floating remainder. The other four arithmetic opcodes call the native binary32 add/subtract/multiply/divide entries. The native module hash, qualified helper entries, exact caller relocation targets and their ABI contracts are retained in the report.

| Compiler helper | ARM9/main ARM entry | Consumed ABI |
| --- | --- | --- |
| `_fadd` | 02024E0C | Binary32 R0/R1 inputs, binary32 result R0 |
| `_fsub` | 02025CA4 | Binary32 R0/R1 inputs, binary32 result R0 |
| `_fmul` | 02025AB8 | Binary32 R0/R1 inputs, binary32 result R0 |
| `_fdiv` | 02025578 | Binary32 R0/R1 inputs, binary32 result R0 |
| `_ffixu` | 020259E8 | Binary32 R0 input, unsigned32 result R0 |
| `_s32_div_f` | 02026144 | Signed32 numerator R0, denominator R1; quotient R0 and remainder R1 |

The signed division helper passed 593 independent bounded original-native cases, with boundary values and deterministic random pairs. Quotient truncates toward zero and remainder follows the numerator's sign in the ordinary domain. For a zero denominator this helper returns the numerator in R0 and zero in R1. For minimum signed32 divided by -1, R0 wraps to `0x80000000` and R1 is zero. These facts concern this signed32 two-register helper and do not replace the separately measured signed64 entry behavior. No generic single-C-return replacement is assumed. The previous comparison helper APSR contracts are also preserved in the verifier.

An additional thirteen direct native unsigned-conversion cases distinguish valid C conversion inputs from negative/out-of-range/infinity/NaN inputs. Invalid C domains are explicitly marked rather than treated as portable C behavior. Neither these helper probes nor the native library bodies used by the fixtures receive new callee source credit.

## Counter, fork and return semantics

The counter occupies signed16 at thread +0xA and its phase byte is at +8; the padding byte at +9 is preserved. Phase zero converts the operand to signed32, narrows it to signed16, and selects phase 10. Phase 10 decrements with the measured signed16 wrap behavior. A nonnegative result sets pending and leaves PC in place; a negative result advances PC, clears pending and resets the phase. Other phase bytes return without the modeled progress. The fixture calls do not establish physical frame duration.

The fork wrapper forwards both raw instruction words to the already recovered allocator wrapper. Slot zero is not activated by that wrapper; failed allocation still leaves the caller's continuation update intact. Synthetic vectors also cover the case where an inactive current secondary slot is the first free slot: its newly installed PC is then advanced by the caller. The opaque third argument retains its raw 32-bit value and is not spuriously converted through float.

Return opcode 1026 pops valid depths 1 through 64. Depth zero instead disables the selected thread and sets pending; when that selected slot is zero it also sets the running byte to 2. The existing distinction between main-thread completion and universal secondary-thread completion remains. Unchecked invalid call depths are not certified. No game outcome or encounter-renewability name is attached to this VM state.

## Execution and portability limits

The final paired replay passed 6,508 actual returns per implementation, 13,016 total, with 2,351 independently initialized machines per implementation. It preserves the earlier context/thread/guard fixtures and adds 1,194 independent native controls: 593 signed division cases, 13 unsigned conversions, 288 arithmetic cases, 96 raw-bit cases, 120 counter cases, 64 fork cases and 20 return cases. All five source bodies are reached; their observed entry counts per implementation are 337, 96, 64, 120 and 484 respectively.

Every counted call reaches the return sentinel, restores SP and the callee-saved register set, remains below 20,000 instructions and uses the existing one-second Unicorn bound. Original and freshly linked replacements compare all R0–R12/SP/LR/PC/CPSR, ordered CPU store addresses/sizes/values, the full 0x7040-byte persistent RAM partition and both 0x8A0-byte VM contexts after each true return. All comparisons pass. There are no native function stubs. The three earlier nonreturning resource probes remain excluded and no post-fault state is used for proof.

Native source matching and Android equivalence remain separate gates. The matching C remainder expression has undefined C domains at denominator zero and minimum signed divided by -1, even though the pinned compiled native helper has the measured results above. A portable Android implementation must handle those domains explicitly, preserve raw integer cell bits, implement the measured conversion/narrowing rules, and separately validate any required NaN payload behavior. The arithmetic fixtures check NaN classification and the complete original/rebuilt machine-state comparison retains exact native payload bits; no Android payload equivalence or on-device execution is claimed. Pointer-bearing VM structs still use the ARM32 layout and require platform abstraction for Android64.

Alternative return expressions, volatile hypotheses and raw-address macros were investigated only as failed work. None is retained: the original readable C body becomes exact under its measured O4 profile. Ordinary original module code and original SCR/assets used by remaining callees stay fixture scaffolding. This batch does not complete a module, a native port, an encounter-access certificate or the whole-ROM source match.
