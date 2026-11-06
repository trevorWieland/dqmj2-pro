import hashlib
import json
import random
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_browser_query_next_query_start_qualified_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_browser_query_next_query_start_qualified_build import build

ENGINE,SERVER,STOP,SP=0x2170000,0x2172000,0x27e0000,0x2701000
TIME,SEND=0x20a8ef8,0x20a8c34


def state(v):
    engine=bytearray([0xcc]*76);server=bytearray([0xdd]*44);struct.pack_into('<iii',engine,0,v['version'],8,0);struct.pack_into('<i',engine,32,77);struct.pack_into('<I',engine,40,v['engineip']);engine[44:64]=bytes((i*13+7)&255 for i in range(20));struct.pack_into('<i',engine,64,v['keys']);struct.pack_into('<IHIH',server,0,v['publicip'],v['publicport'],v['privateip'],v['privateport']);struct.pack_into('<I',server,8,v['privateip']);struct.pack_into('<H',server,12,v['privateport']);server[20:22]=bytes([v['state'],v['flags']]);struct.pack_into('<II',server,28,0xabcdef01,v['challenge']);return engine,server


def model(v,image):
    if v['state']&32:return dict(kind='modeled-timer-caller-return',updatetime=0)
    if v['version']==1:
        payload=bytes([254,253,9 if v['state']&128 else 0])+struct.pack('<I',v['tick'])
        if not v['state']&128:
            if v['challenge']:payload+=struct.pack('>I',v['challenge'])
            payload+=bytes([v['keys']])+bytes((i*13+7)&255 for i in range(v['keys']))+bytes(2) if v['state']&4 else bytes([255,255,255,1])
    else:payload=image[0xe02d4:0xe02d4+13] if v['state']&4 else image[0xe02e4:0xe02e4+8]
    private=v['publicip']==v['engineip'] and v['flags']&2;ip=v['privateip'] if private else v['publicip'];port=v['privateport'] if private else v['publicport'];return dict(kind='send-boundary',payload=payload.hex(),socket=77,flags=0,sockaddrLength=8,sockaddrFields=(bytes([2])+struct.pack('<HI',port,ip)).hex(),updatetime=v['tick'])


def run(image,row,body,v,seed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);engine,server=state(v);cpu.mem_write(ENGINE,bytes(engine));cpu.mem_write(SERVER,bytes(server));initial=[(0x55dd0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1];initial[:2]=[ENGINE,SERVER]
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    pcs=[];time_injections=0;observed=None
    def code(machine,at,size,user):
        nonlocal time_injections,observed
        if at==TIME:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32 or time_injections:raise ValueError('Modeled time boundary kind/mode/count differs')
            time_injections+=1;machine.reg_write(ar.UC_ARM_REG_R0,v['tick']);machine.reg_write(ar.UC_ARM_REG_PC,machine.reg_read(ar.UC_ARM_REG_LR));return
        if at==SEND:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Send stop target mode differs')
            regs=[machine.reg_read(r) for r in C.REGISTERS];sockaddr,length=struct.unpack('<II',bytes(machine.mem_read(regs[13],8)));observed=dict(kind='send-boundary',payload=bytes(machine.mem_read(regs[1],regs[2])).hex(),socket=regs[0],flags=regs[3],sockaddrLength=length,sockaddrFields=bytes(machine.mem_read(sockaddr+1,7)).hex(),updatetime=struct.unpack('<I',bytes(machine.mem_read(SERVER+28,4)))[0]);machine.emu_stop();return
        if at==STOP:
            regs=[machine.reg_read(r) for r in C.REGISTERS]
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Modeled-time caller return ABI differs')
            observed=dict(kind='modeled-timer-caller-return',updatetime=struct.unpack('<I',bytes(machine.mem_read(SERVER+28,4)))[0]);machine.emu_stop();return
        if not a<=at<a+row['bytes'] or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError(('Query caller escaped before original send boundary',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not (SP-0x4000<=at and at+size<=SP or SERVER+28<=at and at+size<=SERVER+32):raise ValueError(('Query unexpected write before send boundary',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=10000)
    if observed is None or time_injections!=1:raise ValueError('Query did not reach bounded caller stop')
    engine_guard=bytes(cpu.mem_read(ENGINE,76))==bytes(engine);got=bytes(cpu.mem_read(SERVER,44));server_guard=got[:28]==bytes(server[:28]) and got[32:]==bytes(server[32:]);expected=model(v,image)
    return dict(address=row['address'],vector=v,seed=seed,observed=observed,expected=expected,modelPassed=observed==expected and engine_guard and server_guard,modeledTimeReturnsInjected=1,actualOriginalHelperInvocations=0,actualOriginalHelperInstructionExecutions=0,authenticCompleteCallerReturned=False,engineAndServerGuardsPreserved=engine_guard and server_guard,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def vectors():
    values=[];rng=random.Random(0x58dc)
    for version in [0,1,2]:
        for flags in [0,2]:
            for state_value in [0,4,8,32,128,132,136,160]:
                for challenge in [0,0x01020304]:
                    i=len(values);values.append(dict(version=version,flags=flags,state=state_value,challenge=challenge,keys=i%21,tick=[0,1,0x12345678,0xffffffff][i%4],engineip=0x01020304,publicip=0x01020304 if i%3 else 0x87654321,publicport=0x8765,privateip=0xc0a80105,privateport=0x1234))
    return values+[dict(version=rng.randrange(3),flags=rng.randrange(256),state=rng.randrange(256),challenge=rng.getrandbits(32),keys=rng.randrange(21),tick=rng.getrandbits(32),engineip=0x01020304,publicip=0x01020304 if i%2 else 0x11223344,publicport=rng.randrange(65536),privateip=rng.getrandbits(32),privateport=rng.randrange(65536)) for i in range(32)]+[dict(version=1,flags=2,state=4,challenge=c,keys=n,tick=0x12345678,engineip=0x01020304,publicip=0x01020304,publicport=0x8765,privateip=0xc0a80105,privateport=0x1234) for n in range(21) for c in [0,0x01020304]]


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[];negative=[]
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed,v in enumerate(vectors()):
            original=run(image,row,native,v,seed);source=run(image,row,linked,v,seed)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent modeled-time query payload model differs',original,source))
            records.append(original)
        folder=WORK/'fixtures'/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;text=source.read_text();changed=text.replace('queryBuffer[pos++] = 0x09;','queryBuffer[pos++] = 0x08;',1)
        if changed==text:raise ValueError('Whole query challenge C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError('Wrong whole query C changed native extent')
        failures=[];chosen=[v for v in vectors() if v['version']==1 and v['state']&128 and not v['state']&32][:16]
        for seed,v in enumerate(chosen):
            result=run(image,row,body,v,seed)
            if result['modelPassed']:raise ValueError('Wrong query opcode did not fail independent modeled-time payload')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],modeledBoundaryFailures=len(failures),records=failures))
    limits=['Actual complete408-byte ordinary C extent and all original relocations genuinely link; byte-copy loop shape, nonzero success condition and volatile local stack accesses preserve measured native behavior.','Only caller instructions execute. At original canonical current_time first instruction an explicitly modeled scalar return is injected without executing helper code. Packet construction then stops BEFORE original sendto first instruction; ICMP-disabled paths return after that modeled time injection. Authentic complete caller executions/helper bodies/network/device/scenes are0.','170 deterministic edge/random input vectors compare native and genuine compiled caller-only traces against an independent QR2 challenge/basic/full and GOA raw-string payload/routing model, including measured32-bit timestamp, optional network-byte-order challenge,0..20 keys and private/public IP/16-bit port selection. Uninitialized sockaddr byte0 is deliberately not claimed.','One same-extent whole wrong C challenge opcode genuinely links and violates16 independent modeled-boundary cases. This is neither real timer/network service validation nor actual game/native Windows execution; external strings/object storage authorship and helper source remain uncredited.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=0,nativeAndCompiledPartialStops=2*sum(r['observed']['kind']=='send-boundary' for r in records),actualNativeCalleeBodiesExecuted=0,modeledExternalTimeReturns=2*len(records),callerOnlyModeledReturns=2*sum(r['observed']['kind']=='modeled-timer-caller-return' for r in records),wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
