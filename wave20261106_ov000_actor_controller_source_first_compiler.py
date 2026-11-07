from pathlib import Path
import match_runtime as C
from project import ROOT
from wave20261106_ov000_actor_controller_source_first_paths import assert_compile,EVIDENCE
LANE=EVIDENCE
COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
def compare(source,directory):
    assert_compile(Path(source),Path(directory))
    previous_work=C.WORK;previous_flags=C.FLAGS
    try:
        C.WORK=Path(directory);C.FLAGS=[*previous_flags,'-lang','c99']
        return C.compare(Path(source),'ov000','2','off',True,compiler=COMPILER)
    finally:C.WORK=previous_work;C.FLAGS=previous_flags
