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

TOP=0x027f2180
WATCH={0x037f8908:'ReleaseHeapBuf',0x027eb90c:'CAM_Search',0x027ebfec:'CAM_GetStaState',0x027f2000:'IsExistManFrame',0x027f16b0:'MakeDisAssFrame',0x027f1ec8:'MakeDeAuthFrame',0x027f1088:'TxManCtrlFrame',0x027ebd58:'CAM_SetPowerMgtMode',0x027ec08c:'CAM_GetLastSeqCtrl',0x027ea0ec:'WSetMacAdrs1',0x027e9cc0:'WSetPowerState',0x027ebd38:'CAM_SetRSSI',0x027ebe58:'CAM_SetLastSeqCtrl',0x027ebe98:'CAM_UpdateLifeTime',0x037f8d58:'SendMessageToWmDirect',0x037f8598:'AddTask'}

def half(cpu,a,v):cpu.mem_write(a,struct.pack('<H',v&65535))
def word(cpu,a,v):cpu.mem_write(a,struct.pack('<I',v&0xffffffff))
def h(cpu,a):return int.from_bytes(cpu.mem_read(a,2),'little')
def w(cpu,a):return int.from_bytes(cpu.mem_read(a,4),'little')

def prepare(main,wram,case,index,linked_bodies=None):
    if case['mode']not in range(4)or case['offset']not in(0,4)or case['packets']not in(0,1,2)or case['peerState']not in(0,32,48,64):raise ValueError('Concrete initialized modes/two-record backing/bounded real packet queue required')
    for key in('workState','control','status','mpdu','rssi','seq','lastSeq','tim','powerMode'):
        if not 0<=case[key]<=65535:raise ValueError('Actual u16 receive fields required:'+key)
    if not 0<=case['counter']<=0xffffffff:raise ValueError('Actual u32 counter seed required')
    linked.qualified(main,linked_bodies)
    cpu,meta=context.setup(main,wram,index,mode=case['mode'],offset=case['offset'],heap=True,bodies=linked_bodies);base=meta['context'];cam=w(cpu,base+0x31c);peer=bytes([0x12,0x34,0x56,0x78,0x9a,0xbc])if case['peerMatches']else bytes([0x22,0x44,0x66,0x88,0xaa,0xcc]);cpu.mem_write(context.base.DATA+0x6b00,peer);registered=linked.call(cpu,0x027eb9b4,[context.base.DATA+0x6b00],meta,linked_bodies);meta['prerequisiteReturns'].append(dict(name='actual-peer-cam-registration',**registered))
    if registered['outgoingR0']!=1:raise ValueError('Original registration must establish station1 in two-record fixture')
    meta['prerequisiteReturns'].append(dict(name='actual-peer-station-setter',**context.base.call(cpu,0x027ebc50,[1,case['peerState']])));sa=bytes([0x12,0x34,0x56,0x78,0x9a,0xbc]);cpu.mem_write(cam+28+4,sa if case['peerMatches']else bytes([0x22,0x44,0x66,0x88,0xaa,0xcc]));half(cpu,cam+28+20,case['lastSeq']);half(cpu,base+844,case['workState']);half(cpu,base+972,1);half(cpu,base+978,case['tim']);half(cpu,base+850,case['powerMode'])
    for a in(1376,1380,1384,1400):word(cpu,base+a,case['counter'])
    packets=[]
    for unused in range(case['packets']):
        allocation=context.base.call(cpu,0x037f886c,[base+452,384]);meta['prerequisiteReturns'].append(dict(name='actual-rx-data-buffer-allocation',**allocation));packet=allocation['outgoingR0']
        if not packet:raise ValueError('Original bounded receive-data allocation failed')
        cpu.mem_write(packet+12,bytes(128));packets.append(packet)
    frame=packets[0]+16 if packets else None
    if frame is not None:
        for offset,value in((8,case['status']),(16,case['mpdu']),(18,case['rssi']),(20,case['control']),(42,case['seq'])):half(cpu,frame+offset,value)
        cpu.mem_write(frame+24,bytes([0x11 if case['firstMulticast']else 0x10,2,3,4,5,6]));cpu.mem_write(frame+30,sa);cpu.mem_write(frame+36,bytes([0x21 if case['thirdMulticast']else 0x20,0x42,0x63,0x84,0xa5,0xc6]))
    return cpu,meta,dict(packets=packets,frame=frame,cam=cam)

def run(main,wram,case,index,body=None,virtual_address=None,linked_bodies=None):
    cpu,meta,args=prepare(main,wram,case,index,linked_bodies);base=meta['context'];frame=args['frame'];execute=TOP if virtual_address is None else virtual_address;extent=720 if body is None else len(body)
    if body is not None:
        if virtual_address is None and len(body)!=720 or virtual_address is not None and not 0<len(body)<=4096:raise ValueError('Complete source extent or bounded compiled wrong-source mapping required')
        if virtual_address is not None:cpu.mem_map(execute,4096)
        cpu.mem_write(execute,body)
    rng=random.Random(0x382000+index);initial=[rng.getrandbits(32)for unused in REGISTERS];initial[-2:]=[context.base.STACK+0x3800,context.base.STOP];cpsr=0x13|((index%4)<<6);cpu.reg_write(UC_ARM_REG_CPSR,cpsr)
    for reg,value in zip(REGISTERS,initial):cpu.reg_write(reg,value)
    active=[];helpers=[];writes=[];own=[];visited=[];returned=[False];boundary=[None]
    def code(machine,pc,width,user):
        while active and pc==active[-1]['returnPc']and machine.reg_read(REGISTERS[-2])==active[-1]['sp']:
            r=active.pop();r.update(actualReturn=True,outgoingR0=machine.reg_read(REGISTERS[0]));helpers.append(r)
        if pc==context.base.STOP:
            if active:raise ValueError('Receive task returned with an unfinished helper')
            returned[0]=True;machine.emu_stop();return
        if not(context.base.MAIN<=pc<context.base.MAIN+len(main)or context.base.WRAM<=pc<context.base.WRAM+len(wram)or virtual_address is not None and execute<=pc<execute+extent):raise ValueError('Receive-data task escaped initialized code')
        if pc==0x027ebfec and machine.reg_read(REGISTERS[0])>=2:
            boundary[0]=dict(kind='unsupported-native-callee-input',callee='0x27ebfec',index=machine.reg_read(REGISTERS[0]),initializedCamRecords=2);machine.emu_stop();return
        if virtual_address is None and TOP+716<=pc<TOP+720:raise ValueError('Receive data task fetched its literal pool')
        if pc in WATCH:active.append(dict(name=WATCH[pc],entry=hex(pc),arguments=[machine.reg_read(r)for r in REGISTERS[:4]],returnPc=machine.reg_read(REGISTERS[-1])&~1,sp=machine.reg_read(REGISTERS[-2])))
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
    if not returned[0]:return dict(case=case,actualOwnReturn=False,error=error or('explicit-callee-boundary-stop'if boundary[0]else'instruction-bound exhaustion'),unsupportedBoundary=boundary[0],postBoundaryStateCredit=0,pc=hex(cpu.reg_read(UC_ARM_REG_PC)),postFaultStateCredit=0,sourceCredit=0)
    named=lambda name:[r for r in helpers if r['name']==name];checks=dict(calleeSaved=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in list(range(4,12))+[13,14]),modeAndInterruptControl=(cpu.reg_read(UC_ARM_REG_CPSR)&255)==cpsr)
    counter=case['counter'];expected={a:counter for a in(1376,1380,1384,1400)};success=False;duplicate=False;tim=case['tim']
    if case['packets']and case['workState']==64:
        multicast=case['thirdMulticast']if case['control']&0x100 else case['firstMulticast'];selected=1384 if multicast else 1380;expected[selected]=(counter+1)&0xffffffff;expected[1376]=(counter+((case['status']&0xf0)>>4)-1)&0xffffffff
        if not case['control']&1:
            if case['mode']==1:success=case['peerMatches']and case['peerState']==64
            elif case['mode']in(2,3):
                success=True
                if case['powerMode']and not case['control']&0x2000:
                    if case['firstMulticast']:tim&=~1
                    elif case['mode']!=3:tim&=~2
            if success and case['seq']==case['lastSeq']:duplicate=True;success=False;expected[1400]=(counter+1)&0xffffffff
    for offset,value in expected.items():checks['counter-'+str(offset)]=w(cpu,base+offset)==value
    checks['independentTimBits']=h(cpu,base+978)==tim
    should_sleep=bool(case['packets']and case['workState']==64 and case['mode']in(2,3)and not case['control']&1 and case['powerMode']and not case['control']&0x2000 and tim==0);checks['independentPowerSaveCall']=[r['arguments'][0]for r in named('WSetPowerState')if execute<=r['returnPc']<execute+extent]==([1]if should_sleep else[])
    if not case['packets']:checks['emptyQueueNoEffects']=not writes and not helpers
    else:
        checks.update(remainingInputCount=h(cpu,base+460)==case['packets']-1,originalOwnershipTransition=bool(named('SendMessageToWmDirect'))==success,actualFreeOnRejection=bool(named('ReleaseHeapBuf'))==(not success),followupTask=[r['arguments'][:2]for r in named('AddTask')]==([[2,6]]if case['packets']>1 and case['workState']==64 else[]))
        if success:
            length=(case['mpdu']-24)&65535;checks.update(fullLengthWrap=h(cpu,frame+6)==length,indicationCode=h(cpu,args['packets'][0]+12)==0x180,indicationLength=h(cpu,args['packets'][0]+14)==((length+45)//2)&65535,fullSequenceForwarded=any(r['arguments'][:2]==[1,case['seq']]for r in named('CAM_SetLastSeqCtrl')),lowRssiForwarded=any(r['arguments'][:2]==[1,case['rssi']&255]for r in named('CAM_SetRSSI')),actualLifetimeUpdate=any(r['arguments'][0]==1 for r in named('CAM_UpdateLifeTime')))
        if case['workState']!=64:checks['unassociatedSkipsCounters']=not own
    return dict(case=case,actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,registers=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),pc=cpu.reg_read(UC_ARM_REG_PC),orderedNonstackWrites=writes,ownedNonstackWrites=own,memorySha256={hex(a):hashlib.sha256(cpu.mem_read(a,n)).hexdigest()for a,n in meta['regions'].items()},actualDeclaredHelperReturns=helpers,actualSetupEntryReturns=meta['prerequisiteReturns'],visited=sorted(set(pc for pc in visited if execute<=pc<execute+extent)),instructions=len(visited),providerReplacements=[],sourceCredit=0,sourceLinkedBodies=meta['sourceLinkedProducers'],actualSourceLinkedSetupReturns=meta.get('actualSourceLinkedSetupReturns',[]),baseInitializationRemainsOriginal=True,physicalReceiveAndConcurrentSchedulingUnproved=True)

def cases():
    base=dict(mode=0,offset=0,packets=1,peerState=64,peerMatches=True,workState=64,control=0,status=16,mpdu=24,rssi=0,seq=1,lastSeq=0,tim=3,powerMode=0,counter=0,firstMulticast=False,thirdMulticast=False);rows=[]
    rows.extend(dict(base,mode=m,offset=o,packets=n,workState=s)for m,o,n,s in itertools.product(range(4),(0,4),(0,1,2),(0,48,64)))
    rows.extend(dict(base,mode=m,offset=o,peerState=peer,peerMatches=match,control=c,seq=seq,counter=count)for m,o,peer,match,c,seq,count in itertools.product(range(4),(0,4),(0,32,48,64),(False,True),(0,1,0x100,0x300),(0,1),(0,0xffffffff)))
    rows.extend(dict(base,mode=m,control=c,firstMulticast=a,thirdMulticast=b,status=s,mpdu=length,rssi=r)for m,c,a,b,s,length,r in itertools.product((1,2,3),(0,0x100),(False,True),(False,True),(0,16,240),(0,23,24,25,65535),(0,255,65535)))
    rows.extend(dict(base,mode=m,powerMode=p,tim=t,control=c,firstMulticast=multi,packets=n)for m,p,t,c,multi,n in itertools.product((2,3),(0,1),(0,1,2,3),(0,1,0x2000),(False,True),(1,2)))
    return rows
