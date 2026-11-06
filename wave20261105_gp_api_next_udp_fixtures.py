import hashlib
import json
import re
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_gp_api_next_udp_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_gp_api_next_udp_build import build

INPUT,HEADER,PAYLOAD,OUTPUT,PEERS,HANDLERS,STOP,SP=0x2170000,0x2171000,0x2172000,0x2173000,0x2174000,0x2175000,0x27e0000,0x2701000
GET=0x20a9508


def helper(image):
    inventory=(ROOT/'config/arm9/symbols.txt').read_text().splitlines();record=next((x for x in inventory if re.fullmatch(r'\S+ kind:function\(thumb,size=0x8\) addr:0x020a9508',x)),None);body=image[0xa9508:0xa9510]
    if record is None or body[:4]!=bytes.fromhex('00487047'):raise ValueError('Original RAM singleton getter body/entry differs')
    global_address=struct.unpack('<I',body[4:])[0];data=next((x for x in inventory if re.fullmatch(r'\S+ kind:bss addr:0x%08x'%global_address,x)),None)
    if data is None:raise ValueError('Original RAM singleton target is not canonical BSS')
    return dict(address=GET,mode='thumb',bytes=8,canonicalInventoryRecord=record,nativeSha256=hashlib.sha256(body).hexdigest(),globalAddress=global_address,globalRecord=data,sourceCredit=0)


def vector(a,seed):
    return dict(initialized=0 if seed%2==0 else 1,ip=0 if seed%8==1 else (0x01020304+seed),port=0 if seed%8==3 else (0x1200+seed),headerEmpty=seed%8==5,headerNull=seed%8==7,initialEmpty=seed%8==3,length=[0,1,15,16,17,255,0x10000,0x7fffffff][seed%8],reliable=seed%3,timeout=seed*100)


def run(image,row,body,v,seed,getter):
    a=int(row['address'],0);global_address=getter['globalAddress'];cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);engine=bytearray([0xa7]*60);struct.pack_into('<IIII',engine,0,0x11112222,PEERS,HANDLERS,v['initialized']);engine[16:44]=bytes(28);struct.pack_into('<I',engine,44,0x22223333);cpu.mem_write(global_address,bytes(engine));initialmsg=bytes([0 if v['initialEmpty'] else 0x41])+bytes(range(1,16));header=bytes([0 if v['headerEmpty'] else 0x61])+bytes(range(17,32));cpu.mem_write(INPUT,initialmsg);cpu.mem_write(HEADER,header);cpu.mem_write(PAYLOAD,bytes([0x59])*64);cpu.mem_write(OUTPUT,bytes.fromhex('efbeadde'));hdr=0 if v['headerNull'] else HEADER;ip,port=v['ip'],v['port'];callbacks=[0x20a9565,0x20a9665,0x20a95a9,0x20a97b5,0x20a9829,0x20a98d5,0x20a9905];args={0x20a98d4:[0x11112222,ip,port,PAYLOAD,v['length']],0x20a9904:[0x11112222,0x33334444,ip,port,77,PAYLOAD,v['length']],0x20a99cc:[port,0,0,*callbacks,0x12345678],0x20a9aa8:[ip,port,OUTPUT],0x20a9b08:[ip,port,INPUT,v['timeout']],0x20a9c54:[ip,port,HEADER,PAYLOAD,v['length'],v['reliable']],0x20a9d78:[INPUT,HEADER,callbacks[0],callbacks[1],callbacks[2],callbacks[3],callbacks[4],0x12345678],0x20a9e0c:[hdr],0x20a9ed8:[ip,port]}[a]
    initial=[(0x55dd0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
    for i,arg in enumerate(args):
        if i<4:initial[i]=arg
        else:cpu.mem_write(SP+4*(i-4),struct.pack('<I',arg&0xffffffff))
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    if a==0x20a98d4:expected=dict(kind='return',value=0)
    elif a==0x20a9904:expected=dict(kind='provider',address=hex(0x20a865c if v['length']>=16 else 0x20b4384))
    elif a==0x20a99cc:expected=dict(kind='provider',address=hex(0x20b5f38))
    elif not v['initialized']:expected=dict(kind='return',value=11 if a==0x20a9aa8 else 0 if a==0x20a9ed8 else 3)
    elif a==0x20a9b08 and (not ip or not port):expected=dict(kind='return',value=10)
    elif a==0x20a9d78 and (v['initialEmpty'] or v['headerEmpty']):expected=dict(kind='return',value=10)
    elif a==0x20a9e0c and (v['headerNull'] or v['headerEmpty']):expected=dict(kind='return',value=10)
    else:expected=dict(kind='provider',address=hex(0x20a85dc if a==0x20a9d78 else 0x20a8764))
    expected_engine=bytearray(engine)
    if a==0x20a99cc:
        for at,value in zip([36,16,20,24,28,40,32],callbacks):struct.pack_into('<I',expected_engine,at,value)
    expected_output=struct.pack('<I',3) if a==0x20a9aa8 and not v['initialized'] else bytes.fromhex('efbeadde');pcs=[];helper_entries=0;actual=None;interface=True;providers={0x20a865c,0x20b4384,0x20b5f38,0x20a85dc,0x20a8764}
    def code(machine,at,size,user):
        nonlocal helper_entries,actual,interface
        if at==STOP:
            regs=[machine.reg_read(r) for r in C.REGISTERS]
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('UDP actual caller return ABI differs')
            actual=dict(kind='return',value=regs[0]);machine.emu_stop();return
        if at in providers:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('UDP provider stop mode differs')
            regs=[machine.reg_read(r) for r in C.REGISTERS];actual=dict(kind='provider',address=hex(at))
            if at==0x20b4384:interface=regs[:3]==[0x33334444,0,0]
            elif at==0x20b5f38:interface=regs[:2]==[0,port]
            elif at==0x20a85dc:interface=regs[:3]==[4,1,0] and bytes(machine.mem_read(regs[13]+4,32))==initialmsg+header
            elif at==0x20a865c:interface=regs[0]==PEERS and struct.unpack('<I',bytes(machine.mem_read(regs[1],4)))[0]==ip and struct.unpack('<H',bytes(machine.mem_read(regs[1]+4,2)))[0]==port and struct.unpack('<I',bytes(machine.mem_read(regs[1]+8,4)))[0]==0x33334444
            else:
                compare=0x20a9529 if a==0x20a9e0c else 0x20a9539;interface=regs[0]==(HANDLERS if a==0x20a9e0c else PEERS) and regs[2:4]==[compare,0] and struct.unpack('<I',bytes(machine.mem_read(regs[13],4)))[0]==0
                interface=interface and (bytes(machine.mem_read(regs[1]+16,16))==header if a==0x20a9e0c else struct.unpack('<I',bytes(machine.mem_read(regs[1],4)))[0]==ip and struct.unpack('<H',bytes(machine.mem_read(regs[1]+4,2)))[0]==port)
            machine.emu_stop();return
        if at==GET:helper_entries+=1
        if not (a<=at<a+row['bytes'] or GET<=at<GET+8) or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError(('UDP escaped original bounded graph',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not (SP-0x4000<=at and at+size<=SP or global_address<=at and at+size<=global_address+60 or OUTPUT<=at and at+size<=OUTPUT+4):raise ValueError(('UDP unexpected write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=10000)
    if actual is None or helper_entries!=1:raise ValueError('UDP actual singleton entry/stop count differs')
    guards=bytes(cpu.mem_read(global_address,60))==bytes(expected_engine) and bytes(cpu.mem_read(OUTPUT,4))==expected_output and bytes(cpu.mem_read(INPUT,16))==initialmsg and bytes(cpu.mem_read(HEADER,16))==header and bytes(cpu.mem_read(PAYLOAD,64))==bytes([0x59])*64
    return dict(address=row['address'],vector=v,seed=seed,observed=actual,expected=expected,topReturned=actual['kind']=='return',partialProviderStopped=actual['kind']=='provider',providerInterfaceModelPassed=interface,modelPassed=actual==expected and interface and guards,actualOriginalHelperInvocations=helper_entries,providerInstructionExecutions=0,engineAndInputGuardsPreserved=guards,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();getter=helper(image);records=[];negative=[]
    changes={0x20a9aa8:('*thePeerState = GS_UDP_PEER_CLOSED;','*thePeerState = 2;'),0x20a9b08:('return GS_UDP_NETWORK_ERROR;','return GS_UDP_ADDRESS_ERROR;'),0x20a9c54:('return GS_UDP_NETWORK_ERROR;','return GS_UDP_ADDRESS_ERROR;'),0x20a9d78:('return GS_UDP_NETWORK_ERROR;','return GS_UDP_ADDRESS_ERROR;'),0x20a9e0c:('return GS_UDP_NETWORK_ERROR;','return GS_UDP_ADDRESS_ERROR;')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed in range(16):
            v=vector(a,seed);original=run(image,row,native,v,seed,getter);source=run(image,row,linked,v,seed,getter)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent UDP bounded state/provider model differs',original,source))
            records.append(original)
        if a not in changes:continue
        folder=WORK/'fixtures'/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;text=source.read_text();old,new=changes[a];changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole UDP C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong UDP C extent changed',row['address'],bad['compiledBytes']))
        failures=[]
        for seed in range(16):
            v=vector(a,seed);v['initialized']=0;result=run(image,row,body,v,seed,getter)
            if result['modelPassed'] or not result['topReturned']:raise ValueError('Wrong UDP C did not return independent model failure')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),sourceDependencies=bad['sourceDependencies'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],returningModelRejections=len(failures),records=failures))
    limits=['Nine complete ordinary C native extents and original calls/tagged callback literals genuinely link. Public comparison object layouts are independently checked at native Engine60/Peer12/Handler60/GT2Callbacks16 widths/offsets; source fixed16 copies retain original countdown byte order and variable payload copy retains the original ARM call.','Only the actual canonical8-byte RAM singleton getter executes as original callee code once per vector. Null-application-callback and uninitialized/invalid-parameter paths actually return; other cases stop BEFORE first Array/GT2/network provider instruction with independently checked peer/header/callback-field/allocator/reject call staging. No synthetic provider return or hardware/network operation occurs.','144 bounded native/source vectors exercise4NZCV patterns, initialization/parameter/header/length boundaries and measured provider call frames. Five same-extent whole wrong C units genuinely link and return80 independent state/output model failures. Initial caller is excluded from helper-entry counts.','Runtime application callback delivery, later provider paths, successful allocation/connect/send, source authorship of helper/data objects and full game/Windows execution remain unproven/uncredited.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),wholeCNegativeControlsRejected=len(negative),wrongC=negative,originalHelperEntries=[getter],nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
