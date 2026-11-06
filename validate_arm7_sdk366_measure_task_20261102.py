import copy
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import match_runtime
import arm7_sdk356_measure_task_native_20261102 as native
import link_arm7_sdk363_measure_task_20261102 as linker
import compile_arm7_sdk350_mlme_tasks_timeouts_20261102 as callback_compiler
from project import ROOT,sha256,write_json,configuration

REPORT=ROOT/'evidence/matches/arm7-sdk365-measure-task624-20261102.json'
CONTROLS=ROOT/'evidence/verification/arm7-sdk366-measure-task-controls-20261102.json'
WORK=ROOT/'work/arm7-bulk-20261030/sdk366-measure-task-controls'

def checked(path,digest):
    p=(ROOT/path).resolve();p.relative_to(ROOT.resolve())
    if not p.is_file()or sha256(p)!=digest:raise ValueError('Current declared input/product unavailable or changed:'+path)
    return p

def records(trace):
    p=checked(trace['path'],trace['compressedSha256']);raw=gzip.decompress(p.read_bytes())
    if hashlib.sha256(raw).hexdigest()!=trace['rawSha256']:raise ValueError('Native raw records changed')
    return json.loads(raw)

def current(report):
    if report.get('processor')!='arm7'or report.get('program')!=''or report.get('romSha256')!='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6':raise ValueError('Published full processor/program/build identity differs')
    if len(report['matches'])!=1 or report['matchedInitializedBytes']!=624 or report['newOrdinaryFunctionCount']!=1 or report['initializedDenominatorDelta']or report['wholeModuleLinked']or report['sourceReconstructionComplete']or report['originalCalleesAndAdditionalDefinitionsCredit']or report['unsupportedSourceCredit']:raise ValueError('Complete own-source range or zero-scaffolding limits changed')
    checked(report['generator'],report['generatorSha256'])
    for r in report['generatorSources']:checked(r['path'],r['sha256'])
    if sha256(configuration()['rom'])!='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6':raise ValueError('Original ROM differs')
    row=report['matches'][0];seed=linker.qualified(row)
    if not row['exactBytes']or not row['exactAfterDeclaredRelocation']or not row['sourceOnlyCompilerInput']or row['originalObjectScaffolding']:raise ValueError('Complete source-only exact match evidence required')
    checked(row['object'],row['objectSha256']);checked(row['source'],row['sourceSha256'])
    for r in row['sourceDependencies']:checked(r['path'],r['sha256'])
    if row['command']!=[str(ROOT/seed['compiler']),*seed['compilerFlags'],'-c',str(ROOT/seed['source']),'-o',str(ROOT/row['object'])]or row['cwd']!=str(ROOT):raise ValueError('Actual compiler source-only argv/CWD differs')
    link=row['realLink'];directory=(ROOT/link['lcf']).parent
    for name,digest in[('unit.lcf',link['lcfSha256']),('linked.elf',link['linkedElfSha256']),('caller.o',link['splitObjectSha256']),('caller.bin',link['linkedCallerSha256'])]:checked((directory/name).relative_to(ROOT).as_posix(),digest)
    image=(ROOT/seed['binary']).read_bytes();a=int(seed['address'],0)-seed['base']
    if not link['exactLinkedBytes']or(directory/'caller.bin').read_bytes()!=image[a:a+624]or not link['qualifiedCanonicalScope']['namespaceRestored']or link['qualifiedCanonicalScope']['adapterSha256']!=sha256(linker.__file__):raise ValueError('Full actual original-linked range/scope cleanup differs')
    native_path=checked(report['originalContextReport']['path'],report['originalContextReport']['sha256']);baseline=json.loads(native_path.read_text())
    if baseline['generatorSha256']!=sha256(native.__file__)or baseline['actualOwnReturns']!=1112 or baseline['failedModels']or len(baseline['unsupported'])!=48 or report['unsupportedOriginalAttempts']!=baseline['unsupported']or any(r['postFaultStateCredit']or r['sourceCredit']or r['actualOwnReturn']for r in baseline['unsupported']):raise ValueError('Original supported/unsupported partition differs')
    originals=records(baseline['nativeTrace']);cases=native.cases();wanted=[(i,c)for i,(c,r)in enumerate(zip(cases,originals))if r['actualOwnReturn']]
    proof=records(row['oracle']['trace'])
    if len(originals)!=1160 or len(proof)!=1112 or len(wanted)!=1112:raise ValueError('Full measured case partition missing')
    helpers=setup=0
    for record,(i,c)in zip(proof,wanted):
        if record['index']!=i or record['case']!=c or record['original']!=originals[i]:raise ValueError('Fresh original physical-case ordering/records differ')
        for side in('original','compiled'):
            r=record[side]
            if not r['actualOwnReturn']or not r['modelPassed']or not all(r['modelChecks'].values())or r['providerReplacements']or any(not h['actualReturn']for h in r['actualDeclaredHelperReturns']+r['actualSetupEntryReturns']):raise ValueError('Actual returning provider-free model/observed-helper evidence failed')
            helpers+=len(r['actualDeclaredHelperReturns']);setup+=len(r['actualSetupEntryReturns'])
        fields=('registers','cpsr','pc','orderedNonstackWrites','ownedNonstackWrites','memorySha256','modelChecks','actualDeclaredHelperReturns')
        if not all(record['comparisons'].values())or any(record['original'][k]!=record['compiled'][k]for k in fields):raise ValueError('Original versus source full CPU/stack/RAM/stores differ')
    callback=row['oracle']['sourceLinkedCallbackProof'];c=callback['row'];checked(c['object'],c['objectSha256']);checked(c['source'],c['sourceSha256']);p=checked(callback['bodyPath'],callback['bodySha256'])
    if callback['additionalSourceCredit']!=0 or p.read_bytes()!=image[0xdad4:0xdad4+44]:raise ValueError('Fresh full callback source/dependency zero-credit proof missing')
    callback_compiler.linker.qualified(c)
    for r in c['sourceDependencies']:checked(r['path'],r['sha256'])
    if c['command']!=[str(ROOT/c['compiler']),*c['compilerFlags'],'-c',str(ROOT/c['source']),'-o',str(ROOT/c['object'])]or c['cwd']!=str(ROOT):raise ValueError('Fresh callback actual compiler inputs differ')
    cp=callback['realLink'];cd=(ROOT/cp['lcf']).parent
    for n,h in[('unit.lcf',cp['lcfSha256']),('linked.elf',cp['linkedElfSha256']),('caller.o',cp['splitObjectSha256']),('caller.bin',cp['linkedCallerSha256'])]:checked((cd/n).relative_to(ROOT).as_posix(),h)
    if not cp['exactLinkedBytes']or not cp['qualifiedCanonicalScope']['namespaceRestored']:raise ValueError('Complete callback source link/scope evidence missing')
    expected_callback=dict(address='0x27edad4',bytes=44,sha256=callback['bodySha256'],additionalCredit=0,asynchronousCallbackExecutionUnproved=True)
    if any(r['compiled']['sourceLinkedCallback']!=expected_callback for r in proof):raise ValueError('Fresh source callback body was not installed before own entry')
    if(helpers,setup)!=(report['totalActualDeclaredHelperReturns'],report['totalActualSetupEntryReturns'])or report['totalActualOwnReturns']!=2224 or report['nativeSymbols']!={k:v['address']for k,v in link['bindings'].items()}:raise ValueError('Measured return totals/native symbol publication differ')
    wrong=report['wrongC'];bad=records(wrong['trace']);returned=sum(r['result']['actualOwnReturn']for r in bad);rejected=sum(r['result']['actualOwnReturn']and not r['result']['modelPassed']for r in bad)
    if returned!=1112 or(returned,rejected)!=(wrong['actualOwnReturns'],wrong['modelRejections'])or not rejected:raise ValueError('Returning independent wrong-C rejection absent')
    return dict(functions=1,bytes=624,actualOwnReturns=2224,actualDeclaredHelperReturns=helpers,actualSetupReturns=setup,wrongReturns=returned,wrongRejected=rejected,unsupportedOriginalAttempts=48,unsupportedSourceCredit=0)

def main():
    p=subprocess.run([sys.executable,str(ROOT/'match_arm7_sdk365_measure_task_20261102.py')],cwd=ROOT.parent,capture_output=True,text=True,timeout=900)
    if p.returncode:raise ValueError(p.stdout+p.stderr)
    report=json.loads(REPORT.read_text());positive=current(report);row=report['matches'][0];controls=[];WORK.mkdir(parents=True,exist_ok=True);originals=(linker.base.namespace,linker.base.derive_bindings,linker.base.data_binding)
    def reject(name,call):
        try:call()
        except(ValueError,FileNotFoundError)as e:controls.append(dict(name=name,rejected=True,error=str(e)));return
        raise ValueError('Negative control passed:'+name)
    for field,value in[('processor','arm9'),('program','utility-child'),('module','arm7-wram'),('mode','thumb'),('address','0x27ed868'),('bytes',620),('codeBytes',604),('sourceSha256','0'*64),('sourceDependencies',[]),('compilerFlags',[]),('compilerSha256','0'*64),('targetSha256','0'*64),('qualifiedCanonicalScope',{}),('namespaceAllowedCallbackAddresses',['0x27ed410']),('compilerImplicitHelpers',[]),('runtimePointerQualification',None),('nativeInterfaceContract',{}),('relocationContract',[])]:reject('qualified-'+field,lambda r=dict(row,**{field:value}):linker.qualified(r))
    for field,value in[('symbol','_ll_udiv'),('relocationOffset',404),('target','0x3806e4c'),('mode','thumb'),('abiReportSha256','0'*64),('abiGeneratorSha256','0'*64),('usedReturn','r1'),('sourceOperator','arbitrary expression'),('sourceCalleeCredit',484)]:
        altered=copy.deepcopy(row);altered['compilerImplicitHelpers'][0][field]=value;reject('generated-helper-contract-'+field,lambda r=altered:linker.qualified(r))
    reject('default-scope-refusal',lambda:linker.validate(row,WORK/'no-scope',qualify_scope=False));reject('runtime-word-withheld',lambda:linker.validate(row,WORK/'no-word',qualify_runtime_word=False))
    for field,value in[('offset',0),('type',2),('symbol','_arbitrary_div'),('sourceSymbolType','STT_OBJECT'),('explicitAddend',0),('originalEncodedWord','00000000')]:
        r=copy.deepcopy(row);rel=next(z for z in r['relocations']if z['symbol']=='_u32_div_f');rel[field]=value;reject('implicit-generated-relocation-'+field,lambda r=r:linker.validate(r,WORK/('bad-'+field)))
    for field,value in[('matches',[]),('matchedInitializedBytes',625),('totalActualOwnReturns',2225),('unsupportedSourceCredit',48),('nativeSymbols',{})]:reject('current-'+field,lambda r=dict(report,**{field:value}):current(r))
    changed=copy.deepcopy(report);changed['matches'][0]['oracle']['trace']['path']='work/arm7-bulk-20261030/sdk366-missing-records.gz';reject('missing-native-output',lambda:current(changed))
    main=(ROOT/row['binary']).read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();case=native.cases()[0]
    for field,value in[('mode',1),('offset',8),('counter',-1),('counter',0x100000000),('cca',0x100000000),('state',65536),('time',-1),('channelByte',256)]:reject('physical-field-'+field+'-'+str(value),lambda c=dict(case,**{field:value}):native.run(main,wram,c,0))
    for state in(0x81,0x83):
        for index in(-1,16,65535):reject('read-bounds-'+str(state)+'-'+str(index),lambda c=dict(case,state=state,channelIndex=index):native.run(main,wram,c,0))
    fresh=linker._FRESH
    try:linker._FRESH=None;reject('fresh-scope-required',linker.current_scope)
    finally:linker._FRESH=fresh
    baseline=originals[0]('')[1]
    with linker.installed(row):
        now=linker.base.namespace('')[1]
        if set(now)-set(baseline)!={0x027edad4}or any(now[k]!=v for k,v in baseline.items()):raise ValueError('Exact one-entry namespace delta differs')
    def forced_error():
        with linker.installed(row):raise ValueError('Forced caller exception must restore original namespace')
    reject('exception-context-restoration',forced_error)
    for address in(0x0380fff0,0x0380fff8,0x0380fffc):reject('unchanged-other-word-'+hex(address),lambda address=address:originals[2](dict(program=''),address,originals[0]('')[0]))
    if originals!=(linker.base.namespace,linker.base.derive_bindings,linker.base.data_binding):raise ValueError('Temporary caller rules escaped cleanup')
    result=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),canonicalReport=REPORT.relative_to(ROOT).as_posix(),canonicalReportSha256=sha256(REPORT),positive=positive,negativeControls=controls,negativeControlCount=len(controls),allRejected=True,allOriginalHooksRestored=True,sourceCreditPendingIntegrator=0);write_json(CONTROLS,result);print(json.dumps(dict(reportSha256=sha256(REPORT),controlSha256=sha256(CONTROLS),controls=len(controls),positive=positive)),flush=True)

if __name__=='__main__':main()
