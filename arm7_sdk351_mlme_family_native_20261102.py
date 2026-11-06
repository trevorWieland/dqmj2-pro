import hashlib
import itertools
import json
import random
from pathlib import Path
import match_runtime
from match_runtime import REGISTERS
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR,UC_ARM_REG_PC
import arm7_sdk345_mlme_task_native_20261102 as tasks
import prove_arm7_sdk340_mlme_timeout_callback_scope_20261102 as scope

context=scope.context
SIZES=dict(tasks.SIZES,**{})
SIZES.update({e['address']:e['bytes']for e in scope.ENTRIES})

def cases():
    rows=tasks.cases()
    for entry in scope.ENTRIES:
        if entry['task']==0:domains=itertools.product((0,1,65535),(0,1,65535),(0,1,65535),(0,15,16,65535),(0,2),(0,4))
        else:domains=itertools.product((0,1,65535),(0,2),(0,4),(0,1,0xffffffff))
        for values in domains:
            if entry['task']==0:elapsed,period,maximum,channel,mode,offset=values;seed=0x5555;argument=(len(rows)*0x1234567)&0xffffffff
            else:seed,mode,offset,argument=values;elapsed=1;period=1;maximum=1;channel=0
            rows.append(dict(entry=entry['address'],elapsed=elapsed,period=period,maximum=maximum,channel=channel,mode=mode,offset=offset,seed=seed,argument=argument,state=0x13 if entry['task']==0 else 0xffff))
    return rows

def run(main,wram,case,index,body=None,virtual_address=None,linked_bodies=None):
    if case.get('entry')not in SIZES or case.get('mode')not in(0,2)or case.get('offset')not in(0,4):raise ValueError('Only the five qualified entries and explicit initialized context modes/offsets are supported')
    for field in(('state','result','channelCount','elapsed','period','scanType')if case['entry']in tasks.SIZES else('state','seed','channel','elapsed','period','maximum')):
        if not isinstance(case.get(field),int)or not 0<=case[field]<=65535:raise ValueError('Physical halfword input contract differs:'+field)
    if case['entry']==0x027ed220 and(case['channel']not in range(256)or case['state']==17 and case['channelCount']>=16):raise ValueError('Complete sixteen-byte channel-list bounds required')
    if virtual_address not in(None,0x02680000):raise ValueError('Only explicit diagnostic wrong-C output region allowed')
    if case['entry']in tasks.SIZES:return tasks.run(main,wram,case,index,body,virtual_address,linked_bodies)
    entry=next(e for e in scope.ENTRIES if e['address']==case['entry']);cpu,meta=scope.setup(main,wram,case,index);base=meta['context'];top=case['entry'];execute=top if virtual_address is None else virtual_address
    for entry_address,closed in(linked_bodies or{}).items():
        if SIZES.get(entry_address)!=len(closed)or main[entry_address-scope.context.base.MAIN:entry_address-scope.context.base.MAIN+len(closed)]!=closed:raise ValueError('Only complete exact selected source bodies may be linked into native fixture')
        cpu.mem_write(entry_address,closed)
    if body is not None:
        if len(body)!=entry['bytes']:raise ValueError('Complete callback source extent required')
        if virtual_address is not None:cpu.mem_map(virtual_address,0x1000)
        cpu.mem_write(execute,body)
    rng=random.Random(0x351000+index);initial=[rng.getrandbits(32)for unused in REGISTERS];initial[0]=case['argument'];initial[-2:]=[scope.context.base.STACK+0x3800,scope.context.base.STOP];cpsr=0x13|((index%4)<<6);cpu.reg_write(UC_ARM_REG_CPSR,cpsr)
    for reg,value in zip(REGISTERS,initial):cpu.reg_write(reg,value)
    helpers=[];active=[];visited=[];stores=[];own=[];returned=[False]
    def code(machine,pc,width,user):
        while active and pc==active[-1]['returnPc']and machine.reg_read(REGISTERS[-2])==active[-1]['sp']:
            r=active.pop();r.update(actualReturn=True,outgoingR0=machine.reg_read(REGISTERS[0]));helpers.append(r)
        if pc==scope.context.base.STOP:
            if active:raise ValueError('Callback tail helper unfinished')
            returned[0]=True;machine.emu_stop();return
        if not(scope.context.base.MAIN<=pc<scope.context.base.MAIN+len(main)or scope.context.base.WRAM<=pc<scope.context.base.WRAM+len(wram)or virtual_address is not None and execute<=pc<execute+len(body)):raise ValueError('Callback escaped measured initialized code')
        if pc==0x037f8598:active.append(dict(entry=hex(pc),arguments=[machine.reg_read(r)for r in REGISTERS[:4]],sp=machine.reg_read(REGISTERS[-2]),returnPc=machine.reg_read(REGISTERS[-1])&~1))
        if execute<=pc<execute+entry['bytes']:visited.append(pc)
    def write(machine,access,a,width,value,user):
        if scope.context.base.STACK<=a<scope.context.base.STACK+0x4000:return
        r=[a,width,value&((1<<(8*width))-1)];stores.append(r)
        if execute<=machine.reg_read(UC_ARM_REG_PC)<execute+entry['bytes']:own.append(r)
    hooks=[cpu.hook_add(UC_HOOK_CODE,code),cpu.hook_add(UC_HOOK_MEM_WRITE,write)];error=None
    try:cpu.emu_start(execute,scope.context.base.STOP+4,count=10000)
    except Exception as exc:error=type(exc).__name__+':'+str(exc)
    finally:
        for token in hooks:cpu.hook_del(token)
    if not returned[0]:return dict(actualOwnReturn=False,error=error or'instruction-bound exhaustion',pc=hex(cpu.reg_read(UC_ARM_REG_PC)),postFaultStateCredit=0,sourceCredit=0)
    expected=[];state=case['state']
    if entry['task']==0:
        elapsed=(case['elapsed']+case['period'])&65535;expected.append([base+0x40e,2,elapsed])
        if elapsed>=case['maximum']:state=17 if case['channel']<16 else 21;expected.append([base+0x404,2,state])
    elif entry['task']==1:expected.extend([[base+0x408,2,7],[base+0x404,2,37]]);state=37
    else:expected.append([base+0x404,2,131]);state=131
    reference,rmeta=scope.setup(main,wram,case,index);reference.reg_write(UC_ARM_REG_CPSR,cpsr)
    for a,width,value in expected:reference.mem_write(a,value.to_bytes(width,'little'))
    api=scope.context.base.call(reference,0x037f8598,[2,entry['task']],10000);same=all(bytes(cpu.mem_read(a,n))==bytes(reference.mem_read(a,n))for a,n in meta['regions'].items()if a!=scope.context.base.STACK);task=scope.context.task_state(cpu,base);checks=dict(calleeSaved=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in list(range(4,12))+[13,14]),modeAndInterruptControl=(cpu.reg_read(UC_ARM_REG_CPSR)&255)==cpsr,orderedOwnWrites=own==expected,independentAllNonstackMemory=same,forwardedTask=[r['arguments'][:2]for r in helpers]==[[2,entry['task']]],state=scope.gethalf(cpu,base+0x404)==state,actualEnqueuedSlot=task['slots'][entry['task']]['flag']==1)
    return dict(actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,registers=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),pc=cpu.reg_read(UC_ARM_REG_PC),orderedNonstackWrites=stores,ownedNonstackWrites=own,memorySha256={hex(a):hashlib.sha256(cpu.mem_read(a,n)).hexdigest()for a,n in meta['regions'].items()},visited=sorted(set(visited)),actualDeclaredHelperReturns=helpers,actualSetupEntryReturns=meta['prerequisiteReturns']+rmeta['prerequisiteReturns'],independentOriginalApiModel=dict(actualIndependentApiReturns=[api],allNonstackMemoryCompared=True),sourceCredit=0,providerReplacements=[],sourceLinkedSelectedUnits=[dict(entry=hex(a),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())for a,b in sorted((linked_bodies or{}).items())],physicalAlarmLaunchConcurrencyAndAndroidUnproved=True)
