import hashlib
import re
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from capstone.arm import ARM_REG_PC
from link_runtime_unit import measured_module


def boundaries(entry):
    module,data,config=measured_module('main');address=int(entry['address'],0);base=int(module['base'],0)
    if address!=0x020067FC or entry['bytes']!=124 or not re.search(r'^\S+ kind:function\(arm,size=0x7c\) addr:0x020067fc$',config,re.M):
        raise ValueError('Complete configured ARM thread-removal boundary differs')
    native=data[address-base:address-base+124];decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);decoder.detail=True
    instructions=list(decoder.disasm(native[:120],address))
    if len(instructions)!=30 or int.from_bytes(native[120:124],'little')!=0x020E33C0:
        raise ValueError('Thread-removal full code/literal identity differs')
    expected={0x02006804:0x02007FF4,0x0200681C:0x020067A0,0x02006820:0x02006C70,0x02006828:0x0200716C,
        0x02006830:0x02006878,0x02006844:0x020062A4,0x0200684C:0x02006388,0x0200685C:0x02006924,
        0x02006860:0x02006CA4,0x02006868:0x02008008,0x0200686C:0x020069DC}
    calls={row.address:row.operands[0].imm for row in instructions if row.mnemonic=='bl'}
    if calls!=expected:raise ValueError('Measured native scheduler/mutex/queue/alarm call sites differ')
    literals=[]
    for row in instructions:
        for operand in row.operands:
            if operand.type==3 and operand.mem.base==ARM_REG_PC:
                target=row.address+8+operand.mem.disp
                if target!=address+120:raise ValueError('Unqualified literal reference outside full code/pool unit')
                literals.append({'pc':hex(row.address),'storage':hex(target),'word':'0x20e33c0'})
    if len(literals)!=1:raise ValueError('Exactly one named scheduler data literal required')
    return {'instructionBytes':120,'generatedLiteralBytes':4,'paddingCredit':0,'instructionMode':'arm',
        'moduleSha256':hashlib.sha256(data).hexdigest(),'completeConfiguredNativeBoundary':True,
        'calls':{hex(k):hex(v)for k,v in calls.items()},'literalReferences':literals,'initializedDenominatorDelta':0,
        'limits':['Complete configured function/code/literal proof; current-target bounded no-return and broader computed-caller coverage remain separately scoped']}
