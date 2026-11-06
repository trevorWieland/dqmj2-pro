import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_gpi_connect_next_peer_dispatch_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_gpi_connect_next_peer_dispatch_build import build

CONNECTED,QUEUE,SEND,PEERSEND,CLOCK=0x20affbc,0x20b01e0,0x20ac9e8,0x20aff44,0x20a8ef8
REFERENCE,CONNECTION,PEER,OPS,STOP,SP=0x2170000,0x2171000,0x2172000,0x2174000,0x27e0000,0x2701000


def vector(seed):return dict(peerPresent=seed%3!=0,outLen=(seed//3)%2,count=seed%6,finishedMask=(seed//6)%32)


def run(image,row,body,v,seed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000)
    peer=bytearray([0x88]*80);struct.pack_into('<I',peer,8,0x7f000001);struct.pack_into('<H',peer,12,12345);struct.pack_into('<I',peer,52,v['outLen']);head=OPS if v['count'] else 0;last=OPS+(v['count']-1)*24 if v['count'] else 0;struct.pack_into('<III',peer,64,head,head,last);ops=bytearray()
    for i in range(5):ops.extend(struct.pack('<6I',2 if v['finishedMask']&(1<<i) else 0,0x1234,0x2178001,OPS+(i+1)*24 if i+1<v['count'] else 0,104,0x12345678))
    memory={REFERENCE:struct.pack('<I',CONNECTION),CONNECTION:bytes([0x77])*0x600,PEER:bytes(peer),OPS:bytes(ops)}
    for at,data in memory.items():cpu.mem_write(at,data)
    if a==CONNECTED:
        args=[REFERENCE,PEER if v['peerPresent'] else 0];expected=dict(kind='return',value=3) if not v['peerPresent'] else dict(kind='provider',address=hex(SEND if v['outLen'] else PEERSEND))
    else:
        args=[REFERENCE,PEER];pending=any(not v['finishedMask']&(1<<i) for i in range(max(0,v['count']-1)));expected=dict(kind='provider',address=hex(CLOCK)) if pending else dict(kind='return')
    initial=[(0x55cc0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[:2]=args;initial[-2:]=[SP,STOP|1]
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;pcs=[];interface=True
    def code(machine,at,size,user):
        nonlocal observed,interface
        regs=[machine.reg_read(r) for r in C.REGISTERS]
        if at==STOP:
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Actual peer-dispatch return ABI differs')
            observed=dict(kind='return') if a==QUEUE else dict(kind='return',value=regs[0]);machine.emu_stop();return
        if at in [SEND,PEERSEND,CLOCK]:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Actual dispatch provider Thumb mode differs')
            observed=dict(kind='provider',address=hex(at))
            if at==PEERSEND:interface=regs[:2]==[REFERENCE,PEER]
            elif at==SEND:
                ptr,flag=struct.unpack('<II',machine.mem_read(regs[13],8));interface=regs[:4]==[REFERENCE,0x7f000001,12345,PEER+44] and SP-0x100<=ptr<SP and flag==1
            machine.emu_stop();return
        if not a<=at<a+row['bytes'] or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Peer-dispatch escaped bounded code/mode')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not(SP-0x4000<=at and at+size<=SP):raise ValueError('Unexpected dispatch/queue RAM write')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=10000)
    if observed is None:raise ValueError('Dispatch/queue did not reach actual bounded return/provider')
    guards=all(bytes(cpu.mem_read(at,len(data)))==data for at,data in memory.items())
    return dict(address=row['address'],seed=seed,vector=v,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and guards and interface,providerInterfaceModelPassed=interface,independentMutationModelPassed=guards,actualOriginalHelperInvocations=0,providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[];negative=[]
    variants={CONNECTED:('return GP_NETWORK_ERROR;','return (GP_NETWORK_ERROR-1);'),QUEUE:('anIterator != peer->peerOpQueue.last','anIterator == peer->peerOpQueue.last')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed in range(128):
            v=vector(seed);original=run(image,row,native,v,seed);source=run(image,row,linked,v,seed)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent dispatch/queue gate model differs',original,source))
            records.append(original)
        folder=WORK/'fixtures'/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        wrong=folder/'match.c';text=(ROOT/row['source']).read_text();old,new=variants[a];changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole dispatch/queue wrong-C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Whole dispatch/queue wrong-C extent differs',row['address'],bad['compiledBytes']))
        failures=[]
        for seed in range(16):
            v=vector(seed);v.update(peerPresent=False,count=2,finishedMask=0);result=run(image,row,body,v,seed)
            if result['modelPassed']:raise ValueError('Whole dispatch/queue wrong-C accepted independent model')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],records=failures))
    limits=['Two complete ordinary C peer dispatch/timeout-queue callers660B genuinely match original whole extents/imports and actual ASCII/NOFILE configuration. Peer80/queue12/op24/recvmessage12(date4,message8)/keys16/compiler layouts retained;0external allocation/storage extent/authorship credit.','256paired actual entries independently cover dispatchnull/error3,send/peer-send provider frames,and NONNULL-PEER queue empty/first==last/all-finished skipped-last iteration returns versus first unfinished node pre-clock stops.0synthetic returns.','Clock/send/peer-send/read-message/parser/allocator/duplicate/callback/UDP bodies and post-provider timeout/response/payload effects remain unexecuted;0complete nonnull connected-peer dispatch returns.2sameextent whole wrong-C variants genuinely link and violate32independent return/queue models;2wrong queue layouts plus original binding negatives reject.0network/device/game/nativeWindows execution.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=0,wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
