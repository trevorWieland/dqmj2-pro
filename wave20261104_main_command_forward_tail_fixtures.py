import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261104_main_command_forward_tail_build import build
from wave20261104_main_command_forward_next_build import build as query_build
from wave20261104_main_command_forward_tail_helpers import frozen_inputs,execute as helper_checks
from wave20261104_main_command_forward_tail_bindings import verify_original

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-command-forward/tail'
WORK=ROOT/'work/w4mcf/tail/fixtures'
BASE,ENTRY,QUERY,PROVIDER,TABLE,STOP,SP=0x02000000,0x0205fbb4,0x0205fb90,0x02063e38,0x021c0e68,0x027e0000,0x02701000


def run(image,body,query,index,enabled,pattern,seed,flags):
    words=[((pattern<<i)|(pattern>>(32-i if i else 32)))&0xffffffff for i in range(9)];initial_data=struct.pack('<9I',*words)
    at=(index>>5)+4;mask=1<<(index&31);old=(words[at]>>(index&31))&1
    words[at]=(words[at]|mask) if enabled else words[at]&~mask&0xffffffff;expected=struct.pack('<9I',*words)
    cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_ARM);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946)
    cpu.mem_map(BASE,0x200000);cpu.mem_write(BASE,image);cpu.mem_write(ENTRY,body);cpu.mem_write(QUERY,query)
    cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x1000,0x1000);cpu.mem_write(TABLE-16,initial_data)
    initial=[(0x11220000+i*0x101+seed)&0xffffffff for i in range(15)];initial[0]=index&0xffffffff;initial[1]=enabled&0xffffffff;initial[-2:]=[SP,STOP]
    cpu.reg_write(ar.UC_ARM_REG_CPSR,flags)
    for reg,word in zip(C.REGISTERS,initial):cpu.reg_write(reg,word)
    reads=[];writes=[];pcs=[];returned=False;pending=[];calls={QUERY:0,PROVIDER:0};returns={QUERY:0,PROVIDER:0}
    def code(machine,address,size,user):
        nonlocal returned
        if address==STOP:
            if pending:raise ValueError('Helper frames did not actually return')
            returned=True;machine.emu_stop();return
        if pending and address==pending[-1][1]:
            helper,continuation,stack=pending.pop()
            if machine.reg_read(ar.UC_ARM_REG_SP)!=stack:raise ValueError('Actual helper return did not restore its entry SP')
            returns[helper]+=1
        if address in calls:
            calls[address]+=1;pending.append((address,machine.reg_read(ar.UC_ARM_REG_LR),machine.reg_read(ar.UC_ARM_REG_SP)))
        if not (ENTRY<=address<ENTRY+92 or QUERY<=address<QUERY+36 or PROVIDER<=address<PROVIDER+8):raise ValueError('Call chain escaped exact measured executable spans')
        pcs.append(hex(address))
    def memory(machine,access,address,size,word,user):
        if SP-0x1000<=address<SP:return
        (writes if access==un.UC_MEM_WRITE else reads).append([hex(address),size])
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_READ|un.UC_HOOK_MEM_WRITE,memory)
    cpu.emu_start(ENTRY,STOP+4,count=128)
    registers=[cpu.reg_read(reg) for reg in C.REGISTERS];data=bytes(cpu.mem_read(TABLE-16,36));word_address=TABLE+(index>>5)*4
    if not returned or pending or calls!={QUERY:1,PROVIDER:2} or returns!=calls or registers[4:12]!=initial[4:12] or registers[13]!=SP:raise ValueError('Complete setter/query/provider chain failed exact call/return/ABI bounds')
    actual=dict(r0=registers[0],registers=registers,cpsr=cpu.reg_read(ar.UC_ARM_REG_CPSR),dataHex=data.hex(),reads=reads,writes=writes,pcs=pcs,calls={hex(k):v for k,v in calls.items()},actualHelperReturns={hex(k):v for k,v in returns.items()},actualTopReturn=True)
    expected_reads=[['0x2063e40',4],['0x2063e40',4],[hex(word_address),4],[hex(word_address),4]];expected_writes=[[hex(word_address),4]]
    correct=registers[0]==old and data==expected and reads==expected_reads and writes==expected_writes
    return actual,correct


def execute(rows):
    helpers=helper_checks();inputs=frozen_inputs();query_contract=next(c for c in inputs['cases'] if c['address']==hex(QUERY))
    previous_work=C.WORK
    try:query_row,query_body=query_build(ROOT/query_contract['source'],WORK/'query-source')
    finally:C.WORK=previous_work
    if query_row['sourceSha256']!=query_contract['sourceSha256'] or query_row['targetSha256']!=query_contract['nativeSha256'] or query_row['bytes']!=36:raise ValueError('Rebuilt frozen query contract differs')
    row=next(r for r in rows if r['address']==hex(ENTRY));source=ROOT/row['source'];text=source.read_text()
    if text.count('if(enabled)')!=1:raise ValueError('Semantic set/clear mutation not isolated')
    wrong=WORK/'wrong-operation/source.c';wrong.parent.mkdir(parents=True,exist_ok=True);wrong.write_text(text.replace('if(enabled)','if(!enabled)'));shutil.copyfile(source.with_name('context.h'),wrong.with_name('context.h'))
    bad,bad_body=build(wrong,wrong.parent/'build',True);verify_original(bad,bad['nativeSymbolEntries'])
    if bad['compiledBytes']!=92 or bad['realLink']['linkerAttempt']['exitCode']!=0 or bad['realLink']['exactCallerBytes']:raise ValueError('Wrong C did not genuinely link full92B and fail bytes')
    image=(ROOT/inputs['image']['path']).read_bytes();native=image[ENTRY-BASE:ENTRY-BASE+92];native_query=image[QUERY-BASE:QUERY-BASE+36];linked=(ROOT/row['realLink']['linkedElf']).with_name('caller.bin').read_bytes();records=[];negatives=[];seed=0
    for index in (-33,-1,0,1,31,32,63,64):
        for pattern in (0,0xffffffff,0xaaaaaaaa,0x55555555,0x80000001,0x7ffffffe):
            for enabled in (0,1,2,-1):
                flags=((seed&15)<<28)|0x10;args=(index,enabled,pattern,seed,flags);seed+=1
                original,ok=run(image,native,native_query,*args);rebuilt,good=run(image,linked,query_body,*args);negative,accepted=run(image,bad_body,query_body,*args)
                if not ok or not good or original!=rebuilt or accepted:raise ValueError(('Independent complete bit-setter chain oracle failed',args,ok,good,accepted))
                records.append(dict(index=index,enabled=enabled,pattern=hex(pattern),seed=seed-1,flags=flags,original=original,recompiled=rebuilt));negatives.append(dict(index=index,enabled=enabled,pattern=hex(pattern),result=negative,independentMutationModelRejected=True))
    n=len(records);result=dict(status='passed',traceSha256=C.sha(json.dumps(records,sort_keys=True,separators=(',',':')).encode()),supportedAddress=hex(ENTRY),supportedReturningVectors=n,nativeAndCompiledReturningCalls=2*n,wrongReturningControls=len(negatives),wholeCNegativeControlsRejected=1,positiveNativeProviderReturningCalls=4*n,negativeNativeProviderReturningCalls=2*n,totalNativeProviderReturningCalls=6*n,originalQueryReturningCalls=n,positiveCompiledQueryReturningCalls=n,negativeCompiledQueryReturningCalls=n,totalCompiledQueryReturningCalls=2*n,positiveNativeHelperExecutions=5*n,positiveCompiledHelperExecutions=n,negativeNativeHelperExecutions=2*n,negativeCompiledHelperExecutions=n,actualNativeCalleeBodiesExecuted=7*n,actualCompiledHelperExecutions=2*n,nativeDevicesOrScenesExecuted=0,externalStorageExtentAuthorshipCredit=0,helperReconstructionCredit=0,unicornVersion=un.__version__,originalHelperQualification=helpers,helperSourceRebuild=query_row,wrongC=dict(row=bad,source=wrong.relative_to(ROOT).as_posix(),sourceSha256=sha256(wrong)),records=records,wrongRecords=negatives,limits=['Complete92B bit-setter, original12B provider and original/rebuilt frozen36B query execute exact bounded call/return chains with independent old-bit/set-clear formulas, exact read/write widths, neighboring-word preservation and preserved ABI.','Signed index/shift boundaries, zero/nonzero enable values, varied32-bit words and NZCV flags are finite supplied vectors. Synthetic word views include addresses before the provider point and do not establish original C object bounds or gameplay-valid indices.','Provider12B is original executable evidence with zero source/extent credit; query36B source was already frozen in predecessor next8 and receives no new source credit. Dispatcher56B imports, game scenes and devices remain unexecuted.'])
    write_json(LANE/'bit-fixtures.json',result)
    return {k:v for k,v in result.items() if k not in ['records','wrongRecords','wrongC','helperSourceRebuild']}
