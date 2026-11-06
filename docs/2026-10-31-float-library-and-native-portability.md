# Floating library recovery and native portability

Nine newly qualified main ARM routines cover 1,572 initialized function bytes. They remain queued after cohort 94 until their complete module build is accepted. A separately generated 128-byte lowercase table is initialized data, with zero function or executable-byte credit.

| Address | Bytes | Measured operation | Actual native/C top returns |
| --- | ---: | --- | ---: |
| `0202263C` | 40 | Copy binary64 sign | 320 |
| `02022684` | 188 | Fraction/exponent decomposition | 320 |
| `02022740` | 588 | Binary exponent scaling | 320 |
| `02023E48` | 20 | Raw high-word sign mask | 320 |
| `02023E5C` | 112 | Binary64 class | 320 |
| `02022480` | 444 | Ceiling | 320 |
| `02022664` | 32 | Clear binary64 sign | 320 |
| `02023ECC` | 44 | Decompose then scale by combined exponent | 320 |
| `02023EF8` | 104 | Bounded case-insensitive raw-byte comparison | 3,584 |

The public reference is Petari revision `177da59137be40bcca5cd996e013c228ae20b198`, whose CC0 license was already independently recorded. Exact files and hashes are in `provenance/msl-math-reference-20261031.json` and `provenance/msl-ceil-reference-20261031.json`. Unmodified references stay in separate dependency directories. The adapted double-word views select the measured little-endian high/low words. They are not inferred original SDK names or a compiler-version identification. The unavailable public fabs file was not invented: its 32-byte source follows the measured sign-clear operation and independent bit model.

The first five units independently match O3 speed profiles; some smaller units also match O2. Ceiling and the 44-byte composition wrapper have their own measured profiles. No surrounding-source compiler configuration follows. All accepted proposals have real compiler objects, genuine MWLD symbol/layout/byte comparisons, isolated native/C machines, relevant register and complete public-memory effects, actual bounded return, and returning whole-C negative controls. The nine routines produce 6,144 actual top returns and 640 negative-control returns. Original arithmetic/classification helpers receive zero additional source credit. Unvisited/dead instructions remain distinct from byte matching.

An initial floor hypothesis for `02022480` was rejected by native returns: positive epsilon becomes one and negative epsilon becomes negative zero. The ceiling reference then matches all 444 bytes. Its original arithmetic canonicalizes NaNs to positive `7FFFFFFFFFFFFFFF`, including negative and payload NaNs. The initial payload-preserving model failed three of 160 native cases and is retained with its exact source/hash and characterization. The corrected model preserves this target behavior without changing the source or native code.

The comparator's initial guessed table address was a one-byte literal mismatch. Reading the measured literal established `020D8D04`. Its 128 bytes independently equal the ASCII uppercase-to-lowercase mapping with identity elsewhere in that bounded range. Input bytes 128..255 bypass the table. This proves a byte operation, not game text encoding, localization or Unicode behavior. The mathematical C table compiles and genuinely links to those 128 bytes. Its original consumers produce 3,584 returning checks plus sixteen compiled-data-mutant returns. Following data and enclosing historical object declarations remain separate.

Reproduce with `match_main_float_primitives_20261031.py`, `match_main_float_rounding_20261031.py`, `match_main_float_scale_wrapper_20261031.py`, `match_main_case_compare_20261031.py` and `match_main_ascii_lower_data_20261031.py`. The byte comparator uses 1,792 paired arrangements: all leading bytes, bounded lengths, ASCII case pairs and same-pointer cases. Unterminated strings, invalid pointers, full call-site reachability and floating exponent-addition overflow remain unsupported.

## Actual Windows and compiled Android subset

Run `python compile_float_runtime_ports_20261031.py`, then `python verify_windows_float_runtime_20261031.py`. Eight unchanged reconstructed sources and the mathematical table compile using the already pinned repository-local NDK r30 Clang/LLD. The Windows x64 DLL has no entry point/runtime imports and a zero PE timestamp. It passes 2,912 actual public calls against the native golden values and complete public effects. All 3,744 tested caller buffers lie above 4 GiB. Floating and byte-pointer ABI projections are explicit; ARM scratch registers and flags are not host C API requirements.

The measured integer word views require strict alias optimization disabled for these host tests. No source patch or warning suppression is used. Ceiling is deliberately excluded from this portability subset because its original ARM addition canonicalizes NaNs differently from ordinary host arithmetic. That unresolved target-arithmetic adaptation is retained, not normalized away or counted as an eight-function success.

The same source set compiles as an Android API 33 AArch64 shared library with no needed shared libraries and at least 16 KiB load alignment. Recompiling from the repository's parent directory reproduces both Windows and Android binary hashes. These are compilation and Windows-execution results, with zero new DS source coverage.

Run `python prepare_float_runtime_android_20261031.py` to build the console runner and `build/android-float-runtime-bundle-20261031/`. Its executable is `j2p_float_runtime_check_arm64`; a successful future run must exit zero and print `J2P float runtime: 2912 cases passed`. The bundle contains unchanged C sources, the runner, generated synthetic vectors and hashed metadata, with no ROM/save/game assets. Its ELF/API/PIE/alignment properties are inspected. Platform libc supplies console output and buffer operations.

No device transfer or execution occurred. Android device/API compatibility, dual-screen rendering/input/audio, save integration and full-game execution remain unproved. The complete Windows game is also unproved. Build receipts are in `evidence/portability/float-runtime-build-20261031.json`, `windows-float-runtime-execution-20261031.json`, `float-runtime-cross-directory-20261031.json` and `android-float-runtime-runner-20261031.json`.
