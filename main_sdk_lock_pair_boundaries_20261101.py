import hashlib
import re
from functools import lru_cache
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM,CS_MODE_THUMB,CS_GRP_CALL,CS_GRP_JUMP
from capstone.arm import ARM_REG_PC
from link_runtime_unit import measured_module


@lru_cache(maxsize=1)
def measured_references():
    result=[]
    for name in('main','itcm'):
        module,data,config=measured_module(name);base=int(module['base'],0)
        for mode,size,address in re.findall(r'^\S+ kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]{8})$',config,re.M):
            address,size=int(address,0),int(size,0)
            decoder=Cs(CS_ARCH_ARM,CS_MODE_THUMB if mode=='thumb'else CS_MODE_ARM);decoder.detail=True
            for instruction in decoder.disasm(data[address-base:address-base+size],address):
                if(instruction.group(CS_GRP_CALL)or instruction.group(CS_GRP_JUMP))and instruction.operands and instruction.operands[0].type==2:
                    target=instruction.operands[0].imm&~1
                    if any(a<=target<a+n for a,n in{0x02005F08:116,0x02005F8C:108}.items()):
                        result.append({'module':name,'root':hex(address),'mode':mode,'pc':hex(instruction.address),'target':hex(target)})
    return result


def boundaries(entry):
    module,data,config=measured_module('main');address=int(entry['address'],0);size=entry['bytes'];base=int(module['base'],0)
    pattern=r'^\S+ kind:function\(arm,size=0x'+f'{size:x}'+r'\) addr:0x'+f'{address:08x}'+r'$'
    if not re.search(pattern,config,re.M):raise ValueError('Complete configured ARM main lock boundary differs')
    native=data[address-base:address-base+size];decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);decoder.detail=True
    instructions=list(decoder.disasm(native,address))
    if sum(row.size for row in instructions)!=size or any(operand.type==3 and operand.mem.base==ARM_REG_PC for row in instructions for operand in row.operands):
        raise ValueError('Lock function includes unqualified instruction/pool/data bytes')
    expected={0x02005F08:{0x02005F30:0x02008020,0x02005F38:0x02007FF4,0x02005F68:0x02008034,0x02005F70:0x02008008},
        0x02005F8C:{0x02005FA4:0x02008020,0x02005FAC:0x02007FF4,0x02005FBC:0x02008F4C,0x02005FE4:0x02008034,0x02005FEC:0x02008008}}
    calls={row.address:row.operands[0].imm for row in instructions if row.group(CS_GRP_CALL)and row.operands[0].type==2}
    if calls!=expected[address]:raise ValueError('Original full-word lock helper call identities differ')
    refs=[r for r in measured_references()if address<=int(r['target'],0)<address+size and not address<=int(r['pc'],0)<address+size]
    if any(int(row['target'],0)!=address for row in refs):raise ValueError('Unreconciled configured incoming interior entry')
    words=[]
    for name in('main','itcm'):
        other,raw,unused=measured_module(name);origin=int(other['base'],0)
        for offset in range(0,len(raw)-3,4):
            word=int.from_bytes(raw[offset:offset+4],'little')
            if address<=word&~1<address+size:
                words.append({'module':name,'storage':hex(origin+offset),'word':hex(word)})
                if word&~1!=address:raise ValueError('Unreconciled aligned original word into lock body interior')
    return {'instructionBytes':size,'generatedLiteralBytes':0,'paddingCredit':0,'instructionMode':'arm',
        'moduleSha256':hashlib.sha256(data).hexdigest(),'configuredBoundaryAndCompleteInstructionDecode':True,
        'directHelperCallSites':{hex(k):hex(v)for k,v in calls.items()},'outsideRootReferences':refs,'alignedRootPointerWords':words,
        'outsideInteriorOrPoolReferences':[],'initializedDenominatorDelta':0,
        'limitations':['Configured ARM/Thumb direct-flow and aligned initialized-word scan; opaque computed pointer producers and broad callback modes remain unresolved']}
