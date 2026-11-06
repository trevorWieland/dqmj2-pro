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
import arm7_sdk345_mlme_task_native_20261102 as common
from project import ROOT,sha256,write_json

TOP,SIZE=0x027ed864,624
WATCH=dict(common.WATCH,**{})
WATCH.update({0x027ea5d0:'BBP_Read',0x027ea5fc:'BBP_Write',0x027e9368:'WSetCCA_ED',0x027e9cec:'WSetForcePowerState',0x03806e44:'unsigned-division'})

def prepare(main,wram,case,index):
    seed=dict(entry=TOP,mode=case['mode'],offset=case['offset'],state=case['state'],scanType=0,channel=0,channelCount=0,elapsed=0,period=case['time'],result=0);cpu,meta,args=common.prepare(main,wram,seed,index);base=meta['context'];req=args['request'];cfm=args['confirmation'];common.half(cpu,req+12,10);common.half(cpu,req+0x12,case['ccaMode']);common.half(cpu,req+0x14,case['edThreshold']);common.half(cpu,req+0x16,case['time']);cpu.mem_write(req+0x18,bytes([case['channelByte']])*16);common.word(cpu,base+0x408,case['counter']);common.word(cpu,base+0x40c,case['cca']);common.half(cpu,base+0x410,case['power']);common.half(cpu,base+0x412,case['backupCca']);common.half(cpu,base+0x414,case['backupEd']);common.half(cpu,base+0x418,case['channelIndex']);common.half(cpu,base+0x41a,case['status']);common.half(cpu,0x0480819c,case['hardwareStatus']);cpu.mem_write(cfm+8,bytes([0xa5,0x5a])*16);return cpu,meta,args

def run(main,wram,case,index,body=None,virtual_address=None,linked_callback=None):
    if case.get('mode')not in(0,2)or case.get('offset')not in(0,4):raise ValueError('Explicit initialized context modes/offsets required')
    for field in('state','channelIndex','hardwareStatus','power','backupCca','backupEd','status','time','ccaMode','edThreshold'):
        if not isinstance(case.get(field),int)or not 0<=case[field]<=65535:raise ValueError('Physical halfword field required:'+field)
    for field in('counter','cca'):
        if not isinstance(case.get(field),int)or not 0<=case[field]<=0xffffffff:raise ValueError('Full unsigned word field required:'+field)
    if not isinstance(case.get('channelByte'),int)or not 0<=case['channelByte']<=255:raise ValueError('Physical channel byte required')
    if case['state']in(0x81,0x83)and not 0<=case['channelIndex']<16:raise ValueError('Direct channel-list read requires index below16')
    cpu,meta,args=prepare(main,wram,case,index);base=meta['context'];cfm=args['confirmation'];execute=TOP if virtual_address is None else virtual_address;extent=SIZE if body is None else len(body)
    if linked_callback is not None:
        if len(linked_callback)!=44 or main[0x027edad4-common.context.base.MAIN:0x027edad4-common.context.base.MAIN+44]!=linked_callback:raise ValueError('Only complete freshly linked byte-identical measurement callback permitted')
        cpu.mem_write(0x027edad4,linked_callback)
    if body is not None:
        if virtual_address is None and len(body)!=SIZE or virtual_address is not None and not 0<len(body)<=4096:raise ValueError('Complete positive or bounded wrong source required')
        if virtual_address is not None:cpu.mem_map(execute,0x1000)
        cpu.mem_write(execute,body)
    rng=random.Random(0x356000+index);initial=[rng.getrandbits(32)for unused in REGISTERS];initial[-2:]=[common.context.base.STACK+0x3800,common.context.base.STOP];cpsr=0x13|((index%4)<<6);cpu.reg_write(UC_ARM_REG_CPSR,cpsr)
    for reg,value in zip(REGISTERS,initial):cpu.reg_write(reg,value)
    writes=[];own=[];helpers=[];active=[];visited=[];returned=[False]
    def code(machine,pc,width,user):
        while active and pc==active[-1]['returnPc']and machine.reg_read(REGISTERS[-2])==active[-1]['sp']:
            row=active.pop();row.update(actualReturn=True,outgoingR0=machine.reg_read(REGISTERS[0]));helpers.append(row)
        if pc==common.context.base.STOP:
            if active:raise ValueError('Incomplete watched measurement helper')
            returned[0]=True;machine.emu_stop();return
        if not(common.context.base.MAIN<=pc<common.context.base.MAIN+len(main)or common.context.base.WRAM<=pc<common.context.base.WRAM+len(wram)or virtual_address is not None and execute<=pc<execute+extent):raise ValueError('Measurement task escaped original initialized code')
        if pc in WATCH:active.append(dict(name=WATCH[pc],entry=hex(pc),arguments=[machine.reg_read(r)for r in REGISTERS[:4]],sp=machine.reg_read(REGISTERS[-2]),returnPc=machine.reg_read(REGISTERS[-1])&~1))
        visited.append(pc)
    def write(machine,access,a,width,value,user):
        if common.context.base.STACK<=a<common.context.base.STACK+0x4000:return
        r=[a,width,value&((1<<(8*width))-1)];writes.append(r)
        if execute<=machine.reg_read(UC_ARM_REG_PC)<execute+extent:own.append(r)
    hooks=[cpu.hook_add(UC_HOOK_CODE,code),cpu.hook_add(UC_HOOK_MEM_WRITE,write)];error=None
    try:cpu.emu_start(execute,common.context.base.STOP+4,count=300000)
    except Exception as exc:error=type(exc).__name__+':'+str(exc)
    finally:
        for token in hooks:cpu.hook_del(token)
    if not returned[0]:return dict(case=case,actualOwnReturn=False,error=error or'instruction-bound exhaustion',pc=hex(cpu.reg_read(UC_ARM_REG_PC)),instructions=len(visited),postFaultStateCredit=0,sourceCredit=0)
    checks=dict(calleeSaved=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in list(range(4,12))+[13,14]),modeAndInterruptControl=(cpu.reg_read(UC_ARM_REG_CPSR)&255)==cpsr);named=lambda name:[r for r in helpers if r['name']==name];state=common.h(cpu,base+0x404);expected=None
    if case['state']==0x82:
        expected=[[base+0x408,4,(case['counter']+1)&0xffffffff]]
        if case['hardwareStatus']&1:expected.append([base+0x40c,4,(case['cca']+100)&0xffffffff])
        checks['sampleState']=state==0x82
    elif case['state']==0x83:
        ratio=0
        if case['counter']and case['cca']:ratio=min(((case['cca']//case['counter'])+1)&0xffffffff,100)
        expected=[[cfm+8+2*case['channelIndex'],2,(case['channelByte']|(ratio<<8))&65535],[base+0x418,2,(case['channelIndex']+1)&65535],[base+0x404,2,0x81]];checks.update(ratioState=state==0x81,originalByteGetter=any(r['arguments'][0]==args['request']+0x18+case['channelIndex']for r in named('WL_ReadByte')))
        direct_div=[r for r in named('unsigned-division')if execute<=r['returnPc']<execute+extent];checks['unsignedDivisionGuard']=bool(direct_div)==bool(case['counter']and case['cca'])
        if direct_div:checks['exactUnsignedDivisionArguments']=direct_div[0]['arguments'][:2]==[case['cca'],case['counter']]and direct_div[0]['outgoingR0']==case['cca']//case['counter']
    elif case['state']==0x84:
        expected=[[base+0x350,2,common.h(cpu,base+0x32e)],[cfm+4,2,case['status']],[base+0x404,2,0]]+[[cfm+8+2*c,2,0]for c in range(case['channelIndex'],16)];checks.update(completionState=state==0,actualStop=bool(named('WStop')),actualOriginalConfirm=bool(named('IssueMlmeConfirm')),backupCcaForwarded=any(r['arguments'][:2]==[0x13,case['backupCca']]for r in named('BBP_Write')),backupEdForwarded=any(r['arguments'][:2]==[0x35,case['backupEd']]for r in named('BBP_Write')),powerForwarded=any(r['arguments'][0]==case['power']for r in named('WSetForcePowerState')))
    elif case['state']in(0x80,0x81):
        if case['channelByte']==0:checks.update(channelEnd=state==0x84,countersCleared=common.w(cpu,base+0x408)==0 and common.w(cpu,base+0x40c)==0)
        else:
            flash=named('FLASH_VerifyCheckSum');checks['actualFlashVerifier']=bool(flash)
            if flash and flash[-1]['outgoingR0']!=0:checks['flashError']=state==0x84 and common.h(cpu,base+0x41a)==14
            elif flash:checks.update(actualMeasurementTimeout=any(r['arguments'][:2]==[case['time'],0x027edad4]for r in named('SetupTimeOut')),measurementStarted=state==0x82)
    else:expected=[];checks['unhandledStatePreserved']=state==case['state']
    if expected is not None:checks['independentOrderedOwnStores']=own==expected
    checks['actualTaskReschedule']=[r['arguments'][:2]for r in named('AddTask')if execute<=r['returnPc']<execute+extent]==([[2,5]]if state!=0 else[])
    return dict(case=case,actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,registers=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),pc=cpu.reg_read(UC_ARM_REG_PC),orderedNonstackWrites=writes,ownedNonstackWrites=own,actualDeclaredHelperReturns=helpers,actualSetupEntryReturns=meta['prerequisiteReturns'],visited=sorted(set(pc for pc in visited if execute<=pc<execute+extent)),instructions=len(visited),memorySha256={hex(a):hashlib.sha256(cpu.mem_read(a,n)).hexdigest()for a,n in meta['regions'].items()},providerReplacements=[],syntheticMmioInput=dict(address='0x0480819c',halfword=case['hardwareStatus']),sourceCredit=0,sourceLinkedCallback=None if linked_callback is None else dict(address='0x27edad4',bytes=44,sha256=hashlib.sha256(linked_callback).hexdigest(),additionalCredit=0,asynchronousCallbackExecutionUnproved=True),physicalRadioTimingFlashTransportAndConcurrencyUnproved=True)

def cases():
    base=dict(mode=0,offset=0,state=0x82,counter=0,cca=0,channelIndex=0,channelByte=0,hardwareStatus=0,power=0,backupCca=0,backupEd=0,status=0,time=1,ccaMode=0,edThreshold=0);rows=[]
    for mode,offset in itertools.product((0,2),(0,4)):
        local=dict(base,mode=mode,offset=offset);rows.extend(dict(local,state=s)for s in(0,1,0x7f,0x85,65535))
        rows.extend(dict(local,counter=c,cca=a,hardwareStatus=hw,channelIndex=ch)for c,a,hw,ch in itertools.product((0,1,0x80000000,0xffffffff),(0,1,0x80000000,0xffffffff),(0,1,65535),(0,15)))
        rows.extend(dict(local,state=0x83,counter=c,cca=a,channelIndex=i,channelByte=b)for c,a,i,b in itertools.product((0,1,0x80000000,0xffffffff),(0,1,0x80000000,0xffffffff),(0,15),(0,1,14,255)))
        rows.extend(dict(local,state=0x84,channelIndex=i,status=s,power=p,backupCca=0xab,backupEd=0xcd)for i,s,p in itertools.product((0,1,15,16,65535),(0,14,65535),(0,0x8000,65535)))
        rows.extend(dict(local,state=s,channelIndex=i,channelByte=b)for s,i,b in itertools.product((0x80,0x81),(0,15),(0,1,14,255)))
    return rows

def main():
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();results=[]
    for i,c in enumerate(cases()):results.append(run(main,wram,c,i))
    raw=json.dumps(results,sort_keys=True,separators=(',',':')).encode();compressed=gzip.compress(raw,mtime=0);trace=ROOT/'work/arm7-bulk-20261030/sdk356-measure-task-native/native-cases.json.gz';trace.parent.mkdir(parents=True,exist_ok=True);trace.write_bytes(compressed);failed=[dict(index=i,case=r['case'],checks=r['modelChecks'])for i,r in enumerate(results)if r['actualOwnReturn']and not r['modelPassed']];unsupported=[r for r in results if not r['actualOwnReturn']];report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),address=hex(TOP),bytes=SIZE,attemptedCases=len(results),actualOwnReturns=sum(r['actualOwnReturn']for r in results),actualDeclaredHelperReturns=sum(len(r.get('actualDeclaredHelperReturns',[]))for r in results),failedModels=failed,unsupported=unsupported,nativeTrace=dict(path=trace.relative_to(ROOT).as_posix(),compressedSha256=sha256(trace),rawSha256=hashlib.sha256(raw).hexdigest()),sourceCredit=0,providerReplacements=[],actualReturnsNotBoundaryStops=True,postFaultStateCredit=0);write_json(ROOT/'evidence/attempts/arm7-sdk356-measure-task-native-20261102.json',report);print(json.dumps(dict(attempted=len(results),actualReturns=report['actualOwnReturns'],failedModels=len(failed),unsupported=len(unsupported),sourceCredit=0)),flush=True)

if __name__=='__main__':main()
