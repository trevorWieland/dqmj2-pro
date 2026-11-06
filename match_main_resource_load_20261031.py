from project import ROOT,configuration,verify_inputs,write_json,sha256
import match_runtime as compiler
from link_runtime_unit import validate,measured_module
from match_main_overlap_copy_20261030 import main_references
from main_resource_load_native_20261031 import execute,cases,ENTRY,THUNK
from seal_recovery_evidence_20261031 import code_closure

SOURCE='src/runtime/20261031_resource_load/native_main_0203cb8c.c'
BINDINGS={f'native_fn_{address}':{'module':'main','processor':'arm9','kind':'function','mode':'arm','address':'0x'+address} for address in ['0202a8e0','0202a250','0202a37c','0202a818','0202a498']}


def main():
    inputs=verify_inputs(configuration());metadata,original,config=measured_module('main');compiler.WORK=ROOT/'work/main-resource-load-source-20261031/compile'
    rows,_=compiler.compare(ROOT/SOURCE,'main',2,'off',False);assert len(rows)==1;row=rows[0];assert row['exactAfterDeclaredRelocation']
    directory=ROOT/'work/main-resource-load-source-20261031/linked';proof=validate(row,BINDINGS,directory=directory);assert proof['exactCallerBytes']
    rebuilt=bytearray(original);rebuilt[ENTRY-0x02000000:ENTRY-0x02000000+160]=(directory/'caller.bin').read_bytes()
    row.update(sourceLanguage='C',ordinaryFunctionCredit=1,originalObjectScaffolding=False,realMainLink=proof,exactAfterRealMwLink=True,sourceDependencies=[])
    row['relocations']=[{**r,'target':r['symbol'],'targetAddress':BINDINGS[r['symbol']]['address'],'targetMode':'arm','targetModule':'main','addend':r['explicitAddend']} for r in proof['originalRelocations']]
    row['boundaries']=dict(main_references(row,original,config),instructionBytes=160,literalPoolBytes=0,generatedLiteralOrPaddingBytes=0)
    results=[];observed=set();maximum=0;provided=0;thunk_returns=0
    for tag,case in enumerate(cases()):
        a=execute(original,case,tag);b=execute(bytes(rebuilt),case,tag);assert a==b;results.append({'case':list(case),'result':a});observed.update(a['pcs']);maximum=max(maximum,a['state']['instructions']);provided+=2*a['state']['providerCalls'];thunk_returns+=2*a['state']['thunkToBodyEntries']
    source=(ROOT/SOURCE).read_text(encoding='utf-8-sig');controls=[]
    for name,text in [('wrong-read-polarity',source.replace('native_fn_0202a818(path, buffer, bytes, 0) == 0','native_fn_0202a818(path, buffer, bytes, 0) != 0')),('wrong-cleanup-heap',source.replace('native_fn_0202a498((s32)heap, buffer)','native_fn_0202a498((s32)selector, buffer)'))]:
        path=ROOT/f'nonmatching/main-runtime/20261031/resource-load-{name}.c';path.write_text(text,encoding='utf-8');compiler.WORK=ROOT/f'work/main-resource-load-controls-20261031/{name}/compile';bad,_=compiler.compare(path,'main',2,'off',False);work=compiler.WORK.parent/'linked'
        try:validate(bad[0],BINDINGS,directory=work)
        except ValueError as error:refusal=str(error)
        else:raise AssertionError('Wrong whole C matched')
        payload=(work/'caller.bin').read_bytes();assert len(payload)==160;mutant=bytearray(original);mutant[ENTRY-0x02000000:ENTRY-0x02000000+160]=payload;vectors=[]
        for tag,case in enumerate([(0,1,0,False,0,False),(7,1,1,True,0,False),(7,0xFFFFFFFF,0,True,0,False),(7,1,0,True,1,False),(1,1,0,False,0,True),(1,1,0,True,1,True)]):
            a=execute(original,case,tag);b=execute(bytes(mutant),case,tag,check=False);vectors.append({'case':list(case),'actualReturns':2,'rejected':not b['modelPassed'],'positiveControl':b['modelPassed']})
        assert any(v['rejected'] for v in vectors) and any(v['positiveControl'] for v in vectors)
        controls.append({'name':name,'source':path.relative_to(ROOT).as_posix(),'sourceSha256':sha256(path),'wholeCompiledCRealLinked':True,'byteRefusal':refusal,'cases':vectors})
    assert verify_inputs(configuration())==inputs
    report={'schemaVersion':1,'romSha256':configuration()['romSha256'],'processor':'arm9','module':'main','matches':rows,'matchedFunctions':1,'matchedBytes':160,'nativeSymbolEntries':BINDINGS,'generatorSources':[{'path':p,'sha256':sha256(ROOT/p)} for p in code_closure(['match_main_resource_load_20261031.py'])],
        'oracle':{'pairs':len(results),'actualTopReturns':2*len(results),'actualThunkToBodyReturns':thunk_returns,'providedCalls':provided,'instructionLimit':1000,'maximumInstructions':maximum,'ownInstructionPcs':sum(ENTRY<=p<ENTRY+160 for p in observed),'rows':results},'negativeControls':{'actualReturns':24,'controls':controls},'inputsUnchanged':True,'wholeModuleLinked':False,'sourceCreditAcceptedByThisScript':0,
        'limitations':['Five lower file/heap/allocator/read/cleanup boundaries are supplied; they receive no original-native-helper or source credit','The selected16-byte thunk executes unchanged and is not counted again as source','Both selector branches call the same allocator with raw alignment4 orFFFFFFFC; no allocator-side semantics is inferred','Huge lengths test unsigned rounding/protocol only; no real huge allocation or complete file transfer is modeled','Read provider writes a bounded prefix; no filesystem validity, bank selection, loader success meaning or game/device execution is established','Raw32-bit path/buffer/heap/return words follow the measured target ABI; malformed pointer dereferences and asynchronous operations are unsupported']}
    write_json(ROOT/'evidence/matches/main-resource-load-20261031.json',report);print({'bytes':160,'actualTopReturns':2*len(results),'thunkToBodyReturns':thunk_returns,'providedCalls':provided,'ownInstructionPcs':sum(ENTRY<=p<ENTRY+160 for p in observed),'negativeReturns':24})


if __name__=='__main__':
    main()
