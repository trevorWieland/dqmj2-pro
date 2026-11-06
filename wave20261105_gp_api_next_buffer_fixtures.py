import hashlib
import json
import re
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_gp_api_next_buffer_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_gp_api_next_buffer_build import build

CONN,OBJECT,VIEW,DATA,INPUT,OUT1,OUT2,IDENT,STOP,SP=0x216f000,0x2170000,0x2171000,0x2173000,0x2176000,0x2177000,0x2177010,0x2177020,0x27e0000,0x2701000
COPY,MOVE=0x201b19c,0x201b1bc
PROVIDERS={0x20a928c,0x20a8c24,0x20a8bf0,0x20ac734,0x20a9ed8}


def helpers(image):
    inventory=(ROOT/'config/arm9/symbols.txt').read_text().splitlines();result={}
    for a,size in [(COPY,32),(MOVE,76)]:
        record=next((x for x in inventory if re.fullmatch(r'\S+ kind:function\(arm,size=0x%x\) addr:0x%08x'%(size,a),x)),None)
        if record is None:raise ValueError('Actual canonical ARM byte copy/move entry differs')
        result[a]=dict(address=a,mode='arm',bytes=size,canonicalInventoryRecord=record,nativeSha256=hashlib.sha256(image[a-0x2000000:a-0x2000000+size]).hexdigest(),sourceCredit=0)
    return result


def vector(a,seed):
    length=[0,1,7,8,15,31,63,127][seed%8];capacity=length if seed%4==0 else 4096 if a==0x20ac880 and seed%3 else 128;position=length if seed%4==0 else length//2;return dict(length=length,capacity=capacity,position=position,count=[0,1,4,8,16,23,31,40][seed%8],nullString=seed%7==0,nullView=a==0x20acb98 and seed%8==1,nullData=a==0x20acb98 and seed%8==2,char=(seed*29)&255,clip=seed%2,ip=0x01020304,port=0x1234)


def run(image,row,body,v,seed,allowed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);state=bytearray([0xa7]*0x5d8);cpu.mem_write(OBJECT,bytes(state));cpu.mem_write(CONN,struct.pack('<I',OBJECT));raw=bytes((i*17+seed)&255 for i in range(4352));inputbytes=bytes((i*37+seed)&255 for i in range(128));cpu.mem_write(DATA,raw);cpu.mem_write(INPUT,inputbytes);cpu.mem_write(OUT1,bytes.fromhex('78563412'));cpu.mem_write(OUT2,bytes.fromhex('efbeadde'));cpu.mem_write(IDENT,b'CM\0');dataptr=0 if v['nullData'] else DATA;view=struct.pack('<Iiii',dataptr,v['capacity'],v['length'],v['position']);cpu.mem_write(VIEW,view);vp=0 if v['nullView'] else VIEW;source=0 if v['nullString'] else INPUT;args={0x20ac63c:[CONN,VIEW,v['char']],0x20ac684:[CONN,VIEW,source,v['count']],0x20ac734:[CONN,77,DATA,v['length'],OUT1,OUT2,IDENT],0x20ac880:[CONN,77,VIEW,OUT1,OUT2,IDENT],0x20ac954:[CONN,77,VIEW,OUT1,v['clip'],IDENT],0x20ac9e8:[CONN,v['ip'],v['port'],VIEW,OUT1,v['clip']],0x20acb98:[CONN,vp]}[a];initial=[(0x55dd0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
    for i,arg in enumerate(args):
        if i<4:initial[i]=arg
        else:cpu.mem_write(SP+4*(i-4),struct.pack('<I',arg&0xffffffff))
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    expected_view=bytearray(view);expected_data=bytearray(raw);remaining=v['length']-v['position']
    if a==0x20ac63c:
        expected=dict(kind='provider',address=hex(0x20a928c)) if v['capacity']==v['length'] else dict(kind='return',value=0)
        if expected['kind']=='return':expected_data[v['length']:v['length']+2]=bytes([v['char'],0]);struct.pack_into('<i',expected_view,8,v['length']+1)
    elif a==0x20ac684:
        expected=dict(kind='return',value=0) if not source else dict(kind='provider',address=hex(0x20a928c)) if v['capacity']-v['length']<v['count'] else dict(kind='return',value=0)
        if source and expected['kind']=='return':expected_data[v['length']:v['length']+v['count']]=inputbytes[:v['count']];expected_data[v['length']+v['count']]=0;struct.pack_into('<i',expected_view,8,v['length']+v['count'])
    elif a==0x20acb98:
        expected=dict(kind='return',value=0)
        if vp and dataptr and v['position']:
            expected_data[:remaining]=raw[v['position']:v['length']];expected_data[remaining]=0;struct.pack_into('<i',expected_view,8,remaining);struct.pack_into('<i',expected_view,12,0)
    elif a==0x20ac880:expected=dict(kind='provider',address=hex(0x20a928c if v['length']+2048>v['capacity'] else 0x20a8bf0))
    elif a in [0x20ac954,0x20ac9e8]:expected=dict(kind='return',value=0) if remaining==0 else dict(kind='provider',address=hex(0x20ac734 if a==0x20ac954 else 0x20a9ed8))
    else:expected=dict(kind='provider',address=hex(0x20a8c24))
    observed=None;pcs=[];calls=[];interface=True
    def code(machine,at,size,user):
        nonlocal observed,interface
        if at==STOP:
            regs=[machine.reg_read(r) for r in C.REGISTERS]
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Buffer actual caller return ABI differs')
            observed=dict(kind='return',value=regs[0]);machine.emu_stop();return
        if at in PROVIDERS and at!=a:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Buffer provider original mode differs')
            regs=[machine.reg_read(r) for r in C.REGISTERS];observed=dict(kind='provider',address=hex(at))
            if at==0x20a928c:interface=regs[:2]==[DATA,(v['capacity']+2048+1 if a==0x20ac63c else v['capacity']+max(2048,v['count'])+1 if a==0x20ac684 else v['length']+2048+1)]
            elif at==0x20a8c24:interface=regs[:4]==[77,DATA,v['length'],0]
            elif at==0x20a8bf0:interface=regs[:4]==[77,DATA+v['length'],v['capacity']-v['length'],0]
            elif at==0x20ac734:interface=regs[:4]==[CONN,77,DATA+v['position'],remaining] and struct.unpack('<I',bytes(machine.mem_read(regs[13]+8,4)))[0]==IDENT
            elif at==0x20a9ed8:interface=regs[:2]==[v['ip'],v['port']]
            machine.emu_stop();return
        entry=next((r for start,r in allowed.items() if start<=at<start+r['bytes']),None)
        if at in allowed:calls.append(at)
        if a<=at<a+row['bytes']:mode='thumb'
        elif entry:mode=entry['mode']
        else:raise ValueError(('Buffer escaped actual bounded RAM helper graph',hex(at)))
        if bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(mode=='thumb'):raise ValueError('Buffer caller/helper actual mode differs')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not (SP-0x4000<=at and at+size<=SP+4*max(0,len(args)-4) or VIEW<=at and at+size<=VIEW+16 or DATA<=at and at+size<=DATA+4352):raise ValueError(('Buffer unexpected write',hex(a),hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=100000)
    if observed is None:raise ValueError('Buffer did not reach authentic return/provider boundary')
    guards=bytes(cpu.mem_read(VIEW,16))==bytes(expected_view) and bytes(cpu.mem_read(DATA,4352))==bytes(expected_data) and bytes(cpu.mem_read(INPUT,128))==inputbytes and bytes(cpu.mem_read(OBJECT,0x5d8))==bytes(state) and bytes(cpu.mem_read(OUT1,4))==bytes.fromhex('78563412') and bytes(cpu.mem_read(OUT2,4))==bytes.fromhex('efbeadde')
    return dict(address=row['address'],vector=v,seed=seed,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and interface and guards,providerInterfaceModelPassed=interface,actualOriginalHelperInvocations=len(calls),helperEntries=[hex(x) for x in calls],bufferAndInputGuardsPreserved=guards,providerInstructionExecutions=0,bufferSha256=hashlib.sha256(bytes(cpu.mem_read(DATA,4352))).hexdigest(),view=bytes(cpu.mem_read(VIEW,16)).hex(),pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();allowed=helpers(image);records=[];negative=[]
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed in range(32):
            v=vector(a,seed);original=run(image,row,native,v,seed,allowed);source=run(image,row,linked,v,seed,allowed)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent buffer byte/length/provider model differs',original,source))
            records.append(original)
        if a not in [0x20ac63c,0x20ac684,0x20ac880,0x20acb98]:continue
        folder=WORK/'fixtures'/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;text=source.read_text();header_only=a==0x20ac880
        if header_only:
            p=folder/'context.h';p.write_text(p.read_text().replace('#define GPI_READ_SIZE 2048','#define GPI_READ_SIZE 4096'));changed=text
        else:
            old,new=('if(size == len)','if(size != len)') if a==0x20ac63c else ('if((size - len) < stringLen)','if((size - len) > stringLen)') if a==0x20ac684 else ('buffer->len -= buffer->pos;','buffer->len += buffer->pos;');changed=text.replace(old,new,1)
            if changed==text:raise ValueError('Whole buffer C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong buffer C extent changed',row['address'],bad['compiledBytes']))
        failures=[]
        for seed in range(16):
            v=vector(a,seed);v.update(length=8,position=4,capacity=128,count=4,nullString=False,nullView=False,nullData=False);result=run(image,row,body,v,seed,allowed)
            if result['modelPassed']:raise ValueError('Wrong buffer C did not violate independent byte/allocator model')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),sourceDependencies=bad['sourceDependencies'],algorithmHeaderConstantChanged=header_only,compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],returningModelRejections=sum(r['topReturned'] for r in failures),partialModelRejections=sum(r['partialProviderStopped'] for r in failures),records=failures))
    limits=['Seven ordinary C complete native extents genuinely link with original call/data witnesses. Nintendo growth quantum2048 differs public16384; successful grown input pointer/size commit before recv is preserved from measured native instructions. No original object-storage/helper-source credit.','224 bounded vectors compare actual native/genuine compiled caller instructions with independent byte-array append/overlap-clip, length/position and allocator/socket/provider argument models. Actual original ARM32 memcpy/ARM76 memmove execute only on RAM paths. Other paths stop BEFORE real realloc/socket/GP/UDP provider instructions, with0 synthetic returns/provider bodies/network operations.','Four same-extent whole ordinary C/header algorithm variants genuinely link and violate64 independent observations; growth-constant and capacity predicate errors are partial provider failures, while wrong overlap length actually returns a model failure. Wrong buffer scalar width is rejected by native compiler geometry.','Successful growth callbacks, receive/send results, network state, complete GP connection object extent and full game/Windows/hardware execution remain unproven/uncredited; no later provider behavior is inferred from exact compilation.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),wholeCNegativeControlsRejected=len(negative),wrongC=negative,originalHelperEntries=list(allowed.values()),nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
