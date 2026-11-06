import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_main_later_build import build
from wave20261105_main_later_helper import frozen_inputs,execute as helper_checks
from wave20261104_main_tail_bindings import verify_original

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-arm-later'
WORK=ROOT/'work/w5ml/fixtures'
BASE,TABLE,OBJECT,OUT,HELPER,STOP,SP=0x02000000,0x02170000,0x02172000,0x02173000,0x02008c14,0x027e0000,0x02701000
SPECS={0x204095c:('find',16),0x2040998:('allocate',16),0x20409f4:('release',16),0x2040a50:('find',8),0x2040a8c:('allocate',8),0x2040ae8:('release',8),0x2040b44:('find',8),0x2040b80:('allocate',8),0x2040bdc:('release',8)}


def table_model(address,key,count,keys,seed):
    mode,stride=SPECS[address];data=bytearray(((i*29+seed*17)&127)|128 for i in range(stride*4))
    for i,value in enumerate(keys):struct.pack_into('<I',data,i*stride,value)
    initial=bytes([0x37]*8)+bytes(data)+bytes([0x62]*8);expected=bytearray(initial);reads=[];writes=[];result=0;helper=[]
    for i in range(max(count,0)):
        at=TABLE+i*stride;reads.append([hex(at),4]);found=keys[i]==(0 if mode=='allocate' else key)
        if found:
            if mode=='find':result=at+4
            else:
                expected[8+i*stride+4:8+i*stride+8]=bytes(4);struct.pack_into('<I',expected,8+i*stride,key if mode=='allocate' else 0)
                writes=[[hex(at+4),4],[hex(at),4]];helper=[[0,hex(at+4),4]];result=at+4 if mode=='allocate' else 1
            break
    return dict(initial=initial,expected=bytes(expected),reads=reads,writes=writes,r0=result,helper=helper)


def run(image,address,body,key,count,keys,seed,flags,output=None):
    copy=address==0x2041f74
    if copy:
        data=bytes(((i*31+seed*11)&255) for i in range(0x7c));destination=bytes([0xa5]*32);target=0 if output==0 else OBJECT+0x70 if output==1 else OUT
        expected_out=bytearray(destination)
        if output==2:expected_out[:12]=data[0x70:0x7c]
        expected=dict(initial=data,expected=data,r0=OBJECT+0x70,reads=[] if output==0 else [[hex(OBJECT+0x70+4*i),4] for i in range(3)],writes=[] if output==0 else [[hex(target+4*i),4] for i in range(3)],helper=[])
    else:expected=table_model(address,key,count,keys,seed)
    cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_ARM);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(BASE,0x200000);cpu.mem_write(BASE,image);cpu.mem_write(address,body)
    cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x1000,0x1000)
    cpu.mem_write(OBJECT if copy else TABLE-8,expected['initial'])
    if copy:cpu.mem_write(OUT,destination)
    initial=[(0x11220000+i*0x101+seed)&0xffffffff for i in range(15)];initial[0]=OBJECT if copy else key;initial[1]=target if copy else TABLE;initial[2]=count&0xffffffff;initial[-2:]=[SP,STOP]
    cpu.reg_write(ar.UC_ARM_REG_CPSR,flags)
    for reg,word in zip(C.REGISTERS,initial):cpu.reg_write(reg,word)
    reads=[];writes=[];pcs=[];returned=False;pending=[];helper_inputs=[];helper_returns=0
    def code(machine,at,size,user):
        nonlocal returned,helper_returns
        if at==STOP:
            if pending:raise ValueError('Original fill helper did not return')
            returned=True;machine.emu_stop();return
        if pending and at==pending[-1][0]:
            continuation,stack=pending.pop()
            if machine.reg_read(ar.UC_ARM_REG_SP)!=stack:raise ValueError('Actual helper return SP differs')
            helper_returns+=1
        if at==HELPER:
            args=[machine.reg_read(ar.UC_ARM_REG_R0),hex(machine.reg_read(ar.UC_ARM_REG_R1)),machine.reg_read(ar.UC_ARM_REG_R2)]
            if args[0]!=0 or args[2] not in (4,8):raise ValueError('Unbounded helper input encountered')
            helper_inputs.append(args);pending.append((machine.reg_read(ar.UC_ARM_REG_LR),machine.reg_read(ar.UC_ARM_REG_SP)))
        if not(address<=at<address+len(body) or HELPER<=at<HELPER+20):raise ValueError('Caller escaped exact selected/native helper spans')
        pcs.append(hex(at))
    def memory(machine,access,at,size,word,user):
        if SP-0x1000<=at<SP:return
        (writes if access==un.UC_MEM_WRITE else reads).append([hex(at),size])
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_READ|un.UC_HOOK_MEM_WRITE,memory);cpu.emu_start(address,STOP+4,count=256)
    registers=[cpu.reg_read(reg) for reg in C.REGISTERS];state=bytes(cpu.mem_read(OBJECT if copy else TABLE-8,len(expected['initial'])));out=bytes(cpu.mem_read(OUT,32)) if copy else b''
    if not returned or pending or helper_returns!=len(helper_inputs) or registers[4:12]!=initial[4:12] or registers[13]!=SP:raise ValueError('Complete caller/helper ABI or actual return failed')
    actual=dict(r0=registers[0],registers=registers,cpsr=cpu.reg_read(ar.UC_ARM_REG_CPSR),dataHex=state.hex(),outHex=out.hex(),reads=reads,writes=writes,pcs=pcs,actualTopReturn=True,helperInputs=helper_inputs,actualNativeHelperReturns=helper_returns)
    correct=registers[0]==expected['r0'] and state==expected['expected'] and reads==expected['reads'] and writes==expected['writes'] and helper_inputs==expected['helper'] and (not copy or out==bytes(expected_out))
    return actual,correct


def execute(rows):
    qualification=helper_checks();inputs=frozen_inputs();image=(ROOT/inputs['image']['path']).read_bytes();row=next(r for r in rows if r['address']=='0x2040998');source=ROOT/row['source'];text=source.read_text()
    if text.count('native_fn_02008c14(0,result,4)')!=1:raise ValueError('Wrong payload-width mutation not isolated')
    wrong=WORK/'wrong-payload/source.c';wrong.parent.mkdir(parents=True,exist_ok=True);wrong.write_text(text.replace('native_fn_02008c14(0,result,4)','native_fn_02008c14(0,result,8)'));shutil.copyfile(source.with_name('context.h'),wrong.with_name('context.h'))
    bad,bad_body=build(wrong,wrong.parent/'build',True);verify_original(bad,bad['nativeSymbolEntries'])
    if bad['compiledBytes']!=92 or bad['realLink']['linkerAttempt']['exitCode']!=0 or bad['realLink']['exactCallerBytes']:raise ValueError('Wrong payload C must genuinely link full92B and fail bytes')
    patterns=[(0,1,7,7),(1,2,3,4),(0,0,0,0),(0xffffffff,0,7,1)];records=[];negatives=[];seed=0
    for row in rows:
        address=int(row['address'],0);native=image[address-BASE:address-BASE+row['bytes']];linked=(ROOT/row['realLink']['linkedElf']).with_name('caller.bin').read_bytes()
        if address==0x2041f74:vectors=[(0,0,(0,0,0,0),output) for output in (0,1,2) for repeat in range(4)]
        else:vectors=[(key,count,keys,None) for count in (-1,0,1,4) for keys in patterns for key in (0,1,7,0xffffffff,42)]
        for key,count,keys,output in vectors:
            flags=((seed&15)<<28)|0x10;args=(key,count,keys,seed,flags,output);seed+=1
            original,ok=run(image,address,native,*args);rebuilt,good=run(image,address,linked,*args)
            if not ok or not good or original!=rebuilt:raise ValueError(('Independent complete table/copy model failed',hex(address),args,ok,good,original))
            records.append(dict(address=hex(address),key=key,count=count,keys=keys,seed=seed-1,flags=flags,output=output,original=original,recompiled=rebuilt))
            if address==0x2040998 and original['helperInputs']:
                negative,accepted=run(image,address,bad_body,*args)
                if accepted:raise ValueError('Actual wrong payload8 write escaped independent model')
                negatives.append(dict(key=key,count=count,keys=keys,result=negative,independentPayloadExtentModelRejected=True))
    n=len(records);native_helpers=sum(r['original']['actualNativeHelperReturns']+r['recompiled']['actualNativeHelperReturns'] for r in records)+sum(r['result']['actualNativeHelperReturns'] for r in negatives)
    result=dict(status='passed',traceSha256=C.sha(json.dumps(records,sort_keys=True,separators=(',',':')).encode()),functions=10,bytes=760,supportedReturningVectors=n,nativeAndCompiledReturningCalls=2*n,actualNativeCalleeBodiesExecuted=native_helpers,wrongReturningControls=len(negatives),wholeCNegativeControlsRejected=1,nativeDevicesOrScenesExecuted=0,helperCodeAndExtentCredit=0,originalDataStorageExtentAuthorshipCredit=0,unicornVersion=un.__version__,originalHelperQualification=qualification,wrongC=dict(row=bad,source=wrong.relative_to(ROOT).as_posix(),sourceSha256=sha256(wrong)),records=records,wrongRecords=negatives,limits=['All ten complete selected callers execute finite original+linked vectors against independent first-key/free-slot/reset/copy formulas, exact pointer returns/read-write widths, untouched slot tail/neighbor bytes and preserved ABI.','Original20B word-fill helper executes bounded4-byte positive and8-byte wrong-C calls with explicit exact canonical ARM entry/native-body proof and actual entry/return counting; it receives zero source/extent credit.','Synthetic tables/object views supply memory only; original object bounds/storage/authorship, gameplay-valid keys/counts, hardware and game scenes remain unproved.'])
    write_json(LANE/'table-fixtures.json',result)
    return {k:v for k,v in result.items() if k not in ['records','wrongRecords','wrongC']}
