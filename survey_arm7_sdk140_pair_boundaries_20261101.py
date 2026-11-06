import json
import struct
from pathlib import Path
import arm7_runtime
import audit_arm7_bulk_20261030 as inventory
from project import ROOT,sha256,write_json

REPORT=ROOT/'evidence/arm7/sdk140-pair-boundaries-20261101.json'
RANGES={0x027e9b98:(64,60),0x027e9bd8:(128,116)}

def measure():
    known={(s['module'],i.address)for s in inventory.specs()if not s['program']for i in s['instructions']};layout=arm7_runtime.derive((ROOT/'extract/arm7/arm7.bin').read_bytes());results=[]
    for entry,(size,code)in RANGES.items():
        references=[];literals=[];modules=[]
        for module in layout['modules']:
            data=(ROOT/module['binary']).read_bytes();base=int(module['runtimeBase'],0);modules.append(dict(module=module['id'],binary=module['binary'],base=hex(base),bytes=len(data),sha256=sha256(ROOT/module['binary'])))
            for offset in range(0,len(data)-3,4):
                site=base+offset;word=struct.unpack_from('<I',data,offset)[0]
                if word&0x0e000000==0x0a000000:
                    displacement=word&0xffffff
                    if displacement&0x800000:displacement-=0x1000000
                    target=(site+8+displacement*4)&0xffffffff
                    if entry<=target<entry+size and not entry<=site<entry+size:references.append(dict(module=module['id'],site=hex(site),target=hex(target),kind='call'if word&0x01000000 else'branch',knownCanonicalArmInstruction=(module['id'],site)in known,targetEntry=target==entry,targetPool=target>=entry+code,word=hex(word)))
                if entry<=word<entry+size and not entry<=site<entry+size:literals.append(dict(module=module['id'],site=hex(site),value=hex(word),kind='uninterpreted-aligned-word-reference',entry=word==entry))
        if any(r['knownCanonicalArmInstruction']and not r['targetEntry']for r in references):raise ValueError('Known outside branch enters interior/pool; reconcile before complete-function credit')
        results.append(dict(address=hex(entry),mode='arm',module='arm7-main',program='',processor='arm7',bytes=size,codeBytes=code,literalBytes=size-code,references=references,literalReferences=literals,modules=modules,knownOutsideInteriorBranchCount=0,wholeProgramIndirectOrThumbReferenceCompletenessProven=False,sharedTailOrAlternateEntryAdopted=False,sourceCredit=0,denominatorDelta=0))
    return dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',functions=results,limits=['Bounded aligned ARM branch and word-reference scan of measured host ARM7 module bytes; data false positives retained','Indirect/computed branches and Thumb callers are not exhaustively resolved','The two complete canonical spans are adjacent and nonoverlapping; this adds no function boundary or initialized bytes'],sourceCredit=0)

def main():
    result=measure();write_json(REPORT,result);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),entryRefs=[len(r['references'])for r in result['functions']],sourceCredit=0)),flush=True)
if __name__=='__main__':main()
