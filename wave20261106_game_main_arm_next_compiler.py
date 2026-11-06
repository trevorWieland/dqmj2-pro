import re
from pathlib import Path
from project import ROOT,sha256
import match_runtime as C
SOURCE=ROOT/'src/runtime/parallel_wave20261105/game-main-arm-next'
WORK=ROOT/'work/w6gm'
NAMES=set('02070fd8 0207147c 0207154c 020715a8 02071748 02071b28 02071bc0 02071d78 020720a4 0207211c 020721b4 020724f4 02072568 020725e8 020726d8 020727d0 020728ec 02072b74 02072c6c 02072de8 02072e7c 02072ea0 02072f70 02073090 0207313c 02073574 020735f8 020743f8 0207483c 020748d0 02074974 02074a54'.split())

COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/sp1p5/mwccarm.exe'
RUNTIME_SHA='fa61db8211e80a8811323ba5dcea406efd6051ac52fe3f5422ceb00363d42485'


def compare(source,directory,optimization='2',inline='on',speed=True):
    source=Path(source).resolve();directory=Path(directory).resolve()
    if not source.is_relative_to(SOURCE) and not source.is_relative_to(WORK):raise ValueError('Source outside exclusive game source/work scope')
    if not directory.is_relative_to(WORK):raise ValueError('Compiler outputs outside private game work scope')
    if sha256(ROOT/'match_runtime.py')!=RUNTIME_SHA:raise ValueError('Pinned native compiler support changed')
    names=re.findall(r'\bnative_main_([0-9a-f]{8})\s*\(',source.read_text())
    if len(names)!=1 or names[0] not in NAMES:raise ValueError('Exactly one exclusively owned caller is required')
    flags,work=C.FLAGS,C.WORK
    try:
        C.WORK=directory;C.FLAGS=[*flags,'-lang','c99']
        return C.compare(source,'main',optimization,inline,speed,compiler=COMPILER)
    finally:C.FLAGS,C.WORK=flags,work
