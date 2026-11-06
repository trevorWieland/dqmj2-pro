import re
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM,CS_GRP_CALL
from capstone.arm import ARM_REG_PC
from link_runtime_unit import measured_module


def boundaries(entry):
    module,raw,config=measured_module('main');address=int(entry['address'],0);base=int(module['base'],0)
    if address!=0x0200867C or entry['bytes']!=152 or not re.search(r'^\S+ kind:function\(arm,size=0x98\) addr:0x0200867c$',config,re.M):
        raise ValueError('Complete configured DMA caller boundary differs')
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);decoder.detail=True
    instructions=list(decoder.disasm(raw[address-base:address-base+152],address))
    if len(instructions)!=38 or any(o.type==3 and o.mem.base==ARM_REG_PC for i in instructions for o in i.operands):
        raise ValueError('DMA source unit has unattributed code/pool bytes')
    expected={0x0200869C:0x020088A4,0x020086C0:0x02008714,0x020086D8:0x02005C64,0x020086F0:0x01FF8448,0x0200870C:0x01FF8448}
    calls={i.address:i.operands[0].imm for i in instructions if i.group(CS_GRP_CALL)and i.operands[0].type==2}
    indirect=[i.address for i in instructions if i.group(CS_GRP_CALL)and i.operands[0].type==1]
    if calls!=expected or indirect!=[0x020086B4]:raise ValueError('Native main/ITCM/direct callback call identities differ')
    return {'instructionBytes':152,'generatedLiteralBytes':0,'paddingCredit':0,'instructionMode':'arm',
        'completeConfiguredNativeBoundary':True,'directCalls':{hex(k):hex(v)for k,v in calls.items()},
        'indirectCallbackCallPc':'0x20086b4','initializedDenominatorDelta':0,
        'limits':['Bounded configured function/call-role proof; physical DMA completion and arbitrary callback/opaque caller coverage remain separate']}
