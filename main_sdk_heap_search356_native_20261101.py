import hashlib
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946,UC_ARM_REG_CPSR

DATA,STACK,STOP,COMMIT=0x02380000,0x03030000,0x0F000000,0x0202AE9C
HELPERS={0x0202AD78:44,0x0202ADA4:40,0x0202ADCC:48,0x0202ADFC:44,0x02008C14:20,0x0202B9CC:16}


def case(index,backwards):
    rng=random.Random(0x0202B044*10000+index)
    count=index%5;mode=index//5%2;request=(0,4,20,64,128,336,640)[index//10%7]
    alignment=(1,2,4,8,16,32,64)[(index*3+index//7)%7]
    flags=index//7%4;used=bool(index&1);group=rng.randrange(65536);feature=(rng.randrange(65536)&~1)|mode
    capacities=[(64,128,128,320)[(slot+index//11)%4]for slot in range(count)]
    return dict(count=count,mode=mode,request=request,alignment=alignment,flags=flags,used=used,group=group,
        feature=feature,capacities=capacities,backwards=backwards)


def execute(original,entry,caller,commit,index,budget=20000):
    spec=case(index,entry==0x0202B0F8);rng=random.Random(0x0202B044*10000+index)
    page=bytearray(rng.randbytes(4096));exp=DATA+0x40;nodes=[]
    for slot,capacity in enumerate(spec['capacities']):nodes.append(dict(address=DATA+0x200+slot*0x280,bytes=capacity))
    old_used=DATA+0xE00 if spec['used']else 0
    struct.pack_into('<IIIIIHH',page,exp-DATA-4,spec['flags'],nodes[0]['address']if nodes else 0,nodes[-1]['address']if nodes else 0,
        old_used,old_used,spec['group'],spec['feature'])
    for slot,node in enumerate(nodes):struct.pack_into('<HHIII',page,node['address']-DATA,0x4652,0,node['bytes'],nodes[slot-1]['address']if slot else 0,nodes[slot+1]['address']if slot+1<len(nodes)else 0)
    if old_used:struct.pack_into('<HHIII',page,old_used-DATA,0x5544,0x1234,32,0,0)
    expected=bytearray(page);pattern=rng.getrandbits(32);chosen=None;smallest=0xFFFFFFFF
    order=list(reversed(nodes))if spec['backwards']else nodes
    for node in order:
        body=node['address']+16
        aligned=((body+node['bytes']-spec['request'])&~(spec['alignment']-1))if spec['backwards']else((body+spec['alignment']-1)&~(spec['alignment']-1))
        eligible=aligned>=body if spec['backwards']else node['bytes']>=spec['request']+(aligned-body)
        if eligible and smallest>node['bytes']:
            chosen=dict(node,start=aligned);smallest=node['bytes']
            if spec['mode']==0 or node['bytes']==spec['request']:break
    result=0;new_free=[]
    if chosen:
        result=chosen['start'];header=result-16;end=chosen['address']+16+chosen['bytes'];used_end=result+spec['request']
        before=header-chosen['address'];fill_start=header if before>=20 else chosen['address']
        if end-used_end<20:used_end=end
        if spec['flags']&3:
            word=struct.pack('<I',0 if spec['flags']&1 else pattern)
            for off in range(fill_start-DATA,used_end-DATA,4):expected[off:off+4]=word
        for node in nodes:
            if node['address']!=chosen['address']:new_free.append(node)
            else:
                if before>=20:new_free.append(dict(address=node['address'],bytes=header-node['address']-16))
                if end-(result+spec['request'])>=20:new_free.append(dict(address=result+spec['request'],bytes=end-(result+spec['request'])-16))
        for slot,node in enumerate(new_free):
            struct.pack_into('<HHIII',expected,node['address']-DATA,0x4652,0,node['bytes'],new_free[slot-1]['address']if slot else 0,new_free[slot+1]['address']if slot+1<len(new_free)else 0)
        struct.pack_into('<II',expected,exp-DATA,new_free[0]['address']if new_free else 0,new_free[-1]['address']if new_free else 0)
        attributes=spec['backwards']<<15|((header-fill_start)&127)<<8|spec['group']&255
        struct.pack_into('<HHIII',expected,header-DATA,0x5544,attributes,used_end-header-16,old_used,0)
        struct.pack_into('<II',expected,exp-DATA+8,old_used or header,header)
        if old_used:struct.pack_into('<I',expected,old_used-DATA+12,header)
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_946)
    cpu.mem_map(0x02000000,0x400000);cpu.mem_write(0x02000000,original);cpu.mem_write(entry,caller);cpu.mem_write(COMMIT,commit)
    table=struct.unpack_from('<I',original,0x2B9D8)[0];cpu.mem_write(table+4,struct.pack('<I',pattern));cpu.mem_write(DATA,bytes(page))
    cpu.mem_map(STACK,4096);cpu.mem_write(STACK,bytes([0xA5])*4096);cpu.mem_map(STOP,4096)
    control=0x10|(index%4<<6);cpu.reg_write(UC_ARM_REG_CPSR,index%16<<28|control)
    initial=[rng.getrandbits(32)for unused in REGISTERS];initial[:3]=[exp-36,spec['request'],spec['alignment']];initial[-2:]=[STACK+0x800,STOP|(index&1)]
    for register,value in zip(REGISTERS,initial):cpu.reg_write(register,value)
    active=[];returns=[];writes=[];reads=[];visited=[];commit_entries=[];stopped=False
    def instruction(machine,address,width,user):
        nonlocal stopped
        while active and active[-1][1]==address:returns.append(active.pop()[0])
        if address==STOP:stopped=True;machine.emu_stop();return
        if address==COMMIT:
            sp=machine.reg_read(REGISTERS[-2]);commit_entries.append(dict(arguments=[machine.reg_read(register)for register in REGISTERS[:4]],fifthWord=struct.unpack('<I',machine.mem_read(sp,4))[0]))
        if address in HELPERS or address==COMMIT:active.append((address,machine.reg_read(REGISTERS[-1])&~1))
        if not(entry<=address<entry+len(caller)or COMMIT<=address<COMMIT+424 or any(a<=address<a+size for a,size in HELPERS.items())):
            raise ValueError('Connected heap execution escaped qualified original/source instruction scope')
        visited.append(address)
    def memory(machine,access,address,width,value,user):
        if not(DATA<=address and address+width<=DATA+4096 or STACK+0x700<=address and address+width<=STACK+0x800):
            raise ValueError('Connected heap write escaped disposable backing/own stack frame')
        writes.append([address,width,value&((1<<(8*width))-1)])
    cpu.hook_add(UC_HOOK_CODE,instruction);cpu.hook_add(UC_HOOK_MEM_WRITE,memory)
    cpu.hook_add(UC_HOOK_MEM_READ,lambda machine,access,address,width,value,user:reads.append([address,width]))
    cpu.emu_start(entry,STOP+4,count=budget)
    if not stopped or active or cpu.reg_read(REGISTERS[-2])!=STACK+0x800:raise ValueError('Connected heap caller did not return cleanly')
    if any(cpu.reg_read(REGISTERS[i])!=initial[i]for i in range(4,12))or cpu.reg_read(UC_ARM_REG_CPSR)&0xDF!=control:
        raise ValueError('Connected heap callee-save/control-mode ABI differs')
    if bytes(cpu.mem_read(STACK,0x700))!=bytes([0xA5])*0x700 or bytes(cpu.mem_read(STACK+0x800,0x800))!=bytes([0xA5])*0x800:
        raise ValueError('Connected heap outer stack guard differs')
    actual=bytes(cpu.mem_read(DATA,4096));value=cpu.reg_read(REGISTERS[0])
    expected_calls=[dict(arguments=[exp,chosen['address'],result,spec['request']],fifthWord=int(spec['backwards']))]if chosen else []
    call_model_passed=commit_entries==expected_calls
    return dict(case=spec,modelPassed=actual==bytes(expected)and value==result and call_model_passed,independentSelectionAndFifthWordPassed=call_model_passed,actualOwnReturn=True,sourceCredit=0,
        selectedAddress=hex(chosen['address'])if chosen else None,result=value,expectedResult=result,backingSha256=hashlib.sha256(actual).hexdigest(),
        expectedBackingSha256=hashlib.sha256(expected).hexdigest(),actualCommitEntries=commit_entries,
        actualCommitReturnsSeparate=returns.count(COMMIT),actualOriginalHelperReturnsSeparate=[hex(a)for a in returns if a!=COMMIT],
        rawRegisters=[cpu.reg_read(register)for register in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),orderedReads=reads,orderedWrites=writes,
        visited=sorted(set(visited)),fullMappedMemorySha256={hex(base):hashlib.sha256(bytes(cpu.mem_read(base,size))).hexdigest()for base,size in[(0x02000000,0x400000),(STACK,4096),(STOP,4096)]},providerReplacements=[])



def oracle(root,work,callers,commit):
    import gzip
    import json
    original=(root/'extract/arm9/arm9.bin').read_bytes()
    if hashlib.sha256(original).hexdigest()!='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f':raise ValueError('Original search main image differs')
    native_commit=original[COMMIT-0x02000000:COMMIT-0x02000000+424]
    if commit!=native_commit:raise ValueError('Fresh source-linked424 commit bytes differ')
    summaries={}
    for entry,code in sorted(callers.items()):
        size=180 if entry==0x0202B044 else 176
        native=original[entry-0x02000000:entry-0x02000000+size]
        if code!=native:raise ValueError('Complete freshly linked search C differs')
        records=[];visited=set();helper_count=0;commit_returns=0;selected=0;misses=0;nonfirst=0
        for index in range(560):
            first=execute(original,entry,native,native_commit,index);second=execute(original,entry,code,commit,index)
            if first!=second or not first['modelPassed']:raise ValueError('Fresh original/compiled connected search CPU/state/multi-block model differs')
            records.append(first);visited.update(pc for pc in first['visited']if entry<=pc<entry+size)
            commit_returns+=2*first['actualCommitReturnsSeparate'];helper_count+=2*len(first['actualOriginalHelperReturnsSeparate'])
            selected+=int(first['selectedAddress']is not None);misses+=int(first['selectedAddress']is None)
            if first['selectedAddress']is not None and first['case']['count']>1:
                first_addr=DATA+0x200+(first['case']['count']-1)*0x280 if first['case']['backwards']else DATA+0x200
                nonfirst+=int(int(first['selectedAddress'],0)!=first_addr)
        missing=sorted(set(range(entry,entry+size,4))-visited)
        if missing or not misses or not selected or not nonfirst:raise ValueError('Search branch/complete-instruction/nonfirst selection coverage missing')
        raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();path=work/(f'{entry:08x}-native-records.json.gz')
        path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
        summaries[hex(entry)]=dict(vectors=560,actualOriginalAndCompiledReturns=1120,actualFreshSourceLinkedCommitReturnsSeparate=commit_returns//2,
            actualOriginalCommitReturnsSeparate=commit_returns//2,actualOriginalAndSourceLinkedCommitReturnsSeparate=commit_returns,
            actualOriginalLowerHelperReturnsSeparate=helper_count,sourceLinkedCommitAdditionalCoverageCredit=0,providerReplacements=[],
            successfulSelectionCases=selected,missCases=misses,selectedBeyondFirstTraversalNodeCases=nonfirst,
            completeInstructionCoverage=dict(codeBytes=size,visited=sorted(visited),unvisited=missing),
            fullRawRegistersFlagsStackMemoryReadsWritesAndFifthWordCompared=True,independentMultiBlockHeapModel=True,
            trace=dict(path=path.relative_to(root).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=hashlib.sha256(path.read_bytes()).hexdigest(),gzipMtime=0),
            maxInstructionsPerExecution=20000,externalReplayDeadlineSeconds=300,
            limitations=['Stable sorted0..4 free nodes, zero/one existing used node, both first/best feature modes and power-of-two alignment1..64',
                'Word-rounded requests0/4/20/64/128/336/640; deterministicu16 feature/group and low two option bits',
                'Original lower helpers execute; fresh C424 commit is a separately pinned zero-additional-credit source-linked dependency',
                'Malformed/cyclic/concurrent lists, negative/nonpower-of-two alignment, physical heap ownership and scene feasibility unproved',
                'Original32-bit guest pointer/layout ABI; no Android/native64-bit portability claim'])
    return summaries


def wrong_body(root,work,entry,code,commit,label):
    import gzip
    import json
    original=(root/'extract/arm9/arm9.bin').read_bytes();records=[];rejections=0;helpers=0;commits=0
    for index in range(560):
        value=execute(original,entry,code,commit,index)
        rejections+=int(not value['modelPassed']);helpers+=len(value['actualOriginalHelperReturnsSeparate']);commits+=value['actualCommitReturnsSeparate']
        records.append(value)
    if not rejections:raise ValueError('Wrong ordinary search C survived the independent model')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();path=work/'native-records.json.gz'
    path.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
    return dict(name=label,address=hex(entry),compiledBytes=len(code),actualWrongSourceReturns=560,independentModelRejections=rejections,
        actualSourceLinkedCommitReturnsSeparate=commits,actualOriginalLowerHelperReturnsSeparate=helpers,providerReplacements=[],
        completeGeneratedBodyExecutedWithoutOriginalTail=True,trace=dict(path=path.relative_to(root).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),
            compressedSha256=hashlib.sha256(path.read_bytes()).hexdigest(),gzipMtime=0),additionalSourceCredit=0)
