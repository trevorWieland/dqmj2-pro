from pathlib import Path
import match_runtime as C
from project import ROOT,read_json,sha256

INPUT=ROOT/'evidence/lanes/parallel-wave20261105/main-math-next/original-imports.json'
INPUT_SHA='dc381ce9828a1aa5ea79c27c6fae9d820138ac44698d904a32abb43db734c444'
COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/sp1p5/mwccarm.exe'
RUNTIME_SHA='fa61db8211e80a8811323ba5dcea406efd6051ac52fe3f5422ceb00363d42485'


def compare(source,directory):
    source=Path(source).resolve()
    if not any(source.is_relative_to(p) for p in [ROOT/'src/runtime/parallel_wave20261105/main-math-next',ROOT/'work/w5mn']) or sha256(ROOT/'match_runtime.py')!=RUNTIME_SHA or sha256(INPUT)!=INPUT_SHA:raise ValueError('Scoped SDK source/compiler import contract changed')
    mapping=read_json(INPUT)['mapping'];original_address=C.symbol_address;original_flags=C.FLAGS;original_work=C.WORK
    def address(name):
        if name in ('_dfltu', '_dmul', '_dadd', '_deq', '_dflt', '_ddiv', '_dsub'):return int(mapping[name]['address'],0)
        return original_address(name)
    try:
        C.symbol_address=address;C.FLAGS=[*original_flags,'-ipa','file','-lang','c99'];C.WORK=Path(directory)
        return C.compare(source,'main','4,p','on,noauto',False,compiler=COMPILER)
    finally:C.symbol_address=original_address;C.FLAGS=original_flags;C.WORK=original_work
