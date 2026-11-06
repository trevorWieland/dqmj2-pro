import re
from pathlib import Path
from project import ROOT,sha256
import wave20261106_socl_continuation_next_compiler as original

C=original.C
COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/sp1p6/mwccarm.exe'
COMPILER_SHA='2819dea7ae847ff83699d18bbc567238abe2804b6783b3bcc5893c5e546b0334'
RUNTIME_SHA='fa61db8211e80a8811323ba5dcea406efd6051ac52fe3f5422ceb00363d42485'
NAMES={'02091518','0209158c','020917f8','02091864'}
EXPECTED_FLAGS=['-O4,p','-enum','int','-char','signed','-str','noreuse','-proc','arm946e','-gccext,on','-fp','soft','-inline','on,noauto','-Cpp_exceptions','off','-RTTI','off','-interworking','-w','off','-sym','on','-gccinc','-nolink','-msgstyle','gcc','-ipa','file','-lang','c99','-thumb']


def helper_address(symbol,caller,fallback):
    if symbol=='_s32_div_f':
        if caller!='0209158c':raise ValueError('Signed divide helper is qualified only for the original client-v2 caller')
        return 0x02026144
    return fallback(symbol)


def compare(source,directory):
    source=Path(source).resolve();directory=Path(directory).resolve();names=re.findall(r'\bnative_main_([0-9a-f]{8})\s*\(',source.read_text())
    if len(names)!=1 or names[0] not in NAMES:raise ValueError('Exact owned sixth caller required')
    if not (source.is_relative_to(ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/sixth') or source.is_relative_to(ROOT/'work/w6sc')) or not directory.is_relative_to(ROOT/'work/w6sc'):raise ValueError('Exclusive sixth source/work scope differs')
    if sha256(COMPILER)!=COMPILER_SHA or sha256(ROOT/'match_runtime.py')!=RUNTIME_SHA:raise ValueError('Pinned real frontend/support changed')
    flags,work,resolver=C.FLAGS,C.WORK,C.symbol_address
    try:
        C.FLAGS=[*flags,'-ipa','file','-lang','c99'];C.WORK=directory;C.symbol_address=lambda symbol:helper_address(symbol,names[0],resolver)
        rows,compiled=C.compare(source,'main','4,p','on,noauto',False,thumb=True,compiler=COMPILER)
        for row in rows:
            if not row.get('compileFailed') and row['compilerFlags']!=EXPECTED_FLAGS:raise ValueError('Exact measured C99/Thumb helper profile differs')
            for relocation in row.get('relocations',[]):
                if not relocation['symbol'].startswith(('native_fn_','native_data_')) and (names[0]!='0209158c' or relocation['symbol']!='_s32_div_f' or relocation['target']!='0x2026144' or relocation['type']!=10 or relocation['addend']!=-4):raise ValueError('Unqualified actual compiler helper symbol/target/ABI')
        return rows,compiled
    finally:C.FLAGS,C.WORK,C.symbol_address=flags,work,resolver
