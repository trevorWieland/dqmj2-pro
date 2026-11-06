import random
from collections import Counter
from functools import lru_cache
import match_runtime
import audit_arm7_bulk_20261030 as inventory
import prove_arm7_lane_halfword_pointer_20261031 as producer
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from project import ROOT,sha256

BASE,WRAM,DATA,STACK,RETURN=producer.BASE,producer.WRAM,producer.DATA,producer.STACK,producer.RETURN
ADDRESS,SIZE,CODE=0x027e8c78,216,212
INITIALIZER,ALLOCATOR,APPEND,HEAP,CALLBACK=0x027e8c5c,0x037f886c,0x037f89f4,0x037fcc74,RETURN+0x100


@lru_cache(maxsize=1)
def scope():
    specs={s['address']:s for s in inventory.specs() if not s['program'] and s['mode']=='arm'};pending=[ADDRESS,ALLOCATOR];chosen={}
    while pending:
        first=pending.pop()
        if first in chosen or first==HEAP:continue
        if first not in specs:raise ValueError('Unqualified original native helper')
        chosen[first]=specs[first]
        pending.extend(i.operands[0].imm for i in specs[first]['instructions'] if i.mnemonic=='bl')
    allowed={i.address for s in chosen.values() for i in s['instructions']};wram=(ROOT/producer.CONFIG['']['wram']).read_bytes();append=chosen[APPEND]
    tag=int.from_bytes(wram[max(append['pools'])-WRAM:max(append['pools'])-WRAM+4],'little')&0xffff
    return chosen,allowed,tag


def cases():
    return [dict(offset=offset,selector=mode,allocated=allocated,context=context,passes=passes)
        for offset in (0x40,0x800) for mode in (0,1) for allocated in (False,True) for context in (0,0xffffffff) for passes in (1,2)]


def setup(body,case,seed):
    if len(body)!=SIZE:raise ValueError('Full compiled node initializer extent differs')
    config=producer.CONFIG[''];main=(ROOT/config['main']).read_bytes();wram=(ROOT/config['wram']).read_bytes()
    if sha256(ROOT/config['main'])!=config['mainSha256'] or sha256(ROOT/config['wram'])!=config['wramSha256']:raise ValueError('Original ARM7 namespace modules changed')
    producer.qualify_roles(main,config);main=bytearray(main+bytes(0x20000-len(main)));main[ADDRESS-BASE:ADDRESS-BASE+SIZE]=body
    regions={BASE:bytes(main),WRAM:wram+bytes(0x18000-len(wram)),DATA:random.Random(seed+701).randbytes(0x4000),STACK:random.Random(seed+709).randbytes(0x4000),RETURN:bytes(0x1000),0x04000000:random.Random(seed+719).randbytes(0x1000)}
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for first,data in regions.items():cpu.mem_map(first,len(data));cpu.mem_write(first,data)
    target=DATA+case['offset'];descriptor=DATA+0x3000;arguments=DATA+0x3100;block=DATA+0x2000
    cpu.mem_write(descriptor,target.to_bytes(4,'little'));words=[case['selector'],CALLBACK if case['selector'] else 0,case['context']]
    cpu.mem_write(arguments,b''.join(w.to_bytes(4,'little') for w in words));chosen,allowed,tag=scope();reads,writes,ownwrites,visited,frames,lower=[],[],[],set(),[],[];returned=Counter();state=dict(phase='prefix',pc=None,instructions=0)
    def code(uc,pc,size,unused):
        state['pc']=pc;state['instructions']+=1
        if uc.reg_read(UC_ARM_REG_CPSR)&32:raise ValueError('Node/allocator fixture entered unqualified Thumb code')
        if state['phase']=='prefix':
            if not (config['constructor']<=pc<config['stop'] or config['fill']<=pc<config['fill']+config['fillBytes']):raise ValueError('Original producer prefix escaped')
            return
        while frames and frames[-1][1]==pc:returned[frames.pop()[0]]+=1
        if pc in (CALLBACK,HEAP):
            count=1 if pc==CALLBACK else 3;args=[uc.reg_read(r) for r in match_runtime.REGISTERS[:count]];expected=[141] if pc==CALLBACK else [0,case['context'],141]
            if args!=expected:raise ValueError('Actual lower allocation boundary words differ')
            lower.append(dict(entry=hex(pc),arguments=args,returnWord=block if case['allocated'] else 0,originalImplementationExecuted=False))
            for index in (1,2,3,12):uc.reg_write(match_runtime.REGISTERS[index],(seed*0x10203+index*0x1030507)&0xffffffff)
            uc.reg_write(match_runtime.REGISTERS[0],block if case['allocated'] else 0);uc.reg_write(UC_ARM_REG_PC,uc.reg_read(match_runtime.REGISTERS[14]));return
        if pc not in allowed:raise ValueError('Node/allocator execution escaped qualified ARM instruction roles: '+hex(pc))
        if pc in chosen and pc!=ADDRESS:frames.append((pc,uc.reg_read(match_runtime.REGISTERS[14])))
        if ADDRESS<=pc<ADDRESS+CODE:visited.add(pc)
    def read(uc,access,where,size,value,unused):
        if state['phase']=='caller':reads.append([where,size])
    def write(uc,access,where,size,value,unused):
        if state['phase']!='caller':return
        row=[where,size,value&((1<<(size*8))-1)];writes.append(row)
        if ADDRESS<=state['pc']<ADDRESS+CODE and not STACK<=where<STACK+0x4000:ownwrites.append(row)
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_READ,read);cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    def registers(argument):
        values=[(seed*0x10203+i*0x1030507+0x7129)&0xffffffff for i in range(15)];values[0]=argument;values[13:]=[STACK+0x3000,RETURN];flags=0x1f|((seed&15)<<28)|((seed&1)<<7)
        cpu.reg_write(UC_ARM_REG_CPSR,flags)
        for register,value in zip(match_runtime.REGISTERS,values):cpu.reg_write(register,value)
        return values,flags
    registers(descriptor);cpu.emu_start(config['constructor'],config['stop'],timeout=500000,count=10000)
    if cpu.reg_read(UC_ARM_REG_PC)!=config['stop'] or cpu.reg_read(match_runtime.REGISTERS[14])!=config['stop'] or bytes(cpu.mem_read(target,0x694))!=bytes(0x694):raise ValueError('Actual descriptor/clear prefix did not reach its natural nonreturn boundary')
    state['phase']='caller'
    def invoke(budget=20000):
        reads.clear();writes.clear();ownwrites.clear();visited.clear();frames.clear();lower.clear();returned.clear();state['instructions']=0
        initial,flags=registers(arguments);guard=bytes(cpu.mem_read(STACK+0x3000,0x1000));fault=None
        try:cpu.emu_start(ADDRESS,RETURN,timeout=500000,count=budget)
        except (UcError,ValueError) as error:fault=str(error)
        actual=cpu.reg_read(UC_ARM_REG_PC)==RETURN and fault is None
        if not actual:return dict(actualReturn=False,fault=fault,pc=hex(cpu.reg_read(UC_ARM_REG_PC)),instructions=state['instructions'],postFaultStateExcluded=True)
        result=[cpu.reg_read(r) for r in match_runtime.REGISTERS];final_flags=cpu.reg_read(UC_ARM_REG_CPSR)
        if result[4:12]!=initial[4:12] or result[13:]!=initial[13:] or final_flags&255!=flags&255 or bytes(cpu.mem_read(STACK+0x3000,0x1000))!=guard or frames:raise ValueError('Node initializer actual return/stack/register/helper-frame contract differs')
        return dict(actualReturn=True,registers=result,cpsr=final_flags,instructions=state['instructions'])
    return dict(cpu=cpu,regions=regions,invoke=invoke,case=case,target=target,arguments=arguments,words=words,block=block,tag=tag,reads=reads,writes=writes,ownWrites=ownwrites,lowerCalls=lower,helperReturns=returned,visited=visited)


def execute(machine,budget=20000):
    steps=[];cpu=machine['cpu'];target=machine['target'];case=machine['case'];block=machine['block']
    for iteration in range(case['passes']):
        expected={first:bytearray(cpu.mem_read(first,len(data))) for first,data in machine['regions'].items() if first!=STACK};owned=[]
        def put(where,size,value):
            for first,data in expected.items():
                if first<=where and where+size<=first+len(data):data[where-first:where-first+size]=(value&((1<<(size*8))-1)).to_bytes(size,'little');return
            raise ValueError('Independent node model escaped mapped backing')
        def own(where,size,value):put(where,size,value);owned.append([where,size,value&((1<<(size*8))-1)])
        for offset,value in zip((0x17c,0x180,0x184),machine['words']):own(target+offset,4,value)
        for index in range(11):
            first=target+0x188+12*index
            for offset,size,value in ((0,4,0xffffffff),(4,4,0xffffffff),(8,2,0),(10,2,index+2)):put(first+offset,size,value)
        if case['allocated']:
            for offset,size,value in ((0,4,0xffffffff),(4,4,0xffffffff),(8,2,2),(10,2,machine['tag'])):put(block+offset,size,value)
            for offset,size,value in ((0,4,block),(4,4,block),(8,2,1)):put(target+0x188+offset,size,value)
        own(target+0x3e0,4,(block if case['allocated'] else 0)+12);own(target+0x3e4,2,0);own(target+0x3e8,2,0)
        result=machine['invoke'](budget)
        machine['lastExecution']=result
        if not result['actualReturn']:return dict(actualReturn=False,execution=result,postFaultStateExcluded=True)
        if machine['ownWrites']!=owned or any(bytes(cpu.mem_read(first,len(data)))!=data for first,data in expected.items()):raise ValueError('Independent complete node/list/allocated-block/IRQ restoration memory or owned-order model differs')
        if machine['helperReturns'][INITIALIZER]!=11 or machine['helperReturns'][ALLOCATOR]!=1 or machine['helperReturns'][APPEND]!=(1 if case['allocated'] else 0) or len(machine['lowerCalls'])!=1:raise ValueError('Actual original helper returns/lower boundary counts differ')
        steps.append(dict(execution=result,ownedOrderedWrites=owned,orderedReads=machine['reads'][:],orderedWrites=machine['writes'][:],ownVisited=sorted(machine['visited']),
            actualNativeHelperReturns={hex(k):v for k,v in sorted(machine['helperReturns'].items())},lowerAllocationProviders=machine['lowerCalls'][:],
            completeMemorySha256={hex(first):sha256_bytes(bytes(cpu.mem_read(first,len(data)))) for first,data in machine['regions'].items()}))
    return dict(actualReturn=True,steps=steps,actualOwnedReturns=len(steps),actualOriginalClearPrerequisiteReturns=1,constructorPrefixReturnCredit=0,independentCompleteMemoryAndOwnedStoreModel=True,
        meaningfulReturnContract='void; incidental R0 is compared without assigning API meaning',physicalAllocationOrIrqOrDeviceExecutionCredit=0)


def sha256_bytes(value):
    import hashlib
    return hashlib.sha256(value).hexdigest()


digest=sha256_bytes
