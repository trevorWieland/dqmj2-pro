from project import ROOT,configuration,verify_inputs,write_json,sha256
import match_runtime as compiler
from link_runtime_unit import validate,measured_module
from match_main_overlap_copy_20261030 import main_references
from main_decimal_pad_native_20261031 import execute,cases,ENTRY
from seal_recovery_evidence_20261031 import code_closure

SOURCE='src/runtime/20261031_decimal_pad/native_main_020236e8.c'
BINDINGS={f'native_fn_{a}':{'module':'main','processor':'arm9','kind':'function','mode':'arm','address':'0x'+a} for a in ['02023568','02022a54']}


def main():
    inputs=verify_inputs(configuration());metadata,original,config=measured_module('main');compiler.WORK=ROOT/'work/main-decimal-pad-source-20261031/compile'
    rows,_=compiler.compare(ROOT/SOURCE,'main',3,'off',True);assert len(rows)==1;row=rows[0];assert row['exactAfterDeclaredRelocation']
    directory=ROOT/'work/main-decimal-pad-source-20261031/linked';proof=validate(row,BINDINGS,directory=directory);assert proof['exactCallerBytes']
    rebuilt=bytearray(original);rebuilt[ENTRY-0x02000000:ENTRY-0x02000000+168]=(directory/'caller.bin').read_bytes()
    row.update(sourceLanguage='C',ordinaryFunctionCredit=1,originalObjectScaffolding=False,realMainLink=proof,exactAfterRealMwLink=True,sourceDependencies=[])
    row['boundaries']=dict(main_references(row,original,config),instructionBytes=168,literalPoolBytes=0,generatedLiteralOrPaddingBytes=0)
    results=[];observed=set();maximum=0
    for tag,case in enumerate(cases()):
        a=execute(original,case,tag);b=execute(bytes(rebuilt),case,tag);assert a==b;results.append({'case':case,'result':a});observed.update(a['pcs']);maximum=max(maximum,a['state']['instructions'])
    real_chain=[]
    for bits in [0,0x8000000000000000,0x3FF0000000000000,0xBFF0000000000000,0x4024000000000000,0x3FB999999999999A,0x7FF0000000000000,0xFFF0000000000000,0x7FF8000000000001,1,0x0010000000000000,0x7FEFFFFFFFFFFFFF]:
        for limit in [-1,1,6,32]:
            case=[0,limit,0,0,0,False];tag=len(real_chain)
            a=execute(original,case,tag,real_bits=bits);b=execute(bytes(rebuilt),case,tag,real_bits=bits);assert a==b
            real_chain.append({'rawBits':hex(bits),'limit':limit,'result':a});maximum=max(maximum,a['state']['instructions'])
    source=(ROOT/SOURCE).read_text(encoding='utf-8-sig');controls=[]
    for name,text in [('wrong-padding-index',source.replace('out->digits[previous] = 0;', 'out->digits[previous + 1] = 0;')),('wrong-byte-adjustment',source.replace('+= 48;', '+= 47;'))]:
        path=ROOT/f'nonmatching/main-runtime/20261031/range-map-{name}.c';path.write_text(text,encoding='utf-8');compiler.WORK=ROOT/f'work/main-decimal-pad-controls-20261031/{name}/compile';bad,_=compiler.compare(path,'main',3,'off',True);work=compiler.WORK.parent/'linked'
        try:validate(bad[0],BINDINGS,directory=work)
        except ValueError as error:refusal=str(error)
        else:raise AssertionError('Wrong complete C matched')
        payload=(work/'caller.bin').read_bytes();assert len(payload)<=168;mutant=bytearray(original);mutant[ENTRY-0x02000000:ENTRY-0x02000000+len(payload)]=payload;vectors=[]
        for tag,case in enumerate([[1,4,0,1,0,False],[4,2,0,9,0,False],[1,4,0,10,0,False],[1,4,0,255,0,False]]):
            a=execute(original,case,tag);b=execute(bytes(mutant),case,tag,check=False);vectors.append({'case':case,'actualReturns':2,'rejected':not b['modelPassed'],'positiveControl':b['modelPassed']})
        assert any(c['rejected'] for c in vectors) and any(c['positiveControl'] for c in vectors)
        controls.append({'name':name,'source':path.relative_to(ROOT).as_posix(),'sourceSha256':sha256(path),'wholeCompiledCRealLinked':True,'byteRefusal':refusal,'cases':vectors})
    assert verify_inputs(configuration())==inputs
    report={'schemaVersion':1,'romSha256':configuration()['romSha256'],'processor':'arm9','module':'main','matches':rows,'matchedFunctions':1,'matchedBytes':168,'nativeSymbolEntries':{},'generatorSources':[{'path':p,'sha256':sha256(ROOT/p)} for p in code_closure(['match_main_decimal_pad_20261031.py'])],
        'oracle':{'pairs':len(results),'actualTopReturns':2*(len(results)+len(real_chain)),'syntheticActualReturns':2*len(results),'actualNativeConverterReturns':2*len(real_chain),'realChainRows':real_chain,'syntheticConverterProvidersPerRun':1,'realChainFunctionProviders':0,'converterBodyExecutedInRealChain':True,'converterArithmeticIndependentlyValidated':False,'roundingBodyAndLeavesExecuted':True,'instructionLimit':100000,'maximumInstructions':maximum,'ownInstructionPcs':len(observed),'rows':results},'negativeControls':{'actualReturns':16,'controls':controls},'inputsUnchanged':True,'wholeModuleLinked':False,'sourceCreditAcceptedByThisScript':0,
        'limitations':['Synthetic converter outputs are supplied after checking all three raw argument words; additional real chains execute the converter and harvest its output as an explicit continuation fixture, not an independent arithmetic oracle','Original rounding entry and both digit helpers execute through actual returns, separately counted; no dependency source credit','Allocated260-byte buffers bound all tested byte counts; aliases cover identical settings/output objects only','Signed16 narrowing follows the measured target ABI; no historical structure names are claimed','No full game, source-only module, or Android execution is established']}
    write_json(ROOT/'evidence/matches/main-decimal-pad-20261031.json',report);print({'bytes':168,'actualTopReturns':2*(len(results)+len(real_chain)),'actualNativeConverterReturns':2*len(real_chain),'ownInstructionPcs':len(observed),'maximumInstructions':maximum,'negativeReturns':16})


if __name__=='__main__':
    main()
