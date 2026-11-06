import gzip
import hashlib
import json
import struct
import subprocess
from pathlib import Path
from project import ROOT, read_json, write_json, sha256
import check_main_joint_scalar752_windows32_20261102 as windows
import main_texture_pattern436_fixture_20261102 as fixture

NATIVE = ROOT / 'evidence/matches/main-texture-pattern436-v3-20261102.json'
REPORT = ROOT / 'evidence/ports/main-texture-pattern436-windows32-20261102.json'
SOURCE_DIR = ROOT / 'src/runtime/20261102_texture_pattern436'
HELPERS = [
    'src/runtime/20261101_resource_dictionary/native_main_0202bbb4.c',
    'src/runtime/main-null01/native_main_0202bf88.c',
    'src/runtime/main-null01/native_main_0202bfb4.c',
    'src/runtime/20261101_animation_obj352/native_main_0202bfe0.c',
    'src/runtime/20261101_animation_obj352/native_main_0202c054.c',
]


def main():
    native = read_json(NATIVE)
    pin = next(r for r in native['replayDependencies'] if r['path'].endswith('.json.gz'))
    assert sha256(ROOT / pin['path']) == pin['sha256']
    cases = json.loads(gzip.decompress((ROOT / pin['path']).read_bytes()))['cases']
    assert len(cases) == 3072
    windows.WORK = ROOT / 'work/main-texture-pattern436-windows32-20261102'
    windows.DRIVER = ROOT / 'src/ports/20261102_texture_pattern436/driver.c'
    own = [SOURCE_DIR / f'native_main_{address:08x}.c' for address in fixture.OWN]
    aliases = '\n'.join(f'#define native_fn_{address:08x} native_main_{address:08x}'
        for address in [*fixture.HELPERS, 0x02034248, 0x02034320]) + '\n'
    results = []
    for kind in [-1, 0, 1, 2]:
        label = 'preferred' if kind < 0 else native['negativeControls'][kind]['label']
        paths = list(own)
        if kind >= 0: paths[kind] = ROOT / native['negativeControls'][kind]['source']
        paths += [ROOT / name for name in HELPERS]
        folder = windows.WORK / label
        folder.mkdir(parents=True, exist_ok=True)
        wrapped = []
        for ordinal, path in enumerate(paths):
            wrapper = folder / f'unit-source-{ordinal}.c'
            wrapper.write_text(aliases + '#include "' + path.as_posix() + '"\n', encoding='utf-8')
            wrapped.append(wrapper)
        windows.SOURCES = wrapped
        exe, built = windows.compile_sources(label)
        built['unmodifiedSourceInputs'] = [dict(path=p.relative_to(ROOT).as_posix(), sha256=sha256(p)) for p in paths]
        indices = list(range(3072)) if kind < 0 else [i for i in range(3072) if fixture.inputs(i)[2] == list(fixture.OWN)[kind]]
        chunks, expected = [struct.pack('<I', len(indices))], []
        for index in indices:
            page, output, entry, args, context = fixture.inputs(index)
            assert hashlib.sha256(output).hexdigest() == cases[index]['dataSha256']
            chunks.append(struct.pack('<4I', entry, *args) + page)
            expected.append(output)
        run = subprocess.run([str(exe)], input=b''.join(chunks), cwd=ROOT.parent, capture_output=True,
            timeout=120, creationflags=subprocess.CREATE_NO_WINDOW)
        assert run.returncode == 0, (label, run.returncode, run.stderr)
        stride = 65540
        assert len(run.stdout) == len(indices) * stride
        rejected, digests = 0, []
        for ordinal, wanted in enumerate(expected):
            offset = ordinal * stride
            assert struct.unpack_from('<I', run.stdout, offset)[0] == ordinal
            output = run.stdout[offset + 4:offset + stride]
            rejected += output != wanted
            digests.append(hashlib.sha256(output).hexdigest())
        assert (rejected == 0) == (kind < 0)
        if kind >= 0: assert rejected == native['negativeControls'][kind]['modelRejections']
        results.append(dict(label=label, build=built, actualPublicCalls=len(indices), rejected=rejected,
            positiveControls=len(indices) - rejected, outputDigest=hashlib.sha256(''.join(digests).encode()).hexdigest()))
    write_json(REPORT, dict(passed=True, sourceCredit=0, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        preferred=results[0], controls=results[1:], actualPreferredPublicCalls=3072, actualWrongPublicCalls=3072,
        unmodifiedTargetAndFiveHelperBodies=True, separateTranslationUnits=8,
        arithmeticHardwareCalls=0, arithmeticHardwareBoundary='Fails the process if exercised',
        entire65536ByteInputOutputCompared=True, nativeReportSha256=sha256(NATIVE),
        fullGame=False, renderedUi=False, androidDeviceExecutions=0,
        reproductionCommand='python check_main_texture_pattern436_windows32_20261102.py'))
    print(dict(preferred=3072, wrong=3072, rejected=sum(r['rejected'] for r in results[1:]),
        unmodifiedSourceTranslationUnits=8, hardwareCalls=0))


if __name__ == '__main__':
    main()
