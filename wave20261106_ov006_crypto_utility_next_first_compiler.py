from pathlib import Path
import match_runtime as C
from project import ROOT,sha256,read_json
LANE=ROOT/'evidence/lanes/parallel-wave20261106/ov006-crypto-utility-next'
COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'

def compare(source,directory):
 source=Path(source).resolve()
 if not any(source.is_relative_to(p)for p in [ROOT/'src/ov006/parallel_wave20261106/crypto-utility-next/first',ROOT/'work/w6cu']):raise ValueError('Unowned crypto source path')
 if sha256(LANE/'claim.json')!='5a84576227224d0a3eb40cab967d0fa3907a0063a540ca28ce1a555b19423409':raise ValueError('crypto admission changed')
 from wave20261106_ov006_crypto_utility_next_helpers import qualify
 proof=read_json(LANE/'runtime-helper-abi.json');assert proof['allPassed']
 for pin in [proof['originalMainImage'],proof['originalMainInventory']]:assert sha256(ROOT/pin['path'])==pin['sha256']
 helpermap={'_u32_div_f':0x2026350,'_ll_mul':0x2026124}
 def scoped(name):
  if name not in helpermap:return original(name)
  target=helpermap[name];contract=dict(program='',processor='arm9',module='main',mode='arm',kind='function',address=hex(target));return qualify(name,contract)
 flags,work,original=C.FLAGS,C.WORK,C.symbol_address
 try:
  C.FLAGS=[*flags,'-ipa','file','-lang','c99'];C.WORK=Path(directory);C.symbol_address=scoped
  return C.compare(source,'ov006','4,p','on,noauto',False,thumb=True,compiler=COMPILER)
 finally:C.FLAGS,C.WORK,C.symbol_address=flags,work,original
