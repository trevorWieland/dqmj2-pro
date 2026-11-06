from pathlib import Path
import match_runtime as C
from project import ROOT,read_json,sha256
LANE=ROOT/'evidence/lanes/parallel-wave20261105/wcm-manager-next/first'
INPUT=LANE/'original-imports.json'
INPUT_SHA='65dbbfa0cf66731c31f7049cf9a3cb5a4232c4808c5961c95597ff77dede10cf'
COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'

def compare(source,directory):
 source=Path(source).resolve()
 if not any(source.is_relative_to(p)for p in [ROOT/'src/runtime/parallel_wave20261105/wcm-manager-next/first',ROOT/'work/w6wc/first'])or sha256(INPUT)!=INPUT_SHA:raise ValueError('Scoped selected WCM source/import changed')
 imports=read_json(INPUT)
 if sha256(COMPILER)!=imports['compilerSha256']:raise ValueError('Pinned compiler changed')
 flags,work,fn=C.FLAGS,C.WORK,C.symbol_address
 def address(name):
  if name=='_s32_div_f':
   binding=imports['mapping'][name]
   if binding!={'program':'','processor':'arm9','module':'main','kind':'function','mode':'arm','address':'0x2026144'}:raise ValueError('Original division ABI entry differs')
   return 0x2026144
  return fn(name)
 try:
  C.FLAGS=[*flags,'-ipa','file','-lang','c99'];C.WORK=Path(directory);C.symbol_address=address
  return C.compare(source,'main','4,p','on,noauto',False,thumb=True,compiler=COMPILER)
 finally:C.FLAGS,C.WORK,C.symbol_address=flags,work,fn
