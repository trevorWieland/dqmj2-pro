import concurrent.futures
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import match_runtime as C
from project import ROOT, write_json, read_json
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings

SOURCE = ROOT / 'nonmatching/overlay-lane/20261102-geometry876/021dbc18/whole-q12/source.c'
DEFAULT = 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
PROFILES = [(compiler, '2', True) for compiler in C.COMPILER_PINS if compiler != DEFAULT] + [(DEFAULT, '1', True), (DEFAULT, '3', True), (DEFAULT, '2', False)]


def worker(index):
    compiler, opt, speed = PROFILES[index]
    directory = ROOT / 'work/ol879-profiles' / str(index)
    C.WORK = directory / 'compile'
    rows, unused = C.compare(SOURCE, 'ov000', opt, 'off', speed, compiler=compiler)
    source = rows[0]
    result = dict(index=index, compiler=compiler, optimization=opt, speed=speed, source=source, sourceCredit=0)
    if not source.get('compileFailed'):
        try:
            result['genuineLink'] = validate(source, qualified_bindings(source), directory / 'canonical')
        except ValueError as error:
            if not error.args or not isinstance(error.args[0], dict):
                raise
            result['genuineLink'] = error.args[0]
    path = ROOT / 'evidence/attempts' / f'ov000-geometry879-profile-{index}-20261102.json'
    write_json(path, result)
    return result


def run(index):
    result = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--worker', str(index)], cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise ValueError((index, result.returncode, result.stdout, result.stderr))
    return read_json(ROOT / 'evidence/attempts' / f'ov000-geometry879-profile-{index}-20261102.json')


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--worker':
        worker(int(sys.argv[2]))
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            results = list(pool.map(run, range(len(PROFILES))))
        write_json(ROOT / 'evidence/attempts/ov000-geometry879-profiles-20261102.json', dict(sourceCredit=0, rows=results, limits=['Bounded six-profile codegen experiments only; zero game/native/exact credit. Other-compiler behavior does not inherit876/877 qualification.']))
        print([(row['index'], row.get('genuineLink', {}).get('linkedBytes'), row.get('genuineLink', {}).get('matchingBytes')) for row in results])
