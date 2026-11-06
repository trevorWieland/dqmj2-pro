import hashlib
import json
import re
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,read_json,sha256
from wave20261106_dwc_auth_next_second_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_dwc_auth_next_second_build import build
from wave20261106_dwc_auth_next_context_link import context_contract,DATA_ADDRESS

START,FILL,CALPOST=0x209770c,0x2097ab0,0x2097fac
GLOBAL,CTRL,HTTP,CAL,STOP,SP=0x21d18f0,0x2171000,0x217c000,0x217e000,0x27e0000,0x2701000
STRCMP=0x201d800
PROVIDERS={0x209820c:'thumb',0x2098ed8:'thumb',0x20061ac:'arm'}


def helper_contract(image):
    record='func_0201d800 kind:function(arm,size=0x114) addr:0x0201d800'
    if record not in (ROOT/'config/arm9/symbols.txt').read_text().splitlines():raise ValueError('Actual canonical strcmp full entry absent')
    return dict(address=hex(STRCMP),bytes=276,mode='arm',program='',processor='arm9',module='main',canonicalInventoryRecord=record,nativeSha256=hashlib.sha256(image[STRCMP-0x2000000:STRCMP-0x2000000+276]).hexdigest(),calleeSourceCredit=0,calleeExtentCredit=0,actualOriginalBytesOnly=True)


def run(image,row,body,seed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000)
    alloc,free=0x27e1000+(seed&1),0x27e2000+((seed>>1)&1);work=bytearray([0x61])*5108;struct.pack_into('<I',work,0x1314,HTTP);struct.pack_into('<II',work,0x120c,alloc,free);url=0x20deb48 if seed&1 else 0x20deb90;ignore=(seed>>1)&1;context=struct.pack('<7I',url,0,4096,0,0,ignore,20000);memory={GLOBAL:struct.pack('<III',0x11223344,0x22334455,CTRL),CTRL:bytes(work),HTTP:bytes([0x63])*7188,CAL:bytes([0x64])*148,DATA_ADDRESS:context}
    for at,data in memory.items():cpu.mem_write(at,data)
    if a==START:args=[seed%3];target=0x209820c;frame=[HTTP,DATA_ADDRESS]
    elif a==FILL:args=[];target=0x2098ed8;frame=[HTTP,0x20debcc]
    elif a==CALPOST:args=[HTTP,CAL,[0,1,2,0xffffffff][seed%4]];target=0x20061ac;frame=[SP-52,33,0x20decac,3]
    else:raise ValueError('Unknown own caller')
    initial=[0x64d00000+i*0x101+seed for i in range(15)];initial[:len(args)]=args;initial[-2:]=[SP,STOP|1];cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;interface=True;pcs=[];helpers=0;helper_returns=0;helper_active=False
    def code(machine,at,size,user):
        nonlocal observed,interface,helpers,helper_returns,helper_active
        regs=[machine.reg_read(r) for r in C.REGISTERS];thumb=bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)
        if at in PROVIDERS:
            if at!=target or thumb!=(PROVIDERS[at]=='thumb'):raise ValueError('Unexpected provider/native mode')
            observed=dict(kind='provider',address=hex(at));interface=regs[:len(frame)]==frame
            if a==CALPOST:interface=interface and struct.unpack('<I',machine.mem_read(regs[13],4))[0]==1
            machine.emu_stop();return
        if a==START and STRCMP<=at<STRCMP+276:
            if thumb:raise ValueError('Actual original strcmp lost ARM mode')
            if at==STRCMP:
                if helper_active:raise ValueError('Unexpected recursive original helper')
                helpers+=1;helper_active=True
            pcs.append(at);return
        if not a<=at<a+len(body) or not thumb:raise ValueError('Caller escaped actual body/helper before provider')
        if helper_active:helper_returns+=1;helper_active=False
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if SP-0x4000<=at and at+size<=SP:return
        if a==START and at in [DATA_ADDRESS+12,DATA_ADDRESS+16,DATA_ADDRESS+20] and size==4:return
        raise ValueError('Unexpected caller/helper RAM mutation')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=20000)
    if observed is None:raise ValueError('Caller did not reach bounded provider')
    expected_context=bytearray(context)
    if a==START:struct.pack_into('<III',expected_context,12,alloc,free,1 if url!=0x20deb90 else ignore)
    guards=all(bytes(cpu.mem_read(at,len(data)))==(bytes(expected_context) if at==DATA_ADDRESS else data) for at,data in memory.items())
    model=observed==dict(kind='provider',address=hex(target)) and interface and guards and helpers==(1 if a==START else 0) and helpers==helper_returns
    return dict(address=row['address'],seed=seed,vector=dict(url=hex(url),initialIgnoreCa=ignore,alloc=hex(alloc),free=hex(free),args=args),observed=observed,topReturned=False,partialProviderStopped=True,providerInterfaceModelPassed=interface,independentMutationModelPassed=guards,modelPassed=model,actualOriginalHelperInvocations=helpers,actualOriginalHelperReturns=helper_returns,providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();helper=helper_contract(image);records=[];negative=[]
    variants={START:('DWCauthhttpparam.alloc = DWCauth->param.alloc;','DWCauthhttpparam.alloc = DWCauth->param.free;'),FILL:('DWCauth->http,native_data_020debcc','DWCauth->http,native_data_020debd4'),CALPOST:('native_data_020decac,3,1','native_data_020decac,4,1')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];compiled=(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes()
        for seed in range(8):
            left=run(image,row,native,seed);right=run(image,row,compiled,seed)
            if left!=right or not left['modelPassed']:raise ValueError(('Independent Auth context/frame model differs',left,right))
            records.append(left)
        directory=WORK/'wrong-c'/f'{a:08x}';directory.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
        before,after=variants[a];text=(ROOT/row['source']).read_text();changed=text.replace(before,after,1)
        if changed==text:raise ValueError('Meaningful whole-C negative did not change source')
        if a==START:changed=changed.replace('DWCauthhttpparam.alloc = DWCauth->param.free;','DWCauthhttpparam.alloc = (DWCAuthAlloc)DWCauth->param.free;')
        source=directory/'wrong.c';source.write_text(changed);bad,body=build(source,directory/'proof',negative=True);failed=sum(not run(image,row,body,seed)['modelPassed'] for seed in range(4))
        if failed!=4:raise ValueError('Wrong complete C unexpectedly passed independent context/frame model')
        negative.append(dict(address=row['address'],genuinelyLinked=True,matchedNative=False,independentModelFailures=failed,changedExpression=[before,after],realLink=bad['realLink']))
    limits=['24 paired full caller entries,48actual original/source pre-provider stops.0complete caller returns or synthetic callee returns. AuthStart alone executes original canonical276B ARM strcmp body16times/returns,0helper source/extent credit. HTTP creation/result lookup and formatting providers stop before their first instruction.','AuthStart compares actual original test/production URLs and models alloc/free/ignoreCA writes in the admitted28B context. CAL verifies first formatter frame with SDK3.1. FillResult verifies first Date provider frame only; later parsing/error/result branches are compile/link-exact but unexecuted.','No HTTP/network requests, provider I/O bodies, flash/WiFi/timer/device/game/nativeWindows execution. All BSS/URL/CAL/external storage authorship remains0credit; defined28B initialized context also0data credit pending strict independent acceptance.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,actualOriginalHelperQualification=helper,nativeAndCompiledReturningCalls=0,nativeAndCompiledPartialStops=2*len(records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),actualOriginalHelperReturns=2*sum(r['actualOriginalHelperReturns'] for r in records),wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
