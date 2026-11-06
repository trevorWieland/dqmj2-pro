import hashlib
import json
import struct
import match_runtime as compiler
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT
import wave20261106_wcm_manager_next_cps_second_models as F


class Live:
    def __init__(self,cpu,writes):self.cpu,self.writes=cpu,writes
    def read(self,address,size):return bytes(self.cpu.mem_read(address,size))
    def write(self,address,value):self.cpu.mem_write(address,value);self.writes.append(('contract',address,len(value),value.hex()))


def run(image,row,body,v,seed):
    address=int(row['address'],0);memory,args=F.initial(address,v);expected,wanted,contract,result=F.model(address,v)
    cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946)
    cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(address,body)
    cpu.mem_map(F.STOP,0x1000);cpu.mem_map(F.SP-0x4000,0x6000)
    for at,raw in memory.regions.items():cpu.mem_write(at,bytes(raw))
    for index,value in enumerate(args[4:]):cpu.mem_write(F.SP+index*4,struct.pack('<I',value&0xffffffff))
    initial=[(0x11440000+seed*0x101+i*0x110011)&0xffffffff for i in range(15)]
    initial[:min(len(args),4)]=[value&0xffffffff for value in args[:4]];initial[-2:]=[F.SP,F.STOP|1]
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0x30,0x10000030,0x80000030,0xf0000030][seed%4])
    for reg,value in zip(compiler.REGISTERS,initial):cpu.reg_write(reg,value)
    bindings={int(value['address'],0):value for value in row['nativeSymbolEntries'].values() if value['kind']=='function'}
    bindings.pop(address,None)
    bindings.update(F.dynamic_callbacks(v))
    writes=[];calls=[];pcs=[];reads=[];raw_wire=[];returned=False;live=Live(cpu,writes)
    def code(machine,at,size,user):
        nonlocal returned
        if at==F.STOP:returned=True;machine.emu_stop();return
        if at in bindings:
            if bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(bindings[at]['mode']=='thumb'):raise ValueError('Original contract entry mode differs')
            values=[machine.reg_read(reg) for reg in compiler.REGISTERS[:4]]
            count=F.arity(at,values,live)
            values.extend(struct.unpack('<'+'I'*max(0,count-4),live.read(machine.reg_read(ar.UC_ARM_REG_SP),4*max(0,count-4))))
            if at==F.RELIABLE:raw_wire.append(dict(arguments=values[:count],payload=live.read(values[2],values[3]).hex()))
            value,normalized=F.effect(at,values[:count],live,v);calls.append((hex(at),normalized))
            link=machine.reg_read(ar.UC_ARM_REG_LR)
            for index in [1,2,3,12]:machine.reg_write(compiler.REGISTERS[index],(0xa5110000+len(calls)*0x100+index)&0xffffffff)
            machine.reg_write(ar.UC_ARM_REG_R0,value&0xffffffff)
            if at in F.RET64:machine.reg_write(ar.UC_ARM_REG_R1,(value>>32)&0xffffffff)
            if at==F.DIV:machine.reg_write(ar.UC_ARM_REG_R1,(values[0]-value*values[1])&0xffffffff)
            cpsr=(machine.reg_read(ar.UC_ARM_REG_CPSR)&0x0fffffdf)|([0,0x10000000,0x80000000,0xf0000000][(seed+len(calls))%4])|(32 if link&1 else 0)
            machine.reg_write(ar.UC_ARM_REG_PC,link&~1);machine.reg_write(ar.UC_ARM_REG_CPSR,cpsr);return
        if not address<=at<address+len(body) or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError(('Unexpected caller graph/mode escape',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        allowed=F.SP-0x4000<=at and at+size<=F.SP+4*max(0,len(args)-4)
        allowed=allowed or any(start<=at and at+size<=start+len(raw) for start,raw in memory.regions.items() if start!=F.SP-0x1000 and start not in F.READ_ONLY)
        if not allowed:raise ValueError(('Caller escaped bounded writes',hex(at),size))
        writes.append(('caller',at,size,(value&((1<<(size*8))-1)).to_bytes(size,'little').hex()))
    def read(machine,access,at,size,value,user):
        pc=machine.reg_read(ar.UC_ARM_REG_PC)
        if at in F.OBSERVED and address<=pc<address+len(body):reads.append((at,size,int.from_bytes(machine.mem_read(at,size),'little')))
    cpu.hook_add(un.UC_HOOK_MEM_READ,read)
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write)
    cpu.emu_start(address|1,F.STOP+4,count=50000)
    registers=[cpu.reg_read(reg) for reg in compiler.REGISTERS]
    if not returned or registers[4:12]!=initial[4:12] or registers[13]!=F.SP:raise ValueError('Returning caller callee-saved ABI differs')
    actual={at:bytes(cpu.mem_read(at,len(raw))) for at,raw in expected.items()}
    read_passed=reads==F.expected_reads(address,v)
    passed=actual==expected and calls==wanted and read_passed and (contract=='void' or registers[0]==result)
    trace=dict(opaqueAndDefinedWireBytesCompared=raw_wire,orderedSharedWordReads=reads,registers=registers,cpsr=cpu.reg_read(ar.UC_ARM_REG_CPSR),writes=writes,calls=calls,pcs=pcs,externalMemory={hex(at):raw.hex() for at,raw in actual.items()},modelPassed=passed)
    return dict(topReturned=True,modelPassed=passed,orderedSharedWordReadsPassed=read_passed,orderedSharedWordReads=reads,expectedSharedWordReads=F.expected_reads(address,v),traceSha256=hashlib.sha256(json.dumps(trace,sort_keys=True).encode()).hexdigest(),contractCalls=len(calls),calls=calls,expectedCalls=wanted,returnValue=registers[0],expectedReturn=result,returnContract=contract,externalMemoryPassed=actual==expected)


def prove(row,native,source):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[]
    for seed,vector in enumerate(F.cases(int(row['address'],0))):
        original=run(image,row,native,vector,seed);rebuilt=run(image,row,source,vector,seed)
        if original!=rebuilt or not original['modelPassed']:raise ValueError(('Independent bounded WCM caller model differs',row['address'],vector,original,rebuilt))
        records.append(dict(seed=seed,vector=vector,traceSha256=original['traceSha256'],contractCalls=original['contractCalls']))
    return dict(address=row['address'],cases=len(records),actualNativeAndSourceCallerReturns=2*len(records),records=records,allGprsCpsrCalleeSavedStackAndOrderedWritesCompared=True,orderedObservedWordReadsCompared=bool(F.OBSERVED),observedReadAddresses=sorted(F.OBSERVED),definedWirePrefixesIndependentlyModeled=True,allRawWireBytesComparedBetweenNativeAndSource=True,opaqueUnsigned64HelperContract=False,opaqueSignedDivisionHelperContract=any(b['kind']=='function'and b['address']=='0x2026144'for b in row['nativeSymbolEntries'].values()),opaqueUnsigned32DivisionHelperContract=any(b['kind']=='function'and b['address']=='0x2026350'for b in row['nativeSymbolEntries'].values()),originalImportEntryModesChecked=True,suppliedCalleeBodiesExecuted=0,suppliedCalleeSourceOrExecutionCredit=0,networkDevicesOrScenesExecuted=0,indirectCallbackNamespace='Runtime inputs remain unresolved; synthetic ARM/Thumb callback addresses are fixture-only and add no static binding or callee source credit')
