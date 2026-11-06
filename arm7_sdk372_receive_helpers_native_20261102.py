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

SIZES={0x027ea9c8:144,0x027edb20:84}
WATCH={0x037fd5c0:'OS_CancelAlarm',0x037fd21c:'OS_GetTick',0x037fd54c:'OS_SetPeriodicAlarm',0x037f8d58:'SendMessageToWmDirect',0x037f8598:'AddTask',0x037fc6d4:'OS_SendMessage'}

def half(cpu,a,v):cpu.mem_write(a,struct.pack('<H',v&65535))
def word(cpu,a,v):cpu.mem_write(a,struct.pack('<I',v&0xffffffff))
def h(cpu,a):return int.from_bytes(cpu.mem_read(a,2),'little')
def w(cpu,a):return int.from_bytes(cpu.mem_read(a,4),'little')
def q(cpu,a):return int.from_bytes(cpu.mem_read(a,8),'little')

def prepare(main,wram,case,index):
    if case['entry']not in SIZES or case['mode']not in(0,2)or case['offset']not in(0,4):raise ValueError('Exact helper entries and initialized field contexts required')
    cpu,meta=context.setup(main,wram,index,mode=case['mode'],offset=case['offset'],heap=True);base=meta['context'];extra={}
    if case['entry']==0x027edb20:
        records=[]
        for manager,count in((base+500,case['queuedToWm']),(base+512,case['requests'])):
            for unused in range(count):
                allocation=context.base.call(cpu,0x037f886c,[manager,384]);meta['prerequisiteReturns'].append(dict(name='actual-command-buffer-allocation',**allocation))
                if not allocation['outgoingR0']:raise ValueError('Bounded actual request allocation failed')
                if manager==base+512:records.append(allocation['outgoingR0'])
        if not records:raise ValueError('Current confirmation pointer needs a real queued request')
        for unused in range(case['prefillSend']):meta['prerequisiteReturns'].append(dict(name='actual-send-queue-prefill',**context.base.call(cpu,0x037fc6d4,[context.SEND,0,0])))
        word(cpu,base+1060,records[0]);half(cpu,base+1064,case['busy']);extra=dict(requests=records,queueBefore=w(cpu,context.SEND+28),sendCapacity=w(cpu,context.SEND+20));args=[]
    else:
        initialized=context.base.call(cpu,0x037fd128,[]);meta['prerequisiteReturns'].append(dict(name='actual-original-tick-initializer',**initialized));half(cpu,0x04000100,case['hardwareTick']);args=[case['milliseconds'],case['callback']]
    return cpu,meta,args,extra

def run(main,wram,case,index,body=None,virtual_address=None):
    cpu,meta,args,extra=prepare(main,wram,case,index);base=meta['context'];top=case['entry'];size=SIZES[top];execute=top if virtual_address is None else virtual_address;extent=size if body is None else len(body)
    if body is not None:
        if virtual_address is None and len(body)!=size or virtual_address is not None and not 0<len(body)<=4096:raise ValueError('Complete source helper or explicit bounded wrong-C mapping required')
        if virtual_address is not None:cpu.mem_map(execute,0x1000)
        cpu.mem_write(execute,body)
    rng=random.Random(0x372000+index);initial=[rng.getrandbits(32)for unused in REGISTERS];initial[:len(args)]=args;initial[-2:]=[context.base.STACK+0x3800,context.base.STOP];cpsr=0x13|((index%4)<<6);cpu.reg_write(UC_ARM_REG_CPSR,cpsr)
    for reg,value in zip(REGISTERS,initial):cpu.reg_write(reg,value)
    active=[];helpers=[];writes=[];own=[];visited=[];returned=[False]
    def code(machine,pc,width,user):
        while active and pc==active[-1]['returnPc']and machine.reg_read(REGISTERS[-2])==active[-1]['sp']:
            r=active.pop();r.update(actualReturn=True,outgoingR0=machine.reg_read(REGISTERS[0]),outgoingR1=machine.reg_read(REGISTERS[1]));helpers.append(r)
        if pc==context.base.STOP:
            if active:raise ValueError('Helper entry returned with unfinished native callee')
            returned[0]=True;machine.emu_stop();return
        if not(context.base.MAIN<=pc<context.base.MAIN+len(main)or context.base.WRAM<=pc<context.base.WRAM+len(wram)or virtual_address is not None and execute<=pc<execute+extent):raise ValueError('Helper entry escaped initialized code')
        if virtual_address is None and execute+size-({464:8,224:4,176:4,144:8,84:4}[size])<=pc<execute+extent:raise ValueError('Own entry fetched its measured literal pool')
        if pc in WATCH:active.append(dict(name=WATCH[pc],entry=hex(pc),arguments=[machine.reg_read(r)for r in REGISTERS[:4]],stackWords=list(struct.unpack('<4I',machine.mem_read(machine.reg_read(REGISTERS[-2]),16))),sp=machine.reg_read(REGISTERS[-2]),returnPc=machine.reg_read(REGISTERS[-1])&~1))
        visited.append(pc)
    def write(machine,access,a,width,value,user):
        if context.base.STACK<=a<context.base.STACK+0x4000:return
        r=[a,width,value&((1<<(8*width))-1)];writes.append(r)
        if execute<=machine.reg_read(UC_ARM_REG_PC)<execute+extent:own.append(r)
    tokens=[cpu.hook_add(UC_HOOK_CODE,code),cpu.hook_add(UC_HOOK_MEM_WRITE,write)];error=None
    try:cpu.emu_start(execute,context.base.STOP+4,count=300000)
    except Exception as e:error=type(e).__name__+':'+str(e)
    finally:
        for token in tokens:cpu.hook_del(token)
    if not returned[0]:return dict(case=case,actualOwnReturn=False,error=error or'instruction-bound exhaustion',pc=hex(cpu.reg_read(UC_ARM_REG_PC)),postFaultStateCredit=0,sourceCredit=0)
    named=lambda name:[r for r in helpers if r['name']==name];checks=dict(calleeSaved=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in list(range(4,12))+[13,14]),modeAndInterruptControl=(cpu.reg_read(UC_ARM_REG_CPSR)&255)==cpsr)
    if top==0x027edb20:
        request=extra['requests'][0];remaining=case['requests']-1;successful=not case['queuedToWm']and extra['queueBefore']<extra['sendCapacity'];checks.update(independentBusyBit=h(cpu,base+1064)==(case['busy']&65534),independentOwnStore=own==[[base+1064,2,case['busy']&65534]],originalRequestForwarded=any(r['arguments'][:2]==[base+512,request]for r in named('SendMessageToWmDirect')),requestCount=h(cpu,base+520)==remaining,requestHead=w(cpu,base+512)==(extra['requests'][1]if remaining else 0xffffffff),queueCount=w(cpu,context.SEND+28)==extra['queueBefore']+int(successful),toWmCount=h(cpu,base+508)==case['queuedToWm']+int(not successful),currentRequestPointer=w(cpu,base+1060)==request,independentFollowupOrder=[r['arguments'][:2]for r in named('AddTask')]==([[2,19]]if case['queuedToWm']else[])+([[2,11]]if remaining else[]))
    else:
        tick=[r for r in named('OS_GetTick')if execute<=r['returnPc']<execute+extent];alarm=base+0x608;period=((33514*case['milliseconds'])>>6)&0xffffffff;now=(tick[0]['outgoingR0']|(tick[0]['outgoingR1']<<32))if len(tick)==1 else 0;checks.update(oneTickRead=len(tick)==1,actualCancel=any(r['arguments'][0]==alarm for r in named('OS_CancelAlarm')),actualSetPeriodic=any(r['arguments'][0]==alarm for r in named('OS_SetPeriodicAlarm')),storedCallback=w(cpu,alarm)==case['callback'],storedArgument=w(cpu,alarm+4)==0,storedPeriod=q(cpu,alarm+28)==period,storedStart=q(cpu,alarm+36)==((now+period)&0xffffffffffffffff),noOwnNonstackStores=not own)
    return dict(case=case,actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,registers=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),pc=cpu.reg_read(UC_ARM_REG_PC),orderedNonstackWrites=writes,ownedNonstackWrites=own,memorySha256={hex(a):hashlib.sha256(cpu.mem_read(a,n)).hexdigest()for a,n in meta['regions'].items()},actualDeclaredHelperReturns=helpers,actualSetupEntryReturns=meta['prerequisiteReturns'],visited=sorted(set(pc for pc in visited if execute<=pc<execute+extent)),instructions=len(visited),sourceCredit=0,providerReplacements=[],timerDispatchAndValidCommandLaunchUnproved=True)

def cases():
    rows=[]
    for mode,offset,busy,requests,queued,prefill in itertools.product((0,2),(0,4),(0,1,2,3,65535),(1,2),(0,1),(0,16)):rows.append(dict(entry=0x027edb20,mode=mode,offset=offset,busy=busy,requests=requests,queuedToWm=queued,prefillSend=prefill))
    for mode,offset,ms,tick,callback in itertools.product((0,2),(0,4),(0,1,1000,65535,0x7fffffff,0x80000000,0xffffffff),(0,1,65535),(0x027ed410,0x027ed514)):rows.append(dict(entry=0x027ea9c8,mode=mode,offset=offset,milliseconds=ms,hardwareTick=tick,callback=callback))
    return rows
