import copy
import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json,sha256
from wave20261105_main_large_tail_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-arm-large/tail'
WORK=ROOT/'work/w5mg/tail/fixtures'
CALLEE_SHA='1e2c345c15f52b2207292530a5b8a9474141d59cab4645d7f68ccd736aabeb18'
ADDRESS,CALLEE,BUFFER,FORMAT,STOP,SP=0x20211e8,0x2020890,0x2170000,0x2172000,0x27e0000,0x2701000

def qualify(value,image,inventory,relocations):
    identity=value['identity']
    if (identity.get('program') or '',identity['processor'],identity['module'],identity['mode'],int(identity['address'],0),identity['bytes'])!=('','arm9','main','arm',CALLEE,2288):raise ValueError('Original empty-format callee identity/extent/mode differs')
    if value['canonicalInventoryRecord'] not in inventory.splitlines() or value['canonicalInventoryRecord']!='func_02020890 kind:function(arm,size=0x8f0) addr:0x02020890':raise ValueError('Actual canonical ARM formatter entry missing')
    if value['originalCallerBranchRecord'] not in relocations.splitlines() or value['originalCallerBranchRecord']!='from:0x02021210 kind:arm_call to:0x02020890 module:main':raise ValueError('Actual original wrapper-to-formatter call changed')
    body=image[CALLEE-0x2000000:CALLEE-0x2000000+2288]
    if len(body)!=2288 or hashlib.sha256(body).hexdigest()!=identity['targetSha256']:raise ValueError('Complete original formatter bytes changed')
    return dict(address=hex(CALLEE),bytes=2288,sourceCredit=0,executionDomain='Empty UTF16 format only; no nested callback/import')

def run(image,body,vector,seed):
    capacity,flags=vector;cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_ARM);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x200000);cpu.mem_write(0x2000000,image);cpu.mem_write(ADDRESS,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x1000,0x2000);before=bytes(((i*29+seed*11)&127)|128 for i in range(160));cpu.mem_write(BUFFER,before);cpu.mem_write(FORMAT,bytes(2));initial=[(0x11220000+i*0x101+seed)&0xffffffff for i in range(15)];initial[:4]=[BUFFER,capacity,FORMAT,0];initial[-2:]=[SP,STOP];cpu.reg_write(ar.UC_ARM_REG_CPSR,flags|0x10)
    for reg,word in zip(C.REGISTERS,initial):cpu.reg_write(reg,word)
    pcs=[];returned=False;visits=0
    def code(machine,at,size,user):
        nonlocal returned,visits
        if at==STOP:returned=True;machine.emu_stop();return
        if at==CALLEE:visits+=1
        if not (ADDRESS<=at<ADDRESS+108 or CALLEE<=at<CALLEE+2288):raise ValueError('Empty-format source/original executed unqualified import/callback')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not ((SP-0x1000<=at and at+size<=SP) or (BUFFER<=at and at+size<=BUFFER+160)):raise ValueError('Empty-format caller wrote outside bounded own regions')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(ADDRESS,STOP+4,count=3000);regs=[cpu.reg_read(r) for r in C.REGISTERS];actual=bytes(cpu.mem_read(BUFFER,160));abi=regs[4:12]==initial[4:12] and regs[13]==SP
    if not returned or not abi or visits!=1 or regs[0]!=0 or bytes(cpu.mem_read(FORMAT,2))!=bytes(2):raise ValueError('Empty-format actual caller/callee returning ABI differs')
    return dict(address=hex(ADDRESS),vector=list(vector),seed=seed,topReturned=True,returnValue=regs[0],abiPreserved=True,originalCalleeBodyExecutions=visits,bufferHex=actual.hex(),bufferTailPreserved=actual[2:]==before[2:],firstWchar=int.from_bytes(actual[:2],'little'),pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest(),nativeNestedCalleeExecutions=0)

def execute(rows):
    path=LANE/'native-callee-inputs.json'
    if sha256(path)!=CALLEE_SHA:raise ValueError('Immutable original callee qualification changed')
    value=read_json(path);image=(ROOT/value['image']['path']).read_bytes();inventory=(ROOT/value['inventory']['path']).read_text();relocations=(ROOT/value['relocations']['path']).read_text()
    for key in ['image','inventory','relocations']:
        if sha256(ROOT/value[key]['path'])!=value[key]['sha256']:raise ValueError('Original callee input changed')
    positive=qualify(value,image,inventory,relocations);boundary_controls=[]
    for key,wrong in [('program','child'),('processor','arm7'),('module','ov000'),('mode','thumb'),('address','0x2020894'),('bytes',2292)]:
        changed=copy.deepcopy(value);changed['identity'][key]=wrong
        try:qualify(changed,image,inventory,relocations)
        except ValueError as e:boundary_controls.append(dict(case=key,rejected=True,reason=str(e)))
        else:raise ValueError('Changed original formatter boundary admitted')
    changed=bytearray(image);changed[CALLEE-0x2000000]^=1
    for label,raw,inv,recs in [('body',bytes(changed),inventory,relocations),('entry-record',image,inventory.replace(value['canonicalInventoryRecord'],''),relocations),('call-record',image,inventory,relocations.replace(value['originalCallerBranchRecord'],''))]:
        try:qualify(value,raw,inv,recs)
        except ValueError as e:boundary_controls.append(dict(case=label,rejected=True,reason=str(e)))
        else:raise ValueError('Changed original callee evidence admitted')
    row=next(r for r in rows if r['address']=='0x20211e8');native=image[ADDRESS-0x2000000:ADDRESS-0x2000000+112];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes();cases=[(n,f) for n in [1,2,8,79] for f in [0,0x10000000,0x80000000,0xf0000000]];records=[]
    for seed,vector in enumerate(cases):
        original=run(image,native,vector,seed);rebuilt=run(image,linked,vector,seed)
        if original!=rebuilt or original['firstWchar']!=0 or not original['bufferTailPreserved']:raise ValueError('Independent actual empty-format terminator model differs')
        records.append(original)
    source=ROOT/row['source'];folder=WORK/'wrong-terminator';folder.mkdir(parents=True,exist_ok=True)
    for p in row['sourceDependencies']:shutil.copyfile(ROOT/p['path'],folder/(ROOT/p['path']).name)
    text=source.read_text();changed=text.replace('text[count]=0;','text[count]=1;',1)
    if changed==text:raise ValueError('Wrong full C terminator did not mutate source')
    wrong=folder/source.name;wrong.write_text(changed);bad,body=build(wrong,folder/'link',negative=True);negative=[]
    for seed,vector in enumerate(cases):
        actual=run(image,body,vector,seed)
        if actual['firstWchar']!=1 or not actual['topReturned'] or not actual['bufferTailPreserved']:raise ValueError('Wrong C did not actually return after a wrong terminator')
        negative.append(actual)
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();limits=['Only112B output-wrapper empty UTF16 format/capacity>=1 paths execute16original/source vectors32actualtopreturns, calling actual unchanged original2288B formatter once per run(32positive+16wrongC actual native callee invocations total48). No original nested callback/import runs.','Original2288B formatter and other imports receive0source/extent credit; its full canonical ARM boundary/hash/caller branch qualification and9 boundary negatives are pinned.224B floating-reader wrapper remains unexecuted.','Other formats, truncation/error paths, varargs payloads, floating parsing, hardware and game scenes remain unexecuted. Original errno/reader/output-callback storage/extent/authorship0credit.'];report=dict(status='passed',records=records,originalAndSourceReturningVectors=len(records),nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=2*len(records)+len(negative),positiveNativeCalleeBodyExecutions=2*len(records),wrongCNativeCalleeBodyExecutions=len(negative),nativeDevicesOrScenesExecuted=0,traceSha256=trace,originalCallee=positive,calleeNegativeControls=boundary_controls,wrongC=dict(sourceSha256=sha256(wrong),genuineLink=bad['realLink'],compiledBytes=bad['compiledBytes'],actualReturningModelRejections=len(negative),records=negative),limits=limits);write_json(LANE/'wrapper-fixtures.json',report);return report
