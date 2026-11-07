from pathlib import Path
import re
import match_runtime as C
from project import ROOT
from wave20261106_overlay_strict_reuse_source_paths import EVIDENCE,assert_compile
LANE=EVIDENCE
COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'


def compare(source,directory):
    source=Path(source);directory=Path(directory);assert_compile(source,directory);match=re.search(r'native_(ov003|ov006)_(021dea38|021dd434)',source.read_text())
    if match is None or(match[1],match[2])not in[('ov003','021dea38'),('ov006','021dd434')]:raise ValueError('Source is not one of exactly two admitted reuse identities')
    previous_work=C.WORK;previous_flags=C.FLAGS
    try:
        C.WORK=directory;C.FLAGS=[*previous_flags,'-lang','c99'];return C.compare(source,match[1],'2','off',match[1]=='ov006',compiler=COMPILER)
    finally:C.WORK=previous_work;C.FLAGS=previous_flags
