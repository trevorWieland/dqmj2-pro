import hashlib
import struct
from project import ROOT,read_json,write_json,sha256
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_SP,UC_ARM_REG_CPSR
from match_runtime import REGISTERS

TABLE=0x020D3FE0
DATA=0x03010000
STACK=0x03020000
STOP=0x0F000000
ENTRIES=[0x02027FE8,0x02028044,0x020280A0]
HELPERS=[(0x02000DCC,28),(0x02000DE8,28),(0x02000E04,24)]


def phase_index(raw):
    signed=raw if raw<0x80000000 else raw-0x100000000
    high=((signed*0xB60B60B60B)>>32)&0xFFFFFFFF
    return (((high+0x800)&0xFFFFFFFF)>>16)&4095


def execute(arm,table,raw,axis,expected):
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    for base,size in [(0x02000000,0x1000),(0x02027000,0x2000),(0x020D3000,0x5000),(DATA,0x1000),(STACK,0x1000),(STOP,0x1000)]:
        uc.mem_map(base,size)
    uc.mem_write(0x02000000,arm[:0x1000]);uc.mem_write(0x02027000,arm[0x27000:0x29000]);uc.mem_write(TABLE,table)
    guard=bytes((i*29+raw+axis)&255 for i in range(4096));uc.mem_write(DATA,guard);uc.mem_write(STACK,b'\xB7'*4096)
    for base,size in [(0x02000000,0x1000),(0x02027000,0x2000),(STOP,0x1000)]:uc.mem_protect(base,size,UC_PROT_READ|UC_PROT_EXEC)
    uc.mem_protect(0x020D3000,0x5000,UC_PROT_READ)
    for index,register in enumerate(REGISTERS):uc.reg_write(register,(0xA0110000+index*0x101)&0xFFFFFFFF)
    initial=[uc.reg_read(register) for register in REGISTERS]
    uc.reg_write(UC_ARM_REG_CPSR,0xA0000013);uc.reg_write(UC_ARM_REG_R0,DATA+0x100);uc.reg_write(UC_ARM_REG_R1,raw)
    uc.reg_write(UC_ARM_REG_SP,STACK+0xF00);uc.reg_write(UC_ARM_REG_LR,STOP)
    entry=ENTRIES[axis];helper,helper_size=HELPERS[axis]
    pcs=[];reads=[];writes=[];state={'helperEntries':0,'helperReturns':0}
    index=phase_index(raw)
    sine,cosine=expected[index]
    def code(machine,address,size,user):
        if not (entry<=address<entry+84 or helper<=address<helper+helper_size):raise AssertionError(('unexpected PC',hex(address)))
        pcs.append(address)
        if address==helper:
            state['helperEntries']+=1
            assert machine.reg_read(UC_ARM_REG_R1)==(sine&0xFFFFFFFF) and machine.reg_read(REGISTERS[2])==(cosine&0xFFFFFFFF)
        if address==entry+80:
            state['helperReturns']+=1
    def read(machine,access,address,size,value,user):
        if TABLE<=address<TABLE+16384:reads.append((address,size))
    def write(machine,access,address,size,value,user):
        writes.append((address,size,value&((1<<(size*8))-1)))
    uc.hook_add(UC_HOOK_CODE,code);uc.hook_add(UC_HOOK_MEM_READ,read);uc.hook_add(UC_HOOK_MEM_WRITE,write)
    uc.emu_start(entry,STOP,count=200)
    assert uc.reg_read(UC_ARM_REG_PC)==STOP and uc.reg_read(UC_ARM_REG_SP)==STACK+0xF00
    assert [uc.reg_read(register) for register in REGISTERS[4:12]]==initial[4:12]
    assert state=={'helperEntries':1,'helperReturns':1}
    assert reads==[(TABLE+index*4,2),(TABLE+index*4+2,2)]
    matrices=[(4096,0,0,0,cosine,sine,0,-sine,cosine),(cosine,0,-sine,0,4096,0,sine,0,cosine),(cosine,sine,0,-sine,cosine,0,0,0,4096)]
    model=bytearray(guard);model[0x100:0x124]=struct.pack('<9i',*matrices[axis])
    memory=bytes(uc.mem_read(DATA,4096));assert memory==bytes(model)
    order=[0,4,8,12,16,20,24,28,32] if axis!=1 else [0,32,4,12,20,28,24,8,16]
    actual=[(address-DATA-0x100,size,value) for address,size,value in writes if DATA<=address<DATA+4096]
    assert [offset for offset,size,value in actual]==order and all(size==4 for offset,size,value in actual)
    return ([uc.reg_read(register) for register in REGISTERS],uc.reg_read(UC_ARM_REG_CPSR),memory,bytes(uc.mem_read(STACK,4096)),pcs,reads,writes)


def main(source_wrappers=None,source_table=None):
    from derive_sdk_trig_20261031 import derive
    pairs,_=derive()
    arm=(ROOT/'extract/arm9/arm9.bin').read_bytes()
    assert sha256(ROOT/'extract/arm9/arm9.bin')=='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
    original=arm[TABLE-0x02000000:TABLE-0x02000000+16384]
    source_arm=bytearray(arm)
    for item in source_wrappers or []:
        binary=ROOT/item['binary'];assert sha256(binary)==item['sha256']
        payload=binary.read_bytes();address=int(item['address'],0);assert len(payload)==92
        source_arm[address-0x02000000:address-0x02000000+92]=payload
    source_arm=bytes(source_arm)
    table_path=(ROOT/source_table).resolve() if source_table else ROOT/'work/sdk-trig-source-20261031/sincos-linked.bin'
    assert table_path.is_relative_to(ROOT)
    source=table_path.read_bytes()
    assert source==original
    cases=[(phase*360,phase%3) for phase in range(4096)]
    cases += [(raw&0xFFFFFFFF,axis) for raw in [-2147483648,-1474560,-360,-1,0,1,359,360,1474559,1474560,2147483647] for axis in range(3)]
    digest=hashlib.sha256();phases=set();maximum=0;coverage={str(i):set() for i in range(3)}
    for ordinal,(raw,axis) in enumerate(cases):
        native=execute(arm,original,raw,axis,pairs);rebuilt=execute(source_arm,source,raw,axis,pairs);assert native==rebuilt
        phases.add(phase_index(raw));coverage[str(axis)].update(native[4]);maximum=max(maximum,len(native[4]))
        digest.update(struct.pack('<II',raw,axis));digest.update(native[2]);digest.update(struct.pack('<15I',*native[0]))
        if ordinal%512==0:print({'contextsCompleted':ordinal+1},flush=True)
    assert len(phases)==4096
    report={'sourceCredit':0,'compiledWrapperInputs':source_wrappers or [],'compiledOrdinaryWrapperBytes':92*len(source_wrappers or []),'generator':'sdk_trig_native_oracle_20261031.py','generatorSha256':sha256(ROOT/'sdk_trig_native_oracle_20261031.py'),
        'dataReport':'evidence/data/sdk-trig-table-20261031.json','contexts':len(cases),'actualTopLevelReturns':len(cases)*2,
        'actualNativeMatrixHelperReturns':len(cases)*2,'providedCalls':0,'distinctPairIndices':len(phases),'signed16NativeTableReads':len(cases)*4,
        'nativeCaseDigest':digest.hexdigest(),'maximumInstructions':maximum,'instructionLimit':200,'wallClockWatchdog':False,'actualReturnRequired':True,'sourceTableBinary':table_path.relative_to(ROOT).as_posix(),'sourceTableBinarySha256':sha256(table_path),'fullOutputAndGuardsModeled':True,
        'orderedWritesModeled':True,'allRegistersFlagsStackAndTraceEqual':True,'coverage':{axis:sorted(hex(x) for x in rows) for axis,rows in coverage.items()},
        'limitations':['Actual original/compiled wrapper provenance is explicit; original Thumb matrix helpers remain separate and receive no new source credit','Raw angle words and matrix storage are synthetic; no current game scene or native host port is claimed']}
    output='sdk-trig-source-wrappers-20261031.json' if source_wrappers else 'sdk-trig-native-consumers-20261031.json'
    write_json(ROOT/'evidence/verification'/output,report)
    print({key:report[key] for key in ['contexts','actualTopLevelReturns','distinctPairIndices','providedCalls','maximumInstructions']})


if __name__=='__main__':
    main()
