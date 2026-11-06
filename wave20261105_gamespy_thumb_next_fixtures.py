import hashlib
import json
import random
import shutil
import struct
import re
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json,sha256
from wave20261105_gamespy_thumb_next_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-thumb-next/first'
WORK=ROOT/'work/w5gt/first/fixtures'
SERVER,ARRAY,HASH,BUCKETS,ROWS,KEY,LIST,STOP,SP=0x2170000,0x2171000,0x2172000,0x2173000,0x2174000,0x2175000,0x2176000,0x27e0000,0x2701000
UNSUPPORTED={0x20a85a8:'Original allocator callback is not exercised',0x20a866c:'Element-copy/shift provider graph is not exercised',0x20a86b8:'Sorted comparator/allocation graph is not exercised'}
HELPER_ADDRESSES=[0x201d800,0x20a64d0,0x20a5fe4,0x20a8a3c,0x20a8640]


def helpers(image):
    inventory=(ROOT/'config/arm9/symbols.txt').read_text();result={}
    for address in HELPER_ADDRESSES:
        matches=re.findall(r'^(\S+ kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:0x%08x)$'%address,inventory,re.M)
        if len(matches)!=1:raise ValueError('Original configured helper missing')
        record,mode,size=matches[0];size=int(size,0);body=image[address-0x2000000:address-0x2000000+size]
        result[address]=dict(address=hex(address),bytes=size,mode=mode,canonicalInventoryRecord=record,nativeSha256=hashlib.sha256(body).hexdigest(),sourceCredit=0)
    return result


def setup(address,vector):
    server=bytearray(64);array=bytearray(24);table=bytearray(20);buckets=bytearray(16);rows=bytearray(96);key=vector.get('key','ping').encode('latin1')+b'\0';key=key+bytes(32-len(key));items=bytes(range(128))
    struct.pack_into('<IIIIII',array,0,vector.get('count',0),8,4,8,0,LIST);struct.pack_into('<I',table,0,BUCKETS);struct.pack_into('<I',table,4,vector.get('buckets',0));struct.pack_into('<I',server,28,vector.get('ping',1234)&0xffffffff)
    for i in range(4):struct.pack_into('<I',buckets,4*i,ROWS+24*i);struct.pack_into('<i',rows,24*i,vector.get('values',[1,2,3,4])[i])
    initial={SERVER:bytes(server),ARRAY:bytes(array),HASH:bytes(table),BUCKETS:bytes(buckets),ROWS:bytes(rows),KEY:key,LIST:items};expected=dict(initial);stack=[];result=None
    if address==0x20a601c:
        args=[0 if vector.get('null') else SERVER,KEY,vector['fallback']&0xffffffff,0];result=vector['ping'] if not vector.get('null') and vector['key']=='ping' else vector['fallback']
    elif address in (0x20a60b4,0x20a60e8):
        at=4 if address==0x20a60b4 else 12;data=bytearray(initial[SERVER]);struct.pack_into('<H',data,at,vector['port']);initial[SERVER]=bytes(data);expected=dict(initial);args=[SERVER,0,0,0];result=((vector['port']&255)<<8)|(vector['port']>>8)
    elif address==0x20a8594:args=[ARRAY,0,0,0]
    elif address==0x20a86ec:
        args=[ARRAY,vector['count']-1,0,0];data=bytearray(initial[ARRAY]);struct.pack_into('<I',data,0,vector['count']-1);expected[ARRAY]=bytes(data)
    elif address in (0x20a87dc,0x20a87fc):args=[ARRAY,0,KEY,0];result=0 if address==0x20a87fc else None
    elif address==0x20a8844:args=[KEY,LIST,0,4];stack=[0];result=0
    elif address==0x20a8970:args=[0 if vector.get('null') else HASH,0,0,0];result=0 if vector.get('null') else sum(vector['values'][:vector['buckets']])
    elif address in (0x20a8940,0x20a89a4,0x20a89f0,0x20a8a3c):args=[0,KEY,0,0];result=0 if address in (0x20a89f0,0x20a8a3c) else None
    elif address in (0x20a8a84,0x20a8ab0):args=[HASH,0,KEY,0];result=0 if address==0x20a8ab0 else None
    else:raise ValueError('Unsupported fixture target')
    return initial,expected,args,stack,None if result is None else result&0xffffffff


def run(image,row,body,vector,seed,helper_rows):
    address=int(row['address'],0);regions,expected,args,stack,result=setup(address,vector);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(address,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000)
    for at,data in regions.items():cpu.mem_write(at,data)
    for i,value in enumerate(stack):cpu.mem_write(SP+4*i,struct.pack('<I',value))
    initial=[(0x55660000+i*0x101+seed)&0xffffffff for i in range(15)];initial[:4]=args;initial[-2:]=[SP,STOP|1];cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    pcs=[];entries={a:0 for a in helper_rows};returned=False
    def code(machine,at,size,user):
        nonlocal returned
        if at==STOP:returned=True;machine.emu_stop();return
        if at in entries:entries[at]+=1
        mode='thumb' if address<=at<address+row['bytes'] else next((r['mode'] for a,r in helper_rows.items() if a<=at<a+r['bytes']),None)
        if mode is None or bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&0x20)!=(mode=='thumb'):raise ValueError(('Original helper graph/mode escape',hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        parameter_store=address==0x20a8844 and at==SP and size==4 and value==stack[0] and machine.reg_read(ar.UC_ARM_REG_PC)==0x20a8854
        if not (SP-0x4000<=at and at+size<=SP) and not (address==0x20a86ec and at==ARRAY and size==4) and not parameter_store:raise ValueError('Fixture wrote outside stack/measured count/exact preserved parameter slot')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(address|1,STOP+4,count=30000);registers=[cpu.reg_read(r) for r in C.REGISTERS]
    if not returned or registers[4:12]!=initial[4:12] or registers[13]!=SP:raise ValueError('Actual Thumb return/callee-saved ABI differs')
    actual={a:bytes(cpu.mem_read(a,len(v))) for a,v in regions.items()}
    if stack and bytes(cpu.mem_read(SP,4*len(stack)))!=struct.pack('<'+'I'*len(stack),*stack):raise ValueError('Incoming callback argument stack slot changed')
    return dict(address=hex(address),vector=vector,seed=seed,topReturned=True,calleeSavedAbiPreserved=True,modelPassed=actual==expected and (result is None or result==registers[0]),cReturnValueModeled=result is not None,returnValue=registers[0],memorySha256=hashlib.sha256(b''.join(actual[a] for a in sorted(actual))).hexdigest(),pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest(),actualOriginalHelperEntries={hex(a):n for a,n in entries.items()},actualOriginalHelperInvocations=sum(entries.values()),nativeEntryModesChecked=True)


def cases(address):
    if address==0x20a601c:return [dict(null=n,key=k,ping=p,fallback=-31337) for n in [False,True] for k in ['ping','PING','missing',''] for p in [0,1234,0xffffffff]]
    if address in (0x20a60b4,0x20a60e8):return [dict(port=v) for v in [0,1,255,256,0x7f80,0x80ff,65535]+[random.Random(707+i).randrange(65536) for i in range(64)]]
    if address==0x20a86ec:return [dict(count=n) for n in range(1,9)]
    if address==0x20a8970:return [dict(null=n,buckets=b,values=v) for n in [False,True] for b in range(5) for v in [[1,2,3,4],[-3,0,7,100]]]
    return [dict(count=0,buckets=0) for unused in range(8)]


def execute(rows):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();helper_rows=helpers(image);records=[];negative=[];unsupported=[]
    for row in rows:
        address=int(row['address'],0)
        if address in UNSUPPORTED:unsupported.append(dict(address=row['address'],returningVectors=0,reason=UNSUPPORTED[address]));continue
        native=image[address-0x2000000:address-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed,vector in enumerate(cases(address)):
            original=run(image,row,native,vector,seed,helper_rows);source=run(image,row,linked,vector,seed,helper_rows)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent Thumb memory/return model differs',original,source))
            records.append(original)
        mutations={0x20a601c:(')==0)return native_fn_020a64d0',')!=0)return native_fn_020a64d0',dict(null=False,key='ping',ping=1234,fallback=-31337)),0x20a60b4:('&0xff00','&0xfe00',dict(port=17)),0x20a60e8:('&0xff00','&0xfe00',dict(port=17)),0x20a86ec:('array->count--;','array->count-=2;',dict(count=3)),0x20a8970:('count = 0','count = 1',dict(null=False,buckets=2,values=[1,2,3,4]))}
        if address not in mutations:continue
        old,new,vector=mutations[address];folder=WORK/format(address,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];text=source.read_text();changed=text.replace(old,new,1)
        if changed==text:raise ValueError(('Whole wrong Thumb C did not mutate',row['address']))
        wrong=folder/source.name;wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Whole wrong Thumb C changed complete extent',row['address'],bad['compiledBytes']))
        actual=[]
        for seed in range(16):
            v=run(image,row,body,vector,seed,helper_rows)
            if not v['topReturned'] or v['modelPassed']:raise ValueError('Whole wrong Thumb C did not return a model violation')
            actual.append(v)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),genuineLink=bad['realLink'],compiledBytes=bad['compiledBytes'],actualReturningModelRejections=len(actual),records=actual))
    report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),helperBodies=list(helper_rows.values()),unsupported=unsupported,wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest(),limits=['Actual Thumb callers and original ARM/Thumb strcmp/server lookup/ping/hash lookup/array-length helpers execute with entry modes checked; no code or provider stubs substitute for helper bodies.','Independent models cover both24-byte port routines as16-bit byte swaps, null-server/ping/missing-key default paths, null hash operations, positive bucket sums, last-item removal and empty callback traversals. Complete memory and callee-saved ABI are checked; void functions do not receive an invented C return-value contract.','Integer numeric-string conversion/ctype branches, nonempty hash/comparator/map callbacks, allocation/element-copy/shift/sorted paths, malformed inputs, network/hardware/scenes and complete external storage extent/authorship remain unexecuted/uncredited. Original helper bodies receive zero additional source credit.'])
    write_json(LANE/'caller-fixtures.json',report);return report
