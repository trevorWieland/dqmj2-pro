import hashlib
import itertools
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR
import arm7_sdk288_transmit_context_20261102 as context

SIZES={0x037faec0:800,0x027f0b0c:116,0x027f0c7c:100,0x027f0ce0:140,0x027f0f14:232,0x027f1114:148,0x027f11a8:64}
IE=context.HW+0x210

def run(main,wram,case,index,bindings,body=None,budget=150000,virtual_address=None):
    if case['entry']in(0x027f0c7c,0x027f0ce0)and case['priority']not in(0,1,2):raise ValueError('Fixed three-queue/three-halfword source ABI domain required')
    top=case['entry'];size=SIZES[top];execute=top if virtual_address is None else virtual_address;cpu,setup=context.setup(main,wram,index,case['mode'],initialize_transmit=top!=0x037faec0,context_offset=case['contextOffset']);base=setup['context'];stages=setup['prerequisiteReturns']
    for name,entry,args in [('os-heap-init',0x037fce24,[0,context.DATA+0x7400,context.DATA+0x8000,1]),('os-heap-create',0x037fcecc,[0,context.DATA+0x7800,context.DATA+0x8000]),('os-heap-current',0x037fcdf0,[0,0])]:stages.append(dict(name=name,**context.call(cpu,entry,args)))
    cpu.mem_write(context.DATA+0x7100,bytes(12));stages.append(dict(name='actual-complete-heap-buffer-initializer',**context.call(cpu,0x027e8c78,[context.DATA+0x7100])));rng=random.Random(0x295000+index);q=base+0x42c+20*case['priority'];frame=context.DATA+0x5100
    def half(address,value):cpu.mem_write(address,struct.pack('<H',value&65535))
    def word(address,value):cpu.mem_write(address,struct.pack('<I',value&0xffffffff))
    def h(address):return int.from_bytes(cpu.mem_read(address,2),'little')
    def w(address):return int.from_bytes(cpu.mem_read(address,4),'little')
    mode=h(base+0x350)
    if mode!=case['mode']:raise ValueError('Actual original mode setter did not produce declared raw mode')
    if top==0x037faec0:
        if case['prefill']:cpu.mem_write(base+0x42c,rng.randbytes(0xb0))
        half(base+0x334,case['wep'])
    elif top==0x027f0b0c:
        half(base+0x33a,(h(base+0x33a)&~128)|(case['nullKey']<<7));half(base+0x47c,case['busy']);half(base+0x490,case['busy']);word(IE,case['irq'])
    elif top in(0x027f0c7c,0x027f0ce0):
        half(q,case['busy']);word(q+12,frame);cpu.mem_write(frame,bytes(48));half(frame,case['frameStatus']);half(frame+4,case['retry']);half(frame+0x14,case['control']);half(frame+0xc,0xa5a5);half(frame+0x2a,0x5a5a);mac=w(q+8)
        if not context.MAC<=mac<context.MAC+0x5000:raise ValueError('Original initializer MAC frame pointer outside explicit backing')
        half(mac,case['status']);half(mac+4,case['retry']);half(mac+0x22,case['sequence']);word(IE,case['irq'])
    elif top==0x027f0f14:
        half(base+0x468,case['busy']);half(base+0x46a,case['count'])
        if case['busy']:
            allocated=context.call(cpu,0x037f886c,[base+0x188,0x80]);stages.append(dict(name='actual-live-end-record-allocation',**allocated))
            if not allocated['outgoingR0']:raise ValueError('Actual end-record allocation failed')
            word(base+0x4bc,allocated['outgoingR0'])
        if case['queued']:
            cpu.mem_write(context.DATA+0x5100,bytes.fromhex('123456789abc'));created=context.call(cpu,0x027f16b0,[context.DATA+0x5100,0x1234]);stages.append(dict(name='actual-disassociation-frame-constructor',**created))
            if not created['outgoingR0']:raise ValueError('Actual queued-frame constructor failed')
            stages.append(dict(name='actual-management-queue-placement',**context.call(cpu,0x027f10a0,[created['outgoingR0']])));case=dict(case,createdFrame=created['outgoingR0'])
    elif top==0x027f1114:
        q=base+0x454;half(q,case['busy']);half(q+2,case['count']);mac=w(q+8);half(mac,case['status']);half(mac+4,case['retry']);half(mac+8,0x55aa)
    elif top==0x027f11a8:
        half(base+0x4a4,case['busy'])
        if case['pointer']is not None:word(base+0x4ac,case['pointer'])
    initial=[rng.getrandbits(32)for unused in REGISTERS];initial[0]=case['priority'];initial[-2:]=[context.STACK+0x3800,context.STOP|(index&1)];cpu.reg_write(UC_ARM_REG_CPSR,0x13|((index%4)<<6))
    for reg,value in zip(REGISTERS,initial):cpu.reg_write(reg,value)
    if body is not None:
        if virtual_address is None and len(body)!=size:raise ValueError('Full compiled function extent required')
        if virtual_address is not None:cpu.mem_map(execute,0x1000)
        cpu.mem_write(execute,body)
    watched={int(r['address'],0)for r in bindings.values()if r['kind']=='function'}|{0x027f0950};returned=[False];active=[];helpers=[];visited=[];stores=[];owned=[];before={key:bytes(cpu.mem_read(base+key,2))for key in(0x468,0x46a)};mp_count=h(base+0x46a);mac=w(base+0x45c);beacon=w(base+0x4ac);irq_before=w(IE);end_record=w(base+0x4bc);pre_frame_status=h(frame)
    def code(machine,pc,width,user):
        if pc==context.STOP:
            if active:raise ValueError('Entry returned with unfinished declared native callee')
            returned[0]=True;machine.emu_stop();return
        if not(context.MAIN<=pc<context.MAIN+len(main)or context.WRAM<=pc<context.WRAM+len(wram)or virtual_address is not None and execute<=pc<execute+len(body)):raise ValueError('Target escaped original initialized code or explicit diagnostic source')
        while active and pc==active[-1]['returnPc']and machine.reg_read(REGISTERS[-2])==active[-1]['sp']:
            record=active.pop();record.update(actualReturn=True,outgoingR0=machine.reg_read(REGISTERS[0]));helpers.append(record)
        if pc in watched and pc!=top:active.append(dict(entry=hex(pc),arguments=[machine.reg_read(r)for r in REGISTERS[:4]],sp=machine.reg_read(REGISTERS[-2]),returnPc=machine.reg_read(REGISTERS[-1])&~1))
        visited.append(pc)
    def write(machine,access,address,width,value,user):
        if context.STACK<=address<context.STACK+0x4000:return
        record=[address,width,value&((1<<(width*8))-1)];stores.append(record)
        if execute<=machine.reg_read(UC_ARM_REG_PC)<execute+(size if body is None else len(body)):owned.append(record)
    tokens=[cpu.hook_add(UC_HOOK_CODE,code),cpu.hook_add(UC_HOOK_MEM_WRITE,write)]
    try:cpu.emu_start(execute,context.STOP+4,count=budget)
    except Exception as error:return dict(actualOwnReturn=False,error=str(error),pc=hex(cpu.reg_read(UC_ARM_REG_PC)),postFaultCredit=0,sourceCredit=0)
    finally:
        for token in tokens:cpu.hook_del(token)
    if not returned[0]:return dict(actualOwnReturn=False,error='instruction bound exhausted',pc=hex(cpu.reg_read(UC_ARM_REG_PC)),postFaultCredit=0,sourceCredit=0)
    checks=dict(calleeSaved=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in list(range(4,12))+[13,14]),returnMode=bool(cpu.reg_read(UC_ARM_REG_CPSR)&32)==bool(index&1),cpuModeAndInterruptControlRestored=(cpu.reg_read(UC_ARM_REG_CPSR)&255)==(0x13|((index%4)<<6)|(32 if index&1 else 0)));expected=[]
    if top==0x037faec0:
        checks.update(allBusyCleared=all(h(base+off)==0 for off in(0x42c,0x440,0x454,0x468,0x47c,0x490,0x4a4)),queuedFramesCleared=all(w(base+off)==0 for off in(0x438,0x44c,0x460)),keyIndicesFFFF=h(base+0x4ce)==65535 and h(base+0x4d0)==65535,exactClearArguments=any(r['entry']=='0x37fdfd0'and r['arguments'][:3]==[0,base+0x42c,176]for r in helpers),physicalControlWord=h(base+0x3ce)==((8 if mode==0 else 0x208 if mode==1 else 0x108)|(0x4000 if case['wep']else 0)),originalCallbackSelection=w(base+0x464)==int(bindings['TxqEndBroadCast'if mode==1 else'TxqEndPsPoll']['address'],0))
    elif top==0x027f0b0c:
        expected=[[0x048080b4,2,0xc0],[base+0x47c,2,0],[base+0x490,2,0]];checks.update(irqRestored=w(IE)==irq_before,clearKsidBranch=any(r['entry']=='0x27ea0c8'for r in helpers)==(case['nullKey']==0))
    elif top==0x027f0ce0:
        expected=[[0x048080b4,2,(1,4,8)[case['priority']]]]
        if case['busy']:
            if not case['control']&0x4000:expected.append([frame+12,2,case['retry']])
            expected.append([frame+0x2a,2,case['sequence']])
        checks['irqRestored']=w(IE)==irq_before
    elif top==0x027f0c7c:
        expected=[]if not case['busy']else[[frame+8,2,case['status']or 2]];checks['callbackCalledOnlyWhenBusy']=any(r['entry']=='0x27f0950'for r in helpers)==bool(case['busy'])
        if case['busy']:checks['actualCallbackClearedBusy']=h(base+0x454)==0
    elif top==0x027f0f14:
        calls=[r['arguments'][:2]for r in helpers if r['entry']=='0x27f0ffc'];wanted=[[0,1],[1,0],[2,1 if mode==1 else 0]]if mode in(1,2,3)else[[0,0],[1,0],[2,0]];checks['actualThreeQueueCalls']=calls==wanted;release=mode==1 and bool(case['busy']);checks['actualReleaseOnlyForMode1Busy']=any(r['entry']=='0x37f8908'for r in helpers)==release
        if release:expected=[[base+0x468,2,0],[base+0x46a,2,(mp_count-1)&65535]];checks['actualAllocatedRecordReleased']=any(r['entry']=='0x37f8908'and r['arguments'][:2]==[base+0x188,end_record]for r in helpers)
        else:checks['otherModeBusyAndCounterUnchanged']=bytes(cpu.mem_read(base+0x468,2))==before[0x468]and bytes(cpu.mem_read(base+0x46a,2))==before[0x46a]
        if case['queued']:checks['actualQueuedFrameMarkedStatus2']=h(case['createdFrame']+8)==2
    elif top==0x027f1114:
        expected=[[base+0x456,2,(case['count']+1)&65535]]
        if case['busy']:expected.append([mac+4,2,0]);checks['noBusyRateCall']=not any(r['entry']=='0x27ea584'for r in helpers)
        else:
            rates=[r['outgoingR0']for r in helpers if r['entry']=='0x27ea584'];checks['oneOriginalRateReturn']=len(rates)==1;rate=rates[0]if rates else 0;expected.extend([[base+0x454,2,1],[mac,2,0],[mac+4,2,0],[mac+8,2,rate&65535],[0x048080a8,2,0x8000|((mac&0x3fff)>>1)]])
    elif top==0x027f11a8:expected=[[base+0x4a4,2,1],[0x04808080,2,0x8000|((beacon&0x3fff)>>1)]]
    if top!=0x037faec0:checks['independentOwnOrderedStores']=owned==expected
    return dict(actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,registers=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),pc=cpu.reg_read(UC_ARM_REG_PC),relevantRegisters=[cpu.reg_read(REGISTERS[i])for i in list(range(4,12))+[13,14]],orderedNonstackWrites=stores,ownedNonstackWrites=owned,expectedOwnWrites=expected,actualDeclaredHelperReturns=helpers,actualSetupEntryReturns=stages,visited=sorted(set(p for p in visited if execute<=p<execute+(size if body is None else len(body)))),instructions=len(visited),memorySha256={hex(a):hashlib.sha256(cpu.mem_read(a,length)).hexdigest()for a,length in setup['regions'].items()},case=case,providerReplacements=[],sourceCredit=0,allHelperReturnCountIsDeclaredWatchSetOnly=True,sceneAndRadioTimingUnproved=True)

def cases():
    base=dict(mode=0,contextOffset=0,priority=0,busy=0,irq=0,control=0,status=0,frameStatus=0,retry=0,sequence=0,prefill=False,wep=0,nullKey=0,count=0,pointer=None,queued=False);rows=[]
    rows.extend(dict(base,entry=0x037faec0,mode=m,contextOffset=o,prefill=p,wep=w)for m,o,p,w in itertools.product(range(4),(0,4),(False,True),(0,1,65535)))
    rows.extend(dict(base,entry=0x027f0b0c,mode=m,nullKey=n,busy=b,irq=i)for m,n,b,i in itertools.product(range(4),(0,1),(0,65535),(0,0x01000000,0xffffffff)))
    rows.extend(dict(base,entry=0x027f0ce0,mode=m,priority=p,busy=b,control=c,retry=0xabcd,sequence=s,irq=0xffffffff)for m,p,b,c,s in itertools.product(range(4),range(3),(0,1),(0,0x4000,65535),(0,65535)))
    rows.extend(dict(base,entry=0x027f0c7c,mode=m,priority=p)for m,p in itertools.product(range(4),range(3)))
    rows.extend(dict(base,entry=0x027f0c7c,mode=m,priority=2,busy=1,status=s,frameStatus=f,retry=r)for m,s,f,r in itertools.product((0,2,3),(0,2,65535),(0,2),(0,65535)))
    rows.extend(dict(base,entry=0x027f0f14,mode=m,busy=b,count=c,queued=q)for m,b,c,q in itertools.product(range(4),(0,1),(0,65535),(False,True)))
    rows.extend(dict(base,entry=0x027f1114,mode=m,busy=b,count=c,status=65535,retry=65535)for m,b,c in itertools.product(range(4),(0,1,65535),(0,65535)))
    rows.extend(dict(base,entry=0x027f11a8,mode=m,busy=b,pointer=p)for m,b,p in itertools.product(range(4),(0,65535),(None,0,1,0x3fff,0x4000,0xffffffff)))
    return rows
