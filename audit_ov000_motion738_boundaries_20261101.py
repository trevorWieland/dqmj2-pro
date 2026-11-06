import json
import sys
from project import ROOT,write_json,sha256,configuration
import match_runtime as c
sys.path.insert(0,str(ROOT/'deps/native'))
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM,CS_MODE_THUMB,CS_GRP_CALL,CS_GRP_JUMP
from capstone.arm import ARM_OP_IMM
from link_runtime_unit import measured_module
BASE=0x021D7240
UNITS=[(0x022199B8,492),(0x02219CE4,140)]
def number(value):return int(value,0)if isinstance(value,str)else value

def execute():
    path=ROOT/'evidence/verification/ov000-motion738-boundary-inventory-20261101.json';inventory=json.loads(path.read_text());metadata,image,unused=measured_module('ov000')
    incoming,internal,unsupported=[],[],[];seen=set();interior_starts=[];examined=0
    for row in inventory['entries']:
        start,size=number(row['address']),row['bytes'];mode=row.get('mode')or'arm'
        if any(a<start<a+n for a,n in UNITS):interior_starts.append(row)
        if not size or mode not in['arm','thumb']or start<BASE or start+size>BASE+len(image):
            unsupported.append(row);continue
        decoder=Cs(CS_ARCH_ARM,CS_MODE_THUMB if mode=='thumb'else CS_MODE_ARM);decoder.detail=True;decoder.skipdata=True;examined+=1
        for instruction in decoder.disasm(image[start-BASE:start-BASE+size],start):
            if not instruction.id or not any(group in instruction.groups for group in[CS_GRP_CALL,CS_GRP_JUMP])or not instruction.operands or instruction.operands[0].type!=ARM_OP_IMM:continue
            target=instruction.operands[0].imm&0xFFFFFFFF
            unit=next(((a,n)for a,n in UNITS if a<=target<a+n),None)
            if not unit:continue
            key=(mode,instruction.address,target)
            if key in seen:continue
            seen.add(key);item=dict(sourceCandidateStart=hex(start),sourceMode=mode,sourcePc=hex(instruction.address),mnemonic=instruction.mnemonic,target=hex(target),targetUnit=hex(unit[0]),entry=target==unit[0])
            if unit[0]<=instruction.address<unit[0]+unit[1]:internal.append(item)
            else:incoming.append(item)
    raw=[]
    for offset in range(0,len(image)-3,4):
        value=int.from_bytes(image[offset:offset+4],'little')
        if any(a<=value<a+n for a,n in UNITS):raw.append(dict(storageAddress=hex(BASE+offset),rawWord=hex(value),atEntry=any(value==a for a,n in UNITS),classification='Unclassified aligned raw-word lead,not proof of pointer/reachability'))
    pools=[]
    for address,size in UNITS:
        code=size-12 if address==0x22199b8 else size
        for offset in range(code,size,4):
            literal=address+offset;readers=[]
            for pos in range(0,code,4):
                word=int.from_bytes(image[address-BASE+pos:address-BASE+pos+4],'little');pc=address+pos
                if word>>28==14 and word&0x0F7F0000==0x051F0000 and pc+8+((word&4095)if word&0x00800000 else-(word&4095))==literal:readers.append(hex(pc))
            if not readers:raise ValueError('738 unreferenced purported literal')
            pools.append(dict(address=hex(literal),bytes=4,value=hex(int.from_bytes(image[literal-BASE:literal-BASE+4],'little')),nativePcRelativeReaders=readers))
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov000',moduleSha256=metadata['sha256'],sourceCredit=0,inventory=dict(path=path.relative_to(ROOT).as_posix(),sha256=sha256(path)),candidateSpansExamined=examined,unsupportedCandidateEntries=unsupported,heuristicInteriorCandidateStarts=interior_starts,sameModuleDirectIncomingBranches=incoming,internalBranches=internal,externalDirectInteriorTargets=[r for r in incoming if not r['entry']],alignedRawWordLeads=raw,literalEvidence=pools,limits=['Bounded same-module ARM/Thumb disassembly of frozen heuristic inventory; data may decode as branch leads. Every positive branch needs source/code classification before reachability claims.','Register-indirect calls, possible unclassified regions, other modules/processor namespaces and loaded-overlay resolution are outside this scan. No global absence/reachability claim.','Raw aligned address words remain unclassified leads. Native prologue/epilogues, all own code, model branches and genuine C byte equality are separate evidence.'])
    write_json(ROOT/'evidence/verification/ov000-motion738-boundary-audit-20261101.json',report);print(dict(examined=examined,incoming=len(incoming),externalDirectInterior=len(report['externalDirectInteriorTargets']),interiorStarts=len(interior_starts),rawLeads=len(raw),unsupported=len(unsupported)),flush=True)
if __name__=='__main__':execute()
