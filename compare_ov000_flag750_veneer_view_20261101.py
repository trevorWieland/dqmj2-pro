import json
import match_runtime as c
from project import ROOT,sha256,write_json
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
def execute():
    original=ROOT/'src/transplants/ov000-reuse01/native_ov000_022198e0.c';directory=ROOT/'nonmatching/overlay-lane/20261101-flag750-veneer-view';directory.mkdir(parents=True,exist_ok=True);source=directory/'source.c'
    text='#include "context.h"\nu32 native_ov000_022198e0(void) {\n    return native_fn_ov000_022198ec();\n}\n'
    if source.exists()and source.read_text()!=text:raise ValueError('750 frozen veneer alternative differs')
    source.write_text(text);source.with_name('context.h').write_bytes((ROOT/'src/overlays/ov000_20261101_flag750/context.h').read_bytes())
    c.WORK=ROOT/'work/ol750-veneer-view/compile';rows,u=c.compare(source,'ov000','2','off',True)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError('750 veneer alternative compile failed')
    proof=validate(rows[0],qualified_bindings(rows[0]),c.WORK.parent/'link')
    write_json(ROOT/'evidence/attempts/ov000-flag750-zero-input-veneer-view-20261101.json',dict(schemaVersion=1,sourceCredit=0,functionCredit=0,byteCredit=0,originalSelectedSource=dict(path=original.relative_to(ROOT).as_posix(),sha256=sha256(original)),unmodifiedOriginal=True,rawU32ReturnFacadePreserved=True,logicalRequiredWords=0,alternative=rows[0],realLink=proof,limits=['Optional interface/preference research only: no accepted source or registry change.','Old generic12B transplant forwards4 words; original target80B and its only12B leaf consume none of the entry words. Dynamic160-pair helper proof records poisonedR0..R3.','Zero required physical words does not determine original unused formal count. Current4-word source is retained until integrator review.','This12B genuine match adds0 decomplication/function/source credit and is not a positive dependency of the80B packet.']))
    print(dict(existingVeneerBytes=12,genuineExact=True,newCredit=0),flush=True)
if __name__=='__main__':execute()
