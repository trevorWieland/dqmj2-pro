import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_main_later_next_build import build
from wave20261105_main_later_next_bindings import verify_original

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-arm-later/next'
WORK=ROOT/'work/w5ml/next/fixtures'
BASE,OBJECT,TARGET,PARAM,DATA,FIRST,SECOND,STOP,SP=0x2000000,0x2170000,0x2172000,0x2173000,0x2176000,0x2178000,0x2179000,0x27e0000,0x2701000


def model(address,vector,seed):
    regions=[];reads=[];writes=[]
    if address==0x203a260:
        flags,nonnull=vector;data=bytearray([0xa5]*0x150);struct.pack_into('<I',data,0x110,flags);struct.pack_into('<I',data,0x14c,TARGET if nonnull else 0);expected=bytearray(data);target=struct.pack('<4I',0x12345678,0x89abcdef,0xdeadbeef,0x13579bdf);after=bytearray(target)
        if nonnull:struct.pack_into('<I',after,0,0);struct.pack_into('<I',expected,0x14c,0);writes.extend([[hex(TARGET),4],[hex(OBJECT+0x14c),4]])
        struct.pack_into('<I',expected,0x110,flags&~7&0xffffffff);writes.append([hex(OBJECT+0x110),4]);reads=[[hex(OBJECT+0x14c),4],[hex(OBJECT+0x110),4]];regions=[(OBJECT,bytes(data),bytes(expected)),(TARGET,target,bytes(after))];args=[OBJECT];result=OBJECT
    elif address==0x203c8a4:
        default,limit,used,size=vector;global_address=0x20f5bf4;selected=global_address if default else PARAM;aligned=(size+3)&0xfffffffc;next_used=(used+aligned)&0xffffffff;accepted=next_used<limit
        for at in (global_address,PARAM):
            initial=bytes([0x47]*8)+struct.pack('<III',DATA,limit,used)+bytes([0x71]*8);expected=bytearray(initial)
            if at==selected and accepted:struct.pack_into('<I',expected,16,next_used)
            regions.append((at-8,initial,bytes(expected)))
        if default:reads.append(['0x203c8dc',4])
        reads.extend([[hex(selected+8),4],[hex(selected+4),4]])
        if accepted:reads.append([hex(selected),4]);writes.append([hex(selected+8),4])
        args=[0 if default else PARAM,size];result=(DATA+used)&0xffffffff if accepted else 0
    elif address==0x2041af0:
        key,position,duplicate=vector;table=0x20f65b4;data=bytearray(((i*29+seed*17)&127)|128 for i in range(64*16))
        keys=[1000+i for i in range(64)]
        if position>=0:keys[position]=key
        if duplicate and position>=0:keys[63]=key
        for i,value in enumerate(keys):struct.pack_into('<I',data,i*16,value)
        found=next((i for i,value in enumerate(keys) if value==key),None);end=64 if found is None else found+1;reads=[['0x2041b20',4],*[[hex(table+i*16),4] for i in range(end)]];regions=[(table-8,bytes([0x42]*8)+bytes(data)+bytes([0x73]*8),bytes([0x42]*8)+bytes(data)+bytes([0x73]*8))];args=[key];result=0 if found is None else table+found*16
    else:
        left,right=vector;regions=[(FIRST,left,left),(SECOND,right,right)];args=[FIRST,SECOND];i=0
        while True:
            a=left[i] if left[i]<128 else left[i]-256;b=right[i] if right[i]<128 else right[i]-256
            if 65<=a<=90:a+=32
            if 65<=b<=90:b+=32
            reads.extend([[hex(FIRST+i),1],[hex(SECOND+i),1]]);result=(a-b)&0xffffffff
            if result or a==0:break
            i+=1
    return dict(regions=regions,reads=reads,writes=writes,args=args,r0=result)


def run(image,address,body,vector,seed,flags):
    expected=model(address,vector,seed);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_ARM);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(BASE,0x200000);cpu.mem_write(BASE,image);cpu.mem_write(address,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x1000,0x1000)
    for at,initial,after in expected['regions']:cpu.mem_write(at,initial)
    initial=[(0x11220000+i*0x101+seed)&0xffffffff for i in range(15)];initial[:len(expected['args'])]=expected['args'];initial[-2:]=[SP,STOP];cpu.reg_write(ar.UC_ARM_REG_CPSR,flags)
    for reg,word in zip(C.REGISTERS,initial):cpu.reg_write(reg,word)
    reads=[];writes=[];pcs=[];returned=False
    def code(machine,at,size,user):
        nonlocal returned
        if at==STOP:returned=True;machine.emu_stop();return
        limit=address+len(body)-(4 if address in (0x203c8a4,0x2041af0) else 0)
        if not address<=at<limit:raise ValueError('Fixture escaped complete caller into imported/data bytes')
        pcs.append(hex(at))
    def memory(machine,access,at,size,word,user):
        if SP-0x1000<=at<SP:return
        (writes if access==un.UC_MEM_WRITE else reads).append([hex(at),size])
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_READ|un.UC_HOOK_MEM_WRITE,memory);cpu.emu_start(address,STOP+4,count=2048)
    registers=[cpu.reg_read(reg) for reg in C.REGISTERS];states=[bytes(cpu.mem_read(at,len(before))) for at,before,after in expected['regions']]
    if not returned or registers[4:12]!=initial[4:12] or registers[13]!=SP:raise ValueError('Complete caller actual return/ABI bound failed')
    actual=dict(r0=registers[0],registers=registers,cpsr=cpu.reg_read(ar.UC_ARM_REG_CPSR),regionSha256=[C.sha(state) for state in states],reads=reads,writes=writes,pcs=pcs,actualTopReturn=True)
    correct=registers[0]==expected['r0'] and all(state==after for state,(at,before,after) in zip(states,expected['regions'])) and reads==expected['reads'] and writes==expected['writes']
    return actual,correct


def wrong_sources(rows):
    result={}
    for address,before,after in [('0x203c8a4','used<allocator->limit','used<=allocator->limit'),('0x2040c38','a+=32;','a+=31;')]:
        row=next(r for r in rows if r['address']==address);source=ROOT/row['source'];text=source.read_text()
        if text.count(before)!=1:raise ValueError('Measured semantic mutation not isolated')
        target=WORK/('wrong-'+format(int(address,0),'08x'))/'source.c';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text.replace(before,after));shutil.copyfile(source.with_name('context.h'),target.with_name('context.h'))
        bad,body=build(target,target.parent/'build',True);verify_original(bad,bad['nativeSymbolEntries'])
        if bad['compiledBytes']!=row['bytes'] or bad['realLink']['linkerAttempt']['exitCode']!=0 or bad['realLink']['exactCallerBytes']:raise ValueError('Wrong C did not genuinely link full original extent and fail bytes')
        result[address]=dict(row=bad,body=body,source=target.relative_to(ROOT).as_posix(),sourceSha256=sha256(target),mutation=[before,after])
    return result


def execute(rows):
    wrong=wrong_sources(rows);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[];negatives=[];seed=0
    for address in (0x203a260,0x203c8a4,0x2041af0,0x2040c38):
        row=next(r for r in rows if int(r['address'],0)==address);native=image[address-BASE:address-BASE+row['bytes']];linked=(ROOT/row['realLink']['linkedElf']).with_name('caller.bin').read_bytes()
        if address==0x203a260:vectors=[(flags,nonnull) for flags in (0,1,2,4,7,8,0xffffffff,0xa5a5a5a5) for nonnull in (False,True)]
        elif address==0x203c8a4:vectors=[(default,limit,used,size) for default in (False,True) for limit in (0,4,16) for used in (0,4,12) for size in (0,1,3,4,15,0xffffffff)]
        elif address==0x2041af0:vectors=[(key,position,duplicate) for key in (0,42,0xffffffff) for position in (-1,0,1,31,63) for duplicate in (False,True)]
        else:vectors=[(bytes([a,0]),bytes([b,0])) for a in range(256) for b in (0,65,97,128,255)]+[(b'FoO\0',b'fOo\0'),(b'Alpha!\0',b'ALPHA?\0'),(b'\xffA\0',b'\xffa\0')]
        for vector in vectors:
            flags=((seed&15)<<28)|0x10;args=(vector,seed,flags);seed+=1;original,ok=run(image,address,native,*args);rebuilt,good=run(image,address,linked,*args)
            if not ok or not good or original!=rebuilt:raise ValueError(('Independent complete model failed',hex(address),vector,ok,good,original))
            saved_vector=[v.hex() if isinstance(v,bytes) else v for v in vector];records.append(dict(address=hex(address),vector=saved_vector,seed=seed-1,flags=flags,original=original,recompiled=rebuilt))
            use_wrong=address==0x203c8a4 and ((vector[2]+((vector[3]+3)&0xfffffffc))&0xffffffff)==vector[1] or address==0x2040c38 and 65<=vector[0][0]<=90
            if use_wrong:
                negative,accepted=run(image,address,wrong[hex(address)]['body'],*args)
                if accepted:raise ValueError('Actual wrong C escaped independent bound/fold model')
                negatives.append(dict(address=hex(address),vector=saved_vector,result=negative,independentModelRejected=True))
    result=dict(status='passed',traceSha256=C.sha(json.dumps(records,sort_keys=True,separators=(',',':')).encode()),functions=4,bytes=244,supportedReturningVectors=len(records),nativeAndCompiledReturningCalls=2*len(records),wrongReturningControls=len(negatives),wholeCNegativeControlsRejected=2,actualNativeCalleeBodiesExecuted=0,nativeDevicesOrScenesExecuted=0,originalDataStorageExtentAuthorshipCredit=0,unicornVersion=un.__version__,wrongC=[{k:v for k,v in info.items() if k!='body'} for info in wrong.values()],records=records,wrongRecords=negatives,limits=['Four complete import-free callers run finite original+linked vectors with independently supplied pointer/flag/allocator/table/string views, exact reads/writes, neighboring-state preservation, actual returns and preserved ABI.','Allocator uses32-bit alignment wrap and strict next-used<limit; exact-bound <= mutation is independently rejected. Comparator covers every first byte against five chosen second bytes plus terminated multibyte strings; only measured ASCII range folds, high bytes remain signed.','Other eight selected caller imports, original data storage/object extent/authorship, gameplay-valid states, devices and scenes remain unproved.'])
    write_json(LANE/'memory-fixtures.json',result)
    return {k:v for k,v in result.items() if k not in ['records','wrongRecords','wrongC']}
