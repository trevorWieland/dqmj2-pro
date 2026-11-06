import gzip
import hashlib
import json
from project import ROOT,configuration,verify_inputs,write_json,sha256
import match_runtime as compiler
from link_runtime_unit import validate,measured_module
from match_main_overlap_copy_20261030 import main_references
from main_va_adapter_native_20261031 import execute,cases,ENTRY
from seal_recovery_evidence_20261031 import code_closure

SOURCE='src/runtime/20261031_va_adapter/native_main_020211c0.c'
BINDINGS={'native_fn_020211e8':{'module':'main','processor':'arm9','kind':'function','mode':'arm','address':'0x020211e8'}}


def main():
    inputs=verify_inputs(configuration());metadata,original,config=measured_module('main');compiler.WORK=ROOT/'work/main-va-adapter-source-20261031/compile';rows,_=compiler.compare(ROOT/SOURCE,'main',2,'off',True);row=rows[0];assert len(rows)==1 and row['exactAfterDeclaredRelocation']
    directory=compiler.WORK.parent/'linked';proof=validate(row,BINDINGS,directory=directory);assert proof['exactCallerBytes'];rebuilt=bytearray(original);rebuilt[ENTRY-0x02000000:ENTRY-0x02000000+40]=(directory/'caller.bin').read_bytes()
    row.update(sourceLanguage='C',ordinaryFunctionCredit=1,originalObjectScaffolding=False,realMainLink=proof,exactAfterRealMwLink=True,sourceDependencies=[]);row['boundaries']=dict(main_references(row,original,config),instructionBytes=40,literalPoolBytes=0,generatedLiteralOrPaddingBytes=0)
    results=[];observed=set();maximum=0
    for tag,case in enumerate(cases()):
        a=execute(original,case,tag);b=execute(bytes(rebuilt),case,tag);assert a==b;results.append({'case':case,'result':a});observed.update(a['pcs']);maximum=max(maximum,a['state']['instructions'])
    source=(ROOT/SOURCE).read_text(encoding='utf-8-sig');badsource=ROOT/'nonmatching/main-runtime/20261031/va-adapter/wrong-eight-alignment.c';badsource.write_text(source.replace('~3U','~7U'),encoding='utf-8');compiler.WORK=ROOT/'work/main-va-adapter-control-20261031/compile';bad,_=compiler.compare(badsource,'main',2,'off',True);directory=compiler.WORK.parent/'linked'
    try:validate(bad[0],BINDINGS,directory=directory)
    except ValueError as error:refusal=str(error)
    else:raise AssertionError('Wrong complete C matched')
    payload=(directory/'caller.bin').read_bytes();assert len(payload)==40;mutant=bytearray(original);mutant[ENTRY-0x02000000:ENTRY-0x02000000+40]=payload;controls=[]
    for tag,case in enumerate([(0x02510100,6,count,bias,False) for count in [0,1,4] for bias in [0,4]]):
        a=execute(original,case,tag);b=execute(bytes(mutant),case,tag,check=False);controls.append({'case':case,'actualReturns':2,'rejected':not b['modelPassed'],'positiveControl':b['modelPassed']})
    assert sum(x['rejected'] for x in controls)==3 and sum(x['positiveControl'] for x in controls)==3 and verify_inputs(configuration())==inputs
    raw=json.dumps(results,sort_keys=True,separators=(',',':')).encode('utf-8');compressed=gzip.compress(raw,mtime=0)
    path=ROOT/'evidence/vectors/main-va-adapter-20261031.json.gz';path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(compressed);assert gzip.decompress(path.read_bytes())==raw
    vector={'path':path.relative_to(ROOT).as_posix(),'sha256':sha256(path),'uncompressedSha256':hashlib.sha256(raw).hexdigest(),'compressedBytes':len(compressed),'uncompressedBytes':len(raw),'cases':len(results),'gzipMtime':0}
    report={'schemaVersion':1,'romSha256':configuration()['romSha256'],'processor':'arm9','module':'main','matches':rows,'matchedFunctions':1,'matchedBytes':40,'nativeSymbolEntries':{},'generatorSources':[{'path':p,'sha256':sha256(ROOT/p)} for p in code_closure(['match_main_va_adapter_20261031.py'])],'oracle':{'pairs':len(results),'actualTopReturns':2*len(results),'lowerProviders':2*len(results),'variableArgumentCounts':[0,1,2,3,4,5,6,7,8],'ownInstructionPcs':len(observed),'instructionLimit':100,'maximumInstructions':maximum,'vectorArtifact':vector},'negativeControls':{'wholeCompiledCRealLinked':True,'source':badsource.relative_to(ROOT).as_posix(),'sourceSha256':sha256(badsource),'byteRefusal':refusal,'actualReturns':12,'cases':controls},'replayDependencies':[{'path':vector['path'],'sha256':vector['sha256']}],'inputsUnchanged':True,'wholeModuleLinked':False,'sourceCreditAcceptedByThisScript':0,'limitations':['The manual argument-home expression is qualified only to the pinned32-bit Metrowerks ARM register-home ABI and four-byte-aligned stacks','Three fixed raw buffer/limit/format words plus actual variadic words are forwarded; raw lower return is preserved','All lower formatting is explicitly supplied; no Unicode, locale, bounds, truncation, real formatting or scene semantics are established','Provider mutation of the first variadic home is separate from the saved incoming R3 that the wrapper restores','Pointer32 casts and stack-home locations are not a portable host or Android va_list implementation']}
    write_json(ROOT/'evidence/matches/main-va-adapter-20261031.json',report);print({'bytes':40,'actualTopReturns':2*len(results),'providedLowerReturns':2*len(results),'ownInstructionPcs':len(observed),'negativeReturns':12})


if __name__=='__main__':main()
