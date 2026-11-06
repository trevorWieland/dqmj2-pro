from pathlib import Path
import match_runtime as C
from project import ROOT,sha256
LANE=ROOT/'evidence/lanes/parallel-wave20261106/ov006-aes-next'
COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'

def compare(source,directory):
 source=Path(source).resolve()
 if not any(source.is_relative_to(p)for p in [ROOT/'src/ov006/parallel_wave20261106/aes-next',ROOT/'work/w6an']):raise ValueError('Unowned AES source path')
 if sha256(LANE/'claim.json')!='4e9352c205ad0ad872940255d44162992de3c12c20e420a00c3957650fc16fd1':raise ValueError('AES admission changed')
 flags,work=C.FLAGS,C.WORK
 try:
  C.FLAGS=[*flags,'-ipa','file','-lang','c99'];C.WORK=Path(directory)
  return C.compare(source,'ov006','4,p','on,noauto',False,thumb=True,compiler=COMPILER)
 finally:C.FLAGS,C.WORK=flags,work
