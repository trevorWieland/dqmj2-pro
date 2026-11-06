import gzip
import json
import struct
import match_runtime
from project import ROOT,configuration,sha256,write_json
from link_runtime_unit import measured_module
import mechanics_save_native_name_oracle as legacy
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
BASE,STACK,STOP=0x02000000,0x027F0000,0x027FF800
ROOTS,POINTERS,LEAVES=0x020DA084,0x02500000,0x02501000
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]


def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


def memory_fixture():
    memory={ROOTS:bytearray(24*4),POINTERS:bytearray(0x1000),LEAVES:bytearray(0x4000)};groups=[0,1,2,21];leaves={}
    for number,group in enumerate(groups):
        struct.pack_into('<I',memory[ROOTS],group*4,POINTERS+group*16)
        for table in range(4):
            leaf=LEAVES+(number*4+table)*0x400;leaves[group,table]=leaf;struct.pack_into('<I',memory[POINTERS],group*16+table*4,leaf)
            for index in range(256):
                value=0x90000000|(group<<20)|(table<<16)|(index*4)
                if group==0 and table==0 and index<3:value=[0,0xFFFFFFFF,0x80000000][index]
                struct.pack_into('<I',memory[LEAVES],leaf-LEAVES+index*4,value)
    return memory,leaves


def machine(arm):
    u=Uc(UC_ARCH_ARM,UC_MODE_ARM);u.ctl_set_cpu_model(UC_CPU_ARM_946);u.mem_map(BASE,0x800000);u.mem_write(BASE,arm);u.reg_write(UC_ARM_REG_CPSR,0x10);initial=[0xA0460000+i*0x100 for i in range(13)]
    for reg,value in zip(REGS,initial):u.reg_write(reg,value)
    u.reg_write(UC_ARM_REG_SP,STACK);u.reg_write(UC_ARM_REG_LR,STOP);return u,initial


def returned(u,initial):
    if u.reg_read(UC_ARM_REG_PC)!=STOP or u.reg_read(UC_ARM_REG_SP)!=STACK or u.reg_read(UC_ARM_REG_CPSR)&63!=16 or[u.reg_read(r)for r in REGS[4:12]]!=initial[4:12]:raise ValueError('546 actual return orcallee-saved frame differs')


def pointer_case(arm,memory,leaves,group,table,index,erased=False):
    u,initial=machine(arm)
    for address,data in memory.items():u.mem_write(address,bytes(data))
    u.reg_write(UC_ARM_REG_R0,group);u.reg_write(UC_ARM_REG_R1,table);u.reg_write(UC_ARM_REG_R2,0 if erased else index);reads=[];writes=[];observed=[]
    def code(vm,a,size,data):
        if not 0x0205DC70<=a<0x0205DC88:raise ValueError('546 pointer escaped native range')
        observed.append(a)
    def read(vm,access,a,size,value,data):reads.append([vm.reg_read(UC_ARM_REG_PC),a,size])
    def write(vm,access,a,size,value,data):writes.append([a,size,value])
    u.hook_add(UC_HOOK_CODE,code);u.hook_add(UC_HOOK_MEM_READ,read);u.hook_add(UC_HOOK_MEM_WRITE,write);u.emu_start(0x0205DC70,STOP,count=32);returned(u,initial);expected=legacy.pointer(memory,group,table,index);actual=u.reg_read(UC_ARM_REG_R0);effective=0 if erased else index;addresses=[0x0205DC84,ROOTS+group*4,POINTERS+group*16+table*4,leaves[group,table]+effective*4]
    if [r[1]for r in reads]!=addresses or any(r[2]!=4 for r in reads)or writes or u.reg_read(UC_ARM_REG_R1)!=table or u.reg_read(UC_ARM_REG_R2)!=effective or u.reg_read(UC_ARM_REG_R3)!=ROOTS:raise ValueError('546 triple-pointer read contract differs')
    if not erased and actual!=expected:raise ValueError('546 independent legacy pointer model differs')
    return dict(group=group,table=table,index=index,erasedR2=erased,reads=reads,returnedR0=actual,expectedR0=expected,argumentErasureRejected=actual!=expected,actualTopReturns=1,providedCalls=0)


def navigation_case(arm,pointer,low,high,held):
    u,initial=machine(arm);keys=struct.unpack_from('<I',arm,0x0202A63C-BASE)[0];repeat=struct.unpack_from('<I',arm,0x020494B8-BASE)[0];u.mem_write(keys,bytes(0x40));u.mem_write(pointer,bytes(0x40));u.mem_write(keys,struct.pack('<H',held));u.mem_write(keys+6,struct.pack('<H',0x10));u.mem_write(pointer+12,struct.pack('<2H',low,high));u.mem_write(repeat+1,b'\x77');u.reg_write(UC_ARM_REG_R0,pointer);before=bytes(u.mem_read(BASE,0x800000));reads=[];writes=[];observed=[];getter=[];getterReturns=[]
    def code(vm,a,size,data):
        if not(0x020491F8<=a<0x020494BC or 0x0202A634<=a<0x0202A640):raise ValueError(('546 early navigation escaped range',hex(a)))
        observed.append(a)
        if a==0x0202A634:getter.append([vm.reg_read(UC_ARM_REG_SP),vm.reg_read(UC_ARM_REG_LR)])
        if a==0x02049204:
            if vm.reg_read(UC_ARM_REG_SP)!=STACK-24 or vm.reg_read(UC_ARM_REG_R0)!=keys or vm.reg_read(UC_ARM_REG_CPSR)&32:raise ValueError('546 native getter actual return differs')
            getterReturns.append(a)
    def read(vm,access,a,size,value,data):
        if pointer<=a<pointer+0x40:reads.append([vm.reg_read(UC_ARM_REG_PC),a,size])
    def write(vm,access,a,size,value,data):
        if not STACK-4096<=a<STACK:writes.append([a,size,value&((1<<(size*8))-1)])
    u.hook_add(UC_HOOK_CODE,code);u.hook_add(UC_HOOK_MEM_READ,read);u.hook_add(UC_HOOK_MEM_WRITE,write);u.emu_start(0x020491F8,STOP,count=256);returned(u,initial);after=bytes(u.mem_read(BASE,0x800000));want=bytearray(before)
    if held==0:want[repeat+1-BASE]=0
    if after[:STACK-4096-BASE]!=bytes(want[:STACK-4096-BASE])or after[STACK-BASE:]!=bytes(want[STACK-BASE:])or u.reg_read(UC_ARM_REG_R0)!=0:raise ValueError('546 early navigation effect model differs')
    if reads!=[[0x0204922C,pointer+12,2],[0x02049230,pointer+14,2]]or getter!=[[STACK-24,0x02049204]]or getterReturns!=[0x02049204]:raise ValueError('546 navigation descriptor reads oractualgetter frame differs')
    expectedWrites=[]if held else[[repeat+1,1,0]]
    if writes!=expectedWrites:raise ValueError('546 navigation ordered write model differs')
    return dict(pointer=pointer,low=low,high=high,held=held,reads=reads,writes=writes,returnedR0=0,actualTopReturns=1,actualNativeDependencyReturns=1,providedCalls=0,observed=observed)


def run():
    if sha256(ROOT/'mechanics_save_native_name_oracle.py')!='30cdab70d02c1e32ada49400698dc75708fd7596b60a19d49625ffc1981415cd':raise ValueError('546 legacy pure pointer model changed')
    meta,arm,symbols=measured_module('main');overlay,body,unused=measured_module('ov002');memory,leaves=memory_fixture();pointer=[];navigation=[];negatives=[]
    for group in[0,1,2,21]:
        for table in range(4):
            for index in[0,1,2,15,127,255]:pointer.append(pointer_case(arm,memory,leaves,group,table,index))
    for address in[0x02600000,0x02601000]:
        for low,high in[(0,0),(1,0),(2,1),(65535,65534)]:
            for held in[0,1]:navigation.append(navigation_case(arm,address,low,high,held))
    for group,table,index in[(0,0,1),(21,3,255)]:
        case=pointer_case(arm,memory,leaves,group,table,index,True)
        if not case['argumentErasureRejected']:raise ValueError('546 erased R2 control unexpectedly agrees')
        negatives.append(case)
    sites=[]
    for a,n,reason in[(0x021D9430,20,'DA040 return remains R0 across MOVR4/LDRR8/LDRR5 until BL491F8'),(0x021D95C8,24,'LSR writes selected unsigned16 intoR2; STRH preserves it; MOVR0/R1 then BL5DC70'),(0x021D9784,32,'Second path explicitlymoves computed unsigned16 fromR6 toR2 before BL5DC70')]:sites.append(dict(module='ov002',address=hex(a),bytes=n,sha256=match_runtime.sha(body[a-0x021D7240:a-0x021D7240+n]),reason=reason))
    traces=dict(pointer=pointer,navigation=navigation,erasedArgumentControls=negatives);payload=encoded(traces);archive=ROOT/'evidence/generated/ov002-inputs546-native-traces-20261101.json.gz';archive.write_bytes(gzip.compress(payload,mtime=0));report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',evidenceClass='native-input-requirements',sourceCredit=0,matchedBytes=0,moduleSha256=meta['sha256'],overlayModule='ov002',overlaySha256=overlay['sha256'],subjectCaller=dict(address='0x021D9420',mode='arm',bytes=1040,sha256=match_runtime.sha(body[0x021D9420-0x021D7240:0x021D9420-0x021D7240+1040])),callerSites=sites,qualifiedInputs=[dict(module='main',address='0x020491F8',mode='arm',bytes=708,sha256=match_runtime.sha(arm[0x020491F8-BASE:0x020494BC-BASE]),incoming='R0 descriptor pointer',scope='Supported key6 mask0x10 path readsunsigned16 offsets0x0C/0x0E; boundhigh<=low returns0; otherpaths andformal typedefs areunqualified'),dict(module='main',address='0x0205DC70',mode='arm',bytes=24,sha256=match_runtime.sha(arm[0x0205DC70-BASE:0x0205DC88-BASE]),incoming='R0 group,R1 table,R2 index',scope='Three fullword-indexed loads are directlyobserved; no boundsguard orlegalgame domain claim')],acceptedSourceProvenance=dict(path='src/mechanics_save/native_name.c',sha256=sha256(ROOT/'src/mechanics_save/native_name.c'),duplicateSourceCredit=0),existingIndependentModel=dict(path='mechanics_save_native_name_oracle.py',sha256=sha256(ROOT/'mechanics_save_native_name_oracle.py'),pureApi='pointer(memory,group,table,index)',historicalValidateNotInvoked=True),pointerCases=len(pointer),navigationCases=len(navigation),actualTopReturns=len(pointer)+len(navigation),actualNativeDependencyReturns=len(navigation),providedCalls=0,negativeEvidence=dict(erasedR2Controls=negatives,actualTopReturns=len(negatives),sourceCredit=0),traceArchive=dict(path=archive.relative_to(ROOT).as_posix(),sha256=sha256(archive),decodedSha256=match_runtime.sha(payload)),generatorSha256=sha256(__file__),reproductionCommand='python prove_ov002_inputs546_20261101.py',limits=['Both raw M2C542 andindependent Ghidra543 omit required live R0/R2 atthese caller sites; nativeinstruction/VM evidence isauthoritative','All executions usefresh ARM946 machines andrequireactual return,SP/callee-saved restoration andbounded PC ranges','Navigation probes coveronly theexplicit bound-rejection path; theydo not establish full routine behavior,clean global byte return orcomplete original formal signature','Triplepointer indices androots aredeterministic synthetic fixtures,including returned0/FFFFFFFF/80000000; no text encoding,asset reachability orvalid-index restriction isinferred','No accepted source,shared catalogue,adapter orregistry changes; freshcaller overrides only; zero new source credit'])
    write_json(ROOT/'evidence/verification/ov002-inputs546-native-20261101.json',report);print(dict(actualTopReturns=report['actualTopReturns'],actualNativeDependencyReturns=report['actualNativeDependencyReturns'],providedCalls=0,erasedR2Controls=len(negatives)))

if __name__=='__main__':run()
