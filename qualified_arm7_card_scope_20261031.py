from contextlib import contextmanager
from pathlib import Path
import link_arm7_bulk_20261030 as linker
import prove_arm7_lane_card_callbacks_scope_20261031 as scope
from project import ROOT,read_json,write_json,sha256

MANIFEST='provenance/arm7-lane-card-callback-scope-handoff-20261031.json'
MANIFEST_SHA='ebccf9f39cbe3ee3b23bd8e98f8c65e381c3c36ed1f4a9f19b3fb83ddc7b5fa5'
REPORT='evidence/arm7/lane-card-callback-scope-20261031.json'
REPORT_SHA='762a389d613559fa4216031db86a72fda3fad9a327d443e33347efe6131f2258'
BASE_NAMESPACE=linker.namespace
REFERENCE=dict(path=REPORT,sha256=REPORT_SHA)


def inventory():
    if sha256(ROOT/MANIFEST)!=MANIFEST_SHA or sha256(ROOT/REPORT)!=REPORT_SHA:
        raise ValueError('Qualified callback manifest or native execution witness differs')
    for pin in read_json(ROOT/MANIFEST)['files']:
        path=(ROOT/pin['path']).resolve()
        if not path.is_relative_to(ROOT) or sha256(path)!=pin['sha256']:
            raise ValueError('Frozen callback boundary/source witness changed')
    raw=(ROOT/scope.MODULE).read_bytes();rows=scope.qualify(raw);report=read_json(ROOT/REPORT)
    if report['candidateRanges']!=rows or report['actualDirectCallbackReturns']!=360 or report['actualIndirectCallbackReturns']!=12:
        raise ValueError('Callback ranges or actual return witness differs')
    if report['initializedDenominatorBytesAdded'] or report['newSourceCredit']:
        raise ValueError('Boundary witness acquired source or denominator credit')
    modules,functions=BASE_NAMESPACE('')
    for row in rows:
        address=int(row['address'],0)
        if address in functions or row['module'] not in modules or row['processor']!='arm7' or row['program'] or row['mode']!='arm':
            raise ValueError('Callback supplement conflicts with the original namespace')
    return rows


def guard(entry):
    if entry.get('processor')!='arm7' or entry.get('program','')!='' or entry.get('module')!='arm7-wram' or entry.get('mode')!='arm':
        raise ValueError('Qualified callback extension is host ARM7 WRAM ARM only')
    if entry.get('qualifiedCanonicalScope')!=REFERENCE:
        raise ValueError('Explicit hash-qualified canonical scope reference required')
    rows=inventory();address=int(entry['address'],0)
    matches=[row for row in rows if int(row['address'],0)==address]
    if matches:
        row=matches[0]
        if entry['bytes']!=row['bytes'] or entry.get('codeBytes',row['instructionBytes'])!=row['instructionBytes'] or entry['targetSha256']!=row['sourceSha256'] or entry['inputModuleSha256']!=scope.MODULE_HASH:
            raise ValueError('Qualified complete callback extent or original module differs')
    elif address not in BASE_NAMESPACE('')[1]:
        raise ValueError('Entry is outside original and specifically qualified scopes')
    return rows


def namespace(program):
    modules,functions=BASE_NAMESPACE(program)
    if program:return modules,functions
    for row in inventory():
        address=int(row['address'],0)
        functions[address]=dict(program='',processor='arm7',module='arm7-wram',mode='arm',kind='function',address=hex(address),
            boundarySource='hash-qualified-native-callback-entry-20261031',canonicalScopeEvidence=REFERENCE)
    return modules,functions


@contextmanager
def installed(entry):
    guard(entry)
    if linker.namespace is not BASE_NAMESPACE:
        raise ValueError('Another namespace override is already installed')
    linker.namespace=namespace
    try:yield
    finally:linker.namespace=BASE_NAMESPACE


def validate(entry,directory):
    with installed(entry):proof=linker.validate(entry,directory)
    proof['qualifiedCanonicalScope']=dict(REFERENCE,manifest=MANIFEST,manifestSha256=MANIFEST_SHA,
        adapter='qualified_arm7_card_scope_20261031.py',adapterSha256=sha256(__file__),legacyInventoryUnchanged=True,
        legacyLinkerUnchanged=True,additionalBoundaryBytes=244,additionalInitializedDenominatorBytes=0)
    write_json(Path(directory)/'qualified-proof.json',proof)
    return proof


def main():
    rows=inventory();controls=[]
    for row in rows:
        entry=dict(processor='arm7',program='',module='arm7-wram',mode='arm',address=row['address'],bytes=row['bytes'],
            targetSha256=row['sourceSha256'],inputModuleSha256=scope.MODULE_HASH,qualifiedCanonicalScope=REFERENCE)
        guard(entry)
        for change in [dict(processor='arm9'),dict(program='utility-child'),dict(mode='thumb'),dict(module='arm7-main'),
            dict(address=hex(int(row['address'],0)+4)),dict(bytes=row['bytes']-4),dict(codeBytes=row['instructionBytes']-4),dict(targetSha256='0'*64),dict(qualifiedCanonicalScope={})]:
            try:guard(dict(entry,**change))
            except ValueError:controls.append(dict(address=row['address'],change=change,rejected=True))
            else:raise AssertionError('Unqualified callback request accepted')
    write_json(ROOT/'evidence/verification/qualified-arm7-card-scope-controls-20261031.json',dict(sourceCredit=0,
        qualifiedBoundaries=rows,positiveScopeGuards=3,negativeScopeGuards=controls,passed=True,generatorSha256=sha256(__file__),
        limitations=['Canonical boundary extension only; every C body still requires genuine linking, isolated native validation and integrator acceptance']))
    print(dict(qualifiedEntries=3,negativeGuards=len(controls),sourceCredit=0))


if __name__=='__main__':main()
