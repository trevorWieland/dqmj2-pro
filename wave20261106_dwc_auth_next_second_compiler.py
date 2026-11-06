from wave20261106_dwc_auth_next_second_paths import assert_owned,assert_compile,EVIDENCE,SOURCE as OWN_SOURCE,WORK as OWN_WORK
from pathlib import Path
import match_runtime as C
from project import ROOT,read_json,sha256

LANE=ROOT/'evidence/lanes/parallel-wave20261105/dwc-auth-next/second'
INPUT=LANE/'original-imports.json'
INPUT_SHA='d9764f919b7bb053ad033652070c3b6c59b5a14d15c3c8214b0375b8ac5dbc88'
COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'


def compare(source,directory):
    assert_owned(LANE)
    assert_compile(Path(source),Path(directory))
    source=Path(source).resolve()
    if not any(source.is_relative_to(p) for p in [ROOT/'src/runtime/parallel_wave20261105/dwc-auth-next/second',ROOT/'work/w6da/second']) or sha256(INPUT)!=INPUT_SHA:raise ValueError('Scoped Thumb source/import identity changed')
    value=read_json(INPUT)
    if sha256(COMPILER)!=value['compilerSha256'] or value['callerMode']!='thumb':raise ValueError('Pinned Thumb compiler contract changed')
    original_address=C.symbol_address;original_flags=C.FLAGS;original_work=C.WORK
    def address(name):
        if name in value['mapping']:return int(value['mapping'][name]['address'],0)
        return original_address(name)
    try:
        C.symbol_address=address;C.FLAGS=[*original_flags,'-ipa','file','-lang','c99'];C.WORK=Path(directory)
        return C.compare(source,'main','4,p','on,noauto',False,thumb=True,compiler=COMPILER)
    finally:C.symbol_address=original_address;C.FLAGS=original_flags;C.WORK=original_work
