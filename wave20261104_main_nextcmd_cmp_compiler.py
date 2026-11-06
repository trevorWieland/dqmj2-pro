from pathlib import Path
from project import ROOT, sha256
import match_runtime as C
from wave20261104_main_tail_compiler import COMPILER, RUNTIME_SHA256, HELPERS as BASE_HELPERS, helper_binding as base_binding
from wave20261104_main_nextcmd_cmp_abi import HELPERS as COMPARISONS, binding as comparison_binding

HELPERS = {**BASE_HELPERS, **{name: item[0] for name, item in COMPARISONS.items()}}


def helper_binding(name):
    return comparison_binding(name) if name in COMPARISONS else base_binding(name)


def compare(source, directory):
    source = Path(source).resolve()
    allowed = [ROOT / 'src/runtime/parallel_wave20261104/main-command-next/sixth', ROOT / 'work/w4nc/sixth']
    if not any(source.is_relative_to(path) for path in allowed) or sha256(ROOT / 'match_runtime.py') != RUNTIME_SHA256:
        raise ValueError('Scoped comparison caller/runtime differs')
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
                    raise ValueError('Original comparison/helper identity or relocation differs')
                relocation['binding'] = 'explicit-original-comparison-helper-identity' if relocation['symbol'] in COMPARISONS else 'explicit-measured-compiler-helper-identity'
    return rows, body
