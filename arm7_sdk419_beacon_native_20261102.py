import hashlib
import itertools
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR,UC_ARM_REG_PC
import arm7_sdk306_task_command_context_20261102 as context
import arm7_sdk418_probe_response_native_20261102 as probe
from arm7_sdk417_mp_key_native_20261102 import half,word,h,w
from project import ROOT
TOP=0x027f284c
WATCH={0x027eb9b4:'CAM_SearchAdd',0x027ebd38:'CAM_SetRSSI',0x037fdfd0:'MIi_CpuClear32',0x027f3c1c:'ElementChecker',0x027ead5c:'WL_ReadByte',0x027f31fc:'RxProbeResFrame',0x027eabec:'ClearTimeOut',0x027e990c:'WSetChannel',0x027ebe38:'CAM_SetSupRate',0x027e91bc:'WSetActiveZoneTime',0x027e9744:'WSetDTIMPeriod',0x027e96ec:'WSetBeaconPeriod',0x027ea0ec:'WSetMacAdrs1',0x037f8598:'AddTask',0x037fdf9c:'MIi_CpuCopy16',0x027ebe98:'CAM_UpdateLifeTime',0x03806bf0:'unsigned-u64-quotient',0x037fdd00:'OS_DisableInterrupts',0x037fdd14:'OS_RestoreInterrupts',0x027f1114:'TxPsPollFrame',0x027e9cc0:'WSetPowerState',0x027edfa0:'MLME_IssueBeaconRecvIndication',0x027f4b88:'UpdateApList'}

def prepare(main,wram,case,index):
    if case['mode']not in range(4)or case['offset']not in(0,4)or case['bodyLength']not in(0,12,14)or case['period']not in(1,100,65535)or case['state']not in(0,0x13):raise ValueError('Bounded nonzero-period beacon context required')
    pcase=dict(mode=case['mode'],offset=case['offset'],state=case['state'],mask=case.get('mask','none'),existing='none',bodyLength=14 if case['bodyLength']else 12,provided=False,maxLength=case.get('maxLength',64),ssidLength=case.get('ssidLength',0));cpu,meta,e=probe.prepare(main,wram,pcase,index);base=meta['context'];peer=bytes([0x12,0x34,0x56,0x78,0x9a,0xbc]);source=context.base.DATA+0x6b00;cpu.mem_write(source,peer);r=context.base.call(cpu,0x027eb9b4,[source]);meta['prerequisiteReturns'].append(dict(name='actual-cam-registration',**r))
    if r['outgoingR0']!=1:raise ValueError('Original CAM registration failed')
    meta['prerequisiteReturns'].append(dict(name='actual-cam-state-setter',**context.base.call(cpu,0x027ebc50,[1,64])));cam=w(cpu,base+796);half(cpu,cam+28+26,0xffff);half(cpu,cam+28+24,0xffff);frame=e['frame'];cpu.mem_write(frame+30,bytes([0x22,0x44,0x66,0x88,0xaa,0xcc])if case['camFull']else peer);half(cpu,frame+6,case['bodyLength']);half(cpu,frame+2,0xa5a5);half(cpu,frame+8,0x8000 if case['bssidMatches']else 0);half(cpu,frame+18,case['rssi']);cpu.mem_write(frame+44,struct.pack('<Q',case['timestamp']));half(cpu,base+946,case['period']);half(cpu,base+964,0x1234);half(cpu,base+862,0);half(cpu,base+844,32);word(cpu,base+1392,case['counter']);half(cpu,context.base.DATA+0x1c00+56,1);e.update(camBase=cam,oldLife=h(cpu,cam+28+24),oldRssi=h(cpu,cam+28+10),oldNext=bytes(cpu.mem_read(0x048080f0,8)).hex());return cpu,meta,e

def run(main,wram,case,index,body=None,virtual_address=None,body_map=None):

    cpu,meta,extra=prepare(main,wram,case,index);base=meta['context'];execute=TOP if virtual_address is None else virtual_address;extent=1612 if body is None else len(body)

    for address,linked in(body_map or{}).items():
        sizes={0x027f284c:1612,0x027f31fc:976,0x027f25cc:428}
        if address not in sizes or len(linked)!=sizes[address]or linked!=main[address-context.base.MAIN:address-context.base.MAIN+sizes[address]]:raise ValueError('Only freshly linked complete exact receive definitions may be installed')
        cpu.mem_write(address,linked)
    if body is not None:

        if virtual_address is None and len(body)!=1612 or virtual_address is not None and not 0<len(body)<=4096:raise ValueError('Complete1612 source or bounded freshly compiled wrong source required')

        if virtual_address is not None:cpu.mem_map(execute,4096)

        cpu.mem_write(execute,body)

    rng=random.Random(0x417000+index);initial=[rng.getrandbits(32)for unused in REGISTERS];initial[0]=extra['frame'];initial[-2:]=[context.base.STACK+0x3800,context.base.STOP];cpsr=0x13|((index%4)<<6);cpu.reg_write(UC_ARM_REG_CPSR,cpsr)

    for reg,value in zip(REGISTERS,initial):cpu.reg_write(reg,value)

    active=[];helpers=[];writes=[];own=[];visited=[];returned=[False]

    def code(machine,pc,width,user):

        while active and pc==active[-1]['returnPc']and machine.reg_read(REGISTERS[-2])==active[-1]['sp']:

            r=active.pop();r.update(actualReturn=True,outgoingR0=machine.reg_read(REGISTERS[0]));helpers.append(r)

        if pc==context.base.STOP:

            if active:raise ValueError('MP receiver returned with unfinished native helper')

            returned[0]=True;machine.emu_stop();return

        if not(context.base.MAIN<=pc<context.base.MAIN+len(main)or context.base.WRAM<=pc<context.base.WRAM+len(wram)or virtual_address is not None and execute<=pc<execute+extent):raise ValueError('MP receiver escaped initialized code')

        if pc in WATCH:active.append(dict(name=WATCH[pc],entry=hex(pc),arguments=[machine.reg_read(r)for r in REGISTERS[:4]],returnPc=machine.reg_read(REGISTERS[-1])&~1,sp=machine.reg_read(REGISTERS[-2])))

        visited.append(pc)

    def write(machine,access,a,width,value,user):

        if context.base.STACK<=a<context.base.STACK+0x4000:return

        r=[a,width,value&((1<<(8*width))-1)];writes.append(r)

        if execute<=machine.reg_read(UC_ARM_REG_PC)<execute+extent:own.append(r)

    tokens=[cpu.hook_add(UC_HOOK_CODE,code),cpu.hook_add(UC_HOOK_MEM_WRITE,write)];error=None

    try:cpu.emu_start(execute,context.base.STOP+4,count=200000)

    except Exception as e:error=type(e).__name__+':'+str(e)

    finally:

        for token in tokens:cpu.hook_del(token)

    if not returned[0]:return dict(case=case,actualOwnReturn=False,error=error or'instruction-bound exhaustion',pc=hex(cpu.reg_read(UC_ARM_REG_PC)),postFaultStateCredit=0,sourceCredit=0)

    cam=255 if case['camFull']else 1;long=case['bodyLength']>12 and cam!=255;passive=long and case['state']==19;timing=long and not passive and case['bssidMatches']and case['mode']in(2,3);expected=(((case['timestamp']//(case['period']*1024))+1)*(case['period']*1024))&0xffffffffffffffff;expected|=1;raw=struct.pack('<Q',expected)if timing else bytes.fromhex(extra['oldNext']);checks=dict(calleeSaved=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in list(range(4,12))+[13,14]),modeAndInterruptControl=(cpu.reg_read(UC_ARM_REG_CPSR)&255)==cpsr,counterWrap=w(cpu,base+1392)==((case['counter']+1)&0xffffffff),frameCam=h(cpu,extra['frame']+2)==cam,rssi=h(cpu,extra['camBase']+28+10)==(extra['oldRssi']if cam==255 else case['rssi']),beaconLost=h(cpu,base+964)==(0 if timing else 0x1234),nextTimestamp=bytes(cpu.mem_read(0x048080f0,8))==raw,life=h(cpu,extra['camBase']+28+24)==extra['oldLife'])
    if passive:
        entered=case['bssidMatches']and case.get('ssidLength',0)==0;masked=entered and case.get('mask','none')=='match';accepted=entered and not masked and case.get('maxLength',64)>=33;checks['passiveConfirmationCount']=h(cpu,extra['cfm']+8)==int(accepted);checks['passiveMask']=h(cpu,extra['cfm']+6)==(0x41 if masked else 0x40);checks['passiveRemaining']=h(cpu,base+1032)==(case.get('maxLength',64)-33 if accepted else case.get('maxLength',64));checks['passiveState']=h(cpu,base+1028)==(0x15 if accepted and case.get('maxLength',64)-33<32 else 19)
    return dict(case=case,actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,registers=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),pc=cpu.reg_read(UC_ARM_REG_PC),orderedNonstackWrites=writes,ownedNonstackWrites=own,memorySha256={hex(a):hashlib.sha256(cpu.mem_read(a,n)).hexdigest()for a,n in meta['regions'].items()},actualDeclaredHelperReturns=helpers,actualSetupEntryReturns=meta['prerequisiteReturns'],visited=sorted(set(pc for pc in visited if execute<=pc<execute+extent)),instructions=len(visited),providerReplacements=[],sourceCredit=0,physicalTimingAndRFUnproved=True)

def cases():
    base=dict(mode=0,offset=0,bodyLength=14,period=100,state=0,timestamp=0,camFull=False,bssidMatches=True,rssi=0,counter=0);rows=[]
    for mode,offset,length,match,full,rssi,counter in itertools.product(range(4),(0,4),(0,12,14),(False,True),(False,True),(0,255,65535),(0,0xffffffff)):
        rows.append(dict(base,mode=mode,offset=offset,bodyLength=length,bssidMatches=match,camFull=full,rssi=rssi,counter=counter))
    for mode,offset,timestamp,period,match,rssi,counter in itertools.product((2,3),(0,4),(0,1,102399,102400,0x100000000,0xffffffffffffffff),(1,100,65535),(False,True),(255,65535),(0,0xffffffff)):
        rows.append(dict(base,mode=mode,offset=offset,timestamp=timestamp,period=period,bssidMatches=match,rssi=rssi,counter=counter))
    for mode,offset,maximum,mask,ssid,length in itertools.product(range(4),(0,4),(32,33,64),('none','match'),(0,1),(12,14)):
        rows.append(dict(base,mode=mode,offset=offset,state=19,maxLength=maximum,mask=mask,ssidLength=ssid,bodyLength=length))
    return rows
