from project import ROOT,configuration,verify_inputs,write_json,sha256
import match_runtime as compiler
from link_runtime_unit import validate,measured_module
from match_main_overlap_copy_20261030 import main_references
from main_record_init_native_20261031 import execute,cases,ENTRY
from seal_recovery_evidence_20261031 import code_closure

SOURCE='src/runtime/20261031_record_init/native_main_020343fc.c'
BINDINGS={'native_data_020dd5f8':{'module':'main','processor':'arm9','kind':'data','mode':'data','address':'0x020dd5f8'}}


def main():
    inputs=verify_inputs(configuration());metadata,original,config=measured_module('main');compiler.WORK=ROOT/'work/main-record-init-source-20261031/compile'
    rows,_=compiler.compare(ROOT/SOURCE,'main',2,'off',False);assert len(rows)==1;row=rows[0];assert row['exactAfterDeclaredRelocation']
    directory=ROOT/'work/main-record-init-source-20261031/linked';proof=validate(row,BINDINGS,directory=directory);assert proof['exactCallerBytes']
    rebuilt=bytearray(original);rebuilt[ENTRY-0x02000000:ENTRY-0x02000000+76]=(directory/'caller.bin').read_bytes()
    row.update(sourceLanguage='C',ordinaryFunctionCredit=1,originalObjectScaffolding=False,realMainLink=proof,exactAfterRealMwLink=True,sourceDependencies=[])
    row['relocations']=[{**r,'target':r['symbol'],'targetAddress':BINDINGS[r['symbol']]['address'],'targetMode':'data','targetModule':'main','addend':r['explicitAddend']} for r in proof['originalRelocations']]
    row['boundaries']=dict(main_references(row,original,config),instructionBytes=72,literalPoolBytes=4,generatedLiteralOrPaddingBytes=4)
    results=[];observed=set();maximum=0;counts=set()
    for tag,case in enumerate(cases()):
        a=execute(original,case,tag);b=execute(bytes(rebuilt),case,tag);assert a==b;results.append(a);observed.update(a['pcs']);maximum=max(maximum,a['state']['instructions']);counts.add(a['actualCount'])
    source=(ROOT/SOURCE).read_text(encoding='utf-8-sig');controls=[]
    for name,text in [('wrong-byte-global',source.replace('extern u32 native_data_020dd5f8;','extern u8 native_data_020dd5f8;')),('wrong-fill-base',source.replace('index | 0x100','index | 0x200'))]:
        path=ROOT/f'nonmatching/main-runtime/20261031/record-init-{name}.c';path.write_text(text,encoding='utf-8');compiler.WORK=ROOT/f'work/main-record-init-controls-20261031/{name}/compile';bad,_=compiler.compare(path,'main',2,'off',False);work=compiler.WORK.parent/'linked'
        try:validate(bad[0],BINDINGS,directory=work)
        except ValueError as error:refusal=str(error)
        else:raise AssertionError('Wrong full C matched')
        payload=(work/'caller.bin').read_bytes();assert len(payload)==76;mutant=bytearray(original);mutant[ENTRY-0x02000000:ENTRY-0x02000000+76]=payload;vectors=[]
        for tag,case in enumerate([(0,0,0),(1,0,1),(255,0,0),(5,2,1),(128,1,0),(9,3,1)]):
            a=execute(original,case,tag);b=execute(bytes(mutant),case,tag,check=False);vectors.append({'case':list(case),'actualReturns':2,'rejected':not b['modelPassed'],'positiveControl':b['modelPassed']})
        controls.append({'name':name,'source':path.relative_to(ROOT).as_posix(),'sourceSha256':sha256(path),'wholeCompiledCRealLinked':True,'byteRefusal':refusal,'cases':vectors})
        assert any(v['rejected'] for v in vectors)
    assert counts==set(range(256)) and verify_inputs(configuration())==inputs
    report={'schemaVersion':1,'romSha256':configuration()['romSha256'],'processor':'arm9','module':'main','matches':rows,'matchedFunctions':1,'matchedBytes':76,'nativeSymbolEntries':BINDINGS,'generatorSources':[{'path':p,'sha256':sha256(ROOT/p)} for p in code_closure(['match_main_record_init_20261031.py'])],
        'oracle':{'pairs':len(results),'actualTopReturns':2*len(results),'functionResultProviders':0,'instructionLimit':10000,'maximumInstructions':maximum,'ownInstructionPcs':len(observed),'distinctByteCounts':len(counts),'sourceAliasLayouts':5,'rows':results},'negativeControls':{'actualReturns':24,'controls':controls},'inputsUnchanged':True,'wholeModuleLinked':False,'sourceCreditAcceptedByThisScript':0,
        'limitations':['Only the76-byte caller is new source; the global word is a measured value without data-source credit','Buffers are synthetic, aligned and bounded; aliases exercise stores preceding source-byte loads','All256 byte counts are tested, without asserting historical record or scene meanings','Malformed pointers, concurrency, original global ownership and complete game/device execution remain unsupported','Per-unit O2/off/space profile is demonstrated; width and loop-shape corrections are not generalized to unrelated functions']}
    write_json(ROOT/'evidence/matches/main-record-init-20261031.json',report);print({'bytes':76,'actualTopReturns':2*len(results),'ownInstructionPcs':len(observed),'maximumInstructions':maximum,'negativeReturns':24})


if __name__=='__main__':
    main()
