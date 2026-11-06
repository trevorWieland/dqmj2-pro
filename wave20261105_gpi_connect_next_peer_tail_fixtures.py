import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_gpi_connect_next_peer_tail_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_gpi_connect_next_peer_tail_build import build

SEND,TRANSFER,CALLBACK,ARRAYLEN,SPRINTF,LOOKUP=0x20aff44,0x20b0600,0x20b06d0,0x20a8640,0x200616c,0x20b03c4
REFERENCE,CONNECTION,PEER,ARRAY,TID,TEXT,STOP,SP=0x2170000,0x2171000,0x2172000,0x2173000,0x2174000,0x2175000,0x27e0000,0x2701000


def vector(seed):return dict(peerPresent=seed%3!=0,outLen=(seed//3)%2,ip=(0x7f000001+seed)&0xffffffff,port=[0,1,65535,12345][seed%4],length=7+seed,reliable=seed%2,profileid=-123456789+seed,count=0xffffffff-seed,time=0x12345678+seed,messageType=seed%200)


def run(image,row,body,v,seed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000)
    peer=bytearray([0x88]*80);struct.pack_into('<I',peer,52,v['outLen']);struct.pack_into('<I',peer,60,ARRAY);memory={REFERENCE:struct.pack('<I',CONNECTION),CONNECTION:bytes([0x77])*0x600,PEER:bytes(peer),ARRAY:bytes([0xd6])*32,TID:struct.pack('<iII',v['profileid'],v['count'],v['time']),TEXT:b'payload-prefix\0',SP:struct.pack('<II',v['reliable'],REFERENCE)}
    for at,data in memory.items():cpu.mem_write(at,data)
    if a==SEND:
        args=[REFERENCE,PEER if v['peerPresent'] else 0];expected=dict(kind='return',value=3) if not v['peerPresent'] else dict(kind='return',value=0) if v['outLen'] else dict(kind='provider',address=hex(ARRAYLEN))
    elif a==TRANSFER:args=[REFERENCE,PEER,v['messageType'],TID];expected=dict(kind='provider',address=hex(SPRINTF))
    else:args=[v['ip'],v['port'],TEXT,v['length']];expected=dict(kind='provider',address=hex(LOOKUP))
    initial=[(0x55cc0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
    for i,arg in enumerate(args):initial[i]=arg&0xffffffff
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;pcs=[];interface=True
    def code(machine,at,size,user):
        nonlocal observed,interface
        regs=[machine.reg_read(r) for r in C.REGISTERS]
        if at==STOP:
            if a!=SEND or regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Actual peer-tail return ABI differs')
            observed=dict(kind='return',value=regs[0]);machine.emu_stop();return
        if at in [ARRAYLEN,SPRINTF,LOOKUP]:
            if bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(at!=SPRINTF):raise ValueError('Actual peer-tail provider ARM/Thumb mode differs')
            observed=dict(kind='provider',address=hex(at))
            if at==ARRAYLEN:interface=regs[0]==ARRAY
            elif at==SPRINTF:interface=SP-0x100<=regs[0] and regs[0]+64<=SP and regs[1:4]==[0x20e10ac,v['messageType'],v['profileid']&0xffffffff] and struct.unpack('<II',machine.mem_read(regs[13],8))==(v['count'],v['time'])
            else:interface=regs[:3]==[REFERENCE,v['ip'],v['port']]
            machine.emu_stop();return
        if not a<=at<a+row['bytes'] or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Peer-tail escaped bounded caller/mode')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not(SP-0x4000<=at and at+size<=SP):raise ValueError('Unexpected peer-tail pre-provider RAM write')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=10000)
    if observed is None:raise ValueError('Peer-tail caller failed to reach bounded return/provider')
    guards=all(bytes(cpu.mem_read(at,len(data)))==data for at,data in memory.items())
    return dict(address=row['address'],seed=seed,vector=v,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and guards and interface,providerInterfaceModelPassed=interface,independentMutationModelPassed=guards,actualOriginalHelperInvocations=0,providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[];negative=[]
    variants={SEND:('if(peer->outputBuffer.len)','if(!peer->outputBuffer.len)'),TRANSFER:('tid.count = transferID->count;','tid.count = transferID->time;'),CALLBACK:('gpiGetPeerByAddr(connection, ip, port)','gpiGetPeerByAddr(connection, messageLength, port)')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed in range(128):
            v=vector(seed);original=run(image,row,native,v,seed);source=run(image,row,linked,v,seed)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent peer-tail gate/variadic/stack model differs',original,source))
            records.append(original)
        folder=WORK/'fixtures'/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        wrong=folder/'match.c';text=(ROOT/row['source']).read_text();old,new=variants[a];changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole peer-tail wrong-C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Whole peer-tail wrong-C extent differs',row['address'],bad['compiledBytes']))
        failures=[]
        for seed in range(16):
            v=vector(seed);v.update(peerPresent=True,outLen=1);result=run(image,row,body,v,seed)
            if result['modelPassed']:raise ValueError('Whole peer-tail wrong-C accepted independent model')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],records=failures))
    limits=['Three complete ordinary C peer-tail callers336B genuinely match full native extents/all original call/data words and peer80/message24/transferID12(profile0,count4,time8)/knownminimumconnection600 views. Original growth chunk2048,not publicmodern16384,retained;0external storage allocation/authorship credit.','384paired actual entries independently cover send null-peer/error3,pending-output/return0,pre-ArrayLength frames,NONNULL transferID profile/count/time variadic printf stack frames,and messagecallback sixth incomingargument userData as lookupconnection plus ip/port.0synthetic returns.','AllArrayLength/printf/lookup/send/allocator/realloc/memcpy/UDP/callback bodies and payload processing remain unexecuted;0complete transfer/messagecallback returns.3sameextent whole wrong-C variants genuinely link and violate48independent gate/variadic/lookup models;3wrong peerlayouts/native2048 proof/original binding negatives reject.0network/device/game/nativeWindows execution.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=0,wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
