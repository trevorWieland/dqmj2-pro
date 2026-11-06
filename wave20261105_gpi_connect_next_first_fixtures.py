import hashlib
import json
import random
import re
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_gpi_connect_next_first_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261105_gpi_connect_next_first_build import build

DATE,BLOCKING,REMOVE,DIV,DESTROY,REFERENCE,CONNECTION,NODES,STOP,SP=0x20adfbc,0x20afb40,0x20afad8,0x2026144,0x20afa8c,0x2170000,0x2171000,0x2173000,0x27e0000,0x2701000
HEAD=0x5c4


def helpers(image):
    inventory=(ROOT/'config/arm9/symbols.txt').read_text();out={}
    for address,mode,n in [(DIV,'arm',524),(DESTROY,'thumb',None)]:
        record=next((x for x in inventory.splitlines() if re.fullmatch(r'\S+ kind:function\(%s,size=0x[0-9a-f]+\) addr:0x%08x'%(mode,address),x)),None)
        if record is None:raise ValueError('Actual canonical signed-div/destructor entry/mode absent')
        size=int(re.search(r'size=0x([0-9a-f]+)',record)[1],16)
        if n is not None and size!=n:raise ValueError('Actual signed-div extent differs')
        out[address]=dict(address=hex(address),mode=mode,bytes=size,canonicalInventoryRecord=record,nativeSha256=hashlib.sha256(image[address-0x2000000:address-0x2000000+size]).hexdigest(),bodyExecuted=address==DIV,sourceCredit=0)
    return out


def valid_date(day,month,year):
    if day==month==year==0:return 1
    if min(day,month,year)<0:return 0
    if month==0:
        if day!=0:return 0
    elif month in [1,3,5,7,8,10,12]:
        if day>31:return 0
    elif month in [4,6,9,11]:
        if day>30:return 0
    elif month==2:
        leap=year%4==0 and year%100!=0 or year%400==0
        if day>29 if leap else day>28:return 0
    else:return 0
    if year<1900 or year>2079:return 0
    if year==2079 and (month>6 or month==6 and day>6):return 0
    return 1


def vector(a,seed):
    rng=random.Random(0x51c0000+a+seed);cases=[(0,0,0),(29,2,1900),(29,2,2000),(29,2,2004),(29,2,2001),(6,6,2079),(7,6,2079),(0,0,1900),(0,2,1900),(-1,1,2000),(1,-1,2000),(1,1,-1),(31,4,2000),(32,1,2000),(1,13,2000),(29,2,2147483647)]
    date=cases[seed%len(cases)] if seed<96 else (rng.choice([-1,0,1,28,29,30,31,32,2147483647]),rng.randrange(-1,15),rng.choice([-1,0,1899,1900,1996,2000,2001,2004,2078,2079,2080,2100,2147483647]));count=seed%5;nodes=[]
    for i in range(5):nodes.append(dict(type=rng.choice([0,1,3,4,6]),blocking=rng.randrange(2),id=17+i,next=NODES+(i+1)*36 if i+1<count else 0))
    target=0 if seed%4==0 else NODES+4*36 if seed%4==1 else NODES+(seed%max(1,count))*36
    return dict(date=list(date),count=count,nodes=nodes,target=target)


def run(image,row,body,v,seed,allowed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);cpu.mem_write(REFERENCE,struct.pack('<I',CONNECTION));connection=bytearray([0x77]*0x5d8);head=NODES if v['count'] else 0;struct.pack_into('<I',connection,HEAD,head);cpu.mem_write(CONNECTION,bytes(connection));nodes=bytearray()
    for i,r in enumerate(v['nodes']):nodes+=struct.pack('<9I',r['type'],0x2178000+i*4,r['blocking'],0,0,7,r['id'],0,r['next'])
    cpu.mem_write(NODES,bytes(nodes));expected_connection=bytearray(connection);expected_nodes=bytearray(nodes);provider_args=[]
    if a==DATE:args=v['date'];expected=dict(kind='return',value=valid_date(*args))
    elif a==BLOCKING:args=[REFERENCE];expected=dict(kind='return',value=int(any(r['blocking'] and r['type']!=3 for r in v['nodes'][:v['count']])))
    else:
        args=[REFERENCE,v['target']];index=(v['target']-NODES)//36 if v['target']>=NODES and (v['target']-NODES)%36==0 else -1
        if 0<=index<v['count']:
            if index==0:struct.pack_into('<I',expected_connection,HEAD,v['nodes'][index]['next'])
            else:struct.pack_into('<I',expected_nodes,(index-1)*36+32,v['nodes'][index]['next'])
            expected=dict(kind='provider',address=hex(DESTROY));provider_args=[REFERENCE,v['target']]
        else:expected=dict(kind='return')
    initial=[(0x55dd0000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
    for i,arg in enumerate(args):initial[i]=arg&0xffffffff
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;pcs=[];calls=[];interface=True
    def code(machine,at,size,user):
        nonlocal observed,interface
        if at==STOP:
            regs=[machine.reg_read(r) for r in C.REGISTERS]
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Date/list actual caller return ABI differs')
            observed=dict(kind='return',value=regs[0]) if 'value' in expected else dict(kind='return');machine.emu_stop();return
        if at==DESTROY:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Actual operation destructor mode differs')
            observed=dict(kind='provider',address=hex(at));regs=[machine.reg_read(r) for r in C.REGISTERS];interface=regs[:len(provider_args)]==provider_args;machine.emu_stop();return
        helper=allowed[DIV] if DIV<=at<DIV+allowed[DIV]['bytes'] else None
        if at==DIV:calls.append(at)
        wanted='thumb' if a<=at<a+row['bytes'] else 'arm' if helper else None;mode='thumb' if machine.reg_read(ar.UC_ARM_REG_CPSR)&32 else 'arm'
        if wanted is None or mode!=wanted:raise ValueError(('Date/list escaped original caller/helper/mode',hex(at),mode,wanted))
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not(SP-0x4000<=at and at+size<=SP) and not(CONNECTION<=at and at+size<=CONNECTION+len(connection)) and not(NODES<=at and at+size<=NODES+len(nodes)):raise ValueError(('Date/list unexpected write',hex(at),size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=100000)
    if observed is None:raise ValueError('Date/list caller did not reach actual return/provider')
    memory=bytes(cpu.mem_read(REFERENCE,4))==struct.pack('<I',CONNECTION) and bytes(cpu.mem_read(CONNECTION,len(connection)))==bytes(expected_connection) and bytes(cpu.mem_read(NODES,len(nodes)))==bytes(expected_nodes)
    return dict(address=row['address'],vector=v,seed=seed,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and memory and interface,providerInterfaceModelPassed=interface,independentMutationModelPassed=memory,actualOriginalHelperInvocations=len(calls),helperEntries=[hex(x) for x in calls],providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();allowed=helpers(image);records=[];negative=[];variants={DATE:('year % 100','year % 200'),BLOCKING:('operation->type != GPI_PROFILE_SEARCH','operation->type == GPI_PROFILE_SEARCH'),REMOVE:('if(pcurr == operation)','if(pcurr != operation)')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed in range(192):
            v=vector(a,seed);original=run(image,row,native,v,seed,allowed);source=run(image,row,linked,v,seed,allowed)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent date/list model differs',original,source))
            records.append(original)
        folder=WORK/'fixtures'/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        source=ROOT/row['source'];wrong=folder/source.name;text=source.read_text();old,new=variants[a];changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole date/list wrong-C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
        if bad['compiledBytes']!=row['bytes']:raise ValueError(('Wrong date/list C extent changed',row['address'],bad['compiledBytes']))
        failures=[]
        for seed in range(16):
            v=vector(a,seed)
            if a==DATE:v['date']=[29,2,1900]
            elif a==BLOCKING:
                v['count']=3
                for i,r in enumerate(v['nodes']):r.update(type=3,blocking=int(i==0),next=NODES+(i+1)*36 if i<2 else 0)
            else:
                v.update(count=3,target=NODES+36)
                for i,r in enumerate(v['nodes']):r['next']=NODES+(i+1)*36 if i<2 else 0
            result=run(image,row,body,v,seed,allowed)
            if result['modelPassed']:raise ValueError('Date/list wrong C accepted independent model')
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],actualReturningModelRejections=sum(r['topReturned'] for r in failures),partialModelRejections=sum(r['partialProviderStopped'] for r in failures),records=failures))
    limits=['Three complete ordinaryC date-validator/operation-blocking/unlink functions genuinely match full native extents and exact original interworking imports. Qualified GPIConnection prefix5d8/head5c4 and36-byte operation data4/block8/id24/next32 layout independently compiler-checked. No new suffix fields/source offsets guessed.','576paired entry vectors independently cover measured all-zero/zero-day/year-range1900..2079June6/century-leap date rules and acyclic0..4-node typed lists with null/missing/head/interior targets. Original canonicalARM524-byte signed-div helper executes actual code;0helper source credit or divide-zero execution.','Date/blocking and unmatched unlink paths return through actual caller entry. Matched unlink mutation/provider frames stop BEFORE actual canonicalThumb destructor020afa8c;0synthetic returns,deallocation/destructor body or callback effects. Date validation preserves original zero-component acceptance, not an inferred calendar policy.','Three complete same-extent wrong-C variants genuinely link and violate48 independent return/frame/mutation models.3wrong layouts and unchanged original call namespace/mode/kind/addend/origin/opcode controls reject. No full game/nativeWindows/hardware execution inferred.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),wholeCNegativeControlsRejected=len(negative),wrongC=negative,originalHelperEntries=list(allowed.values()),nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
