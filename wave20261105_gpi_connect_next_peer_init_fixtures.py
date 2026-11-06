import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json,sha256
from wave20261105_gpi_connect_next_peer_init_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_gpi_connect_next_peer_init_build import build

START,UDP,SIG,ERROR,SEND=0x20b049c,0x20a9aa8,0x20b0464,0x20b2c88,0x20ac9e8
REFERENCE,CONNECTION,PEER,INPUT,STOP,SP=0x2170000,0x2171000,0x2172000,0x2174000,0x27e0000,0x2701000


def vector(seed):
    v=dict(peerPresent=seed%11!=0,state=[100,106,101,102,103,105,999,104][seed%8],inputPresent=seed%2!=0,protocol=(seed//2)%4,nack=(seed//8)%2,outLen=(seed//16)%2)
    if seed<64:v.update(peerPresent=True,state=104)
    return v


def helpers(image):
    value=read_json(LANE/'string-helpers.json');inventory=(ROOT/'config/arm9/symbols.txt').read_text();result={}
    for item in value['helpers']:
        at=int(item['address'],0);raw=image[at-0x2000000:at-0x2000000+item['bytes']]
        if item['mode']!='arm' or item['canonicalInventoryRecord'] not in inventory.splitlines() or hashlib.sha256(raw).hexdigest()!=item['nativeSha256']:raise ValueError('Actual original RAM-only ARM string helper identity differs')
        result[at]=item
    return result,{k:int(v,0) for k,v in value['roles'].items()}


def run(image,row,body,v,seed,allowed,roles):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000)
    texts=[b'\\aack\\\\final\\trailing\0',b'\\anack\\\\final\\trailing\0',b'\\wrong\\\\final\\trailing\0',b'partial only\0'];text=texts[v['protocol']];peer=bytearray([0x88]*80);struct.pack_into('<I',peer,0,v['state']);struct.pack_into('<I',peer,8,0x7f000001);struct.pack_into('<H',peer,12,12345);struct.pack_into('<I',peer,24,v['nack']);struct.pack_into('<IIII',peer,28,INPUT if v['inputPresent'] else 0,len(text)+10,len(text)-1,0);struct.pack_into('<I',peer,52,v['outLen']);expected_peer=bytearray(peer);expected_text=bytearray(text)
    def final_outcome():return dict(kind='provider',address=hex(SEND)) if v['outLen'] else dict(kind='return',value=0)
    if not v['peerPresent'] or v['state'] in [100,106]:expected=dict(kind='return',value=3)
    elif v['state']==102:expected=dict(kind='provider',address=hex(START))
    elif v['state']==103:expected=dict(kind='provider',address=hex(UDP))
    elif v['state']==104 and v['inputPresent']:
        end=text.find(b'\\final\\')
        if end<0:expected=final_outcome()
        else:
            expected_text[end]=0
            if v['protocol']==1:
                struct.pack_into('<I',expected_peer,24,v['nack']+1);expected=dict(kind='provider',address=hex(ERROR if v['nack'] else SIG))
            elif v['protocol']==0:struct.pack_into('<I',expected_peer,0,105);struct.pack_into('<I',expected_peer,36,0);expected=final_outcome()
            else:expected=dict(kind='provider',address=hex(ERROR))
    else:expected=final_outcome()
    memory={REFERENCE:struct.pack('<I',CONNECTION),CONNECTION:bytes([0x77])*0x600,PEER:bytes(peer),INPUT:text}
    for at,data in memory.items():cpu.mem_write(at,data)
    initial=[(0x55bb0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[:2]=[REFERENCE,PEER if v['peerPresent'] else 0];initial[-2:]=[SP,STOP|1]
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;pcs=[];interface=True;entries=[]
    def code(machine,at,size,user):
        nonlocal observed,interface
        regs=[machine.reg_read(r) for r in C.REGISTERS]
        if at==STOP:
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Actual peer-init return ABI differs')
            observed=dict(kind='return',value=regs[0]);machine.emu_stop();return
        if at in [START,UDP,SIG,ERROR,SEND]:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Actual peer-init provider mode differs')
            observed=dict(kind='provider',address=hex(at))
            if at in [START,SIG]:interface=regs[:2]==[REFERENCE,PEER]
            elif at==UDP:interface=regs[:2]==[0x7f000001,12345] and SP-0x100<=regs[2]<SP
            elif at==ERROR:
                message='Error getting buddy authorization.' if v['protocol']==1 else 'Error parsing buddy message.';interface=regs[:2]==[REFERENCE,roles[message]]
            else:
                ptr,flag=struct.unpack('<II',machine.mem_read(regs[13],8));interface=regs[:4]==[REFERENCE,0x7f000001,12345,PEER+44] and SP-0x100<=ptr<SP and flag==1
            machine.emu_stop();return
        item=next((item for start,item in allowed.items() if start<=at<start+item['bytes']),None)
        if item:
            if machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Actual original string helper ARM mode differs')
            if at==int(item['address'],0):entries.append(dict(address=item['address'],mode='arm',arguments=regs[:3],nativeSha256=item['nativeSha256']))
        elif not a<=at<a+row['bytes'] or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError(('Peer-init escaped bounded original code/mode',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if SP-0x4000<=at and at+size<=SP:return
        if size==4 and at in [PEER,PEER+24,PEER+36]:return
        if size==1 and INPUT<=at<INPUT+len(text):return
        raise ValueError(('Unexpected peer-init memory write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=100000)
    if observed is None:raise ValueError('Actual peer-init did not reach bounded return/provider')
    expected_memory=dict(memory);expected_memory[PEER]=bytes(expected_peer);expected_memory[INPUT]=bytes(expected_text);guards=all(bytes(cpu.mem_read(at,len(data)))==data for at,data in expected_memory.items())
    return dict(address=row['address'],seed=seed,vector=v,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and guards and interface,providerInterfaceModelPassed=interface,independentMutationModelPassed=guards,actualOriginalHelperInvocations=len(entries),helperEntries=entries,providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);row=rows[0];image=(ROOT/'extract/arm9/arm9.bin').read_bytes();a=int(row['address'],0);allowed,roles=helpers(image);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes();records=[]
    for seed in range(128):
        v=vector(seed);original=run(image,row,native,v,seed,allowed,roles);source=run(image,row,linked,v,seed,allowed,roles)
        if original!=source or not original['modelPassed']:raise ValueError(('Independent peer-init state/string/mutation model differs',original,source))
        records.append(original)
    folder=WORK/'fixtures/wrong-C';folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    wrong=folder/'match.c';text=(ROOT/row['source']).read_text();changed=text.replace('return GP_NETWORK_ERROR;','return (GP_NETWORK_ERROR-1);',1)
    if changed==text:raise ValueError('Whole peer-init wrong-C did not mutate')
    wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
    if bad['compiledBytes']!=row['bytes']:raise ValueError('Whole peer-init wrong-C changed extent')
    failures=[]
    for seed in range(16):
        v=vector(seed);v.update(peerPresent=False);result=run(image,row,body,v,seed,allowed,roles)
        if result['modelPassed']:raise ValueError('Whole peer-init wrong-C accepted independent error model')
        failures.append(result)
    limits=['One complete ordinary C peer-init516 caller genuinely matches native whole extent/all original library/SDK/data bindings. Standard strstr/strncmp declarations consumed from actual private string.h preserve original borrowed-buffer register lifetime;0callee source/external storage allocation/authorship credit.','128paired actual entries independently cover null/invalid/getting/connected/unknown states,pre-start-connect/UDP-state/send frames,missingbuffer/incompleteframe paths,and actual ACK/NACK/invalid response RAM mutations. Original ARM strstr108/strncmp52 execute and return on bounded ASCII buffers;their canonical entry/body hashes/modes are verified,0synthetic returns.','OtherUDP/profile/startconnect/GetSig/error/send/allocator/callback bodies stop BEFORE instructions. No actual TCP/UDP/session/game/Windows execution inferred. One sameextent complete wrong-C genuinely links and violates16independent null-peer return models;wrong layout/original binding and standard-header context negative reject.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),wholeCNegativeControlsRejected=1,wrongC=[dict(address=row['address'],sourceSha256=sha256(wrong),compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],records=failures)],nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
