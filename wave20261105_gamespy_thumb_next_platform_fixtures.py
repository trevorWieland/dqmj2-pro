import hashlib
import ipaddress
import json
import random
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json,sha256
from wave20261105_gamespy_thumb_next_platform_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-thumb-next/platform'
WORK=ROOT/'work/w5gt/platform/fixtures'
INPUT,ADDR,LENGTH,READ,WRITE,EXCEPT,STOP,SP=0x2170000,0x2172000,0x2174000,0x2175000,0x2175100,0x2175200,0x27e0000,0x2701000
NETWORKS=[ipaddress.IPv4Network(s) for s in ['10.0.0.0/8','172.16.0.0/12','192.168.0.0/16']]


def cpu_at(image,address,body,seed):
    cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(address,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000)
    initial=[(0x55660000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    return cpu,initial


def private_ip(image,row,body,v,seed):
    address=int(row['address'],0);cpu,initial=cpu_at(image,address,body,seed);data=bytes.fromhex(v['data'])+bytes([0xcc])*60;cpu.mem_write(INPUT,data);initial[0]=INPUT
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    pcs=[];returned=False
    def code(machine,at,size,user):
        nonlocal returned
        if at==STOP:returned=True;machine.emu_stop();return
        if not address<=at<address+row['bytes'] or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Private IP fixture escaped original Thumb caller')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not SP-0x4000<=at or at+size>SP:raise ValueError('Private IP fixture wrote outside stack')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(address|1,STOP+4,count=1000);regs=[cpu.reg_read(r) for r in C.REGISTERS]
    if not returned or regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Private IP return/callee-saved ABI differs')
    ip=ipaddress.IPv4Address(bytes.fromhex(v['data']));expected=int(any(ip in network for network in NETWORKS));actual=bytes(cpu.mem_read(INPUT,len(data)))
    return dict(address=row['address'],vector=v,seed=seed,topReturned=True,calleeSavedAbiPreserved=True,returnValue=regs[0],modelPassed=regs[0]==expected and actual==data,actualOriginalHelperInvocations=0,initialCallerExcludedFromHelperMetric=True,memorySha256=hashlib.sha256(actual).hexdigest(),pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def private_cases():
    values=[bytes([n,17,34,51]) for n in range(256)];values += [bytes([a,b,0,1]) for a in [10,11,172,192] for b in [0,15,16,31,32,167,168,169,255]]
    rng=random.Random(0x1105);values += [bytes(rng.randrange(256) for i in range(4)) for n in range(64)]
    return [dict(data=v.hex()) for v in values]


def boundary(image,row,body,v,seed):
    address=int(row['address'],0);cpu,initial=cpu_at(image,address,body,seed);sockaddr=bytes([0xee,2,0x34,0x12,10,1,2,3]);regions={ADDR:sockaddr,LENGTH:struct.pack('<I',v.get('length',8)&0xffffffff),INPUT:bytes([0xaa])*64,READ:struct.pack('<I',0xdeadbeef),WRITE:struct.pack('<I',0xdeadbeef),EXCEPT:struct.pack('<I',0xdeadbeef)};expected=dict(regions)
    for at,data in regions.items():cpu.mem_write(at,data)
    if address==0x20a8c00:
        target=0x2090378;initial[:4]=[v['socket']&0xffffffff,INPUT,64,0x123];cpu.mem_write(SP,struct.pack('<II',ADDR,LENGTH));changed=bytearray(sockaddr);changed[0]=v['length']&255;expected[ADDR]=bytes(changed)
    elif address==0x20a8c68:
        target=0x20904ec;initial[:4]=[v['socket']&0xffffffff,ADDR,LENGTH,0x777];changed=bytearray(sockaddr);changed[0]=v['length']&255;expected[ADDR]=bytes(changed)
    elif address==0x20a8ca8:target=0x20907f4;initial[:4]=[v['socket']&0xffffffff,READ if v['read'] else 0,WRITE if v['write'] else 0,EXCEPT if v['except'] else 0]
    else:raise ValueError('Unqualified SDK boundary')
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    pcs=[];stopped=False;capture=None
    def code(machine,at,size,user):
        nonlocal stopped,capture
        if at==target:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('SDK entry mode differs')
            stopped=True;registers=[machine.reg_read(reg) for reg in C.REGISTERS];stack=registers[13]
            capture=dict(target=hex(target),mode='thumb',incomingRegisters=registers[:4],callerSp=hex(stack),callerLr=hex(registers[14]),localPollFd=bytes(machine.mem_read(registers[0],8)).hex() if address==0x20a8ca8 else None,stackArgument=struct.unpack('<I',machine.mem_read(stack,4))[0] if address==0x20a8c00 else None)
            machine.emu_stop();return
        if not address<=at<address+row['bytes'] or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('SDK boundary escaped original Thumb caller')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        allowed=SP-0x4000<=at and at+size<=SP
        if address in (0x20a8c00,0x20a8c68) and ADDR<=at and at+size<=ADDR+8:allowed=True
        if not allowed:raise ValueError(('SDK-boundary unexpected write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(address|1,STOP+4,count=1000)
    if not stopped:raise ValueError('Original SDK boundary not reached')
    correct=all(bytes(cpu.mem_read(a,len(value)))==expected[a] for a,value in regions.items());registers=capture['incomingRegisters'];correct=correct and registers[0]==v['socket']&0xffffffff if address!=0x20a8ca8 else correct
    if address==0x20a8c00:correct=correct and registers[1:]==[INPUT,64,0x123] and capture['stackArgument']==ADDR
    elif address==0x20a8c68:correct=correct and registers[1]==ADDR
    else:correct=correct and registers[1:]==[1,0,0] and bytes.fromhex(capture['localPollFd'])==struct.pack('<Ihh',v['socket']&0xffffffff,(1 if v['read'] else 0)|(8 if v['write'] else 0),0)
    return dict(address=row['address'],vector=v,seed=seed,scope='entry-through-instructions-before-canonical-SOC-helper',stoppedBeforeHelperInstruction=True,callerReturned=False,helperInstructionsExecuted=0,modelPassed=bool(correct),capture=capture,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[];negative=[];stops=[];boundary_negative=[];unsupported=[]
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        if a==0x20a8e18:
            for seed,v in enumerate(private_cases()):
                original=private_ip(image,row,native,v,seed);source=private_ip(image,row,linked,v,seed)
                if original!=source or not original['modelPassed']:raise ValueError(('Private IP independent model differs',original,source))
                records.append(original)
            old,new,v='b1 == 10','b1 == 11',dict(data=bytes([10,1,2,3]).hex())
        elif a in (0x20a8c00,0x20a8c68,0x20a8ca8):
            vectors=[dict(socket=s,length=n) for s in [-1,0,5,0x7fffffff] for n in [-1,0,8,257,0x12345678]] if a!=0x20a8ca8 else [dict(socket=s,read=bool(mask&1),write=bool(mask&2),**{'except':bool(mask&4)}) for s in [-1,0,5,0x7fffffff] for mask in range(8)]
            for seed,v in enumerate(vectors):
                original=boundary(image,row,native,v,seed);source=boundary(image,row,linked,v,seed)
                if original!=source or not original['modelPassed']:raise ValueError(('Measured socket boundary model differs',original,source))
                stops.append(original)
            if a!=0x20a8c00:continue
            old,new,v='addr->len = (u8)*fromlen','addr->family = (u8)*fromlen',dict(socket=5,length=257)
        else:unsupported.append(dict(address=row['address'],returningVectors=0,reason='Original OS_GetTick hardware path and tick conversion unexecuted'));continue
        folder=WORK/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;wrong.write_text(source.read_text());text=wrong.read_text();changed=text.replace(old,new,1)
        if text==changed:raise ValueError('Wrong complete platform C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError('Wrong complete platform C extent changed')
        failures=[]
        for seed in range(16):
            result=private_ip(image,row,body,v,seed) if a==0x20a8e18 else boundary(image,row,body,v,seed)
            if result['modelPassed']:raise ValueError('Wrong complete platform C did not violate independent model')
            failures.append(result)
        item=dict(address=row['address'],sourceSha256=sha256(wrong),sourceDependencies=bad['sourceDependencies'],genuineLink=bad['realLink'],compiledBytes=bad['compiledBytes'],modelRejections=len(failures),records=failures)
        (negative if a==0x20a8e18 else boundary_negative).append(item)
    limits=['Independent explicit RFC1918 network-membership model checks actual full Thumb IP caller returns, unchanged input, code-entry mode and callee-saved ABI; it does not use the broader Python is_private classification.','Socket receive/name/poll callers execute only up to genuine canonical SOC helper entries. No helper instruction or caller return is executed; separate byte/ABI models check8-byte address writes, fifth stack argument and signed16-bit poll layout/events/zero64-bit timeout.','Both tick wrappers have complete exact C/native/link proofs, while actual OS_GetTick hardware, elapsed time conversion returns, socket I/O, callbacks, devices/scenes and external storage extent/authorship remain unexecuted/uncredited.']
    trace=hashlib.sha256(json.dumps(dict(returns=records,boundaries=stops),sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,boundaryRecords=stops,nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=0,helperBodies=[],unsupported=unsupported,wholeCNegativeControlsRejected=len(negative),wrongC=negative,boundaryWholeCNegativeControlsRejected=len(boundary_negative),boundaryWrongC=boundary_negative,actualNativeAndSourceEntryToKernelStops=2*len(stops),boundaryCallerReturns=0,boundaryHelperInstructions=0,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
