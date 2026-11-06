import hashlib
import itertools
import json
import random
import struct
from pathlib import Path
import match_runtime
from match_runtime import REGISTERS
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR
import arm7_sdk306_task_command_context_20261102 as context
from project import ROOT,sha256,write_json

SIZES={0x027f0ac4:72,0x027ee0e4:236,0x027ef548:176}
PARAMS=[('WSetMacAdrs',0x027e8e68,16,True),('WSetRetryLimit',0x027e8ec8,22,False),('WSetEnableChannel',0x027e8efc,24,False),('WSetMode',0x027e8f3c,28,False),('WSetRate',0x027e8fbc,30,False),('WSetWepMode',0x027e8ff0,32,False),('WSetWepKeyId',0x027e9090,34,False),('WSetWepKey',0x027e90b4,36,True),('WSetBeaconType',0x027e9114,116,False),('WSetBcSsidResponse',0x027e914c,118,False),('WSetBeaconLostThreshold',0x027e9184,120,False),('WSetActiveZoneTime',0x027e91bc,122,False),('WSetSsidMask',0x027e926c,124,True),('WSetPreambleType',0x027e929c,156,False),('WSetAuthAlgo',0x027e9344,158,False)]

def prepare(main,wram,case,index):
    top=case['entry'];cpu,meta=context.setup(main,wram,index,mode=case['mode'],offset=case['contextOffset'],heap=top!=0x027f0ac4);base=meta['context'];request=confirmation=None
    def half(a,v):cpu.mem_write(a,struct.pack('<H',v&65535))
    def word(a,v):cpu.mem_write(a,struct.pack('<I',v&0xffffffff))
    if top==0x027f0ac4:
        arg0=base+0x47c+20*case['slot'];mac=int.from_bytes(cpu.mem_read(arg0+8,4),'little')
        if not context.base.MAC<=mac<context.base.MAC+0x5000:raise ValueError('Actual initialized key-frame MAC pointer required')
        half(mac+4,case['retry']);half(arg0+4,case['outCount']);half(arg0,case['busy']);word(base+0x5a8,case['counter']);word(base+0x5a4,case['counter']);arg1=None
    else:
        allocation=context.base.call(cpu,0x037f886c,[base+512,384]);meta['prerequisiteReturns'].append(dict(name='actual-command-buffer-allocation',**allocation));request=allocation['outgoingR0']
        if not request:raise ValueError('Original command allocation failed')
        cpu.mem_write(request+12,bytes([0xa5])*384);half(base+0x34c,case['state']);arg0=request;confirmation=request+(160 if top==0x027ee0e4 else 20);arg1=confirmation
        if top==0x027ee0e4:
            values=case['values'];cpu.mem_write(request+16,bytes(values['mac']));cpu.mem_write(request+36,bytes(values['keys']));cpu.mem_write(request+124,bytes(values['ssidMask']))
            for name,entry,offset,pointer in PARAMS:
                if not pointer:half(request+offset,values[str(offset)])
        else:half(request+16,case['control']);half(request+18,case['channel'])
        cpu.mem_write(confirmation,struct.pack('<HHH',0x3030,0xa55a,0x5aa5))
    word(0x04000210,case['irq']);return cpu,meta,dict(arg0=arg0,arg1=arg1,request=request,confirmation=confirmation)

def memory(cpu,meta,include_stack=True):return{hex(a):hashlib.sha256(cpu.mem_read(a,n)).hexdigest()for a,n in meta['regions'].items()if include_stack or a!=context.base.STACK}

def reference_parameters(main,wram,case,index):
    cpu,meta,args=prepare(main,wram,case,index);request=args['request'];confirmation=args['confirmation'];cpu.reg_write(UC_ARM_REG_CPSR,0x13|((index%4)<<6));cpu.mem_write(confirmation+2,b'\x01\x00');writes=[[confirmation+2,2,1]];calls=[];ret=1
    def write(machine,access,address,width,value,user):
        if not context.base.STACK<=address<context.base.STACK+0x4000:writes.append([address,width,value&((1<<(8*width))-1)])
    token=cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    try:
        if case['state']==16:
            ret=0
            for name,entry,offset,pointer in PARAMS:
                value=request+offset if pointer else int.from_bytes(cpu.mem_read(request+offset,2),'little');arguments=[value,0]if name=='WSetActiveZoneTime'else[value];result=context.base.call(cpu,entry,arguments);calls.append(dict(name=name,**result));ret=(ret|result['outgoingR0'])&65535
    finally:cpu.hook_del(token)
    return dict(expectedR0=ret,memorySha256=memory(cpu,meta,False),orderedNonstackWrites=writes,actualIndependentApiReturns=calls,expectedIe=int.from_bytes(cpu.mem_read(0x04000210,4),'little'))

def reference_device(main,wram,case,index):
    cpu,meta,args=prepare(main,wram,case,index);base=meta['context'];confirmation=args['confirmation'];cpu.reg_write(UC_ARM_REG_CPSR,0x13|((index%4)<<6));cpu.mem_write(confirmation+2,b'\x01\x00');writes=[[confirmation+2,2,1]];calls=[];ret=0
    def write(machine,access,address,width,value,user):
        if not context.base.STACK<=address<context.base.STACK+0x4000:writes.append([address,width,value&((1<<(8*width))-1)])
    def host_half(address,value):cpu.mem_write(address,struct.pack('<H',value));writes.append([address,2,value])
    def invoke(name,entry,arguments):calls.append(dict(name=name,**context.base.call(cpu,entry,arguments)))
    token=cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    try:
        if case['state']&0xf0!=0x10:ret=1
        elif case['control']==1:
            if case['state']!=16:ret=1
            else:
                invoke('WSetChannel',0x027e990c,[case['channel'],1]);host_half(base+0x350,0);invoke('WStart',0x037f8de0,[]);invoke('WSetForcePowerState',0x027e9cec,[0x8000]);host_half(base+0x34c,17)
        elif case['control']==0:
            if case['state']!=17:ret=1
            else:invoke('WSetForcePowerState',0x027e9cec,[0]);invoke('WStop',0x037f9198,[]);host_half(base+0x34c,16)
    finally:cpu.hook_del(token)
    return dict(expectedR0=ret,memorySha256=memory(cpu,meta,False),orderedNonstackWrites=writes,actualIndependentApiReturns=calls,expectedIe=int.from_bytes(cpu.mem_read(0x04000210,4),'little'))

def run(main,wram,case,index,body=None,virtual_address=None,budget=200000):
    top=case['entry'];size=SIZES[top]
    if top==0x027f0ac4 and(case['slot']not in(0,1)or case['mode']!=2):raise ValueError('Raw mode2 and two actual initialized key slots required')
    if top==0x027ef548 and any(case[key]not in range(65536)for key in('state','control','channel')):raise ValueError('Explicit physical u16 device fields required')
    expected_reference=reference_parameters(main,wram,case,index)if top==0x027ee0e4 else reference_device(main,wram,case,index)if top==0x027ef548 else None;cpu,meta,args=prepare(main,wram,case,index);base=meta['context'];rng=random.Random(0x327000+index);initial=[rng.getrandbits(32)for unused in REGISTERS];initial[0]=args['arg0']
    if args['arg1']is not None:initial[1]=args['arg1']
    initial[-2:]=[context.base.STACK+0x3800,context.base.STOP|(index&1)];cpu.reg_write(UC_ARM_REG_CPSR,0x13|((index%4)<<6))
    for reg,value in zip(REGISTERS,initial):cpu.reg_write(reg,value)
    before_context=bytes(cpu.mem_read(base,1684));execute=top if virtual_address is None else virtual_address
    if body is not None:
        if virtual_address is None and len(body)!=size:raise ValueError('Exact full source body or explicitly separate diagnostic address required')
        if virtual_address is not None:cpu.mem_map(execute,0x1000)
        cpu.mem_write(execute,body)
    watched={entry for name,entry,offset,pointer in PARAMS}if top==0x027ee0e4 else{0x027e990c,0x037f8de0,0x027e9cec,0x037f9198}if top==0x027ef548 else set();active=[];helpers=[];stores=[];owned=[];visited=[];returned=[False]
    def code(machine,pc,width,user):
        if pc==context.base.STOP:
            if active:raise ValueError('Entry returned with unfinished observed original helper')
            returned[0]=True;machine.emu_stop();return
        if not(context.base.MAIN<=pc<context.base.MAIN+len(main)or context.base.WRAM<=pc<context.base.WRAM+len(wram)or virtual_address is not None and execute<=pc<execute+len(body)):raise ValueError('Entry escaped original initialized code')
        while active and pc==active[-1]['returnPc']and machine.reg_read(REGISTERS[-2])==active[-1]['sp']:
            row=active.pop();row.update(actualReturn=True,outgoingR0=machine.reg_read(REGISTERS[0]));helpers.append(row)
        if pc in watched and pc!=execute:active.append(dict(entry=hex(pc),arguments=[machine.reg_read(r)for r in REGISTERS[:4]],returnPc=machine.reg_read(REGISTERS[-1])&~1,sp=machine.reg_read(REGISTERS[-2]),observedDepth=len(active)))
        visited.append(pc)
    def write(machine,access,address,width,value,user):
        if context.base.STACK<=address<context.base.STACK+0x4000:return
        row=[address,width,value&((1<<(8*width))-1)];stores.append(row)
        if execute<=machine.reg_read(UC_ARM_REG_PC)<execute+(size if body is None else len(body)):owned.append(row)
    tokens=[cpu.hook_add(UC_HOOK_CODE,code),cpu.hook_add(UC_HOOK_MEM_WRITE,write)]
    try:cpu.emu_start(execute,context.base.STOP+4,count=budget)
    except Exception as error:return dict(actualOwnReturn=False,error=type(error).__name__+':'+str(error),pc=hex(cpu.reg_read(UC_ARM_REG_PC)),postFaultCredit=0,sourceCredit=0)
    finally:
        for token in tokens:cpu.hook_del(token)
    if not returned[0]:return dict(actualOwnReturn=False,error='instruction bound exhausted',pc=hex(cpu.reg_read(UC_ARM_REG_PC)),postFaultCredit=0,sourceCredit=0)
    checks=dict(calleeSaved=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in list(range(4,12))+[13,14]),cpuModeAndInterruptControl=(cpu.reg_read(UC_ARM_REG_CPSR)&255)==(0x13|((index%4)<<6)|(32 if index&1 else 0)),irqEnableMatchesScopedOriginalApiEffects=int.from_bytes(cpu.mem_read(0x04000210,4),'little')==(expected_reference['expectedIe']if top==0x027ef548 else case['irq']))
    if top==0x027f0ac4:
        q=args['arg0'];low=case['retry']&255;expected=[[base+(0x5a4 if low else 0x5a8),4,(case['counter']+(low if low else 1))&0xffffffff],[q+4,2,(case['outCount']+1)&65535],[q,2,0]];checks.update(fullLowByteCounterAndHalfwordWrap=stores==expected,noHelpers=not helpers,otherKeySlotPreserved=bytes(cpu.mem_read(base+0x47c+20*(1-case['slot']),20))==before_context[0x47c+20*(1-case['slot']):0x490+20*(1-case['slot'])])
    elif top==0x027ee0e4:
        checks.update(composedRealSetterEffects=memory(cpu,meta,False)==expected_reference['memorySha256'],composedRealSetterWriteOrder=stores==expected_reference['orderedNonstackWrites'],fullObservedReturn=cpu.reg_read(REGISTERS[0])==expected_reference['expectedR0']);expected_calls=[]
        for ref in expected_reference['actualIndependentApiReturns']:expected_calls.append((ref['entry'],ref['arguments']))
        checks['completeOriginalSetterArgumentOrder']=[(r['entry'],r['arguments'][:2 if r['entry']=='0x27e91bc'else 1])for r in helpers if r['observedDepth']==0]==expected_calls
    else:
        checks.update(composedActualControlEffects=memory(cpu,meta,False)==expected_reference['memorySha256'],composedControlWriteOrder=stores==expected_reference['orderedNonstackWrites'],fullReturn=cpu.reg_read(REGISTERS[0])==expected_reference['expectedR0']);expected_calls=[(r['entry'],r['arguments'])for r in expected_reference['actualIndependentApiReturns']];arities={0x027e990c:2,0x037f8de0:0,0x027e9cec:1,0x037f9198:0};checks['allControlCallArgumentsAndOrdering']=[(r['entry'],r['arguments'][:arities[int(r['entry'],0)]])for r in helpers if r['observedDepth']==0]==expected_calls

    return dict(actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,registers=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),pc=cpu.reg_read(UC_ARM_REG_PC),orderedNonstackWrites=stores,ownedNonstackWrites=owned,actualDeclaredHelperReturns=helpers,actualSetupEntryReturns=meta['prerequisiteReturns'],independentOriginalApiModel=expected_reference,memorySha256=memory(cpu,meta),visited=sorted(set(p for p in visited if execute<=p<execute+(size if body is None else len(body)))),instructions=len(visited),providerReplacements=[],sourceCredit=0,physicalRadioSceneReachabilityAndConcurrentSchedulerUnproved=True)

def parameter_values(pattern):
    scalars={str(offset):0 for name,entry,offset,pointer in PARAMS if not pointer};scalars.update(mac=[0x12,0x34,0x56,0x78,0x9a,0xbc],keys=[0]*80,ssidMask=[255]*32)
    if pattern=='sane':scalars.update({'22':3,'24':0x3ffe,'28':2,'30':2,'122':10,'120':16,'156':1})
    elif pattern=='ones':scalars={k:([255]*len(v)if isinstance(v,list)else 65535)for k,v in scalars.items()}
    elif pattern=='mixed':scalars.update({'22':65535,'24':2,'28':3,'30':1,'32':3,'34':3,'116':1,'118':1,'120':255,'122':65535,'156':1,'158':1},keys=[i^0x80 for i in range(80)])
    return scalars

def cases():
    base=dict(mode=0,contextOffset=0,irq=0xffffffff);rows=[]
    for slot,retry,counter in itertools.product((0,1),range(256),(0,0xffffffff)):rows.append(dict(base,entry=0x027f0ac4,slot=slot,retry=retry,counter=counter,outCount=(0,1,65535)[retry%3],busy=(0,1,65535)[(retry//3)%3],mode=2,contextOffset=4 if retry&1 else 0))
    rows.extend(dict(base,entry=0x027f0ac4,slot=s,retry=r,counter=v,outCount=o,busy=1,mode=2)for s,r,v,o in itertools.product((0,1),(256,257,32768,65535),(0,0xffffffff),(0,1,65535)))
    rows.extend(dict(base,entry=0x027ee0e4,state=state,values=parameter_values(p),mode=m,contextOffset=o)for state,p,m,o in itertools.product((0,15,16,17,32,64,65535),('zero','sane','ones','mixed'),(0,2),(0,4)))
    rows.extend(dict(base,entry=0x027ef548,state=s,control=c,channel=ch,mode=m,contextOffset=o)for s,c,ch,m,o in itertools.product((0,15,16,17,18,31,32,64,65535),(0,1,2,65535),(0,14,65535),(0,2),(0,4)))
    return rows

def main():
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();results=[]
    for index,case in enumerate(cases()):
        try:result=run(main,wram,case,index)
        except Exception as error:result=dict(actualOwnReturn=False,modelPassed=False,error=type(error).__name__+':'+str(error),postFaultCredit=0)
        results.append(dict(case=case,result=result))
        if not result.get('modelPassed'):print(json.dumps(dict(index=index,case=case,result=result.get('modelChecks',result))),flush=True);break
        if index%256==255:print('completed'+str(index+1),flush=True)
    report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),planned=len(cases()),completed=len(results),allPassed=len(results)==len(cases())and all(r['result'].get('modelPassed')for r in results),records=results,sourceCredit=0);write_json(ROOT/'evidence/attempts/arm7-sdk327-control-setters-key-native-20261102.json',report);print(json.dumps(dict(planned=report['planned'],completed=report['completed'],allPassed=report['allPassed'])),flush=True)

if __name__=='__main__':main()
