import hashlib
import struct
import sys
from project import ROOT
sys.path.insert(0,str(ROOT/'deps/native'))
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR,UC_CPU_ARM_946

REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12,UC_ARM_REG_SP,UC_ARM_REG_LR]
TERMINATE=0x02008430
CACHE=0x02007308
FAMILIES={
    0x0204540c:('load',[0x02004e58,0x02004f18,0x02004fd8,0x02005098]),
    0x02045490:('load',[0x02004eb8,0x02004f78,0x02005038,0x020050f8]),
    0x02045514:('pointer',[0x020040ec,0x02004140,0x02004194,0x02004224]),
    0x02045560:('pointer',[0x02004120,0x02004174,0x020041e4,0x0200427c]),
    0x020459dc:('load',[0x02004b58,0x02004c18,0x02004cd8,0x02004d98]),
    0x02045a60:('cached-load',[0x02004bb8,0x02004c78,0x02004d38,0x02004df8]),
    0x02045b98:('mmio',[0x04000008,0x0400000a,0x0400000c,0x0400000e]),
    0x02045c14:('mmio',[0x04001008,0x0400100a,0x0400100c,0x0400100e])
}


def vector(seed,bank):
    registers=[(0x193a0041*(i+3)+seed*0x10203)&0xffffffff for i in range(15)]
    registers[:4]=[bank,0x03002000+seed*32,0x140+seed*16,0x20+seed*4]
    registers[-2:]=[0x0301fff0,0x03018000]
    values=[(0xa5f0+seed*5+i*3)&0xffff for i in range(8)]
    return dict(seed=seed,bank=bank,registers=registers,registerValues=values,flags=((seed&15)<<28)|((seed&1)<<27)|0x1f)


def contract_result(target,seed):
    return 0x03008000+seed*128+(target&0x7f)


def expected(address,v,wrong=False):
    kind,targets=FAMILIES[address]
    bank=v['bank'];args=v['registers'];events=[];reads=[]
    if kind=='cached-load':events.append(dict(address=CACHE,args=[args[1],args[3]]))
    if bank>3:
        events.append(dict(address=TERMINATE,args=[]))
        return dict(endpoint='terminate-entry',events=events,reads=reads,result=None)
    index=bank^1 if wrong else bank
    if kind=='mmio':
        offset=0 if address==0x02045b98 else 4
        reads.append(dict(address=targets[index],bytes=2))
        result=v['registerValues'][offset+bank]&3
    elif kind=='pointer':
        events.append(dict(address=targets[index],args=[]))
        result=contract_result(targets[bank],v['seed'])
    else:
        events.append(dict(address=targets[index],args=args[1:4]))
        result=1
    return dict(endpoint='return',events=events,reads=reads,result=result)


def run(code,address,bindings,v):
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02000000,0x100000)
    uc.mem_map(0x03000000,0x20000)
    uc.mem_map(0x04000000,0x2000)
    uc.mem_write(address,code)
    for index,target in enumerate([0x04000008,0x0400000a,0x0400000c,0x0400000e,0x04001008,0x0400100a,0x0400100c,0x0400100e]):
        uc.mem_write(target,struct.pack('<H',v['registerValues'][index]))
    uc.reg_write(UC_ARM_REG_CPSR,v['flags'])
    for register,value in zip(REGS,v['registers']):uc.reg_write(register,value)
    targets={int(b['address'],0):b for b in bindings.values() if b['kind']=='function'}
    events=[];writes=[];reads=[];count=0;endpoint=None

    def on_code(machine,pc,size,user):
        nonlocal count,endpoint
        count+=1
        if pc==v['registers'][-1]:
            endpoint='return';machine.emu_stop();return
        if pc in targets:
            binding=targets[pc]
            assert binding['mode']=='arm' and binding['module']=='main' and binding['processor']=='arm9'
            argc=0 if pc==TERMINATE else 2 if pc==CACHE else 0 if FAMILIES[address][0]=='pointer' else 3
            args=[machine.reg_read(r) for r in REGS[:argc]]
            events.append(dict(address=pc,args=args))
            if pc==TERMINATE:
                endpoint='terminate-entry';machine.emu_stop();return
            saved_lr=machine.reg_read(UC_ARM_REG_LR)
            for index,register in enumerate([UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R12]):
                machine.reg_write(register,(0xcdef0000+v['seed']*257+index*0x1021)&0xffffffff)
            machine.reg_write(UC_ARM_REG_R0,contract_result(pc,v['seed']))
            machine.reg_write(UC_ARM_REG_CPSR,(((v['seed']+3)&15)<<28)|((v['seed']&1)<<27)|0x1f)
            machine.reg_write(UC_ARM_REG_PC,saved_lr)
            return
        assert address<=pc<address+len(code),('Caller escaped declared scope',hex(pc))

    def on_write(machine,access,target,size,value,user):
        writes.append(dict(address=target,bytes=size,value=value&((1<<(size*8))-1)))

    def on_read(machine,access,target,size,value,user):
        if 0x04000000<=target<0x04002000:reads.append(dict(address=target,bytes=size))

    uc.hook_add(UC_HOOK_CODE,on_code)
    uc.hook_add(UC_HOOK_MEM_WRITE,on_write)
    uc.hook_add(UC_HOOK_MEM_READ,on_read)
    uc.emu_start(address,0,count=512,timeout=200000)
    assert endpoint is not None
    final=[uc.reg_read(register) for register in REGS]
    assert not any(not 0x0301fd00<=write['address']<0x03020000 for write in writes)
    if endpoint=='return':
        assert final[4:12]==v['registers'][4:12]
        assert final[-2]==v['registers'][-2]
    return dict(endpoint=endpoint,events=events,reads=reads,registers=final,cpsr=uc.reg_read(UC_ARM_REG_CPSR),writes=writes,instructions=count,ramSha256=hashlib.sha256(bytes(uc.mem_read(0x03000000,0x20000))).hexdigest())


def execute(address,native,source,bindings):
    cases=[];rejected=0
    vectors=[vector(seed,seed%4) for seed in range(8)]+[vector(index+16,bank) for index,bank in enumerate([4,255,0x80000000,0xffffffff])]
    for v in vectors:
        original=run(native,address,bindings,v)
        rebuilt=run(source,address,bindings,v)
        assert original==rebuilt
        model=expected(address,v)
        assert original['endpoint']==model['endpoint'] and original['events']==model['events'] and original['reads']==model['reads']
        if model['endpoint']=='return':assert original['registers'][0]==model['result']
        altered=expected(address,v,True)
        if v['bank']<=3:
            assert original['events']!=altered['events'] or original['reads']!=altered['reads']
            rejected+=1
        cases.append(dict(seed=v['seed'],bank=hex(v['bank']),endpoint=original['endpoint'],modelPassed=True,sourceEqualsOriginal=True,stateSha256=hashlib.sha256(repr(original).encode()).hexdigest()))
    return dict(modelCases=len(cases),supportedReturningVectors=8,actualNativeAndSourceCallerReturns=16,stopAtTerminateEntryVectors=4,terminationEndpointIsNotCallerReturn=True,modelTargetSwapControlsRejected=rejected,allGprsCpsrOrderedWritesAndRamCompared=True,calleeSavedAndStackAbiCheckedOnReturns=True,callerNonStackWrites=0,nativeCalleeBodiesExecuted=0,hardwareOrGameExecutionCredit=0,providedSdkContracts='Deterministic ABI-preserving register providers only; cache/load/pointer bodies are not executed; MMIO values are prescribed memory snapshots',cases=cases)
