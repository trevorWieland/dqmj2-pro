import io
import math
import os
import re
import struct
import subprocess
from project import ROOT,configuration,verify_inputs,sha256,write_json,read_json
import match_runtime as compiler
from elftools.elf.elffile import ELFFile
from elf_units import split_symbol
from link_runtime_unit import LINKER,LINKER_HASH
from derive_sdk_trig_20261031 import derive,source_text
from seal_recovery_evidence_20261031 import code_closure

SOURCE='generated/math/20261031_sincos_data.c'
NAME='native_math_sincos_020d3fe0'
ADDRESS=0x020D3FE0
SIZE=16384
WORK=ROOT/'work/sdk-trig-source-20261031'


def compile_data():
    import sys,unicorn,elftools
    assert sys.version_info[:3]==(3,13,5) and unicorn.__version__=='2.1.4' and elftools.__version__=='0.33'
    inputs=verify_inputs(configuration())
    pairs,derivation=derive()
    expected=struct.pack('<8192h',*(value for pair in pairs for value in pair))
    source=ROOT/SOURCE
    assert source.read_text(encoding='utf-8')==source_text(pairs)
    floating=[(round(4096*math.sin(2*math.pi*i/4096)),round(4096*math.cos(2*math.pi*i/4096))) for i in range(4096)]
    assert pairs==floating
    arm=ROOT/'extract/arm9/arm9.bin'
    assert sha256(arm)=='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
    original=arm.read_bytes()[ADDRESS-0x02000000:ADDRESS-0x02000000+SIZE]
    assert original==expected
    symbols=(ROOT/'config/arm9/symbols.txt').read_text()
    for address in [ADDRESS,ADDRESS+SIZE]:
        assert re.search(r'^data_'+f'{address:08x}'+r' kind:data\(any\) addr:0x'+f'{address:08x}'+r'$',symbols,re.M)
    layout=(ROOT/'config/arm9/delinks.txt').read_text()
    spans=[(int(a,0),int(b,0)) for a,b in re.findall(r'^\s*\.rodata\s+start:(0x[0-9a-f]+)\s+end:(0x[0-9a-f]+)',layout,re.M)]
    assert any(a<=ADDRESS and ADDRESS+SIZE<=b for a,b in spans)
    functions=[(int(address,0),int(size,0)) for size,address in re.findall(r'kind:function\((?:arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)',symbols)]
    assert not any(start<ADDRESS+SIZE and ADDRESS<start+size for start,size in functions)
    WORK.mkdir(parents=True,exist_ok=True)
    executable=compiler.COMPILER
    compiler_hash=sha256(executable)
    assert compiler_hash==compiler.COMPILER_PINS[executable.relative_to(ROOT).as_posix()]
    assert sha256(LINKER)==LINKER_HASH
    env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'))
    object_path=WORK/'sincos.o'
    command=[str(executable),*compiler.FLAGS,'-c',str(source),'-o',str(object_path)]
    subprocess.run(command,cwd=ROOT,env=env,capture_output=True,check=True,timeout=30)
    object_hash=sha256(object_path)
    stable=WORK/(object_hash+'.o');stable.write_bytes(object_path.read_bytes())
    with object_path.open('rb') as stream:
        elf=ELFFile(stream)
        symbol=next(row for row in elf.get_section_by_name('.symtab').iter_symbols() if row.name==NAME)
        section=elf.get_section(symbol['st_shndx'])
        assert symbol['st_info']['type']=='STT_OBJECT' and symbol['st_size']==SIZE and symbol['st_value']==0
        assert section['sh_type']=='SHT_PROGBITS' and not section['sh_flags']&4
        assert section.data()[:SIZE]==expected
        assert not any(row['sh_type'] in ('SHT_REL','SHT_RELA') and row['sh_info']==symbol['st_shndx'] and row.num_relocations() for row in elf.iter_sections())
        section_index=symbol['st_shndx'];padding=section['sh_size']-SIZE
        split=WORK/'sincos-split.o'
        split_symbol(elf,NAME,split,section_padding=padding,target_section='.rodata')
    lcf=WORK/'sincos.lcf'
    lcf.write_text('MEMORY {\nDATA: ORIGIN = 0x020d3fe0 > sincos.bin\n}\nSECTIONS {\n.rodata: { sincos-split.o(.rodata) } > DATA\n}\n',encoding='utf-8')
    linked=WORK/'sincos.elf'
    link_command=[str(LINKER),'-nostdlib','-nodeadstrip','-main',NAME,str(lcf),str(split),'-o',str(linked)]
    subprocess.run(link_command,cwd=WORK,env=env,capture_output=True,check=True,timeout=30)
    with linked.open('rb') as stream:
        elf=ELFFile(stream);symbol=next(row for row in elf.get_section_by_name('.symtab').iter_symbols() if row.name==NAME)
        assert symbol['st_info']['type']=='STT_OBJECT' and symbol['st_value']==ADDRESS and symbol['st_size']==SIZE
    payload=(WORK/'sincos.bin').read_bytes()
    assert payload==expected
    binary=WORK/'sincos-linked.bin';binary.write_bytes(payload)
    row={'name':NAME,'symbol':NAME,'module':'main','processor':'arm9','kind':'initialized-data','sourceLanguage':'C',
        'address':hex(ADDRESS),'size':SIZE,'bytes':SIZE,'initializedBytes':SIZE,'compiledBytes':SIZE,
        'sourceSymbolType':'STT_OBJECT','section':'.rodata','targetSection':'.rodata','sectionIndex':section_index,'sectionOffset':0,
        'sectionPaddingBytes':padding,'source':SOURCE,'sourceSha256':sha256(source),'object':stable.relative_to(ROOT).as_posix(),
        'objectSha256':object_hash,'compiler':executable.relative_to(ROOT).as_posix(),'compilerSha256':compiler_hash,
        'flags':compiler.FLAGS,'compilerFlags':compiler.FLAGS,'nativeAlias':'data_020d3fe0','exactBytes':True,
        'exactAfterRealMwLink':True,'linkedDataBinary':binary.relative_to(ROOT).as_posix(),'linkedDataBinarySha256':sha256(binary),
        'linkedElf':linked.relative_to(ROOT).as_posix(),'linkedElfSha256':sha256(linked),'lcf':lcf.relative_to(ROOT).as_posix(),
        'lcfSha256':sha256(lcf),'linkerSha256':LINKER_HASH,'relocations':[],'ordinaryFunctionCredit':0,
        'targetSha256':compiler.sha(original),'outputSha256':compiler.sha(expected),'rawSha256':compiler.sha(expected),
        'exactAfterDeclaredRelocation':True,'splitObject':split.relative_to(ROOT).as_posix(),'splitObjectSha256':sha256(split),
        'targetSectionEvidence':{'path':'config/arm9/delinks.txt','sha256':sha256(ROOT/'config/arm9/delinks.txt'),'section':'.rodata'}}
    assert verify_inputs(configuration())==inputs
    return row,derivation,inputs,arm


def main():
    row,derivation,inputs,arm=compile_data()
    from sdk_trig_native_oracle_20261031 import main as native_consumers
    from validate_sdk_trig_data_20261031 import main as negative_controls
    native_consumers()
    negative_controls()
    oracle=read_json(ROOT/'evidence/verification/sdk-trig-native-consumers-20261031.json')
    controls=read_json(ROOT/'evidence/verification/sdk-trig-data-controls-20261031.json')
    assert oracle['distinctPairIndices']==4096 and oracle['actualTopLevelReturns']==8258 and controls['passed']
    assert verify_inputs(configuration())==inputs
    report={'schemaVersion':1,'romSha256':configuration()['romSha256'],'arm9Sha256':sha256(arm),
        'dataMatches':[row],'dataAliases':{'data_020d3fe0':hex(ADDRESS)},'nativeSymbols':{},'initializedDataBytes':SIZE,
        'ordinaryCCodeBytes':0,'generatedFromIndependentMathematics':True,'derivation':derivation,
        'floatAndDecimalPairsAgree':4096,'nativeAndCompiledSigned16ElementsCompared':8192,
        'sourceDataBytesFromNativeInput':0,'oracle':oracle,'negativeControls':controls,'inputsUnchanged':True,'sourceCreditAcceptedByThisScript':0,
        'wholeModuleLinked':False,'generatorSources':[{'path':p,'sha256':sha256(ROOT/p)} for p in code_closure(['match_sdk_trig_data_20261031.py'])],
        'limitations':['Quantized data is reconstructed; no consumer function, executable logic, original variable name or complete game is credited','Full-module adoption and source-ledger registration remain pending; the candidate contributes no accepted credit']}
    write_json(ROOT/'evidence/data/sdk-trig-table-20261031.json',report)
    print({'dataObjects':1,'independentlyGeneratedBytes':SIZE,'sourceAndMwldBytesExact':True,'acceptedSourceCredit':0})


if __name__=='__main__':
    main()
