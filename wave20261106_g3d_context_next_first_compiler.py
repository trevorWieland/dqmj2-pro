from pathlib import Path
import match_runtime as C
from project import ROOT,sha256
PROFILE={0x2031b44:'sp1p5'}

def compare(source,directory,address):
 source=Path(source).resolve()
 if address not in PROFILE or not any(source.is_relative_to(p)for p in[ROOT/'src/runtime/parallel_wave20261106/g3d-context-next',ROOT/'work/w6gn']):raise ValueError('Unowned G2D source identity/path')
 if sha256(ROOT/'evidence/lanes/parallel-wave20261106/g3d-context-next/claim.json')!='217f193dc0f6f57e2bf4c5cf2636ae2f20967c2aa85ee770a08841921d74d986':raise ValueError('G2D admission changed')
 flags,work=C.FLAGS,C.WORK
 try:
  C.FLAGS=[*flags,'-ipa','file','-lang','c99'];C.WORK=Path(directory);return C.compare(source,'main','4,p','on,noauto',False,thumb=False,compiler=ROOT/('tools/mwccarm/mwccarm/2.0/'+PROFILE[address]+'/mwccarm.exe'))
 finally:C.FLAGS,C.WORK=flags,work
