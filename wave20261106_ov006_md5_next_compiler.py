from pathlib import Path
import match_runtime as C
from project import ROOT,sha256
LANE=ROOT/'evidence/lanes/parallel-wave20261106/ov006-md5-next'
COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'

def compare(source,directory):
 source=Path(source).resolve()
 if not any(source.is_relative_to(p)for p in [ROOT/'src/ov006/parallel_wave20261106/md5-next',ROOT/'work/w6mn']):raise ValueError('Unowned MD5 source path')
 if sha256(LANE/'claim.json')!='55173c8bb43f29eb12b477c698adcbff389e1405a08d3e899e7ae5d745ddc901':raise ValueError('MD5 admission changed')
 flags,work=C.FLAGS,C.WORK
 try:
  C.FLAGS=[*flags,'-ipa','file','-lang','c99'];C.WORK=Path(directory)
  return C.compare(source,'ov006','4,p','on,noauto',False,thumb=True,compiler=COMPILER)
 finally:C.FLAGS,C.WORK=flags,work
