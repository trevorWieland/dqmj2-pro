import json
import match_runtime
import arm7_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM,CS_MODE_THUMB,CS_GRP_CALL,CS_GRP_JUMP
from capstone.arm import ARM_REG_PC,ARM_CC_AL
from project import ROOT,sha256,write_json


def main():
    layout=arm7_runtime.derive((ROOT/'extract/arm7/arm7.bin').read_bytes())
    modules={row['id']:row for row in layout['modules']}
    inventory=ROOT/'evidence/arm7/ghidra-runtime-inventory.json'
    functions=json.loads(inventory.read_text())['functions']
    stores=[]
    for row in functions:
        if row['mode'] not in ('arm','thumb'):
            continue
        module=modules[row['module']]
        binary=ROOT/module['binary']
        if sha256(binary)!=module['sha256']:
            raise ValueError('Current measured host ARM7 module differs')
        raw=binary.read_bytes()
        base=int(module['base'],0)
        decoder=Cs(CS_ARCH_ARM,CS_MODE_THUMB if row['mode']=='thumb' else CS_MODE_ARM)
        decoder.detail=True
        for first,last in row['ranges']:
            constants={}
            first,last=int(first,0),int(last,0)
            recent=[]
            for instruction in decoder.disasm(raw[first-base:last-base],first):
                operands=instruction.operands
                recent.append([hex(instruction.address),instruction.mnemonic,instruction.op_str,instruction.bytes.hex()])
                if instruction.mnemonic.startswith('str') and len(operands)>=2 and operands[1].type==3:
                    memory=operands[1].mem
                    if memory.base in constants and not memory.index:
                        target=(constants[memory.base]+memory.disp)&0xFFFFFFFF
                        if target==0x0380FFF4:
                            stores.append(dict(program='',processor='arm7',module=row['module'],mode=row['mode'],parent=row['address'],
                                pc=hex(instruction.address),target=hex(target),conditionCode=instruction.cc,sourceRegister=instruction.reg_name(operands[0].reg),
                                knownSourceValue=constants.get(operands[0].reg),window=recent[-12:],
                                inputModuleSha256=module['sha256'],staticLeadOnly=True,sourceCredit=0))
                assigned={}
                if instruction.cc==ARM_CC_AL and len(operands)>=2 and operands[0].type==1:
                    dest=operands[0].reg
                    if instruction.mnemonic=='ldr' and operands[1].type==3 and operands[1].mem.base==ARM_REG_PC:
                        pcbase=(instruction.address+4)&~3 if row['mode']=='thumb' else instruction.address+8
                        target=pcbase+operands[1].mem.disp
                        if base<=target<=base+len(raw)-4:
                            assigned[dest]=int.from_bytes(raw[target-base:target-base+4],'little')
                    elif instruction.mnemonic=='mov':
                        if operands[1].type==2:
                            assigned[dest]=operands[1].imm&0xFFFFFFFF
                        elif operands[1].type==1 and operands[1].reg in constants:
                            assigned[dest]=constants[operands[1].reg]
                    elif instruction.mnemonic in ('add','sub') and len(operands)==3 and operands[1].type==1 and operands[1].reg in constants and operands[2].type==2:
                        assigned[dest]=(constants[operands[1].reg]+(operands[2].imm if instruction.mnemonic=='add' else -operands[2].imm))&0xFFFFFFFF
                for register in instruction.regs_access()[1]:
                    constants.pop(register,None)
                constants.update(assigned)
                if instruction.group(CS_GRP_CALL) or instruction.group(CS_GRP_JUMP):
                    constants.clear()
    report=dict(generator='scan_arm7_lane_work_pointer_producers_20261031.py',generatorSha256=sha256(__file__),
        inventorySha256=sha256(inventory),target='0x0380fff4',program='',processor='arm7',stores=stores,sourceCredit=0,
        limitation='Static straight-line constant-address leads only; calls/branches reset facts, entry execution and caller reachability remain required')
    path=ROOT/'evidence/attempts/arm7-lane-work-pointer-producers-20261031.json'
    write_json(path,report)
    print(dict(report=path.relative_to(ROOT).as_posix(),sha256=sha256(path),stores=[(row['parent'],row['pc'],row['sourceRegister']) for row in stores],sourceCredit=0))


if __name__=='__main__':
    main()
