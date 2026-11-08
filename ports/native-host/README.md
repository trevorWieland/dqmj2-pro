# Native display hosts

The Windows and Android hosts share a C11 session backed by the checked C7 matrix
API. They draw a calibration grid and marker, map input into a 256 × 192 viewport,
and preserve the session while surfaces change. These are intermediate native
port components. Game assets, DS graphics playback and gameplay remain unfinished.
They require no ROM, compiler license or reference emulator.

## Windows

Use a complete LLVM-MinGW installation, CMake, Ninja and Python 3.13:

```sh
cmake -S ports/native-host/windows -B work/native-host/windows -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build work/native-host/windows --parallel 2
ctest --test-dir work/native-host/windows --output-on-failure --timeout 15
work/native-host/windows/j2p_native_host.exe
```

Keep the executable beside `libj2p_native_scene_matrices.dll`. The smoke test
creates two real windows, resizes a client, rejects input in the letterbox margin,
checks the shared matrix translation and closes both windows. `--smoke-capture`
also saves uniquely named client-area BMP captures beside the executable.
Per-monitor DPI awareness is requested before window creation. A live move between
monitors with different DPI has not been tested.

## Android

Install Android platform 33, build-tools 35.0.1, NDK 30.0.16248370, a JDK supporting
Java release 8, CMake and Ninja. Pass their paths explicitly:

```sh
python ports/native-host/android/build_apk.py --sdk "$ANDROID_HOME" --ndk "$ANDROID_NDK_HOME" --jdk-bin "$JAVA_HOME/bin"
adb install -r work/native-host/android/dqm-native-host.apk
adb shell am start -n dev.dqmj2pro.dualsurface.native3/.MainActivity
```

The app discovers eligible displays dynamically and keeps one process/session.
With no eligible second display it presents both surfaces on the main display.
The package is a development app with a local debug signing key under `work/`.
Signing keys are not publication inputs.

The measured Thor run exercised two physical displays, mapped touch on both,
portrait/landscape changes, fallback and restoration, and generation/bounds
refusals. An owned virtual display's add/remove events were observed, but Android
refused activity launch there. Active physical hot-unplug remains untested.
Both native libraries and the APK are aligned for 16 KiB pages; the test device
used 4 KiB pages, so execution on a 16 KiB device remains untested.

The hosts add no ARM matching, source-coverage or ByteMatch credit. Their native
component tests and display tests do not establish a playable native game.
