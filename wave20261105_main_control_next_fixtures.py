import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json,sha256
from wave20261105_main_control_next_build import build
from wave20261105_main_control_next_controls import original_helpers

LANE=ROOT/'evidence/lanes/parallel-wave20261105/main-control-next'
WORK=ROOT/'work/w5cn/fixtures'
POOL,LOOKUP,NEEDLE,OUTPUT,STOP,SP=0x2174000,0x2176000,0x2178000,0x2179000,0x27e0000,0x2701000
HEADER,LOOKUP_SLOT,COUNTER,ITEMS=0x21c6744,0x21c6bf4,0x21c6c14,0x21c6c58
ALLOWED={0x207b02c:[],0x207b94c:[],0x207b974:[0x207afec,0x207b94c,0x2026144],0x207ba64:[],0x207d31c:[0x207b058],0x207d8e4:[0x207d2c8],0x207f1a4:[],0x207ffb4:[0x201b248]}


def divide(a,b):return (abs(a)//abs(b))*(-1 if (a<0)!=(b<0) else 1)


def vectors(address,image):
    if address==0x207b02c:return [dict(index=i%4,flags=f,mask=m) for i,(f,m) in enumerate((f,m) for f in [0,2,0x8102,0xffff] for m in [0,2,0x10002,-1])]
    if address==0x207b94c:return [dict(value=value,kind=kind) for value in [-100,0,100] for kind in [-1,1,2,4]]
    if address==0x207b974:return [dict(index=i%4,input=x,pair=p,percentage=s,begin=b,end=e,lower0=-20,upper0=100,lower1=10,upper1=200) for i,(x,p,s,b,e) in enumerate((x,p,s,b,e) for x in [-10,0,3,10,12] for p in [0,1] for s in [0,1] for b,e in [(0,0),(0,10),(10,10)])]
    if address==0x207ba64:return [dict(value=x,mode=m) for x in [-1000,-11,-1,0,1,11,1000] for m in [-1,0,1,2,3]]
    if address==0x207d31c:return [dict(index=i%4,value=x,mode=m,flags=f) for i,(x,m,f) in enumerate((x,m,f) for x in [-1000,-100,0,100,1000] for m in [0,1,2,3,4,5] for f in [0,2])]
    if address==0x207d8e4:return [dict(value=x,mode=m,code=c) for x in [-1000,0,1000] for m in [0,1,3] for c in [1,5]]
    if address==0x207f1a4:return [dict(count=c,initialPending=p) for c in [-100,-1,0] for p in [0,3,0xffffffff]]
    if address==0x207ffb4:
        table=image[0xdb298:0xdb298+1260];needles=[table[i*3:i*3+3] for i in [0,1,20,200,419]];absent=next(bytes([x,0xfe,0xfd]) for x in range(256) if all(table[i:i+3]!=bytes([x,0xfe,0xfd]) for i in range(0,1260,3)));return [dict(needle=x.hex()) for x in [*needles,absent]]
    raise ValueError('Unowned fixture target')


def setup(address,vector,seed):
    row=bytearray((seed*23+i*31)&255 for i in range(160));regions={HEADER:bytearray(struct.pack('<II',0x11223344,POOL)),POOL:row,LOOKUP_SLOT:bytearray(struct.pack('<I',LOOKUP)),LOOKUP:bytearray(8),COUNTER:bytearray(struct.pack('<III',0x55667788,3,0)),ITEMS:bytearray(8),NEEDLE:bytearray(8),OUTPUT:bytearray(b'\x31\x42\x53\x64\x75\x86\x97\xa8')};arguments=[0,0,0,0];stack=struct.pack('<I',2);index=vector.get('index',0)
    if address==0x207b02c:struct.pack_into('<H',row,index*40+4,vector['flags']);arguments[:2]=[index,vector['mask']&0xffffffff]
    elif address==0x207b94c:arguments[:2]=[vector['value']&0xffffffff,vector['kind']&0xffffffff]
    elif address==0x207b974:
        struct.pack_into('<hhhhhh',row,index*40+16,*[vector[k] for k in ['lower0','upper0','lower1','upper1','begin','end']]);arguments=[index,vector['input']&0xffffffff,vector['pair'],vector['percentage']]
    elif address==0x207ba64:arguments[:2]=[vector['value']&0xffffffff,vector['mode']&0xffffffff]
    elif address==0x207d31c:row[index*40+37]=vector['flags'];arguments[:3]=[vector['mode'],vector['value']&0xffffffff,index]
    elif address==0x207d8e4:regions[LOOKUP][0]=vector['mode'];regions[LOOKUP][3]=vector['code'];arguments[:2]=[vector['mode'],vector['value']&0xffffffff]
    elif address==0x207f1a4:struct.pack_into('<II',regions[COUNTER],4,vector['initialPending'],vector['count']&0xffffffff)
    elif address==0x207ffb4:regions[NEEDLE][:3]=bytes.fromhex(vector['needle']);arguments[:2]=[NEEDLE,OUTPUT]
    return regions,arguments,stack


def expected(address,vector,regions,image):
    after={a:bytes(v) for a,v in regions.items()}
    if address==0x207b02c:value=int(bool(vector['flags']&(vector['mask']&0xffff)))
    elif address==0x207b94c:value=vector['value']-1 if vector['kind']==2 else 0
    elif address==0x207b974:
        lower=vector['lower'+str(vector['pair'])];upper=vector['upper'+str(vector['pair'])];begin,end=vector['begin'],vector['end'];percentage=vector['percentage']
        if begin==0 and end==0:lower=upper;percentage=1
        elif vector['input']>begin:
            if vector['input']>=end:lower=upper
            elif begin!=end:lower+=divide((upper-lower)*(vector['input']-begin),end-begin)
        value=divide(lower*105,100) if percentage!=1 else lower
    elif address==0x207ba64:value=divide(vector['value']*6,5) if vector['mode']==1 else divide(vector['value']*3,2) if vector['mode']==2 else vector['value']
    elif address==0x207d31c:
        multipliers={1:(21,20),2:(11,10),3:(23,20),4:(6,5)};factor=multipliers.get(vector['mode']);value=divide(vector['value']*factor[0],factor[1]) if vector['flags']&2 and factor else vector['value']
    elif address==0x207d8e4:value=divide(vector['value']*6,5) if vector['mode'] and vector['code']==5 else vector['value']
    elif address==0x207f1a4:state=bytearray(after[COUNTER]);struct.pack_into('<I',state,4,1);after[COUNTER]=bytes(state);value=COUNTER
    elif address==0x207ffb4:
        data=image[0xdb298:0xdb298+1260];needle=bytes.fromhex(vector['needle']);match=next((i for i in range(420) if data[i*3:i*3+3]==needle),None);value=int(match is not None)
        if match is not None:output=bytearray(after[OUTPUT]);struct.pack_into('<HH',output,0,match//4,match%4);after[OUTPUT]=bytes(output)
    return value&0xffffffff,after


def run(image,row,body,vector,seed,helpers):
    address=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_ARM);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x200000);cpu.mem_write(0x2000000,image);cpu.mem_write(address,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x8000,0x9000);regions,arguments,stack=setup(address,vector,seed)
    for at,data in regions.items():cpu.mem_write(at,bytes(data))
    cpu.mem_write(SP,stack);initial=[(0x33440000+i*0x101+seed)&0xffffffff for i in range(15)];initial[:4]=arguments;initial[-2:]=[SP,STOP];cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x10)
    for register,value in zip(C.REGISTERS,initial):cpu.reg_write(register,value)
    allowed={a:helpers[a]['bytes'] for a in ALLOWED[address]};pcs=[];entries={a:0 for a in allowed};returned=False
    def code(machine,at,size,user):
        nonlocal returned
        if at==STOP:returned=True;machine.emu_stop();return
        if at in entries:entries[at]+=1
        if not address<=at<address+row['bytes'] and not any(base<=at<base+length for base,length in allowed.items()):raise ValueError(('Fixture escaped exact caller/original helper graph',hex(address),hex(at)))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if SP-0x8000<=at and at+size<=SP:return
        if address==0x207f1a4 and COUNTER<=at and at+size<=COUNTER+12:return
        if address==0x207ffb4 and OUTPUT<=at and at+size<=OUTPUT+8:return
        raise ValueError(('Fixture wrote outside declared caller memory/stack',hex(address),hex(at)))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(address,STOP+4,count=100000);registers=[cpu.reg_read(r) for r in C.REGISTERS]
    if not returned or registers[4:12]!=initial[4:12] or registers[13]!=SP or bytes(cpu.mem_read(SP,len(stack)))!=stack:raise ValueError(('Actual return/ABI/caller stack differs',hex(address),vector))
    value,after=expected(address,vector,regions,image);actual={a:bytes(cpu.mem_read(a,len(v))) for a,v in regions.items()};model=registers[0]==value and actual==after
    return dict(address=hex(address),vector=vector,seed=seed,topReturned=True,calleeSavedAbiPreserved=True,modelPassed=model,returnValue=registers[0],memorySha256=hashlib.sha256(b''.join(actual[a] for a in sorted(actual))).hexdigest(),pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest(),actualOriginalHelperEntries={hex(a):n for a,n in entries.items()},actualOriginalHelperInvocations=sum(entries.values()))


def wrong_case(address,image):
    if address==0x207b02c:return dict(index=0,flags=2,mask=2),'!=0','==0'
    if address==0x207b94c:return dict(value=100,kind=2),'if(kind==2)','if(kind==4)'
    if address==0x207b974:return dict(index=0,input=3,pair=0,percentage=1,begin=0,end=10,lower0=10,upper0=100,lower1=20,upper1=200),'if(percentage!=1)','if(percentage!=2)'
    if address==0x207ba64:return dict(value=100,mode=1),'if(mode==1)','if(mode==3)'
    if address==0x207d31c:return dict(index=0,value=100,mode=1,flags=2),'index,2)','index,4)'
    if address==0x207d8e4:return dict(value=100,mode=1,code=5),'code==5','code==4'
    if address==0x207f1a4:return dict(count=0,initialPending=3),'pending=1','pending=2'
    if address==0x207ffb4:return dict(needle=image[0xdb298:0xdb29b].hex()),'for(column=0;','for(column=1;'
    raise ValueError('No owned whole-C control')


def execute(rows):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();helpers={int(x['address'],0):x for x in original_helpers()};records=[];negative=[]
    for row in rows:
        address=int(row['address'],0);native=image[address-0x2000000:address-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed,vector in enumerate(vectors(address,image)):
            original=run(image,row,native,vector,seed,helpers);source=run(image,row,linked,vector,seed,helpers)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent range/flag/count/search model differs',row['address'],original,source))
            records.append(original)
        vector,old,new=wrong_case(address,image);folder=WORK/format(address,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for item in row['sourceDependencies']:shutil.copyfile(ROOT/item['path'],folder/(ROOT/item['path']).name)
        source=ROOT/row['source'];text=source.read_text();changed=text.replace(old,new,1)
        if text==changed:raise ValueError(('Whole wrong C did not mutate',row['address'],old))
        wrong=folder/source.name;wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong complete C changed native extent',row['address'],bad['compiledBytes'],row['bytes']))
        controls=[]
        for seed in range(16):
            actual=run(image,row,body,vector,seed,helpers)
            if actual['modelPassed'] or not actual['topReturned']:raise ValueError(('Wrong whole C did not actually return a model violation',row['address'],actual))
            controls.append(actual)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),genuineLink=bad['realLink'],compiledBytes=bad['compiledBytes'],actualReturningModelRejections=len(controls),records=controls))
    positive_helpers=2*sum(r['actualOriginalHelperInvocations'] for r in records);wrong_helpers=sum(r['actualOriginalHelperInvocations'] for n in negative for r in n['records']);report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=positive_helpers,actualPositiveOriginalHelperInvocations=positive_helpers,actualWrongCOriginalHelperInvocations=wrong_helpers,totalActualOriginalHelperInvocations=positive_helpers+wrong_helpers,nativeDevicesOrScenesExecuted=0,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest(),wholeCNegativeControlsRejected=len(negative),wrongC=negative,limits=['Bounded actual original/source caller execution uses original canonical helper bodies only on explicitly allowed paths. Synthetic in-memory 40-byte rows, first-match lookup record and empty shared-count state satisfy each declared interface; the original 1260-byte triple table is unchanged.','Models independently specify signed truncation, flags, interpolation/clamping, 105-percent adjustment under selection kind2, callback-loop zero/negative count behavior and first lexicographic triple match. Values avoid signed arithmetic overflow.','Random selector kinds0/3, positive shared-count callbacks, absent lookup modes/end-sentinel behavior, invalid indices/pointers, overflow, hardware and game scenes remain unexecuted. Original RNG and count-callback bodies are pinned but never executed. All helper, external storage and table authorship source credit remains zero.']);write_json(LANE/'caller-fixtures.json',report);return report
