import gzip
import hashlib
import json
from project import ROOT,configuration,verify_inputs,write_json,sha256
import match_runtime as compiler
from link_runtime_unit import validate,measured_module
from match_main_overlap_copy_20261030 import main_references
from main_range_reader_native_20261031 import execute,cases,ENTRY
from seal_recovery_evidence_20261031 import code_closure

SOURCE='src/runtime/20261031_range_reader/native_main_020369e0.c'
BINDINGS={f'native_fn_{a}':{'module':'main','processor':'arm9','kind':'function','mode':'arm','address':'0x'+a} for a in ['0203694c','02036994']}


def main():
    inputs=verify_inputs(configuration());metadata,original,config=measured_module('main');compiler.WORK=ROOT/'work/main-range-reader-source-20261031/compile';rows,_=compiler.compare(ROOT/SOURCE,'main',2,'off',True);row=rows[0];assert len(rows)==1 and row['exactAfterDeclaredRelocation']
    directory=compiler.WORK.parent/'linked';proof=validate(row,BINDINGS,directory=directory);assert proof['exactCallerBytes'];rebuilt=bytearray(original);rebuilt[ENTRY-0x02000000:ENTRY-0x02000000+172]=(directory/'caller.bin').read_bytes()
    row.update(sourceLanguage='C',ordinaryFunctionCredit=1,originalObjectScaffolding=False,realMainLink=proof,exactAfterRealMwLink=True,sourceDependencies=[]);row['boundaries']=dict(main_references(row,original,config),instructionBytes=168,literalPoolBytes=4,generatedLiteralOrPaddingBytes=0)
    results=[];observed=set();maximum=0;callbacks=0;helpers=0
    for tag,case in enumerate(cases()):
        a=execute(original,case,tag);b=execute(bytes(rebuilt),case,tag);assert a==b;results.append({'case':case,'result':a});observed.update(a['pcs']);maximum=max(maximum,a['state']['instructions']);callbacks+=a['state']['callbackProviders']*2;helpers+=a['state']['originalHelperReturns']*2
    text=(ROOT/SOURCE).read_text(encoding='utf-8-sig');path=ROOT/'nonmatching/main-runtime/20261031/range-reader/wrong-stop-key.c';path.write_text(text.replace('key == 10','key == 11').replace('key == 10','key == 11'),encoding='utf-8');compiler.WORK=ROOT/'work/main-range-reader-control-20261031/compile';bad,_=compiler.compare(path,'main',2,'off',True);directory=compiler.WORK.parent/'linked'
    try:validate(bad[0],BINDINGS,directory=directory)
    except ValueError as error:refusal=str(error)
    else:raise AssertionError('Wrong whole C matched')
    payload=(directory/'caller.bin').read_bytes();assert len(payload)==172;mutant=bytearray(original);mutant[ENTRY-0x02000000:ENTRY-0x02000000+172]=payload;controls=[]
    control_cases=[([1,10,2,0],1,0,False,True,0),([11,1,0],1,127,True,True,1),([1,2,0],1,128,False,False,1),([0],0,0,True,True,0)]
    for tag,case in enumerate(control_cases):
        a=execute(original,case,tag);b=execute(bytes(mutant),case,tag,check=False);controls.append({'case':case,'actualReturns':2,'rejected':not b['modelPassed'],'positiveControl':b['modelPassed']})
    assert sum(x['rejected'] for x in controls)==2 and sum(x['positiveControl'] for x in controls)==2 and verify_inputs(configuration())==inputs
    raw=json.dumps(results,sort_keys=True,separators=(',',':')).encode();compressed=gzip.compress(raw,mtime=0);path_vectors=ROOT/'evidence/vectors/main-range-reader-20261031.json.gz';path_vectors.parent.mkdir(parents=True,exist_ok=True);path_vectors.write_bytes(compressed);assert gzip.decompress(path_vectors.read_bytes())==raw
    vector={'path':path_vectors.relative_to(ROOT).as_posix(),'sha256':sha256(path_vectors),'uncompressedSha256':hashlib.sha256(raw).hexdigest(),'compressedBytes':len(compressed),'uncompressedBytes':len(raw),'cases':len(results),'gzipMtime':0}
    report={'schemaVersion':1,'romSha256':configuration()['romSha256'],'processor':'arm9','module':'main','matches':rows,'matchedFunctions':1,'matchedBytes':172,'nativeSymbolEntries':{},'generatorSources':[{'path':p,'sha256':sha256(ROOT/p)} for p in code_closure(['match_main_range_reader_20261031.py'])],
        'oracle':{'pairs':len(results),'actualTopReturns':2*len(results),'originalHelperReturns':helpers,'callbackProviders':callbacks,'ownInstructionPcs':len(observed),'instructionLimit':2000,'maximumInstructions':maximum,'vectorArtifact':vector},'negativeControls':{'wholeCompiledCRealLinked':True,'source':path.relative_to(ROOT).as_posix(),'sourceSha256':sha256(path),'byteRefusal':refusal,'actualReturns':8,'cases':controls},'replayDependencies':[{'path':vector['path'],'sha256':vector['sha256']}],'inputsUnchanged':True,'wholeModuleLinked':False,'sourceCreditAcceptedByThisScript':0,
        'limitations':['Raw keys0 and10 terminate the supplied callback stream; no text/encoding/font/gameplay meaning is assigned','Three original lookup bodies execute; callback results/mutations are provided and counted separately','Allocated aligned records cover direct/sparse mappings, default selection, signed byte metrics and defined unsigned32 accumulation wrap','The callback pointer is cached before provider changes; base/fallback fields are read after each callback','Pointer/address words and signed32 casts are qualified to the measured ARM32 ABI; invalid pointers, cycles, arbitrary aliases and unterminated streams are unsupported','No real callback body, ordinary caller reachability, source-only module or complete game execution is proved']}
    write_json(ROOT/'evidence/matches/main-range-reader-20261031.json',report);print({'bytes':172,'actualTopReturns':2*len(results),'originalHelperReturns':helpers,'callbackProviders':callbacks,'ownInstructionPcs':len(observed),'maximumInstructions':maximum,'negativeReturns':8})


if __name__=='__main__':main()
