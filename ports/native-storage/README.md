# Native storage layer

This builds the checked guest-address mapper, byte-wise card-cache view, polling-read transfer algorithm and read-only host-file provider. The Windows x64 implementation uses Windows file APIs; Android uses `pread`. These are native C libraries for a reconstructed storage subsystem. A complete game, NitroFS mount parser and renderer are still separate work.

Use a native C11 compiler, CMake 3.22 or newer, Ninja and Python 3. Windows builds can use LLVM-MinGW or a Visual Studio developer environment:

```text
cmake -S ports/native-storage -B work/native-storage/windows -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build work/native-storage/windows
ctest --test-dir work/native-storage/windows --output-on-failure
```

Select a compiler with `-DCMAKE_C_COMPILER=...` when it is outside `PATH`. Host tests create deterministic synthetic files in the build directory and check 84 read cases, destination canaries, backend progress, cache contents, short reads and rejected mapping/budget cases. They use no original game inputs. Separate private qualification compares this subsystem with actual original ARM caller/helper execution under a synthetic 512-byte card-bus boundary; these public tests do not replace that oracle.

For Android, select the official NDK toolchain:

```text
cmake -S ports/native-storage -B work/native-storage/android-arm64 -G Ninja -DCMAKE_TOOLCHAIN_FILE=/path/to/ndk/build/cmake/android.toolchain.cmake -DANDROID_ABI=arm64-v8a -DANDROID_PLATFORM=android-33 -DANDROID_STL=none -DBUILD_TESTING=OFF -DCMAKE_BUILD_TYPE=Release
cmake --build work/native-storage/android-arm64
```

Android builds require resolved imports and 16 KiB ELF segment alignment, following [Android's native-library guidance](https://developer.android.com/guide/practices/page-sizes). Cross-compilation does not establish Android device execution or dual-display behavior.

Each guest mapping has explicit program, CPU, module and generation identities. The caller owns the lifetime of the backing RAM and file handle and provides synchronization. Windows seek/read operations sharing a handle must be serialized. Cached source/destination overlap is outside this port's supported domain. Complete blocks are committed individually; a later failure can follow earlier completed blocks. The block budget bounds work. This target selects only the current byte-wise cache implementation.
