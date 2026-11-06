import hashlib
import json
import random
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_gpi_connect_next_operation_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_gpi_connect_next_operation_build import build

CREATE,DISPATCH,CONNECT,SEND=0x20afa1c,0x20afb68,0x20ad144,0x20ad63c
ENCODER=0x20b2c98
HEAP,RESET,ERROR,COPY=0x20a927c,0x20aa9b4,0x20b2c88,0x20b2a38
REFERENCE,CONNECTION,OPERATION,OUTPUT,INPUT,STOP,SP=0x2170000,0x2171000,0x2172000,0x2173000,0x2174000,0x27e0000,0x2701000
TARGETS={0:0x20ad830,1:0x20b0910,2:0x20ae2e4,4:0x20b2908,5:0x20b0a80,6:0x20b29a0}


def vector(a,seed):return dict(type=[-1,0,1,2,3,4,5,6,7][seed%9],state=[0,4,2,-1][seed%4],firewallArgument=seed%3,blocking=seed&1,newuser=(seed//2)&1,callback=0x20b2d51 if seed&1 else 0,result=(17+seed)&0xffffffff)


def run(image,row,body,v,seed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);cpu.mem_write(REFERENCE,struct.pack('<I',CONNECTION));connection=bytearray([0x77]*(0x610 if a==SEND else 0x5d8));struct.pack_into('<I',connection,0x1f4,v['state']&0xffffffff);struct.pack_into('<I',connection,0x10c,0x5555);connection[0x177:0x177+9]=b'password\0';cpu.mem_write(CONNECTION,bytes(connection));operation=bytearray(776) if a==SEND else bytearray([0x66]*36);struct.pack_into('<I',operation,0,v['type']&0xffffffff);struct.pack_into('<I',operation,28,v['result']);cpu.mem_write(OPERATION,bytes(operation));cpu.mem_write(OUTPUT,struct.pack('<I',0xabcdef77));cpu.mem_write(INPUT,b'opaque-input\0');strings=[]
    for i,name in enumerate([b'nick\0',b'unique\0',b'mail@example.test\0',b'password\0',b'token\0',b'challenge\0',b'key\0']):
        address=INPUT+0x100*(i+1);cpu.mem_write(address,name);strings.append((address,name))
    expected_connection=bytearray(connection)
    if a==CREATE:args=[REFERENCE,v['type'],INPUT,OUTPUT,v['blocking'],v['callback'],INPUT+0x900];expected=dict(kind='provider',address=hex(HEAP));provider_args=[36]
    elif a==DISPATCH:
        args=[REFERENCE,OPERATION,INPUT];expected=dict(kind='provider',address=hex(TARGETS[v['type']])) if v['type'] in TARGETS else dict(kind='return',value=0);provider_args=args
    elif a==SEND:
        args=[REFERENCE,OPERATION];expected=dict(kind='provider',address=hex(ENCODER));provider_args=[CONNECTION+0x177]
    else:
        args=[REFERENCE,*[address for address,text in strings],v['firewallArgument'],v['newuser'],v['blocking'],v['callback'],INPUT+0x900]
        if v['state']==4:expected=dict(kind='provider',address=hex(RESET));provider_args=[REFERENCE]
        elif v['state']!=0:expected=dict(kind='provider',address=hex(ERROR));provider_args=[REFERENCE,0x20e09e8]
        else:expected=dict(kind='provider',address=hex(COPY));provider_args=[CONNECTION+0x110,strings[0][0],31];struct.pack_into('<I',expected_connection,0x10c,1)
    initial=[(0x55dd0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
    for i,arg in enumerate(args):
        if i<4:initial[i]=arg&0xffffffff
        else:cpu.mem_write(SP+4*(i-4),struct.pack('<I',arg&0xffffffff))
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;pcs=[];interface=True
    def code(machine,at,size,user):
        nonlocal observed,interface
        if at==STOP:
            regs=[machine.reg_read(r) for r in C.REGISTERS]
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Operation/connect actual return ABI differs')
            observed=dict(kind='return',value=regs[0]);machine.emu_stop();return
        if at in [HEAP,RESET,ERROR,COPY,ENCODER,*TARGETS.values()]:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Operation/connect original provider mode differs')
            observed=dict(kind='provider',address=hex(at));regs=[machine.reg_read(r) for r in C.REGISTERS];interface=regs[:len(provider_args)]==[x&0xffffffff for x in provider_args]
            if at==ENCODER:interface=interface and SP-0x4000<=regs[1]<SP and regs[1]+45<=SP
            machine.emu_stop();return
        if not a<=at<a+row['bytes'] or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError(('Operation/connect escaped bounded caller/mode',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not(SP-0x4000<=at and at+size<=SP+4*max(0,len(args)-4)) and not(CONNECTION<=at and at+size<=CONNECTION+len(connection)) and not(OPERATION<=at and at+size<=OPERATION+len(operation)):raise ValueError(('Operation/connect unexpected write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=100000)
    if observed is None:raise ValueError('Operation/connect did not reach actual return/provider')
    guards=bytes(cpu.mem_read(CONNECTION,len(connection)))==bytes(expected_connection) and bytes(cpu.mem_read(OPERATION,len(operation)))==bytes(operation) and bytes(cpu.mem_read(OUTPUT,4))==struct.pack('<I',0xabcdef77) and bytes(cpu.mem_read(REFERENCE,4))==struct.pack('<I',CONNECTION) and bytes(cpu.mem_read(INPUT,13))==b'opaque-input\0' and all(bytes(cpu.mem_read(address,len(text)))==text for address,text in strings)
    return dict(address=row['address'],vector=v,seed=seed,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and guards and interface,providerInterfaceModelPassed=interface,independentMutationModelPassed=guards,actualOriginalHelperInvocations=0,helperEntries=[],providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[];negative=[];variants={CREATE:('gsimalloc(sizeof(GPIOperation))','gsimalloc(sizeof(GPIOperation)-4)'),DISPATCH:('if(result != GP_NO_ERROR)','if(result == GP_NO_ERROR)'),CONNECT:('iconnection->connectState != GPI_NOT_CONNECTED','iconnection->connectState == GPI_NOT_CONNECTED'),SEND:('iconnection->password, passwordenc','iconnection->password+1, passwordenc')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed in range(160):
            v=vector(a,seed);original=run(image,row,native,v,seed);source=run(image,row,linked,v,seed)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent operation/connect frame/state differs',original,source))
            records.append(original)
        folder=WORK/'fixtures'/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;text=source.read_text();old,new=variants[a];changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole operation/connect wrong-C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong operation/connect C extent changed',row['address'],bad['compiledBytes']))
        failures=[]
        for seed in range(16):
            v=vector(a,seed)
            if a==DISPATCH:v['type']=3
            if a==CONNECT:v['state']=2
            result=run(image,row,body,v,seed)
            if result['modelPassed']:raise ValueError('Operation/connect wrong C independent model accepted')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],actualReturningModelRejections=sum(r['topReturned'] for r in failures),partialModelRejections=sum(r['partialProviderStopped'] for r in failures),records=failures))
    limits=['Four complete ordinaryC operation-create/dispatch/connect/newuser bodies genuinely match full native extents and original call/data literals.36-byte operation,776-byte connect-data/newuser772,qualified GPIprefix5d8/connectState1f4/firewall10c/nick110 and exact enum values independently compiler-checked.','640paired actual entry vectors independently model36-byte allocation request,six typed operation dispatch frames/default-type returns,connect reset/error/copy gates,and native forced-wireless firewall1 write. Actual source macroGS_WIRELESS_DEVICE1 preserves measured unconditional firewall write; caller firewall argument is not consulted in that branch.','Newuser encoder also stops BEFORE body. Its minimum610-byte private view names only independently original-pool-qualified productID608/namespaceID60c plus opaque suffix;canonicalBSS game-name object has0storagecredit. No encoding,random,base64,newuser output or suffix-field runtime execution inferred. All allocator/handler/reset/error-setter/strzcpy providers stop BEFORE bodies.0synthetic returns,allocations,string copies,reset/error sideeffects,operation handler success,post-allocation insertion,network or complete connect execution. Original error string storage remains external with0storage/extent/authorship credit.','Four same-extent whole wrong-C variants genuinely link and violate64 independent frame/mutation models; default dispatch wrong result write is observed through complete actual returns.4wrong layouts and unchanged original namespace/mode/kind/entry/addend/origin/opcode negatives reject. No nativeWindows/game/hardware execution inferred.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=0,wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
