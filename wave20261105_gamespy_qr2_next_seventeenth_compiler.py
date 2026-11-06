from pathlib import Path
import match_runtime as C
from project import ROOT,read_json,sha256

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-qr2-next/seventeenth'
INPUT=LANE/'original-imports.json'
INPUT_SHA='c1a7c87155cf106d61dc51d53df2f8ade740c64a484a251522ac98ae7c4c8687'
COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'


def compare(source,directory):
    source=Path(source).resolve()
    if not any(source.is_relative_to(path) for path in [ROOT/'src/runtime/parallel_wave20261105/gamespy-qr2-next/seventeenth',ROOT/'work/w5qr/seventeenth']) or sha256(INPUT)!=INPUT_SHA:
        raise ValueError('Scoped selected Thumb source/import identity changed')
    value=read_json(INPUT)
    if sha256(COMPILER)!=value['compilerSha256'] or value['callerMode']!='thumb':raise ValueError('Pinned Thumb compiler contract changed')
    original_flags,original_work=C.FLAGS,C.WORK
    try:
        C.FLAGS=[*original_flags,'-ipa','file','-lang','c99'];C.WORK=Path(directory)
        return C.compare(source,'main','4,p','on,noauto',False,thumb=True,compiler=COMPILER)
    finally:C.FLAGS,C.WORK=original_flags,original_work
