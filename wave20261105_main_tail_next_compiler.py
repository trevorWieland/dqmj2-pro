from pathlib import Path
from project import ROOT, sha256
import match_runtime as C

RUNTIME_SHA256 = 'fa61db8211e80a8811323ba5dcea406efd6051ac52fe3f5422ceb00363d42485'
COMPILER = ROOT / 'tools/mwccarm/mwccarm/2.0/sp1p5/mwccarm.exe'


def compare(source, directory):
    source = Path(source).resolve()
    allowed = [ROOT / 'src/runtime/parallel_wave20261105/main-tail-next', ROOT / 'work/w5tn']
    if not any(source.is_relative_to(path) for path in allowed) or sha256(ROOT / 'match_runtime.py') != RUNTIME_SHA256:
        raise ValueError('Scoped summary source/runtime differs')
    work = C.WORK
    try:
        C.WORK = Path(directory)
        rows, bodies = C.compare(source, 'main', '2', 'on', True, compiler=COMPILER)
    finally:
        C.WORK = work
    for row in rows:
        if any(not r['symbol'].startswith(('native_fn_', 'native_data_')) for r in row.get('relocations', [])):
            raise ValueError('This packet qualifies no compiler-helper aliases or anonymous data relocations')
    return rows, bodies
