import hashlib
import json
from project import ROOT,sha256
REFERENCE=ROOT/'provenance/arm7-host-callee-word-context-v3-20261101.json'
REFERENCE_SHA='8b461e8c759fc3a43982fa197c3f0a58e6fcd2094375229bf71803f8ec5ca759'
EXPECTED={'writer':(0x03804c00,88,2,0x03804c00),'reader':(0x03804c7c,116,1,0x03804c7c),'transfer':(0x03804c58,36,1,0x03804c58),'owner-tail':(0x03806390,40,1,0x037fbb78)}

def validate(ref):
    if ref['schemaVersion']!=3 or ref['sourceCredit']!=0 or ref['acceptedSourceOverridesPermitted']or not ref['qualifiedHostOnly']:raise ValueError('Draft-only host context policy differs')
    if len(ref['proofs'])!=4 or {p['kind']for p in ref['proofs']}!=set(EXPECTED):raise ValueError('Exact four scoped callee proofs required')
    result={}
    for proof in ref['proofs']:
        address,size,words,callee=EXPECTED[proof['kind']]
        if int(proof['calleeAddress'],0)!=callee or proof['semanticWords']!=words:raise ValueError('Exact demonstrated word contract differs')
        for name,hashkey in [('proofReport','proofReportSha256'),('controls','controlsSha256'),('proofGenerator','proofGeneratorSha256')]:
            path=(ROOT/proof[name]).resolve()
            if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=proof[hashkey]:raise ValueError('Current complete source/native/control proof missing or changed')
        report=json.loads((ROOT/proof['proofReport']).read_text());control=json.loads((ROOT/proof['controls']).read_text());row=next((x for x in report['matches']if int(x['address'],0)==address),None)
        if row is None or any(row[k]!=value for k,value in proof['nativeRowIdentity'].items()):raise ValueError('Complete native/source qualified identity differs')
        if row['processor']!='arm7'or row['program']or row['module']!='arm7-wram'or row['mode']!='arm'or row['bytes']!=size:raise ValueError('Wrong processor/program/module/mode/bounds')
        if report['generatorSha256']!=proof['proofGeneratorSha256']or control['inputReportSha256']!=proof['proofReportSha256']or not control['restoredPositive']or control['additionalSourceCredit']!=0:raise ValueError('Source-native controls no longer qualify proof')
        for item in [dict(path=row['source'],sha256=row['sourceSha256']),*row['sourceDependencies']]:
            if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError('Current typed C/header differs')
        raw=(ROOT/row['binary']).read_bytes();offset=address-row['base']
        if hashlib.sha256(raw).hexdigest()!=row['inputModuleSha256']or hashlib.sha256(raw[offset:offset+size]).hexdigest()!=row['targetSha256']:raise ValueError('Original full module/function changed')
        if not row['exactBytes']or not row['exactAfterDeclaredRelocation']or not row['sourceOnlyCompilerInput']or row['originalObjectScaffolding']:raise ValueError('Complete source-only native/link gate absent')
        if proof['kind']=='owner-tail':
            tail=row['oracle']['tailWitness']
            if int(tail['qualifyingEntry'],0)!=callee or not tail['callerWordComparedWithoutNarrowing']or tail['ownerFieldReadWidth']!=2 or tail['fixedFlag']!=1 or row['oracle']['actualOriginalAndCompiledReturns']!=1680:raise ValueError('Full inherited owner-word/tail-chain witness differs')
        elif row['sourceAbiContract']['physicalArgumentWords']!=words:raise ValueError('Actual typed callee argument count differs')
        result[callee]=words
    return result

def apply(child,program):
    if program:return dict(applied=False,reason='Host callee context excluded from utility-child namespace',sourceCredit=0)
    if sha256(REFERENCE)!=REFERENCE_SHA:raise ValueError('Frozen callee-context reference changed')
    words=validate(json.loads(REFERENCE.read_text()));child.ARGUMENTS['arm7'].update(words)
    return dict(applied=True,reference=REFERENCE.relative_to(ROOT).as_posix(),referenceSha256=REFERENCE_SHA,qualifiedWordCounts={hex(k):v for k,v in words.items()},sourceCredit=0,acceptedSourcesChanged=False,returnTypesOrPointersInferred=False)
