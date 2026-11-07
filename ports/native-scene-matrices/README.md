# Native scene matrices

This standalone C11 library provides checked Q12 matrix commands, node poses,
static SBC plans, owned scene event tapes and per-shape matrix snapshots. Its
POSITION adapter produces homogeneous coordinate records in command order.
The separate warm BB7 API requires explicit caller-owned, coherent cached state.
See the contracts beside each runtime component for supported inputs and refusals.

The library builds for Windows x64 and Android ARM64, API 33, with 16 KiB ELF
segment alignment. Rendering, animation, gameplay and Android device execution
remain unproven. Cold billboard cache generation, BB8 and a billboard scene walker
are outside this target's qualified scope.

Configure with a qualified Clang or GCC C11 compiler. The Windows CI uses pinned
LLVM-MinGW and runs both Release and Debug:

```sh
cmake -S ports/native-scene-matrices -B work/native-scene-matrices -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build work/native-scene-matrices
ctest --test-dir work/native-scene-matrices --output-on-failure
```

For Android, pass the NDK toolchain and disable host tests:

```sh
cmake -S ports/native-scene-matrices -B work/native-scene-matrices-android -G Ninja -DCMAKE_TOOLCHAIN_FILE="$ANDROID_NDK_HOME/build/cmake/android.toolchain.cmake" -DANDROID_ABI=arm64-v8a -DANDROID_PLATFORM=android-33 -DANDROID_STL=none -DBUILD_TESTING=OFF -DCMAKE_BUILD_TYPE=Release
cmake --build work/native-scene-matrices-android
python ports/native-storage/check_android_elf.py work/native-scene-matrices-android/libj2p_native_scene_matrices.so
```

The four host tests exercise planning, event/snapshot replay, signed coordinate
decoding, retained state, warm matrix effects and atomic refusal of unsupported
inputs. Their model fixtures are synthesized test data; no ROM, compiler license,
original assets or reference emulator is needed. The POSITION fixtures include
eight models and sixteen coordinate records. Warm tests cover twelve successful
cases and forty-seven refusals. The copied test inputs and qualified C/header
hashes are recorded in `qualified-source-manifest.json`.

These portable components add no accepted ARM matching or ByteMatch progress
credit. The original matrix capture provenance was superseded by the corrected
capture-v2 qualification listed in the manifest; the matrix implementation stayed
unchanged.
