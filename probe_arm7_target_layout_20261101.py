import os
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from project import ROOT, read_json, write_json, sha256
from probe_windows_target_layout_20261101 import SOURCE, FIELDS, elf_values


def main():
    reference_path = ROOT / 'evidence/portability/windows-target-layout-20261101.json'
    reference = read_json(reference_path)
    assert sha256(SOURCE) == reference['source']['sha256']
    expected = reference['armTargets'][0]['values']
    work = ROOT / 'work/arm7-target-layout-20261101'
    work.mkdir(parents=True, exist_ok=True)
    targets = []
    for index, target in enumerate(reference['armTargets']):
        compiler = ROOT / f"tools/mwccarm/mwccarm/{target['profile']}/mwccarm.exe"
        assert sha256(compiler) == target['compilerSha256']
        obj = work / f'profile-{index}.o'
        command = list(map(str, [compiler, '-O2', '-enum', 'int', '-char', 'signed', '-proc', 'arm7tdmi',
            '-gccinc', '-nolink', '-c', SOURCE, '-o', obj]))
        run = subprocess.run(command, cwd=ROOT, capture_output=True, timeout=60,
            env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')),
            creationflags=subprocess.CREATE_NO_WINDOW)
        assert run.returncode == 0, run.stderr.decode(errors='replace')
        values = dict(zip(FIELDS, elf_values(obj)))
        assert values == expected
        targets.append(dict(profile=target['profile'], compilerSha256=sha256(compiler), command=command,
            values=values, objectSha256=sha256(obj), matchesMeasuredArm9AndWindowsPack4=True))
    report = dict(passed=True, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        arm7Targets=targets, reference=dict(path=reference_path.relative_to(ROOT).as_posix(), sha256=sha256(reference_path)),
        source=dict(path=SOURCE.relative_to(ROOT).as_posix(), sha256=sha256(SOURCE)),
        sourceCredit=0, gameExecutionCount=0,
        limitations=['Primitive/nested record probes only; explicit source assertions and native behavior checks remain required'])
    write_json(ROOT / 'evidence/portability/arm7-target-layout-20261101.json', report)
    print(dict(passed=True, arm7Profiles=len(targets), arm9AndWindowsPack4Agreement=True, sourceCredit=0))


if __name__ == '__main__':
    main()
