import hashlib
import json
import struct
from pathlib import Path
from project import ROOT,sha256,write_json
REPORT=ROOT/'evidence/arm7/core126-state76-boundary-20261101.json'


def main():
    start=0x027ea584;end=start+76;code_end=start+72;branches=[];words=[];inputs=[]
    for module,base in [('arm7-main',0x027e0000),('arm7-wram',0x037f8000)]:
        path=ROOT/('extract/arm7/runtime/'+module+'.bin');raw=path.read_bytes();inputs.append(dict(module=module,path=path.relative_to(ROOT).as_posix(),base=hex(base),bytes=len(raw),sha256=sha256(path)))
        for offset in range(0,len(raw)-3,4):
            address=base+offset;word=struct.unpack_from('<I',raw,offset)[0]
            if start<=address<end:continue
            if start<=word<end:words.append(dict(module=module,address=hex(address),word=hex(word),targetKind='entry'if word==start else'code-interior'if word<code_end else'literal-interior',candidateOnly=True))
            if word>>28==15 or(word>>25)&7!=5:continue
            delta=(word&0xffffff)<<2
            if delta&(1<<25):delta-=1<<26
            target=(address+8+delta)&0xffffffff
            if start<=target<end:branches.append(dict(module=module,address=hex(address),word=hex(word),target=hex(target),link=bool(word&(1<<24)),condition=word>>28,targetKind='entry'if target==start else'code-interior'if target<code_end else'literal-interior',rawAlignedCandidateOnly=True))
    native=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes()[start-0x027e0000:end-0x027e0000];inventory=ROOT/'evidence/arm7/ghidra-runtime-inventory.json';rows=[r for r in json.loads(inventory.read_text())['functions']if r['module']=='arm7-main'and int(r['address'],0)==start];result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-main',mode='arm',address=hex(start),bytes=76,codeBytes=72,literalBytes=4,end=hex(end),spanSha256=hashlib.sha256(native).hexdigest(),rawInventory=dict(path=inventory.relative_to(ROOT).as_posix(),sha256=sha256(inventory),matchingRows=rows),inputModules=inputs,outsideAlignedArmBranchCandidates=branches,outsideAlignedLiteralWordCandidates=words,outsideInteriorBranchCandidates=[r for r in branches if r['targetKind']!='entry'],boundedHostAlignedScanOnly=True,thumbOrOpaqueReferenceCompletenessProven=False,sourceAssemblyDataOrDenominatorCredit=0);write_json(REPORT,result);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),outsideEntryBranches=len([r for r in branches if r['targetKind']=='entry']),outsideInteriorBranches=len(result['outsideInteriorBranchCandidates']),outsideWordCandidates=len(words))),flush=True)
if __name__=='__main__':main()
