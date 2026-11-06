import hashlib
import itertools
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR,UC_ARM_REG_PC
import arm7_sdk306_task_command_context_20261102 as context
import arm7_sdk397_compiled_cam_context_20261102 as linked
from project import ROOT

SIZES={0x027eb90c:168,0x027eb9b4:320,0x027ec5a4:228}
WATCH={0x027ea480:'MatchMacAdrs',0x027ec5a4:'CAM_InitElement',0x027ebd58:'CAM_SetPowerMgtMode',0x027ea0ec:'WSetMacAdrs1',0x027ebc50:'CAM_SetStaState'}

def half(cpu,a,v):cpu.mem_write(a,struct.pack('<H',v&65535))
def h(cpu,a):return int.from_bytes(cpu.mem_read(a,2),'little')
def w(cpu,a):return int.from_bytes(cpu.mem_read(a,4),'little')

def prepare(main,wram,case,index,linked_bodies=None):
    if case['entry']not in SIZES or case['mode']not in range(4)or case['offset']not in(0,4)or case['slot']not in(0,1):raise ValueError('Exact CAM APIs and two initialized records required')
    for key in('count','state','frameCount','life','maxLife','support'):
        if not 0<=case[key]<=65535:raise ValueError('Physical u16 CAM fields required:'+key)
    linked.qualified(main,linked_bodies)
    cpu,meta=context.setup(main,wram,index,mode=case['mode'],offset=case['offset'],heap=True,bodies=linked_bodies);base=meta['context'];cam=w(cpu,base+0x31c);mac=bytes([0x13 if case['multicast']else 0x12,0x34,0x56,0x78,0x9a,0xbc]);source=context.base.DATA+0x6b00;cpu.mem_write(source,mac);slot=case['slot']if case['entry']==0x027ec5a4 else 1;record=cam+28*slot;cpu.mem_write(record,bytes([0xa5])*28);half(cpu,record,case['state']);half(cpu,record+22,case['frameCount']);half(cpu,record+24,case['life']);half(cpu,record+26,case['maxLife']);cpu.mem_write(record+4,mac if case['matching']else bytes([0x22,0x44,0x66,0x88,0xaa,0xcc]));half(cpu,base+0x52c,case['count']);half(cpu,base+934,case['support']);args=[slot,source]if case['entry']==0x027ec5a4 else[source];return cpu,meta,args,dict(record=record,mac=mac,source=source,oldRecord=bytes(cpu.mem_read(record,28)).hex())

def run(main,wram,case,index,body=None,virtual_address=None,linked_bodies=None):
    cpu,meta,args,extra=prepare(main,wram,case,index,linked_bodies);base=meta['context'];top=case['entry'];size=SIZES[top];execute=top if virtual_address is None else virtual_address;extent=size if body is None else len(body)
    if body is not None:
        if virtual_address is None and len(body)!=size or virtual_address is not None and not 0<len(body)<=4096:raise ValueError('Complete original-sized C or bounded compiled wrong C required')
        if virtual_address is not None:cpu.mem_map(execute,4096)
        cpu.mem_write(execute,body)
    rng=random.Random(0x395000+index);initial=[rng.getrandbits(32)for unused in REGISTERS];initial[:len(args)]=args;initial[-2:]=[context.base.STACK+0x3800,context.base.STOP];cpsr=0x13|((index%4)<<6);cpu.reg_write(UC_ARM_REG_CPSR,cpsr)
    for reg,value in zip(REGISTERS,initial):cpu.reg_write(reg,value)
    active=[];helpers=[];writes=[];own=[];visited=[];returned=[False]
    def code(machine,pc,width,user):
        while active and pc==active[-1]['returnPc']and machine.reg_read(REGISTERS[-2])==active[-1]['sp']:
            r=active.pop();r.update(actualReturn=True,outgoingR0=machine.reg_read(REGISTERS[0]));helpers.append(r)
        if pc==context.base.STOP:
            if active:raise ValueError('CAM API returned with unfinished helper')
            returned[0]=True;machine.emu_stop();return
        if not(context.base.MAIN<=pc<context.base.MAIN+len(main)or context.base.WRAM<=pc<context.base.WRAM+len(wram)or virtual_address is not None and execute<=pc<execute+extent):raise ValueError('CAM API escaped initialized code')
        if virtual_address is None and top+size-4<=pc<top+size:raise ValueError('CAM API fetched its literal pool')
        if pc in WATCH and pc!=execute:active.append(dict(name=WATCH[pc],entry=hex(pc),arguments=[machine.reg_read(r)for r in REGISTERS[:4]],returnPc=machine.reg_read(REGISTERS[-1])&~1,sp=machine.reg_read(REGISTERS[-2])))
        visited.append(pc)
    def write(machine,access,a,width,value,user):
        if context.base.STACK<=a<context.base.STACK+0x4000:return
        r=[a,width,value&((1<<(8*width))-1)];writes.append(r)
        if execute<=machine.reg_read(UC_ARM_REG_PC)<execute+extent:own.append(r)
    tokens=[cpu.hook_add(UC_HOOK_CODE,code),cpu.hook_add(UC_HOOK_MEM_WRITE,write)];error=None
    try:cpu.emu_start(execute,context.base.STOP+4,count=100000)
    except Exception as e:error=type(e).__name__+':'+str(e)
    finally:
        for token in tokens:cpu.hook_del(token)
    if not returned[0]:return dict(case=case,actualOwnReturn=False,error=error or'instruction-bound exhaustion',pc=hex(cpu.reg_read(UC_ARM_REG_PC)),postFaultStateCredit=0,sourceCredit=0)
    checks=dict(calleeSaved=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in list(range(4,12))+[13,14]),modeAndInterruptControl=(cpu.reg_read(UC_ARM_REG_CPSR)&255)==cpsr);initialize=top==0x027ec5a4;expected=None
    if top!=0x027ec5a4:
        if case['multicast']:expected=0
        elif top==0x027eb90c:expected=1 if case['count']>1 and case['state']and case['matching']else 255
        elif case['count']>1 and case['state']and case['matching']:expected=1
        elif case['count']<=1 or case['state']==0 or case['state']<48 and case['frameCount']==0:expected=1;initialize=True
        else:expected=255
        checks['fullWordResult']=cpu.reg_read(REGISTERS[0])==expected
    if initialize:
        record=extra['record'];checks.update(resetState=h(cpu,record)==32,oldFreeCountWrap=h(cpu,base+0x52c)==((case['count']+int(case['state']==0))&65535),macCopied=bytes(cpu.mem_read(record+4,6))==extra['mac'],maxLifePreserved=h(cpu,record+26)==case['maxLife'],lifeFromPreservedMax=h(cpu,record+24)==case['maxLife'],sequenceSentinel=h(cpu,record+20)==65535,supportRateCopied=h(cpu,record+16)==case['support'],rssiAndCapabilityCleared=h(cpu,record+10)==0 and h(cpu,record+12)==0,frameCountCleared=h(cpu,record+22)==0)
    else:checks['noGlobalEffects']=not writes and bytes(cpu.mem_read(extra['record'],28)).hex()==extra['oldRecord']and h(cpu,base+0x52c)==case['count']
    return dict(case=case,actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,registers=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),pc=cpu.reg_read(UC_ARM_REG_PC),orderedNonstackWrites=writes,ownedNonstackWrites=own,memorySha256={hex(a):hashlib.sha256(cpu.mem_read(a,n)).hexdigest()for a,n in meta['regions'].items()},actualDeclaredHelperReturns=helpers,actualSetupEntryReturns=meta['prerequisiteReturns'],visited=sorted(set(pc for pc in visited if execute<=pc<execute+extent)),instructions=len(visited),providerReplacements=[],sourceCredit=0,sourceLinkedBodies=meta['sourceLinkedProducers'],actualSourceLinkedSetupReturns=meta.get('actualSourceLinkedSetupReturns',[]),baseInitializationRemainsOriginal=True,physicalStationLegitimacyAndConcurrentRadioUnproved=True)

def cases():
    base=dict(entry=0x027eb90c,mode=0,offset=0,slot=1,count=2,state=64,frameCount=0,life=0,maxLife=65535,support=0xffff,matching=False,multicast=False);rows=[]
    rows.extend(dict(base,mode=m,offset=o,count=c,state=s,matching=match,multicast=multi)for m,o,c,s,match,multi in itertools.product(range(4),(0,4),(0,1,2,65535),(0,16,48,64),(False,True),(False,True)))
    rows.extend(dict(base,entry=0x027eb9b4,mode=m,offset=o,count=c,state=s,matching=match,multicast=multi,frameCount=f,life=life)for m,o,c,s,match,multi,f,life in itertools.product((0,1),(0,4),(0,1,2,65535),(0,16,32,48,64),(False,True),(False,True),(0,1),(0,65535)))
    rows.extend(dict(base,entry=0x027ec5a4,mode=m,offset=o,slot=slot,count=c,state=s,maxLife=life,support=0xffff if (m+slot)%2 else 0,multicast=bool(slot),matching=False)for m,o,slot,c,s,life in itertools.product(range(4),(0,4),(0,1),(1,65535),(0,64),(0,1,65535)))
    return rows
