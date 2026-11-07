import json
import re
from pathlib import Path
from project import ROOT, sha256, read_json, write_json
import match_runtime as compiler

SOURCE = ROOT / 'src/runtime/goal_resume20261106/source_1'
WORK = ROOT / 'work/goal-resume-20261106/source-1'
CLAIM = ROOT / 'evidence/lanes/parallel-wave20261106/goal-resume-source-1/claim.json'


def compare(source, output):
    source, output = Path(source).resolve(), Path(output).resolve()
    if not source.is_relative_to(SOURCE) and not source.is_relative_to(WORK):
        raise ValueError('Source is outside the reassigned source lane')
    if not output.is_relative_to(WORK):
        raise ValueError('Compiler output is outside the reassigned work lane')
    claim = read_json(CLAIM)
    names = re.findall(r'\bnative_main_([0-9a-f]{8})\s*\(', source.read_text())
    allowed = {format(int(row['address'], 0), '08x') for row in claim['claimedFunctions']}
    if len(names) != 1 or names[0] not in allowed:
        raise ValueError('Compiler source does not name one exclusively reassigned function')
    for path, expected in claim['inputPins'].items():
        if sha256(ROOT / path) != expected:
            raise ValueError('Pinned source-lane input changed: ' + path)
    saved_work, saved_flags = compiler.WORK, compiler.FLAGS
    try:
        compiler.WORK = output
        compiler.FLAGS = [*saved_flags, '-lang', 'c99']
        return compiler.compare(source, 'main', '2', 'on', True,
                                compiler=ROOT / 'tools/mwccarm/mwccarm/2.0/sp1p5/mwccarm.exe')
    finally:
        compiler.WORK, compiler.FLAGS = saved_work, saved_flags


def main():
    for source in sorted((SOURCE / 'first').glob('*.c')):
        rows, unused = compare(source, WORK / 'first-baseline' / source.stem)
        write_json(WORK / 'first-baseline' / (source.stem + '.json'), rows)
        print(json.dumps([dict(name=r.get('name'), target=r.get('bytes'), built=r.get('compiledBytes'),
                              matching=r.get('matchingBytes'), exact=r.get('exactAfterDeclaredRelocation'),
                              failed=r.get('compileFailed')) for r in rows]), flush=True)


if __name__ == '__main__':
    main()
