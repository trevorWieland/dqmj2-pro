import match_runtime
from unittest.mock import patch
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
from capstone.arm import ARM_OP_MEM,ARM_OP_IMM,ARM_REG_PC,ARM_REG_LR,ARM_CC_AL,ARM_CC_INVALID
import wave20261105_arm7_boundary_next_flow as arm
from wave20261106_arm7_sdk_next_switch_flow import bounded_switch


def analyze(image,base,entry,mode,entries):
    if mode=='arm':
        with patch.object(arm,'switch_witness',bounded_switch):return arm.analyze(image,base,entry,entries)
    if mode!='thumb'or entry&1:raise ValueError('Actual ARM7 entry mode/alignment differs')
    engine=Cs(CS_ARCH_ARM,CS_MODE_THUMB);engine.detail=True;todo=[entry];decoded={};edges=[];literals=[];calls=[];returns=[];tails=[];issues=[];addresses=[];limit=base+len(image)
    def schedule(at,origin,kind):
        edges.append(dict(origin=hex(origin),target=hex(at),kind=kind))
        if at&1 or not base<=at<limit:issues.append(dict(address=hex(origin),reason='Thumb noncall edge leaves measured module/alignment'));return
        todo.append(at)
    while todo:
        at=todo.pop()
        if at in decoded:continue
        if len(decoded)>len(image)//2:raise ValueError('Unbounded actual Thumb reachability')
        i=next(engine.disasm(image[at-base:at-base+4],at,count=1),None)
        if i is None or i.size not in[2,4]:issues.append(dict(address=hex(at),reason='invalid Thumb instruction'));continue
        mnemonic=i.mnemonic
        if(i.size==4 and mnemonic!='bl')or mnemonic.startswith(('blx','it','cbz','cbnz','tbb','tbh','clz','rev','uxth','uxtb','sxth','sxtb')):issues.append(dict(address=hex(at),reason='unsupported ARMv4T Thumb encoding'));continue
        decoded[at]=dict(address=hex(at),hex=i.bytes.hex(),mnemonic=mnemonic,operands=i.op_str,mode='thumb')
        for op in i.operands:
            if op.type==ARM_OP_MEM and op.mem.base==ARM_REG_PC:
                target=((at+4)&~3)+op.mem.disp
                if mnemonic!='ldr'or op.mem.index or not base<=target<=limit-4:issues.append(dict(address=hex(at),reason='unsupported/outside Thumb literal read'));continue
                literals.append(dict(origin=hex(at),address=hex(target),bytes=4,hex=image[target-base:target-base+4].hex()))
        if mnemonic=='adr':addresses.append(dict(origin=hex(at),reason='Thumb ADR requires independently measured pointee coverage'))
        conditional=i.cc not in[ARM_CC_AL,ARM_CC_INVALID]
        if mnemonic=='bl':
            if not i.operands or i.operands[0].type!=ARM_OP_IMM:issues.append(dict(address=hex(at),reason='unresolved Thumb call'));continue
            calls.append(dict(origin=hex(at),target=hex(i.operands[0].imm),mode='thumb'));schedule(at+i.size,at,'call-return');continue
        if mnemonic=='b'or(mnemonic.startswith('b')and conditional and i.operands and i.operands[0].type==ARM_OP_IMM):
            target=i.operands[0].imm
            if target in entries and target!=entry:tails.append(dict(origin=hex(at),target=hex(target),mode='thumb'))
            else:schedule(target,at,'branch')
            if conditional:schedule(at+i.size,at,'conditional-fallthrough')
            continue
        if mnemonic=='bx':
            if len(i.operands)==1 and i.operands[0].reg==ARM_REG_LR:returns.append(dict(address=hex(at),kind='ARMv4T Thumb BX-LR return'))
            else:issues.append(dict(address=hex(at),reason='unqualified dynamic Thumb BX'))
            continue
        if ARM_REG_PC in i.regs_access()[1]:
            if mnemonic=='pop'and any(op.reg==ARM_REG_PC for op in i.operands):returns.append(dict(address=hex(at),kind='ARMv4T Thumb POP-PC return'))
            else:issues.append(dict(address=hex(at),reason='unqualified Thumb PC write'))
            continue
        schedule(at+i.size,at,'fallthrough')
    code=arm.union([(a,a+len(bytes.fromhex(r['hex'])))for a,r in decoded.items()]);data=arm.union([(int(r['address'],0),int(r['address'],0)+r['bytes'])for r in literals])if literals else[]
    if arm.overlap(code,data):issues.append(dict(reason='Thumb literal bytes overlap reachable instructions'))
    end=max([b for a,b in code+data if b>entry],default=entry);covered=arm.union(code+data)if code or data else[];holes=[];cursor=entry
    for a,b in covered:
        if a<entry:issues.append(dict(reason='literal/function extent precedes native entry'));continue
        if a>cursor:holes.append((cursor,a))
        cursor=max(cursor,b)
    return dict(entry=hex(entry),entryMode='thumb',architecture='ARMv4T',reachableInstructionBytes=sum(b-a for a,b in code),instructions=[decoded[a]for a in sorted(decoded)],instructionRanges=arm.rows(code),edges=edges,directCalls=calls,tailCalls=tails,indirectCalls=[],returns=returns,literalReads=literals,literalReadRanges=arm.rows(data),literalReadBytes=sum(b-a for a,b in data),addressOnlyReferences=addresses,unresolved=issues,computedEvidenceEndExclusive=hex(end),computedEvidenceEnvelopeBytes=end-entry,unaccountedRanges=arm.rows(holes),completePhysicalEvidence=not issues and not holes and bool(returns or tails),sourceOwnershipGranted=False,sourceCredit=0)
