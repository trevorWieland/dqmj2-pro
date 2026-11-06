from collections import deque
import match_runtime as C
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from capstone.arm import ARM_OP_MEM,ARM_OP_IMM,ARM_REG_PC,ARM_REG_LR,ARM_CC_AL


def union(spans):
    result=[]
    for start,end in sorted(spans):
        if end<=start:raise ValueError('Nonpositive physical span')
        if result and start<=result[-1][1]:result[-1]=(result[-1][0],max(result[-1][1],end))
        else:result.append((start,end))
    return result


def rows(spans):return [dict(start=hex(a),endExclusive=hex(b),bytes=b-a) for a,b in union(spans)] if spans else []


def overlap(left,right):return [(max(a,c),min(b,d)) for a,b in left for c,d in right if max(a,c)<min(b,d)]


def switch_witness(image,base,address,engine):
    values=[next(engine.disasm(image[a-base:a-base+4],a,count=1),None) for a in range(address-12,address+4,4)]
    if any(v is None for v in values):return None
    cmp,guard,sub,dispatch=values
    if cmp.mnemonic!='cmp' or guard.mnemonic!='bgt' or sub.mnemonic!='subs' or dispatch.mnemonic!='addpl':return None
    if len(cmp.operands)!=2 or cmp.operands[1].type!=ARM_OP_IMM or len(sub.operands)!=3 or sub.operands[2].type!=ARM_OP_IMM:return None
    if cmp.operands[0].reg!=sub.operands[1].reg or dispatch.op_str!='pc, pc, '+sub.reg_name(sub.operands[0].reg)+', lsl #2':return None
    lower,upper=sub.operands[2].imm,cmp.operands[1].imm
    if not 0<=lower<=upper<=65535 or upper-lower>255:return None
    sourceRegister=cmp.operands[0].reg;definition=None
    for candidate in range(address-16,max(base,address-64)-1,-4):
        item=next(engine.disasm(image[candidate-base:candidate-base+4],candidate,count=1),None)
        if item is None:return None
        if sourceRegister in item.regs_access()[1]:
            if item.mnemonic!='ldrh' or item.operands[0].reg!=sourceRegister:return None
            definition=candidate;break
    if definition is None:return None
    targets=[address+8+4*index for index in range(upper-lower+1)]
    for target in targets:
        word=int.from_bytes(image[target-base:target-base+4],'little')
        if word&0xff000000!=0xea000000:return None
    return dict(dispatch=hex(address),zeroExtendedSourceRegister=cmp.reg_name(sourceRegister),zeroExtendedDefinition=hex(definition),unsignedInputBits=16,upperCompare=hex(address-12),upperExcludedBySignedGreaterBranch=hex(address-8),lowerSubtractionWithFlags=hex(address-4),lower=lower,upper=upper,indices=upper-lower+1,tableEntryMode='arm',tableEncoding='actual unconditional ARM branch instructions, not data addresses',tableAddresses=[hex(t) for t in targets],criticalLinearFlowStart=hex(definition),criticalLinearFlowEnd=hex(address+4),requiresNoMiddleControlFlowEntry=True)


def analyze(image,base,entry,entries=()):
    if entry&3 or not base<=entry<base+len(image):raise ValueError('ARMv4T entry outside aligned measured module')
    engine=Cs(CS_ARCH_ARM,CS_MODE_ARM);engine.detail=True
    pending=deque([entry]);decoded={};edges=[];literals=[];addresses=[];unresolved=[];returns=[];calls=[];tails=[];indirectCalls=[];switches=[]
    entries=set(entries)-{entry}
    def schedule(target,origin,kind):
        edges.append(dict(origin=hex(origin),target=hex(target),kind=kind,mode='arm'))
        if target&3 or not base<=target<base+len(image):unresolved.append(dict(origin=hex(origin),target=hex(target),reason='unaligned/outside-module noncall control flow'));return
        pending.append(target)
    while pending:
        address=pending.popleft()
        if address in decoded:continue
        if len(decoded)>len(image)//4:raise ValueError('Unbounded original ARM reachability')
        instruction=next(engine.disasm(image[address-base:address-base+4],address,count=1),None)
        if instruction is None or instruction.size!=4:unresolved.append(dict(address=hex(address),reason='invalid ARM instruction'));continue
        i=instruction;mnemonic=i.mnemonic;word=int.from_bytes(i.bytes,'little');condition=(word>>28)&15
        if mnemonic.startswith(('blx','clz','pld','ldrd','strd','qadd','qsub','qdadd','qdsub','smulb','smult','smlab','smlat','smlawb','smlawt','smulwb','smulwt','mrrc','mcrr')) or condition==15:
            unresolved.append(dict(address=hex(address),word=hex(word),reason='instruction unavailable/unsupported for ARMv4T'));continue
        decoded[address]=dict(address=hex(address),word=hex(word),hex=i.bytes.hex(),mnemonic=mnemonic,operands=i.op_str,mode='arm')
        for operand in i.operands:
            if operand.type==ARM_OP_MEM and operand.mem.base==ARM_REG_PC:
                if operand.mem.index:unresolved.append(dict(address=hex(address),reason='indexed PC-relative data/control requires independent range witness'));continue
                target=address+8+operand.mem.disp;width=1 if mnemonic.startswith(('ldrb','strb')) else 2 if mnemonic.startswith(('ldrh','ldrsh','strh')) else 4
                if not mnemonic.startswith('ldr'):unresolved.append(dict(address=hex(address),reason='PC-relative store is not a literal read'));continue
                if target<base or target+width>base+len(image):unresolved.append(dict(address=hex(address),reason='literal read outside initialized module'));continue
                literals.append(dict(origin=hex(address),address=hex(target),bytes=width,hex=image[target-base:target-base+width].hex(),value=hex(int.from_bytes(image[target-base:target-base+width],'little'))))
        if mnemonic.split('.')[0] in ['adr']:
            addresses.append(dict(origin=hex(address),reason='address-only ADR requires independent pointee-use witness',instruction=decoded[address]))
        isBranch=(word&0x0e000000)==0x0a000000
        conditional=condition!=14
        if isBranch:
            displacement=(word&0xffffff)<<2
            if displacement&(1<<25):displacement-=1<<26
            target=address+8+displacement
            if word&0x01000000:
                calls.append(dict(origin=hex(address),target=hex(target),mode='arm',word=hex(word),condition=condition));schedule(address+4,address,'call-return');continue
            if target in entries:tails.append(dict(origin=hex(address),target=hex(target),mode='arm',word=hex(word)))
            else:schedule(target,address,'branch')
            if conditional:schedule(address+4,address,'conditional-fallthrough')
            continue
        if (word&0x0ffffff0)==0x012fff10:
            register=word&15
            if register==14:returns.append(dict(address=hex(address),instruction=decoded[address],kind='BX-LR ARMv4T interworking return'))
            else:
                previous=int.from_bytes(image[address-base-4:address-base],'little') if address>=base+4 else None
                if previous==0xe1a0e00f:
                    indirectCalls.append(dict(origin=hex(address),targetRegister='r'+str(register),linkRegisterAssignment=hex(address-4),targetMode='runtime-low-bit-unresolved',minimumBodyCredit=0));schedule(address+4,address,'measured-MOV-LR-PC/BX-call-return')
                else:unresolved.append(dict(address=hex(address),reason='dynamic BX lacks measured return-link setup',targetRegister='r'+str(register)))
            if conditional:schedule(address+4,address,'conditional-return-fallthrough')
            continue
        written=i.regs_access()[1]
        if ARM_REG_PC in written:
            switch=switch_witness(image,base,address,engine)
            if switch:
                switches.append(switch)
                for target in switch['tableAddresses']:schedule(int(target,0),address,'bounded-ARM-executable-switch')
            elif (mnemonic.startswith(('pop','ldm')) and 'sp' in i.op_str) or (mnemonic.startswith('mov') and len(i.operands)>1 and i.operands[1].reg==ARM_REG_LR):returns.append(dict(address=hex(address),instruction=decoded[address],kind='ARM register/frame return'))
            else:unresolved.append(dict(address=hex(address),reason='unresolved PC write',instruction=decoded[address]))
            if conditional:schedule(address+4,address,'conditional-PC-write-fallthrough')
            continue
        schedule(address+4,address,'fallthrough')
    for switch in switches:
        for target in range(int(switch['criticalLinearFlowStart'],0)+4,int(switch['criticalLinearFlowEnd'],0),4):
            incoming=[e for e in edges if int(e['target'],0)==target]
            if not incoming or any(int(e['origin'],0)!=target-4 or e['kind'] not in ['fallthrough','conditional-fallthrough'] for e in incoming):unresolved.append(dict(address=hex(target),reason='bounded switch guard/source chain has another control-flow entry',incoming=incoming))
    code=union([(a,a+4) for a in decoded])
    data=union([(int(r['address'],0),int(r['address'],0)+r['bytes']) for r in literals]) if literals else []
    conflicts=overlap(code,data)
    if conflicts:unresolved.append(dict(reason='literal-read bytes overlap reachable instructions',ranges=rows(conflicts)))
    internalData=[(a,b) for a,b in data if a>=entry]
    end=max([b for a,b in code+internalData],default=entry)
    covered=union(code+[(max(entry,a),min(end,b)) for a,b in data if entry<=a<end])
    cursor=entry;holes=[]
    for a,b in covered:
        if a>cursor:holes.append((cursor,a))
        cursor=max(cursor,b)
    if cursor<end:holes.append((cursor,end))
    return dict(entry=hex(entry),entryMode='arm',architecture='ARMv4T',reachableInstructionBytes=sum(b-a for a,b in code),instructionRanges=rows(code),instructionCount=len(decoded),instructions=[decoded[a] for a in sorted(decoded)],edges=edges,directCalls=calls,tailCalls=tails,indirectCalls=indirectCalls,returns=returns,boundedExecutableSwitches=switches,literalReads=literals,literalReadRanges=rows(data),literalReadBytes=sum(b-a for a,b in data),addressOnlyReferences=addresses,unresolved=unresolved,computedEvidenceEndExclusive=hex(end),computedEvidenceEnvelopeBytes=end-entry,unaccountedRanges=rows(holes),completePhysicalEvidence=not unresolved and not holes and bool(returns or tails),sourceOwnershipGranted=False,sourceCredit=0)
