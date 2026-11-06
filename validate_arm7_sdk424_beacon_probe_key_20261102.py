import copy
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import match_runtime
import link_arm7_sdk421_beacon_probe_key_20261102 as linker
from project import ROOT,sha256,configuration,write_json

REPORT=ROOT/'evidence/matches/arm7-sdk423-beacon-probe-key3016-20261102.json'
CONTROLS=ROOT/'evidence/verification/arm7-sdk424-beacon-probe-key-controls-20261102.json'
WORK=ROOT/'work/arm7-bulk-20261030/sdk424-beacon-probe-key-controls'

def verify_file(row):
    path=(ROOT/row['path']).resolve();path.relative_to(ROOT.resolve())
    if not path.is_file()or sha256(path)!=row['sha256']:raise ValueError('Missing or changed current source/product:'+row['path'])

def records(trace):
    verify_file(dict(path=trace['path'],sha256=trace['compressedSha256']));raw=gzip.decompress((ROOT/trace['path']).read_bytes())
    if hashlib.sha256(raw).hexdigest()!=trace['rawSha256']:raise ValueError('Deterministic raw native records changed')
    return json.loads(raw)

def current(report):
    seeds=json.loads(linker.PROFILE.read_text())['units'];matches=report['matches']
    if len(matches)!=3 or report['matchedInitializedBytes']!=3016 or report['newOrdinaryFunctionCount']!=3 or report['initializedDenominatorDelta']!=0 or report['wholeModuleLinked']or report['originalCalleesAndAdditionalDefinitionsCredit']!=0 or report['totalActualOwnReturns']!=25920 or not report['sourceInputsNoWorkCaches']or report['sourceReconstructionComplete']:raise ValueError('Three complete ordinary-source units/zero scaffolding/actual-return summary changed')
    if report['generatorSha256']!=sha256(ROOT/report['generator']):raise ValueError('Actual source-only generator changed')
    for pin in report['generatorSources']:verify_file(pin)
    if sha256(configuration()['rom'])!=report['romSha256']:raise ValueError('Measured original ROM identity changed')
    by_name={r['name']:r for r in matches}
    if set(by_name)!={s['name']for s in seeds}:raise ValueError('Complete qualified source identities missing or duplicated')
    own=helper=setup=wrong_return=wrong_reject=0;symbols={}
    for seed in seeds:
        row=by_name[seed['name']];linker.qualified(row)
        expected_callees=[dict(entry=s['address'],bytes=s['bytes'],sha256=s['targetSha256'],additionalCredit=0)for s in seeds if s['address']!=seed['address']]
        if row['oracle']['sourceLinkedReceiveCallees']!=expected_callees or row['oracle']['sourceLinkedReceiveAdditionalCredit']!=0:raise ValueError('Complete fresh source-linked receive identities or zero callee credit differs')
        if not row['exactBytes']or not row['exactAfterDeclaredRelocation']or not row['sourceOnlyCompilerInput']or row['originalObjectScaffolding']or row['unrecoveredCalleesAndExtraDefinitionsCredit']!=0:raise ValueError('Full ordinary-source byte evidence/zero dependency credit missing')
        for path,digest in[(row['object'],row['objectSha256']),(row['source'],row['sourceSha256'])]:verify_file(dict(path=path,sha256=digest))
        for pin in row['sourceDependencies']:verify_file(pin)
        expected=[str(ROOT/seed['compiler']),*seed['compilerFlags'],'-c',str(ROOT/seed['source']),'-o',str(ROOT/row['object'])]
        if row['command']!=expected or row['cwd']!=str(ROOT):raise ValueError('Actual complete source-only compiler command differs')
        proof=row['realLink'];directory=(ROOT/proof['lcf']).parent;image=(ROOT/row['binary']).read_bytes();start=int(row['address'],0)-seed['base'];target=image[start:start+row['bytes']]
        for name,digest in[('unit.lcf',proof['lcfSha256']),('linked.elf',proof['linkedElfSha256']),('caller.o',proof['splitObjectSha256']),('caller.bin',proof['linkedCallerSha256'])]:verify_file(dict(path=(directory/name).relative_to(ROOT).as_posix(),sha256=digest))
        if proof['sourceObjectSha256']!=row['objectSha256']or not proof['exactLinkedBytes']or(directory/'caller.bin').read_bytes()!=target or hashlib.sha256(target).hexdigest()!=row['targetSha256']:raise ValueError('Complete current genuine linked range differs')
        if proof['callerSpecificQualification']['generatorSha256']!=sha256(ROOT/'link_arm7_sdk421_beacon_probe_key_20261102.py'):raise ValueError('Exact caller data/role qualification changed')
        if row['nativeSymbols']!={k:v['address']for k,v in proof['bindings'].items()}or any(not isinstance(v,str)or not v.startswith('0x')for v in row['nativeSymbols'].values()):raise ValueError('Measured hexadecimal symbol publication differs')
        for name,value in row['nativeSymbols'].items():
            if name in symbols and symbols[name]!=value:raise ValueError('Conflicting named physical symbol')
            symbols[name]=value
        layout=row['abiLayoutProof'];verify_file(dict(path=layout['source'],sha256=layout['sourceSha256']));verify_file(dict(path=layout['object'],sha256=layout['objectSha256']))
        import match_arm7_sdk423_beacon_probe_key_20261102 as producer
        indices=list(range(len(producer.FIELDS)))
        if layout['expressions']!=[producer.FIELDS[i]for i in indices]or layout['values']!=[producer.VALUES[i]for i in indices]:raise ValueError('Full compatible primitive/frame/context/alarm layout missing')
        module=producer.MODULES[seed['name']];wanted=module.cases();proof_records=records(row['oracle']['trace'])
        if len(proof_records)!=len(wanted)or row['oracle']['actualOriginalAndCompiledReturns']!=2*len(wanted):raise ValueError('Complete actual-return/vector evidence missing')
        for record,case in zip(proof_records,wanted):
            if record['case']!=case:raise ValueError('Supported deterministic input order differs')
            for key in('original','compiled'):
                result=record[key]
                if not result['actualOwnReturn']or not result['modelPassed']or not all(result['modelChecks'].values())or result['providerReplacements']:raise ValueError('Independent returning provider-free state proof failed')
                if any(not r['actualReturn']for r in result['actualDeclaredHelperReturns']+result['actualSetupEntryReturns']):raise ValueError('Observed helper/setup lacked actual return')
                helper+=len(result['actualDeclaredHelperReturns']);setup+=len(result['actualSetupEntryReturns'])
            fields=('registers','cpsr','pc','orderedNonstackWrites','ownedNonstackWrites','memorySha256','modelChecks','actualDeclaredHelperReturns')
            if not all(record['comparisons'].values())or any(record['original'][k]!=record['compiled'][k]for k in fields):raise ValueError('Original versus freshly compiled full registers/state/effects differ')
        own+=2*len(wanted);wrong=row['wrongC'];wrong_records=records(wrong['trace']);returned=sum(r['result']['actualOwnReturn']for r in wrong_records);rejected=sum(r['result']['actualOwnReturn']and not r['result']['modelPassed']for r in wrong_records)
        if len(wrong_records)!=len(wanted)or returned!=len(wrong_records)or(returned,rejected)!=(wrong['actualOwnReturns'],wrong['modelRejections'])or not rejected:raise ValueError('Per-unit actual returning independent wrong-source rejection missing')
        wrong_return+=returned;wrong_reject+=rejected
    linked={r['entry']:r for r in report['sourceLinkedDefinitions']}
    if len(linked)!=3 or any(linked[row['address']]['bytes']!=row['bytes']or linked[row['address']]['sha256']!=row['targetSha256']for row in matches):raise ValueError('Fresh complete source-linked receive closure missing')
    if report['initializedNullTableSourceCredit']!=0:raise ValueError('Original read-only table received source credit')
    if symbols!=report['nativeSymbols']or(own,helper,setup,wrong_return,wrong_reject)!=(report['totalActualOwnReturns'],report['totalActualDeclaredHelperReturns'],report['totalActualSetupEntryReturns'],report['totalWrongCActualReturns'],report['totalWrongCModelRejections']):raise ValueError('Measured symbol publication/actual-return totals disagree')
    return dict(functions=3,bytes=3016,actualOwnReturns=own,actualDeclaredHelperReturns=helper,actualSetupReturns=setup,wrongReturns=wrong_return,wrongModelRejections=wrong_reject)

def main(reproduce=True):
    if reproduce:
        p=subprocess.run([sys.executable,str(ROOT/'match_arm7_sdk423_beacon_probe_key_20261102.py')],cwd=ROOT.parent,capture_output=True,text=True,timeout=1800)
        if p.returncode:raise ValueError(p.stdout+p.stderr)
    report=json.loads(REPORT.read_text());positive=current(report);seeds=json.loads(linker.PROFILE.read_text())['units'];controls=[];WORK.mkdir(parents=True,exist_ok=True);originals=(linker.base.namespace,linker.base.derive_bindings,linker.base.data_binding)
    def reject(name,call):
        try:call()
        except(ValueError,FileNotFoundError)as error:controls.append(dict(name=name,rejected=True,error=str(error)));return
        raise ValueError('Negative control unexpectedly accepted:'+name)
    for seed in seeds:
        for key,value in[('processor','arm9'),('program','dwc/utility.bin/move/child.srl'),('module','arm7-boot'),('mode','thumb'),('address',hex(int(seed['address'],0)+4)),('bytes',seed['bytes']-4),('codeBytes',seed['codeBytes']+4),('base',0),('binary','inputs/rom.nds'),('sourceSha256','0'*64),('compilerSha256','0'*64),('compilerFlags',seed['compilerFlags']+['-O0']),('sourceDependencies',[]),('runtimePointerQualification',None),('initializedOriginalTables',[{}]),('nativeHelperContracts',[{}]),('nativeInterfaceContract',{}),('targetSha256','0'*64),('inputModuleSha256','0'*64),('authoritativeExclusionSnapshot',{})]:reject(seed['name']+'-wrong-'+key,lambda s=dict(seed,**{key:value}):linker.qualified(s))
    for key,value in[('matches',report['matches'][:-1]),('matchedInitializedBytes',3020),('totalActualOwnReturns',25919),('originalCalleesAndAdditionalDefinitionsCredit',84),('nativeSymbols',{}),('sourceInputsNoWorkCaches',False),('sourceReconstructionComplete',True)]:reject('publication-'+key,lambda r=dict(report,**{key:value}):current(r))
    altered=copy.deepcopy(report);altered['matches'][0]['oracle']['trace']['path']='work/arm7-bulk-20261030/sdk407-missing-native-records.json.gz';reject('missing-product-withholds-current-credit',lambda:current(altered))
    ordinary=report['matches'][0];reject('runtime-word-qualification-withheld',lambda:linker.validate(ordinary,WORK/'no-runtime-word',qualify_runtime_word=False))
    for field,value in[('offset',0),('type',2),('symbol','arbitrary_unqualified_pointer'),('sourceSymbolType','STT_OBJECT'),('explicitAddend',0),('originalEncodedWord','00000000')]:
        altered=copy.deepcopy(ordinary);altered['relocations'][0][field]=value;reject('untouched-object-relocation-'+field,lambda r=altered,n=field:linker.validate(r,WORK/('wrong-'+n)))
    for target in(0x0380fff0,0x0380fff8,0x0380fffc):reject('unchanged-unknown-data-'+hex(target),lambda t=target:originals[2](dict(program=''),t,originals[0]('')[0]))
    probe=next(r for r in report['matches']if r['name']=='RxProbeResFrame');reject('null-table-qualification-withheld',lambda:linker.validate(probe,WORK/'no-null-table',qualify_tables=False))
    for key,value in [('elements',2),('elementBytes',4),('address','0x27f74c2'),('valueSha256','0'*64),('sourceDataCredit',6)]:
        altered=copy.deepcopy(probe);altered['initializedOriginalTables'][0][key]=value;reject('null-table-'+key,lambda r=altered:linker.qualified(r))
    beacon=next(r for r in report['matches']if r['name']=='RxBeaconFrame');reject('quotient-role-withheld',lambda:linker.validate(beacon,WORK/'no-quotient',qualify_quotient=False))
    for key,value in [('symbol','_ll_sdiv'),('entry','0x3806bfc'),('sha256','0'*64),('helperSourceCredit',64)]:
        altered=copy.deepcopy(beacon);altered['nativeHelperContracts'][0][key]=value;reject('quotient-contract-'+key,lambda r=altered:linker.qualified(r))
    main_bytes=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    import match_arm7_sdk423_beacon_probe_key_20261102 as producer
    for name,changes in [('RxKeyDataFrame',[('mode',4),('offset',8),('aid',0),('aid',16),('payload',9),('stride',10)]),('RxProbeResFrame',[('mode',4),('offset',8),('state',0x100),('mask','arbitrary'),('existing','arbitrary'),('maxLength',100000)]),('RxBeaconFrame',[('mode',4),('offset',8),('period',0),('state',0x100),('bodyLength',65535)])]:
        native=producer.MODULES[name];case=native.cases()[0]
        for key,value in changes:reject(name+'-native-context-'+key+'-'+str(value),lambda n=native,c=dict(case,**{key:value}):n.run(main_bytes,wram,c,0))
        reject(name+'-partial-source-body',lambda n=native,c=case:n.run(main_bytes,wram,c,0,body=bytes(4)))
        reject(name+'-unknown-source-linked-range',lambda n=native,c=case:n.run(main_bytes,wram,c,0,body_map={0x27f284c:bytes(4)}))
    if originals!=(linker.base.namespace,linker.base.derive_bindings,linker.base.data_binding):raise ValueError('Caller-specific rule escaped success/error cleanup')
    output=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),canonicalReport=REPORT.relative_to(ROOT).as_posix(),canonicalReportSha256=sha256(REPORT),positive=positive,negativeControls=controls,negativeControlCount=len(controls),allRejected=True,allOriginalGuardsRestored=True,sourceCreditPendingIntegratorModuleAcceptance=0);write_json(CONTROLS,output);print(json.dumps(dict(reportSha256=sha256(REPORT),controls=len(controls),controlSha256=sha256(CONTROLS),positive=positive)),flush=True)

if __name__=='__main__':main()
