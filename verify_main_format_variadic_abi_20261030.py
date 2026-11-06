import subprocess
from project import ROOT, read_json, sha256, write_json


def main():
    report = read_json(ROOT / 'evidence/matches/main-format-wrappers-20261030.json')
    row = next(item for item in report['matches'] if int(item['address'], 0) == 0x0201D444)
    source = ROOT / row['source']
    assert sha256(source) == row['sourceSha256'] and sha256(ROOT / row['object']) == row['objectSha256']
    build = read_json(ROOT / 'evidence/portability/windows-runtime-build-20261030.json')
    clang = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin/clang.exe'
    assert sha256(clang) == build['compilerSha256']
    target = ROOT / 'work/main-format-wrappers-20261030/host-abi-rejection.obj'
    process = subprocess.run([str(clang), '--target=x86_64-pc-windows-msvc', '-ffreestanding', '-c', str(source), '-o', str(target)],
                             capture_output=True, text=True, timeout=60)
    assert process.returncode != 0 and 'NdsWordPointerRequired' in process.stderr
    assert sha256(source) == row['sourceSha256'] and sha256(ROOT / row['object']) == row['objectSha256']
    write_json(ROOT / 'evidence/verification/main-format-variadic-host-abi-rejection-20261030.json',
               {'source': row['source'], 'sourceSha256': row['sourceSha256'], 'compilerSha256': sha256(clang),
                'incorrect64BitHostBuildRejected': True, 'exitCode': process.returncode, 'stderr': process.stderr,
                'ndsSourceAndObjectUnchanged': True, 'sourceCredit': 0})
    print({'incorrect64BitAbiRejected': True, 'nativeMatchedSourceUnchanged': True})


if __name__ == '__main__':
    main()
