from pathlib import Path
import match_runtime as C
from project import ROOT,read_json,sha256

LANE=ROOT/'evidence/lanes/parallel-wave20261105/dwc-match-tail-next/fourth'
INPUT=LANE/'original-imports.json'
INPUT_SHA='fd61082eb495ca54ef1ef4f150acb342d94ec41184dfb0a53feb834332724950'
COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'


def compare(source,directory):
    source=Path(source).resolve()
    if not any(source.is_relative_to(path) for path in [ROOT/'src/runtime/parallel_wave20261105/dwc-match-tail-next/fourth',ROOT/'work/w6mt/fourth']) or sha256(INPUT)!=INPUT_SHA:
        raise ValueError('Scoped selected Thumb source/import identity changed')
    value=read_json(INPUT)
    if sha256(COMPILER)!=value['compilerSha256'] or value['callerMode']!='thumb':raise ValueError('Pinned Thumb compiler contract changed')
    original_flags,original_work,original_address=C.FLAGS,C.WORK,C.symbol_address
    def address(name):
        if name in ['strlen','strchr','strncmp','strncpy']:
            binding=value['mapping'][name];expected={'strlen':'0x201d69c','strchr':'0x201d948','strncmp':'0x201d914','strncpy':'0x201d780'}[name]
            if binding!={'program':'','processor':'arm9','module':'main','kind':'function','mode':'arm','address':expected}:raise ValueError('Scoped standard-header function identity changed')
            return int(expected,0)
        if name=='_s32_div_f':
            binding=value['mapping'][name]
            if binding!={'program':'','processor':'arm9','module':'main','kind':'function','mode':'arm','address':'0x2026144'}:raise ValueError('Scoped signed32 division-helper identity changed')
            return int(binding['address'],0)
        return original_address(name)
    try:
        C.symbol_address=address
        C.FLAGS=[*original_flags,'-ipa','file','-lang','c99'];C.WORK=Path(directory)
        return C.compare(source,'main','4,p','on,noauto',False,thumb=True,compiler=COMPILER)
    finally:C.FLAGS,C.WORK,C.symbol_address=original_flags,original_work,original_address
