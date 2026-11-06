# Encounter VM/thread C recovery — 2026-10-29

Eleven additional ordinary-C bodies reproduce 988 native ARM9/main executable bytes through fresh SP1p5 compilation and genuine MWLD linking. Byte-identical accepted-source candidates are in `src/encounter/20261029-threads/`; the original typed hypotheses remain in `nonmatching/encounter/20261029_thread04/`. Registration and the combined module replay remain coordinator-owned. This is additional function recovery, not completion of a module or the whole ROM.

Run `python nonmatching/encounter/verify_20261029_threads.py`. The verifier defaults to the promoted source directory and accepts `--source-root src/encounter/20261029-threads`, resolved against the repository root. The final full replay passed with an absolute script invocation from the parent DQM working directory. Its versioned report is `evidence/matches/encounter-20261029-threads.json`. All selected C files and the complete local header closure are checked against fixed hashes before compilation.

| ARM9/main ARM entry | Bytes | Measured role | Exact profile |
| --- | ---: | --- | --- |
| 0204BC08 | 112 | Validate SCR magic, install code pointer, clear selected VM sections | O2 |
| 0204BC78 | 68 | Resource-load wrapper, guarded by the current active byte | O2 |
| 0204BCBC | 68 | Active/resource release wrapper | O2 |
| 0204BD00 | 104 | Start a signed script-table entry and initialize main thread | O2 |
| 0204BD6C | 116 | Execute the four VM thread slots until each selected thread yields | O3 |
| 0204BED0 | 76 | Find the first free slot and initialize positive slot indices | O2 |
| 0204BF1C | 56 | Advance PC and clear pending | O2 |
| 0204BF7C | 88 | Branch when condition byte is nonzero | O2, opt speed |
| 0204BFD4 | 88 | Branch when condition byte is zero | O2, opt speed |
| 0204C02C | 104 | Typed value store, with an early return for a nonwritable destination | O2 |
| 0204C3AC | 108 | Push a return PC, increment signed depth and jump | O2 |

All profiles use the verified private `2.0/sp1p5/mwccarm.exe`, ARM946E, soft float, and inline off; full flags and compiler/object/source/link hashes are recorded per entry. Compiler SHA-256 is `89b2fc16c7f1f29ede1e52bdee5bc8ae4d63fe7e50d8074354dfd92c43d47aca`; separately pinned MWLD SHA-256 is `bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74`. The new header SHA-256 is `e9e61e1baf04164c351e29a6491b91df584ad14192e01a1bb14484e3be31c6fb`. The previous five-function source/header/verifier and reports remain unchanged.

The typed thread model has a 32-bit PC at +0, signed16 depth at +4, active byte at +6, pending byte at +7, an opaque word at +8, and 64 return-PC words at +0xC; stride is 0x10C. This refines the previous opaque status/remaining bytes without changing their measured offsets. Historical identifiers and unused field meanings remain unclaimed. VM pointers retain the measured ARM32 layout and are not an Android64 platform representation.

## Native ABI and behavior constraints

The native fork caller 0204C418 loads instruction words +8/+0xC into R1/R2 and calls 0204BED0 at 0204C42C. The latter body and its slot finder overwrite R2 before using its incoming value. The reconstructed definition therefore retains an explicit third opaque, unused 32-bit formal parameter. Its historical interpretation is not claimed. The final fixture supplies the R2 canary 0xB16B00B5; the measured caller instruction span and its hash are in that function's `abiEvidence`. The first preliminary two-formal draft was replaced before freezing and contributes no separate credit.

The earlier explicit float-helper contracts are preserved in the new verifier/report. In particular, `_feq`, `_fneq`, `_fgr`, `_fls`, `_fgeq`, and `_fleq` expose compiler-internal APSR EQ/NE/HI/CC/CS/LS results consumed by the native caller, rather than interchangeable generic C integer-return interfaces. The mappings remain local to the verifier process; callee anchor objects contain no initialized executable bytes and receive zero source credit. No assembly, executable blob, byte-encoded instruction or instruction patch is used in any of the eleven recovered bodies.

Observed behavior includes several limits that a native port must preserve or handle explicitly. A bad SCR magic still installs the source pointer before returning zero and does not reset the other VM fields. Entry start rejects a negative signed PC but does not validate a nonnegative PC against code length; the fixture includes positive 0x7FFFFFFF without executing that PC. The free-slot helper can return slot zero, but the initializer only activates indices greater than zero. A nonwritable immediate destination returns without advancing PC or clearing pending.

The VM running byte becoming 2 marks thread zero finishing. It is not a certificate that every secondary thread has completed. Four-slot vectors independently vary the prior running byte, all 16 active masks, and both direct termination and nested call/store/return programs. Main completion and secondary-slot state are compared separately. CALL push fixtures cover signed depths 0, 1, 31 and 63; unchecked depths outside 0..63 remain unsupported.

## Fresh execution and evidence limits

The final paired replay passed 5,314 actual returns for each implementation, 10,628 total, with 1,157 independently initialized machines per implementation. It preserves the earlier 625 native cases, 108 float/thread controls and 4,223 connected guard-prefix calls, then adds 358 VM initialization, table-entry, resource-guard, slot, branch, store, call-frame and nested execution cases. Every counted call reaches the return sentinel, restores SP and the callee-saved registers, remains below 20,000 instructions, and uses the one-second Unicorn bound.

Each returning call compares all R0–R12, SP, LR, PC and CPSR, the complete ordered CPU-store address/size/value stream, the full 0x7040-byte persistent RAM partition and both 0x8A0-byte VM contexts. All eleven new entries are reached. Per implementation the observed entry counts are 105, 3, 3, 97, 128, 48, 5, 20, 587, 1,740 and 261 in table order. Matching bodies are installed only at their measured original entries; no native function is stubbed.

Three nonreturning probes per implementation are kept outside the true-return count: the previously documented SYS5/SYS104 boundaries and a null resource-load probe failing at main0200BD38. Their post-fault state is not used for proof. The load wrapper's active guard and unload-without-resource paths are exercised; a successful real resource load and allocator-owned resource free are not certified. The original module code, SCR bytecode and assets used by other fixture callees remain scaffolding with zero additional source credit.

Early profiles that differed in code size or allocation remain failed experiments under the unique work directory. Readable common-return-variable control flow recovered the initializer/guard layouts; declaring the loop index before its pointer recovered the native thread-executor allocation; an explicit local next-PC value recovered CALL-frame scheduling. These are ordinary C hypotheses accepted only after full actual linked-byte comparison. The per-unit O3/speed settings above do not generalize to unrelated source units. Earlier sweep object-discovery counters with compiler-hash filename omissions are not used for progress measurements.

The existing encounter-access restrictions remain: original script predicate rearming does not prove ordinary contact, battle eligibility, full travel/reentry or renewable acquisition. Raw entry-reason values have not been relabeled as named win/capture/loss outcomes. The coordinator must preserve the previous matches in the combined source build before these 988 bytes enter the accepted progress ledger.
