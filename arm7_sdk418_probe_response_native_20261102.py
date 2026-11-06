import hashlib
import itertools
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR,UC_ARM_REG_PC
import arm7_sdk306_task_command_context_20261102 as context
from arm7_sdk417_mp_key_native_20261102 import half,word,h,w
from project import ROOT

TOP=0x027f31fc
WATCH={0x027ea480:'MatchMacAdrs',0x037fdf74:'MIi_CpuClear16',0x037fdfd0:'MIi_CpuClear32',0x027f3c1c:'ElementChecker',0x027ead5c:'WL_ReadByte',0x027ea0ec:'WSetMacAdrs1',0x027ead30:'WL_WriteByte',0x027eabec:'ClearTimeOut',0x037f8598:'AddTask'}

def prepare(main,wram,case,index):
    if case['mode']not in range(4)or case['offset']not in(0,4)or case['state']not in(0,0x13)or case['bodyLength']not in(12,14,15)or case['mask']not in('none','match','miss')or case['existing']not in('none','match','miss')or case['maxLength']not in(0,32,33,64,65535):raise ValueError('Bounded scan context required')
    cpu,meta=context.setup(main,wram,index,mode=case['mode'],offset=case['offset'],heap=True);base=meta['context'];r=context.base.call(cpu,0x037f886c,[base+476,384]);meta['prerequisiteReturns'].append(dict(name='actual-management-frame-allocation',**r));block=r['outgoingR0']
    if not block:raise ValueError('Actual frame allocation failed')
    cpu.mem_write(block+12,bytes([0xa5])*352);frame=block+16;bssid=bytes([0x20,0x42,0x64,0x86,0xa8,0xca]);other=bytes([0x22,0x44,0x66,0x88,0xaa,0xcc]);cpu.mem_write(frame+36,bssid);half(cpu,frame+6,case['bodyLength']);half(cpu,frame+8,0x8000);half(cpu,frame+18,0x12ab);half(cpu,frame+52,0x1234);half(cpu,frame+54,0x4321);element=case.get('element','unknown');ie=bytes([88,0])if element=='unknown'else(bytes([0,0])if element=='empty'else bytes([0,1,88 if element=='X'else 89]));cpu.mem_write(frame+56,ie);req=context.base.DATA+0x1c00;cfm=context.base.DATA+0x1800;check=context.base.DATA+0x1f00;cpu.mem_write(req,bytes(84));cpu.mem_write(cfm,bytes([0xa5])*256);half(cpu,req+76,case['mask']!='none');cpu.mem_write(req+78,bssid if case['mask']=='match'else other);half(cpu,cfm+2,4);half(cpu,cfm+6,0x40);half(cpu,cfm+8,case['existing']!='none');half(cpu,cfm+10,34);cpu.mem_write(cfm+14,bssid if case['existing']=='match'else other);half(cpu,base+1028,case['state']);word(cpu,base+1052,req);word(cpu,base+1056,cfm);half(cpu,base+1032,case['maxLength']);half(cpu,base+866,case['ssidLength']);cpu.mem_write(base+868,b'X'+bytes(31));checker=0
    if case['provided']:
        cpu.mem_write(check,bytes(44));word(cpu,check,frame+56);half(cpu,check+8,len(ie));half(cpu,check+10,3);half(cpu,check+12,0x38);half(cpu,check+4,0x8000);half(cpu,check+6,0x4321);r=context.base.call(cpu,0x027f3c1c,[check]);meta['prerequisiteReturns'].append(dict(name='actual-element-checker-producer',**r));checker=check
    return cpu,meta,dict(frame=frame,checker=checker,cfm=cfm,bssid=bssid,oldCfm=bytes(cpu.mem_read(cfm,256)).hex(),oldMax=h(cpu,base+1032))

def run(main,wram,case,index,body=None,virtual_address=None,body_map=None):

    cpu,meta,extra=prepare(main,wram,case,index);base=meta['context'];execute=TOP if virtual_address is None else virtual_address;extent=976 if body is None else len(body)

    for address,linked in(body_map or{}).items():
        sizes={0x027f284c:1612,0x027f31fc:976,0x027f25cc:428}
        if address not in sizes or len(linked)!=sizes[address]or linked!=main[address-context.base.MAIN:address-context.base.MAIN+sizes[address]]:raise ValueError('Only freshly linked complete exact receive definitions may be installed')
        cpu.mem_write(address,linked)
    if body is not None:

        if virtual_address is None and len(body)!=976 or virtual_address is not None and not 0<len(body)<=4096:raise ValueError('Complete976 source or bounded freshly compiled wrong source required')

        if virtual_address is not None:cpu.mem_map(execute,4096)

        cpu.mem_write(execute,body)

    rng=random.Random(0x417000+index);initial=[rng.getrandbits(32)for unused in REGISTERS];initial[:2]=[extra['frame'],extra['checker']];initial[-2:]=[context.base.STACK+0x3800,context.base.STOP];cpsr=0x13|((index%4)<<6);cpu.reg_write(UC_ARM_REG_CPSR,cpsr)

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

    expected=bytearray.fromhex(extra['oldCfm']);early=case['state']!=0x13;masked=not early and case['mask']=='match';duplicate=not early and not masked and case['existing']=='match';entered=not early and not masked and not duplicate;long=case['bodyLength']>12;element=case.get('element','unknown');length=33 if element=='unknown'else 32;match=element in('unknown','X')or case['ssidLength']==0;accepted=entered and long and match and case['maxLength']>=length;target=10+(68 if case['existing']=='miss'else 0)
    if masked:struct.pack_into('<H',expected,6,0x41)
    if entered:
        expected[target:target+64]=bytes(64)
        if long:
            struct.pack_into('<H',expected,target,length)
            if accepted:
                struct.pack_into('<H',expected,target+44,0x4321);expected[target+4:target+10]=extra['bssid'];struct.pack_into('<H',expected,target+50,0x1234);struct.pack_into('<H',expected,target+2,0xab);struct.pack_into('<H',expected,target+62,int(element=='unknown'));
                if element=='unknown':expected[target+64:target+66]=bytes([88,0])
                elif element in('X','Y'):struct.pack_into('<H',expected,target+10,1);expected[target+12]=88 if element=='X'else 89
                struct.pack_into('<H',expected,2,4+length);struct.pack_into('<H',expected,8,int(case['existing']!='none')+1)
    state=0x15 if accepted and case['maxLength']-length<32 else case['state'];maximum=case['maxLength']-length if accepted else case['maxLength'];checks=dict(calleeSaved=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in list(range(4,12))+[13,14]),modeAndInterruptControl=(cpu.reg_read(UC_ARM_REG_CPSR)&255)==cpsr,completeConfirmationAndGuards=bytes(cpu.mem_read(extra['cfm'],256))==expected,state=h(cpu,base+1028)==state,remainingMax=h(cpu,base+1032)==maximum)
    if early or duplicate:checks['earlyNoEffects']=not writes
    return dict(case=case,actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,confirmation=bytes(cpu.mem_read(extra['cfm'],256)).hex(),expectedConfirmation=expected.hex(),registers=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),pc=cpu.reg_read(UC_ARM_REG_PC),orderedNonstackWrites=writes,ownedNonstackWrites=own,memorySha256={hex(a):hashlib.sha256(cpu.mem_read(a,n)).hexdigest()for a,n in meta['regions'].items()},actualDeclaredHelperReturns=helpers,actualSetupEntryReturns=meta['prerequisiteReturns'],visited=sorted(set(pc for pc in visited if execute<=pc<execute+extent)),instructions=len(visited),providerReplacements=[],sourceCredit=0,physicalScanReachabilityUnproved=True)

def cases():
    rows=[]
    for mode,offset,state,mask,existing,length,provided,maximum,ssid in itertools.product(range(4),(0,4),(0,0x13),('none','match','miss'),('none','match','miss'),(12,14),(False,True),(0,32,33,64,65535),(0,1)):
        rows.append(dict(mode=mode,offset=offset,state=state,mask=mask,existing=existing,bodyLength=length,provided=provided,maxLength=maximum,ssidLength=ssid))
    for mode,offset,provided,maximum,ssid,element in itertools.product(range(4),(0,4),(False,True),(0,32,33,64,65535),(0,1),('X','Y','empty')):
        rows.append(dict(mode=mode,offset=offset,state=0x13,mask='none',existing='none',bodyLength=14 if element=='empty'else 15,provided=provided,maxLength=maximum,ssidLength=ssid,element=element))
    return rows
