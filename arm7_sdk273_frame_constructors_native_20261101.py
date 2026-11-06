import hashlib
import itertools
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC

MAIN,WRAM,DATA,STACK,MAC,HW,STOP,WORD=0x027e0000,0x037f8000,0x023c0000,0x03030000,0x04804000,0x04000000,0x0f000000,0x0380fff4
SIZES={0x027f16b0:124,0x027f172c:168,0x027f17d4:180,0x027f19fc:352,0x027f1b5c:140,0x027f1e08:192,0x027f1ec8:148}
RATE_VALUES=(2,4,11,12,18,22,24,36,48,72,96,108,0,0,0,0)

def run(main,wram,case,index,body=None,budget=100000):
    top=case['entry'];size=SIZES[top]
    if hashlib.sha256(main).hexdigest()!='ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416'or hashlib.sha256(wram).hexdigest()!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c':raise ValueError('Original complete host runtime modules changed')
    if struct.unpack_from('<16H',main,0x174d0)!=RATE_VALUES:raise ValueError('Original complete16-entry rate-value data differs')
    if struct.unpack_from('<2I',main,top-MAIN+size-8)!=(WORD,0xffff):raise ValueError('Complete constructor runtime/header literals differ')
    if case['ssidLength']not in range(33)or not 0<=case['word']<=65535:raise ValueError('Declared u16 argument and complete32-byte SSID backing required')
    if body is not None:
        if len(body)!=size:raise ValueError('Complete constructor source extent required')
        main=main[:top-MAIN]+body+main[top-MAIN+size:]
    data_size=0x20000 if case['largeHeap']else 0x8000;heap_end=0x7820 if case['heapFailure']else data_size;rng=random.Random(0x273000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T);regions={MAIN:main+bytes(0x20000-len(main)),WRAM:wram+bytes(0x18000-len(wram)),DATA:rng.randbytes(data_size),STACK:rng.randbytes(0x4000),MAC:bytes(0x5000),HW:bytes(0x1000),STOP:bytes(0x1000)}
    for address,raw in regions.items():cpu.mem_map(address,len(raw));cpu.mem_write(address,raw)
    context=DATA+case['contextOffset'];source=DATA+0x5100;cpu.mem_write(DATA+0x7000,struct.pack('<I',context));phase='prefix';returned=[False];prefix_fill=[];fills=[];setup=[];active=[];helpers=[];visited=[];writes=[];owned=[];watched={0x027f1680,0x037f886c,0x027eb078,0x027f1fb4,0x027f2068,0x027f20dc,0x027ead30,0x027ead5c,0x027ea0ec,0x027ebebc,0x027ec04c}
    def code(machine,pc,size,user):
        if pc==STOP:
            if active:raise ValueError('Constructor returned with unfinished native helper')
            returned[0]=True;machine.emu_stop();return
        if phase=='prefix':
            if not(0x027e89ec<=pc<0x027e8a10 or 0x037fe014<=pc<0x037fe014+92):raise ValueError('Incoming descriptor prefix escaped')
            if pc==0x037fe014:prefix_fill.append(dict(entry=hex(pc),returnPc=machine.reg_read(REGISTERS[-1])&~1,sp=machine.reg_read(REGISTERS[-2])))
        if not(MAIN<=pc<MAIN+len(main)or WRAM<=pc<WRAM+len(wram)):raise ValueError('Constructor escaped initialized host code')
        if phase=='target':
            if top+SIZES[top]-8<=pc<top+SIZES[top]:raise ValueError('Constructor executed its runtime/header literals')
            while active and pc==active[-1]['returnPc']and machine.reg_read(REGISTERS[-2])==active[-1]['sp']:
                item=active.pop();item['actualReturn']=True;item['outgoingR0']=machine.reg_read(REGISTERS[0]);item['calleeSavedPreserved']=[machine.reg_read(r)for r in REGISTERS[4:12]]==item.pop('saved');helpers.append(item)
            if pc in watched:active.append(dict(entry=hex(pc),arguments=[machine.reg_read(r)for r in REGISTERS[:4]],returnPc=machine.reg_read(REGISTERS[-1])&~1,sp=machine.reg_read(REGISTERS[-2]),saved=[machine.reg_read(r)for r in REGISTERS[4:12]]))
            visited.append(pc)
    def store(machine,access,address,width,value,user):
        if phase=='target':
            row=[address,width,value&((1<<(width*8))-1)];writes.append(row)
            if top<=machine.reg_read(UC_ARM_REG_PC)<top+SIZES[top]:owned.append(row)
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_WRITE,store);cpu.reg_write(UC_ARM_REG_CPSR,0xd3);cpu.reg_write(REGISTERS[0],DATA+0x7000);cpu.reg_write(REGISTERS[-2],STACK+0x3f00);cpu.reg_write(REGISTERS[-1],STOP);cpu.emu_start(0x027e89ec,0x027e8a10,count=10000)
    if prefix_fill and cpu.reg_read(UC_ARM_REG_PC)==prefix_fill[-1]['returnPc']and cpu.reg_read(REGISTERS[-2])==prefix_fill[-1]['sp']:fills.append(dict(prefix_fill.pop(),actualReturn=True,observedAtPrefixBoundary=True))
    if cpu.reg_read(UC_ARM_REG_PC)!=0x027e8a10 or int.from_bytes(cpu.mem_read(WORD,4),'little')!=context or cpu.mem_read(context,0x694)!=bytes(0x694)or len(fills)!=1 or prefix_fill:raise ValueError('Actual descriptor clear and pointer installation differ')
    cpu.mem_write(context+0x31c,struct.pack('<I',DATA+0x6000));cpu.mem_write(context+0x320,struct.pack('<HH',16 if case['aidExhausted']else 2,2));cpu.mem_write(context+0x304,struct.pack('<I',DATA+0x6400))
    stages=[('queue-init',0x037fc6ac,[DATA+0x6400,DATA+0x6800,16]),('mode',0x027e8f3c,[case['mode']]),('cam-init',0x027ec51c,[]),('tx-init',0x037faec0,[])]
    for name,entry,args in stages:
        phase=name;returned[0]=False;cpu.reg_write(REGISTERS[-2],STACK+0x3f00);cpu.reg_write(REGISTERS[-1],STOP)
        for reg,value in zip(REGISTERS,args):cpu.reg_write(reg,value)
        cpu.emu_start(entry,STOP+4,count=100000)
        if not returned[0]:raise ValueError('Original constructor prerequisite did not return:'+name)
        setup.append(dict(name=name,entry=hex(entry),actualReturn=True,sourceCredit=0))
    for offset in range(0x188,0x23c,12):cpu.mem_write(context+offset,struct.pack('<IIH',0xffffffff,0xffffffff,0))
    for name,entry,args in [('os-heap-init',0x037fce24,[0,DATA+0x7400,DATA+data_size,1]),('os-heap-create',0x037fcecc,[0,DATA+0x7800,DATA+heap_end]),('os-heap-current',0x037fcdf0,[0,0])]:
        phase=name;returned[0]=False;cpu.reg_write(REGISTERS[-2],STACK+0x3f00);cpu.reg_write(REGISTERS[-1],STOP)
        for reg,value in zip(REGISTERS,args):cpu.reg_write(reg,value)
        cpu.emu_start(entry,STOP+4,count=100000)
        if not returned[0]:raise ValueError('Original OS heap prerequisite did not return:'+name)
        setup.append(dict(name=name,entry=hex(entry),actualReturn=True,sourceCredit=0))
    cpu.mem_write(context+0x17c,bytes(12));cpu.mem_write(source,bytes.fromhex('123456789abc'));cpu.mem_write(context+866,struct.pack('<H',case['ssidLength']));cpu.mem_write(context+868,bytes((i*17+3)&255 for i in range(32)));cpu.mem_write(context+932,struct.pack('<HH',case['basic'],case['support']));cpu.mem_write(context+948,struct.pack('<H',case['listen']));cpu.mem_write(context+960,struct.pack('<H',case['capability']));cpu.mem_write(context+424,struct.pack('<H',case['backlog']));cpu.mem_write(context+1336,struct.pack('<H',case['connected']));cpu.mem_write(context+0x3f4,struct.pack('<H',case['initialFatal']));cpu.mem_write(context+966,bytes.fromhex('fedcba987654'));initial=[rng.getrandbits(32)for unused in REGISTERS];initial[:3]=[0 if case.get('nullDestination')else source,case['word'],case['check']]
    if top==0x027f19fc:
        phase='actual-cam-mac-getter';returned[0]=False;cpu.reg_write(REGISTERS[0],case['camIndex']);cpu.reg_write(REGISTERS[-2],STACK+0x3f00);cpu.reg_write(REGISTERS[-1],STOP);cpu.emu_start(0x027ec04c,STOP+4,count=100000);mac_address=cpu.reg_read(REGISTERS[0])
        if not returned[0]or not DATA+0x6000<=mac_address<=DATA+0x6400-6:raise ValueError('Original CAM MAC getter did not return qualified record storage')
        setup.append(dict(name='actual-cam-mac-getter',entry='0x27ec04c',actualReturn=True,outgoingR0=mac_address,sourceCredit=0));cpu.mem_write(mac_address,bytes.fromhex('123456789abc'));cpu.mem_write(source,bytes([case['ssidID'],case['ssidLength']])+bytes((i*17+3)&255 for i in range(32)));initial[:3]=[case['camIndex'],case['word'],0 if case['nullSsid']else source]
        if case['aidExhausted']:
            for cam in range(1,16):
                phase='actual-cam-aid-population';returned[0]=False;cpu.reg_write(REGISTERS[0],cam);cpu.reg_write(REGISTERS[-2],STACK+0x3f00);cpu.reg_write(REGISTERS[-1],STOP);cpu.emu_start(0x027ebebc,STOP+4,count=100000)
                if not returned[0]or cpu.reg_read(REGISTERS[0])!=cam:raise ValueError('Original CAM allocation population did not genuinely return successive1..15')
                setup.append(dict(name='actual-cam-aid-population',entry='0x27ebebc',incomingR0=cam,actualReturn=True,outgoingR0=cpu.reg_read(REGISTERS[0]),sourceCredit=0))
    initial[-2:]=[STACK+0x3800,STOP|(index&1)];cpu.reg_write(UC_ARM_REG_CPSR,0x13|((index%4)<<6))
    for reg,value in zip(REGISTERS,initial):cpu.reg_write(reg,value)
    if case.get('wrongRuntimePointer'):cpu.mem_write(WORD,bytes(4))
    before={a:bytes(cpu.mem_read(a,len(raw)))for a,raw in regions.items()};phase='target';returned[0]=False
    try:cpu.emu_start(top,STOP+4,count=budget)
    except Exception as error:return dict(case=case,actualOwnReturn=False,error=str(error),pc=hex(cpu.reg_read(UC_ARM_REG_PC)),postFaultCredit=0,sourceCredit=0)
    if not returned[0]:return dict(case=case,actualOwnReturn=False,error='instruction bound exhausted',pc=hex(cpu.reg_read(UC_ARM_REG_PC)),postFaultCredit=0,sourceCredit=0)
    requested={0x027f16b0:54,0x027f172c:94,0x027f17d4:100,0x027f19fc:96,0x027f1b5c:90,0x027f1e08:61+case['word'],0x027f1ec8:54}[top];management_denied=top in(0x027f1e08,0x027f1ec8)and case['check']!=0 and not case['backlog']<24-case['connected'];failed=not management_denied and((requested+12+31)&~31)>heap_end-0x7800-32;expected=[];frame=DATA+0x7830
    checks=dict(calleeSaved=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in list(range(4,12))+[13,14]),returnMode=bool(cpu.reg_read(UC_ARM_REG_CPSR)&32)==bool(initial[-1]&1),helperCalleeSaved=all(r['calleeSavedPreserved']for r in helpers))
    checks['independentAllocationArgument']=[]if management_denied else any(r['entry']=='0x37f886c'and r['arguments'][:2]==[context+0x188,requested]for r in helpers)
    if management_denied:checks['independentAllocationArgument']=not any(r['entry']=='0x37f886c'for r in helpers)
    if management_denied:
        checks['rawReturnZero']=cpu.reg_read(REGISTERS[0])==0;checks['noNonstackEffects']=[r for r in writes if not STACK<=r[0]<STACK+0x4000]==[];checks['noAllocationCall']=not any(r['entry']=='0x37f886c'for r in helpers)
    elif failed:
        checks['rawReturnZero']=cpu.reg_read(REGISTERS[0])==0;checks['originalFatalBit2']=int.from_bytes(cpu.mem_read(context+0x3f4,2),'little')==(case['initialFatal']|2);checks['noOwnFrameStores']=[r for r in owned if not STACK<=r[0]<STACK+0x4000]==[];checks['actualAllocationFailure']=any(r['entry']=='0x37f886c'and r['outgoingR0']==0 for r in helpers)
    else:
        checks['actualAllocatedFrameReturn']=cpu.reg_read(REGISTERS[0])==frame;expected=[[DATA+0x782c,2,0xffff]];rate_count=case['support'].bit_count();ssid_length=case['ssidLength'];ofst=2+ssid_length+2+rate_count
        if top==0x027f172c:expected.extend([[frame+44,2,case['capability']],[frame+46,2,case['listen']]]);length=ofst+4;control=0
        elif top==0x027f17d4:expected.extend([[frame+44,2,case['capability']],[frame+46,2,case['listen']]]);length=ofst+10;control=0x20
        elif top==0x027f19fc:
            aid=next((r['outgoingR0']for r in helpers if r['entry']=='0x27ebebc'),0);status=19 if case['word']==0 and aid==0 else case['word'];expected.extend([[frame+44,2,case['capability']],[frame+46,2,status],[frame+48,2,(aid|0xc000)&65535]]);length=2+rate_count+6;control=0x30;checks['camAllocatorCalledOnlyForStatusZero']=any(r['entry']=='0x27ebebc'for r in helpers)==(case['word']==0);checks['actualCamGetterMacDestination']=cpu.mem_read(frame+24,6)==bytes.fromhex('123456789abc');checks['independentAidAvailability']=aid==(0 if case['word']!=0 or case['aidExhausted']else 1)
        elif top==0x027f1b5c:length=ofst;control=0x40
        elif top==0x027f1e08:length=(6+((case['word']+2)&65535 if case['word']else 0))&65535;control=0xb0
        else:expected.append([frame+44,2,case['word']]);length=2;control=0xa0 if top==0x027f16b0 else 0xc0
        expected.extend([[frame+6,2,length],[frame+18,2,(length+28)&65535],[frame+20,2,control]]);checks['independentOwnOrderedStores']=[r for r in owned if not STACK<=r[0]<STACK+0x4000]==expected;checks['originalAllocateActuallyReturnedExpectedBuffer']=any(r['entry']=='0x37f886c'and r['outgoingR0']==DATA+0x7820 for r in helpers);checks['originalHeaderHelperActuallyReturned']=any(r['entry']=='0x27f1fb4'for r in helpers)
        if top==0x027f1e08 and case['word']:checks['independentChallengeHeader']=cpu.mem_read(frame+50,2)==bytes([16,case['word']&255])
        if top==0x027f19fc:
            rate_bytes=bytes([1,rate_count])+bytes((RATE_VALUES[i]|(128 if case['basic']&(1<<i)else 0))&255 for i in range(16)if case['support']&(1<<i));checks['independentResponseRateElement']=cpu.mem_read(frame+50,len(rate_bytes))==rate_bytes;ssid=bytes(2)if case['nullSsid']else bytes([case['ssidID'],case['ssidLength']])+bytes((i*17+3)&255 for i in range(case['ssidLength']));checks['independentResponseSsidTrailer']=cpu.mem_read(frame+54+len(rate_bytes),len(ssid))==ssid;checks['independentCamArgument']=all(r['arguments'][0]==case['camIndex']for r in helpers if r['entry']in('0x27ebebc','0x27ec04c'))
        if top in(0x027f172c,0x027f17d4,0x027f1b5c):
            payload=bytes([0,ssid_length])+bytes((i*17+3)&255 for i in range(ssid_length))+bytes([1,rate_count])+bytes((RATE_VALUES[i]|(128 if case['basic']&(1<<i)else 0))&255 for i in range(16)if case['support']&(1<<i));offset=48 if top==0x027f172c else 54 if top==0x027f17d4 else 44;checks['independentElementPayload']=cpu.mem_read(frame+offset,len(payload))==payload
            if top==0x027f17d4:checks['independentCurrentApMac']=cpu.mem_read(frame+48,6)==bytes.fromhex('fedcba987654')
    return dict(case=case,actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,registers=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),orderedWrites=writes,ownWrites=owned,expectedOwnNonstackStores=expected,actualNativeHelperReturns=helpers,actualSetupReturns=setup,actualPrefixFillReturns=fills,prefixBoundaryReached=True,constructorPrefixActualReturnCredit=0,visited=sorted(set(visited)),instructions=len(visited),memorySha256={hex(a):hashlib.sha256(cpu.mem_read(a,len(raw))).hexdigest()for a,raw in regions.items()},providerReplacements=[],sourceCredit=0,syntheticBacklogAndConnectedFields=True,packetTypeExtensionAndroidPortabilityAndSceneUnproved=True)

def cases():
    base=dict(contextOffset=0,mode=1,ssidLength=3,basic=1,support=3,listen=0x1234,capability=0x13,backlog=0,connected=0,initialFatal=0,heapFailure=False,word=2,check=0,camIndex=0,ssidID=0,nullSsid=False,aidExhausted=False,largeHeap=False)
    rows=[dict(base,entry=entry,ssidLength=length,basic=basic,support=support,contextOffset=off,heapFailure=failed)for entry,length,(basic,support),off,failed in itertools.product((0x027f172c,0x027f17d4,0x027f1b5c),(0,1,31,32),((0,0),(1,3),(0xfff,0xfff),(0x8000,0xffff)),(0,4),(False,True))]
    rows +=[dict(base,entry=entry,word=word,check=check,backlog=backlog,connected=connected,heapFailure=failed)for entry,word,check,backlog,connected,failed in itertools.product((0x027f1e08,0x027f1ec8),(0,1,2,254,255,256,1943,1944,65535),(0,1,0xffffffff),(0,23,24,65535),(0,1,24,25,65535),(False,True))]
    rows +=[dict(base,entry=0x027f16b0,word=word,heapFailure=failed)for word,failed in itertools.product((0,1,2,0xffff),(False,True))]
    rows +=[dict(base,entry=0x027f19fc,word=status,camIndex=cam,ssidLength=length,nullSsid=null,ssidID=identifier,basic=basic,support=support,heapFailure=failed,aidExhausted=exhausted)for status,cam,length,null,identifier,(basic,support),failed,exhausted in itertools.product((0,1,19,0xffff),(0,1),(0,1,32),(False,True),(0,221),((1,3),(0xfff,0xfff)),(False,True),(False,True))]
    rows +=[dict(base,entry=0x027f1e08,word=word,check=check,contextOffset=off,largeHeap=True)for word,check,off in itertools.product((65533,65534,65535),(0,1),(0,4))]
    return rows
