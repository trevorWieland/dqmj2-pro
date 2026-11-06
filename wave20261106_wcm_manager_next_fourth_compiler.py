from pathlib import Path
import match_runtime as C
from project import ROOT,read_json,sha256
LANE=ROOT/'evidence/lanes/parallel-wave20261105/wcm-manager-next/fourth'
INPUT=LANE/'original-imports.json'
INPUT_SHA='30f0a6c254468e434dc2b06893d0b088b7631a2e0332fa20c19a0f2425c1b3f2'
COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'

def compare(source,directory):
 source=Path(source).resolve()
 if not any(source.is_relative_to(p)for p in [ROOT/'src/runtime/parallel_wave20261105/wcm-manager-next/fourth',ROOT/'work/w6wc/fourth'])or sha256(INPUT)!=INPUT_SHA:raise ValueError('Scoped selected WCM source/import changed')
 imports=read_json(INPUT)
 if sha256(COMPILER)!=imports['compilerSha256']:raise ValueError('Pinned compiler changed')
 flags,work,fn=C.FLAGS,C.WORK,C.symbol_address
 def address(name):
  if name=='_s32_div_f':
   binding=imports['mapping'][name]
   if binding!={'program':'','processor':'arm9','module':'main','kind':'function','mode':'arm','address':'0x2026144'}:raise ValueError('Original division ABI entry differs')
   return 0x2026144
  if name=='_u32_div_f':
   if imports['mapping'][name]!={'program':'','processor':'arm9','module':'main','kind':'function','mode':'arm','address':'0x2026350'}:raise ValueError('Scoped original unsigned division entry differs')
   return 0x2026350
  return fn(name)
 try:
  C.FLAGS=[*flags,'-ipa','file','-lang','c99'];C.WORK=Path(directory);C.symbol_address=address
  return C.compare(source,'main','4,p','on,noauto',False,thumb=True,compiler=COMPILER)
 finally:C.FLAGS,C.WORK,C.symbol_address=flags,work,fn
