from pathlib import Path
from project import ROOT, sha256
import match_runtime as C
from link_runtime_unit import verify_binding

from wave20261104_main_tail_compiler import RUNTIME_SHA256, HELPERS, COMPILER, helper_binding


def compare(source, directory):
    source = Path(source).resolve()
    allowed = [ROOT / 'src/runtime/parallel_wave20261104/main-command-third', ROOT / 'work/w4mc3']
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
