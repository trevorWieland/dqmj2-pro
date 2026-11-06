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


TOP=0x027f25cc

WATCH={0x027ea480:'MatchMacAdrs',0x027eb90c:'CAM_Search',0x027ebfec:'CAM_GetStaState',0x027f2000:'IsExistManFrame',0x027f1ec8:'MakeDeAuthFrame',0x027f1088:'TxManCtrlFrame',0x027ebd58:'CAM_SetPowerMgtMode',0x027ebe98:'CAM_UpdateLifeTime',0x027ec0d8:'CAM_GetAID',0x027ead30:'WL_WriteByte',0x037fdf9c:'MIi_CpuCopy16'}


def half(cpu,a,v):cpu.mem_write(a,struct.pack('<H',v&65535))

def word(cpu,a,v):cpu.mem_write(a,struct.pack('<I',v&0xffffffff))

def h(cpu,a):return int.from_bytes(cpu.mem_read(a,2),'little')

def w(cpu,a):return int.from_bytes(cpu.mem_read(a,4),'little')


def prepare(main,wram,case,index):

    if case['mode']not in range(4)or case['offset']not in(0,4)or case['aid']not in range(1,16)or case['payload']not in(0,1,2,3,4,5,8)or case['stride']!=12:raise ValueError('Bounded initialized MP context, nonzero representable AID and four-byte payload required')

    cpu,meta=context.setup(main,wram,index,mode=case['mode'],offset=case['offset'],heap=True);base=meta['context'];peer=bytes([0x12,0x34,0x56,0x78,0x9a,0xbc]);bssid=bytes([0x20,0x42,0x64,0x86,0xa8,0xca]);source=context.base.DATA+0x6b00;cpu.mem_write(source,peer);r=context.base.call(cpu,0x027eb9b4,[source]);meta['prerequisiteReturns'].append(dict(name='actual-cam-registration',**r))

    if r['outgoingR0']!=1:raise ValueError('Actual station registration prerequisite failed')

    meta['prerequisiteReturns'].append(dict(name='actual-cam-state-setter',**context.base.call(cpu,0x027ebc50,[1,case['peerState']])));cam=w(cpu,base+796);half(cpu,cam+28+2,case['aid']);cpu.mem_write(base+936,bssid);blocks=[]

    for manager in(base+476,base+500):

        r=context.base.call(cpu,0x037f886c,[manager,384]);meta['prerequisiteReturns'].append(dict(name='actual-management-or-result-allocation',**r));blocks.append(r['outgoingR0'])

        if not blocks[-1]:raise ValueError('Original bounded heap allocation failed')

        cpu.mem_write(blocks[-1]+12,bytes([0xa5])*352)

    frame=blocks[0]+16;end=blocks[1];mp=end+16;half(cpu,frame+16,24+case['payload']);half(cpu,frame+18,case['rssi']);half(cpu,frame+14,case['rate']);half(cpu,frame+20,0x1000 if case['power']else 0);cpu.mem_write(frame+24,bssid if case['bssidMatches']else peer);cpu.mem_write(frame+30,peer);payload=bytes([0x11,0x22,0x33,0x44,0x55,0x66]);cpu.mem_write(frame+44,payload);half(cpu,base+1128,case['busy']);word(cpu,base+1212,end);half(cpu,base+1220,case['setMap']);half(cpu,base+1222,case['getMap']);half(cpu,mp,case['bitmap']);half(cpu,mp+6,case['stride']);slot=(case['setMap']&((1<<case['aid'])-2)).bit_count();target=mp+10+slot*12;return cpu,meta,dict(frame=frame,end=end,mp=mp,slot=slot,target=target,payload=payload,oldOutput=bytes(cpu.mem_read(mp+10,184)).hex())


def run(main,wram,case,index,body=None,virtual_address=None,body_map=None):

    cpu,meta,extra=prepare(main,wram,case,index);base=meta['context'];execute=TOP if virtual_address is None else virtual_address;extent=428 if body is None else len(body)

    for address,linked in(body_map or{}).items():
        sizes={0x027f284c:1612,0x027f31fc:976,0x027f25cc:428}
        if address not in sizes or len(linked)!=sizes[address]or linked!=main[address-context.base.MAIN:address-context.base.MAIN+sizes[address]]:raise ValueError('Only freshly linked complete exact receive definitions may be installed')
        cpu.mem_write(address,linked)
    if body is not None:

        if virtual_address is None and len(body)!=428 or virtual_address is not None and not 0<len(body)<=4096:raise ValueError('Complete428 source or bounded freshly compiled wrong source required')

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

    bit=1<<case['aid'];accepted=bool(case['busy']and case['bssidMatches']and case['payload']<=4 and case['peerState']==64 and not(case['getMap']&bit)and(case['setMap']&bit));checks=dict(calleeSaved=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in list(range(4,12))+[13,14]),modeAndInterruptControl=(cpu.reg_read(UC_ARM_REG_CPSR)&255)==cpsr,getBitmap=h(cpu,base+1222)==(case['getMap']|bit if accepted else case['getMap']),resultBitmap=h(cpu,extra['mp'])==(case['bitmap']&~bit if accepted else case['bitmap']));expected=bytearray.fromhex(extra['oldOutput'])

    if accepted:

        start=extra['slot']*12;struct.pack_into('<H',expected,start,case['payload']);expected[start+2]=case['rate']&255;expected[start+3]=case['rssi']&255;count=(case['payload']+2)//2*2 if case['payload']else 0;expected[start+8:start+8+count]=extra['payload'][:count]

    checks['allSlotsAndPadding']=bytes(cpu.mem_read(extra['mp']+10,184))==expected

    if not case['busy']or not case['bssidMatches']:checks['earlyGateNoEffects']=not writes

    return dict(case=case,actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,registers=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),pc=cpu.reg_read(UC_ARM_REG_PC),orderedNonstackWrites=writes,ownedNonstackWrites=own,memorySha256={hex(a):hashlib.sha256(cpu.mem_read(a,n)).hexdigest()for a,n in meta['regions'].items()},actualDeclaredHelperReturns=helpers,actualSetupEntryReturns=meta['prerequisiteReturns'],visited=sorted(set(pc for pc in visited if execute<=pc<execute+extent)),instructions=len(visited),providerReplacements=[],sourceCredit=0,physicalMultiplayerAndPeerLegitimacyUnproved=True)


def cases():

    base=dict(mode=0,offset=0,aid=1,payload=0,stride=12,peerState=64,rssi=0,rate=0,power=False,bssidMatches=True,busy=1,setMap=65534,getMap=0,bitmap=65535);rows=[]

    for mode,offset,aid,payload,busy,match,peer,duplicate,poll in itertools.product((0,1,2,3),(0,4),(1,2,15),(0,1,2,3,4,5,8),(0,1),(False,True),(32,64),(False,True),(False,True)):

        bit=1<<aid;rows.append(dict(base,mode=mode,offset=offset,aid=aid,payload=payload,busy=busy,bssidMatches=match,peerState=peer,getMap=bit if duplicate else 0,setMap=65534 if poll else 65534&~bit,rssi=65535,rate=0x12ab,power=bool(offset)))

    return rows

