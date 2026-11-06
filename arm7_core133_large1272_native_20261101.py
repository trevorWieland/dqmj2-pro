import hashlib
import itertools
import random
import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR
from match_runtime import REGISTERS

TOP,VIRTUAL,MAIN,WRAM,DATA,STACK,STOP,WORD=0x027efd3c,0x026d0000,0x027e0000,0x037f8000,0x023c0000,0x03030000,0x0f000000,0x0380fff4
FUNCTIONS={TOP:(1272,1212),0x037f8870:(168,160),0x037fd4f8:(280,276),0x037fe41c:(20,20),0x037fe430:(24,24)}
HEAP_TABLE=0x03805b30

def cases():
    result=[]
    flags=(0,0x8000,0x8002,0x8004,0x8008,0x8010,0x801e,0xffff)
    for mode,active,flag in itertools.product((0,2,65535),(0,1,65535),flags):
        result.append(dict(mode=mode,active=active,flags=flag,payload=519,length=517,defaultPayload=208,defaultLength=517,mask=0xfffe,feature=2))
    for active,flag in itertools.product((1,65535),flags):
        result.append(dict(mode=1,active=active,flags=flag,payload=208,length=516,defaultPayload=208,defaultLength=516,mask=0xfffe,feature=2))
    for flag,length,default_length in itertools.product(flags,(0,516,517,65535),(0,517)):
        result.append(dict(mode=1,active=0,flags=flag,payload=519,length=length,defaultPayload=0x80cf,defaultLength=default_length,mask=0xfffe,feature=2))
    for payload,feature,mask in itertools.product((0,207,208,518,519,0x8000,0x80cf,0x80d0,0xffff),(0,2),(0,0x8000,0xfffe)):
        result.append(dict(mode=1,active=0,flags=0,payload=payload,length=0,defaultPayload=208,defaultLength=0,mask=mask,feature=feature))
    return result

def expected(raw,case,context,packet,response,frame):
    view=bytearray(raw);writes=[]
    def get(address):return struct.unpack_from('<H',view,address-DATA)[0]
    def put(address,value,width=2):
        value&=(1<<(8*width))-1;view[address-DATA:address-DATA+width]=value.to_bytes(width,'little');writes.append([address,width,value])
    put(response+2,1)
    if case['mode']!=1:return 11,'mode',view,writes,False
    if case['active']!=0:return 8,'active',view,writes,False
    flag=get(packet+0x10)
    if flag&0x8000:
        for bit,field,offset in [(2,0x14,0x4c0),(4,0x16,0x4cc),(8,0x18,0x4c2),(16,0x1c,0x4c8)]:
            if not flag&bit:put(packet+field,get(context+offset))
    if get(packet+0x1c)>516:return 5,'length',view,writes,False
    payload=get(packet+0x14);put(context+0x4c0,payload)
    if payload&0x8000:
        payload&=0x7fff;put(packet+0x14,payload);value=((payload-208)&0xffffffff)>>2;put(frame+14,234)
        if value>65536:return 5,'encoded-payload',view,writes,False
    else:
        feature=1 if case['feature']&2 else 0;value=payload+feature
        if value>518+feature:return 5,'payload',view,writes,False
        put(packet+0x14,(2 if feature else 0)+4*value+208);put(frame+14,240 if feature else 234)
    put(context+0x4bc,0,4)
    return 8,'empty-heap',view,writes,True

def run(main,wram,case,index,body=None,budget=20000):
    rng=random.Random(0xfd3c00+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    regions={MAIN:main+bytes(0x20000-len(main)),WRAM:wram+bytes(0x18000-len(wram)),DATA:rng.randbytes(0x8000),STACK:rng.randbytes(0x4000),STOP:bytes(4096)}
    if body is not None:regions[VIRTUAL]=body+bytes(4096-len(body))
    for base,raw in regions.items():cpu.mem_map(base,len(raw));cpu.mem_write(base,raw)
    context=DATA+0x100;packet=DATA+0x1800;response=DATA+0x1900;frame=DATA+0x2000
    cpu.mem_write(WORD,struct.pack('<I',context));cpu.mem_write(HEAP_TABLE,bytes(4));cpu.mem_write(context+0x17c,bytes(12));cpu.mem_write(context+0x470,struct.pack('<I',frame))
    for address,value in [(context+0x32e,case['mode']),(context+0x468,case['active']),(context+0x690,case['feature']),(context+0x4c0,case['defaultPayload']),(context+0x4c8,case['defaultLength']),(context+0x4cc,case['mask']),(context+0x4c2,0x88),(packet+0x10,case['flags']),(packet+0x14,case['payload']),(packet+0x16,case['mask']),(packet+0x18,0x100),(packet+0x1c,case['length'])]:cpu.mem_write(address,struct.pack('<H',value))
    if case.get('zeroRuntimePointer'):cpu.mem_write(WORD,bytes(4))
    if case.get('invalidHeapPointer'):cpu.mem_write(HEAP_TABLE,struct.pack('<I',0xffff0000))
    before={base:bytes(cpu.mem_read(base,len(raw)))for base,raw in regions.items()}
    result,kind,model,wanted,allocated=expected(before[DATA],case,context,packet,response,frame)
    initial=[rng.getrandbits(32)for r in REGISTERS];initial[0:2]=[packet,response];initial[-2:]=[STACK+0x3800,STOP|(index&1)]
    mode=0x13|((index%4)<<6);cpu.reg_write(UC_ARM_REG_CPSR,((index%16)<<28)|mode)
    for reg,value in zip(REGISTERS,initial):cpu.reg_write(reg,value)
    writes=[];reads=[];visited=[];active=[];helpers=[];returned=[False];own=VIRTUAL if body is not None else TOP
    source_code=body.rfind(bytes.fromhex('1eff2fe1'))+4 if body is not None else 0
    if body is not None and not 4<=source_code<len(body):raise ValueError('Complete source ARM return/pool suffix witness missing')
    def code(machine,pc,size,user):
        if pc==STOP:
            if active:raise ValueError('Top returned with active native helpers')
            returned[0]=True;machine.emu_stop();return
        while active and active[-1]['lr']==pc and active[-1]['sp']==machine.reg_read(REGISTERS[-2]):
            item=active.pop();item.update(actualReturn=True,result=machine.reg_read(REGISTERS[0]),calleeSavedPreserved=[machine.reg_read(r)for r in REGISTERS[4:12]]==item['saved']);helpers.append(item)
        allowed=(own<=pc<own+(source_code if body is not None else FUNCTIONS[TOP][1]))or any(entry<=pc<entry+sizes[1]for entry,sizes in FUNCTIONS.items()if entry!=TOP)
        if not allowed or size!=4 or machine.reg_read(UC_ARM_REG_CPSR)&32:raise ValueError('Large1272 escaped supported own/real-helper ARM code')
        visited.append(pc)
        if pc in FUNCTIONS and pc!=TOP:active.append(dict(entry=hex(pc),lr=machine.reg_read(REGISTERS[-1])&~1,sp=machine.reg_read(REGISTERS[-2]),incoming=[machine.reg_read(r)for r in REGISTERS[:4]],saved=[machine.reg_read(r)for r in REGISTERS[4:12]]))
    def store(machine,access,address,width,value,user):
        if not(DATA<=address and address+width<=DATA+0x8000)and not(STACK<=address and address+width<=STACK+0x4000):raise ValueError('Large1272 store escaped synthetic fields/private frames')
        writes.append([address,width,value&((1<<(8*width))-1)])
    def load(machine,access,address,width,value,user):
        reads.append([address,width])
        if DATA<=address and address+width<=DATA+0x8000 or STACK<=address and address+width<=STACK+0x4000:return
        if address in(WORD,HEAP_TABLE)and width==4:return
        if any(entry+code<=address and address+width<=entry+extent and width==4 for entry,(extent,code)in FUNCTIONS.items()):return
        if body is not None and VIRTUAL<=address and address+width<=VIRTUAL+len(body)and width==4:return
        raise ValueError('Large1272 read outside supported fields/heap word/code pools')
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_WRITE,store);cpu.hook_add(UC_HOOK_MEM_READ,load);cpu.emu_start(own,STOP+4,count=budget)
    if not returned[0]:raise ValueError('Large1272 did not actually return within count cap')
    external=[w for w in writes if not STACK<=w[0]<STACK+0x4000];entries=[int(h['entry'],0)for h in helpers]
    wanted_entries=[0x037fe41c,0x037fe430,0x037fd4f8,0x037f8870]if allocated else[]
    checks=dict(result=cpu.reg_read(REGISTERS[0])==result,allExternalWrites=external==wanted,wholeSyntheticData=bytes(cpu.mem_read(DATA,len(model)))==bytes(model),abi=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in range(4,12))and cpu.reg_read(REGISTERS[-2])==initial[-2]and cpu.reg_read(REGISTERS[-1])==initial[-1]and cpu.reg_read(UC_ARM_REG_CPSR)&0xdf==mode,helperEntries=sorted(entries)==sorted(wanted_entries),helperAbi=all(h['calleeSavedPreserved']for h in helpers),otherMappedMemory=all(bytes(cpu.mem_read(base,len(raw)))==raw for base,raw in before.items()if base not in(DATA,STACK)))
    if allocated:
        allocator=next(h for h in helpers if int(h['entry'],0)==0x037f8870);heap=next(h for h in helpers if int(h['entry'],0)==0x037fd4f8)
        final_payload=struct.unpack_from('<H',model,packet-DATA+0x14)[0];mask=struct.unpack_from('<H',model,packet-DATA+0x16)[0];count=(mask&0xfffe).bit_count();feature=1 if case['feature']&2 else 0;value=((case['payload']&0x7fff)-208)>>2 if case['payload']&0x8000 else case['payload']+feature
        effective_payload=struct.unpack_from('<H',model,context-DATA+0x4c0)[0]
        if case['flags']&0x8000 and not case['flags']&2:value=((effective_payload&0x7fff)-208)>>2 if effective_payload&0x8000 else effective_payload+feature
        length=((value+9)&~1)*count+26
        checks['actualAllocatorAndHeapArguments']=allocator['incoming'][:2]==[context+0x188,length]and heap['incoming'][:3]==[0,0,length+12]and allocator['result']==0 and heap['result']==0
    return dict(actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,branch=kind,rawResult=cpu.reg_read(REGISTERS[0]),externalWrites=external,allWrites=writes,allReads=reads,rawRegisters=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),helpers=helpers,actualNativeHelperReturns=len(helpers),visited=sorted(set(visited)),instructions=len(visited),syntheticDataSha256=hashlib.sha256(bytes(cpu.mem_read(DATA,len(model)))).hexdigest(),providers=[],syntheticRuntimePointerAndEmptyHeap=True,fullGameOrPhysicalHardwareContext=False)
