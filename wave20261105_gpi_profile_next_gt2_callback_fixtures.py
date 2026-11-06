import hashlib
import json
import re
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_gpi_profile_next_gt2_callback_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_gpi_profile_next_gt2_callback_build import build

SOCKET,CONNECTION,MESSAGE,HANDLED,SEND_ARRAY,RECV_ARRAY,SEND_DATA,RECV_DATA,THUMB,ARM,NTH,CLOSE,STOP,SP=0x2170000,0x2171000,0x2172000,0x2173000,0x2174000,0x2175000,0x2176000,0x2177000,0x20b2d50,0x200616c,0x20a8644,0x20b5b4c,0x27e0000,0x2701000
SOCKET_ERROR,CONNECT,CONNECTED,RECEIVED,CLOSED,PING,SEND_FILTER,RECV_FILTER,DUMP,UNRECOGNIZED=0x20b3be4,0x20b3c24,0x20b3ca4,0x20b3d04,0x20b3d60,0x20b3db0,0x20b3e00,0x20b3e80,0x20b3f00,0x20b3f8c
CONNECTIONS={CONNECTED,RECEIVED,CLOSED,PING,SEND_FILTER,RECV_FILTER}


def helpers(image):
    inventory=(ROOT/'config/arm9/symbols.txt').read_text();result=[]
    for address,mode,n in [(NTH,'thumb',24),(THUMB,'thumb',96),(ARM,'arm',None)]:
        record=next((x for x in inventory.splitlines() if re.fullmatch(r'\S+ kind:function\(%s,size=0x[0-9a-f]+\) addr:0x%08x'%(mode,address),x)),None)
        if record is None:raise ValueError('Actual canonical filter helper/fixture provider entry/mode absent')
        size=int(re.search(r'size=0x([0-9a-f]+)',record)[1],16)
        if n is not None and size!=n:raise ValueError('Actual canonical filter/helper extent differs')
        result.append(dict(address=hex(address),mode=mode,bytes=size,originalCanonicalRecord=record,nativeSha256=hashlib.sha256(image[address-0x2000000:address-0x2000000+size]).hexdigest(),providerBodyExecuted=0,sourceCredit=0))
    return result


def vector(a,seed):
    return dict(state=seed%6,armProvider=(seed//6)%2==1,length=[-1,0,1,12][(seed//12)%4],socketDepth=[-2,-1,0,2][seed%4],connectionDepth=[-1,0,1,3][(seed//4)%4],result=seed%6,ip=0x11223344+seed,port=(0xb000+seed)&0xffff,latency=17+seed,reliable=seed&1,send=(seed//3)&1,reset=(seed//2)&1)


def run(image,row,body,v,seed,proof):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);state=v['state'];target=ARM if v['armProvider'] else THUMB;tag=target if v['armProvider'] else target|1
    if v.get('wrongMode'):tag=THUMB
    other=THUMB if v.get('wrongMode') else THUMB|1 if v['armProvider'] else ARM
    socket=bytearray([0x77]*76);connection=bytearray([0x66]*160);put=lambda buf,off,val:struct.pack_into('<I',buf,off,val&0xffffffff);put(socket,20,seed&1);put(socket,28,v['socketDepth']);put(connection,8,SOCKET);put(connection,24,0x12345678);put(connection,36,v['connectionDepth']);put(connection,152,SEND_ARRAY);put(connection,156,RECV_ARRAY)
    for off in [32,36,40,44,48]:put(socket,off,0 if state==1 else tag)
    for off in [40,44,48,52]:put(connection,off,0 if state==1 else tag)
    cpu.mem_write(SOCKET,bytes(socket));cpu.mem_write(CONNECTION,bytes(connection));expected_socket=bytearray(socket);expected_connection=bytearray(connection);cpu.mem_write(MESSAGE,b'opaque-message-bytes\0');cpu.mem_write(HANDLED,struct.pack('<I',0xabcdef77));expected_handled=0 if a==UNRECOGNIZED else 0xabcdef77
    for arr,data,fn in [(SEND_ARRAY,SEND_DATA,tag),(RECV_ARRAY,RECV_DATA,other)]:
        raw=bytearray([0x33]*24);put(raw,0,2);put(raw,8,4);put(raw,20,data);cpu.mem_write(arr,bytes(raw));cpu.mem_write(data,struct.pack('<II',fn,fn))
    s=0 if state==0 and a in [SOCKET_ERROR,CONNECT,DUMP,UNRECOGNIZED] else SOCKET;c=0 if state==0 and a in CONNECTIONS or a==CONNECT and state==5 or a==DUMP and state==5 else CONNECTION;message=0 if state==3 else MESSAGE;length=0 if state==4 else v['length'];normal_message=message if message and length else 0;normal_length=length if message and length else 0;filter_id=-1 if state==1 else 2 if state==4 else state&1;expected=dict(kind='return',value=1);provider_args=[];provider_stack=[];provider_target=None;connection_increment=False;socket_increment=False
    if a==SOCKET_ERROR:
        args=[s]
        if s and state!=1:provider_args=[s];socket_increment=True;provider_target=target
    elif a==CONNECT:
        args=[s,c,v['ip'],v['port'],v['latency'],message,length]
        if s and c and state!=1:provider_args=[s,c,v['ip'],v['port']];provider_stack=[v['latency'],normal_message,normal_length&0xffffffff];connection_increment=socket_increment=True;provider_target=target
    elif a==CONNECTED:
        args=[c,v['result'],message,length]
        if c:put(expected_connection,24,v['result'])
        if c and state!=1:provider_args=[c,v['result'],normal_message,normal_length&0xffffffff];connection_increment=socket_increment=True;provider_target=target
    elif a==RECEIVED:
        args=[c,message,length,v['reliable']]
        if c and state!=1:provider_args=[c,normal_message,normal_length&0xffffffff,v['reliable']];connection_increment=socket_increment=True;provider_target=target
    elif a in [CLOSED,PING]:
        arg=v['result'] if a==CLOSED else v['latency'];args=[c,arg]
        if c and state!=1:provider_args=[c,arg];connection_increment=socket_increment=True;provider_target=target
    elif a in [SEND_FILTER,RECV_FILTER]:
        args=[c,filter_id,message,length,v['reliable']]
        if c and 0<=filter_id<2:
            provider_args=[c,filter_id,normal_message,normal_length&0xffffffff];provider_stack=[v['reliable']];connection_increment=socket_increment=True;provider_target=target if a==SEND_FILTER else THUMB if v['armProvider'] else ARM
    elif a==DUMP:
        args=[s,c,v['ip'],v['port'],v['reset'],message,length,v['send']]
        if s and state!=1:provider_args=[s,c,v['ip'],v['port']];provider_stack=[v['reset'],normal_message,normal_length&0xffffffff];socket_increment=True;connection_increment=bool(c);provider_target=target
    else:
        args=[s,v['ip'],v['port'],message,length,HANDLED]
        if s and state!=1:provider_args=[s,v['ip'],v['port'],normal_message];provider_stack=[normal_length&0xffffffff];socket_increment=True;provider_target=target
    if socket_increment:put(expected_socket,28,v['socketDepth']+1)
    if connection_increment:put(expected_connection,36,v['connectionDepth']+1)
    if provider_target is not None:expected=dict(kind='provider',address=hex(provider_target),mode='thumb' if provider_target==THUMB else 'arm')
    initial=[(0x55dd0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
    for i,arg in enumerate(args):
        if i<4:initial[i]=arg&0xffffffff
        else:cpu.mem_write(SP+4*(i-4),struct.pack('<I',arg&0xffffffff))
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;pcs=[];calls=[];interface=True
    def code(machine,at,size,user):
        nonlocal observed,interface
        if at==STOP:
            regs=[machine.reg_read(r) for r in C.REGISTERS]
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('GT2 callback actual return ABI differs')
            observed=dict(kind='return',value=regs[0]);machine.emu_stop();return
        if at in [THUMB,ARM,CLOSE]:
            mode='thumb' if machine.reg_read(ar.UC_ARM_REG_CPSR)&32 else 'arm'
            if at in [THUMB,ARM] and mode!=('thumb' if at==THUMB else 'arm'):raise ValueError('GT2 actual supplied callback mode differs')
            observed=dict(kind='provider',address=hex(at),mode=mode);regs=[machine.reg_read(r) for r in C.REGISTERS];interface=regs[:len(provider_args)]==provider_args
            if provider_stack:interface=interface and bytes(machine.mem_read(regs[13],4*len(provider_stack)))==struct.pack('<'+'I'*len(provider_stack),*provider_stack)
            machine.emu_stop();return
        if at==NTH:calls.append(at)
        if (not a<=at<a+row['bytes'] and not NTH<=at<NTH+24) or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError(('GT2 escaped bounded caller/array helper/mode',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not (SP-0x4000<=at and at+size<=SP+4*max(0,len(args)-4)) and not (SOCKET<=at and at+size<=SOCKET+76) and not(CONNECTION<=at and at+size<=CONNECTION+160) and not(at==HANDLED and size==4):raise ValueError(('GT2 unexpected write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=100000)
    if observed is None:raise ValueError('GT2 caller did not reach actual return/provider')
    guards=bytes(cpu.mem_read(SOCKET,76))==bytes(expected_socket) and bytes(cpu.mem_read(CONNECTION,160))==bytes(expected_connection) and bytes(cpu.mem_read(HANDLED,4))==struct.pack('<I',expected_handled) and bytes(cpu.mem_read(MESSAGE,21))==b'opaque-message-bytes\0'
    return dict(address=row['address'],vector=v,seed=seed,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and guards and interface,providerInterfaceModelPassed=interface,independentMutationModelPassed=guards,actualOriginalHelperInvocations=len(calls),helperEntries=[hex(x) for x in calls],providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();proof=helpers(image);records=[];negative=[];mode_negative=[];variants={SOCKET_ERROR:('socket->callbackLevel++;','socket->callbackLevel--;'),RECEIVED:('if(!len || !message)','if(len || !message)'),CLOSED:('connection->callbackLevel++;','connection->callbackLevel--;')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed in range(64):
            v=vector(a,seed);original=run(image,row,native,v,seed,proof);source=run(image,row,linked,v,seed,proof)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent GT2 callback frame/mutation differs',original,source))
            records.append(original)
        v=vector(a,2);v.update(state=2,armProvider=False,length=12,wrongMode=True)
        for label,body in [('native',native),('genuine-source',linked)]:
            try:run(image,row,body,v,2,proof)
            except ValueError as error:
                if 'supplied callback mode differs' not in str(error):raise
                mode_negative.append(dict(caller=row['address'],version=label,rejectedBeforeBody=True,reason=str(error)))
            else:raise ValueError('GT2 even supplied Thumb callback pointer admitted')
        if a not in variants:continue
        folder=WORK/'fixtures'/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;text=source.read_text();old,new=variants[a];changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole GT2 wrong-C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong GT2 C extent changed',row['address'],bad['compiledBytes']))
        failures=[]
        for seed in range(16):
            v=vector(a,seed);v.update(state=2,length=12);result=run(image,row,body,v,seed,proof)
            if result['modelPassed']:raise ValueError('GT2 wrong C independent model accepted')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],actualReturningModelRejections=sum(r['topReturned'] for r in failures),partialModelRejections=sum(r['partialProviderStopped'] for r in failures),records=failures))
    limits=['Ten complete ordinary C GT2 callback bodies genuinely match entire native extents with original call/Thumb/BLX bytes. Public callback source and independently compiler-checked76-byte socket/160-byte connection layouts reuse copied immutable comparative types; no shared files changed.','640paired actual entry vectors model null/missing callbacks, result/handled stores, message/length normalization, callback-depth increments, and all per-interface register/stack arguments. Existing native24-byte ArrayNth executes for filter lookup using supplied array prefixes;0helpercode doublecredit.','Callbacks stop BEFORE fixture-supplied canonical ARM/Thumb target instructions. Fixture target entries/modes are proven; their bodies/prototypes/semantic implementations are not reconstructed by this caller test. No synthetic returns; callback-depth decrement/close tails remain byte-exact yet runtime-unexecuted.0callback/close/network/hardware effects.','Three complete same-extent wrong-C variants genuinely link and violate48 partial independent frame/mutation models.20even supplied Thumb callback pointer cases reject native/source mode before target body. Callback input memory is fixture state, never asserted original callback storage. No complete game/native Windows execution is inferred.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),wholeCNegativeControlsRejected=len(negative),wrongC=negative,wrongFixturePointerModesRejected=mode_negative,originalHelperEntries=proof,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
