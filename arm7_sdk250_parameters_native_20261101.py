import hashlib
import itertools
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC

MAIN,WRAM,DATA,STACK,MAC,STOP,WORD=0x027e0000,0x037f8000,0x023c0000,0x03030000,0x04804000,0x0f000000,0x0380fff4
SIZES={0x027e9578:100,0x027e9744:68,0x027ead78:52}
CODES={0x027e9578:88,0x027e9744:60,0x027ead78:44}

def run(main,wram,case,index,body=None,budget=20000):
    top=case['entry'];size=SIZES[top]
    if hashlib.sha256(main).hexdigest()!='ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416'or hashlib.sha256(wram).hexdigest()!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c':raise ValueError('Measured complete host modules changed')
    if top==0x027e9744 and not 0<=case['period']<=65535:raise ValueError('Declared u16 period producer domain required')
    if body is not None:
        if len(body)!=size:raise ValueError('Complete compiled parameter extent required')
        main=main[:top-MAIN]+body+main[top-MAIN+size:]
    rng=random.Random(0x250000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    regions={MAIN:main+bytes(0x20000-len(main)),WRAM:wram+bytes(0x18000-len(wram)),DATA:rng.randbytes(0x8000),STACK:rng.randbytes(0x4000),MAC:rng.randbytes(0x5000),STOP:bytes(0x1000)}
    for address,raw in regions.items():cpu.mem_map(address,len(raw));cpu.mem_write(address,raw)
    context=DATA+case['contextOffset'];source=DATA+0x2000+case['sourceAlignment'];cpu.mem_write(DATA+0x7000,struct.pack('<I',context));phase='prefix';returned=[False];visited=[];writes=[];helpers=[];active=[];fill=[];fill_returns=[]
    def code(machine,pc,size,user):
        if pc==STOP:
            if active:raise ValueError('Caller returned with unfinished native MAC helper')
            returned[0]=True;machine.emu_stop();return
        if phase=='prefix'and not(0x027e89ec<=pc<0x027e8a10 or 0x037fe014<=pc<0x037fe014+92):raise ValueError('Incoming descriptor prefix escaped')
        if phase=='prefix':
            if fill and pc==fill[-1]['returnPc']and machine.reg_read(REGISTERS[-2])==fill[-1]['sp']:fill_returns.append(dict(fill.pop(),actualReturn=True))
            if pc==0x037fe014:fill.append(dict(entry=hex(pc),returnPc=machine.reg_read(REGISTERS[-1])&~1,sp=machine.reg_read(REGISTERS[-2])))
        if not(MAIN<=pc<MAIN+len(main)or WRAM<=pc<WRAM+len(wram)):raise ValueError('Parameter execution escaped original initialized modules')
        if phase=='target':
            if top+CODES[top]<=pc<top+SIZES[top]:raise ValueError('Parameter executed literal data')
            while active and pc==active[-1]['returnPc']and machine.reg_read(REGISTERS[-2])==active[-1]['sp']:
                item=active.pop();item['actualReturn']=True;item['outgoingR0']=machine.reg_read(REGISTERS[0]);item['calleeSavedPreserved']=[machine.reg_read(r)for r in REGISTERS[4:12]]==item.pop('saved');helpers.append(item)
            if pc==0x027ea0ec:active.append(dict(entry=hex(pc),arguments=[machine.reg_read(r)for r in REGISTERS[:2]],returnPc=machine.reg_read(REGISTERS[-1])&~1,sp=machine.reg_read(REGISTERS[-2]),saved=[machine.reg_read(r)for r in REGISTERS[4:12]]))
            visited.append(pc)
    def store(machine,access,address,width,value,user):
        if phase=='target':writes.append([address,width,value&((1<<(width*8))-1)])
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_WRITE,store);cpu.reg_write(UC_ARM_REG_CPSR,0xd3);cpu.reg_write(REGISTERS[0],DATA+0x7000);cpu.reg_write(REGISTERS[-2],STACK+0x3f00);cpu.reg_write(REGISTERS[-1],STOP);cpu.emu_start(0x027e89ec,0x027e8a10,count=10000)
    if fill and cpu.reg_read(UC_ARM_REG_PC)==fill[-1]['returnPc']and cpu.reg_read(REGISTERS[-2])==fill[-1]['sp']:fill_returns.append(dict(fill.pop(),actualReturn=True,observedAtPrefixBoundary=True))
    if cpu.reg_read(UC_ARM_REG_PC)!=0x027e8a10 or int.from_bytes(cpu.mem_read(WORD,4),'little')!=context or cpu.mem_read(context,0x694)!=bytes(0x694)or len(fill_returns)!=1 or fill:raise ValueError('Original descriptor prefix/clear mismatch')
    cpu.mem_write(context,rng.randbytes(0x694));cpu.mem_write(source,struct.pack('<3H',*case['mac']));cpu.mem_write(MAC+0x40d0,struct.pack('<H',case['status']));initial=[rng.getrandbits(32)for unused in REGISTERS]
    if top==0x027e9578:initial[0]=0 if case.get('nullSource')else source
    elif top==0x027e9744:initial[0]=case['period']
    else:initial[:2]=case['seeds']
    initial[-2:]=[STACK+0x3800,STOP|(index&1)];cpu.reg_write(UC_ARM_REG_CPSR,0x13|((index%4)<<6))
    for reg,value in zip(REGISTERS,initial):cpu.reg_write(reg,value)
    if case.get('wrongRuntimePointer'):cpu.mem_write(WORD,bytes(4))
    before={address:bytes(cpu.mem_read(address,len(raw)))for address,raw in regions.items()};phase='target';returned[0]=False
    try:cpu.emu_start(top,STOP+4,count=budget)
    except Exception as error:return dict(case=case,actualOwnReturn=False,error=str(error),pc=hex(cpu.reg_read(UC_ARM_REG_PC)),postFaultCredit=0,sourceCredit=0)
    if not returned[0]:return dict(case=case,actualOwnReturn=False,error='instruction bound exhausted',pc=hex(cpu.reg_read(UC_ARM_REG_PC)),postFaultCredit=0,sourceCredit=0)
    expected=[]
    if top==0x027e9578:
        for destination in(context+0x3a8,MAC+0x4020):expected.extend([[destination+2*i,2,v]for i,v in enumerate(case['mac'])])
        expected.append([MAC+0x40d0,2,case['status']&~0x400 if case['mac'][0]&1 else case['status']|0x400])
    elif top==0x027e9744:
        if 1<=case['period']<=255:expected=[[context+0x3b8,2,case['period']],[MAC+0x408e,2,case['period']],[MAC+0x4088,2,0]]
    else:expected=[[context+0x5f0,2,((case['seeds'][0]&0xfff8)+5)&65535],[context+0x5f2,2,(case['seeds'][1]|1)&65535]]
    model={address:bytearray(raw)for address,raw in before.items()if address!=STACK}
    for address,width,value in expected:
        base=next(a for a,raw in model.items()if a<=address and address+width<=a+len(raw));model[base][address-base:address-base+width]=value.to_bytes(width,'little')
    checks=dict(calleeSaved=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in list(range(4,12))+[13,14]),returnMode=bool(cpu.reg_read(UC_ARM_REG_CPSR)&32)==bool(initial[-1]&1),independentFullNonstackMemory=all(bytes(cpu.mem_read(a,len(raw)))==bytes(raw)for a,raw in model.items()),independentOrderedNonstackStores=[r for r in writes if not STACK<=r[0]<STACK+0x4000]==expected,actualMacHelperReturns=len(helpers)==(2 if top==0x027e9578 else 0),helperCalleeSaved=all(r['calleeSavedPreserved']for r in helpers))
    if top in(0x027e9578,0x027e9744):checks['declaredStatusReturn']=cpu.reg_read(REGISTERS[0])==(5 if top==0x027e9744 and not 1<=case['period']<=255 else 0)
    return dict(case=case,actualOwnReturn=True,modelChecks=checks,modelPassed=all(checks.values()),registers=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),orderedWrites=writes,visited=sorted(set(visited)),instructions=len(visited),actualNativeHelperReturns=helpers,prefixBoundaryReached=True,actualPrefixFillReturns=fill_returns,constructorActualReturnCredit=0,memorySha256={hex(a):hashlib.sha256(cpu.mem_read(a,len(raw))).hexdigest()for a,raw in regions.items()},providerReplacements=[],sourceCredit=0,physicalMmioConcurrencyAndSceneUnproved=True)

def cases():
    common=dict(mac=[0x1234,0x5678,0x9abc],period=1,seeds=[0,0],sourceAlignment=0,status=0,contextOffset=0)
    vectors=[]
    for off,align,first,last,status in itertools.product((0,4),(0,2),(0,1,2,255,0x8000,65535),(0,65535),(0,0x400,0xffff,0xa55a)):
        vectors.append(dict(common,entry=0x027e9578,contextOffset=off,sourceAlignment=align,mac=[first,0x5678,last],status=status))
    for off,period in itertools.product((0,4),(0,1,2,254,255,256,257,32767,32768,65535)):
        vectors.append(dict(common,entry=0x027e9744,contextOffset=off,period=period))
    for off,a,b in itertools.product((0,4),(0,1,7,8,0xfff8,65535,0x80000000,0xffffffff),(0,1,2,0xffff,0x10000,0x80000000,0xffffffff)):
        vectors.append(dict(common,entry=0x027ead78,contextOffset=off,seeds=[a,b]))
    return vectors
