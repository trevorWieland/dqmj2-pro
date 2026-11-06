from pathlib import Path
import match_lowlevel as C
from match_runtime import COMPILER_PINS
from project import ROOT,sha256
from wave20261106_itcm_reset_next_paths import assert_compile

COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/sp1p6/mwccarm.exe'


def compare(source,directory,compiler=COMPILER):
    source=Path(source).resolve();directory=Path(directory).resolve();assert_compile(source,directory)
    compiler=Path(compiler).resolve();key=compiler.relative_to(ROOT).as_posix()
    if COMPILER_PINS.get(key)!=sha256(compiler):raise ValueError('ITCM reset pinned compiler differs')
    old_work=C.WORK;old_flags=C.FLAGS;old_compiler=C.COMPILER
    try:
        C.WORK=directory;C.FLAGS=[*old_flags,'-ipa','file','-lang','c99'];C.COMPILER=compiler
        rows,compiled=C.compare(source,'itcm','4,p','on,noauto',False)
        for row in rows:
            row.update(compilerPath=key,compilerSha256=sha256(compiler))
        return rows,compiled
    finally:C.WORK=old_work;C.FLAGS=old_flags;C.COMPILER=old_compiler
