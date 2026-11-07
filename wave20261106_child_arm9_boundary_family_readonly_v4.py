import collections
import hashlib
import json
import struct
import subprocess
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM,CS_MODE_THUMB
from capstone.arm import ARM_OP_IMM,ARM_OP_MEM,ARM_REG_PC,ARM_REG_SP,ARM_REG_LR,ARM_REG_R0,ARM_REG_R1,ARM_REG_R2,ARM_REG_R3,ARM_REG_R12,ARM_CC_AL,ARM_CC_INVALID,ARM_INS_BL,ARM_INS_BLX,ARM_INS_B,ARM_INS_BX
from project import ROOT,configuration,read_json,write_json,sha256,native_dependencies
from wave20261106_nns_primary_readonly_scout import intervals

REVISION='0da3da2f2eaf3888774e1d2f0cd572c6db3e2cfb'
PROGRAM='dwc/utility.bin/move/child.srl'
LANE=ROOT/'evidence/lanes/parallel-wave20261106/child-arm9-independent-boundary-scout-v4'


def derive(image,base,address,limit,mode,known_entries):
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM if mode=='arm'else CS_MODE_THUMB);decoder.detail=True;pending=[(address,0,frozenset([ARM_REG_LR]),frozenset(),())];seen={};code={};pool=set();calls=[];exits=[];issues=[]
    while pending:
        pc,stack,register_tokens,stack_tokens,alias_items=pending.pop();state=(stack,register_tokens,stack_tokens,alias_items)
        if pc in seen:
            previous=seen[pc]
            if previous[0]!=stack:issues.append(dict(kind='SP-join-unresolved',origin=hex(pc),incoming=[previous[0],stack]));continue
            old_alias_map=dict(previous[3]);new_alias_map=dict(alias_items);keys=set(old_alias_map)|set(new_alias_map);joined_aliases=tuple(sorted((r,old_alias_map[r]if r in old_alias_map and r in new_alias_map and old_alias_map[r]==new_alias_map[r]else None)for r in keys))
            register_tokens=previous[1]&register_tokens;stack_tokens=previous[2]&stack_tokens;alias_items=joined_aliases;state=(stack,register_tokens,stack_tokens,alias_items)
            if previous==state:continue
        if not address<=pc<limit:issues.append(dict(kind='fallthrough-outside-next-entry-bound',origin=hex(pc)));continue
        ins=list(decoder.disasm(image[pc-base:pc-base+4],pc,count=1))
        if not ins or pc+ins[0].size>limit:issues.append(dict(kind='undecodable-or-cross-entry',origin=hex(pc)));continue
        i=ins[0];seen[pc]=state;code[pc]=dict(address=hex(pc),bytes=bytes(i.bytes).hex(),mnemonic=i.mnemonic,operands=i.op_str,size=i.size,stackDeltaBefore=stack,entryLRRegistersBefore=[i.reg_name(r)for r in sorted(register_tokens)],entryLRStackSlotsBefore=sorted(stack_tokens));conditional=i.cc not in[ARM_CC_AL,ARM_CC_INVALID];fall=pc+i.size;delta=0;stack_known=False;old_tokens=set(register_tokens);tokens=set(register_tokens);slots=set(stack_tokens);aliases=dict(alias_items);old_aliases=dict(aliases)
        if i.mnemonic.startswith('push'):delta=-4*len(i.operands);stack_known=True
        elif i.mnemonic.startswith('pop'):delta=4*len(i.operands);stack_known=True
        elif len(i.operands)>=2 and i.operands[0].type!=ARM_OP_IMM and i.operands[0].reg==ARM_REG_SP and i.mnemonic.startswith(('add','sub'))and i.operands[-1].type==ARM_OP_IMM:
            if len(i.operands)==2 or i.operands[1].reg==ARM_REG_SP:delta=i.operands[-1].imm*(-1 if i.mnemonic.startswith('sub')else 1);stack_known=True
        if delta and conditional:
            cleanup=[];cleanup_stack=stack;cleanup_end=fall;valid=False
            if i.mnemonic.startswith('pop')and any(op.reg==ARM_REG_PC for op in i.operands):cleanup=[i]
            elif mode=='arm'and i.mnemonic.startswith('add')and not i.update_flags and delta>0:
                cleanup_stack=stack+delta;cursor=fall
                for unused in range(3):
                    decoded=list(decoder.disasm(image[cursor-base:cursor-base+4],cursor,count=1))
                    if not decoded or cursor+decoded[0].size>limit:break
                    candidate=decoded[0]
                    if candidate.cc!=i.cc or candidate.update_flags:break
                    if candidate.mnemonic.startswith('pop')and any(op.reg==ARM_REG_PC for op in candidate.operands):cleanup.append(candidate);break
                    if candidate.mnemonic.startswith('mov')and len(candidate.operands)==2 and candidate.operands[0].reg==ARM_REG_R0 and candidate.operands[1].type==ARM_OP_IMM:cleanup.append(candidate);cursor+=candidate.size;continue
                    break
            if cleanup and cleanup[-1].mnemonic.startswith('pop'):
                returning=cleanup[-1];pc_index=next(index for index,op in enumerate(returning.operands)if op.reg==ARM_REG_PC);original_lr_slot=cleanup_stack+4*pc_index;restored=cleanup_stack+4*len(returning.operands)
                if restored==0 and original_lr_slot in stack_tokens:
                    for candidate in cleanup:
                        if candidate.address!=pc:code[candidate.address]=dict(address=hex(candidate.address),bytes=bytes(candidate.bytes).hex(),mnemonic=candidate.mnemonic,operands=candidate.op_str,size=candidate.size,stackDeltaBefore=cleanup_stack,entryLRRegistersBefore=[candidate.reg_name(r)for r in sorted(register_tokens)],entryLRStackSlotsBefore=sorted(stack_tokens),correlatedCleanupCondition=i.cc)
                    cleanup_end=returning.address+returning.size;exits.append(dict(origin=hex(returning.address),kind='same-unchanged-condition-entry-LR-cleanup-return',originalEntryLRProven=True,entryLRExactStackSlot=original_lr_slot,stackDelta=restored,condition=i.cc,noInterveningFlagWrites=True,cleanupWords=[bytes(x.bytes).hex()for x in cleanup],conditionalSkipLeavesOriginalSPAndTokens=True));valid=True
            if valid:pending.append((cleanup_end,stack,register_tokens,stack_tokens,alias_items));continue
            issues.append(dict(kind='conditional-SP-correlation-deferred',origin=hex(pc)));continue
        if ARM_REG_SP in i.regs_access()[1]and not stack_known:issues.append(dict(kind='unmodeled-SP-write',origin=hex(pc)));continue
        after=stack+delta
        for r in i.regs_access()[1]:tokens.discard(r);aliases.pop(r,None)
        if i.mnemonic.startswith('push'):
            for index,operand in enumerate(i.operands):
                at=after+4*index;slots.discard(at)
                if operand.reg in old_tokens:slots.add(at)
        elif i.mnemonic.startswith('pop'):
            for index,operand in enumerate(i.operands):
                if stack+4*index in slots:tokens.add(operand.reg)
        elif i.mnemonic.startswith('mov')and len(i.operands)==2 and i.operands[1].type!=ARM_OP_IMM:
            dest,source=i.operands[0].reg,i.operands[1].reg
            if source in old_tokens and not conditional:tokens.add(dest)
            if source==ARM_REG_SP:aliases[dest]=stack if not conditional or old_aliases.get(dest)==stack else None
            elif source in old_aliases:aliases[dest]=old_aliases[source]if not conditional or old_aliases.get(dest)==old_aliases[source]else None
        elif i.mnemonic.startswith(('add','sub'))and len(i.operands)>=2:
            dest=i.operands[0].reg;source=i.operands[1].reg
            if dest!=ARM_REG_SP and(source==ARM_REG_SP or source in old_aliases):
                if i.operands[-1].type!=ARM_OP_IMM or conditional or(source in old_aliases and old_aliases[source]is None):aliases[dest]=None;issues.append(dict(kind='dynamic-or-conditional-stack-alias-deferred',origin=hex(pc)))
                else:aliases[dest]=(stack if source==ARM_REG_SP else old_aliases[source])+i.operands[-1].imm*(-1 if i.mnemonic.startswith('sub')else 1)
        for operand in i.operands:
            if operand.type!=ARM_OP_MEM:continue
            mem=operand.mem
            if mem.base==ARM_REG_PC:
                if mem.index or not i.mnemonic.startswith('ldr'):issues.append(dict(kind='computed-or-writing-PC-memory',origin=hex(pc)));continue
                literal=((pc+4)&~3 if mode=='thumb'else pc+8)+mem.disp
                if not address<=literal<=limit-4:issues.append(dict(kind='external-or-cross-entry-literal',origin=hex(pc),literal=hex(literal)))
                else:pool.add(literal)
            if mem.base==ARM_REG_SP or mem.base in old_aliases:
                if mem.index or i.writeback:issues.append(dict(kind='dynamic-or-writeback-stack-slot-deferred',origin=hex(pc)));continue
                if mem.base!=ARM_REG_SP and old_aliases[mem.base]is None:issues.append(dict(kind='unknown-joined-stack-alias-slot-deferred',origin=hex(pc)));continue
                at=(stack if mem.base==ARM_REG_SP else old_aliases[mem.base])+mem.disp
                if i.mnemonic.startswith('str'):
                    width=1 if i.mnemonic.startswith('strb')else 2 if i.mnemonic.startswith('strh')else 4
                    slots={x for x in slots if not max(x,at)<min(x+4,at+width)}
                    if width==4 and i.operands[0].reg in old_tokens and not conditional:slots.add(at)
                elif i.mnemonic.startswith('ldr')and not i.mnemonic.startswith(('ldrb','ldrh','ldrs')):
                    if at in slots and not conditional:tokens.add(i.operands[0].reg)
                elif i.mnemonic.startswith(('ldm','stm')):issues.append(dict(kind='stack-multiple-transfer-deferred',origin=hex(pc)))
        def advance(target):pending.append((target,after,frozenset(tokens),frozenset(slots),tuple(sorted(aliases.items()))))
        if i.id in[ARM_INS_BL,ARM_INS_BLX]:
            for r in[ARM_REG_R0,ARM_REG_R1,ARM_REG_R2,ARM_REG_R3,ARM_REG_R12,ARM_REG_LR]:tokens.discard(r);aliases.pop(r,None)
            slots={x for x in slots if x>=after}
            if i.operands and i.operands[0].type==ARM_OP_IMM:calls.append(dict(origin=hex(pc),target=hex(i.operands[0].imm&~1),targetMode=('thumb'if mode=='arm'else'arm')if i.id==ARM_INS_BLX else mode,nativeWord=bytes(i.bytes).hex(),stackDelta=after,entryLRLiveRegistersAfter=[i.reg_name(r)for r in sorted(tokens)],entryLRStackSlotsAfter=sorted(slots)))
            else:issues.append(dict(kind='indirect-callee-contract-deferred',origin=hex(pc)))
            advance(fall);continue
        if i.id==ARM_INS_BX:
            register=i.operands[0].reg
            if register in old_tokens and after==0:exits.append(dict(origin=hex(pc),kind='entry-LR-token-register-return',returnRegister=i.reg_name(register),originalEntryLRProven=True,stackDelta=after))
            else:issues.append(dict(kind='BX-without-proven-entry-LR-and-balanced-SP',origin=hex(pc),register=i.reg_name(register),stackDelta=after))
            if conditional:advance(fall)
            continue
        if i.id==ARM_INS_B and i.operands and i.operands[0].type==ARM_OP_IMM:
            target=i.operands[0].imm&~1
            if address<=target<limit:advance(target)
            elif(target,mode)in known_entries and after==0:exits.append(dict(origin=hex(pc),kind='same-mode-known-entry-tail',target=hex(target),stackDelta=after))
            else:issues.append(dict(kind='external-tail-not-balanced-known-mode-entry',origin=hex(pc),target=hex(target),stackDelta=after))
            if conditional:advance(fall)
            continue
        if('pc'in i.op_str and(i.mnemonic.startswith(('pop','ldm'))or(i.mnemonic.startswith('mov')and i.op_str.startswith('pc,')))):
            if ARM_REG_PC in tokens and after==0:exits.append(dict(origin=hex(pc),kind='entry-LR-token-PC-return',originalEntryLRProven=True,stackDelta=after))
            else:issues.append(dict(kind='PC-return-without-proven-entry-LR-and-balanced-SP',origin=hex(pc),stackDelta=after))
            if conditional:advance(fall)
            continue
        if i.op_str.startswith('pc,'):issues.append(dict(kind='computed-PC-boundary-deferred',origin=hex(pc)));continue
        advance(fall)
    covered=set();end=address
    for pc,row in code.items():covered.update(range(pc,pc+row['size']));end=max(end,pc+row['size'])
    code_bytes=len(covered)
    for literal in pool:
        if any(x in covered for x in range(literal,literal+4)):issues.append(dict(kind='literal-instruction-overlap',literal=hex(literal)))
        covered.update(range(literal,literal+4));end=max(end,literal+4)
    holes=[];first=None
    for pc in range(address,end+1):
        if pc<end and pc not in covered:
            if first is None:first=pc
        elif first is not None:holes.append(dict(start=hex(first),end=hex(pc),bytes=image[first-base:pc-base].hex(),classification='unclassified-padding-or-unreachable-code-ambiguity'));first=None
    if holes:issues.append(dict(kind='unclassified-gap-padding-deferred',gaps=holes))
    if not exits:issues.append(dict(kind='no-qualified-return-or-tail'))
    calls=list({(x['origin'],x['target'],x['targetMode']):x for x in calls}.values());exits=list({json.dumps(x,sort_keys=True):x for x in exits}.values())
    return dict(address=hex(address),mode=mode,derivedEnd=hex(end),bytes=end-address,bodySha256=hashlib.sha256(image[address-base:end-base]).hexdigest(),derivationUsedAcceptedSourceSize=False,codeBytes=code_bytes,literalBytes=4*len(pool),instructions=[code[k]for k in sorted(code)],literals=[dict(address=hex(p),bytes=image[p-base:p-base+4].hex())for p in sorted(pool)],calls=calls,exits=exits,issues=issues,gaps=holes,allExtentBytesClassified=not holes,complete=not issues)


def qualify_return_tokens():
    base=0x1000;known={(0x1100,'thumb'),(0x1100,'arm')};fixtures=[('thumb-pop-r3-bx-r3','00b508bc1847','thumb',True),('thumb-preserved-through-call','00b500f07df808bc1847','thumb',True),('wrong-pop-slot','10b508bc1847','thumb',False),('overwritten-return-register','00b508bc00231847','thumb',False),('unbalanced-SP','00b57047','thumb',False),('BL-clobbered-live-LR','00f07ef87047','thumb',False),('overwritten-return-stack-slot','00b5009008bc1847','thumb',False),('arbitrary-BX-register','1847','thumb',False),('dynamic-SP-indexed-slot','10402de902008de71080bde8','arm',False),('dynamic-SP-alias-indexed-slot','00b56946885008bc1847','thumb',False),('overwritten-slot-through-SP-alias','00b56946086008bc1847','thumb',False),('BLX-clobbered-live-LR','3e0000fa1eff2fe1','arm',False),('ARM-BL-clobbered-LR','3e0000eb1eff2fe1','arm',False),('ARM-preserved-LR-through-call','10402de93d0000eb1080bde8','arm',True),('conditional-call-common-saved-LR','00b5002801d000f07bf808bc1847','thumb',True),('one-path-overwritten-LR-slot','00b5002800d0009108bc1847','thumb',False),('unknown-joined-SP-alias-slot','00b56946002800d001a9086008bc1847','thumb',False),('same-condition-stack-cleanup','10402de904d04de2000050e304d08d021080bd0804d08de21080bde8','arm',True),('same-condition-cleanup-with-return-value','10402de904d04de2000050e304d08d020000a0031080bd0804d08de21080bde8','arm',True),('conditional-PC-pop','10402de9000050e31080bd081080bde8','arm',True),('wrong-cleanup-condition','10402de904d04de2000050e304d08d021080bd1804d08de21080bde8','arm',False),('flag-write-between-cleanup-steps','10402de904d04de2000050e304d08d02000050e31080bd0804d08de21080bde8','arm',False),('wrong-cleanup-SP-amount','10402de904d04de2000050e308d08d021080bd0804d08de21080bde8','arm',False),('overwritten-cleanup-return-slot','10402de904d04de208108de5000050e304d08d021080bd0804d08de21080bde8','arm',False)]
    result=[]
    for name,hexbytes,mode,expected in fixtures:
        data=bytes.fromhex(hexbytes);r=derive(data,base,base,base+len(data),mode,known)
        if r['complete']!=expected:raise ValueError(('Actual return-token control differs',name,r))
        result.append(dict(case=name,nativeBytes=hexbytes,mode=mode,expectedComplete=expected,actualComplete=r['complete'],exits=r['exits'],issues=r['issues'],reconstructionOrExecutionCredit=0))
    return dict(passed=True,positiveCases=sum(e['expectedComplete']for e in result),negativeCases=sum(not e['expectedComplete']for e in result),records=result,originalInputsUnchanged=True)


def main():
    if LANE.resolve()!=(ROOT/'evidence/lanes/parallel-wave20261106/child-arm9-independent-boundary-scout-v4').resolve():raise ValueError('Exact new boundary evidence root differs')
    controls=qualify_return_tokens()
    pins={};gitpins={};counts=collections.Counter()
    def pin(path):
        name=path.relative_to(ROOT).as_posix()if hasattr(path,'relative_to')else path;digest=sha256(ROOT/name)
        if name in pins and pins[name]!=digest:raise ValueError('Boundary/protection input changed')
        pins[name]=digest;return digest
    def git(path):
        raw=subprocess.check_output(['git','show',REVISION+':'+path],cwd=ROOT);gitpins[REVISION+':'+path]=hashlib.sha256(raw).hexdigest();return raw
    native_dependencies(configuration());import utility_runtime
    from ndspy.rom import NintendoDSRom
    rompath=configuration()['rom'];pin(rompath);romraw=(ROOT/rompath).read_bytes()
    if hashlib.sha256(romraw).hexdigest()!=configuration()['romSha256']:raise ValueError('Original measured ROM differs')
    game=NintendoDSRom(romraw);payload=game.files[game.filenames.idOf('dwc/utility.bin')];pin('extract/files/dwc/utility.bin')
    if payload!=(ROOT/'extract/files/dwc/utility.bin').read_bytes():raise ValueError('Original utility payload differs from raw ROM')
    layout,files=utility_runtime.derive();modules={m['id']:m for m in layout['modules']if m['processor']=='arm9'}
    for m in modules.values():
        pin(m['binary'])
        if files[ROOT/m['binary']]!=(ROOT/m['binary']).read_bytes():raise ValueError('Original decoder-derived runtime image differs')
    for path in['project.json','utility_runtime.py','audit_regions.py','evidence/utility/ghidra-arm9.json','evidence/utility/runtime-functions.json','evidence/utility/entry-seeds.json','evidence/utility/loader-entrypoints.json','initialized_storage_protection_v3_20261106.py']:pin(path)
    for path in layout['decoderFiles']:pin(path)
    ghidra=read_json(ROOT/'evidence/utility/ghidra-arm9.json');starts=collections.defaultdict(set);modes=collections.defaultdict(set);seeds=collections.defaultdict(list)
    for f in ghidra['functions']:a=int(f['address'],0);starts[f['module']].add(a);modes[f['module']].add((a,f['mode']))
    for path,key in[('evidence/utility/entry-seeds.json','entrySeeds'),('evidence/utility/loader-entrypoints.json','entryPointAssociations')]:
        for e in read_json(ROOT/path)[key]:
            if e.get('processor')!='arm9'or e['module']not in modules:continue
            a=int(e['address'],0)&~1;starts[e['module']].add(a);modes[e['module']].add((a,e['mode']));seeds[e['module'],a].append(dict(path=path,record=e))
    analyses=[]
    for f in ghidra['functions']:
        if f['module']not in modules:continue
        a=int(f['address'],0);m=modules[f['module']];base=int(m['base'],0);image=files[ROOT/m['binary']];limit=min((x for x in starts[f['module']]if x>a),default=base+len(image))
        if len(f['ranges'])!=1 or int(f['ranges'][0][0],0)!=a:analyses.append(dict(module=f['module'],address=hex(a),mode=f['mode'],complete=False,issues=[dict(kind='prior-discontiguous-or-nonentry-body-deferred')],calls=[]));continue
        result=derive(image,base,a,limit,f['mode'],modes[f['module']]);result.update(program=PROGRAM,processor='arm9',module=f['module'],entryEvidence=seeds.get((f['module'],a),[]),priorGhidraRanges=f['ranges'],priorGhidraBoundaryVerified=f.get('boundaryVerified',False),nextKnownEntryBound=hex(limit))
        if int(f['ranges'][0][1],0)>int(result['derivedEnd'],0):result['issues'].append(dict(kind='prior-ghidra-body-extends-beyond-recovered-flow-deferred'));result['complete']=False
        analyses.append(result)
    functions=[json.loads(line)for line in git('ledger/functions.jsonl').splitlines()];byid={(r.get('program')or'',r['processor'],r['module'],int(r['address'],0)):r for r in functions};protect=collections.defaultdict(list)
    for name,key in[('ledger/data.json','records'),('ledger/linkage.json','regions')]:
        for p,c,m,a,b in intervals(json.loads(git(name))[key]):
            if(p,c)==(PROGRAM,'arm9'):protect[m].append((a,b,name))
    for r in functions:
        if r['states']['functionMatched']or r.get('sourceUnit'):
            for p,c,m,a,b in intervals(r):
                if(p,c)==(PROGRAM,'arm9'):protect[m].append((a,b,'accepted171'))
    paths=set((ROOT/'evidence/lanes').rglob('claim.json'))|set((ROOT/'evidence/lanes').rglob('data-claim.json'))|set(ROOT.glob('cohort*-*specification.json'))
    for path in sorted(paths):
        name=path.relative_to(ROOT).as_posix();pin(path)
        for p,c,m,a,b in intervals(read_json(path)):
            if(p,c)==(PROGRAM,'arm9'):protect[m].append((a,b,name))
    incoming=collections.defaultdict(list)
    for source in analyses:
        ledger=byid.get((PROGRAM,'arm9',source['module'],int(source['address'],0)));accepted=bool(ledger and ledger['states']['functionMatched'])
        for call in source['calls']:
            target=int(call['target'],0)
            for name,known in modes.items():
                if(target,call['targetMode'])in known:incoming[name,target].append(dict(callerProgram=PROGRAM,callerProcessor='arm9',callerModule=source['module'],callerEntry=source['address'],callerAccepted171=accepted,callerBoundaryProposedComplete=source['complete'],**call))
    eligible=[];reserved=[];deferred=[]
    for e in analyses:
        a=int(e['address'],0);r=byid.get((PROGRAM,'arm9',e['module'],a))
        if not r or r['states']['functionMatched']:continue
        counts['unaccepted-recorded-entries']+=1;e['originalLedgerBytes']=r.get('bytes');e['originalIncomingCalls']=incoming.get((e['module'],a),[])
        if not e['complete']:
            for issue in e['issues']:counts['deferred:'+issue['kind']]+=1
            deferred.append(e);continue
        proofs=[x for x in e['originalIncomingCalls']if x['callerAccepted171']and x['targetMode']==e['mode']]
        e['acceptedIncomingModeProofs']=proofs;e['physicalProtectionConflicts']=sorted({p for x,y,p in protect[e['module']]if max(a,x)<min(int(e['derivedEnd'],0),y)})
        if not proofs and not e['entryEvidence']:e['complete']=False;e['issues'].append(dict(kind='no-accepted-incoming-call-or-measured-seed-mode-proof'));deferred.append(e);counts['deferred:no-qualified-entry-mode-proof']+=1;continue
        (reserved if e['physicalProtectionConflicts']else eligible).append(e)
    again=set((ROOT/'evidence/lanes').rglob('claim.json'))|set((ROOT/'evidence/lanes').rglob('data-claim.json'))|set(ROOT.glob('cohort*-*specification.json'));changed=[p for p,h in pins.items()if not(ROOT/p).is_file()or sha256(ROOT/p)!=h];stable=again==paths and not changed
    result=dict(status='passed-read-only-independent-child-boundary-census'if stable else'failed-changing-protection-input-epoch',sourceRevision=REVISION,sourceCredit=0,compilerInvoked=False,sourceOrClaimWrites=False,acceptedSourceOriginsConsulted=False,originFunctionSizesConsulted=False,rawOriginalRomPayloadAndDecodedRuntimeImagesVerified=True,counts=dict(counts),unreservedMeasuredBoundaryCandidates=eligible,reservedMeasuredBoundaryCandidates=reserved,deferred=deferred,actualInputPins=[dict(path=p,sha256=h)for p,h in sorted(pins.items())],gitPins=[dict(gitObject=p,sha256=h)for p,h in sorted(gitpins.items())],generatorSha256=sha256(__file__),changedPins=changed,returnTokenQualification=controls,limits=['Native entry/next-entry bounds,reachable instruction/SP paths,returns/tails and actualPC literal footprints derive extents before any accepted-source-size comparison.','Zero/gap bytes are never silently padding. Discontiguous,conditional-SP correlation,unbalanced/unknownSP,computedPC,indirect contracts and ambiguous external data/extent are deferred.','A complete candidate remains evidence-only: Root must independently qualify entry/caller/mode/boundary and current protection before any source or private-index admission.','No original inventory,registry,manifest,ledger,source/helper/Ready,compiler or module products changed.'])
    write_json(LANE/'inventory.json',result);print(dict(status=result['status'],counts=dict(counts),unreserved=len(eligible),unreservedBytes=sum(e['bytes']for e in eligible),reserved=len(reserved),reservedBytes=sum(e['bytes']for e in reserved),pins=len(pins)),flush=True)
    for e in eligible[:35]:print(e['module'],e['mode'],e['address'],e['bytes'],len(e['acceptedIncomingModeProofs']))
    if not stable:raise ValueError('Independent boundary protection/input epoch changed')


if __name__=='__main__':main()
