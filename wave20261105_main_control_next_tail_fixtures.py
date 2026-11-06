import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_main_control_next_tail_build import build
from wave20261105_main_control_next_tail_controls import original_helpers

LANE=ROOT/'evidence/lanes/parallel-wave20261105/main-control-next/tail'
WORK=ROOT/'work/w5cn/tail/fixtures'
MANAGER,HEADER,INFO,ROWS,INPUT,STOP,SP=0x21c672c,0x21c6744,0x2174000,0x2176000,0x2178000,0x27e0000,0x2701000


def divide(value,denominator):return (abs(value)//denominator)*(-1 if value<0 else 1)


def setup(address,vector):
    manager=bytearray(24);struct.pack_into('<II',manager,16,INFO,4);header=struct.pack('<II',0,ROWS);info=bytearray(8+4*60);rows=bytearray(4*40);inputs=bytearray(128);index=vector['index']
    if address==0x207adcc:
        base=8+index*60
        if vector['profile']==1:info[base]=3;info[base+11]=5;info[base+50]=7
        if vector['profile']==2:info[base]=3;info[base+2]=1;info[base+11]=5;info[base+19]=5;info[base+50]=2;info[base+52]=9
        args=[index,vector['level']&0xffffffff,vector['code']&0xffffffff,0];model=0
        for i in range(10):
            if info[base+50+i] and vector['level']>=info[base+i] and vector['code']==info[base+10+i*4+1]:model=info[base+50+i];break
    else:
        struct.pack_into('<H',rows,index*40+8,0x300 if vector['active'] else 0);data=bytes.fromhex(vector['input']);inputs[:len(data)]=data;args=[INPUT,index,vector['value']&0xffffffff,0];model=vector['value']
        for value in inputs[:64]:
            if not value:break
            if value==16 and vector['active']:model=divide(5*model,4)
    return {MANAGER:manager,HEADER:bytearray(header),INFO:info,ROWS:rows,INPUT:inputs},args,model&0xffffffff


def run(image,row,body,vector,seed,helpers):
    address=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_ARM);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(address,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);regions,args,expected=setup(address,vector)
    for at,data in regions.items():cpu.mem_write(at,bytes(data))
    initial=[(0x55660000+i*0x101+seed)&0xffffffff for i in range(15)];initial[:4]=args;initial[-2:]=[SP,STOP];cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x10)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    allowed=[0x207aa98] if address==0x207adcc else [0x207d1e4,0x207cff4,0x207afec];entries={a:0 for a in allowed};pcs=[];returned=False
    def code(machine,at,size,user):
        nonlocal returned
        if at==STOP:returned=True;machine.emu_stop();return
        if at in entries:entries[at]+=1
        if not address<=at<address+row['bytes'] and not any(a<=at<a+helpers[a]['bytes'] for a in allowed):raise ValueError(('Fixture escaped exact byte-control caller/helper graph',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not (SP-0x4000<=at and at+size<=SP):raise ValueError('Read-only byte-control fixture wrote outside its stack')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(address,STOP+4,count=30000);registers=[cpu.reg_read(r) for r in C.REGISTERS]
    if not returned or registers[4:12]!=initial[4:12] or registers[13]!=SP:raise ValueError('Actual byte-control return/callee-saved ABI differs')
    actual={a:bytes(cpu.mem_read(a,len(v))) for a,v in regions.items()};unchanged=all(actual[a]==bytes(v) for a,v in regions.items());return dict(address=hex(address),vector=vector,seed=seed,topReturned=True,calleeSavedAbiPreserved=True,callerMemoryUnchanged=unchanged,modelPassed=unchanged and registers[0]==expected,returnValue=registers[0],memorySha256=hashlib.sha256(b''.join(actual[a] for a in sorted(actual))).hexdigest(),pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest(),actualOriginalHelperEntries={hex(a):n for a,n in entries.items()},actualOriginalHelperInvocations=sum(entries.values()))


def execute(rows):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();helpers={int(r['address'],0):r for r in original_helpers()};records=[];negative=[]
    for row in rows:
        address=int(row['address'],0);native=image[address-0x2000000:address-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        if address==0x207adcc:cases=[dict(index=i%4,profile=p,level=l,code=c) for i,(p,l,c) in enumerate((p,l,c) for p in [0,1,2] for l in [-1,0,3,100] for c in [5,6,300])];badvector=dict(index=0,profile=1,level=3,code=5);old,new='code==item->code','code!=item->code'
        else:
            patterns=[b'\0',b'\1\2\0',b'\x10\0',b'\x10\x10\0',b'\x11\0',bytes([1])*64,bytes([16])*4+b'\0',bytes([1])*63+b'\x10'];cases=[dict(index=i%4,active=a,value=v,input=b.hex()) for i,(a,v,b) in enumerate((a,v,b) for a in [False,True] for v in [-100,0,100] for b in patterns)];badvector=dict(index=0,active=True,value=100,input='1100');old,new='input[i]==16','input[i]==17'
        for seed,vector in enumerate(cases):
            original=run(image,row,native,vector,seed,helpers);source=run(image,row,linked,vector,seed,helpers)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent byte-record/control model differs',original,source))
            records.append(original)
        folder=WORK/format(address,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];text=source.read_text();changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole wrong byte-control C did not mutate')
        wrong=folder/source.name;wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong byte-control C changed complete extent',row['address'],bad['compiledBytes']))
        controls=[]
        for seed in range(16):
            actual=run(image,row,body,badvector,seed,helpers)
            if actual['modelPassed'] or not actual['topReturned']:raise ValueError('Wrong whole C did not actually return a byte-control model violation')
            controls.append(actual)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),genuineLink=bad['realLink'],compiledBytes=bad['compiledBytes'],actualReturningModelRejections=len(controls),records=controls))
    positive=2*sum(r['actualOriginalHelperInvocations'] for r in records);bad=sum(r['actualOriginalHelperInvocations'] for n in negative for r in n['records']);report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=positive,actualPositiveOriginalHelperInvocations=positive,actualWrongCOriginalHelperInvocations=bad,totalActualOriginalHelperInvocations=positive+bad,nativeDevicesOrScenesExecuted=0,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest(),wholeCNegativeControlsRejected=len(negative),wrongC=negative,limits=['Read-only synthetic in-memory metadata records and 40-byte rows satisfy original getter bounds and pointer interfaces. The ten-entry record model independently specifies first nonzero threshold/code match; byte-stream model stops at zero or64 and applies signed truncating5/4 only to byte16 under the explicit active flag.','Actual original configured helper graph executes, including metadata/row getters and flag/arithmetic helpers. Caller memory remains unchanged and callee-saved ABI is checked. Values avoid signed overflow; full64-byte no-terminator and final-position control cases are included.','Invalid metadata indices/pointers, null getter results, overflow, complete external storage/authorship, hardware and scenes remain unexecuted/uncredited. Byte/field labels describe measured behavior rather than established gameplay meanings.']);write_json(LANE/'caller-fixtures.json',report);return report
