import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261104_main_command_forward_next_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-command-forward/next'
WORK=ROOT/'work/w4mcf/next/fixtures'
BASE,STOP,SP,OUT=0x02000000,0x027e0000,0x02701000,0x02710000


def wrong_sources(rows):
    results={}
    for address,before,after in [('0x205ce38','*410LL','*411LL'),('0x205f304','.field4;','.field2;')]:
        row=next(r for r in rows if r['address']==address);source=ROOT/row['source'];text=source.read_text()
        if text.count(before)!=1:raise ValueError('Measured semantic mutation not isolated')
        target=WORK/('wrong-'+format(int(address,0),'08x'))/'source.c';target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(text.replace(before,after));shutil.copyfile(source.with_name('context.h'),target.with_name('context.h'))
        bad,body=build(target,target.parent/'build',True)
        if bad['compiledBytes']!=row['bytes'] or bad['realLink']['linkerAttempt']['exitCode']!=0 or bad['realLink']['exactCallerBytes']:raise ValueError('Wrong C must genuinely link complete original extent and fail bytes')
        results[address]=dict(row=bad,body=body,source=target.relative_to(ROOT).as_posix(),sourceSha256=sha256(target),mutation=[before,after])
    return results


def model(address,index,state,value,output,seed):
    record=address in (0x205cdf0,0x205ce38);base=0x21043ac if record else 0x21b8b10 if address==0x205f304 else 0x21b8af0
    count=32 if record else 16 if address==0x205f304 else 4;stride=0x11c if record else 8
    data=bytearray((i*29+seed*17)&255 for i in range(count*stride));out=bytes([0xa5]*64)
    valid=index<count
    if valid:
        if record:data[index*stride]=state
        else:struct.pack_into('<HH',data,index*stride+2,(value^0xffff)&0xffff,value&0xffff)
    initial=bytes([0x72]*8)+bytes(data)+bytes([0x4d]*8);expected=bytearray(initial);expected_out=bytearray(out);reads=[];writes=[]
    if record:
        active=valid and state==3
        if valid:reads.append([hex(base+index*stride),1])
        if address==0x205cdf0:
            result=base+index*stride+0x84 if active else 0
            if active and output:
                offset=index*stride+0x84;expected_out[:12]=data[offset:offset+12]
                reads.extend([[hex(base+offset+4*i),4] for i in range(3)]);writes.extend([[hex(OUT+4*i),4] for i in range(3)])
        else:
            result=int(active)
            if active:
                scaled=((value*410+2048)>>12)&0xffffffff
                for offset in (0x90,0x94,0x98):
                    struct.pack_into('<I',expected,8+index*stride+offset,scaled);writes.append([hex(base+index*stride+offset),4])
    else:
        result=value&0xffffffff;reads.append([hex(base+index*stride+4),2])
    return dict(base=base,initial=initial,out=out,expected=bytes(expected),expectedOut=bytes(expected_out),r0=result,reads=reads,writes=writes)


def run(image,address,body,index,state,value,output,seed,flags):
    expected=model(address,index,state,value,output,seed);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_ARM);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946)
    cpu.mem_map(BASE,0x200000);cpu.mem_write(BASE,image);cpu.mem_write(address,body)
    cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x1000,0x1000);cpu.mem_map(OUT,0x1000)
    cpu.mem_write(expected['base']-8,expected['initial']);cpu.mem_write(OUT,expected['out'])
    initial=[(0x11220000+i*0x101+seed)&0xffffffff for i in range(15)];initial[0]=index&0xffffffff
    initial[1]=(OUT if output else 0) if address==0x205cdf0 else value&0xffffffff;initial[-2:]=[SP,STOP]
    cpu.reg_write(ar.UC_ARM_REG_CPSR,flags)
    for reg,word in zip(C.REGISTERS,initial):cpu.reg_write(reg,word)
    reads=[];writes=[];pcs=[];returned=False
    def code(machine,at,size,user):
        nonlocal returned
        if at==STOP:returned=True;machine.emu_stop()
        elif not address<=at<address+len(body)-4:raise ValueError('Fixture escaped complete caller into data/import')
        else:pcs.append(hex(at))
    def memory(machine,access,at,size,word,user):
        if SP-0x1000<=at<SP:return
        target=writes if access==un.UC_MEM_WRITE else reads
        target.append([hex(at),size])
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_READ|un.UC_HOOK_MEM_WRITE,memory)
    cpu.emu_start(address,STOP+4,count=128)
    registers=[cpu.reg_read(reg) for reg in C.REGISTERS]
    if not returned or registers[4:12]!=initial[4:12] or registers[13]!=SP:raise ValueError('Complete returning caller failed preserved ABI or instruction bound')
    data=bytes(cpu.mem_read(expected['base']-8,len(expected['initial'])));out=bytes(cpu.mem_read(OUT,64))
    actual=dict(r0=registers[0],registers=registers,cpsr=cpu.reg_read(ar.UC_ARM_REG_CPSR),dataSha256=C.sha(data),outHex=out.hex(),reads=reads,writes=writes,pcs=pcs,actualTopReturn=True)
    native_reads=[[hex(address+len(body)-4),4],*expected['reads']] if expected['reads'] else []
    correct=registers[0]==expected['r0'] and data==expected['expected'] and out==expected['expectedOut'] and reads==native_reads and writes==expected['writes']
    return actual,correct


def execute(rows):
    wrong=wrong_sources(rows);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[];wrong_records=[];seed=0
    for address in (0x205cdf0,0x205ce38,0x205f304,0x205f4a8):
        row=next(r for r in rows if int(r['address'],0)==address);native=image[address-BASE:address-BASE+row['bytes']];linked=(ROOT/row['realLink']['linkedElf']).with_name('caller.bin').read_bytes()
        if address==0x205cdf0:vectors=[(index,state,0,output) for index in (0,1,31,32,0xffffffff) for state in (0,3,255) for output in (False,True)]
        elif address==0x205ce38:vectors=[(index,state,value,False) for index in (0,31,32,0xffffffff) for state in (0,3,255) for value in (-2147483648,-4096,-1,0,1,4096,2147483647)]
        else:vectors=[(index,0,value,False) for index in (0,1,15 if address==0x205f304 else 3) for value in (-32768,-1,0,1,32767,0x1234)]
        for index,state,value,output in vectors:
            flags=((seed&15)<<28)|0x10;args=(index,state,value,output,seed,flags);seed+=1
            original,ok=run(image,address,native,*args);rebuilt,good=run(image,address,linked,*args)
            if not ok or not good or original!=rebuilt:raise ValueError(('Independent full caller model failed',hex(address),args,ok,good,original))
            records.append(dict(address=hex(address),index=index,state=state,value=value,output=output,seed=seed-1,flags=flags,original=original,recompiled=rebuilt))
            use_wrong=address==0x205f304 or address==0x205ce38 and index<32 and state==3 and value in (-2147483648,-4096,4096,2147483647)
            if use_wrong:
                bad,accepted=run(image,address,wrong[hex(address)]['body'],*args)
                if accepted:raise ValueError('Actual returning wrong C escaped independent field/arithmetic oracle')
                wrong_records.append(dict(address=hex(address),index=index,value=value,result=bad,independentModelRejected=True))
    result=dict(status='passed',traceSha256=C.sha(json.dumps(records,sort_keys=True,separators=(',',':')).encode()),functions=4,bytes=220,supportedReturningVectors=len(records),nativeAndCompiledReturningCalls=2*len(records),wrongReturningControls=len(wrong_records),wholeCNegativeControlsRejected=2,actualNativeCalleeOrDeviceExecutions=0,externalStorageExtentAuthorshipCredit=0,unicornVersion=un.__version__,wrongC=[{k:v for k,v in info.items() if k!='body'} for info in wrong.values()],records=records,wrongRecords=wrong_records,limits=['Only four import-free complete callers execute under independently supplied synthetic data views: guarded three-word lookup/copy, signed410 fixed scaling, and two signed-halfword lookups.','Index/state/sign boundaries, nullable output, exact reads/writes, guard bytes, preserved ABI and actual top return are checked against independent formulas.','Synthetic arrays supply fixture memory only; original object storage extent/authorship, game invariants, other callers, native imports, scenes and devices remain unproved.'])
    write_json(LANE/'data-fixtures.json',result)
    return {k:v for k,v in result.items() if k not in ['records','wrongRecords','wrongC']}
