# Native Android checksum compilation — 2026-10-29

The unchanged synthetic checksum runner now compiles for `arm64-v8a`, Android API 33. Two builds in newly created directories, using different working directories, produce the same 8,952-byte ELF: SHA-256 `05aa7f1e22b8b55d602dd7f2044b954f6942d105aa9bc5a66a5902c129765a26`. No Android executable has run. Compiled goldens contain 50 synthetic vectors and 100 planned checksum comparisons; Android comparisons executed remain zero. This supersedes the toolchain-unavailable/compilation-not-run status in the earlier Android research and checksum-bundle notes.

`evidence/portability/android-arm64-compile-20261029.json` contains both exact command sequences, all 44 source/header dependency identities, linker-selected inputs, compiler definitions, raw LLVM inspection output and independent ELF parsing. It verifies ELF64 little-endian `EM_AARCH64`, `ET_DYN`, a dynamic PIE flag, `/system/bin/linker64`, Android API 33 and NDK r30/build16248370 notes, four LOAD segments aligned to 16,384 bytes, no writable executable LOAD and a non-executable stack. Dynamic dependencies are `libdl.so` and `libc.so`. Their measured inputs are API-33 link stubs; actual device libraries and runtime behavior were not inspected.

The [official NDK download table](https://developer.android.com/ndk/downloads) identifies r30 LTS revision `30.0.16248370`, Windows ZIP size 727,980,788 bytes and SHA-1 `9bf167a1985fa7d4a036186b78f702eab9179408`. The downloaded archive matches those publisher values. Its independently measured SHA-256 is `b830098aaf18b67a42eb831c404e15e5f2990a474f054ac145b0bc957ac6d729`; this SHA-256 is a local pin, not a publisher SHA-256 claim. The [official changelog](https://github.com/android/ndk/wiki/Changelog-r30) identifies clang-r574158c and maximum sysroot API 37. Local source properties and tool output confirm the revision, Clang/LLD 21.0.0 and LLVM commit `9f872551d3c681d06fd303b36f16ed5c274735eb`.

The portable SDK was first downloaded/extracted under ignored `build/android-toolchain-staging/20261029-r30/`, while clean replay G copied its tools/dependencies/inputs. Only after the coordinator confirmed that copy finished was the unchanged extraction moved to `tools/android-ndk/r30/`. All four measured executable hashes survived the move and pass version smoke tests. The ZIP contains 9,108 entries and 2,158,087,806 uncompressed bytes. Free disk space before download was 586,393,567,232 bytes. `evidence/toolchains/android-ndk-r30-20261029.json` embeds the download, extraction, adoption and smoke provenance, official metadata snapshot hash, host identity, notices and current tool hashes. No system installation, PATH or system-policy change occurred.

Builds invoke the official Clang driver directly with `--target=aarch64-linux-android33` and an explicit repository-local sysroot, following Google's [other-build-systems guidance](https://developer.android.com/ndk/guides/other_build_systems). C11/O2, PIE and strict warnings are explicit. The core is compiled into a deterministic static archive; the runner is a separate object before linking. Compiler-affecting include/library environment variables are cleared only in child processes, and compiler temporary files remain inside each new build directory. The driver supplies Android definitions; no fake Android/API macro is injected. `__ANDROID_API__` expands through `__ANDROID_MIN_SDK_VERSION__`, which is measured as 33. Current [page-size guidance](https://developer.android.com/guide/practices/page-sizes) is checked against actual ELF LOAD alignment, not assumed from the NDK version.

For an existing private checkout with its recorded NDK and staged archive, replay from any working directory:

```powershell
python C:/Private/dqmj2pro-decomp/compile_android_checks_20261029.py
python C:/Private/dqmj2pro-decomp/compile_android_candidates_20261029.py
```

Replace the example checkout root with the actual private path. The scripts resolve all other paths from themselves. They do not require original ROM/save bytes for cross-compilation, and they do not execute the Android output. Existing checksum sources, runner and goldens are checked against the previously validated bundle hashes before and after compilation. The portable source bundle remains `build/android-native-validation-bundle/`; the generated binaries and logs are under `build/android-arm64-validation-20261029/`.

A new private checkout can obtain the same official portable toolchain using the following sequence. The adoption command refuses to overwrite an existing canonical NDK directory. Coordinate adoption with any concurrent tool/input snapshot copy, as done above.

```powershell
python stage_android_ndk_20261029.py download
python stage_android_ndk_20261029.py extract
python stage_android_ndk_20261029.py smoke
python stage_android_ndk_20261029.py adopt
python stage_android_ndk_20261029.py smoke
python record_android_toolchain_20261029.py
python compile_android_checks_20261029.py
```

The first download checks the selected release against current official metadata and verifies publisher size/SHA-1 before recording local SHA-256. The source-only portable bundle contains no NDK, original ROM/save, DS object/blob, proprietary compiler or license. A standalone consumer can instead use an independently obtained matching NDK and its own pinned build system; the existing CMake target was not exercised by this direct-driver validation. CMake/Ninja, Gradle, APK packaging, JNI, display/input, physical-device ABI/page size and a real Android runner remain separate work.

The next pure-source shortlist is measured in `evidence/portability/android-next-candidates-20261029.json`. All four unmodified units compile into AArch64 relocatable objects with strict warnings; they are not linked into a runnable suite and have not executed on Android. Their ten existing DS function matches remain independent evidence, not new credit from cross-compilation.

| Priority | Matched source unit | Proposed fixture contract |
| --- | --- | --- |
| 1 | `src/mechanics_save/sdk_crc.c` — six functions | Host-owned typed tables and state; all 256 table entries, independent bitwise models, empty/split/boundary-length updates. |
| 2 | `src/mechanics_save/runtime_rng.c` — one function | Explicit private unsigned32 state and signed limit; compare return plus advanced state, including nonpositive limits. Supplied seeds do not predict live scene state. |
| 3 | `src/mechanics_save/sdk_md5_block.c` — one function | Aligned state/block plus actual constant/index arrays; no unresolved-data stubs. |
| 4 | `src/mechanics_save/sdk_md5.c` — two functions | Assert context size88/count offset16/buffer offset24; implement measured copy/fill/compressor/padding contracts, then compare streaming splits and cleared context. |

The candidate report records ROM/CPU/module/address/mode, source/native span hashes and existing match-report hashes for every function, plus unresolved suite dependencies and test plans. CRC is the smallest self-contained next target. RNG needs one explicitly defined state object. MD5 needs genuine dependency bindings and layout assertions before execution. Serialized/DS addresses must remain logical values or be resolved through a typed memory interface; they must not be cast into Android host pointers.

The initial failed validator run was a metadata-parser issue: Clang defines the API macro by alias rather than a literal. Its build logs remain under `build/android-arm64-validation-20261029/failed-initial/`; alias resolution and fresh-directory validation now pass. No original port runner or goldens were changed. All Android compilation/metadata results contribute zero DS source-match, module or whole-ROM credit. A later authorized Android run must identify the actual target and separately record corpus/artifact/output hashes, actual termination and results.
