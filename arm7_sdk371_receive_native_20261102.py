import gzip
import hashlib
import itertools
import json
import random
import struct
from pathlib import Path
import match_runtime
from match_runtime import REGISTERS
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR,UC_ARM_REG_PC
import arm7_sdk306_task_command_context_20261102 as context
from project import ROOT,sha256,write_json

SIZES={0x027f2f78:464,0x027f2e98:224,0x027f3b6c:176}
WATCH={0x027ebfec:'CAM_GetStaState',0x027ebc50:'CAM_SetStaState',0x027ede50:'MLME_IssueDisAssIndication',0x027edbf0:'MLME_IssueDeAuthIndication',0x027f2000:'IsExistManFrame',0x027f1888:'MakeAssResFrame',0x027f3c1c:'ElementChecker',0x027ec0d8:'CAM_GetAID',0x027f16b0:'MakeDisAssFrame',0x027f1ec8:'MakeDeAuthFrame',0x027f1088:'TxManCtrlFrame',0x037f9238:'WSetStaState',0x027ea048:'WClearAids',0x027f0d6c:'DeleteTxFrames'}

def half(cpu,a,v):cpu.mem_write(a,struct.pack('<H',v&65535))
def word(cpu,a,v):cpu.mem_write(a,struct.pack('<I',v&0xffffffff))
def h(cpu,a):return int.from_bytes(cpu.mem_read(a,2),'little')
def w(cpu,a):return int.from_bytes(cpu.mem_read(a,4),'little')

def prepare(main,wram,case,index):
    if case['entry']not in SIZES or case['mode']not in(0,1,2,3)or case['offset']not in(0,4)or case['cam']not in(0,1):raise ValueError('Exact receive entries/initialized modes/two-record backing required')
    cpu,meta=context.setup(main,wram,index,mode=case['mode'],offset=case['offset'],heap=True);base=meta['context'];cam=w(cpu,base+0x31c);state=context.base.call(cpu,0x027ebc50,[case['cam'],case['peerState']]);meta['prerequisiteReturns'].append(dict(name='actual-cam-state-setter',**state));record=context.base.call(cpu,0x037f886c,[base+476,384]);meta['prerequisiteReturns'].append(dict(name='actual-rx-management-buffer-allocation',**record));packet=record['outgoingR0']
    if not packet:raise ValueError('Original bounded frame allocation failed')
    cpu.mem_write(packet+12,bytes(128));frame=packet+16;half(cpu,frame+2,case['cam']);half(cpu,frame+6,case['length']);half(cpu,frame+44,case['reason']if case['entry']!=0x027f2f78 else case['capability']);half(cpu,frame+46,1);sa=bytes([0x12,0x34,0x56,0x78,0x9a,0xbc]);cpu.mem_write(frame+30,sa);cpu.mem_write(base+966,sa if case['matchingSa']else bytes([0x22,0x44,0x66,0x88,0xaa,0xcc]));half(cpu,base+0x34c,case['workState']);half(cpu,cam+28*case['cam']+2,case.get('peerAid',0));half(cpu,base+820,case.get('wepMode',0));half(cpu,base+826,(h(cpu,base+826)&~4)|(4*case.get('preamble',0)));half(cpu,base+866,len(bytes.fromhex(case.get('ssid',''))));cpu.mem_write(base+868,bytes.fromhex(case.get('ssid','')));
    if 'elements'in case:cpu.mem_write(frame+48,bytes.fromhex(case['elements']))
    if case.get('pendingFrame'):
        cpu.mem_write(cam+28*case['cam']+4,sa);pending=context.base.call(cpu,0x027f1888,[case['cam'],10,0])if case['pendingFrame']=='assoc'else context.base.call(cpu,0x027f1ec8,[frame+30,6,1]);meta['prerequisiteReturns'].append(dict(name='actual-pending-management-constructor',**pending))
        if pending['outgoingR0']in(0,0xffffffff):raise ValueError('Original pending management frame constructor failed')
        meta['prerequisiteReturns'].append(dict(name='actual-pending-management-enqueue',**context.base.call(cpu,0x027f1088,[pending['outgoingR0']])));found=context.base.call(cpu,0x027f2000,[frame+30,0x10 if case['pendingFrame']=='assoc'else 0xc0]);meta['prerequisiteReturns'].append(dict(name='actual-pending-management-query',**found))
        if found['outgoingR0']!=1:raise ValueError('Actual pending-management prerequisite did not establish matching queue entry')
    return cpu,meta,dict(packet=packet,frame=frame,camBase=cam,camState=h(cpu,cam+28*case['cam']),workMode=h(cpu,base+0x350))

def run(main,wram,case,index,body=None,virtual_address=None):
    cpu,meta,args=prepare(main,wram,case,index);base=meta['context'];frame=args['frame'];top=case['entry'];size=SIZES[top];execute=top if virtual_address is None else virtual_address;extent=size if body is None else len(body);before=bytes(cpu.mem_read(frame,128))
    if body is not None:
        if virtual_address is None and len(body)!=size or virtual_address is not None and not 0<len(body)<=4096:raise ValueError('Complete own source or explicit bounded wrong-C mapping required')
        if virtual_address is not None:cpu.mem_map(execute,0x1000)
        cpu.mem_write(execute,body)
    rng=random.Random(0x371000+index);initial=[rng.getrandbits(32)for unused in REGISTERS];initial[0]=frame;initial[-2:]=[context.base.STACK+0x3800,context.base.STOP];cpsr=0x13|((index%4)<<6);cpu.reg_write(UC_ARM_REG_CPSR,cpsr)
    for reg,value in zip(REGISTERS,initial):cpu.reg_write(reg,value)
    active=[];helpers=[];writes=[];own=[];visited=[];returned=[False]
    def code(machine,pc,width,user):
        while active and pc==active[-1]['returnPc']and machine.reg_read(REGISTERS[-2])==active[-1]['sp']:
            r=active.pop();r.update(actualReturn=True,outgoingR0=machine.reg_read(REGISTERS[0]));helpers.append(r)
        if pc==context.base.STOP:
            if active:raise ValueError('Receive entry returned with unfinished helper')
            returned[0]=True;machine.emu_stop();return
        if not(context.base.MAIN<=pc<context.base.MAIN+len(main)or context.base.WRAM<=pc<context.base.WRAM+len(wram)or virtual_address is not None and execute<=pc<execute+extent):raise ValueError('Receive entry escaped initialized code')
        if virtual_address is None and execute+size-({464:8,224:4,176:4,144:8,84:4}[size])<=pc<execute+extent:raise ValueError('Own entry fetched its measured literal pool')
        if pc in WATCH:active.append(dict(name=WATCH[pc],entry=hex(pc),arguments=[machine.reg_read(r)for r in REGISTERS[:4]],sp=machine.reg_read(REGISTERS[-2]),returnPc=machine.reg_read(REGISTERS[-1])&~1))
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
    named=lambda name:[r for r in helpers if r['name']==name];checks=dict(calleeSaved=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in list(range(4,12))+[13,14]),modeAndInterruptControl=(cpu.reg_read(UC_ARM_REG_CPSR)&255)==cpsr,incomingFrameUnchanged=bytes(cpu.mem_read(frame,128))==before,initializedModeWasActual=args['workMode']==case['mode'],originalPeerSetterStored=args['camState']==case['peerState'])
    if top==0x027f2f78:
        if case['length']<=4 or case['mode']!=1:checks['earlyReturnNoEffects']=not writes and not helpers
        else:
            checks['actualExistingManagementCheck']=any(r['arguments'][:2]==[frame+30,0x10]for r in named('IsExistManFrame'))
            if case.get('pendingFrame')=='assoc':checks['pendingAssociationEarlyReturn']=not writes and not named('MakeAssResFrame')and not named('MakeDeAuthFrame')
            elif case['cam']==0 or case['peerState']<48:
                checks['unauthenticatedReasonSix']=not named('MakeDeAuthFrame')if case.get('pendingFrame')=='deauth'else any(r['arguments'][:3]==[frame+30,6,1]for r in named('MakeDeAuthFrame'));checks['noAssociationResponse']=not named('MakeAssResFrame')
            elif case['peerState']!=64 and case.get('peerAid',0):checks['nonzeroAidEarlyReturn']=not named('MakeAssResFrame')and not named('ElementChecker')
            else:
                cap=case['capability'];invalid=bool(cap&0xffc2 or not cap&1 or bool(case.get('wepMode',0))!=bool(cap&16)or case.get('preamble',0)and not cap&32);status=10 if invalid else case.get('expectedElementStatus',18);checks['independentAssociationStatus']=any(r['arguments'][:2]==[case['cam'],status]for r in named('MakeAssResFrame'));checks['realElementChecker']=len(named('ElementChecker'))==1
                if case['peerState']==64:checks['priorClassThreeDemotion']=h(cpu,args['camBase']+28*case['cam'])==48 and any(r['arguments'][:2]==[frame+30,1]for r in named('MLME_IssueDisAssIndication'))
    elif case['mode']==1:
        expected=48 if top==0x027f2e98 and case['peerState']==64 else 32 if top==0x027f3b6c and case['peerState']>32 else case['peerState'];checks['parentPeerState']=h(cpu,args['camBase']+28*case['cam'])==expected
        indication='MLME_IssueDisAssIndication'if top==0x027f2e98 else'MLME_IssueDeAuthIndication';should_indicate=case['peerState']==64 if top==0x027f2e98 else case['peerState']>32
        if should_indicate:checks['fullReasonForwarded']=any(r['arguments'][:2]==[frame+30,case['reason']]for r in named(indication))
    elif case['mode']in(2,3):
        changes=(case['workState']==64 if top==0x027f2e98 else case['workState']>32)and case['matchingSa'];expected=(48 if top==0x027f2e98 else 32)if changes else case['workState'];checks['childWorkState']=h(cpu,base+0x34c)==expected
        if changes:
            indication='MLME_IssueDisAssIndication'if top==0x027f2e98 else'MLME_IssueDeAuthIndication';checks['matchedChildFullReasonForwarded']=any(r['arguments'][:2]==[frame+30,case['reason']]for r in named(indication))
        if not changes:checks['unmatchedChildNoIndication']=not named('MLME_IssueDisAssIndication')and not named('MLME_IssueDeAuthIndication')
    else:checks['unhandledModeNoEffects']=not writes and not helpers
    return dict(case=case,actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,registers=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),pc=cpu.reg_read(UC_ARM_REG_PC),orderedNonstackWrites=writes,ownedNonstackWrites=own,memorySha256={hex(a):hashlib.sha256(cpu.mem_read(a,n)).hexdigest()for a,n in meta['regions'].items()},actualDeclaredHelperReturns=helpers,actualSetupEntryReturns=meta['prerequisiteReturns'],visited=sorted(set(pc for pc in visited if execute<=pc<execute+extent)),instructions=len(visited),frame=hex(frame),sourceCredit=0,providerReplacements=[],enclosingPhysicalReceiveSceneUnproved=True)

def cases():
    base=dict(entry=0x027f2e98,mode=0,offset=0,cam=0,peerState=32,workState=32,matchingSa=False,length=8,reason=7,capability=0);rows=[]
    for top in SIZES:
        for mode,offset,cam,state in itertools.product((0,1,2,3),(0,4),(0,1),(0,32,48,64)):
            if top==0x027f2f78:rows.extend(dict(base,entry=top,mode=mode,offset=offset,cam=cam,peerState=state,length=n)for n in(0,4,8))
            else:rows.extend(dict(base,entry=top,mode=mode,offset=offset,cam=cam,peerState=state,workState=s,matchingSa=match,reason=reason)for s,match,reason in itertools.product((32,48,64),(False,True),(0,7,65535)))
    for offset,peer,wep,pre,cap,item,aid in itertools.product((0,4),(48,64),(0,1),(0,1),(0,1,17,33,49,65535),(('0000',18,''),('00005800',18,''),('0000010102',0,''),('000178010102',0,''),('0000010102',1,'78')),(0,1)):
        elements,expected,ssid=item;rows.append(dict(base,entry=0x027f2f78,mode=1,offset=offset,cam=1,peerState=peer,length=4+len(bytes.fromhex(elements)),capability=cap,wepMode=wep,preamble=pre,elements=elements,expectedElementStatus=expected,ssid=ssid,peerAid=aid))
    rows.extend(dict(base,entry=0x027f2f78,mode=1,cam=1,peerState=state,length=8,pendingFrame=pending,offset=offset)for state,pending,offset in itertools.product((32,48,64),('assoc','deauth'),(0,4))if pending=='assoc'or state<48)
    return rows

def main():
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();results=[]
    for i,c in enumerate(cases()):results.append(run(main,wram,c,i))
    raw=json.dumps(results,sort_keys=True,separators=(',',':')).encode();packed=gzip.compress(raw,mtime=0);trace=ROOT/'work/arm7-bulk-20261030/sdk371-receive-native/native-cases.json.gz';trace.parent.mkdir(parents=True,exist_ok=True);trace.write_bytes(packed);failed=[dict(index=i,case=r['case'],checks=r['modelChecks'])for i,r in enumerate(results)if r['actualOwnReturn']and not r['modelPassed']];unsupported=[r for r in results if not r['actualOwnReturn']];report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),attemptedCases=len(results),actualOwnReturns=sum(r['actualOwnReturn']for r in results),failedModels=failed,unsupported=unsupported,nativeTrace=dict(path=trace.relative_to(ROOT).as_posix(),compressedSha256=sha256(trace),rawSha256=hashlib.sha256(raw).hexdigest()),sourceCredit=0,providerReplacements=[],ordinaryRadioSceneAndAdmissionUnproved=True);write_json(ROOT/'evidence/attempts/arm7-sdk371-receive-native-20261102.json',report);print(json.dumps(dict(cases=len(results),actualReturns=report['actualOwnReturns'],failedModels=len(failed),unsupported=len(unsupported),sourceCredit=0)),flush=True)

if __name__=='__main__':main()
