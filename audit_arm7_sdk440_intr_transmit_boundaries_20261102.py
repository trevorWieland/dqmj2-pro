import hashlib
import json
from pathlib import Path
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from capstone.arm_const import ARM_INS_B,ARM_INS_BL,ARM_INS_BLX
import audit_arm7_bulk_20261030 as audit
from project import ROOT,sha256,write_json
PROFILE=ROOT/'nonmatching/arm7-bulk/20261102/lane-sdk433-intr-transmit-compiler-final/profile.json'

def number(v):return int(v,0)if isinstance(v,str)else v

def main():
    profile=json.loads(PROFILE.read_text(encoding='utf-8'));specs=audit.specs();seeds=profile['units'];accepted=json.loads((ROOT/seeds[0]['authoritativeExclusionSnapshot']['path']).read_text(encoding='utf-8'))['functions'];decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);decoder.detail=True;images={s['binary']:(ROOT/s['binary']).read_bytes()for s in seeds};rows=[]
    for seed in seeds:
        start=number(seed['address']);end=start+seed['bytes'];sp=next(r for r in specs if r['module']==seed['module']and r.get('program','')==seed['program']and r['address']==start);image=images[seed['binary']];offset=start-seed['base'];overlaps=[];interior_entries=[];external=[];pools=[]
        if sha256(ROOT/seed['binary'])!=seed['inputModuleSha256']or hashlib.sha256(image[offset:offset+seed['bytes']]).hexdigest()!=seed['targetSha256']or sp['bytes']!=seed['bytes']:raise ValueError('Complete current canonical input extent differs')
        for prior in accepted:
            if(prior['processor'],prior.get('program',''),prior['module'],prior['mode'])!=('arm7',seed['program'],seed['module'],'arm'):continue
            a=number(prior['address']);n=prior.get('bytes',0)
            if(start<a+n and a<end)or not n and start<=a<end:overlaps.append(prior)
        for other in specs:
            if other.get('program','')!=seed['program']or other['mode']!='arm':continue
            if other['module']==seed['module']and start<other['address']<end:interior_entries.append(hex(other['address']))
            for ins in other['instructions']:
                if ins.id not in(ARM_INS_B,ARM_INS_BL,ARM_INS_BLX)or not ins.op_str.startswith('#'):continue
                target=int(ins.op_str[1:],0)&~1
                if start<=target<end and not(start<=ins.address<end and other['module']==seed['module']):external.append(dict(fromModule=other['module'],fromParent=hex(other['address']),site=hex(ins.address),to=hex(target),mnemonic=ins.mnemonic,entry=target==start,interior=target!=start))
        for address,value in sorted(sp['pools'].items()):
            if start<=address<end:pools.append(dict(address=hex(address),bytes=4,value=hex(value)))
        if overlaps or interior_entries or any(r['interior']for r in external):raise ValueError(dict(name=seed['name'],overlaps=overlaps,interiorEntries=interior_entries,externalInterior=[r for r in external if r['interior']]))
        rows.append(dict(processor='arm7',program=seed['program'],module=seed['module'],mode='arm',address=seed['address'],bytes=seed['bytes'],codeBytes=seed['codeBytes'],literalPoolBytes=4*len(pools),targetSha256=seed['targetSha256'],inputModuleSha256=seed['inputModuleSha256'],canonicalBoundaryEvidence=sp['boundaryEvidence'],literalPools=pools,externalDirectCodeReferences=external,acceptedOverlaps=[],interiorCanonicalStarts=[],externalInteriorReferences=[],additionalExecutableBytes=0,denominatorIncrease=0,behavioralReturnCredit=0))
    result=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),profile=PROFILE.relative_to(ROOT).as_posix(),profileSha256=sha256(PROFILE),rows=rows,functions=len(rows),initializedBytes=sum(r['bytes']for r in rows),sourceCredit=0,behavioralReturnCredit=0,scope='Configured ARM instruction ranges in the same processor/program, separate module identities; indirect/discontiguous/unknown-code references not globally excluded',defaultNamespaceAndInventoriesChanged=False);write_json(ROOT/'evidence/attempts/arm7-sdk440-intr-transmit-boundaries-20261102.json',result);print(json.dumps(dict(functions=len(rows),bytes=result['initializedBytes'],externalReferences=sum(len(r['externalDirectCodeReferences'])for r in rows),behavioralReturns=0)),flush=True)

if __name__=='__main__':main()
