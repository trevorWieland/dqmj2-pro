import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json,sha256
from wave20261105_gamespy_thumb_next_lan_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-thumb-next/lan'
WORK=ROOT/'work/w5gt/lan/fixtures'
LIST,DATA,STOP,SP=0x2170000,0x2172000,0x27e0000,0x2701000


def boundary(image,row,body,v,seed):
    address=int(row['address'],0);target=0x20a7390 if address==0x20a834c else 0x20a8d88
    cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(address,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000)
    state=bytearray(2012);struct.pack_into('<I',state,0,2);struct.pack_into('<II',state,1716,v['socket']&0xffffffff,0x12345678);cpu.mem_write(LIST,bytes(state));payload=bytes(range(128));cpu.mem_write(DATA,payload)
    initial=[(0x55880000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1];initial[0]=LIST
    if address==0x20a834c:initial[:4]=[LIST,v['ip'],v['port'],DATA];cpu.mem_write(SP,struct.pack('<I',v['length']))
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    pcs=[];capture=None
    def code(machine,at,size,user):
        nonlocal capture
        if at==target:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Original I/O boundary mode differs')
            registers=[machine.reg_read(reg) for reg in C.REGISTERS];pointer=registers[1]
            if address==0x20a834c and not SP-0x4000<=pointer<=SP-9:raise ValueError('Request buffer outside local caller stack')
            capture=dict(target=hex(target),mode='thumb',incomingRegisters=registers[:4],callerSp=hex(registers[13]),callerLr=hex(registers[14]),requestHeader=bytes(machine.mem_read(pointer,9)).hex() if address==0x20a834c else None);machine.emu_stop();return
        if not address<=at<address+row['bytes'] or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('I/O boundary escaped original Thumb caller')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not SP-0x4000<=at or at+size>SP:raise ValueError(('Unexpected message/LAN write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(address|1,STOP+4,count=4000)
    if capture is None:raise ValueError('Genuine I/O boundary not reached')
    correct=bytes(cpu.mem_read(LIST,len(state)))==bytes(state) and bytes(cpu.mem_read(DATA,len(payload)))==payload
    if address==0x20a834c:
        expected=struct.pack('>H',(v['length']+9)&0xffff)+bytes([2])+struct.pack('<IH',v['ip'],v['port']);correct=correct and capture['incomingRegisters'][0]==LIST and capture['incomingRegisters'][2]==9 and capture['requestHeader']==expected.hex()
    else:correct=correct and capture['incomingRegisters'][0]==v['socket']&0xffffffff
    return dict(address=row['address'],vector=v,seed=seed,scope='entry-through-instructions-before-original-I/O-helper',callerReturned=False,stoppedBeforeHelperInstruction=True,helperInstructionsExecuted=0,modelPassed=bool(correct),capture=capture,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();stops=[];negative=[]
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        if a==0x20a834c:
            vectors=[dict(socket=7,ip=ip,port=port,length=n) for ip in [0,0xffffffff,0x11223344] for port in [0,0xabcd] for n in [0,100]];old,new='requestBuffer[2] = SEND_MESSAGE_REQUEST','requestBuffer[2] = 3'
        elif a==0x20a8480:vectors=[dict(socket=s) for s in [-1,0,7,0x7fffffff] for repeat in range(4)];old,new='slist->slsocket','slist->lanstarttime'
        else:raise ValueError('Unqualified message/LAN caller')
        for seed,v in enumerate(vectors):
            original=boundary(image,row,native,v,seed);source=boundary(image,row,linked,v,seed)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent message/LAN boundary model differs',original,source))
            stops.append(original)
        folder=WORK/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;text=source.read_text();changed=text.replace(old,new,1)
        if text==changed:raise ValueError('Whole message/LAN C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError('Wrong whole message/LAN C extent changed')
        failures=[]
        for seed in range(16):
            result=boundary(image,row,body,vectors[-1],seed)
            if result['modelPassed']:raise ValueError('Whole wrong C did not violate independent I/O boundary model')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),sourceDependencies=bad['sourceDependencies'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],modelRejections=len(failures),records=failures))
    limits=['Both complete ordinary C callers genuinely link exactly over every native byte and unchanged original relocation. Actual entry instructions stop before the original canonical Thumb SendWithRetry/CanReceive helper first instruction. No caller return or I/O helper body executes.','Independent9-byte message model checks big-endian total length, type2, raw network-order IP/port words, payload/list preservation and three outgoing arguments. LAN model checks the signed socket field at list offset1716. Two genuine same-extent whole wrong C units violate these partial boundary models.','Actual socket traffic, send/retry outcomes, receive loop, server allocation/insertion, elapsed-time branch, callbacks, device behavior, external object storage extent/authorship and full game execution remain unexecuted/uncredited.']
    trace=hashlib.sha256(json.dumps(stops,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=[],boundaryRecords=stops,nativeAndCompiledReturningCalls=0,actualNativeCalleeBodiesExecuted=0,wholeCNegativeControlsRejected=0,wrongC=[],boundaryWholeCNegativeControlsRejected=len(negative),boundaryWrongC=negative,actualNativeAndSourceEntryToKernelStops=2*len(stops),boundaryCallerReturns=0,boundaryHelperInstructions=0,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
