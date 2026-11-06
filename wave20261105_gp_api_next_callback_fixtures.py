import hashlib
import json
import shutil
import struct
import re
import match_runtime as C
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_gp_api_next_callback_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_gp_api_next_callback_build import build

CONN,OBJECT,NODES,ARG,OP,PARAM,APP,ALLOC,STOP,SP=0x216f000,0x2170000,0x2172000,0x2174000,0x2175000,0x12345678,0x20acbcc,0x20a927c,0x27e0000,0x2701000
HEAD,LAST,FATAL=0x5d8,0x5dc,0x5bc


def vector(a,seed):
    n=seed%5;blocking=0 if seed%3==0 else 99 if seed%3==1 else 5
    return dict(nodeCount=n,blocking=blocking,types=[1 if (seed+i)%5==0 else 0 for i in range(n)],ids=[5 if (seed+i)%4==0 else 7 for i in range(n)],fatal=seed%2,callbackPresent=seed%3!=0,result=1+seed%3)


def run(image,row,body,v,seed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);obj=bytearray([0xa7]*0x5e0);struct.pack_into('<II',obj,0x1a8,APP|1 if v['callbackPresent'] else 0,PARAM);struct.pack_into('<I',obj,FATAL,7);struct.pack_into('<II',obj,HEAD,NODES if v['nodeCount'] else 0,NODES+24*(v['nodeCount']-1) if v['nodeCount'] else 0);cpu.mem_write(OBJECT,bytes(obj));cpu.mem_write(CONN,struct.pack('<I',OBJECT));nodes=bytearray([0xa3]*128)
    for i in range(v['nodeCount']):struct.pack_into('<IIIIII',nodes,24*i,APP if v.get('wrongCallbackMode') else APP|1,PARAM,ARG,v['types'][i],v['ids'][i],NODES+24*(i+1) if i+1<v['nodeCount'] else 0)
    cpu.mem_write(NODES,bytes(nodes));cpu.mem_write(ARG,bytes([0x63])*128);cpu.mem_write(OP,bytes([0x71])*24+struct.pack('<I',5));args={0x20acbcc:[CONN,v['result'],v['fatal']],0x20acc28:[CONN,APP|1,PARAM,ARG,OP,4],0x20acc9c:[CONN,NODES],0x20ace1c:[CONN,v['blocking']]}[a];initial=[(0x55dd0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
    for i,arg in enumerate(args):
        if i<4:initial[i]=arg
        else:cpu.mem_write(SP+4*(i-4),struct.pack('<I',arg&0xffffffff))
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    expected_obj=bytearray(obj);expected_nodes=bytearray(nodes);expected=None
    if a==0x20acbcc:
        if v['fatal']==1:struct.pack_into('<I',expected_obj,FATAL,1)
        expected=dict(kind='provider',address=hex(ALLOC)) if v['callbackPresent'] else dict(kind='return',void=True)
    elif a==0x20acc28:expected=dict(kind='provider',address=hex(ALLOC))
    elif a==0x20acc9c:expected=dict(kind='provider',address=hex(APP))
    else:
        chosen=next((i for i in range(v['nodeCount']) if v['blocking']==0 or v['ids'][i]==v['blocking'] or v['types'][i]==1),None)
        expected=dict(kind='return',value=0) if chosen is None else dict(kind='provider',address=hex(0x20acc9c))
        if chosen is not None:
            struct.pack_into('<II',expected_obj,HEAD,0,0)
            if v['blocking'] and chosen>0:struct.pack_into('<I',expected_nodes,24*(chosen-1)+20,NODES+24*(chosen+1) if chosen+1<v['nodeCount'] else 0)
    observed=None;pcs=[];interface=True
    def code(machine,at,size,user):
        nonlocal observed,interface
        if at==STOP:
            regs=[machine.reg_read(r) for r in C.REGISTERS]
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Callback actual caller return ABI differs')
            observed=dict(kind='return',void=True) if a==0x20acbcc else dict(kind='return',value=regs[0]);machine.emu_stop();return
        if at in [APP,ALLOC,0x20acc9c] and at!=a:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Callback original/native input target mode differs')
            regs=[machine.reg_read(r) for r in C.REGISTERS];observed=dict(kind='provider',address=hex(at))
            if at==ALLOC:interface=regs[0]==(16 if a==0x20acbcc else 24)
            elif at==APP:interface=regs[:3]==[CONN,ARG,PARAM]
            else:interface=chosen is not None and regs[:2]==[CONN,NODES+24*chosen]
            machine.emu_stop();return
        if not a<=at<a+row['bytes']:raise ValueError(('Callback escaped actual caller extent',hex(at)))
        if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Callback actual caller mode differs')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not(SP-0x4000<=at and at+size<=SP+4*max(0,len(args)-4) or OBJECT<=at and at+size<=OBJECT+len(obj) or NODES<=at and at+size<=NODES+128):raise ValueError(('Callback unexpected write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=100000)
    if observed is None:raise ValueError('Callback did not reach actual return/provider')
    guards=bytes(cpu.mem_read(OBJECT,len(obj)))==bytes(expected_obj) and bytes(cpu.mem_read(NODES,128))==bytes(expected_nodes) and bytes(cpu.mem_read(ARG,128))==bytes([0x63])*128 and bytes(cpu.mem_read(OP,28))==bytes([0x71])*24+struct.pack('<I',5)
    return dict(address=row['address'],vector=v,seed=seed,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and guards and interface,providerInterfaceModelPassed=interface,actualOriginalHelperInvocations=0,providerInstructionExecutions=0,connectionQueueAndInputGuardsPreserved=guards,objectSha256=hashlib.sha256(bytes(cpu.mem_read(OBJECT,len(obj)))).hexdigest(),queueSha256=hashlib.sha256(bytes(cpu.mem_read(NODES,128))).hexdigest(),pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[];negative=[]
    inventory=(ROOT/'config/arm9/symbols.txt').read_text();canonical=next((x for x in inventory.splitlines() if re.fullmatch(r'\S+ kind:function\(thumb,size=0x5c\) addr:0x020acbcc',x)),None)
    if canonical is None:raise ValueError('Fixture-supplied application callback lacks actual canonical same-program Thumb entry')
    indirect=[dict(address=hex(i.address),bytes=i.bytes.hex(),instruction=i.mnemonic+' '+i.op_str) for i in Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(image[0xacc9c:0xacc9c+382],0x20acc9c) if i.mnemonic=='blx' and i.op_str.startswith('r')]
    if len(indirect)!=1:raise ValueError('Measured original indirect callback BLX register instruction differs')
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed in range(40):
            v=vector(a,seed)
            if a==0x20acc9c:v['nodeCount']=1;v['types']=[0];v['ids']=[7]
            original=run(image,row,native,v,seed);source=run(image,row,linked,v,seed)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent callback fatal/queue/provider model differs',original,source))
            records.append(original)
        folder=WORK/'fixtures'/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;text=source.read_text();old,new={0x20acbcc:('if(fatal == GP_FATAL)','if(fatal != GP_FATAL)'),0x20acc28:('gsimalloc(sizeof(GPICallbackData))','gsimalloc(sizeof(GPICallbackData)+4)'),0x20acc9c:('data->callback.param','data->arg'),0x20ace1c:('(pcurr->type == GPI_ADD_ERROR)','(pcurr->type != GPI_ADD_ERROR)')}[a];changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole callback C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong callback C extent changed',row['address'],bad['compiledBytes']))
        failures=[]
        for seed in range(16):
            v=vector(a,seed)
            if a==0x20acc9c:v.update(nodeCount=1,types=[0],ids=[7])
            if a==0x20ace1c:v.update(nodeCount=3,types=[0,0,0],ids=[7,7,7],blocking=99)
            result=run(image,row,body,v,seed)
            if result['modelPassed']:raise ValueError('Wrong callback C did not violate independent fatal/queue/provider model')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),sourceDependencies=bad['sourceDependencies'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],returningModelRejections=sum(r['topReturned'] for r in failures),partialModelRejections=sum(r['partialProviderStopped'] for r in failures),records=failures))
    limits=['Four ordinary C complete native extents genuinely link with original call/data witnesses. Actual native callbackList/lastCallback offsets5d8/5dc differ from later public revision peerList+callback pair. This source uses a minimum measured connection view5e0 and claims no full object-storage extent.','160 vectors compare actual native/genuine compiled caller instructions to independent fatal-bit, allocator-size, stable ordered queue-filter/unlink and callback argument models. Empty/nonselected queues and disabled error callbacks genuinely return. Other paths stop BEFORE actual original allocation, callback-dispatch or fixture-supplied canonical Thumb application callback entry. No synthetic returns or provider/app callback bodies execute.','Four whole ordinary C variants genuinely compile/link unchanged extents and violate64 independent fatal, allocator, indirect callback-parameter and queue-filter observations. Separate wrong public peer-field offset geometry is rejected by pinned compiler.','Error payload creation after allocation, callback invocation/cleanup/free-loop outcomes, recursively added queue nodes, provider behavior, full game/device/native Windows execution remain unproven and uncredited. Literal strings and helper/target source/storage credit0.']
    mode_negatives=[]
    for row in rows:
        if int(row['address'],0)!=0x20acc9c:continue
        v=vector(0x20acc9c,1);v.update(nodeCount=1,types=[0],ids=[7],wrongCallbackMode=True);native=image[0xacc9c:0xacc9c+382];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for label,body in [('native',native),('genuine-source',linked)]:
            try:run(image,row,body,v,1)
            except ValueError as error:
                if 'input target mode differs' not in str(error):raise
                mode_negatives.append(dict(caller=label,rejectedBeforeCallbackBody=True,reason=str(error)))
            else:raise ValueError('Even fixture callback pointer mode was not caught before body execution')
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=0,wholeCNegativeControlsRejected=len(negative),wrongC=negative,actualIndirectCallbackInstruction=indirect[0],fixtureSuppliedCanonicalCallbackEntry=canonical,fixtureCallbackPointerIsNotOriginalStorageEvidence=True,wrongFixtureCallbackModeControls=mode_negatives,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
