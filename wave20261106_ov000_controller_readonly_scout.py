import match_runtime
import bisect
import collections
import hashlib
import json
import re
import subprocess
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from capstone.arm import ARM_OP_IMM,ARM_OP_MEM,ARM_REG_PC,ARM_CC_AL,ARM_CC_INVALID,ARM_INS_BL,ARM_INS_BLX,ARM_INS_B,ARM_INS_BX
from project import ROOT,read_json,write_json,sha256
from wave20261106_nns_primary_readonly_scout import intervals

REV='0da3da2f2eaf3888774e1d2f0cd572c6db3e2cfb'
LANE=ROOT/'evidence/lanes/parallel-wave20261106/ov000-controller-scout'


def blob(path):return subprocess.check_output(['git','show',REV+':'+path],cwd=ROOT)


def cfg(image,base,address,size):
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);decoder.detail=True;pending=[address];seen={};literals=set();edges=[];exits=[];issues=[];memory=[];object_aliases={};blocks={address}
    while pending:
        pc=pending.pop()
        if pc in seen:continue
        if not address<=pc<address+size or pc&3:issues.append(dict(kind='CFG-address-outside-configured-extent',address=hex(pc)));continue
        data=image[pc-base:pc-base+4];decoded=list(decoder.disasm(data,pc,count=1))
        if len(decoded)!=1 or decoded[0].size!=4:issues.append(dict(kind='undecodable-reachable-word',address=hex(pc)));continue
        i=decoded[0];seen[pc]=dict(address=hex(pc),bytes=data.hex(),mnemonic=i.mnemonic,operands=i.op_str);fall=pc+4;conditional=i.cc not in[ARM_CC_AL,ARM_CC_INVALID,ARM_INS_BL,ARM_INS_BLX,ARM_INS_B,ARM_INS_BX];mnemonic=i.mnemonic
        if pc<address+20 and mnemonic in['mov','movs']and len(i.operands)==2 and i.reg_name(i.operands[1].reg)=='r0':object_aliases[i.reg_name(i.operands[0].reg)]='original-r0'
        for operand in i.operands:
            if operand.type==ARM_OP_MEM:
                m=operand.mem;register=i.reg_name(m.base)
                if m.base==ARM_REG_PC and not m.index:literals.add(pc+8+m.disp)
                memory.append(dict(origin=hex(pc),mnemonic=mnemonic,baseRegister=register,indexRegister=i.reg_name(m.index)if m.index else None,displacement=m.disp,width=1 if mnemonic.startswith(('ldrb','ldrsb','strb'))else 2 if mnemonic.startswith(('ldrh','ldrsh','strh'))else 4,heuristicEarlyR0CopyNotPreservationProof=object_aliases.get(register),nativeWord=data.hex()))
        if i.id in[ARM_INS_BL,ARM_INS_BLX]:
            if i.operands and i.operands[0].type==ARM_OP_IMM:edges.append(dict(origin=hex(pc),kind='call',target=hex(i.operands[0].imm)))
            else:issues.append(dict(kind='indirect-call-needs-typed-interface',origin=hex(pc),operands=i.op_str))
            pending.append(fall);continue
        if i.id==ARM_INS_BX:
            if i.op_str=='lr':exits.append(dict(origin=hex(pc),kind='return',conditional=conditional))
            else:issues.append(dict(kind='indirect-branch-needs-entry-proof',origin=hex(pc),operands=i.op_str))
            if conditional:pending.append(fall);blocks.add(fall)
            continue
        if i.id==ARM_INS_B and i.operands and i.operands[0].type==ARM_OP_IMM:
            target=i.operands[0].imm;edges.append(dict(origin=hex(pc),kind='conditional-branch'if conditional else'branch',target=hex(target)));blocks.add(target)
            if address<=target<address+size:pending.append(target)
            else:exits.append(dict(origin=hex(pc),kind='external-tail',target=hex(target)))
            if conditional:pending.append(fall);blocks.add(fall)
            continue
        if('pc'in i.op_str and(mnemonic.startswith(('pop','ldm'))or(mnemonic.startswith('mov')and i.op_str.startswith('pc,')))):
            exits.append(dict(origin=hex(pc),kind='return-or-pc-write',conditional=conditional))
            if conditional:pending.append(fall);blocks.add(fall)
            continue
        if i.op_str.startswith('pc,'):issues.append(dict(kind='computed-PC-needs-table-proof',origin=hex(pc),operands=i.op_str));continue
        pending.append(fall)
    if any(p in seen for p in literals):issues.append(dict(kind='reachable-instruction-also-loaded-as-literal'))
    return dict(reachableWords=len(seen),blockEntryCount=len(blocks),edges=edges,exits=exits,issues=issues,literals=[dict(address=hex(p),insideConfiguredExtent=address<=p<=address+size-4,bytes=image[p-base:p-base+4].hex())for p in sorted(literals)],memory=memory,instructions=[seen[p]for p in sorted(seen)])


def main():
    if LANE.resolve()!=(ROOT/'evidence/lanes/parallel-wave20261106/ov000-controller-scout').resolve():raise ValueError('Exact new read-only ov000 evidence scope differs')
    raw=blob('ledger/functions.jsonl');rows=[json.loads(line)for line in raw.splitlines()];modules=json.loads(blob('manifest.json'))['modules'];metadata=next(m for m in modules if m['name']=='ov000');image=(ROOT/metadata['binary']).read_bytes();base=int(metadata['base'],0);symbols='config/arm9/overlays/ov000/symbols.txt';relocs='config/arm9/overlays/ov000/relocs.txt';pinpaths={metadata['binary'],symbols,relocs};protect=[];paths=sorted(set((ROOT/'evidence/lanes').rglob('claim.json'))|set((ROOT/'evidence/lanes').rglob('data-claim.json'))|set(ROOT.glob('cohort*-*specification.json')))
    for p in paths:
        name=p.relative_to(ROOT).as_posix();pinpaths.add(name);protect.extend((*r,name)for r in intervals(read_json(p))if r[:3]==('','arm9','ov000'))
    gitpins={REV+':ledger/functions.jsonl':hashlib.sha256(raw).hexdigest()}
    for name,key in[('ledger/data.json','records'),('ledger/linkage.json','regions')]:
        content=blob(name);gitpins[REV+':'+name]=hashlib.sha256(content).hexdigest();protect.extend((*r,REV+':'+name)for r in intervals(json.loads(content)[key])if r[:3]==('','arm9','ov000'))
    protect.extend((*r,REV+':ledger/functions.jsonl')for row in rows if row['states']['functionMatched']or row.get('sourceUnit')for r in intervals(row)if r[:3]==('','arm9','ov000'));pins={p:sha256(ROOT/p)for p in pinpaths};records=[]
    for line in(ROOT/relocs).read_text(encoding='utf-8').splitlines():
        m=re.match(r'from:(0x[0-9a-f]+)',line)
        if m:records.append((int(m[1],0),line))
    records.sort();addresses=[r[0]for r in records];inventory=(ROOT/symbols).read_text(encoding='utf-8').splitlines();historical={}
    index='nonmatching/ov000/20261029-broad01/index.json';pinpaths.add(index);pins[index]=sha256(ROOT/index)
    for e in read_json(ROOT/index)['candidates']:historical[(e['address'],e['mode'])]=e
    candidates=[];counts=collections.Counter()
    for row in rows:
        if row['module']!='ov000'or row['states']['functionMatched']or row['mode']!='arm'or not 96<=row['bytes']<=640:continue
        a=int(row['address'],0);n=row['bytes'];conflicts=[dict(start=hex(x),end=hex(y),path=p)for _,_,_,x,y,p in protect if max(a,x)<min(a+n,y)]
        if conflicts:counts['protected-medium']+=1;continue
        counts['unclaimed-medium']+=1;body=image[a-base:a-base+n];out=[r[1]for r in records[bisect.bisect_left(addresses,a):bisect.bisect_left(addresses,a+n)]];analysis=cfg(image,base,a,n);calls=[r for r in analysis['edges']if r['kind']=='call'];issues=analysis['issues']
        if any('module:('in r for r in out):issues.append(dict(kind='plural-overlay-original-relocation'))
        if len(calls)>5 or issues or analysis['blockEntryCount']>14:counts['complex-or-interface-blocked']+=1;continue
        canonical=next((s for s in inventory if re.fullmatch(r'\S+ kind:function\(arm,size=0x%x\) addr:0x%08x'%(n,a),s)),None)
        old=historical.get((row['address'],row['mode']));artifact=[]
        if old:
            directory=ROOT/'nonmatching/ov000/20261029-broad01'/old['directory'];artifact=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in sorted(directory.glob('*'))if p.is_file()and p.suffix in['.c','.json','.s']]
        candidates.append(dict(identity=row,nativeSha256=hashlib.sha256(body).hexdigest(),canonicalInventoryRecord=canonical,originalRelocationRecords=out,cfg=analysis,historicalArtifactPins=artifact,sourceCredit=0,ownershipGranted=False,semanticNamesInferred=False))
    if any(sha256(ROOT/p)!=h for p,h in pins.items()):raise ValueError('Protection/native/index epoch changed during read-only ov000 scan')
    write_json(LANE/'medium-candidates.json',dict(status='read-only-native-triage-no-ownership',sourceRevision=REV,sourceCredit=0,compilerInvoked=False,reconstructionSourceOrClaimWrites=False,nativeModule=metadata['binary'],nativeModuleSha256=sha256(ROOT/metadata['binary']),counts=dict(counts),candidates=candidates,actualInputPins=[dict(path=p,sha256=h)for p,h in sorted(pins.items())],gitPins=[dict(gitObject=p,sha256=h)for p,h in sorted(gitpins.items())],generatorSha256=sha256(__file__),limits='Configured whole spans and mechanical reachable native CFG/literal/memory-width evidence guide scope only. Recorded direct-call namespaces,raw ROM derivation,missing/internal entries,stack/interface and genuine exact source/model proof remain required. No inferred meaning is credited.'))
    print(dict(counts=dict(counts),shortlist=len(candidates)),flush=True)
    for e in candidates[:20]:print(e['identity']['address'],e['identity']['bytes'],len(e['cfg']['edges']),e['cfg']['blockEntryCount'],[c['target']for c in e['cfg']['edges']if c['kind']=='call'])


if __name__=='__main__':main()
