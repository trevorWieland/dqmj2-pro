# ROM-free native component probe

`j2p_scene_probe` tests only checked CPU-side scene matrices, event snapshots,
homogeneous positions and the separate warm-state API. It uses eight synthetic
scene fixtures, eight position fixtures and four warm cases. Thirty-one refusal
checks verify unchanged outputs. It reads no ROM, assets, saves or configuration
files and writes only stdout/stderr. No APK or emulator is needed.

The Windows executable runs beside its DLL. For Android, build using the README
API 33 command, or obtain both files from the same `native-scene-matrices` CI
artifact. With the selected device authorized in ADB, create a new temporary
directory and copy only these two files:

```sh
adb shell mkdir /data/local/tmp/j2p-native-scene-probe
adb push work/native-scene-matrices/android/j2p_scene_probe /data/local/tmp/j2p-native-scene-probe/
adb push work/native-scene-matrices/android/libj2p_native_scene_matrices.so /data/local/tmp/j2p-native-scene-probe/
adb shell chmod 700 /data/local/tmp/j2p-native-scene-probe/j2p_scene_probe
adb shell 'LD_LIBRARY_PATH=/data/local/tmp/j2p-native-scene-probe /data/local/tmp/j2p-native-scene-probe/j2p_scene_probe'
```

Success returns exit code 0 and JSON with `status: C7_ROMFREE_PROBE_PASS`,
`positionRecords: 16`, `sceneReferences: 16`, `sceneSubmissions: 10`,
`warmCases: 4` and `refusals: 31`. Capture the output, then remove only the two
test files and their directory:

```sh
adb shell rm /data/local/tmp/j2p-native-scene-probe/j2p_scene_probe /data/local/tmp/j2p-native-scene-probe/libj2p_native_scene_matrices.so
adb shell rmdir /data/local/tmp/j2p-native-scene-probe
```

On 2026-11-07 the same probe C source, compiled with NDK r30 and linked to the
public C7 CI library, passed on one AYN Thor: ARM64, Android 13/API 33, 4096-byte
pages. Transfers were hash-checked and temporary files were removed. The
[curated receipt](../../evidence/ports/ayn-thor-native-scene-probe-20261107.json)
pins that executable and library. This observed run predates the CMake packaging;
it does not claim every subsequent artifact was executed on a device. ELF
segments are aligned to 16 KiB; actual execution on a 16 KiB page device remains
unproven.

There is no window, renderer, texture upload, display output, animation or game
execution in this probe. Display IDs require discovery at runtime and are not
fixed platform identifiers. No dual-screen rendering is claimed.
