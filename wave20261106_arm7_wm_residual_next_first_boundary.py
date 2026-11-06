import match_runtime as C
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from capstone.arm import ARM_OP_MEM,ARM_REG_PC


def certificate(flow,image,base,expectedHash):
    start=int(flow['entry'],0);end=int(flow['computedEvidenceEndExclusive'],0)
    if flow['entryMode']!='arm' or flow['architecture']!='ARMv4T' or not flow['completePhysicalEvidence'] or flow['unresolved'] or flow['unaccountedRanges']:raise ValueError('ARMv4T physical flow evidence incomplete')
    body=image[start-base:end-base]
    if C.sha(body)!=expectedHash or len(body)!=flow['computedEvidenceEnvelopeBytes']:raise ValueError('Original full evidence span/hash differs')
    mask=bytearray(len(body));instructionAddresses=set()
    for item in flow['instructions']:
        address=int(item['address'],0);word=image[address-base:address-base+4]
        if item['mode']!='arm' or item['hex']!=word.hex() or int(item['word'],0)!=int.from_bytes(word,'little'):raise ValueError('Actual ARM instruction identity differs')
        instructionAddresses.add(address)
        for at in range(address,address+4):mask[at-start]|=1
    for item in flow['literalReads']:
        address=int(item['address'],0);size=item['bytes'];word=image[address-base:address-base+size]
        if address<start or address+size>end or item['hex']!=word.hex() or item['value']!=hex(int.from_bytes(word,'little')):raise ValueError('Actual bounded literal-read identity differs')
        origin=int(item['origin'],0);decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);decoder.detail=True;instruction=next(decoder.disasm(image[origin-base:origin-base+4],origin,count=1),None)
        if origin not in instructionAddresses or instruction is None or not instruction.mnemonic.startswith('ldr') or not any(o.type==ARM_OP_MEM and o.mem.base==ARM_REG_PC and not o.mem.index and origin+8+o.mem.disp==address for o in instruction.operands):raise ValueError('Literal-read original instruction/origin differs')
        width=1 if instruction.mnemonic.startswith('ldrb') else 2 if instruction.mnemonic.startswith(('ldrh','ldrsh')) else 4
        if width!=size:raise ValueError('Literal-read original access width differs')
        for at in range(address,address+size):mask[at-start]|=2
    if set(mask)-{1,2} or mask.count(1)!=flow['reachableInstructionBytes'] or mask.count(2)!=flow['literalReadBytes']:raise ValueError('Instruction/literal physical byte union does not close exactly')
    if set(instructionAddresses)!=set(a for r in flow['instructionRanges'] for a in range(int(r['start'],0),int(r['endExclusive'],0),4)):raise ValueError('Instruction range union differs from actual reachable instructions')
    if len(instructionAddresses)!=len(flow['instructions']):raise ValueError('Duplicate instruction-origin evidence')
    actual=[];decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);decoder.detail=True
    for origin in sorted(instructionAddresses):
        instruction=next(decoder.disasm(image[origin-base:origin-base+4],origin,count=1),None)
        if instruction is None:raise ValueError('Original ARM instruction undecodable')
        for operand in instruction.operands:
            if instruction.mnemonic.startswith('ldr') and operand.type==ARM_OP_MEM and operand.mem.base==ARM_REG_PC and not operand.mem.index:
                address=origin+8+operand.mem.disp;width=1 if instruction.mnemonic.startswith('ldrb') else 2 if instruction.mnemonic.startswith(('ldrh','ldrsh')) else 4;raw=image[address-base:address-base+width];actual.append((origin,address,width,raw.hex(),hex(int.from_bytes(raw,'little'))))
    declared=[(int(r['origin'],0),int(r['address'],0),r['bytes'],r['hex'],r['value'])for r in flow['literalReads']]
    if sorted(actual)!=sorted(declared) or len(set(declared))!=len(declared):raise ValueError('Complete per-origin original literal reads differ')
    return dict(status='passed',sourceCredit=0,start=hex(start),endExclusive=hex(end),bytes=len(body),nativeSpanSha256=C.sha(body),instructionBytes=mask.count(1),literalBytes=mask.count(2),actualLiteralReadOrigins=len(actual),overlapOrUnclassifiedBytes=0,nextEntryUsedToInferSize=False,mode='arm',architecture='ARMv4T')
