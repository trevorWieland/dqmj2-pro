import gc
import hashlib
import json
import struct
import match_runtime
import probe_ov000_birth329_20261031 as B
from project import ROOT,configuration,sha256,write_json
from link_runtime_unit import measured_module
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
ENTRY,GETTER,TABLE,STACK,STOP=0x02044F9C,0x020449D4,0x02500000,0x027F0000,0x027FF800

def run():
    arm,save,assets=B.inputs()
    metadata,image,unused=measured_module('main')
    table=assets['EnmyKindTbl.bin'][8:]
    observations=[]
    for row in range(len(table)//100):
        variants=[]
        for incoming_r1 in[0,1,0xFFFFFFFF,0xA3470000+row]:
            u=Uc(UC_ARCH_ARM,UC_MODE_ARM)
            u.ctl_set_cpu_model(UC_CPU_ARM_946)
            u.mem_map(0x02000000,0x800000)
            u.mem_write(0x02000000,arm)
            u.mem_write(TABLE,table)
            u.mem_write(0x020F69F0,struct.pack('<I',TABLE))
            writes=[]
            getter=[]
            def write(uc,access,address,size,value,data):
                if not STACK-0x1000<=address<STACK:writes.append([address,size,value])
            def code(uc,address,size,data):
                if address==GETTER:getter.append(dict(speciesWord=uc.reg_read(UC_ARM_REG_R0),incomingR1=uc.reg_read(UC_ARM_REG_R1),sp=uc.reg_read(UC_ARM_REG_SP),lr=uc.reg_read(UC_ARM_REG_LR)))
                if address==ENTRY+8:
                    if len(getter)!=1 or uc.reg_read(UC_ARM_REG_SP)!=getter[0]['sp']or uc.reg_read(UC_ARM_REG_R0)!=TABLE+100*row:raise ValueError('Row43 native pointer getter return differs')
                    getter[0]['actualReturn']=True
            u.hook_add(UC_HOOK_CODE,code)
            u.hook_add(UC_HOOK_MEM_WRITE,write)
            u.reg_write(UC_ARM_REG_CPSR,0x10)
            values=[0xB3470000+i*0x100 for i in range(len(B.REGS))]
            for r,v in zip(B.REGS,values):u.reg_write(r,v)
            u.reg_write(UC_ARM_REG_R0,row)
            u.reg_write(UC_ARM_REG_R1,incoming_r1)
            u.reg_write(UC_ARM_REG_SP,STACK)
            u.reg_write(UC_ARM_REG_LR,STOP)
            u.emu_start(ENTRY,STOP,count=100)
            value=u.reg_read(UC_ARM_REG_R0)
            if u.reg_read(UC_ARM_REG_PC)!=STOP or u.reg_read(UC_ARM_REG_SP)!=STACK or u.reg_read(UC_ARM_REG_CPSR)&0x3F!=0x10 or[u.reg_read(r)for r in B.REGS[4:12]]!=values[4:12]or value!=table[100*row+0x43]or writes or len(getter)!=1 or not getter[0].get('actualReturn'):
                raise ValueError('Row43 native actual return/input/value differs')
            variants.append(dict(incomingR1=incoming_r1,actualReturns=1,nativePointerGetterActualReturns=1,returnWord=value,upper24BitsClear=value<=255,pointerGetter=getter[0],nonstackWrites=0))
        observations.append(dict(rowIndex=row,expectedRawByte=table[100*row+0x43],variants=variants))
        if row%32==0:gc.collect()
    raw=json.dumps(observations,sort_keys=True,separators=(',',':')).encode()
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='main',mode='arm',address=hex(ENTRY),bytes=16,moduleInputSha256=metadata['sha256'],nativeSpanSha256=hashlib.sha256(image[ENTRY-0x02000000:ENTRY-0x02000000+16]).hexdigest(),sourceCredit=0,originalFormalSignature='unproven',measuredRequiredInputWords=['R0 row index'],variedIgnoredCarrierWords=['R1'],qualifiedCallerView='u32 raw_row43(s32 speciesWord,u32 preparedVariantWord)',viewQualification='Two outgoing words are explicit in the ov001021FB214 caller; onlyR0 is required by this measured native getter. A one-word semantic input and the two-word physical caller view are kept distinct.',rows=len(observations),actualReturns=4*len(observations),nativePointerGetterActualReturns=4*len(observations),providedCalls=0,freshMachinePerExecution=True,cpu='ARM946',instructionBound=100,payload=dict(file='EnmyKindTbl.bin',sha256=hashlib.sha256(assets['EnmyKindTbl.bin']).hexdigest(),headerBytes=8,rowStride=100,fieldOffset=67,rawRows=len(table)//100,contentsMeaning='unproven'),observations=observations,observationsSha256=hashlib.sha256(raw).hexdigest(),limits=['All complete raw100-byte table rows are tested; this is a memory/table ABI scope,not proof that every row index is a normal game species','R1 variation does not establish original formal arity or permit invented caller words; the actual scouting caller independently prepares its variant inR1','Only original DS code executes and no accepted source/projection catalogue is edited; duplicate source/function credit is zero','Actual scene initialization, invalid row pointers/indices and table loading lifecycle remain unproven','The returned value is a zero-extended raw table byte,not an inferred field name or game meaning'],generatorSha256=sha256(__file__),reproductionCommand='python probe_main_row43_347_20261031.py')
    write_json(ROOT/'evidence/verification/main-row43-347-native-20261031.json',report)
    print(json.dumps(dict(rows=report['rows'],actualReturns=report['actualReturns'],nativePointerGetterActualReturns=report['nativePointerGetterActualReturns'],providedCalls=0,sourceCredit=0)))

if __name__=='__main__':run()
