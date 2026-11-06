import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import match_runtime as C
from project import ROOT,write_json
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings


def main():
    source=ROOT/'src/overlays/ov001_20261102_battle_state951/source.c'
    original=C.FLAGS[:]
    rows=[]
    for name,extra in [('default',[]),('explicit-c99',['-lang','c99'])]:
        C.FLAGS=original+extra
        C.WORK=ROOT/'work/ol955-language'/name/'compile'
        result,unused=C.compare(source,'ov001','2','off',True)
        if len(result)!=1 or result[0].get('compileFailed'):raise ValueError('955 language compile failed')
        proof=validate(result[0],qualified_bindings(result[0]),ROOT/'work/ol955-language'/name/'genuine')
        rows.append(dict(profile=name,source=result[0],genuineLink=proof))
    C.FLAGS=original
    if rows[0]['genuineLink']['originalRelocations']!=rows[1]['genuineLink']['originalRelocations']:
        raise ValueError('955 language relocation difference')
    if rows[0]['genuineLink']['linkedCallerSha256']!=rows[1]['genuineLink']['linkedCallerSha256']:
        raise ValueError('955 language caller-byte difference')
    write_json(ROOT/'evidence/verification/ov001-battle-state955-explicit-c99-20261102.json',dict(schemaVersion=1,sourceCredit=0,language='C99',sameCompleteCallerBytes=True,sameOriginalRelocationTypesAddendsEncodedWords=True,profiles=rows,limits=['Same unchanged source/header with pinned compiler default and explicit-lang c99.','Source acceptance still requires954 native/model/controls and full integrator gates.']))
    print(dict(sameCompleteCallerBytes=True,sameRelocations=True,bytes=628),flush=True)

if __name__=='__main__':main()
