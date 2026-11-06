from pathlib import Path
import re
from project import ROOT, sha256
import match_runtime as C

COMPILER = ROOT / 'tools/mwccarm/mwccarm/2.0/sp1p5/mwccarm.exe'
RUNTIME_SHA = 'fa61db8211e80a8811323ba5dcea406efd6051ac52fe3f5422ceb00363d42485'
NAMES = {'02060adc', '02060c1c', '02060c60', '02060cb4', '02067754'}


def compare(source, directory):
    source = Path(source).resolve()
    if not any(source.is_relative_to(p) for p in [ROOT / 'src/runtime/parallel_wave20261105/main-runtime-next/tenth', ROOT / 'work/w5rn']):
        raise ValueError('Collection source is outside its private scope')
    if sha256(ROOT / 'match_runtime.py') != RUNTIME_SHA:
        raise ValueError('Pinned native compiler support changed')
    names = re.findall(r'\bnative_main_([0-9a-f]{8})\s*\(', source.read_text())
    if len(names) != 1 or names[0] not in NAMES:
        raise ValueError('Only five explicitly owned integer/allocation callers are supported')
    flags, work = C.FLAGS, C.WORK
    try:
        C.WORK = Path(directory)
        if names[0] == '02067754':
            C.FLAGS = [*flags, '-ipa', 'file', '-lang', 'c99']
            return C.compare(source, 'main', '4,p', 'on,noauto', False, compiler=COMPILER)
        return C.compare(source, 'main', '2', 'on', True, compiler=COMPILER)
    finally:
        C.FLAGS, C.WORK = flags, work
