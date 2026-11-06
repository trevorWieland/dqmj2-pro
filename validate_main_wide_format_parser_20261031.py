import struct
from project import ROOT,write_json,sha256
import match_runtime as compiler
from link_runtime_unit import validate
from main_wide_format_parser_native_20261031 import ENTRY,DATA,STACK,STOP,REGS,execute
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC


def returning_control(main,text):
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    for address,size in [(0x02000000,0x400000),(DATA,4096),(STACK,0x8000),(STOP,4096)]:machine.mem_map(address,size)
    machine.mem_write(0x02000000,main)
    arena=bytearray(b'\xA5'*4096);encoded=(text+'\0').encode('utf-16le')
    arena[0x100:0x100+len(encoded)]=encoded;arena[0x40:0x44]=struct.pack('<I',DATA+0x800)
    machine.mem_write(DATA,bytes(arena));machine.mem_write(STACK,b'\x5A'*0x8000)
    for i,reg in enumerate(REGS):machine.reg_write(reg,(0x13579BDF*(i+1))&0xFFFFFFFF)
    for reg,value in zip(REGS[:3],[DATA+0x100,DATA+0x40,DATA+0x400]):machine.reg_write(reg,value)
    machine.reg_write(UC_ARM_REG_SP,STACK+0x6000);machine.reg_write(UC_ARM_REG_LR,STOP)
    saved=[machine.reg_read(reg) for reg in REGS[4:12]]
    machine.emu_start(ENTRY,STOP,count=10000)
    assert machine.reg_read(UC_ARM_REG_PC)==STOP and machine.reg_read(UC_ARM_REG_SP)==STACK+0x6000
    assert [machine.reg_read(reg) for reg in REGS[4:12]]==saved
    result=bytes(machine.mem_read(DATA,4096))
    assert result[:0x40]==bytes(arena[:0x40]) and result[0x44:0x400]==bytes(arena[0x44:0x400]) and result[0x410:]==bytes(arena[0x410:])
    return {'record':result[0x400:0x410].hex(),'argumentPointer':int.from_bytes(result[0x40:0x44],'little'),'returnOffset':machine.reg_read(UC_ARM_REG_R0)-(DATA+0x100)}


def main():
    original=(ROOT/'extract/arm9/arm9.bin').read_bytes();source=(ROOT/'src/runtime/20261031_wide_format_parser/native_main_0201f2c0.c').read_text()
    block='''        if (f.argument_options == long_double_argument) {
            f.argument_options = long_long_argument;
        }'''
    assert block in source
    wrong_length=source.replace(block,'''        if (f.argument_options == long_double_argument) {
            f.conversion_char = 0xFFFF;
            break;
        }''',1)
    variants=[('wrong-long-integer-kind',wrong_length,['%Ld','%Li','%Lu','%d','%llx','%Lf']),('wrong-byte-classification',source.replace('extern const unsigned short native_data_020d8f14','extern const unsigned char native_data_020d8f14'),['%123d','%.123d','%5x','%d','%Lf','%s'])]
    compiler.WORK=ROOT/'work/wide-parser-controls-20261031/compile';controls=[];returns=0
    directory=ROOT/'nonmatching/main-runtime/20261031/wide-format-parser'
    bindings={'native_data_020d8f14':{'processor':'arm9','module':'main','kind':'data','mode':'data','address':'0x020d8f14'}}
    for name,text,vectors in variants:
        path=directory/(name+'.c');path.write_text(text,encoding='utf-8');rows,_=compiler.compare(path,'main',3,'off',speed=True);assert len(rows)==1
        row=rows[0];work=ROOT/'work/wide-parser-controls-20261031'/name
        try:validate(row,bindings,directory=work)
        except ValueError as error:refusal=str(error)
        else:raise AssertionError('Wrong complete C parser matched')
        compiled=bytearray(original);payload=(work/'caller.bin').read_bytes();compiled[0x1F2C0:0x1F2C0+len(payload)]=payload
        rejects=0;positives=0;cases=[]
        for value in vectors:
            native=returning_control(original,value);wrong=returning_control(bytes(compiled),value)
            bad=native!=wrong;rejects+=bad;positives+=not bad;returns+=2
            cases.append({'format':value,'actualReturns':2,'rejected':bad,'positiveControl':not bad,'native':native,'wrong':wrong})
        assert rejects and positives
        controls.append({'name':name,'source':path.relative_to(ROOT).as_posix(),'sourceSha256':sha256(path),'object':row['object'],'objectSha256':row['objectSha256'],'wholeCompiledCParserRealLinked':True,'byteRefusal':refusal,'rejections':rejects,'positiveControls':positives,'cases':cases})
    report={'sourceCredit':0,'passed':True,'generatorSha256':sha256(ROOT/'validate_main_wide_format_parser_20261031.py'),'controls':controls,'actualTopLevelReturns':returns,'providedCalls':0,'rejections':sum(x['rejections'] for x in controls),'positiveControls':sum(x['positiveControls'] for x in controls),'instructionLimit':10000}
    write_json(ROOT/'evidence/verification/main-wide-format-parser-controls-20261031.json',report)
    print({key:report[key] for key in ['passed','actualTopLevelReturns','rejections','positiveControls']})


if __name__=='__main__':
    main()
