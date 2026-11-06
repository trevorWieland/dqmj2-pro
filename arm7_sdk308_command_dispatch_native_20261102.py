import hashlib
import itertools
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR
import arm7_sdk306_task_command_context_20261102 as context

TABLES={0x000:(0x027f7654,11,0,0x20),0x100:(0x027f75cc,5,0,0x40),0x200:(0x027f77bc,23,0,0x10),0x240:(0x027f7624,6,0x40,0x40),0x280:(0x027f7704,23,0x80,0x10),0x2c0:(0x027f75f4,6,0xc0,0x10),0x300:(0x027f76ac,11,0,0)}
TOP=0x037f8a88

def classification(main,case):
    code=case['code'];key=code&0xff00
    if key==0x200:key=code&0xffc0
    table=TABLES.get(key)
    if table is None:return dict(error=3,table=None,index=None,handler=None)
    address,count,low,minimum=table;index=(code&255)-low
    if index==count:raise ValueError('Physical equality-to-table-size behavior withheld from defined-C dispatch domain')
    if index>count:return dict(error=3,table=address,index=index,handler=None)
    req,cfm,handler=struct.unpack_from('<HHI',main,address-context.base.MAIN+8*index);error=1 if(case['state']!=minimum if key in(0x100,0x240)else case['state']<minimum)else 0
    if case['requestLength']<req or case['confirmLength']<cfm:error=4
    if not error and code not in(0x282,0x284,0x288,0x291,0x300):raise ValueError('Original command handler outside current independently modeled synchronous contexts')
    return dict(error=error,table=address,index=index,handler=handler,requestMinimum=req,confirmMinimum=cfm)

def run(main,wram,case,index,bodies=None,body=None,virtual_address=None,budget=200000):
    if case['requestLength']not in range(73)or case['requests']not in(0,1,2)or case['queuedToWm']not in(0,1):raise ValueError('Bounded request/confirmation storage contract required')
    selected=classification(main,case)if not(case['busy']or not case['requests']or case['diag']or case['mismatch'])else dict(error=None,handler=None)
    cpu,meta=context.setup(main,wram,index,case['mode'],case['contextOffset'],heap=True,bodies=bodies);base=meta['context'];stages=meta['prerequisiteReturns'];rng=random.Random(0x308000+index)
    def half(a,v):cpu.mem_write(a,struct.pack('<H',v&65535))
    def word(a,v):cpu.mem_write(a,struct.pack('<I',v&0xffffffff))
    def h(a):return int.from_bytes(cpu.mem_read(a,2),'little')
    def w(a):return int.from_bytes(cpu.mem_read(a,4),'little')
    stages.append(dict(name='actual-send-queue-initializer',**context.base.call(cpu,0x037fc6ac,[context.SEND,context.base.DATA+0x6800,case['sendCapacity']])))
    for unused in range(case['prefillSend']):stages.append(dict(name='actual-send-queue-prefill',**context.base.call(cpu,0x037fc6d4,[context.SEND,0,0])))
    allocations=[]
    for manager,count in((base+500,case['queuedToWm']),(base+512,case['requests'])):
        for unused in range(count):
            record=context.base.call(cpu,0x037f886c,[manager,384]);stages.append(dict(name='actual-command-buffer-allocation',**record))
            if not record['outgoingR0']:raise ValueError('Original allocator failed bounded command fixture')
            if manager==base+512:allocations.append(record['outgoingR0'])
    request=allocations[0]if allocations else None;confirmation=None
    if request is not None:
        cpu.mem_write(request+12,bytes([0x5a])*384);half(request+12,case['code']);half(request+14,case['requestLength']);confirmation=request+16+2*case['requestLength'];half(confirmation,case['code']^int(case['mismatch']));half(confirmation+2,case['confirmLength']);half(confirmation+4,0xa55a)
    half(base+1064,case['busy']);word(base+1060,0xc0ffee11);half(base+830,case['diag']);half(base+844,case['state']);half(base+810,case['retry']);word(0x04000210,case['irq']);before=bytes(cpu.mem_read(base,1684));queue_before=w(context.SEND+28);to_wm_before=h(base+508);requests_before=h(base+520);initial=[rng.getrandbits(32)for unused in REGISTERS];initial[-2:]=[context.base.STACK+0x3800,context.base.STOP|(index&1)];cpu.reg_write(UC_ARM_REG_CPSR,0x13|((index%4)<<6))
    for reg,value in zip(REGISTERS,initial):cpu.reg_write(reg,value)
    execute=TOP if virtual_address is None else virtual_address
    if body is not None:
        if virtual_address is None and len(body)!=720:raise ValueError('Full720-byte source extent required')
        if virtual_address is not None:cpu.mem_map(execute,0x1000)
        cpu.mem_write(execute,body)
    watched={0x037f8d58,0x037f8598,0x037fc6d4,0x037f87ac,0x037f8988}
    if selected.get('handler')is not None:watched.add(selected['handler']&~1)
    active=[];helpers=[];stores=[];owned=[];visited=[];returned=[False]
    def code(machine,pc,width,user):
        if pc==context.base.STOP:
            if active:raise ValueError('Dispatch returned with unfinished declared helper')
            returned[0]=True;machine.emu_stop();return
        if not(context.base.MAIN<=pc<context.base.MAIN+len(main)or context.base.WRAM<=pc<context.base.WRAM+len(wram)or virtual_address is not None and execute<=pc<execute+len(body)):raise ValueError('Dispatch escaped original initialized code')
        while active and pc==active[-1]['returnPc']and machine.reg_read(REGISTERS[-2])==active[-1]['sp']:
            row=active.pop();row.update(actualReturn=True,outgoingR0=machine.reg_read(REGISTERS[0]));helpers.append(row)
        if pc in watched and pc!=execute:active.append(dict(entry=hex(pc),arguments=[machine.reg_read(r)for r in REGISTERS[:4]],returnPc=machine.reg_read(REGISTERS[-1])&~1,sp=machine.reg_read(REGISTERS[-2])))
        visited.append(pc)
    def write(machine,access,address,width,value,user):
        if context.base.STACK<=address<context.base.STACK+0x4000:return
        row=[address,width,value&((1<<(8*width))-1)];stores.append(row)
        if execute<=machine.reg_read(UC_ARM_REG_PC)<execute+(720 if body is None else len(body)):owned.append(row)
    tokens=[cpu.hook_add(UC_HOOK_CODE,code),cpu.hook_add(UC_HOOK_MEM_WRITE,write)]
    try:cpu.emu_start(execute,context.base.STOP+4,count=budget)
    except Exception as error:return dict(actualOwnReturn=False,error=str(error),pc=hex(cpu.reg_read(UC_ARM_REG_PC)),postFaultCredit=0,sourceCredit=0)
    finally:
        for token in tokens:cpu.hook_del(token)
    if not returned[0]:return dict(actualOwnReturn=False,error='instruction bound exhausted',pc=hex(cpu.reg_read(UC_ARM_REG_PC)),postFaultCredit=0,sourceCredit=0)
    checks=dict(calleeSaved=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in list(range(4,12))+[13,14]),cpuModeAndIrqControl=(cpu.reg_read(UC_ARM_REG_CPSR)&255)==(0x13|((index%4)<<6)|(32 if index&1 else 0)),irqEnableRestored=w(0x04000210)==case['irq']);expected_result=None;expected_length=None
    if case['busy']:checks['busyEarlyReturnWritesNothing']=not stores and bytes(cpu.mem_read(base,1684))==before
    elif request is None:checks.update(emptyHeadSentinel=w(base+1060)==0xffffffff,noRemainingRequest=h(base+520)==0,noDelivery=not helpers)
    else:
        expected_result=6 if case['diag']else 13 if case['mismatch']else selected['error'];expected_length=1 if case['diag']or not case['mismatch']and selected['error']else case['confirmLength'];called_handler=not(case['diag']or case['mismatch']or selected['error'])
        if called_handler:
            expected_result=0 if case['code']in(0x282,0x284)else 3
            if case['code']in(0x282,0x284):expected_length=2;checks['actualGetterPayload']=h(confirmation+6)==(case['retry']if case['code']==0x282 else h(base+814))
        successful_send=not to_wm_before and queue_before<case['sendCapacity'];remaining=requests_before-1;expected_head=allocations[1]if remaining else 0xffffffff
        checks.update(currentRequestPointer=w(base+1060)==request,synchronousBusyCleared=h(base+1064)==0,confirmationResult=h(confirmation+4)==expected_result,confirmationLength=h(confirmation+2)==expected_length,confirmationCodePreserved=h(confirmation)==case['code']^int(case['mismatch']),requestCount=h(base+520)==remaining,requestHead=w(base+512)==expected_head,requestTail=w(base+516)==expected_head,toWmCount=h(base+508)==to_wm_before+int(not successful_send),sendQueueCount=w(context.SEND+28)==queue_before+int(successful_send),requestOwnershipFlag=h(request+8)==(0 if successful_send else 11),actualDeliveryCall=any(r['entry']=='0x37f8d58'and r['arguments'][:2]==[base+512,request]for r in helpers))
        adds=[r['arguments'][:2]for r in helpers if r['entry']=='0x37f8598'];expected_adds=([[2,19]]if to_wm_before else[])+([[2,11]]if remaining else[]);checks['actualFollowupTaskOrder']=adds==expected_adds
        if successful_send:checks['actualQueuedFullPointer']=w(context.base.DATA+0x6800+4*queue_before)==request
        if selected.get('handler')is not None:checks['handlerCallOnlyAfterAllDispatchValidation']=any(r['entry']==hex(selected['handler']&~1)for r in helpers)==called_handler
    return dict(actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,expectedResult=expected_result,expectedConfirmLength=expected_length,selectedOriginalTable=selected,requestAddress=None if request is None else hex(request),confirmationAddress=None if confirmation is None else hex(confirmation),registers=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),pc=cpu.reg_read(UC_ARM_REG_PC),orderedNonstackWrites=stores,ownedNonstackWrites=owned,actualDeclaredHelperReturns=helpers,actualSetupEntryReturns=stages,visited=sorted(set(p for p in visited if execute<=p<execute+(720 if body is None else len(body)))),instructions=len(visited),memorySha256={hex(a):hashlib.sha256(cpu.mem_read(a,length)).hexdigest()for a,length in meta['regions'].items()},sourceLinkedProducers=meta['sourceLinkedProducers'],syntheticBeforeEntryBindings=meta['syntheticBeforeEntryBindings'],providerReplacements=[],sourceCredit=0,unsupportedAsyncHandlerAndTableEqualityAndRealSchedulerPaths=True)

def cases():
    base=dict(mode=0,contextOffset=0,busy=0,requests=1,queuedToWm=0,diag=0,mismatch=False,code=0x282,requestLength=0,confirmLength=128,state=16,retry=0,irq=0xffffffff,sendCapacity=2,prefillSend=0);rows=[]
    rows.extend(dict(base,busy=b,requests=n)for b,n in itertools.product((0,1,2,65535),(0,1,2))if b or not n)
    rows.extend(dict(base,diag=d,mismatch=m,code=0x282,queuedToWm=q,requests=n,prefillSend=f)for d,m,q,n,f in itertools.product((0,1,65535),(False,True),(0,1),(1,2),(0,2))if d or m)
    for group,(address,count,low,minimum)in TABLES.items():
        for state in sorted({0,15,16,31,32,63,64,65,65535}):
            rows.extend([dict(base,code=group+count+1,state=state),dict(base,code=group,state=state,requestLength=0,confirmLength=0)])
    rows.extend(dict(base,code=c,state=s,retry=v,requests=n,queuedToWm=q,prefillSend=f,contextOffset=o)for c,s,v,n,q,f,o in itertools.product((0x282,0x284,0x288,0x291,0x300),(0,16,32,64,65535),(0,65535),(1,2),(0,1),(0,2),(0,4)))
    return rows
