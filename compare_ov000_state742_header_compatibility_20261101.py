import json
import match_runtime as c
from project import ROOT,sha256,write_json
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
def execute():
    old=ROOT/'src/overlays/ov000_20261101_motion738';header=ROOT/'src/overlays/ov000_20261101_state742/context.h';results=[]
    for name in['source.c','clamp.c']:
        source=old/name;directory=ROOT/'nonmatching/overlay-lane/20261101-state742-header-compatibility'/name.replace('.c','');directory.mkdir(parents=True,exist_ok=True);copy=directory/'source.c';copy.write_bytes(source.read_bytes());copy.with_name('context.h').write_bytes(header.read_bytes())
        if sha256(source)!=sha256(copy):raise ValueError('742 header experiment changed frozen C body')
        c.WORK=ROOT/'work/ol742-header-compatibility'/name/'compile';rows,u=c.compare(copy,'ov000','2','off',True)
        if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError('742 header experiment failed compiler')
        proof=validate(rows[0],qualified_bindings(rows[0]),c.WORK.parent/'link');results.append(dict(originalSource=dict(path=source.relative_to(ROOT).as_posix(),sha256=sha256(source)),newCopiedSource=rows[0],sameBodySourceBytes=True,genuineLink=proof,sourceCredit=0))
    report=dict(schemaVersion=1,sourceCredit=0,functionCredit=0,byteCredit=0,purpose='Optional header-layout transport research,not new accepted dependencies/source',newHeader=dict(path=header.relative_to(ROOT).as_posix(),sha256=sha256(header)),bothExistingBodiesStillExact=True,existingBodyBytes=632,experiments=results,limits=['Frozen738 source/header remain unchanged. Body copies are byte-identical and only their context header differs.','Field28/40 names replace part of the old opaque prefix with unchanged0x58 used extent; no new storage or reconstructed bytes.','Integrator owns any later shared-context/preference migration. These copied units must never gain duplicate source/function credit.'])
    write_json(ROOT/'evidence/attempts/ov000-state742-header-compatibility-20261101.json',report);print(dict(existingBodies=2,exactBytes=632,newCredit=0),flush=True)
if __name__=='__main__':execute()
