import copy
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import match_runtime
import arm7_sdk401_cam_bootstrap_native_20261102 as receive
import compile_arm7_sdk386_receive_data_20261102 as helper_compiler
import link_arm7_sdk403_cam_bootstrap_20261102 as linker
from project import ROOT,sha256,configuration,write_json

REPORT=ROOT/'evidence/matches/arm7-sdk405-cam-bootstrap292-20261102.json'
CONTROLS=ROOT/'evidence/verification/arm7-sdk407-cam-bootstrap-controls-20261102.json'
WORK=ROOT/'work/arm7-bulk-20261030/sdk407-cam-bootstrap-controls'

def verify_file(row):
    path=(ROOT/row['path']).resolve();path.relative_to(ROOT.resolve())
    if not path.is_file()or sha256(path)!=row['sha256']:raise ValueError('Missing or changed current source/product:'+row['path'])

def records(trace):
    verify_file(dict(path=trace['path'],sha256=trace['compressedSha256']));raw=gzip.decompress((ROOT/trace['path']).read_bytes())
    if hashlib.sha256(raw).hexdigest()!=trace['rawSha256']:raise ValueError('Deterministic raw native records changed')
    return json.loads(raw)

def current(report):
    seeds=json.loads(linker.PROFILE.read_text())['units'];matches=report['matches']
    if len(matches)!=2 or report['matchedInitializedBytes']!=292 or report['newOrdinaryFunctionCount']!=2 or report['initializedDenominatorDelta']!=0 or report['wholeModuleLinked']or report['originalCalleesAndAdditionalDefinitionsCredit']!=0 or report['totalActualOwnReturns']!=576:raise ValueError('Two complete ordinary-source units/zero scaffolding/actual-return summary changed')
    if report['generatorSha256']!=sha256(ROOT/report['generator']):raise ValueError('Actual source-only generator changed')
    for pin in report['generatorSources']:verify_file(pin)
    if sha256(configuration()['rom'])!=report['romSha256']:raise ValueError('Measured original ROM identity changed')
    by_name={r['name']:r for r in matches}
    if set(by_name)!={s['name']for s in seeds}:raise ValueError('Complete qualified source identities missing or duplicated')
    own=helper=setup=wrong_return=wrong_reject=0;symbols={}
    for seed in seeds:
        row=by_name[seed['name']];linker.qualified(row)
        if not row['exactBytes']or not row['exactAfterDeclaredRelocation']or not row['sourceOnlyCompilerInput']or row['originalObjectScaffolding']or row['unrecoveredCalleesAndExtraDefinitionsCredit']!=0:raise ValueError('Full ordinary-source byte evidence/zero dependency credit missing')
        for path,digest in[(row['object'],row['objectSha256']),(row['source'],row['sourceSha256'])]:verify_file(dict(path=path,sha256=digest))
        for pin in row['sourceDependencies']:verify_file(pin)
        expected=[str(ROOT/seed['compiler']),*seed['compilerFlags'],'-c',str(ROOT/seed['source']),'-o',str(ROOT/row['object'])]
        if row['command']!=expected or row['cwd']!=str(ROOT):raise ValueError('Actual complete source-only compiler command differs')
        proof=row['realLink'];directory=(ROOT/proof['lcf']).parent;image=(ROOT/row['binary']).read_bytes();start=int(row['address'],0)-seed['base'];target=image[start:start+row['bytes']]
        for name,digest in[('unit.lcf',proof['lcfSha256']),('linked.elf',proof['linkedElfSha256']),('caller.o',proof['splitObjectSha256']),('caller.bin',proof['linkedCallerSha256'])]:verify_file(dict(path=(directory/name).relative_to(ROOT).as_posix(),sha256=digest))
        if not proof['exactLinkedBytes']or(directory/'caller.bin').read_bytes()!=target or hashlib.sha256(target).hexdigest()!=row['targetSha256']:raise ValueError('Complete current genuine linked range differs')
        if proof['callerSpecificQualification']['generatorSha256']!=sha256(ROOT/'link_arm7_sdk403_cam_bootstrap_20261102.py'):raise ValueError('Exact caller data/role qualification changed')
        if row['nativeSymbols']!={k:v['address']for k,v in proof['bindings'].items()}or any(not isinstance(v,str)or not v.startswith('0x')for v in row['nativeSymbols'].values()):raise ValueError('Measured hexadecimal symbol publication differs')
        for name,value in row['nativeSymbols'].items():
            if name in symbols and symbols[name]!=value:raise ValueError('Conflicting named physical symbol')
            symbols[name]=value
        layout=row['abiLayoutProof'];verify_file(dict(path=layout['source'],sha256=layout['sourceSha256']));verify_file(dict(path=layout['object'],sha256=layout['objectSha256']))
        import match_arm7_sdk405_cam_bootstrap_20261102 as producer
        indices=list(range(len(producer.FIELDS)))
        if layout['expressions']!=[producer.FIELDS[i]for i in indices]or layout['values']!=[producer.VALUES[i]for i in indices]:raise ValueError('Full compatible primitive/frame/context/alarm layout missing')
        module=receive;wanted=[c for c in module.cases()if c['entry']==int(seed['address'],0)];proof_records=records(row['oracle']['trace'])
        if len(proof_records)!=len(wanted)or row['oracle']['actualOriginalAndCompiledReturns']!=2*len(wanted):raise ValueError('Complete actual-return/vector evidence missing')
        for record,case in zip(proof_records,wanted):
            if record['case']!=case:raise ValueError('Supported deterministic input order differs')
            for key in('original','compiled'):
                result=record[key]
                if not result['actualOwnReturn']or not result['modelPassed']or not all(result['modelChecks'].values())or result['providerReplacements']:raise ValueError('Independent returning provider-free state proof failed')
                if any(not r['actualReturn']for r in result['actualDeclaredHelperReturns']+result['actualSetupEntryReturns']):raise ValueError('Observed helper/setup lacked actual return')
                helper+=len(result['actualDeclaredHelperReturns']);setup+=len(result['actualSetupEntryReturns'])
            source_helper=record['compiled']['sourceLinkedHelper']
            if len(source_helper)!=1 or source_helper[0]['entry']!='0x27ec5a4'or source_helper[0]['bytes']!=228 or source_helper[0]['sha256']!=report['sourceLinkedInitializerDefinition']['sha256']:raise ValueError('Fresh complete source-linked initializer missing')
            fields=('registers','cpsr','pc','orderedNonstackWrites','ownedNonstackWrites','memorySha256','modelChecks','actualDeclaredHelperReturns')
            if not all(record['comparisons'].values())or any(record['original'][k]!=record['compiled'][k]for k in fields):raise ValueError('Original versus freshly compiled full registers/state/effects differ')
        own+=2*len(wanted);wrong=row['wrongC'];wrong_records=records(wrong['trace']);returned=sum(r['result']['actualOwnReturn']for r in wrong_records);rejected=sum(r['result']['actualOwnReturn']and not r['result']['modelPassed']for r in wrong_records)
        if len(wrong_records)!=len(wanted)or returned!=len(wrong_records)or(returned,rejected)!=(wrong['actualOwnReturns'],wrong['modelRejections'])or not rejected:raise ValueError('Per-unit actual returning independent wrong-source rejection missing')
        wrong_return+=returned;wrong_reject+=rejected
    hp=report['sourceLinkedInitializerDefinition'];hr=hp['row'];helper_compiler.linker.qualified(hr);verify_file(dict(path=hr['object'],sha256=hr['objectSha256']));verify_file(dict(path=hp['bodyPath'],sha256=hp['sha256']))
    expected=[str(ROOT/hr['compiler']),*hr['compilerFlags'],'-c',str(ROOT/hr['source']),'-o',str(ROOT/hr['object'])]
    if hr['command']!=expected or hr['cwd']!=str(ROOT):raise ValueError('Source-linked initializer actual compile command differs')
    hl=hp['realLink'];hd=(ROOT/hl['lcf']).parent
    for name,digest in[('unit.lcf',hl['lcfSha256']),('linked.elf',hl['linkedElfSha256']),('caller.o',hl['splitObjectSha256']),('caller.bin',hl['linkedCallerSha256'])]:verify_file(dict(path=(hd/name).relative_to(ROOT).as_posix(),sha256=digest))
    if not hl['exactLinkedBytes']or hl['sourceObjectSha256']!=hr['objectSha256']:raise ValueError('Genuine source-linked initializer object/link evidence differs')
    if hp['additionalCredit']!=0 or hp['sha256']!=hr['targetSha256']or (ROOT/hp['bodyPath']).read_bytes()!=(ROOT/hr['binary']).read_bytes()[0xc5a4:0xc688]:raise ValueError('Exact source-linked helper or zero duplicate credit changed')
    if report['initializedBroadcastTableSourceCredit']!=0:raise ValueError('Original read-only table received source credit')
    if symbols!=report['nativeSymbols']or(own,helper,setup,wrong_return,wrong_reject)!=(report['totalActualOwnReturns'],report['totalActualDeclaredHelperReturns'],report['totalActualSetupEntryReturns'],report['totalWrongCActualReturns'],report['totalWrongCModelRejections']):raise ValueError('Measured symbol publication/actual-return totals disagree')
    return dict(functions=2,bytes=292,actualOwnReturns=own,actualDeclaredHelperReturns=helper,actualSetupReturns=setup,wrongReturns=wrong_return,wrongModelRejections=wrong_reject)

def main():
    p=subprocess.run([sys.executable,str(ROOT/'match_arm7_sdk405_cam_bootstrap_20261102.py')],cwd=ROOT.parent,capture_output=True,text=True,timeout=600)
    if p.returncode:raise ValueError(p.stdout+p.stderr)
    report=json.loads(REPORT.read_text());positive=current(report);seeds=json.loads(linker.PROFILE.read_text())['units'];controls=[];WORK.mkdir(parents=True,exist_ok=True);originals=(linker.base.namespace,linker.base.derive_bindings,linker.base.data_binding)
    def reject(name,call):
        try:call()
        except(ValueError,FileNotFoundError)as error:controls.append(dict(name=name,rejected=True,error=str(error)));return
        raise ValueError('Negative control unexpectedly accepted:'+name)
    for seed in seeds:
        for key,value in[('processor','arm9'),('program','dwc/utility.bin/move/child.srl'),('module','arm7-boot'),('mode','thumb'),('address',hex(int(seed['address'],0)+4)),('bytes',seed['bytes']-4),('codeBytes',seed['codeBytes']+4),('base',0),('binary','inputs/rom.nds'),('sourceSha256','0'*64),('compilerSha256','0'*64),('compilerFlags',seed['compilerFlags']+['-O0']),('sourceDependencies',[]),('runtimePointerQualification',None),('initializedOriginalTables',[{}]),('nativeInterfaceContract',{}),('targetSha256','0'*64),('inputModuleSha256','0'*64),('authoritativeExclusionSnapshot',{})]:reject(seed['name']+'-wrong-'+key,lambda s=dict(seed,**{key:value}):linker.qualified(s))
    for key,value in[('matches',report['matches'][:-1]),('matchedInitializedBytes',296),('totalActualOwnReturns',575),('originalCalleesAndAdditionalDefinitionsCredit',84),('nativeSymbols',{})]:reject('publication-'+key,lambda r=dict(report,**{key:value}):current(r))
    altered=copy.deepcopy(report);altered['matches'][0]['oracle']['trace']['path']='work/arm7-bulk-20261030/sdk407-missing-native-records.json.gz';reject('missing-product-withholds-current-credit',lambda:current(altered))
    ordinary=report['matches'][0];reject('runtime-word-qualification-withheld',lambda:linker.validate(ordinary,WORK/'no-runtime-word',qualify_runtime_word=False))
    for field,value in[('offset',0),('type',2),('symbol','arbitrary_unqualified_pointer'),('sourceSymbolType','STT_OBJECT'),('explicitAddend',0),('originalEncodedWord','00000000')]:
        altered=copy.deepcopy(ordinary);altered['relocations'][0][field]=value;reject('untouched-object-relocation-'+field,lambda r=altered,n=field:linker.validate(r,WORK/('wrong-'+n)))
    for target in(0x0380fff0,0x0380fff8,0x0380fffc):reject('unchanged-unknown-data-'+hex(target),lambda t=target:originals[2](dict(program=''),t,originals[0]('')[0]))
    initializer=next(r for r in report['matches']if r['name']=='InitializeCAM');reject('broadcast-table-qualification-withheld',lambda:linker.validate(initializer,WORK/'no-broadcast-table',qualify_tables=False))
    for key,value in [('elements',2),('elementBytes',4),('address','0x27f74b2'),('valueSha256','0'*64),('sourceDataCredit',6)]:
        altered=copy.deepcopy(initializer);altered['initializedOriginalTables'][0][key]=value;reject('broadcast-table-'+key,lambda r=altered:linker.qualified(r))
    main_bytes=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();case=receive.cases()[0]
    for key,value in[('entry',0),('mode',4),('offset',8),('maximum',0),('maximum',5),('support',65536)]:reject('native-bootstrap-context-'+key+'-'+str(value),lambda c=dict(case,**{key:value}):receive.run(main_bytes,wram,c,0))
    reject('partial-bootstrap-body',lambda:receive.run(main_bytes,wram,case,0,body=bytes(4)))
    reject('partial-source-linked-initializer',lambda:receive.run(main_bytes,wram,case,0,compiled_helper=bytes(224)))
    if originals!=(linker.base.namespace,linker.base.derive_bindings,linker.base.data_binding):raise ValueError('Caller-specific rule escaped success/error cleanup')
    output=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),canonicalReport=REPORT.relative_to(ROOT).as_posix(),canonicalReportSha256=sha256(REPORT),positive=positive,negativeControls=controls,negativeControlCount=len(controls),allRejected=True,allOriginalGuardsRestored=True,sourceCreditPendingIntegratorModuleAcceptance=0);write_json(CONTROLS,output);print(json.dumps(dict(reportSha256=sha256(REPORT),controls=len(controls),controlSha256=sha256(CONTROLS),positive=positive)),flush=True)

if __name__=='__main__':main()
