# Early native Android checksum validation, 2026-10-29

`python prepare_android_checks.py` builds a private portable source bundle at `build/android-native-validation-bundle/`. It contains the unchanged matched `src/save_checksum.c`, a C11 runner, generated synthetic golden vectors and CMake configuration. It includes no original ROM/save payload, DS executable blob, game asset, compiler archive or license.

The generator passes 50 deterministic synthetic vectors through both original ARM9 checksum functions, checking actual return, preserved state and unchanged input against independent little-endian sums. All 100 native calls pass. Zero/all-set/ramp/alternating data, 32 xorshift seeds and checksum-boundary single-word cases are represented. Artifact/source/native-input hashes and statuses are in `evidence/portability/android-checksum-bundle-20261029.json` and the bundle manifest. These are additional synthetic goldens; they do not replace the preserved 36-vector/144-execution matching regression.

No Android compilation or Android execution has occurred. The environment probe found no NDK/SDK paths or adb/CMake/Ninja/Clang on PATH. The C runner itself has not been compiled on a host yet. Cross-compilation success must not be reported as device execution. CTest is enabled only for non-cross builds; the runner reports whether it was compiled for Android or a host.

The [research note](2026-10-29-native-android-decomp-research.md) identifies the current official NDK and device/ABI/page-size gates. A local NDK plus CMake/Ninja is sufficient for the first compile; no game renderer or APK shell is needed. A candidate Thor-specific invocation, after separately obtaining and pinning those tools, is:

```powershell
$ndkPath = 'C:/PrivateTools/android-ndk-r30'
$bundleRoot = 'C:/Private/J2P/android-native-validation-bundle'
cmake -S "$bundleRoot/ports/android-native" -B "$bundleRoot/build/android-arm64" -G Ninja -DCMAKE_TOOLCHAIN_FILE="$ndkPath/build/cmake/android.toolchain.cmake" -DANDROID_ABI=arm64-v8a -DANDROID_PLATFORM=android-33 -DCMAKE_BUILD_TYPE=Release
cmake --build "$bundleRoot/build/android-arm64"
```

Those are example paths, not installed tools. Android 33 remains a candidate based on advertised Android 13; actual firmware/SDK/ABIs must be measured. Retain the official NDK toolchain defaults. Inspect the produced ELF and runtime dependencies/page alignment before any approved device replay. No device transfer, deployment, emulator, audio or system-policy action is part of this bundle preparation.

A later physical-device report must identify device/firmware/ABI/runtime page size and source/tool/executable/corpus hashes, then capture 50 vectors, 100 function comparisons and zero failures from the actual Android runner. Windows or local-container output is not that report. Display enumeration, independent top/bottom test patterns, touch/controller routing and lifecycle checks come afterward; two physical panels do not prove Android logical-display behavior. Full native gameplay needs the DS platform replacement in addition to recovered logic.
