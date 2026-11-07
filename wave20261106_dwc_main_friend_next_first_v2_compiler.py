from pathlib import Path
import match_runtime as C
from project import ROOT, read_json, sha256


LANE = ROOT / 'evidence/lanes/parallel-wave20261106/dwc-main-friend-next/first-v2'
NATIVE = LANE / 'native-inputs.json'
NATIVE_SHA = 'cff6cecbce6722d755634d15aefc1549fa76113e7b7cbae5b99a7ef619f52c40'
SOURCE = ROOT / 'src/runtime/parallel_wave20261106/dwc-main-friend-next/first-v2'
WORK = ROOT / 'work/w6mfr/first-v2'
COMPILER = ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'


def compare(source, directory, strict=False):
    source, directory = Path(source).resolve(), Path(directory).resolve()
    if not source.is_relative_to(SOURCE) and not source.is_relative_to(WORK):
        raise ValueError('Selected friend source escaped owned first packet')
    if not directory.is_relative_to(WORK) or sha256(NATIVE) != NATIVE_SHA:
        raise ValueError('Selected friend output or native contract differs')
    value = read_json(NATIVE)
    previous = C.FLAGS, C.WORK, C.symbol_address
    def address(name):
        if name in {'strcmp', 'memcmp'}:
            return {'strcmp': 0x201d800, 'memcmp': 0x201b248}[name]
        return previous[2](name)
    try:
        C.FLAGS = [*previous[0], '-ipa', 'file', '-lang', 'c99'] + (['-requireprotos', '-w', 'error'] if strict else [])
        C.WORK, C.symbol_address = directory, address
        rows, other = C.compare(source, 'main', '4,p', 'on,noauto', False, thumb=True, compiler=COMPILER)
        if rows and not rows[0].get('compileFailed'):
            allowed = {row['address'] for row in value['entries']}
            if any(row['address'] not in allowed for row in rows):
                raise ValueError('Compiler emitted a function outside selected source scope')
        return rows, other
    finally:
        C.FLAGS, C.WORK, C.symbol_address = previous
