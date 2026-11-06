from pathlib import Path
import re
import match_runtime as C
from project import ROOT,sha256

COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
SOURCE=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next'
WORK=ROOT/'work/w6sc'
NAMES=set('0209075c 02090794 020907f4 0209088c 020909c8 02090a3c 02090ae8 02090bdc 02090c18 02090c60 02090cac 02090d1c 0209108c 020911b0 0209128c 020912d4 02091490 02091518 0209158c 0209161c 02091690 020917f8 02091864 02091a68 02091afc 02091c5c 02091de0 02091fbc 02092174 02092284 02092380 02092470 02092584 02092778 02092854 020928f8 02092938 02092a84 02092b50 02092bf0 02092cb8 0209302c 020930ac 020930f4 02093180 020936f4 02093774 020937dc 02093824 020938b8 02093930 02093998 02093a18 02093a6c 02093ac0 02093b2c 02093b7c 02093c64'.split())


def compare(source,directory,optimization='4,p'):
    source=Path(source).resolve();directory=Path(directory).resolve()
    if not any(source.is_relative_to(p) for p in [SOURCE,WORK]) or not directory.is_relative_to(WORK):raise ValueError('Source/compiler outputs escaped exclusive continuation scope')
    names=re.findall(r'\bnative_main_([0-9a-f]{8})\s*\(',source.read_text())
    if len(names)!=1 or names[0] not in NAMES:raise ValueError('Exactly one admitted continuation routine required')
    if sha256(ROOT/'match_runtime.py')!='fa61db8211e80a8811323ba5dcea406efd6051ac52fe3f5422ceb00363d42485':raise ValueError('Pinned original normalizer changed')
    flags,work=C.FLAGS,C.WORK
    try:
        C.FLAGS=[*flags,'-ipa','file','-lang','c99'];C.WORK=directory
        rows,compiled=C.compare(source,'main',optimization,'on,noauto',False,thumb=True,compiler=COMPILER)
        if any(not r['symbol'].startswith(('native_fn_','native_data_')) for row in rows for r in row.get('relocations',[])):raise ValueError('Compiler-helper aliases are not qualified')
        return rows,compiled
    finally:C.FLAGS,C.WORK=flags,work
