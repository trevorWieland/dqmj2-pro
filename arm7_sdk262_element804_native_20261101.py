import hashlib
import itertools
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC

MAIN,WRAM,DATA,STACK,STOP,WORD,TOP=0x027e0000,0x037f8000,0x023c0000,0x03030000,0x0f000000,0x0380fff4,0x027f3c1c
RATES=(2,4,11,12,18,22,24,36,48,72,96,108)

def source_compatible(case):
    position=case['sourceAlignment']
    for kind,payload in case['elements']:
        if kind==4 and len(payload)>=6 and position&1:return False
        position+=len(payload)+2
    return True

def run(main,wram,case,index,body=None,budget=100000):
    if hashlib.sha256(main).hexdigest()!='ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416'or hashlib.sha256(wram).hexdigest()!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c':raise ValueError('Measured full host modules changed')
    if any(record[0]==1 and len(record[1])>2 for record in case['elements']):raise ValueError('Rate helper declared two-byte array capacity exceeded')
    if any(not 0<=record[0]<=255 or len(record[1])>255 for record in case['elements']):raise ValueError('Byte element ID/length domain required')
    stream=b''.join(bytes([kind,len(payload)])+bytes(payload)for kind,payload in case['elements'])
    if len(stream)>512:raise ValueError('Declared independent readable byte-stream backing exceeded')
    if body is not None:
        if len(body)!=804:raise ValueError('Complete804-byte compiled parser required')
        main=main[:TOP-MAIN]+body+main[TOP-MAIN+804:]
    rng=random.Random(0x262000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T);regions={MAIN:main+bytes(0x20000-len(main)),WRAM:wram+bytes(0x18000-len(wram)),DATA:rng.randbytes(0x8000),STACK:rng.randbytes(0x4000),STOP:bytes(0x1000)}
    for address,raw in regions.items():cpu.mem_map(address,len(raw));cpu.mem_write(address,raw)
    context=DATA+case['contextOffset'];checker=DATA+0x2000;source=DATA+0x3000+case['sourceAlignment'];join=DATA+0x4000;cpu.mem_write(DATA+0x7000,struct.pack('<I',context));phase='prefix';returned=[False];fill=[];fills=[];helpers=[];active=[];visited=[];writes=[];owned=[]
    def code(machine,pc,size,user):
        if pc==STOP:
            if active:raise ValueError('Parser returned with unfinished native helper')
            returned[0]=True;machine.emu_stop();return
        if phase=='prefix':
            if not(0x027e89ec<=pc<0x027e8a10 or 0x037fe014<=pc<0x037fe014+92):raise ValueError('Descriptor prefix escaped')
            if fill and pc==fill[-1]['returnPc']and machine.reg_read(REGISTERS[-2])==fill[-1]['sp']:fills.append(dict(fill.pop(),actualReturn=True))
            if pc==0x037fe014:fill.append(dict(entry=hex(pc),returnPc=machine.reg_read(REGISTERS[-1])&~1,sp=machine.reg_read(REGISTERS[-2])))
        if not(MAIN<=pc<MAIN+len(main)or WRAM<=pc<WRAM+len(wram)):raise ValueError('Parser escaped initialized host code')
        if phase=='target':
            if TOP+800<=pc<TOP+804:raise ValueError('Parser executed its runtime-word literal')
            while active and pc==active[-1]['returnPc']and machine.reg_read(REGISTERS[-2])==active[-1]['sp']:
                item=active.pop();item['actualReturn']=True;item['outgoingR0']=machine.reg_read(REGISTERS[0]);item['calleeSavedPreserved']=[machine.reg_read(r)for r in REGISTERS[4:12]]==item.pop('saved');helpers.append(item)
            if pc in(0x027ead5c,0x027ea3b0,0x027ea4d0):active.append(dict(entry=hex(pc),arguments=[machine.reg_read(r)for r in REGISTERS[:2]],returnPc=machine.reg_read(REGISTERS[-1])&~1,sp=machine.reg_read(REGISTERS[-2]),saved=[machine.reg_read(r)for r in REGISTERS[4:12]]))
            visited.append(pc)
    def store(machine,access,address,width,value,user):
        if phase=='target':
            row=[address,width,value&((1<<(width*8))-1)];writes.append(row)
            if TOP<=machine.reg_read(UC_ARM_REG_PC)<TOP+804:owned.append(row)
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_WRITE,store);cpu.reg_write(UC_ARM_REG_CPSR,0xd3);cpu.reg_write(REGISTERS[0],DATA+0x7000);cpu.reg_write(REGISTERS[-2],STACK+0x3f00);cpu.reg_write(REGISTERS[-1],STOP);cpu.emu_start(0x027e89ec,0x027e8a10,count=10000)
    if fill and cpu.reg_read(UC_ARM_REG_PC)==fill[-1]['returnPc']and cpu.reg_read(REGISTERS[-2])==fill[-1]['sp']:fills.append(dict(fill.pop(),actualReturn=True,observedAtPrefixBoundary=True))
    if cpu.reg_read(UC_ARM_REG_PC)!=0x027e8a10 or int.from_bytes(cpu.mem_read(WORD,4),'little')!=context or len(fills)!=1 or fill or cpu.mem_read(context,0x694)!=bytes(0x694):raise ValueError('Actual incoming descriptor/clear prerequisite differs')
    cpu.mem_write(context,rng.randbytes(0x694));cpu.mem_write(source,stream+bytes(2));cpu.mem_write(context+866,struct.pack('<H',case['ssidLength']));cpu.mem_write(context+868,b'j2p'+bytes(29));cpu.mem_write(context+900,bytes([case['ssidMask']])*32);cpu.mem_write(context+932,struct.pack('<HH',*case['workRates']));cpu.mem_write(context+936,struct.pack('<H',case['bssid']));cpu.mem_write(context+958,struct.pack('<HH',case['currentChannel'],case['workCapability']));cpu.mem_write(context+1028,struct.pack('<H',case['mlmeState']));cpu.mem_write(context+1052,struct.pack('<I',0 if case.get('nullJoin')else join));cpu.mem_write(join+74,struct.pack('<H',case['joinChannel']));cpu.mem_write(checker,struct.pack('<I9H',source,case['rxStatus'],case['capability'],len(stream),case['match'],case['found'],0xa55a,0x1234,0x9876,case['initialRates'][0])+struct.pack('<3H',case['initialRates'][1],case['otherCount'],case['otherLength'])+struct.pack('<4I',0x11111111,0x22222222,0x33333333,0x44444444));initial=[rng.getrandbits(32)for unused in REGISTERS];initial[0]=0 if case.get('nullChecker')else checker;initial[-2:]=[STACK+0x3800,STOP|(index&1)];cpu.reg_write(UC_ARM_REG_CPSR,0x13|((index%4)<<6))
    for reg,value in zip(REGISTERS,initial):cpu.reg_write(reg,value)
    if case.get('wrongRuntimePointer'):cpu.mem_write(WORD,bytes(4))
    before={a:bytes(cpu.mem_read(a,len(raw)))for a,raw in regions.items()};phase='target';returned[0]=False
    try:cpu.emu_start(TOP,STOP+4,count=budget)
    except Exception as error:return dict(case=case,actualOwnReturn=False,error=str(error),pc=hex(cpu.reg_read(UC_ARM_REG_PC)),postFaultCredit=0,sourceCredit=0)
    if not returned[0]:return dict(case=case,actualOwnReturn=False,error='instruction bound exhausted',pc=hex(cpu.reg_read(UC_ARM_REG_PC)),postFaultCredit=0,sourceCredit=0)
    model={a:bytearray(raw)for a,raw in before.items()if a!=STACK};expected=[];found=case['found'];match=case['match'];other_count=case['otherCount'];other_length=case['otherLength']
    def put(offset,width,value):
        value&=(1<<(width*8))-1;model[DATA][checker-DATA+offset:checker-DATA+offset+width]=value.to_bytes(width,'little');expected.append([checker+offset,width,value])
    def found_bit(bit):
        nonlocal found
        found|=bit;put(12,2,found)
    def match_bit(bit,yes):
        nonlocal match
        match=match|bit if yes else match&~bit;put(10,2,match)
    def unknown(length):
        nonlocal other_count,other_length
        other_count=(other_count+1)&65535;other_length=(other_length+length+2)&65535;put(24,2,other_count);put(26,2,other_length)
    put(18,2,case['currentChannel'])
    if found&0x800:match_bit(1,True)
    position=0
    for kind,payload in case['elements']:
        length=len(payload);address=source+position
        if kind==0 and length<=32:
            found_bit(1);put(28,4,address)
            if length==0 and found&0x800:match_bit(1,True)
            else:
                match_bit(1,False);compare_length=case['ssidLength'];valid=compare_length==0 or(length>=compare_length if case['mlmeState']==0x13 else length==compare_length)and all((payload[i]|case['ssidMask'])==((b'j2p'+bytes(29))[i]|case['ssidMask'])for i in range(compare_length))
                if valid:match_bit(1,True)
        elif kind==1 and length:
            found_bit(4);basic=support=0;put(20,2,0);put(22,2,0)
            for rate in payload:
                bit=1<<RATES.index(rate&127)if rate&127 in RATES else 0x8000;support|=bit;put(22,2,support)
                if rate&128:basic|=bit;put(20,2,basic)
            work_basic,work_support=case['workRates'];match_bit(4,(basic&~(work_basic|work_support))==0 and((basic|support)&work_basic)==work_basic)
        elif kind==3 and length:found_bit(2);put(18,2,payload[0]);match_bit(2,payload[0]==case['joinChannel'])
        elif kind==5 and length>=3:found_bit(0x100);put(36,4,address)
        elif kind==4 and length>=6:found_bit(0x200);put(32,4,address)
        elif kind==221:
            if length>=8 and payload[:4]==[0,9,191,0]:found_bit(0x400);put(40,4,address)
            else:unknown(length)
        elif kind not in(0,1,2,3,4,5,6):unknown(length)
        position+=length+2
    if found&8 and(case['bssid']&1 or case['rxStatus']&0x8000):match_bit(8,True)
    if found&0x30:
        if case['capability']&3==case['workCapability']&3:match_bit(0x10,True)
        if case['capability']&0x10==case['workCapability']&0x10:match_bit(0x20,True)
    checks=dict(calleeSaved=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in list(range(4,12))+[13,14]),returnMode=bool(cpu.reg_read(UC_ARM_REG_CPSR)&32)==bool(initial[-1]&1),independentFullNonstackMemory=all(bytes(cpu.mem_read(a,len(raw)))==bytes(raw)for a,raw in model.items()),independentOrderedNonstackStores=[r for r in writes if not STACK<=r[0]<STACK+0x4000]==expected,helperCalleeSaved=all(r['calleeSavedPreserved']for r in helpers))
    return dict(case=case,actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,registers=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),orderedWrites=writes,ownWrites=owned,expectedNonstackStores=expected,actualNativeHelperReturns=helpers,actualPrefixFillReturns=fills,prefixBoundaryReached=True,constructorActualReturnCredit=0,visited=sorted(set(visited)),instructions=len(visited),memorySha256={hex(a):hashlib.sha256(cpu.mem_read(a,len(raw))).hexdigest()for a,raw in regions.items()},providerReplacements=[],sourceCredit=0,protocolProducerSceneHardwareAndConcurrencyUnproved=True)

def cases():
    base=dict(elements=[],contextOffset=0,sourceAlignment=0,ssidLength=3,ssidMask=0,workRates=[1,0xfff],initialRates=[0x1234,0x5678],mlmeState=0,currentChannel=6,joinChannel=6,bssid=0,rxStatus=0,capability=0,workCapability=0,found=0,match=0,otherCount=0xffff,otherLength=0xfffe)
    vectors=[dict(base,found=found,match=match,capability=capability,workCapability=work,rxStatus=status,bssid=bssid)for found,match,capability,work,status,bssid in itertools.product((0,8,0x30,0x800,0x838,0xffff),(0,0xffff),(0,3,16,19,0xffff),(0,3,16,19),(0,0x8000),(0,1))]
    records=[(0,[]),(0,list(b'j2p')),(0,list(b'abc')),(0,[0]*32),(0,[0]*33),(1,[]),(1,[2]),(1,[130,4]),(1,[255,0]),(2,[]),(3,[]),(3,[6]),(3,[7]),(4,[0]*5),(4,[0]*6),(5,[0]*2),(5,[0]*3),(6,[0]),(221,[0]*7),(221,[0,9,191,0,1,2,3,4]),(221,[1,9,191,0,1,2,3,4]),(221,[0,8,191,0,1,2,3,4]),(221,[0,9,190,0,1,2,3,4]),(221,[0,9,191,1,1,2,3,4]),(7,[1]),(255,[0]*255)]
    vectors +=[dict(base,elements=[[kind,payload]],contextOffset=off,sourceAlignment=align,found=found,match=0xffff,ssidLength=length,ssidMask=mask,mlmeState=state)for(kind,payload),off,align,found,length,mask,state in itertools.product(records,(0,4),(0,1),(0,0x838),(0,3),(0,255),(0,0x13))]
    vectors +=[dict(base,elements=records,sourceAlignment=align,contextOffset=off,found=0x838,match=0xffff,ssidMask=mask)for align,off,mask in itertools.product((0,1),(0,4),(0,255))]
    return vectors
