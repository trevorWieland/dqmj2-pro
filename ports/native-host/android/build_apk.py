import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import uuid
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SUFFIX = '.exe' if os.name == 'nt' else ''


def owned(path):
    result = path.resolve()
    if not result.is_relative_to(ROOT / 'work') or result == ROOT / 'work':
        raise ValueError('Build outputs must be below repository work/')
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sdk', type=Path, required=True)
    parser.add_argument('--ndk', type=Path, required=True)
    parser.add_argument('--jdk-bin', type=Path, required=True)
    parser.add_argument('--cmake', default=shutil.which('cmake'))
    parser.add_argument('--ninja', default=shutil.which('ninja'))
    parser.add_argument('--build-dir', type=Path, default=ROOT / 'work/native-host/android')
    parser.add_argument('--keystore', type=Path)
    args = parser.parse_args()
    if not args.cmake or not args.ninja:
        parser.error('CMake and Ninja must be installed or supplied explicitly')
    build = owned(args.build_dir)
    sdk, ndk, jdk = args.sdk.resolve(), args.ndk.resolve(), args.jdk_bin.resolve()
    tools = sdk / 'build-tools/35.0.1'
    jar = sdk / 'platforms/android-33/android.jar'
    if 'Pkg.Revision = 30.0.16248370' not in (ndk / 'source.properties').read_text():
        raise ValueError('Android NDK 30.0.16248370 is required')
    build.mkdir(parents=True, exist_ok=True)
    logs = build / 'runs' / uuid.uuid4().hex
    logs.mkdir(parents=True)
    rows = []

    def run(label, command, timeout=120):
        command = [str(value) for value in command]
        started = time.monotonic()
        result = subprocess.run(command, cwd=ROOT, capture_output=True, timeout=timeout)
        (logs / (label + '.stdout')).write_bytes(result.stdout)
        (logs / (label + '.stderr')).write_bytes(result.stderr)
        rows.append(dict(label=label, argv=command, exitCode=result.returncode, seconds=time.monotonic() - started))
        (logs / 'commands.json').write_text(json.dumps(rows, indent=2) + '\n', encoding='utf8')
        if result.returncode:
            raise RuntimeError(label + ': ' + result.stderr.decode(errors='replace')[-3000:])

    run('configure', [args.cmake, '-S', HERE, '-B', build, '-G', 'Ninja',
        '-DCMAKE_MAKE_PROGRAM=' + args.ninja, '-DCMAKE_TOOLCHAIN_FILE=' + str(ndk / 'build/cmake/android.toolchain.cmake'),
        '-DANDROID_ABI=arm64-v8a', '-DANDROID_PLATFORM=android-33', '-DCMAKE_BUILD_TYPE=Release',
        '-DPython3_EXECUTABLE=' + sys.executable])
    run('native', [args.cmake, '--build', build, '--parallel', '2'], 300)
    classes, dex = build / 'classes', build / 'dex'
    classes.mkdir(exist_ok=True)
    dex.mkdir(exist_ok=True)
    java = jdk / ('java' + SUFFIX)
    run('javac', [jdk / ('javac' + SUFFIX), '--release', '8', '-classpath', jar, '-d', classes,
        *sorted((HERE / 'app/java').rglob('*.java'))])
    run('jar', [jdk / ('jar' + SUFFIX), '--create', '--file', build / 'classes.jar', '-C', classes, '.'])
    run('dex', [java, '-cp', tools / 'lib/d8.jar', 'com.android.tools.r8.D8', '--min-api', '33',
        '--lib', jar, '--output', dex, build / 'classes.jar'])
    run('manifest', [tools / ('aapt2' + SUFFIX), 'link', '-o', build / 'unsigned.apk',
        '--manifest', HERE / 'app/AndroidManifest.xml', '-I', jar])
    with zipfile.ZipFile(build / 'unsigned.apk', 'a', compression=zipfile.ZIP_STORED) as bundle:
        bundle.write(dex / 'classes.dex', 'classes.dex')
        for path in (build / 'libj2p_dualsurface.so', build / 'c7/libj2p_native_scene_matrices.so'):
            bundle.write(path, 'lib/arm64-v8a/' + path.name)
    run('align', [tools / ('zipalign' + SUFFIX), '-P', '16', '-f', '4', build / 'unsigned.apk', build / 'aligned.apk'])
    key = args.keystore.resolve() if args.keystore else build / 'local-debug.p12'
    if not key.exists():
        run('key', [jdk / ('keytool' + SUFFIX), '-genkeypair', '-keystore', key, '-storepass', 'android',
            '-keypass', 'android', '-alias', 'native3', '-keyalg', 'RSA', '-keysize', '2048',
            '-validity', '365', '-dname', 'CN=DQM Native Surface Lab'])
    apk = build / 'dqm-native-host.apk'
    run('sign', [java, '-jar', tools / 'lib/apksigner.jar', 'sign', '--ks', key, '--ks-key-alias', 'native3',
        '--ks-pass', 'pass:android', '--out', apk, build / 'aligned.apk'])
    run('signature', [java, '-jar', tools / 'lib/apksigner.jar', 'verify', '--verbose', apk])
    run('page-alignment', [tools / ('zipalign' + SUFFIX), '-c', '-P', '16', '4', apk])
    for path in (build / 'libj2p_dualsurface.so', build / 'c7/libj2p_native_scene_matrices.so'):
        allowed = ['libj2p_native_scene_matrices.so', 'libandroid.so', 'liblog.so'] if path.name == 'libj2p_dualsurface.so' else []
        options = [value for library in allowed for value in ('--allow-library', library)]
        run('elf-' + path.stem, [sys.executable, ROOT / 'ports/native-storage/check_android_elf.py', path, *options])
    result = dict(status='BUILT_AND_STATIC_CHECKED', apk=str(apk), bytes=apk.stat().st_size,
        sha256=hashlib.sha256(apk.read_bytes()).hexdigest(), deviceTested=False, sourceCredit=0)
    (logs / 'result.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
