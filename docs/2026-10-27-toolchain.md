# Local toolchain validation — 2026-10-27

This repository uses locally installed, pinned tools for the measured modified-build ROM namespace `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`. Tool smoke tests, source byte comparisons, behavior checks, module linking, and whole-ROM matching are separate results.

## Installed tools

| Tool | Pin | Installation |
| --- | --- | --- |
| ds-decomp CLI | 0.12.1 | `tools/dsd.exe`; retained validated binary |
| Metrowerks compiler | pack directory 2.0/base; actual Version 3.0 build 114 | `tools/mwccarm/mwccarm/2.0/base/mwccarm.exe` |
| Metrowerks linker | actual Version 2.0 build 82 | `tools/mwccarm/mwccarm/2.0/base/mwldarm.exe` |
| objdiff CLI | 3.8.3, commit `9aeec9cbab1a056ade7dc1f1625aacc41b0f8511` | `tools/objdiff/3.8.3/objdiff-cli.exe` |
| Ghidra | 12.2, official `ghidra_12.2_PUBLIC_20261016.zip` | `tools/ghidra/ghidra_12.2_PUBLIC` |
| Java | Temurin JDK 25.0.5+8, Windows x64 HotSpot | `tools/jdk/jdk-25.0.5+8` |
| m2c | commit `c632946b8cfbe8fce442b522dba92dfa72f1f317` | `tools/m2c/m2c-c632946b8cfbe8fce442b522dba92dfa72f1f317` |
| graphviz Python package | 0.20.3 | `tools/m2c-python`; no global package installation |
| Python runtime | 3.13.5, x64 MSC build | Explicit runtime path and executable SHA-256 recorded in `tools.lock.json` |

The upstream ds-decomp release remains 0.12.1. Its inspected upstream HEAD remains `3b2df91c530ad144cbda0031abb7ce0eec3b1d83`. No ds-decomp upgrade was needed. Compiler settings remain specific to each measured source unit; these observations do not establish a universal compiler configuration.

## Integrity and reproduction

Normal installation enforces existing Python/native pins and cannot silently replace them. `install_tools.py` downloads candidate archives from official GitHub release assets or the pinned m2c source commit. It verifies archive digests, extracts into versioned local directories, installs the locked graphviz wheel into a local package directory, and writes `tools.lock.json`. The lock records every distributed candidate-tool file, executable hashes, native Python module/DLL hashes, distribution metadata, and the actual Python executable. Existing native dependencies are inspected without modification.

The m2c source archive hash was measured locally from its pinned upstream commit archive; unlike the binary release digests, it is not an upstream-published release checksum.

| Archive or executable | SHA-256 |
| --- | --- |
| ds-decomp Windows 0.12.1 | `5917df26bffc05d4752276a2e0b1edd21bd6e920aabe1992be8a50efc9d10932` |
| mwccarm 2.0/base | `7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880` |
| mwldarm 2.0/base | `bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74` |
| objdiff CLI Windows x64 3.8.3 | `dd12dfb5e9e94a7f6c949a37e1815963cf2cffe4c87b4999b7ebc8c15b398a1f` |
| Ghidra 12.2 archive | `2c2cd776db3c1f6a097ba418922378ac3649cadd5e844a6f5f088ae628a7be67` |
| Temurin JDK archive | `636bdc13dc649ddc7d5921c5c7d23cca6e44fd19d662b45cc9c02135a6c96c42` |
| m2c pinned source archive | `503714b92b14ba0e1affcc6decf4ad5763b37035cca66247858298cdf1b38971` |
| graphviz 0.20.3 wheel | `81f848f2904515d8cd359cc611faba817598d2feaac4027b266aa3eda7b3dde5` |

From this repository, using the pinned Python runtime:

```powershell
python install_tools.py --verify
python validation_tools.py
python match_thumb.py
python match_overlay004.py
```

`install_tools.py --verify` performs content checks without downloading, extracting, or replacing the lock. All commands return a nonzero exit status on their respective validation failures. The installer can be run separately when installation is required.

The imported native modules report Unicorn 2.1.4, pyelftools 0.33, and Capstone 5.0.7. Capstone distribution metadata reports 5.0.9. The lock preserves both observations and hashes the imported binding and DLL files rather than treating package metadata as proof of executable identity. No dependency version was silently substituted.

## Observed validation

`evidence/tools/validation.json` records 13 passing tool smoke checks: objdiff/JDK/m2c invocations, an objdiff checksum-object self comparison, ARM and Thumb m2c drafting/compilation probes, and three Ghidra headless imports. Passing the invocation or compilation check does not imply a draft matches source bytes.

Ghidra imported `arm9.bin`, `ov000.bin`, and `ov001.bin` as distinct programs in a private local project. Main loads at `0x02000000`; both overlays load at `0x021D7240` while retaining different program identities. The import script hashes all loaded bytes and compares them with each local module input. The main hash is `ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f`. Selected ARM and Thumb functions disassemble and decompile successfully. Whole-program automatic analysis and cross-module reference resolution remain unvalidated.

Ghidra runs through the distribution's headless Java entry point using the pinned Java executable, distribution VM arguments, a bounded heap, two worker CPUs, and repository-local settings/cache/profile directories. No global PATH, JAVA_HOME, or system policy was changed. Every subprocess has a timeout.

`dsd dis` output requires adaptation because it contains ds-decomp function macros and semicolon comments. The m2c probe removes these wrappers for selected functions and retains GNU-style text/global declarations. This small adapter was validated only on its recorded probes; it is not a general assembler round trip.

The native Thumb return-one probe at `main:0x0208B900` compiles to exactly four bytes with mwccarm 2.0/base plus the recorded `-thumb` flag. This address is counted once in the accepted Thumb source batch, not again as an additional tool-probe match.

The ARM checksum probe at `main:0x0207DA70` remains rejected. Without a prototype, m2c infers void return and removes the accumulator. A typed pointer context produces compiling C with incorrect pointer scaling and nonmatching bytes. Integer, void-pointer, and byte-pointer context experiments also failed the exact comparison: 44 compiled bytes versus 48 native bytes. Drafts, object hashes, failures, and context variants remain in `evidence/tools/`; the existing verified checksum implementation was preserved.

`match_thumb.py` verifies eight accepted main-module Thumb functions totaling 98 bytes, including literal pools after explicit `R_ARM_ABS32` resolution. It performs 576 native/recompiled Unicorn executions over 36 vectors per function, comparing registers, CPSR, ordered writes, target memory, and global buffers, with instruction and return-sentinel bounds. `evidence/matches/thumb.json` records each relocation, source/object hash, and measured ROM namespace. Actual module linking is established separately by the module worker.

`match_overlay004.py` verifies three unprotected ARM functions in overlay 4 totaling 32 bytes. Its 216 native/recompiled executions include null, ARM, and Thumb callbacks, callback memory effects, return values, registers, CPSR, and stack observations. The callback wrapper conditionally invokes its supplied pointer and returns its bitwise complement. This is an observed local behavior, not an inferred game-level identity. Protected overlay functions were not accepted by this batch.

Validation harness repairs and unsupported paths are recorded in `evidence/tools/validation-repairs.json`. Thumb attempt history includes an initially incorrect manual boundary length; current boundaries are read from the module-qualified symbol configuration.

## Deferred tools and remaining work

melonDS stable 1.1 is an upstream candidate, not an installed or validated tool here. No emulator instance was launched. Muted isolated GDB tracing remains deferred until it is needed, copied-save paths are verified, and debugger setup is tested. Its stable release is dated November 18, 2025.

Additional work includes broad Ghidra references and type recovery with overlay identity preserved, validation of m2c adaptation on more instruction patterns, and continued per-unit compiler matching. None of these tool probes establishes a complete module or whole-ROM reconstruction.

Primary sources: [ds-decomp release](https://github.com/AetiasHax/ds-decomp/releases/tag/v0.12.1), [ds-decomp pinned documentation](https://github.com/AetiasHax/ds-decomp/tree/3b2df91c530ad144cbda0031abb7ce0eec3b1d83), [objdiff release](https://github.com/encounter/objdiff/releases/tag/v3.8.3), [Ghidra release](https://github.com/NationalSecurityAgency/ghidra/releases/tag/Ghidra_12.2_build), [Ghidra 12.2 requirements](https://github.com/NationalSecurityAgency/ghidra/blob/Ghidra_12.2_build/GhidraDocs/GettingStarted.md), [Temurin release](https://github.com/adoptium/temurin25-binaries/releases/tag/jdk-25.0.5%2B8), [m2c pinned source](https://github.com/matt-kempster/m2c/tree/c632946b8cfbe8fce442b522dba92dfa72f1f317), [melonDS release](https://github.com/melonDS-emu/melonDS/releases/tag/1.1).

## Compiler and ARM7 observations

The compiler pack directory label differs from its executable identity: `2.0/base/mwccarm.exe` reports Version 3.0 build 114, built March 30, 2006. The linker independently reports Version 2.0 build 82. The lock records their measured banners and hashes. Matching configurations reproduce individual source units without uniquely establishing the historical original compiler.

`validate_compiler_archive.py` independently compares each adopted compiler executable with its exact member in the pinned compiler ZIP, then compiles and executes a signed 16-bit multiplication smoke test in 100 isolated states per compiler. Base, SP1p5, SP1p6 and 1.2/base pass 400 total calls. Their hashes and flags remain per-unit evidence; the two checksum helpers' settings are not generalized. SP1p5 SHA-256 is `89b2fc16c7f1f29ede1e52bdee5bc8ae4d63fe7e50d8074354dfd92c43d47aca`; 1.2/base is `87b4f748825ded418355e4ae35e032ce8b27c083cc4c60598ce2a75d346e4399`. Compiler archive SHA-256 is `dc386e37b2176e960954a733de928337d9b7e7620b9e94228008c31774339ace`. Linker validation remains independent of those compiler smoke tests.

SP1p6 was adopted only after independent archive-member/DLL comparisons and 1,936 arithmetic, shift/wrap and checked-memory executions across ARM/Thumb, optimization goals and caller return modes. Its executable is SHA-256 `2819dea7ae847ff83699d18bbc567238abe2804b6783b3bcc5893c5e546b0334`, reporting Version 3.0 build 133, runtime June 18, 2007. Evidence is in `evidence/save/compiler-sp1p6.json`; the reproducible validator is `evidence/save/validate_sp1p6.py`. This bounds that executable, not every optimization or a historical compiler assignment. Each additional source match still requires its own complete bytes, real linking and behavioral evidence.

The assembler reports Version 1.0 build 20, SHA-256 `e928cbcce71d687fadf25cf426280f23252e2aaae897fc2ce4e5570d8554dc8c`. ARM9 uses `-proc arm5TE`; ARM7 uses `-proc arm4t`. Justified assembly contains verified mnemonic instructions and actual literal pools. Ordinary logic remains C.

ARM7 Thumb SVC wrappers at measured halfword addresses exposed the assembler's default four-byte section alignment. The integrator stages an explicit section-alignment-only change to two bytes for these justified units. Frozen source/object identities remain intact; source-unit evidence records each placement change and full-module comparison must pass.

MW's linked ELF uses virtual segments while writing initialized bytes to separate module binaries. Source BSS is validated as NOBITS before linking, then checked by linked symbol address/size and its zero-file-size memory segment. `elf_units.py` preserves both implicit-addend REL and explicit-addend RELA records. ARM7 startup, initialized data, zero-fill storage and physical descriptor metadata remain separate evidence classes. Failed symbol checks invalidate ARM7 source-link acceptance independently of ARM9.
