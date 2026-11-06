from pathlib import Path
import match_runtime as C
from project import ROOT,read_json,sha256

INPUT=ROOT/'evidence/lanes/parallel-wave20261104/main-arm-later/sdk/original-imports.json'
INPUT_SHA='9e6d84a25a72573a0a5a9291ad847fe55143e938dc0931357676f89a3e042144'
COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
RUNTIME_SHA='fa61db8211e80a8811323ba5dcea406efd6051ac52fe3f5422ceb00363d42485'


def compare(source,directory):
    source=Path(source).resolve()
    if not any(source.is_relative_to(p) for p in [ROOT/'src/runtime/parallel_wave20261104/main-arm-later/sdk',ROOT/'work/w5ml/sdk']) or sha256(ROOT/'match_runtime.py')!=RUNTIME_SHA or sha256(INPUT)!=INPUT_SHA:raise ValueError('Scoped SDK source/compiler import contract changed')
    mapping=read_json(INPUT)['mapping'];original_address=C.symbol_address;original_flags=C.FLAGS;original_work=C.WORK
    def address(name):
        if name in ('_ll_udiv','_u32_div_f'):return int(mapping[name]['address'],0)
        return original_address(name)
    try:
        C.symbol_address=address;C.FLAGS=[*original_flags,'-ipa','file','-lang','c99'];C.WORK=Path(directory)
        return C.compare(source,'main','4,p','on,noauto',False,compiler=COMPILER)
    finally:C.symbol_address=original_address;C.FLAGS=original_flags;C.WORK=original_work
