import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_main_control_next_cycle_build import build
from wave20261105_main_control_next_cycle_controls import original_helpers

LANE=ROOT/'evidence/lanes/parallel-wave20261105/main-control-next/cycle'
WORK=ROOT/'work/w5cn/cycle/fixtures'
STATE,RECORDS,OUTPUT,TABLE,STOP,SP=0x21c6bf4,0x2174000,0x2178000,0x20db298,0x27e0000,0x2701000


def rotate(table,value,mask=3):
    found=next(((r,c) for r in range(105) for c in range(4) if table[r*12+c*3:r*12+c*3+3]==value),None)
    if found is None:return False,value
    r,c=found
    for unused in range(4):
        c=(c+1)&mask;triple=table[r*12+c*3:r*12+c*3+3]
        if triple[0]:return True,triple
    return None,None


def setup(address,vector,table):
    records=b''.join(bytes([v])+bytes([10+i])*7 for i,v in enumerate([0,1,7,200]));output=bytes.fromhex(vector.get('input','010203'))+bytes([0x5a])*5
    regions={STATE:struct.pack('<I',RECORDS),RECORDS:records,OUTPUT:output,TABLE:table};expected=dict(regions)
    if address==0x207d2c8:args=[vector['id'],0,0,0];result=RECORDS+8*[0,1,7,200].index(vector['id'])
    else:
        args=[OUTPUT,0,0,0];result,triple=rotate(table,output[:3])
        if result is None:raise ValueError('Unbounded zero-row rotation is excluded')
        if result:expected[OUTPUT]=triple+output[3:]
        result=int(result)
    return regions,expected,args,result


def run(image,row,body,vector,seed,helpers):
    address=int(row['address'],0);table=image[TABLE-0x2000000:TABLE-0x2000000+1260];regions,expected,args,result=setup(address,vector,table)
    cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_ARM);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(address,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000)
    for at,data in regions.items():cpu.mem_write(at,data)
    initial=[(0x55660000+i*0x101+seed)&0xffffffff for i in range(15)];initial[:4]=args;initial[-2:]=[SP,STOP];cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x10)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    allowed={} if address==0x207d2c8 else helpers;entries={a:0 for a in allowed};pcs=[];returned=False;tail_rmw=[]
    def code(machine,at,size,user):
        nonlocal returned
        if at==STOP:returned=True;machine.emu_stop();return
        if at in entries:entries[at]+=1
        if not address<=at<address+row['bytes'] and not any(a<=at<a+allowed[a]['bytes'] for a in allowed):raise ValueError(('Cycle fixture escaped exact original graph',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        rmw=address==0x2080278 and at==OUTPUT+2 and size==2 and machine.reg_read(ar.UC_ARM_REG_PC) in (0x2008e98,0x2008f34) and ((value>>8)&255)==regions[OUTPUT][3]
        if rmw:tail_rmw.append(dict(pc=hex(machine.reg_read(ar.UC_ARM_REG_PC)),address=hex(at),bytes=size,preservedAdjacentByte=(value>>8)&255))
        if not ((SP-0x4000<=at and at+size<=SP) or (address==0x2080278 and OUTPUT<=at and at+size<=OUTPUT+3) or rmw):raise ValueError('Cycle fixture wrote outside stack/three-byte output and qualified preserving halfword tail')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(address,STOP+4,count=100000);registers=[cpu.reg_read(r) for r in C.REGISTERS]
    if not returned or registers[4:12]!=initial[4:12] or registers[13]!=SP:raise ValueError('Cycle fixture return/callee-saved ABI differs')
    actual={a:bytes(cpu.mem_read(a,len(v))) for a,v in regions.items()}
    return dict(address=hex(address),vector=vector,seed=seed,topReturned=True,calleeSavedAbiPreserved=True,modelPassed=actual==expected and registers[0]==result,returnValue=registers[0],memorySha256=hashlib.sha256(b''.join(actual[a] for a in sorted(actual))).hexdigest(),pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest(),actualOriginalHelperEntries={hex(a):n for a,n in entries.items()},actualOriginalHelperInvocations=sum(entries.values()),originalTailHalfwordRmw=tail_rmw)


def execute(rows):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();table=image[TABLE-0x2000000:TABLE-0x2000000+1260];helpers={int(r['address'],0):r for r in original_helpers()};records=[];negative=[]
    triples=list(dict.fromkeys(table[i:i+3] for i in range(0,1260,3) if table[i]))
    invalid=next(bytes([255,254,v]) for v in range(256) if bytes([255,254,v]) not in triples and bytes([255,254,v]) not in [table[i:i+3] for i in range(0,1260,3)])
    badinput=next(v for v in triples if rotate(table,v)[0] and rotate(table,v,1)[0] and rotate(table,v)[1]!=rotate(table,v,1)[1])
    for row in rows:
        address=int(row['address'],0);native=image[address-0x2000000:address-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        if address==0x207d2c8:cases=[dict(id=v) for unused in range(8) for v in [0,1,7,200]];badvector=dict(id=1);old,new='value==native_data_021c6bf4[index].id','value!=native_data_021c6bf4[index].id'
        else:cases=[dict(input=v.hex()) for v in triples[:64]+[invalid]];badvector=dict(input=badinput.hex());old,new='match.column&=3','match.column&=1'
        for seed,vector in enumerate(cases):
            original=run(image,row,native,vector,seed,helpers);source=run(image,row,linked,vector,seed,helpers)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent cycle/present-record model differs',original,source))
            records.append(original)
        folder=WORK/format(address,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];text=source.read_text();changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole wrong cycle C did not mutate')
        wrong=folder/source.name;wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError('Whole wrong cycle C changed complete extent')
        controls=[]
        for seed in range(16):
            actual=run(image,row,body,badvector,seed,helpers)
            if actual['modelPassed'] or not actual['topReturned']:raise ValueError('Whole wrong cycle C did not return a model violation')
            controls.append(actual)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),genuineLink=bad['realLink'],compiledBytes=bad['compiledBytes'],actualReturningModelRejections=len(controls),records=controls))
    positive=2*sum(r['actualOriginalHelperInvocations'] for r in records);bad=sum(r['actualOriginalHelperInvocations'] for n in negative for r in n['records'])
    report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=positive,actualPositiveOriginalHelperInvocations=positive,actualWrongCOriginalHelperInvocations=bad,totalActualOriginalHelperInvocations=positive+bad,nativeDevicesOrScenesExecuted=0,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest(),wholeCNegativeControlsRejected=len(negative),wrongC=negative,limits=['Synthetic eight-byte records test present IDs0/1/7/200 only; impossible unsigned-byte/-1 sentinel exit and missing IDs remain unexecuted.','Original initialized105x4x3 table supplies first-match and next-nonempty-column models. Original search/memcmp/three-byte-copy bodies execute; invalid input returns zero without mutation. Every run checks complete return, ABI, preserved metadata/table/input padding and expected three-byte output. Original helper at02008e98 or02008f34 performs a final two-byte read-modify-write at output+2; the adjacent byte must remain unchanged and the synthetic eight-byte backing is explicit.','Malformed pointers, zero-triple lookup into all-zero rows, missing IDs, hardware/scenes and full external storage extent/authorship remain unexecuted/uncredited. Helpers/table carry zero additional source credit.'])
    write_json(LANE/'caller-fixtures.json',report);return report
