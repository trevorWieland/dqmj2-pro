import struct
from project import ROOT,write_json,sha256
import match_runtime as compiler
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from sdk_trig_native_oracle_20261031 import execute,phase_index,REGISTERS,DATA,STACK,STOP,TABLE
from derive_sdk_trig_20261031 import derive
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR

ENTRY=0x02027FE8
HELPER=0x02000DCC


def run_mutant(arm,payload,raw,return_offset):
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    for base,size in [(0x02000000,0x1000),(0x02027000,0x2000),(0x020D3000,0x5000),(DATA,0x1000),(STACK,0x1000),(STOP,0x1000)]:uc.mem_map(base,size)
    uc.mem_write(0x02000000,arm[:4096]);uc.mem_write(0x02027000,arm[0x27000:0x29000]);uc.mem_write(ENTRY,payload)
    uc.mem_write(TABLE,arm[0xD3FE0:0xD7FE0])
    guard=bytes((i*29+raw)&255 for i in range(4096));uc.mem_write(DATA,guard);uc.mem_write(STACK,b'\xB7'*4096)
    for base,size in [(0x02000000,4096),(0x02027000,8192),(STOP,4096)]:uc.mem_protect(base,size,UC_PROT_READ|UC_PROT_EXEC)
    uc.mem_protect(0x020D3000,0x5000,UC_PROT_READ)
    for i,register in enumerate(REGISTERS):uc.reg_write(register,0xA0110000+i*0x101)
    preserved=[uc.reg_read(register) for register in REGISTERS[4:12]]
    uc.reg_write(UC_ARM_REG_CPSR,0xA0000013);uc.reg_write(UC_ARM_REG_R0,DATA+0x100);uc.reg_write(UC_ARM_REG_R1,raw)
    uc.reg_write(UC_ARM_REG_SP,STACK+0xF00);uc.reg_write(UC_ARM_REG_LR,STOP)
    state={'helperEntries':0,'helperReturns':0,'instructions':0}
    def code(machine,address,size,user):
        assert ENTRY<=address<ENTRY+len(payload)-8 or HELPER<=address<HELPER+28
        state['instructions']+=1
        if address==HELPER:state['helperEntries']+=1
        if address==ENTRY+return_offset:state['helperReturns']+=1
    uc.hook_add(UC_HOOK_CODE,code);uc.emu_start(ENTRY,STOP,count=200)
    assert uc.reg_read(UC_ARM_REG_PC)==STOP and uc.reg_read(UC_ARM_REG_SP)==STACK+0xF00
    assert [uc.reg_read(register) for register in REGISTERS[4:12]]==preserved
    assert state['helperEntries']==state['helperReturns']==1
    return bytes(uc.mem_read(DATA,4096)),state


def main():
    arm=(ROOT/'extract/arm9/arm9.bin').read_bytes();pairs,_=derive()
    source=(ROOT/'src/math/20261031_trig/sincos_wrappers.c').read_text()
    variants=[('wrong-rounding-bias',source.replace('0x80000000000ULL','0x90000000000ULL')),
        ('wrong-unsigned-angle',source.replace('(u64)(s64)angle','(u64)(u32)angle'))]
    base=ROOT/'work/sdk-trig-wrapper-controls-20261031';directory=ROOT/'nonmatching/math/20261031'
    directory.mkdir(parents=True,exist_ok=True);compiler.WORK=base/'compile'
    controls=[];returns=0
    for name,text in variants:
        path=directory/(name+'.c');path.write_text(text,encoding='utf-8');rows,_=compiler.compare(path,'main',2,'off')
        row=next(x for x in rows if int(x['address'],0)==ENTRY)
        output=base/name
        try:validate(row,qualified_bindings(row),directory=output)
        except ValueError as error:refusal=str(error)
        else:raise AssertionError('Wrong complete C caller matched')
        binary=output/'caller.bin';payload=binary.read_bytes();assert payload!=arm[0x27FE8:0x28044]
        call=next(x for x in row['relocations'] if x['symbol']=='native_fn_02000dcc')
        rejects=0;positives=0;cases=[]
        for value in [0,1,348,349,360,-1,-360,-2147483648,2147483647]:
            raw=value&0xFFFFFFFF
            native=execute(arm,arm[0xD3FE0:0xD7FE0],raw,0,pairs)
            changed,state=run_mutant(arm,payload,raw,call['offset']+4)
            source_value=value if name!='wrong-unsigned-angle' else raw
            bias=0x900 if name=='wrong-rounding-bias' else 0x800
            high=((source_value*0xB60B60B60B)>>32)&0xFFFFFFFF
            index=(((high+bias)&0xFFFFFFFF)>>16)&4095
            sine,cosine=pairs[index]
            model=bytearray(bytes((i*29+raw)&255 for i in range(4096)))
            model[0x100:0x124]=struct.pack('<9i',4096,0,0,0,cosine,sine,0,-sine,cosine)
            assert changed==bytes(model)
            bad=changed!=native[2];rejects+=bad;positives+=not bad;returns+=2
            cases.append({'rawInput':hex(raw),'nativeIndex':phase_index(raw),'mutantIndex':index,'actualReturns':2,'memoryRejected':bad,'positiveControl':not bad,'mutantInstructions':state['instructions']})
        assert rejects and positives
        controls.append({'name':name,'source':path.relative_to(ROOT).as_posix(),'sourceSha256':sha256(path),'object':row['object'],'objectSha256':row['objectSha256'],'wholeCWrongCallerGenuinelyLinked':True,'linkedBinary':binary.relative_to(ROOT).as_posix(),'linkedBinarySha256':sha256(binary),'byteComparisonRefusal':refusal,'memoryRejections':rejects,'positiveControls':positives,'cases':cases})
    report={'sourceCredit':0,'passed':True,'generator':'validate_sdk_trig_wrappers_20261031.py','generatorSha256':sha256(ROOT/'validate_sdk_trig_wrappers_20261031.py'),'controls':controls,'actualTopLevelReturns':returns,'actualOriginalMatrixHelperReturns':returns,'memoryRejections':sum(x['memoryRejections'] for x in controls),'positiveMemoryControls':sum(x['positiveControls'] for x in controls),'providedCalls':0,'instructionLimit':200}
    write_json(ROOT/'evidence/verification/sdk-trig-wrapper-controls-20261031.json',report)
    print({key:report[key] for key in ['passed','actualTopLevelReturns','memoryRejections','positiveMemoryControls']})


if __name__=='__main__':
    main()
