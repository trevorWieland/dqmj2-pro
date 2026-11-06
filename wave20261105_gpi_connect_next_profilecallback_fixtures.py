import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_gpi_connect_next_profilecallback_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_gpi_connect_next_profilecallback_build import build

CALLBACK,HASH,ADD,GET,DIV,LOOKUP,MALLOC=0x20af7f8,0x20b0810,0x20b09e0,0x20b0a50,0x2026144,0x20a8a3c,0x20a927c
REFERENCE,CONNECTION,PROFILE,NODE,TABLE,OUTPUT,STOP,SP=0x2170000,0x2171000,0x2172000,0x2173000,0x2174000,0x2175000,0x27e0000,0x2701000


def vector(seed):
    return dict(id=[0,-1,1,13,2147483647,-2147483648,27,-37][seed%8],buckets=[1,2,3,7,13,31][seed%6],operationType=[0,1,2,3,4,5,6,7,-1][seed%9],callbackPresent=seed%3!=0)


def run(image,row,body,v,seed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000)
    connection=bytearray([0x77]*0x5d8);struct.pack_into('<I',connection,0x5c8,TABLE);profile=bytearray([0xb6]*32);struct.pack_into('<ii',profile,0,v['id'],v['id']+1 if v['id']!=2147483647 else -2147483648);node=bytearray([0xd5]*36);struct.pack_into('<i',node,0,v['operationType']);struct.pack_into('<II',node,12,0x2178001 if v['callbackPresent'] else 0,0x12345678)
    memory={REFERENCE:struct.pack('<I',CONNECTION),CONNECTION:bytes(connection),PROFILE:bytes(profile),NODE:bytes(node),TABLE:bytes([0xc3])*16,OUTPUT:struct.pack('<I',0xabcdef77)}
    for at,data in memory.items():cpu.mem_write(at,data)
    if a==HASH:
        args=[PROFILE,v['buckets']];quotient=abs(v['id'])//v['buckets'];quotient=-quotient if v['id']<0 else quotient;expected=dict(kind='return',value=(v['id']-quotient*v['buckets'])&0xffffffff)
    elif a==GET:args=[REFERENCE,v['id'],OUTPUT];expected=dict(kind='provider',address=hex(LOOKUP))
    elif a==ADD:args=[REFERENCE,v['id']];expected=dict(kind='return',value=0) if v['id']<=0 else dict(kind='provider',address=hex(GET))
    else:
        args=[REFERENCE,NODE];expected=dict(kind='provider',address=hex(MALLOC)) if v['callbackPresent'] and 0<=v['operationType']<=6 else dict(kind='return',value=0)
    initial=[(0x66cc0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
    for i,arg in enumerate(args):initial[i]=arg&0xffffffff
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;pcs=[];interface=True;helper_entries=[]
    def code(machine,at,size,user):
        nonlocal observed,interface
        regs=[machine.reg_read(r) for r in C.REGISTERS]
        if at==STOP:
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Actual profile/callback return ABI differs')
            observed=dict(kind='return',value=regs[0]);machine.emu_stop();return
        provider=LOOKUP if a==GET else GET if a==ADD else MALLOC if a==CALLBACK else None
        if at==provider:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Actual profile provider mode differs')
            observed=dict(kind='provider',address=hex(at))
            if a==GET:interface=regs[0]==TABLE and SP-0x100<=regs[1]<SP and struct.unpack('<i',machine.mem_read(regs[1],4))[0]==v['id']
            elif a==ADD:interface=regs[:2]==[REFERENCE,v['id']&0xffffffff] and SP-0x100<=regs[2]<SP
            else:interface=regs[0]==[32,8,516,16,4,8,4][v['operationType']]
            machine.emu_stop();return
        if a==HASH and DIV<=at<DIV+524:
            if machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Actual signed division helper mode differs')
            if at==DIV:helper_entries.append(dict(address=hex(DIV),mode='arm',arguments=regs[:2]))
        elif not a<=at<a+row['bytes'] or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError(('Profile caller escaped bounded code/mode',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not(SP-0x4000<=at and at+size<=SP):raise ValueError(('Unexpected profile/callback write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=100000)
    if observed is None:raise ValueError('Actual caller did not reach bounded return/provider')
    guards=all(bytes(cpu.mem_read(at,len(data)))==data for at,data in memory.items())
    return dict(address=row['address'],vector=v,seed=seed,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and guards and interface,providerInterfaceModelPassed=interface,independentMutationModelPassed=guards,actualOriginalHelperInvocations=len(helper_entries),helperEntries=helper_entries,providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[];negative=[]
    variants={CALLBACK:('if(callback.callback != NULL)','if(callback.callback == NULL)'),HASH:('profile->profileId % numBuckets','profile->userId % numBuckets'),ADD:('if(id <= 0)','if(id < 0)'),GET:('profileTemp.profileId = profileid;','profileTemp.userId = profileid;')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed in range(128):
            v=vector(seed);original=run(image,row,native,v,seed);source=run(image,row,linked,v,seed)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent profile/callback model differs',original,source))
            records.append(original)
        folder=WORK/'fixtures'/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;text=source.read_text();old,new=variants[a];changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole profile/callback wrong-C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong C extent differs',row['address'],bad['compiledBytes']))
        failures=[]
        for seed in range(16):
            v=vector(seed);v.update(id=0 if a==ADD else seed+1,buckets=13,operationType=seed%7,callbackPresent=True);result=run(image,row,body,v,seed)
            if result['modelPassed']:raise ValueError('Whole wrong-C accepted independent model')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],records=failures))
    limits=['Four complete ordinary C profile/callback bodies match genuine whole native extents,original imports and interworking.32-byte temporary profile and callback argument layouts are scoped compiler/native proofs;0external allocated/storage extent or authorship credit.','512paired actual entries cover signed-remainder full returns with128actual original ARM division entries per image,nonpositive-profile-ID returns,missing/unsupported callbacks,positive lookup/provider argument frames and exact allocation requests32/8/516/16/4/8/4.0synthetic returns.','TableLookup,gpiGetProfile and allocator providers stop BEFORE instructions:0table/heap/search/callback-body executions; post-provider insertion/result/response mutations remain unexecuted.4same-extent wrong-C variants genuinely link and violate64independent models;wrong layouts and original-binding negatives reject.0network/device/game/nativeWindows execution.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
