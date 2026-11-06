from pathlib import Path
from project import ROOT, sha256
import match_runtime as C
from link_runtime_unit import verify_binding

RUNTIME_SHA256 = 'fa61db8211e80a8811323ba5dcea406efd6051ac52fe3f5422ceb00363d42485'
HELPERS = {'_ffix': 0x020259B4, '_fflt': 0x02025A28, '_ffixu': 0x020259E8,
           '_ffltu': 0x02025A70, '_fgr': 0x0202537C, '_fmul': 0x02025AB8,
           '_fadd': 0x02024E0C, '_fsub': 0x02025CA4, '_fdiv': 0x02025578}
COMPILER = ROOT / 'tools/mwccarm/mwccarm/2.0/sp1p5/mwccarm.exe'


def helper_binding(name):
    if name not in HELPERS:
        raise ValueError('Unsupported measured compiler helper: ' + name)
    binding = dict(program='', processor='arm9', module='main', mode='arm', kind='function', address=hex(HELPERS[name]))
    verify_binding(name, binding)
    return binding


def compare(source, directory):
    source = Path(source).resolve()
    allowed = [ROOT / 'src/runtime/parallel_wave20261104/main-arm-next', ROOT / 'work/w4an']
    if not any(source.is_relative_to(path) for path in allowed) or sha256(ROOT / 'match_runtime.py') != RUNTIME_SHA256:
        raise ValueError('Scoped caller source/runtime implementation differs')
    original = C.symbol_address

    def address(name):
        return int(helper_binding(name)['address'], 0) if name in HELPERS else original(name)

    C.WORK = Path(directory)
    try:
        C.symbol_address = address
        rows, body = C.compare(source, 'main', '2', 'off', True, compiler=COMPILER)
    finally:
        C.symbol_address = original
    for row in rows:
        for relocation in row.get('relocations', []):
            if relocation['symbol'] in HELPERS:
                expected = helper_binding(relocation['symbol'])
                if relocation['target'] != expected['address'] or relocation['type'] not in (1, 28, 29):
                    raise ValueError('Compiler helper relocation/namespace differs')
                relocation['binding'] = 'explicit-measured-compiler-helper-identity'
    return rows, body
