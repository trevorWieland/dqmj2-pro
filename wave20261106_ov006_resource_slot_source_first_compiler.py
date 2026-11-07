from pathlib import Path
import re
import match_runtime as C
from project import ROOT
from wave20261106_ov006_resource_slot_source_first_paths import EVIDENCE,assert_compile
LANE=EVIDENCE
COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
SPEED_ENTRIES={0x21e73ac,0x21e749c,0x21e775c,0x21e7b00}

def compare(source,directory):
    source=Path(source);directory=Path(directory);assert_compile(source,directory);previous_work=C.WORK;previous_flags=C.FLAGS
    name=re.search(r'\bnative_ov006_([0-9a-f]{8})\s*\(',source.read_text())
    if name is None:raise ValueError('Actual admitted source entry absent')
    try:
        C.WORK=directory;C.FLAGS=[*previous_flags,'-lang','c99'];return C.compare(source,'ov006','2','off',int(name[1],16)in SPEED_ENTRIES,compiler=COMPILER)
    finally:C.WORK=previous_work;C.FLAGS=previous_flags
