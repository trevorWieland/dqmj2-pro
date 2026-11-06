from pathlib import Path
import match_runtime as C
from project import ROOT,sha256
COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
RUNTIME_SHA='fa61db8211e80a8811323ba5dcea406efd6051ac52fe3f5422ceb00363d42485'


def compare(source,directory):
    source=Path(source).resolve()
    if not any(source.is_relative_to(p) for p in [ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next',ROOT/'work/w5st']):raise ValueError('Source escaped exclusive socket Thumb scope')
    if sha256(ROOT/'match_runtime.py')!=RUNTIME_SHA:raise ValueError('Unchanged original runtime normalizer required')
    old_flags,old_work=C.FLAGS,C.WORK
    try:
        C.FLAGS=[*old_flags,'-ipa','file','-lang','c99'];C.WORK=Path(directory)
        rows,compiled=C.compare(source,'main','4,p','on,noauto',False,thumb=True,compiler=COMPILER)
        if any(not r['symbol'].startswith(('native_fn_','native_data_')) for row in rows for r in row.get('relocations',[])):raise ValueError('No compiler-helper aliases are qualified in this packet')
        return rows,compiled
    finally:C.FLAGS,C.WORK=old_flags,old_work
