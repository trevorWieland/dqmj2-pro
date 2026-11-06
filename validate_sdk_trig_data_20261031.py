import io
import os
import subprocess
import struct
from project import ROOT,read_json,write_json,sha256,verify_inputs,configuration
import match_sdk_trig_data_20261031 as matcher
from derive_sdk_trig_20261031 import derive,source_text
from sdk_trig_native_oracle_20261031 import execute
from elftools.elf.elffile import ELFFile
from elf_units import split_symbol


def build_wrong(pairs,name):
    source=ROOT/f'nonmatching/math/20261031/{name}.c'
    source.parent.mkdir(parents=True,exist_ok=True);source.write_text(source_text(pairs),encoding='utf-8')
    directory=ROOT/f'work/sdk-trig-controls-20261031/{name}'
    directory.mkdir(parents=True,exist_ok=True)
    env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'))
    obj=directory/'wrong.o'
    subprocess.run([str(matcher.compiler.COMPILER),*matcher.compiler.FLAGS,'-c',str(source),'-o',str(obj)],cwd=ROOT,env=env,capture_output=True,check=True,timeout=30)
    with obj.open('rb') as stream:
        elf=ELFFile(stream)
        split=directory/'sincos-split.o';split_symbol(elf,matcher.NAME,split,target_section='.rodata')
    lcf=directory/'wrong.lcf';lcf.write_bytes((matcher.WORK/'sincos.lcf').read_bytes())
    linked=directory/'wrong.elf'
    subprocess.run([str(matcher.LINKER),'-nostdlib','-nodeadstrip','-main',matcher.NAME,str(lcf),str(split),'-o',str(linked)],cwd=directory,env=env,capture_output=True,check=True,timeout=30)
    actual=(directory/'sincos.bin').read_bytes()
    expected=struct.pack('<8192h',*(value for pair in pairs for value in pair))
    assert len(actual)==16384 and actual==expected
    return actual,{'source':source.relative_to(ROOT).as_posix(),'sourceSha256':sha256(source),'object':obj.relative_to(ROOT).as_posix(),'objectSha256':sha256(obj),'linkedElf':linked.relative_to(ROOT).as_posix(),'linkedElfSha256':sha256(linked),'wholeTypedCDataObject':True}


def main():
    before=verify_inputs(configuration())
    pairs,_=derive()
    arm=(ROOT/'extract/arm9/arm9.bin').read_bytes()
    original=arm[0xD3FE0:0xD7FE0]
    altered=list(pairs);altered[1]=(pairs[1][0]+1,pairs[1][1])
    variants=[('wrong-one-pair',altered),('wrong-column-order',[(b,a) for a,b in pairs])]
    rows=[];returns=0
    for name,wrong in variants:
        payload,identity=build_wrong(wrong,name)
        assert payload!=original
        rejected=0;positive=0;cases=[]
        for phase in [0,1,512,1024,2048,2560,3072,4095]:
            raw=phase*360;axis=phase%3
            native=execute(arm,original,raw,axis,pairs)
            mutant=execute(arm,payload,raw,axis,wrong)
            differs=native[2]!=mutant[2]
            expected=pairs[phase]!=wrong[phase]
            assert differs==expected
            rejected+=differs;positive+=not differs;returns+=2
            cases.append({'phase':phase,'axis':axis,'actualReturns':2,'memoryRejected':differs,'positiveControl':not differs})
        assert rejected and positive
        rows.append({'name':name,**identity,'comparisonRejectsDifferentTypedData':True,'memoryRejections':rejected,'positiveControls':positive,'cases':cases})
    assert verify_inputs(configuration())==before
    report={'passed':True,'sourceCredit':0,'generator':'validate_sdk_trig_data_20261031.py','generatorSha256':sha256(ROOT/'validate_sdk_trig_data_20261031.py'),
        'compiledAndRealLinkedWholeCMutants':len(rows),'controls':rows,'actualTopLevelReturns':returns,'actualNativeHelperReturns':returns,
        'memoryRejections':sum(row['memoryRejections'] for row in rows),'positiveMemoryControls':sum(row['positiveControls'] for row in rows),
        'originalInputsUnchanged':True,'limitations':['Mutated data reuses original native consumer instructions; no ordinary logic/source-function credit']}
    write_json(ROOT/'evidence/verification/sdk-trig-data-controls-20261031.json',report)
    print({key:report[key] for key in ['passed','compiledAndRealLinkedWholeCMutants','actualTopLevelReturns','memoryRejections','positiveMemoryControls']})


if __name__=='__main__':
    main()
