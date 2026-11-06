from project import ROOT,configuration,verify_inputs,write_json,sha256
import match_runtime as compiler
from link_runtime_unit import validate,measured_module
from match_main_overlap_copy_20261030 import main_references
from main_range_map_native_20261031 import execute,cases,ENTRY
from seal_recovery_evidence_20261031 import code_closure

SOURCE='src/runtime/20261031_range_map/native_main_02036994.c'


def main():
    inputs=verify_inputs(configuration());metadata,original,config=measured_module('main');compiler.WORK=ROOT/'work/main-range-map-source-20261031/compile'
    rows,_=compiler.compare(ROOT/SOURCE,'main',3,'off',True);assert len(rows)==1;row=rows[0];assert row['exactAfterDeclaredRelocation']
    directory=ROOT/'work/main-range-map-source-20261031/linked';proof=validate(row,{},directory=directory);assert proof['exactCallerBytes']
    rebuilt=bytearray(original);rebuilt[ENTRY-0x02000000:ENTRY-0x02000000+76]=(directory/'caller.bin').read_bytes()
    row.update(sourceLanguage='C',ordinaryFunctionCredit=1,originalObjectScaffolding=False,realMainLink=proof,exactAfterRealMwLink=True,sourceDependencies=[])
    row['boundaries']=dict(main_references(row,original,config),instructionBytes=76,literalPoolBytes=0,generatedLiteralOrPaddingBytes=0)
    results=[];observed=set();maximum=0
    for tag,case in enumerate(cases()):
        a=execute(original,case,tag);b=execute(bytes(rebuilt),case,tag);assert a==b;results.append({'case':case,'result':a});observed.update(a['pcs']);maximum=max(maximum,a['state']['instructions'])
    source=(ROOT/SOURCE).read_text(encoding='utf-8-sig');controls=[]
    for name,text in [('wrong-fallback-offset',source.replace('return (u32)base->fallback;','return (u32)base->fallback + 1;')),('wrong-entry-stride',source.replace('(key - first) * 3','(key - first) * 2'))]:
        path=ROOT/f'nonmatching/main-runtime/20261031/range-map-{name}.c';path.write_text(text,encoding='utf-8');compiler.WORK=ROOT/f'work/main-range-map-controls-20261031/{name}/compile';bad,_=compiler.compare(path,'main',3,'off',True);work=compiler.WORK.parent/'linked'
        try:validate(bad[0],{},directory=work)
        except ValueError as error:refusal=str(error)
        else:raise AssertionError('Wrong complete C matched')
        payload=(work/'caller.bin').read_bytes();assert len(payload)<=76;mutant=bytearray(original);mutant[ENTRY-0x02000000:ENTRY-0x02000000+len(payload)]=payload;vectors=[]
        for tag,case in enumerate([([],0),([(10,20)],10),([(10,20)],11),([(10,20)],20),([(10,20),(0,65535)],21),([(0,65535)],65535)]):
            a=execute(original,case,tag);b=execute(bytes(mutant),case,tag,check=False);vectors.append({'case':case,'actualReturns':2,'rejected':not b['modelPassed'],'positiveControl':b['modelPassed']})
        assert any(c['rejected'] for c in vectors) and any(c['positiveControl'] for c in vectors)
        controls.append({'name':name,'source':path.relative_to(ROOT).as_posix(),'sourceSha256':sha256(path),'wholeCompiledCRealLinked':True,'byteRefusal':refusal,'cases':vectors})
    assert verify_inputs(configuration())==inputs
    report={'schemaVersion':1,'romSha256':configuration()['romSha256'],'processor':'arm9','module':'main','matches':rows,'matchedFunctions':1,'matchedBytes':76,'nativeSymbolEntries':{},'generatorSources':[{'path':p,'sha256':sha256(ROOT/p)} for p in code_closure(['match_main_range_map_20261031.py'])],
        'oracle':{'pairs':len(results),'actualTopReturns':2*len(results),'functionResultProviders':0,'instructionLimit':1000,'maximumInstructions':maximum,'ownInstructionPcs':len(observed),'rows':results},'negativeControls':{'actualReturns':24,'controls':controls},'inputsUnchanged':True,'wholeModuleLinked':False,'sourceCreditAcceptedByThisScript':0,
        'limitations':['Synthetic allocated nodes support inclusive16-bit ranges, first-match precedence and three-byte entries; no historical names or payload meaning are inferred','Only headers are read; returned payload addresses are not dereferenced or decoded','Flexible array tails have allocated backing for the tested ranges; cycles, malformed pointers and concurrent mutation are unsupported','Raw u32 pointer results are qualified to the measured32-bit target ABI','This76-byte candidate awaits registry/module gates and establishes no complete game or Android execution']}
    write_json(ROOT/'evidence/matches/main-range-map-20261031.json',report);print({'bytes':76,'actualTopReturns':2*len(results),'ownInstructionPcs':len(observed),'maximumInstructions':maximum,'negativeReturns':24})


if __name__=='__main__':
    main()
