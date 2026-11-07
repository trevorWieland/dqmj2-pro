# Native resource pipeline

This standalone C11 library connects a file-backed NitroFS mount to the recovered resource loader, bounded arena, dictionary search and texture/palette material setters. It selects 20 C inputs, including unchanged accepted loader/setter files and separate fixed-width filesystem views. Original DS sources and matching credit remain unchanged.

Use CMake 3.22 or newer, Ninja, Python 3 and a Clang or GCC compiler. Windows builds are qualified with LLVM-MinGW:

```text
cmake -S ports/native-resources -B work/native-resources/windows-release -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build work/native-resources/windows-release
ctest --test-dir work/native-resources/windows-release --output-on-failure
```

Select a compiler with `-DCMAKE_C_COMPILER=...` when needed. Repeat with a separate build directory and `-DCMAKE_BUILD_TYPE=Debug` to test the unoptimized path. C11 mode preserves the recovered declarations; the canonical inline-export unit supplies the SDK helper definitions required by non-MSVC targets. Two comparison views suppress the signed-comparison warning while retaining their original definitions and the validated 127-byte name bound.

The host test uses only the Python standard library and generated synthetic NDS files, names, metadata and material records. It exercises real filesystem mounting and file I/O, linear/Patricia lookup, six dictionary sizes, eight texture formats, full VRAM-key masks, front/back allocation, immutable payloads and guard bytes. It checks namespace, generation, path, empty-file and malformed-table cases. No original game, private manifest, ROM compiler, ARM interpreter or downloaded asset is required. These public model checks complement the separate owner-private original-code qualification.

Build Android ARM64 with the official NDK toolchain:

```text
cmake -S ports/native-resources -B work/native-resources/android-arm64 -G Ninja -DCMAKE_TOOLCHAIN_FILE=/path/to/ndk/build/cmake/android.toolchain.cmake -DANDROID_ABI=arm64-v8a -DANDROID_PLATFORM=android-33 -DANDROID_STL=none -DBUILD_TESTING=OFF -DCMAKE_BUILD_TYPE=Release
cmake --build work/native-resources/android-arm64
python ports/native-storage/check_android_elf.py work/native-resources/android-arm64/libj2p_native_resources.so
```

Android links require resolved imports and 16 KiB load-segment alignment, following [Android's native-library guidance](https://developer.android.com/guide/practices/page-sizes). Linking establishes no Android or AYN Thor execution.

The target selects `nitrofs_resource_bridge_20261106.c` exclusively. Do not also compile the original `resource_bridge_20261106.c`. Mounts own immutable FAT/FNT snapshots; resource contexts borrow their mounts and must be destroyed first. Caller-owned mapped RAM remains live until all operations finish. Program, CPU, module and generation identities must match. All related calls and shared file handles require external serialization; active-call guards provide no thread synchronization.

The filesystem supports root-based `rom:` paths, ASCII case folding, slash/backslash and dot traversal. It supplies bounded synchronous dispatch, reads and file-ID lookup. Only the last physical sector of a trimmed image is padded; requested file bytes remain within the input. Current-directory changes, other archives, writes, full async scheduling and NARC parsing require further work.

Material setters update descriptors from VRAM-key metadata. They supply no VRAM upload, draw service or host renderer. The unreachable division boundary in the qualified distinct-object domain terminates if called. The library does not establish game bootstrap, rendering, input, audio, device execution or playable-game status.
