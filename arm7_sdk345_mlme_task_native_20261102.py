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
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR
import arm7_sdk306_task_command_context_20261102 as context
from project import ROOT,sha256,write_json

SIZES={0x027ed220:496,0x027ed474:160}
WATCH={0x037f9238:'WSetStaState',0x027ead5c:'WL_ReadByte',0x027f4d38:'FLASH_VerifyCheckSum',0x027e990c:'WSetChannel',0x037f8de0:'WStart',0x027f1b5c:'MakeProbeReqFrame',0x027f1088:'TxManCtrlFrame',0x027eaaf8:'SetupTimeOut',0x037f9198:'WStop',0x027edb20:'IssueMlmeConfirm',0x037f8598:'AddTask'}

def half(cpu,a,v):cpu.mem_write(a,struct.pack('<H',v&65535))
def word(cpu,a,v):cpu.mem_write(a,struct.pack('<I',v&0xffffffff))
def h(cpu,a):return int.from_bytes(cpu.mem_read(a,2),'little')
def w(cpu,a):return int.from_bytes(cpu.mem_read(a,4),'little')

def prepare(main,wram,case,index):
    cpu,meta=context.setup(main,wram,index,mode=case['mode'],offset=case['offset'],heap=True);base=meta['context'];allocation=context.base.call(cpu,0x037f886c,[base+512,384]);meta['prerequisiteReturns'].append(dict(name='actual-request-heap-allocation',**allocation));req=allocation['outgoingR0']
    if not req:raise ValueError('Real request allocation prerequisite failed')
    cpu.mem_write(req+12,bytes(384));cfm=req+80;word(cpu,base+0x41c,req);word(cpu,base+0x420,cfm);word(cpu,base+1060,req);half(cpu,base+1064,1);half(cpu,base+0x34c,16);half(cpu,base+0x404,case['state']);half(cpu,base+0x408,case['result']);half(cpu,base+0x40a,case['channelCount']);half(cpu,base+0x40e,case['elapsed']);half(cpu,base+0x410,case['period']);half(cpu,req+12,2 if case['entry']==0x027ed220 else 3);half(cpu,req+14,32);half(cpu,req+0x10,case['period']);half(cpu,req+0x38,case['scanType']);half(cpu,req+0x4a,case['period']);cpu.mem_write(req+0x3a,bytes([case['channel']])+bytes(15));half(cpu,cfm,2 if case['entry']==0x027ed220 else 3);half(cpu,cfm+2,128);half(cpu,cfm+4,0xa55a);return cpu,meta,dict(request=req,confirmation=cfm)

def run(main,wram,case,index,body=None,virtual_address=None,linked_bodies=None):
    cpu,meta,pointers=prepare(main,wram,case,index);base=meta['context'];top=case['entry'];size=SIZES[top];execute=top if virtual_address is None else virtual_address
    for entry,closed in(linked_bodies or{}).items():
        expected={0x027ed220:496,0x027ed474:160,0x027ed410:100,0x027ed514:60,0x027edad4:44}.get(entry)
        if expected!=len(closed)or main[entry-context.base.MAIN:entry-context.base.MAIN+len(closed)]!=closed:raise ValueError('Only full byte-identical source-linked selected MLME units are permitted')
        cpu.mem_write(entry,closed)
    if body is not None:
        if virtual_address is None and len(body)!=size or virtual_address is not None and not 0<len(body)<=0x1000:raise ValueError('Complete own positive extent or explicit bounded wrong-C mapping required')
        if virtual_address is not None:size=len(body)
        if virtual_address is not None:cpu.mem_map(virtual_address,0x1000)
        cpu.mem_write(execute,body)
    rng=random.Random(0x345000+index);initial=[rng.getrandbits(32)for unused in REGISTERS];initial[-2:]=[context.base.STACK+0x3800,context.base.STOP];cpu.reg_write(UC_ARM_REG_CPSR,0x13|((index%4)<<6))
    for reg,value in zip(REGISTERS,initial):cpu.reg_write(reg,value)
    active=[];helpers=[];writes=[];own=[];visited=[];returned=[False]
    def code(machine,pc,width,user):
        while active and pc==active[-1]['returnPc']and machine.reg_read(REGISTERS[-2])==active[-1]['sp']:
            row=active.pop();row.update(actualReturn=True,outgoingR0=machine.reg_read(REGISTERS[0]));helpers.append(row)
        if pc==context.base.STOP:
            if active:raise ValueError('Whole task returned with unfinished observed original helper')
            returned[0]=True;machine.emu_stop();return
        if not(context.base.MAIN<=pc<context.base.MAIN+len(main)or context.base.WRAM<=pc<context.base.WRAM+len(wram)or virtual_address is not None and execute<=pc<execute+size):raise ValueError('Task escaped current original initialized code')
        if pc in WATCH:active.append(dict(name=WATCH[pc],entry=hex(pc),arguments=[machine.reg_read(r)for r in REGISTERS[:4]],returnPc=machine.reg_read(REGISTERS[-1])&~1,sp=machine.reg_read(REGISTERS[-2])))
        visited.append(pc)
    def write(machine,access,address,width,value,user):
        if context.base.STACK<=address<context.base.STACK+0x4000:return
        row=[address,width,value&((1<<(8*width))-1)];writes.append(row)
        if execute<=machine.reg_read(UC_ARM_REG_PC)<execute+size:own.append(row)
    tokens=[cpu.hook_add(UC_HOOK_CODE,code),cpu.hook_add(UC_HOOK_MEM_WRITE,write)];error=None
    try:cpu.emu_start(execute,context.base.STOP+4,count=300000)
    except Exception as exc:error=type(exc).__name__+':'+str(exc)
    finally:
        for token in tokens:cpu.hook_del(token)
    if not returned[0]:return dict(case=case,actualOwnReturn=False,error=error or'instruction-bound exhaustion',pc=hex(cpu.reg_read(UC_ARM_REG_PC)),instructions=len(visited),sourceCredit=0,postFaultStateCredit=0)
    checks=dict(calleeSaved=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in list(range(4,12))+[13,14]),modeAndInterruptControl=(cpu.reg_read(UC_ARM_REG_CPSR)&255)==(0x13|((index%4)<<6)),noProviders=True)
    state=h(cpu,base+0x404);cfm=pointers['confirmation'];name_args=lambda name:[r['arguments']for r in helpers if r['name']==name]
    if top==0x027ed474:
        if case['state']==32:checks.update(joinState=state==33,joinResults=h(cpu,base+0x408)==0 and h(cpu,base+0x40a)==0,actualTimeoutArgument=any(a[:2]==[case['period'],0x027ed514]for a in name_args('SetupTimeOut')),actualInstalledPointer=w(cpu,base+0x634)==0x027ed514)
        elif case['state']==37:checks.update(joinCompletion=state==0,confirmation=h(cpu,cfm+4)==case['result']and h(cpu,cfm+6)==case['channelCount'],actualStopConditional=bool(name_args('WStop'))==(case['result']!=0),actualConfirmDelivery=bool(name_args('IssueMlmeConfirm')))
        else:checks['defaultStateNoOwnWrites']=state==case['state']and not own
    else:
        if case['state']in(18,19):
            if name_args('SetupTimeOut'):checks.update(scanState=state==19,actualTimeoutArgument=any(a[:2]==[case['period'],0x027ed410]for a in name_args('SetupTimeOut')),actualInstalledPointer=w(cpu,base+0x634)==0x027ed410)
            else:checks.update(activeAllocationFailure=case['scanType']==0 and state==21 and h(cpu,cfm+4)==8,actualFollowup=any(a[:2]==[2,0]for a in name_args('AddTask')))
        elif case['state']in(16,17):
            reads=name_args('WL_ReadByte');checks['actualChannelAddress']=bool(reads)and reads[0][0]==pointers['request']+0x3a+(0 if case['state']==16 else case['channelCount'])
            if case['channel']==0:checks.update(channelEnd=state==21,actualFollowup=any(a[:2]==[2,0]for a in name_args('AddTask')))
            else:
                flash=[r for r in helpers if r['name']=='FLASH_VerifyCheckSum'];checks['actualFlashOutcome']=bool(flash)
                if flash and flash[-1]['outgoingR0']!=0:checks.update(flashRejection=state==21 and h(cpu,cfm+4)==14,actualFollowup=any(a[:2]==[2,0]for a in name_args('AddTask')))
        elif case['state']==21:checks.update(scanComplete=state==0,restoredConfiguredMode=h(cpu,base+0x350)==h(cpu,base+0x32e),actualConfirmDelivery=bool(name_args('IssueMlmeConfirm')))
        else:checks['defaultStateNoOwnWrites']=state==case['state']and not own
    return dict(case=case,actualOwnReturn=True,modelChecks=checks,modelPassed=all(checks.values()),registers=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),pc=cpu.reg_read(UC_ARM_REG_PC),orderedNonstackWrites=writes,ownedNonstackWrites=own,actualDeclaredHelperReturns=helpers,actualSetupEntryReturns=meta['prerequisiteReturns'],visited=sorted(set(pc for pc in visited if execute<=pc<execute+size)),instructions=len(visited),memorySha256={hex(a):hashlib.sha256(cpu.mem_read(a,n)).hexdigest()for a,n in meta['regions'].items()},pointers=pointers,sourceCredit=0,providerReplacements=[],sourceLinkedSelectedUnits=[dict(entry=hex(a),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())for a,b in sorted((linked_bodies or{}).items())],syntheticContextAndDirectTaskLaunch=True,physicalAlarmDispatchAndSceneReachabilityUnproved=True)

def cases():
    rows=[];base=dict(entry=0x027ed220,mode=0,offset=0,state=19,scanType=1,channel=0,channelCount=0,elapsed=0,period=1,result=0)
    for mode,offset in itertools.product((0,2),(0,4)):
        rows.extend(dict(base,mode=mode,offset=offset,state=state,scanType=kind,period=period)for state,kind,period in itertools.product((0,15,16,17,18,19,21,65535),(0,1),(0,1,65535)))
        rows.extend(dict(base,entry=0x027ed474,mode=mode,offset=offset,state=state,period=period,result=result,channelCount=status)for state,period,result,status in itertools.product((0,31,32,33,37,65535),(0,1,65535),(0,1,7,65535),(0,65535)))
    return rows

def main():
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();results=[]
    for i,c in enumerate(cases()):
        r=run(main,wram,c,i);results.append(r)
        if r.get('actualOwnReturn')and not r['modelPassed']:raise ValueError(dict(index=i,case=c,checks=r['modelChecks']))
    raw=json.dumps(results,sort_keys=True,separators=(',',':')).encode();packed=gzip.compress(raw,mtime=0);path=ROOT/'work/arm7-bulk-20261030/sdk345-mlme-task-native/native-cases.json.gz';path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(packed);report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),attemptedCases=len(results),actualOwnReturns=sum(r['actualOwnReturn']for r in results),unsupported=[r for r in results if not r['actualOwnReturn']],actualDeclaredHelperReturns=sum(len(r.get('actualDeclaredHelperReturns',[]))for r in results),nativeTrace=dict(path=path.relative_to(ROOT).as_posix(),compressedSha256=sha256(path),rawSha256=hashlib.sha256(raw).hexdigest()),sourceCredit=0,providers=[],postFaultStateCredit=0,actualWholeTaskReturnsDistinctFromHelperAndSetupReturns=True);write_json(ROOT/'evidence/attempts/arm7-sdk345-mlme-task-native-20261102.json',report);print(json.dumps({k:v for k,v in report.items()if k not in('unsupported','nativeTrace')}),flush=True)

if __name__=='__main__':main()
