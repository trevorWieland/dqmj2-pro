import copy
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import match_runtime
import arm7_sdk307_task_queue_native_20261102 as tasks
import arm7_sdk308_command_dispatch_native_20261102 as commands
import link_arm7_sdk311_task_command_20261102 as linker
from project import ROOT,sha256,configuration,write_json

REPORT=ROOT/'evidence/matches/arm7-sdk312-task-command-family1224-20261102.json'
CONTROLS=ROOT/'evidence/verification/arm7-sdk313-task-command-controls-20261102.json'
WORK=ROOT/'work/arm7-bulk-20261030/sdk313-task-command-controls'

def verify_file(row):
    path=(ROOT/row['path']).resolve();path.relative_to(ROOT.resolve())
    if not path.is_file()or sha256(path)!=row['sha256']:raise ValueError('Missing or changed current source/product:'+row['path'])

def records(trace):
    verify_file(dict(path=trace['path'],sha256=trace['compressedSha256']));raw=gzip.decompress((ROOT/trace['path']).read_bytes())
    if hashlib.sha256(raw).hexdigest()!=trace['rawSha256']:raise ValueError('Deterministic native evidence raw hash differs')
    return json.loads(raw)

def current(report):
    seeds=json.loads(linker.PROFILE.read_text())['units'];matches=report['matches']
    if len(matches)!=5 or report['matchedInitializedBytes']!=1224 or report['newOrdinaryFunctionCount']!=5 or report['initializedDenominatorDelta']!=0 or report['wholeModuleLinked']or report['originalTablesAndAdditionalDefinitionsSourceCredit']!=0:raise ValueError('Measured five-unit source coverage or zero scaffolding credit changed')
    if report['generatorSha256']!=sha256(ROOT/report['generator']):raise ValueError('Actual source-only generator changed')
    for pin in report['generatorSources']:verify_file(pin)
    if sha256(configuration()['rom'])!=report['romSha256']:raise ValueError('Measured original ROM identity changed')
    by_name={r['name']:r for r in matches}
    if set(by_name)!={s['name']for s in seeds}:raise ValueError('Complete qualified source identities missing/duplicated')
    total=helpers=setup=0;symbols={};expected_sources=sorted([dict(entry=seed['address'],bytes=seed['bytes'],sha256=seed['targetSha256'])for seed in seeds],key=lambda r:int(r['entry'],0))
    for seed in seeds:
        row=by_name[seed['name']];linker.qualified(row)
        if not row['exactBytes']or not row['exactAfterDeclaredRelocation']or not row['sourceOnlyCompilerInput']or row['originalObjectScaffolding']:raise ValueError('Ordinary source full-byte evidence missing')
        for path,digest in[(row['object'],row['objectSha256']),(row['source'],row['sourceSha256'])]:verify_file(dict(path=path,sha256=digest))
        for pin in row['sourceDependencies']:verify_file(pin)
        expected=[str(ROOT/seed['compiler']),*seed['compilerFlags'],'-c',str(ROOT/seed['source']),'-o',str(ROOT/row['object'])]
        if row['command']!=expected or row['cwd']!=str(ROOT):raise ValueError('Actual complete source-only compiler command differs')
        proof=row['realLink'];directory=(ROOT/proof['lcf']).parent;origin=tasks.context.base.WRAM if row['module']=='arm7-wram'else tasks.context.base.MAIN;image=(ROOT/row['binary']).read_bytes();start=int(row['address'],0)-origin;target=image[start:start+row['bytes']]
        for name,digest in[('unit.lcf',proof['lcfSha256']),('linked.elf',proof['linkedElfSha256']),('caller.o',proof['splitObjectSha256']),('caller.bin',proof['linkedCallerSha256'])]:verify_file(dict(path=(directory/name).relative_to(ROOT).as_posix(),sha256=digest))
        if not proof['exactLinkedBytes']or(directory/'caller.bin').read_bytes()!=target or hashlib.sha256(target).hexdigest()!=row['targetSha256']:raise ValueError('Full current genuinely linked native range differs')
        if proof['callerSpecificQualification']['generatorSha256']!=sha256(ROOT/'link_arm7_sdk311_task_command_20261102.py'):raise ValueError('Caller-specific data/role qualification changed')
        if row['nativeSymbols']!={k:v['address']for k,v in proof['bindings'].items()}or any(not isinstance(v,str)or not v.startswith('0x')for v in row['nativeSymbols'].values()):raise ValueError('Measured hexadecimal symbol publication differs')
        for name,value in row['nativeSymbols'].items():
            if name in symbols and symbols[name]!=value:raise ValueError('Conflicting named physical symbol')
            symbols[name]=value
        native=commands if seed['name']=='RequestCmdTask'else tasks;wanted=native.cases()if native is commands else[c for c in native.cases()if c['entry']==int(seed['address'],0)];proof_records=records(row['oracle']['trace'])
        if len(proof_records)!=len(wanted)or row['oracle']['actualOriginalAndCompiledReturns']!=2*len(wanted):raise ValueError('Complete actual-return/vector evidence missing')
        for record,case in zip(proof_records,wanted):
            if record['case']!=case:raise ValueError('Supported deterministic input order differs')
            for key in('original','compiled'):
                result=record[key]
                if not result['actualOwnReturn']or not result['modelPassed']or not all(result['modelChecks'].values())or result['providerReplacements']:raise ValueError('Independent returning provider-free state proof failed')
                if any(not r['actualReturn']for r in result['actualDeclaredHelperReturns']+result['actualSetupEntryReturns']):raise ValueError('Lower observed entry lacked its actual return')
                actual_sources=sorted(result['sourceLinkedProducers'],key=lambda r:int(r['entry'],0))
                if actual_sources!=(expected_sources if key=='compiled'else[]):raise ValueError('Five fresh linked bodies were not installed before compiled prerequisite execution')
                helpers+=len(result['actualDeclaredHelperReturns']);setup+=len(result['actualSetupEntryReturns'])
            fields=('registers','cpsr','pc','orderedNonstackWrites','ownedNonstackWrites','memorySha256','modelChecks','actualDeclaredHelperReturns')
            if not all(record['comparisons'].values())or any(record['original'][k]!=record['compiled'][k]for k in fields):raise ValueError('Original versus freshly compiled full machine/state/effects differ')
        total+=2*len(wanted)
    if symbols!=report['nativeSymbols']or(total,helpers,setup)!=(report['totalActualOwnReturns'],report['totalActualDeclaredHelperReturns'],report['totalActualSetupEntryReturns'])or total!=3626:raise ValueError('Measured symbol publication/actual-return totals disagree')
    if len(report['wrongC'])!=5:raise ValueError('Each full source routine needs its independent wrong-C control')
    for wrong in report['wrongC']:
        proof_records=records(wrong['trace']);returned=sum(r['result']['actualOwnReturn']for r in proof_records);rejected=sum(r['result']['actualOwnReturn']and not r['result']['modelPassed']for r in proof_records)
        if returned!=len(proof_records)or(returned,rejected)!=(wrong['actualOwnReturns'],wrong['modelRejections'])or not rejected:raise ValueError('Actual returning independent wrong-source rejection missing')
    return dict(functions=5,bytes=1224,actualOwnReturns=total,actualDeclaredHelperReturns=helpers,actualSetupReturns=setup,wrongReturns=sum(r['actualOwnReturns']for r in report['wrongC']),wrongModelRejections=sum(r['modelRejections']for r in report['wrongC']))

def main():
    process=subprocess.run([sys.executable,str(ROOT/'match_arm7_sdk312_task_command_family_20261102.py')],cwd=ROOT.parent,capture_output=True,text=True,timeout=420)
    if process.returncode:raise ValueError(process.stdout+process.stderr)
    report=json.loads(REPORT.read_text());positive=current(report);seeds=json.loads(linker.PROFILE.read_text())['units'];controls=[];WORK.mkdir(parents=True,exist_ok=True);originals=(linker.base.namespace,linker.base.derive_bindings,linker.base.data_binding)
    def reject(name,call):
        try:call()
        except(ValueError,FileNotFoundError)as error:controls.append(dict(name=name,rejected=True,error=str(error)));return
        raise ValueError('Negative control unexpectedly accepted:'+name)
    for seed in seeds:
        for key,value in[('processor','arm9'),('program','dwc/utility.bin/move/child.srl'),('module','arm7-boot'),('mode','thumb'),('address',hex(int(seed['address'],0)+4)),('bytes',seed['bytes']-4),('sourceSha256','0'*64),('compilerSha256','0'*64),('compilerFlags',seed['compilerFlags']+['-O0']),('sourceDependencies',[]),('runtimePointerQualification',None),('initializedOriginalTables',[{}]),('nativeInterfaceContract',{}),('targetSha256','0'*64),('inputModuleSha256','0'*64)]:reject(seed['name']+'-wrong-'+key,lambda s=dict(seed,**{key:value}):linker.qualified(s))
    for key,value in[('matches',report['matches'][:-1]),('matchedInitializedBytes',1328),('totalActualOwnReturns',3625),('originalTablesAndAdditionalDefinitionsSourceCredit',96),('nativeSymbols',{})]:reject('publication-'+key,lambda r=dict(report,**{key:value}):current(r))
    altered=copy.deepcopy(report);altered['matches'][0]['oracle']['trace']['path']='work/arm7-bulk-20261030/sdk313-missing-native-records.json.gz';reject('missing-product-withholds-current-credit',lambda:current(altered))
    ordinary=next(r for r in report['matches']if r['name']=='AddTask');initializer=next(r for r in report['matches']if r['name']=='InitializeTask');command=next(r for r in report['matches']if r['name']=='RequestCmdTask')
    reject('runtime-word-qualification-withheld',lambda:linker.validate(ordinary,WORK/'no-runtime-word',qualify_runtime_word=False));reject('initialized-function-table-qualification-withheld',lambda:linker.validate(initializer,WORK/'no-task-table',qualify_tables=False));reject('initialized-command-tables-qualification-withheld',lambda:linker.validate(command,WORK/'no-command-tables',qualify_tables=False))
    for field,value in[('offset',0),('type',2),('symbol','arbitrary_unqualified_pointer'),('sourceSymbolType','STT_OBJECT'),('explicitAddend',0),('originalEncodedWord','00000000')]:
        altered=copy.deepcopy(ordinary);altered['relocations'][0][field]=value;reject('untouched-object-relocation-'+field,lambda r=altered,n=field:linker.validate(r,WORK/('wrong-'+n)))
    for target in(0x0380fff0,0x0380fff8,0x0380fffc):reject('unchanged-unknown-data-'+hex(target),lambda t=target:originals[2](dict(program=''),t,originals[0]('')[0]))
    main_bytes=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();case=next(c for c in tasks.cases()if c['entry']==0x037f8598)
    for key,value in[('priority',-1),('priority',4),('task',24),('task',0xffffffff)]:reject('source-contract-'+key+'-'+str(value),lambda c=dict(case,**{key:value}):tasks.run(main_bytes,wram,c,0))
    command_case=next(c for c in commands.cases()if not c['busy']and c['requests']and not c['diag']and not c['mismatch'])
    for group,table in commands.TABLES.items():reject('withheld-physical-table-equality-'+hex(group),lambda c=dict(command_case,code=group+table[1]):commands.classification(main_bytes,c))
    reject('unmodeled-real-asynchronous-handler',lambda:commands.classification(main_bytes,dict(command_case,code=0,state=32,requestLength=1,confirmLength=1)))
    if originals!=(linker.base.namespace,linker.base.derive_bindings,linker.base.data_binding):raise ValueError('Caller-specific rule escaped success/error cleanup')
    output=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),canonicalReport=REPORT.relative_to(ROOT).as_posix(),canonicalReportSha256=sha256(REPORT),positive=positive,negativeControls=controls,negativeControlCount=len(controls),allRejected=True,allOriginalGuardsRestored=True,sourceCreditPendingIntegratorModuleAcceptance=0);write_json(CONTROLS,output);print(json.dumps(dict(reportSha256=sha256(REPORT),controls=len(controls),controlSha256=sha256(CONTROLS),positive=positive)),flush=True)

if __name__=='__main__':main()
