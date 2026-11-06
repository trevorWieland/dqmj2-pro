import hashlib
import itertools
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR,UC_ARM_REG_PC
import arm7_sdk306_task_command_context_20261102 as context
from project import ROOT

SIZES={0x027ec480:156,0x027ec51c:136}
WATCH={0x027ec5a4:'CAM_InitElement',0x027ebc50:'CAM_SetStaState',0x037fdf74:'MIi_CpuClear16'}

def half(cpu,a,v):cpu.mem_write(a,struct.pack('<H',v&65535))
def h(cpu,a):return int.from_bytes(cpu.mem_read(a,2),'little')
def w(cpu,a):return int.from_bytes(cpu.mem_read(a,4),'little')

def prepare(main,wram,case,index,compiled_helper=None):
    if case['entry']not in SIZES or case['mode']not in range(4)or case['offset']not in(0,4)or case['maximum']not in(1,2,4)or not 0<=case['support']<=65535:raise ValueError('Exact bootstrap APIs and complete one-to-four record backing required')
    bodies=None
    if compiled_helper is not None:
        if len(compiled_helper)!=228 or main[0xc5a4:0xc688]!=compiled_helper:raise ValueError('Complete source-linked 228-byte initializer required')
        bodies={0x027ec5a4:compiled_helper}
    cpu,meta=context.setup(main,wram,index,mode=case['mode'],offset=case['offset'],heap=True,bodies=bodies);base=meta['context'];cam=w(cpu,base+0x31c);half(cpu,base+0x320,4);half(cpu,base+0x322,case['maximum']);half(cpu,base+934,case['support']);cpu.mem_write(cam-16,bytes([0x5a])*16);cpu.mem_write(cam,bytes((case['seed']+i*13)&255 for i in range(112)));cpu.mem_write(cam+112,bytes([0xa5])*16);cpu.mem_write(base+0x52c,bytes((case['seed']+i*7)&255 for i in range(16)));return cpu,meta,dict(cam=cam,oldRows=bytes(cpu.mem_read(cam,112)),oldManager=bytes(cpu.mem_read(base+0x52c,16)))

def run(main,wram,case,index,body=None,virtual_address=None,compiled_helper=None):
    cpu,meta,extra=prepare(main,wram,case,index,compiled_helper);base=meta['context'];top=case['entry'];size=SIZES[top];execute=top if virtual_address is None else virtual_address;extent=size if body is None else len(body)
    if body is not None:
        if virtual_address is None and len(body)!=size or virtual_address is not None and not 0<len(body)<=4096:raise ValueError('Complete source bootstrap or bounded compiled wrong-C mapping required')
        if virtual_address is not None:cpu.mem_map(execute,4096)
        cpu.mem_write(execute,body)
    rng=random.Random(0x401000+index);initial=[rng.getrandbits(32)for unused in REGISTERS];initial[-2:]=[context.base.STACK+0x3800,context.base.STOP];cpsr=0x13|((index%4)<<6);cpu.reg_write(UC_ARM_REG_CPSR,cpsr)
    for reg,value in zip(REGISTERS,initial):cpu.reg_write(reg,value)
    active=[];helpers=[];stores=[];own=[];visited=[];returned=[False]
    def code(machine,pc,width,user):
        while active and pc==active[-1]['returnPc']and machine.reg_read(REGISTERS[-2])==active[-1]['sp']:
            r=active.pop();r.update(actualReturn=True,outgoingR0=machine.reg_read(REGISTERS[0]));helpers.append(r)
        if pc==context.base.STOP:
            if active:raise ValueError('Bootstrap returned with unfinished helper')
            returned[0]=True;machine.emu_stop();return
        if not(context.base.MAIN<=pc<context.base.MAIN+len(main)or context.base.WRAM<=pc<context.base.WRAM+len(wram)or virtual_address is not None and execute<=pc<execute+extent):raise ValueError('Bootstrap escaped initialized modules')
        if virtual_address is None and top+({156:144,136:128}[size])<=pc<top+size:raise ValueError('CAM bootstrap fetched its measured literal pool')
        if pc in WATCH:active.append(dict(name=WATCH[pc],entry=hex(pc),arguments=[machine.reg_read(r)for r in REGISTERS[:4]],returnPc=machine.reg_read(REGISTERS[-1])&~1,sp=machine.reg_read(REGISTERS[-2])))
        visited.append(pc)
    def write(machine,access,a,width,value,user):
        if context.base.STACK<=a<context.base.STACK+0x4000:return
        r=[a,width,value&((1<<(8*width))-1)];stores.append(r)
        if execute<=machine.reg_read(UC_ARM_REG_PC)<execute+extent:own.append(r)
    tokens=[cpu.hook_add(UC_HOOK_CODE,code),cpu.hook_add(UC_HOOK_MEM_WRITE,write)];error=None
    try:cpu.emu_start(execute,context.base.STOP+4,count=100000)
    except Exception as e:error=type(e).__name__+':'+str(e)
    finally:
        for token in tokens:cpu.hook_del(token)
    if not returned[0]:return dict(case=case,actualOwnReturn=False,error=error or'instruction-bound exhaustion',pc=hex(cpu.reg_read(UC_ARM_REG_PC)),postFaultStateCredit=0,sourceCredit=0)
    cam=extra['cam'];rows=bytearray(extra['oldRows']);manager=bytearray(extra['oldManager']);maximum=case['maximum'];checks=dict(calleeSaved=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in list(range(4,12))+[13,14]),modeAndInterruptControl=(cpu.reg_read(UC_ARM_REG_CPSR)&255)==cpsr,beforeGuard=bytes(cpu.mem_read(cam-16,16))==bytes([0x5a])*16,afterGuard=bytes(cpu.mem_read(cam+112,16))==bytes([0xa5])*16)
    if top==0x027ec480:
        rows[:28*maximum]=bytes(28*maximum)
        for i in range(maximum):struct.pack_into('<H',rows,28*i+26,65535)
        struct.pack_into('<H',rows,0,64);rows[4:10]=bytes([255])*6;struct.pack_into('<H',rows,16,case['support']);struct.pack_into('<H',rows,20,65535);struct.pack_into('<H',rows,24,65535);manager[:]=struct.pack('<8H',1,0,1,0,0,0,0,0);calls=[r for r in helpers if r['name']=='CAM_InitElement'];checks['actualBroadcastInitializer']=len(calls)==1 and calls[0]['arguments'][:2]==[0,0x027f74b0]
    else:
        for i in range(1,maximum):rows[28*i:28*i+26]=bytes(26)
        struct.pack_into('<H',manager,0,1);struct.pack_into('<H',manager,2,0);struct.pack_into('<H',manager,4,1);struct.pack_into('<H',manager,6,65534);struct.pack_into('<H',manager,8,0);struct.pack_into('<H',manager,12,0);struct.pack_into('<H',manager,14,1);checks['broadcastRecordUntouched']=bytes(cpu.mem_read(cam,28))==extra['oldRows'][:28]
    checks.update(independentAllRows=bytes(cpu.mem_read(cam,112))==rows,independentManagerIncludingOpaqueHalfword=bytes(cpu.mem_read(base+0x52c,16))==manager,originalBroadcastDataUnchanged=bytes(cpu.mem_read(0x027f74b0,6))==bytes([255])*6)
    return dict(case=case,actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,registers=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),pc=cpu.reg_read(UC_ARM_REG_PC),orderedNonstackWrites=stores,ownedNonstackWrites=own,memorySha256={hex(a):hashlib.sha256(cpu.mem_read(a,n)).hexdigest()for a,n in meta['regions'].items()},actualDeclaredHelperReturns=helpers,actualSetupEntryReturns=meta['prerequisiteReturns'],visited=sorted(set(pc for pc in visited if execute<=pc<execute+extent)),instructions=len(visited),sourceLinkedHelper=meta['sourceLinkedProducers'],providerReplacements=[],sourceCredit=0,physicalPeerValidityAndConcurrentRadioUnproved=True)

def cases():return[dict(entry=e,mode=m,offset=o,maximum=n,support=s,seed=seed)for e,m,o,n,s,seed in itertools.product(SIZES,range(4),(0,4),(1,2,4),(0,65535),(0,0x5a,0xff))]
