from pathlib import Path
import match_runtime as C
from project import ROOT,sha256
PROFILE={0x202e260:'sp1p5'}

def compare(source,directory,address):
 source=Path(source).resolve()
 if address not in PROFILE or not any(source.is_relative_to(p)for p in[ROOT/'src/runtime/parallel_wave20261106/g3d-blendvis-next',ROOT/'work/w6bv']):raise ValueError('Unowned G2D source identity/path')
 if sha256(ROOT/'evidence/lanes/parallel-wave20261106/g3d-blendvis-next/claim.json')!='aa8ece5bd03e405dfecc62fd89b7cf3a0361f5eaad422ea7493be928985fe1c2':raise ValueError('G2D admission changed')
 flags,work=C.FLAGS,C.WORK
 try:
  C.FLAGS=[*flags,'-ipa','file','-lang','c99'];C.WORK=Path(directory);return C.compare(source,'main','4,p','on,noauto',False,thumb=False,compiler=ROOT/('tools/mwccarm/mwccarm/2.0/'+PROFILE[address]+'/mwccarm.exe'))
 finally:C.FLAGS,C.WORK=flags,work
