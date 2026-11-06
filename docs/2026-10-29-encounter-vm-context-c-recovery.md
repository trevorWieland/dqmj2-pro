# Encounter VM context C recovery — 2026-10-29

Five ordinary-C bodies reproduce 804 native executable bytes after fresh compilation and genuine MWLD linking. They remain integration candidates until the coordinator registers them and replays the combined module build. This work does not certify a complete encounter, a named battle outcome, a renewable supply, a fully reconstructed module, or the whole ROM.

The source and shared header are frozen under `nonmatching/encounter/20261029_context01/`. The replay command is `python nonmatching/encounter/verify_20261029_context.py`; absolute invocation resolves paths from the script rather than the caller's working directory. The current machine-readable result is `evidence/matches/encounter-20261029-context.json`. Earlier native behavior and remaining encounter limits are documented in `2026-10-29-encounter-native-guards.md`.

| Native identity | Bytes | Measured role | Compiler profile |
| --- | ---: | --- | --- |
| ARM9/main/ARM/0204C280 | 300 | Float comparison VM opcodes 1039–1044 and condition-byte update | SP1p5, ARM946E, O2, inline off |
| ARM9/main/ARM/02053E2C | 148 | SYS93: three queued signed halfwords become float arguments | SP1p5, ARM946E, O3, inline off |
| ARM9/main/ARM/02054980 | 84 | SYS41: primary-bit getter and thread continuation | SP1p5, ARM946E, O2, inline off |
| ARM9/main/ARM/02054A3C | 96 | SYS220: secondary-bit setter and thread continuation | SP1p5, ARM946E, O2, inline off |
| ARM9/ov000/ARM/021E4DEC | 176 | Raw entry-reason/main-mode mapping to imported VM context | SP1p5, ARM946E, O2, inline off |

The compiler is the existing private `tools/mwccarm/mwccarm/2.0/sp1p5/mwccarm.exe`, SHA-256 `89b2fc16c7f1f29ede1e52bdee5bc8ae4d63fe7e50d8074354dfd92c43d47aca`. The archive directory identifies the verified artifact; it does not by itself establish a literal product-version banner. The linker is the separately pinned `2.0/base/mwldarm.exe`, SHA-256 `bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74`. Full flags, source/object hashes, source dependencies, immutable isolated link artifacts, native module hashes, and zero-code callee anchors are recorded per function. Header SHA-256 is `b010056706bff77e6ae453fe36d7e266c42e31261ea2682304c596651ab33ea3` and is required before compilation. Each anchor initializes zero executable bytes and grants zero callee source credit.

## Float-helper contracts

The pinned compiler emits legacy helper symbols that the shared heuristic symbol parser does not recognize. The verifier supplies a process-local, explicit mapping, then asks the real linker to perform the relocations. It does not edit the shared matcher, registry, source instruction bytes, or linked instruction bytes. The comparison calls consume APSR flags; they must not be replaced with generic C functions returning `int` merely because such functions have similar mathematical names.

| Helper | ARM9/main ARM entry | Caller ABI |
| --- | --- | --- |
| `_ffix` | 020259B4 | Binary32 operand in R0; signed32 result bits in R0 |
| `_fflt` | 02025A28 | Signed32 operand bits in R0; binary32 result bits in R0 |
| `_feq` | 0202549C | Binary32 operand words in R0/R1; caller consumes APSR EQ |
| `_fneq` | 02025504 | Binary32 operand words in R0/R1; caller consumes APSR NE |
| `_fgr` | 0202537C | Binary32 operand words in R0/R1; caller consumes APSR HI |
| `_fls` | 02025440 | Binary32 operand words in R0/R1; caller consumes APSR CC |
| `_fgeq` | 02025320 | Binary32 operand words in R0/R1; caller consumes APSR CS |
| `_fleq` | 020253D8 | Binary32 operand words in R0/R1; caller consumes APSR LS |

The actual comparison caller contains the corresponding conditional moves after each BL. Conversion entries were checked against their measured instructions and typed native fixtures. These are compiler-internal contracts. No generic C integer-return binding or reconstructed helper-body credit is inferred. Finite conversion fixtures stay within the applicable signed range; selected NaN/infinity controls exercise comparisons without claiming portable C behavior for out-of-range float-to-integer casts.

## Execution evidence

The paired fixture run records 4,956 actual returns for the original implementation and 4,956 for the five freshly linked replacements: 9,912 total, with 798 independently initialized machines per implementation. The fixtures include the earlier 625 native VM/accessor/construction cases, 108 new thread/float/signed-triplet cases, and the 4,223 returning calls in the connected original-SCR guard traces. Every counted call reaches the return sentinel, restores SP and the callee-saved register set, remains below 20,000 instructions, and uses the existing one-second Unicorn limit.

The two implementations compare all R0–R12, SP, LR, PC and CPSR after each true return; the ordered address/size/value stream of all CPU stores; the complete 0x7040-byte persistent RAM partition; and both synthetic and global 0x8A0-byte VM contexts. Matching is exact through the hashes of these observations, including scratch and stack writes. Original and rebuilt fixtures use the same deterministic seeds. No native function is stubbed. Original module code and original script/assets remain fixture scaffolding outside the five replaced C bodies.

All five replacements are actually reached. Per implementation their observed entry counts are 699 for 0204C280, 15 for 02053E2C, 105 for 02054980, 48 for 02054A3C, and 127 for 021E4DEC. The new direct SYS93 fixtures cover all four thread slots, signed extrema -32768/32767, negative IDs, preservation of the remaining argument slots, and the existing thread PC/pending updates. Comparison controls add all four thread slots, NaN, opposite infinities, signed zero, and finite unequal operands.

The connected vectors retain the 834-step world prefix, 36 complete conditional map-entry prefixes, and 14 predicate rearming checks. Each implementation also attempts the two known SYS5/SYS104 resource boundaries. Those calls fail, remain unsupported, and contribute zero actual-return credit. Their post-fault state is excluded from the proofs. The map and world prefixes execute all preceding script instructions; no unknown instruction is silently skipped. Replacing these five C bodies preserves the earlier measured predicate results and the earlier limits on access and repeatability claims.

## Failed profiles and limitations

The initial broad drafts compiled before tuning. Several same-size base-compiler bodies differed where the native uses MUL for the 0x10C thread stride and that compiler selected SMULBB. They received no credit. SP1p5/SP1p6 selected the native multiply naturally, and the signed-triplet body required its separately demonstrated O3 profile to recover the native loop schedule and 148-byte size. O2 remained 156 bytes for that body. No volatile qualifier, fabricated alignment, handwritten assembly, or instruction patch was retained. Earlier alternative loop/pointer/qualifier drafts and unsupported processor-option probes remain zero-credit experiments under the unique work directory.

Early sweep stdout undercounted discovered objects because its filename inspector did not account for compiler-hash suffixes. Those discovery counters are excluded from the progress claim. The fresh verifier requires actual compiler objects, matching source/header hashes, and all five successful full linked-body comparisons rather than trusting the old sweep counters.

`NativeVm` models the measured ARM32 layout and checks its total size at compile time. Unused fields and historical identifiers are not claimed to be recovered. Its pointer-bearing layout is deliberately not an Android64 platform representation. A native Android implementation must first replace DS logical addresses and platform dependencies with explicit abstractions, independently of these pinned compiler matching results. The helper contracts and bounded script vectors are useful functional constraints, not a complete platform replacement or device test.
