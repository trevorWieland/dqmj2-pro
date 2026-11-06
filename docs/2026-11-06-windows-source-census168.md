# Windows source census at closed cohort 168

This is compilation and symbol evidence for the accepted source corpus, not a Windows game build. Source coverage stays at 11,339 functions / 1,172,627 initialized bytes (46.669195%).

The pinned Clang compiler produced i686 Windows COFF objects from **10,357 of 10,559 selected C/C++ source files**. Compilation failed for 202 files. Another 125 assembly source units were excluded because they need separately justified native platform implementations. Two compiler workers completed the census in 687.71 seconds without altering production source, compiler diagnostics or accepted-byte accounting.

The target uses four-byte pointers and the previously measured four-byte structure packing. Those layout choices establish a target convention; they do not establish original nominal types or complete host behavior.

| Compiler failure category | Source files |
| --- | ---: |
| Pointer/word type conversions | 123 |
| Missing type or declaration | 17 |
| Other compiler diagnostics | 62 |
| Total | 202 |

The initial symbol census had 99 files with unconfirmed selected entry names. Reading exact matching reports from committed snapshot `9e6aea5ee032dd24a884041a098b669534d88629` resolves 63 additional function names across 31 files. Each additional mapping checks program, processor, module, mode, address, extent, source path and source hash against actual emitted COFF names. **68 files still have unconfirmed selected symbols.** No function definition or alias was invented, and no source was recompiled for this reconciliation.

Authoritative reports:

- [Raw census](../evidence/portability/windows-source-census168-targetabi-v1-20261101.json), with pinned compiler, snapshot and compressed diagnostics.
- [Scoped symbol reconciliation](../evidence/portability/windows-source-census168-symbols-v1-20261106.json), with committed matching-report hashes and remaining omissions.
- [Routing qualification](../evidence/verification/windows-source-census168-routing-qualification-20261106.json), preserving the existing compiler/source/dependency/COFF checks while changing only the accepted snapshot, output paths and worker limit.

The next portability work is to recover and qualify actual pointer/handle/function interfaces, preserve matching variants through explicit migrations, resolve remaining symbols, and implement measured DS services on Windows. Blanket casts, suppressed diagnostics, placeholder routines, forced links and execution of original ARM scaffolding do not satisfy that work.

No complete native game link, game entry point, rendering/input/audio scenario, save/load scenario or native execution was established by this census. The full source-only ROM and Windows game obligations remain open under the [active objective](2026-11-05-source95-native-windows-goal.md).
