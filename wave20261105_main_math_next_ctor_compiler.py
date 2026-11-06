from pathlib import Path
from project import ROOT,sha256
import match_runtime as C

COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/sp1p5/mwccarm.exe'
RUNTIME_SHA='fa61db8211e80a8811323ba5dcea406efd6051ac52fe3f5422ceb00363d42485'

def compare(source,directory):
    source=Path(source).resolve()
    if not any(source.is_relative_to(p) for p in [ROOT/'src/runtime/parallel_wave20261105/main-math-next/ctor',ROOT/'work/w5mn/ctor']) or sha256(ROOT/'match_runtime.py')!=RUNTIME_SHA:raise ValueError('Explicit native-call source/runtime scope differs')
    flags,work=C.FLAGS,C.WORK
    try:
        C.FLAGS=[*flags,'-ipa','file','-lang','c99'];C.WORK=Path(directory)
        return C.compare(source,'main','4,p','on,noauto',False,compiler=COMPILER)
    finally:C.FLAGS,C.WORK=flags,work
