from project import ROOT,configuration,verify_inputs,write_json,sha256
import match_runtime as compiler
from link_runtime_unit import validate,measured_module
from match_main_overlap_copy_20261030 import main_references
from main_digit_rounding_native_20261031 import execute,cases,ENTRY
from seal_recovery_evidence_20261031 import code_closure

SOURCE='src/runtime/20261031_decimal_rounding/native_main_02022a54.c'
BINDINGS={f'native_fn_{a}':{'module':'main','processor':'arm9','kind':'function','mode':'arm','address':'0x'+a} for a in ['02022998','02022a04']}


def main():
    inputs=verify_inputs(configuration());metadata,original,config=measured_module('main');compiler.WORK=ROOT/'work/main-digit-rounding-source-20261031/compile'
    rows,_=compiler.compare(ROOT/SOURCE,'main',2,'off',False);assert len(rows)==1;row=rows[0];assert row['exactAfterDeclaredRelocation']
    directory=ROOT/'work/main-digit-rounding-source-20261031/linked';proof=validate(row,BINDINGS,directory=directory);assert proof['exactCallerBytes']
    rebuilt=bytearray(original);rebuilt[ENTRY-0x02000000:ENTRY-0x02000000+64]=(directory/'caller.bin').read_bytes()
    row.update(sourceLanguage='C',ordinaryFunctionCredit=1,originalObjectScaffolding=False,realMainLink=proof,exactAfterRealMwLink=True,sourceDependencies=[])
    row['relocations']=[{**r,'target':r['symbol'],'targetAddress':BINDINGS[r['symbol']]['address'],'targetMode':'arm','targetModule':'main','addend':r['explicitAddend']} for r in proof['originalRelocations']]
    row['boundaries']=dict(main_references(row,original,config),instructionBytes=64,literalPoolBytes=0,generatedLiteralOrPaddingBytes=0)
    results=[];pcs=set();maximum=0;nested=0
    for tag,case in enumerate(cases()):
        a=execute(original,case,tag);b=execute(bytes(rebuilt),case,tag);assert a==b;results.append({'case':list(case),'result':a});pcs.update(a['pcs']);maximum=max(maximum,a['state']['instructions']);nested+=2*a['state']['helperReturns']
    source=(ROOT/SOURCE).read_text(encoding='utf-8-sig');before='decision = native_fn_02022998(digits, count);\n    ((u8 *)digits)[4] = (u8)count;';assert before in source
    wrong=source.replace(before,'((u8 *)digits)[4] = (u8)count;\n    decision = native_fn_02022998(digits, count);');path=ROOT/'nonmatching/main-runtime/20261031/digit-rounding-wrong-store-order.c';path.write_text(wrong,encoding='utf-8')
    compiler.WORK=ROOT/'work/main-digit-rounding-control-20261031/compile';bad,_=compiler.compare(path,'main',2,'off',False);work=ROOT/'work/main-digit-rounding-control-20261031/linked'
    try:validate(bad[0],BINDINGS,directory=work)
    except ValueError as error:refusal=str(error)
    else:raise AssertionError('Wrong complete C matched')
    payload=(work/'caller.bin').read_bytes();assert len(payload)==64;mutant=bytearray(original);mutant[ENTRY-0x02000000:ENTRY-0x02000000+64]=payload;controls=[]
    for tag,digit in enumerate([4,5,6,255]):
        case=(4,2,[8,8,digit,1],0x7FFF);a=execute(original,case,tag);b=execute(bytes(mutant),case,tag,check=False);controls.append({'case':list(case),'actualReturns':2,'rejected':not b['modelPassed'],'positiveControl':b['modelPassed']})
    assert any(c['rejected'] for c in controls) and any(c['positiveControl'] for c in controls);assert verify_inputs(configuration())==inputs
    report={'schemaVersion':1,'romSha256':configuration()['romSha256'],'processor':'arm9','module':'main','matches':rows,'matchedFunctions':1,'matchedBytes':64,'nativeSymbolEntries':BINDINGS,'generatorSources':[{'path':p,'sha256':sha256(ROOT/p)} for p in code_closure(['match_main_digit_rounding_20261031.py'])],
        'oracle':{'pairs':len(results),'actualTopReturns':2*len(results),'actualNestedHelperReturns':nested,'functionResultProviders':0,'instructionLimit':10000,'maximumInstructions':maximum,'ownInstructionPcs':sum(ENTRY<=p<ENTRY+64 for p in pcs),'rows':results},
        'negativeControls':{'wholeCompiledCRealLinked':True,'source':path.relative_to(ROOT).as_posix(),'sourceSha256':sha256(path),'byteRefusal':refusal,'actualReturns':8,'cases':controls},'wholeModuleLinked':False,'sourceCreditAcceptedByThisScript':0,'inputsUnchanged':True,
        'limitations':['The caller has a void C interface; physical R0 effects are compared without assigning a result meaning','Both lower native routines receive the explicit original pointer/count arguments and execute unchanged','Synthetic byte arrays establish the stated truncation/rounding behavior without claiming original text/number object names','Buffers are aligned and bounded; malformed pointers and concurrent mutation remain unsupported','Only this64-byte caller is new source; lower helpers and full game execution receive no credit']}
    write_json(ROOT/'evidence/matches/main-digit-rounding-20261031.json',report);print({'bytes':64,'actualTopReturns':2*len(results),'actualNestedHelperReturns':nested,'maximumInstructions':maximum,'negativeReturns':8})


if __name__=='__main__':
    main()
