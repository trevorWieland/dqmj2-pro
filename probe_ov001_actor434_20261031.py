import gc
import json
import struct
import match_runtime as c
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import measured_module
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ
from unicorn.arm_const import *
BASE,ENTRY,HELPER,TABLE,STACK,STOP=0x02000000,0x021DB9F4,0x02044CDC,0x02400000,0x027F0000,0x027FF800
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]
IDS=[-32768,-257,-1,0,1,255,256,32767]

def run():
    main,arm,_=measured_module('main');module,overlay,_=measured_module('ov001');container=struct.unpack_from('<I',arm,0x02044D0C-BASE)[0];cases=[];observed=set();negative={'wrong-equality':0,'unsigned-record-index':0}
    for identifier in IDS:
        for nibble in range(16):
            for role in range(2):
                actor=0x02780000+role*0x1000;record=0x02784000+role*0x1000;row=TABLE+100*identifier;word=0xA05A|(nibble<<8);initial=[0xA0434000+i*0x100 for i in range(13)]
                u=Uc(UC_ARCH_ARM,UC_MODE_ARM);u.ctl_set_cpu_model(UC_CPU_ARM_946);u.mem_map(BASE,0x800000);u.mem_write(BASE,arm);u.mem_write(0x021D7240,overlay);u.mem_write(container+4,struct.pack('<I',TABLE));u.mem_write(actor,b'\xA5'*0x360);u.mem_write(record,b'\x5A'*0x84);u.mem_write(actor+0x1E8,struct.pack('<I',record));u.mem_write(record+0x2A,struct.pack('<H',identifier&0xFFFF));u.mem_write(row+4,struct.pack('<H',word));before=bytes(u.mem_read(BASE,0x800000));events=[];reads=[];frame=[];helper_returns=[]
                def code(uc,address,length,data):
                    if not(ENTRY<=address<ENTRY+32 or HELPER<=address<HELPER+48):raise ValueError(('434 unexpected native PC',hex(address)))
                    observed.add(address)
                    if address==HELPER:
                        value=uc.reg_read(UC_ARM_REG_R0)
                        if value!=(identifier&0xFFFFFFFF):raise ValueError('434 signed record input differs')
                        frame.append((uc.reg_read(UC_ARM_REG_SP),uc.reg_read(UC_ARM_REG_LR),[uc.reg_read(r)for r in REGS[4:12]]));events.append([address,value])
                    if address==ENTRY+16:
                        if not frame or uc.reg_read(UC_ARM_REG_SP)!=frame[0][0]or address!=frame[0][1]or[uc.reg_read(r)for r in REGS[4:12]]!=frame[0][2]:raise ValueError('434 helper actual return/frame differs')
                        value=uc.reg_read(UC_ARM_REG_R0)
                        if value!=nibble//3:raise ValueError('434 independent class model differs')
                        helper_returns.append(value);frame.clear()
                def read(uc,access,address,length,value,data):
                    if address in[actor+0x1E8,record+0x2A,row+4]:reads.append([address,length])
                u.hook_add(UC_HOOK_CODE,code);u.hook_add(UC_HOOK_MEM_READ,read);u.reg_write(UC_ARM_REG_CPSR,0x10)
                for register,value in zip(REGS,initial):u.reg_write(register,value)
                u.reg_write(UC_ARM_REG_R0,actor);u.reg_write(UC_ARM_REG_SP,STACK);u.reg_write(UC_ARM_REG_LR,STOP);u.emu_start(ENTRY,STOP,count=256)
                result=u.reg_read(UC_ARM_REG_R0);expected=int(nibble//3==2)
                if result!=expected or u.reg_read(UC_ARM_REG_PC)!=STOP or u.reg_read(UC_ARM_REG_SP)!=STACK or u.reg_read(UC_ARM_REG_CPSR)&0x3F!=0x10 or[u.reg_read(r)for r in REGS[4:12]]!=initial[4:12]or len(helper_returns)!=1 or frame:raise ValueError('434 native top return/model differs')
                after=bytes(u.mem_read(BASE,0x800000));cut=STACK-0x10000-BASE;end=STACK+0x1000-BASE
                if before[:cut]!=after[:cut]or before[end:]!=after[end:]:raise ValueError('434 unexpected nonstack memory effect')
                required=[[actor+0x1E8,4],[record+0x2A,2],[row+4,2]]
                if reads!=required:raise ValueError(('434 native read chain differs',reads,required))
                negative['wrong-equality']+=int(result!=int(nibble//3==1));negative['unsigned-record-index']+=int(row!=TABLE+100*(identifier&0xFFFF))
                cases.append(dict(actorRole=role,incomingR0=hex(actor),recordPointer=hex(record),signedRecordWord=identifier,tableFieldWord=word,derivedClass=helper_returns[0],returnedR0=result,actualTopReturns=1,actualNativeDependencyReturns=1,providedCalls=0,readChain=reads,finalRegisters=[u.reg_read(r)for r in REGS],allNonstackMemoryUnchanged=True));del u;gc.collect()
    if not all(negative.values())or len(observed)!=20:raise ValueError(('434 coverage/negative evidence differs',len(observed),negative))
    write_json(ROOT/'evidence/verification/ov001-actor434-native-input-20261031.json',dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov001',moduleSha256=module['sha256'],entry=hex(ENTRY),mode='arm',nativeBytes=32,nativeSpanSha256=c.sha(overlay[ENTRY-0x021D7240:ENTRY-0x021D7240+32]),mainSha256=main['sha256'],nativeHelper=dict(module='main',address=hex(HELPER),mode='arm',bytes=56,codeBytes=48,nativeSpanSha256=c.sha(arm[HELPER-BASE:HELPER-BASE+56]),tableContainer=hex(container),rowStride=100,fieldOffset=4,independentModel='((fieldWord >> 8) & 15) // 3'),sourceCredit=0,actualTopReturns=len(cases),actualNativeDependencyReturns=len(cases),providedCalls=0,observedNativeInstructionBytes=len(observed)*4,freshMachinePerExecution=True,cpu='ARM946',instructionBound=256,negativeModelRejections=negative,results=cases,generatorSha256=sha256(__file__),reproductionCommand='python probe_ov001_actor434_20261031.py',limits=['Only original ov001 DB9F4 and main44CDC execute; selected source and global catalogues remain untouched','Actor+1E8 points to a synthetic132-byte record; record+2A is consumed as signed16 table index','Synthetic mapped100-byte rows and16 field nibbles qualify the read/return contract, not real monster IDs, table loading or scene reachability','DB9F4 returns Boolean of measured helper class equal2; original formal pointer type and game meaning remain unproven','No source credit and no additional acceptance for the already selected32-byte function']))
    print(json.dumps(dict(topReturns=len(cases),nativeDependencyReturns=len(cases),providedCalls=0,sourceCredit=0,negative=negative)))

if __name__=='__main__':run()
