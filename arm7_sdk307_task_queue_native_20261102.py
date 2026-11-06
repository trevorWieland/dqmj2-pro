import copy
import hashlib
import itertools
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR
import arm7_sdk306_task_command_context_20261102 as context

SIZES={0x027e8bd0:140,0x037f8598:184,0x037f8650:120,0x037f86c8:60}
IE=0x04000210

def run(main,wram,case,index,bodies=None,body=None,virtual_address=None,budget=150000):
    top=case['entry'];size=SIZES[top]
    if case['priority']not in range(4)or case['task']not in range(24):raise ValueError('Four queue priorities and24 complete task records required')
    cpu,meta=context.setup(main,wram,index,case['mode'],case['contextOffset'],initialize_tasks=top!=0x027e8bd0,bodies=bodies,capacity=case['capacity']);base=meta['context'];stages=meta['prerequisiteReturns'];rng=random.Random(0x307000+index)
    def half(address,value):cpu.mem_write(address,struct.pack('<H',value&65535))
    def word(address,value):cpu.mem_write(address,struct.pack('<I',value&0xffffffff))
    if top==0x027e8bd0:
        if case['prefill']:cpu.mem_write(base,rng.randbytes(380))
    elif top==0x037f8598:
        if case['priority']==3:stages.append(dict(name='actual-remove-initial-idle',**context.base.call(cpu,0x037f8650,[3])))
        if case['nonempty']:stages.append(dict(name='actual-add-existing-task',**context.base.call(cpu,0x037f8598,[case['priority'],1 if case['task']!=1 else 2])))
        half(base+190+8*case['task'],case['flag']);half(base+16,case['nextPriority']);half(base+18,case['taskPriority'])
    elif top==0x037f8650:
        if case['priority']==3:stages.append(dict(name='actual-remove-initial-idle',**context.base.call(cpu,0x037f8650,[3])))
        for task in case['chain']:stages.append(dict(name='actual-populate-chain',**context.base.call(cpu,0x037f8598,[case['priority'],task])))
    elif top==0x037f86c8:
        removed=context.base.call(cpu,0x037f8650,[3]);stages.append(dict(name='actual-dispatch-pop-idle',**removed))
        if removed['outgoingR0']!=12:raise ValueError('Real original task producer did not select idle12')
        for unused in range(case['messages']):stages.append(dict(name='actual-null-message-producer',**context.base.call(cpu,0x037fc6d4,[context.RECV,0,0])))
    word(IE,case['irq']);before=context.task_state(cpu,base);thread=bytes(cpu.mem_read(base+24,164));count_before=int.from_bytes(cpu.mem_read(context.RECV+28,4),'little');initial=[rng.getrandbits(32)for unused in REGISTERS];initial[:2]=[case['priority'],case['task']];initial[-2:]=[context.base.STACK+0x3800,context.base.STOP|(index&1)];cpu.reg_write(UC_ARM_REG_CPSR,0x13|((index%4)<<6))
    for reg,value in zip(REGISTERS,initial):cpu.reg_write(reg,value)
    execute=top if virtual_address is None else virtual_address
    if body is not None:
        if virtual_address is None and len(body)!=size:raise ValueError('Complete source range required')
        if virtual_address is not None:cpu.mem_map(execute,0x1000)
        cpu.mem_write(execute,body)
    watched={0x037fb928,0x037fb8f0,0x037fc6d4,0x037fc760,0x037f8704,0x037f8598};active=[];helpers=[];stores=[];own=[];visited=[];returned=[False]
    def code(machine,pc,width,user):
        if pc==context.base.STOP:
            if active:raise ValueError('Task returned with unfinished observed native callee')
            returned[0]=True;machine.emu_stop();return
        if not(context.base.MAIN<=pc<context.base.MAIN+len(main)or context.base.WRAM<=pc<context.base.WRAM+len(wram)or virtual_address is not None and execute<=pc<execute+len(body)):raise ValueError('Task execution escaped qualified initialized code')
        while active and pc==active[-1]['returnPc']and machine.reg_read(REGISTERS[-2])==active[-1]['sp']:
            row=active.pop();row.update(actualReturn=True,outgoingR0=machine.reg_read(REGISTERS[0]));helpers.append(row)
        if pc in watched and pc!=execute:active.append(dict(entry=hex(pc),arguments=[machine.reg_read(r)for r in REGISTERS[:4]],returnPc=machine.reg_read(REGISTERS[-1])&~1,sp=machine.reg_read(REGISTERS[-2])))
        visited.append(pc)
    def write(machine,access,address,width,value,user):
        if context.base.STACK<=address<context.base.STACK+0x4000:return
        row=[address,width,value&((1<<(8*width))-1)];stores.append(row)
        if execute<=machine.reg_read(UC_ARM_REG_PC)<execute+(size if body is None else len(body)):own.append(row)
    tokens=[cpu.hook_add(UC_HOOK_CODE,code),cpu.hook_add(UC_HOOK_MEM_WRITE,write)]
    try:cpu.emu_start(execute,context.base.STOP+4,count=budget)
    except Exception as error:return dict(actualOwnReturn=False,error=str(error),pc=hex(cpu.reg_read(UC_ARM_REG_PC)),postFaultCredit=0,sourceCredit=0)
    finally:
        for token in tokens:cpu.hook_del(token)
    if not returned[0]:return dict(actualOwnReturn=False,error='instruction bound exhausted',pc=hex(cpu.reg_read(UC_ARM_REG_PC)),postFaultCredit=0,sourceCredit=0)
    after=context.task_state(cpu,base);expected=copy.deepcopy(before);expected_return=None;checks=dict(calleeSaved=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in list(range(4,12))+[13,14]),cpuModeAndIrqControl=(cpu.reg_read(UC_ARM_REG_CPSR)&255)==(0x13|((index%4)<<6)|(32 if index&1 else 0)),irqEnableRestored=int.from_bytes(cpu.mem_read(IE,4),'little')==case['irq'])
    if top==0x027e8bd0:
        functions=struct.unpack('<24I',main[context.TASK_TABLE-context.base.MAIN:context.TASK_TABLE-context.base.MAIN+96]);expected.update(heads=[65535,65535,65535,12],tails=[65535,65535,65535,12],nextPriority=0,taskPriority=0,slots=[dict(next=65535,flag=1 if i==12 else 0,function=functions[i])for i in range(24)]);checks['opaqueThreadPreserved']=bytes(cpu.mem_read(base+24,164))==thread
    elif top==0x037f8598:
        task=case['task'];priority=case['priority']
        if before['slots'][task]['flag']==0:
            expected['slots'][task].update(flag=1,next=65535);previous=before['tails'][priority]
            if previous==65535:expected['heads'][priority]=task
            else:expected['slots'][previous]['next']=task
            expected['tails'][priority]=task
            if priority<before['nextPriority']:expected['nextPriority']=priority
        wake=case['priority']!=3 and before['taskPriority']==3;checks['wakeRegardlessOfDuplicateFlag']=any(h['entry']=='0x37fc6d4'for h in helpers)==wake;checks['queueWakeEffect']=int.from_bytes(cpu.mem_read(context.RECV+28,4),'little')==count_before+int(wake)
    elif top==0x037f8650:
        priority=case['priority'];task=before['heads'][priority];expected_return=task
        if task!=65535:
            expected['slots'][task]['flag']=0;following=before['slots'][task]['next']
            if following==65535:expected['heads'][priority]=expected['tails'][priority]=65535
            else:expected['heads'][priority]=following;expected['slots'][task]['next']=65535
        checks['fullWordSentinelOrFirstTaskReturn']=cpu.reg_read(REGISTERS[0])==expected_return
    elif top==0x037f86c8:
        expected['slots'][12].update(flag=1,next=65535);expected['heads'][3]=expected['tails'][3]=12;checks['oneNullMessageConsumed']=int.from_bytes(cpu.mem_read(context.RECV+28,4),'little')==count_before-1;checks['actualReceiveExecuteRequeue']=all(any(h['entry']==address for h in helpers)for address in('0x37fc760','0x37f8704','0x37f8598'))
    checks['independentCompleteTaskGraph']=after==expected
    return dict(actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,beforeTaskState=before,afterTaskState=after,expectedTaskState=expected,expectedReturn=expected_return,registers=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),pc=cpu.reg_read(UC_ARM_REG_PC),orderedNonstackWrites=stores,ownedNonstackWrites=own,actualDeclaredHelperReturns=helpers,actualSetupEntryReturns=stages,visited=sorted(set(p for p in visited if execute<=p<execute+(size if body is None else len(body)))),instructions=len(visited),memorySha256={hex(a):hashlib.sha256(cpu.mem_read(a,length)).hexdigest()for a,length in meta['regions'].items()},sourceLinkedProducers=meta['sourceLinkedProducers'],syntheticBeforeEntryBindings=meta['syntheticBeforeEntryBindings'],providerReplacements=[],sourceCredit=0,sceneSchedulerAndBlockingWaitCompletionUnproved=True)

def cases():
    base=dict(mode=0,contextOffset=0,priority=0,task=0,capacity=16,prefill=False,nonempty=False,flag=0,nextPriority=0,taskPriority=0,chain=[],messages=1,irq=0);rows=[]
    rows.extend(dict(base,entry=0x027e8bd0,mode=m,contextOffset=o,prefill=p)for m,o,p in itertools.product((0,1,2,3),(0,4),(False,True)))
    rows.extend(dict(base,entry=0x037f8598,priority=p,task=t,nonempty=n,flag=f,nextPriority=np,taskPriority=tp,irq=0xffffffff)for p,t,n,f,np,tp in itertools.product(range(4),(0,11,12,23),(False,True),(0,1,2,65535),(0,3,65535),(0,3)))
    rows.extend(dict(base,entry=0x037f8650,priority=p,chain=chain,irq=i)for p,chain,i in itertools.product(range(4),([], [0],[0,23],[0,11,23]),(0,0x01000010,0xffffffff)))
    rows.extend(dict(base,entry=0x037f86c8,capacity=c,messages=n,irq=0xffffffff)for c in(1,2,16)for n in sorted({1,c}))
    return rows
