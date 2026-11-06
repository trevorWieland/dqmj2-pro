import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import match_runtime
import link_arm7_sdk434_intr_transmit_compiler_20261102 as linker
from project import ROOT,sha256,configuration,write_json
REPORT=ROOT/'evidence/matches/arm7-sdk436-intr-transmit-compiler1236-20261102.json'
CONTROLS=ROOT/'evidence/verification/arm7-sdk437-intr-transmit-compiler-controls-20261102.json'
WORK=ROOT/'work/arm7-bulk-20261030/sdk437-intr-transmit-controls'

def file(path,digest):
    p=(ROOT/path).resolve();p.relative_to(ROOT.resolve())
    if not p.is_file()or sha256(p)!=digest:raise ValueError('Missing or changed current source/product:'+path)

def current(report):
    if report['matchedInitializedBytes']!=1236 or report['newOrdinaryFunctionCount']!=7 or len(report['matches'])!=7 or not report['compilerOnlyEvidence']or report['evidenceClass']!='function-matched-compiler-linker-only'or not report['sourceInputsNoWorkCaches']or report['sourceReconstructionComplete']or report['wholeModuleLinked']or report['initializedDenominatorDelta']or report['originalCalleesAndAdditionalDefinitionsCredit']or report['initializedRateTableSourceCredit']:raise ValueError('Seven full compiler-only units/zero scaffold scope differs')
    for field in('totalActualOwnReturns','totalActualDeclaredHelperReturns','totalActualSetupEntryReturns','totalWrongCActualReturns'):
        if report[field]!=0:raise ValueError('Compiler-only proof cannot claim behavioral returns')
    if report['generatorSha256']!=sha256(ROOT/report['generator'])or sha256(configuration()['rom'])!=report['romSha256']:raise ValueError('Current generator/original ROM differs')
    for pin in report['generatorSources']:file(pin['path'],pin['sha256'])
    seeds=json.loads(linker.PROFILE.read_text(encoding='utf-8'))['units'];matches={r['name']:r for r in report['matches']};symbols={}
    if set(matches)!={s['name']for s in seeds}:raise ValueError('Missing/duplicate complete qualified function')
    for seed in seeds:
        row=matches[seed['name']];linker.qualified(row)
        if not row['exactBytes']or not row['exactAfterDeclaredRelocation']or not row['sourceOnlyCompilerInput']or row['originalObjectScaffolding']or not row['compilerOnlyEvidence']or row['actualOwnReturns']or row['unrecoveredCalleesAndExtraDefinitionsCredit']:raise ValueError('Complete C/compiler-only evidence differs')
        if row['oracle']!=dict(vectors=0,actualOriginalAndCompiledReturns=0,actualDeclaredHelperReturns=0,actualSetupEntryReturns=0,providerReplacements=[],behavioralReturnCredit=0):raise ValueError('Fabricated native/model evidence in compiler-only proof')
        file(row['source'],row['sourceSha256']);file(row['object'],row['objectSha256'])
        for dep in row['sourceDependencies']:file(dep['path'],dep['sha256'])
        expected=[str(ROOT/seed['compiler']),*seed['compilerFlags'],'-c',str(ROOT/seed['source']),'-o',str(ROOT/row['object'])]
        if row['command']!=expected or row['cwd']!=str(ROOT):raise ValueError('Actual source-only compiler command differs')
        link=row['realLink'];directory=(ROOT/link['lcf']).parent
        for name,digest in [('unit.lcf',link['lcfSha256']),('linked.elf',link['linkedElfSha256']),('caller.o',link['splitObjectSha256']),('caller.bin',link['linkedCallerSha256'])]:file((directory/name).relative_to(ROOT).as_posix(),digest)
        image=(ROOT/row['binary']).read_bytes();start=int(row['address'],0)-row['base'];target=image[start:start+row['bytes']]
        if not link['exactLinkedBytes']or link['sourceObjectSha256']!=row['objectSha256']or(directory/'caller.bin').read_bytes()!=target or hashlib.sha256(target).hexdigest()!=row['targetSha256']:raise ValueError('Full genuine source-linked current bytes differ')
        if link['callerSpecificQualification']['generatorSha256']!=sha256(ROOT/'link_arm7_sdk434_intr_transmit_compiler_20261102.py'):raise ValueError('Exact caller-specific role guard changed')
        if row['nativeSymbols']!={k:v['address']for k,v in link['bindings'].items()}or any(not isinstance(v,str)or not v.startswith('0x')for v in row['nativeSymbols'].values()):raise ValueError('Measured hexadecimal bindings differ')
        for name,value in row['nativeSymbols'].items():
            if name in symbols and symbols[name]!=value:raise ValueError('Conflicting measured data/function binding')
            symbols[name]=value
        scope=row['boundaryProof'];file(scope['path'],scope['sha256']);proof=json.loads((ROOT/scope['path']).read_text(encoding='utf-8'));entry=next(r for r in proof['rows']if r['module']==seed['module']and r['address']==seed['address'])
        if proof['profileSha256']!=sha256(linker.PROFILE)or proof['generatorSha256']!=sha256(ROOT/proof['generator'])or entry['bytes']!=seed['bytes']or entry['targetSha256']!=seed['targetSha256']or entry['acceptedOverlaps']or entry['interiorCanonicalStarts']or entry['externalInteriorReferences']or entry['denominatorIncrease']or entry['behavioralReturnCredit']:raise ValueError('Complete bounded canonical/reference audit changed')
        wrong=row['wrongC'];build=wrong['build'];file(build['source'],build['sourceSha256']);file(build['object'],build['objectSha256']);body=(ROOT/build['source']).parent/'caller.bin';file(body.relative_to(ROOT).as_posix(),build['linkedBodySha256']);file(((ROOT/build['source']).parent/'linked.elf').relative_to(ROOT).as_posix(),build['linkedElfSha256'])
        if not wrong['byteGateRejected']or wrong['actualOwnReturns']or wrong['behavioralReturnCredit']or body.read_bytes()==target or not build['unchangedWrongCRelocations']:raise ValueError('Fresh compiled wrong-C byte rejection missing or fabricated execution')
    if symbols!=report['nativeSymbols']or report['wrongCByteGateRejections']!=7:raise ValueError('Current measured publication totals differ')
    return dict(functions=7,bytes=1236,wrongCByteGateRejections=7,actualBehavioralReturns=0)

def main(reproduce=True):
    if reproduce:
        p=subprocess.run([sys.executable,str(ROOT/'match_arm7_sdk436_intr_transmit_compiler_20261102.py')],cwd=ROOT.parent,capture_output=True,text=True,timeout=180)
        if p.returncode:raise ValueError(p.stdout+p.stderr)
    report=json.loads(REPORT.read_text(encoding='utf-8'));positive=current(report);seeds=json.loads(linker.PROFILE.read_text(encoding='utf-8'))['units'];controls=[];WORK.mkdir(parents=True,exist_ok=True);originals=(linker.base.namespace,linker.base.derive_bindings,linker.base.data_binding)
    def reject(name,call):
        try:call()
        except(ValueError,FileNotFoundError)as e:controls.append(dict(name=name,rejected=True,error=str(e)));return
        raise ValueError('Invalid compiler-only evidence accepted:'+name)
    for seed in seeds:
        for key,value in [('processor','arm9'),('program','wrong-child-program'),('module','arm7-boot'),('mode','thumb'),('address',hex(int(seed['address'],0)+4)),('bytes',seed['bytes']-4),('sourceSha256','0'*64),('sourceDependencies',[]),('compilerFlags',seed['compilerFlags']+['-O0']),('inputModuleSha256','0'*64),('targetSha256','0'*64),('runtimePointerQualification',None),('initializedOriginalTables',[{}]),('compilerOnlyEvidence',False),('nativeInterfaceContract',{})]:reject(seed['name']+'-'+key,lambda r=dict(seed,**{key:value}):linker.qualified(r))
    for key,value in [('totalActualOwnReturns',1),('totalActualDeclaredHelperReturns',1),('totalWrongCActualReturns',1),('compilerOnlyEvidence',False),('matchedInitializedBytes',1240),('newOrdinaryFunctionCount',8),('sourceInputsNoWorkCaches',False),('initializedRateTableSourceCredit',32)]:reject('publication-'+key,lambda r=dict(report,**{key:value}):current(r))
    changed=copy.deepcopy(report);changed['matches'][0]['object']='work/arm7-bulk-20261030/sdk437-absent-object.o';reject('missing-product-withholds-credit',lambda:current(changed))
    changed=copy.deepcopy(report);changed['matches'][0]['oracle']['actualOriginalAndCompiledReturns']=2;reject('invented-native-oracle',lambda:current(changed))
    for row in report['matches']:
        if any(b['address']=='0x380fff4'for b in row['realLink']['bindings'].values()):reject(row['name']+'-runtime-role-disabled',lambda r=row:linker.validate(r,WORK/r['name']/'no-runtime',qualify_runtime_word=False))
    rate=next(r for r in report['matches']if r['name']=='SetSupRateSet');reject('rate-table-role-disabled',lambda:linker.validate(rate,WORK/'no-rate-table',qualify_tables=False))
    for key,value in [('elements',15),('elementBytes',1),('address','0x27f74d2'),('valueSha256','0'*64),('sourceDataCredit',32)]:
        changed=copy.deepcopy(rate);changed['initializedOriginalTables'][0][key]=value;reject('rate-table-'+key,lambda r=changed:linker.qualified(r))
    ordinary=report['matches'][0]
    for key,value in [('offset',0),('type',2),('symbol','unknown_unqualified_symbol'),('originalEncodedWord','00000000')]:
        changed=copy.deepcopy(ordinary);changed['relocations'][0][key]=value;reject('unchanged-relocation-'+key,lambda r=changed,k=key:linker.validate(r,WORK/('bad-'+k)))
    for address in(0x0380fff0,0x0380fff8,0x0380fffc):reject('default-data-guard-'+hex(address),lambda a=address:originals[2](dict(program=''),a,originals[0]('')[0]))
    if originals!=(linker.base.namespace,linker.base.derive_bindings,linker.base.data_binding):raise ValueError('Scoped role rules leaked after control')
    result=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),canonicalReport=REPORT.relative_to(ROOT).as_posix(),canonicalReportSha256=sha256(REPORT),positive=positive,negativeControls=controls,negativeControlCount=len(controls),allRejected=True,allOriginalGuardsRestored=True,actualBehavioralReturns=0,sourceCreditPendingIntegratorModuleAcceptance=0);write_json(CONTROLS,result);print(json.dumps(dict(controls=len(controls),sha256=sha256(CONTROLS),positive=positive)),flush=True)

if __name__=='__main__':main()
