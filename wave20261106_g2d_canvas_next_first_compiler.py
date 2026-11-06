from pathlib import Path
import match_runtime as C
from project import ROOT,sha256
PROFILE={0x2087fa8:'base',0x20881e8:'sp1p5'}

def compare(source,directory,address):
 source=Path(source).resolve()
 if address not in PROFILE or not any(source.is_relative_to(p)for p in[ROOT/'src/runtime/parallel_wave20261106/g2d-canvas-next/first',ROOT/'work/w6gc']):raise ValueError('Unowned G2D source identity/path')
 if sha256(ROOT/'evidence/lanes/parallel-wave20261106/g2d-canvas-next/claim.json')!='6339f2c2266e003df731d5fcfdfca7f871d6e4f962c24e627ec6f230d89749e8':raise ValueError('G2D admission changed')
 flags,work=C.FLAGS,C.WORK
 try:
  C.FLAGS=[*flags,'-ipa','file','-lang','c99'];C.WORK=Path(directory);return C.compare(source,'main','4,p','on,noauto',False,thumb=False,compiler=ROOT/('tools/mwccarm/mwccarm/2.0/'+PROFILE[address]+'/mwccarm.exe'))
 finally:C.FLAGS,C.WORK=flags,work
