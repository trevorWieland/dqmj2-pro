from project import ROOT,configuration,verify_inputs,write_json,sha256
import match_runtime as compiler
from link_runtime_unit import validate,measured_module
from match_main_overlap_copy_20261030 import main_references
from main_range_keys_native_20261031 import execute,leaf_cases,chain_cases,LEAF,CHAIN
from seal_recovery_evidence_20261031 import code_closure

HEADER='src/runtime/20261031_range_keys/native_range_types.h'
SOURCES=[(LEAF,200,'src/runtime/20261031_range_keys/native_main_02036830.c'),(CHAIN,72,'src/runtime/20261031_range_keys/native_main_0203694c.c')]
BINDINGS={'native_fn_02036830':{'module':'main','processor':'arm9','kind':'function','mode':'arm','address':hex(LEAF)}}


def main():
    inputs=verify_inputs(configuration());metadata,original,config=measured_module('main');rebuilt=bytearray(original);matches=[]
    for entry,size,source in SOURCES:
        compiler.WORK=ROOT/f'work/main-range-keys-source-20261031/{entry:08x}/compile';rows,_=compiler.compare(ROOT/source,'main',3,'off',True);assert len(rows)==1;row=rows[0];assert row['exactAfterDeclaredRelocation']
        directory=compiler.WORK.parent/'linked';proof=validate(row,BINDINGS,directory=directory);assert proof['exactCallerBytes'];rebuilt[entry-0x02000000:entry-0x02000000+size]=(directory/'caller.bin').read_bytes()
        row.update(sourceLanguage='C',ordinaryFunctionCredit=1,originalObjectScaffolding=False,realMainLink=proof,exactAfterRealMwLink=True,sourceDependencies=[{'path':HEADER,'sha256':sha256(ROOT/HEADER)}]);row['boundaries']=dict(main_references(row,original,config),instructionBytes=size-4,literalPoolBytes=4,generatedLiteralOrPaddingBytes=0);matches.append(row)
    results=[];observed=set();maximum=0;nested=0
    for entry,cases in [(LEAF,leaf_cases),(CHAIN,chain_cases)]:
        for tag,case in enumerate(cases()):
            a=execute(original,entry,case,tag);b=execute(bytes(rebuilt),entry,case,tag);assert a==b;results.append({'entry':hex(entry),'case':case,'result':a});observed.update(a['pcs']);maximum=max(maximum,a['state']['instructions']);nested+=a['state']['nestedReturns']*2
    controls=[]
    for entry,size,source in SOURCES:
        text=(ROOT/source).read_text(encoding='utf-8-sig')
        wrong=text.replace('u32 result = 65535;','u32 result = 65534;') if entry==LEAF else text.replace('return 65535;', 'return 65534;')
        assert wrong!=text;path=ROOT/f'nonmatching/main-runtime/20261031/range-keys/control_{entry:08x}.c';path.parent.mkdir(parents=True,exist_ok=True);wrong=wrong.replace('#include \"native_range_types.h\"','#include \"../../../../src/runtime/20261031_range_keys/native_range_types.h\"');path.write_text(wrong,encoding='utf-8');compiler.WORK=ROOT/f'work/main-range-keys-controls-20261031/{entry:08x}/compile';bad,_=compiler.compare(path,'main',3,'off',True);directory=compiler.WORK.parent/'linked'
        try:validate(bad[0],BINDINGS,directory=directory)
        except ValueError as error:refusal=str(error)
        else:raise AssertionError('Wrong whole C matched')
        payload=(directory/'caller.bin').read_bytes();assert len(payload)<=size;mutant=bytearray(rebuilt);mutant[entry-0x02000000:entry-0x02000000+len(payload)]=payload;vectors=[]
        cases=[([(3,0,65535,[0])],5),([(65535,0,65535,[0])],0),([(0,10,20,[100])],10),([(0,10,20,[100])],11)]
        if entry==CHAIN:cases=[([(0,10,20,[100])],9),([(0,10,9,[100])],10),([(0,10,20,[100])],10),([(0,10,20,[100])],11)]
        for tag,case in enumerate(cases):
            a=execute(original,entry,case,tag);b=execute(bytes(mutant),entry,case,tag,check=False);vectors.append({'case':case,'actualReturns':2,'rejected':not b['modelPassed'],'positiveControl':b['modelPassed']})
        assert any(v['rejected'] for v in vectors) and any(v['positiveControl'] for v in vectors)
        controls.append({'source':path.relative_to(ROOT).as_posix(),'sourceSha256':sha256(path),'wholeCompiledCRealLinked':True,'refusal':refusal,'cases':vectors})
    assert verify_inputs(configuration())==inputs
    report={'schemaVersion':1,'romSha256':configuration()['romSha256'],'processor':'arm9','module':'main','matches':matches,'matchedFunctions':2,'matchedBytes':272,'nativeSymbolEntries':{},'generatorSources':[{'path':p,'sha256':sha256(ROOT/p)} for p in code_closure(['match_main_range_keys_20261031.py'])],
        'oracle':{'pairs':len(results),'actualTopReturns':2*len(results),'separateNestedLookupReturns':nested,'functionResultProviders':0,'instructionLimit':1000,'maximumInstructions':maximum,'ownInstructionPcs':len(observed),'rows':results},'negativeControls':{'actualReturns':16,'controls':controls},'inputsUnchanged':True,'wholeModuleLinked':False,'sourceCreditAcceptedByThisScript':0,
        'limitations':['Formats0/1/2 and unknown16-bit formats are raw table protocols; no text or gameplay semantics are inferred','Direct-index keys are within allocated backing; sparse nodes have sorted pairs and complete allocated headers/payloads','Binary search uses byte pointers within the complete allocated node, including header backing for the count-zero high pointer; no before-array typed pointer is formed','First matching chain node wins; sparse duplicate selection follows binary midpoint order and is not a first-duplicate guarantee','Invalid pointers, cycles, inconsistent payload sizes and unbounded chains are unsupported','The272 bytes include eight literal bytes and add no global-data or dependency-source credit']}
    write_json(ROOT/'evidence/matches/main-range-keys-20261031.json',report);print({'bytes':272,'actualTopReturns':2*len(results),'nestedLookupReturns':nested,'ownInstructionPcs':len(observed),'maximumInstructions':maximum,'negativeReturns':16})


if __name__=='__main__':main()
