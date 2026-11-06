import copy
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import match_runtime
import arm7_sdk295_transmit_family_native_20261102 as native
import link_arm7_sdk294_transmit_family_20261102 as linker
from project import ROOT,sha256,configuration,write_json

REPORT=ROOT/'evidence/matches/arm7-sdk296-transmit-family1600-20261102.json'
CONTROLS=ROOT/'evidence/verification/arm7-sdk297-transmit-family-controls-20261102.json'
WORK=ROOT/'work/arm7-bulk-20261030/sdk297-transmit-family-controls'

def verify_file(row):
    path=(ROOT/row['path']).resolve();path.relative_to(ROOT.resolve())
    if not path.is_file()or sha256(path)!=row['sha256']:raise ValueError('Missing or changed current product/input:'+row['path'])

def current(report):
    seeds=json.loads(linker.PROFILE.read_text())['units'];matches=report['matches']
    if len(matches)!=7 or report['matchedInitializedBytes']!=1600 or report['newOrdinaryFunctionCount']!=7 or report['initializedDenominatorDelta']!=0 or report['wholeModuleLinked']or report['originalCallbackAndTableSourceCredit']!=0:raise ValueError('Complete measured seven-unit coverage or zero scaffolding credit changed')
    for pin in report['generatorSources']:verify_file(pin)
    if sha256(configuration()['rom'])!=report['romSha256']:raise ValueError('Measured ROM input differs')
    by_name={r['name']:r for r in matches}
    if set(by_name)!={s['name']for s in seeds}:raise ValueError('Required source identity missing/duplicated')
    vectors=native.cases();total=0;helper=setup=0
    for seed in seeds:
        row=by_name[seed['name']];linker.qualified(row)
        if not row['exactBytes']or not row['exactAfterDeclaredRelocation']or not row['sourceOnlyCompilerInput']or row['originalObjectScaffolding']:raise ValueError('Fresh ordinary source exactness evidence missing')
        for path,digest in[(row['object'],row['objectSha256']),(row['source'],row['sourceSha256'])]:verify_file(dict(path=path,sha256=digest))
        for pin in row['sourceDependencies']:verify_file(pin)
        expected=[str(ROOT/seed['compiler']),*seed['compilerFlags'],'-c',str(ROOT/seed['source']),'-o',str(ROOT/row['object'])]
        if row['command']!=expected or row['cwd']!=str(ROOT):raise ValueError('Actual source-only compiler command differs')
        proof=row['realLink'];path=(ROOT/proof['lcf']).parent/'caller.bin';base=native.context.WRAM if row['module']=='arm7-wram'else native.context.MAIN;binary=(ROOT/row['binary']).read_bytes();start=int(row['address'],0)-base;target=binary[start:start+row['bytes']]
        if not proof['exactLinkedBytes']or not path.is_file()or path.read_bytes()!=target or hashlib.sha256(target).hexdigest()!=row['targetSha256']:raise ValueError('Current full genuinely linked module range differs')
        if proof['callerSpecificQualification']['generatorSha256']!=sha256(ROOT/'link_arm7_sdk294_transmit_family_20261102.py'):raise ValueError('Qualified linker version differs')
        if row['nativeSymbols']!={name:b['address']for name,b in proof['bindings'].items()}or any(not isinstance(v,str)or not v.startswith('0x')for v in row['nativeSymbols'].values()):raise ValueError('Measured hex native-symbol publication changed')
        trace=row['oracle']['trace'];verify_file(dict(path=trace['path'],sha256=trace['compressedSha256']));raw=gzip.decompress((ROOT/trace['path']).read_bytes())
        if hashlib.sha256(raw).hexdigest()!=trace['rawSha256']:raise ValueError('Native records changed after deterministic compression')
        records=json.loads(raw);wanted=[c for c in vectors if c['entry']==int(seed['address'],0)]
        if len(records)!=len(wanted)or row['oracle']['actualOriginalAndCompiledReturns']!=2*len(wanted):raise ValueError('Required complete native/source vector/actual-return records missing')
        for record,case in zip(records,wanted):
            if record['case']!=case:raise ValueError('Native input vector order changed')
            for key in('original','compiled'):
                item=record[key]
                if not item['actualOwnReturn']or not item['modelPassed']or not all(item['modelChecks'].values())or item['providerReplacements']:raise ValueError('Independent returning provider-free state proof failed')
                if any(not r['actualReturn']for r in item['actualDeclaredHelperReturns']+item['actualSetupEntryReturns']):raise ValueError('Observed lower entry did not actually return')
                helper+=len(item['actualDeclaredHelperReturns']);setup+=len(item['actualSetupEntryReturns'])
            if not all(record['comparisons'].values())or any(record['original'][k]!=record['compiled'][k]for k in('registers','cpsr','pc','relevantRegisters','orderedNonstackWrites','ownedNonstackWrites','memorySha256','modelChecks')):raise ValueError('Original versus compiled source field/state effects differ')
        total+=2*len(records)
    if(total,helper,setup)!=(report['totalActualOwnReturns'],report['totalActualDeclaredHelperReturns'],report['totalActualSetupEntryReturns'])or total!=784:raise ValueError('Measured return totals disagree with actual fresh records')
    if len(report['wrongC'])!=7:raise ValueError('Every accepted ordinary function requires a returning wrong-C control')
    for wrong in report['wrongC']:
        trace=wrong['trace'];verify_file(dict(path=trace['path'],sha256=trace['compressedSha256']));raw=gzip.decompress((ROOT/trace['path']).read_bytes())
        if hashlib.sha256(raw).hexdigest()!=trace['rawSha256']:raise ValueError('Wrong-source records changed')
        records=json.loads(raw);returned=sum(r['result']['actualOwnReturn']for r in records);rejected=sum(r['result']['actualOwnReturn']and not r['result']['modelPassed']for r in records)
        if returned!=len(records)or(returned,rejected)!=(wrong['actualOwnReturns'],wrong['modelRejections'])or not rejected:raise ValueError('Wrong ordinary C lacked actual returning independent rejection')
    return dict(functions=7,bytes=1600,actualOwnReturns=total,actualDeclaredHelperReturns=helper,actualSetupReturns=setup,wrongReturns=sum(r['actualOwnReturns']for r in report['wrongC']),wrongModelRejections=sum(r['modelRejections']for r in report['wrongC']))

def main():
    process=subprocess.run([sys.executable,str(ROOT/'match_arm7_sdk296_transmit_family_20261102.py')],cwd=ROOT.parent,capture_output=True,text=True,timeout=360)
    if process.returncode:raise ValueError(process.stdout+process.stderr)
    report=json.loads(REPORT.read_text());positive=current(report);seeds=json.loads(linker.PROFILE.read_text())['units'];controls=[];WORK.mkdir(parents=True,exist_ok=True);originals=(linker.base.namespace,linker.base.derive_bindings,linker.base.data_binding)
    def reject(name,call):
        try:call()
        except(ValueError,FileNotFoundError)as error:controls.append(dict(name=name,rejected=True,error=str(error)));return
        raise ValueError('Negative control unexpectedly accepted:'+name)
    for seed in seeds:
        for key,value in [('processor','arm9'),('program','dwc/utility.bin/move/child.srl'),('module','arm7-boot'),('mode','thumb'),('address',hex(int(seed['address'],0)+4)),('bytes',seed['bytes']-4),('sourceSha256','0'*64),('compilerSha256','0'*64),('compilerFlags',seed['compilerFlags']+['-O0']),('sourceDependencies',[]),('runtimePointerQualification',None),('nativeScopeQualification',None),('nativeInterfaceContract',dict(seed['nativeInterfaceContract'],physicalWordBytes=8))]:reject(seed['name']+'-wrong-'+key,lambda s=dict(seed,**{key:value}):linker.qualified(s))
    for key,value in [('matches',report['matches'][:-1]),('matchedInitializedBytes',1704),('totalActualOwnReturns',783),('originalCallbackAndTableSourceCredit',104)]:reject('publication-'+key,lambda r=dict(report,**{key:value}):current(r))
    altered=copy.deepcopy(report);altered['matches'][0]['oracle']['trace']['path']='work/arm7-bulk-20261030/sdk297-missing-native-records.json.gz';reject('missing-native-product-withholds-current-credit',lambda:current(altered))
    initial=next(r for r in report['matches']if r['name']=='InitTxCtrl');ordinary=next(r for r in report['matches']if r['name']=='ClearTxKeyData')
    reject('reviewed-callback-supplement-withheld',lambda:linker.validate(initial,WORK/'no-callback',qualify_callback=False));reject('runtime-word-qualification-withheld',lambda:linker.validate(ordinary,WORK/'no-runtime-word',qualify_runtime_word=False))
    for field,value in [('offset',0),('type',2),('symbol','arbitrary_unqualified_pointer'),('sourceSymbolType','STT_OBJECT'),('explicitAddend',0),('originalEncodedWord','00000000')]:
        altered=copy.deepcopy(ordinary);altered['relocations'][0][field]=value;reject('unaltered-object-relocation-'+field,lambda r=altered,n=field:linker.validate(r,WORK/('wrong-'+n)))
    for target in(0x0380fff0,0x0380fff8,0x0380fffc):reject('unchanged-unknown-data-'+hex(target),lambda t=target:originals[2](dict(program=''),t,originals[0]('')[0]))
    main_bytes=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();reset_case=next(c for c in native.cases()if c['entry']==0x027f0ce0);reject('out-of-range-three-entry-index',lambda:native.run(main_bytes,wram,dict(reset_case,priority=3),0,{}))
    if originals!=(linker.base.namespace,linker.base.derive_bindings,linker.base.data_binding)or 0x027f0950 in linker.base.namespace('')[1]:raise ValueError('Qualified linker scope escaped success/error cleanup')
    output=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),canonicalReport=REPORT.relative_to(ROOT).as_posix(),canonicalReportSha256=sha256(REPORT),positive=positive,negativeControls=controls,negativeControlCount=len(controls),allRejected=True,allOriginalGuardsRestored=True,sourceCreditPendingIntegratorModuleAcceptance=0);write_json(CONTROLS,output);print(json.dumps(dict(reportSha256=sha256(REPORT),controls=len(controls),controlSha256=sha256(CONTROLS),positive=positive)),flush=True)

if __name__=='__main__':main()
