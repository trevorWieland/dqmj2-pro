import argparse
import copy
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
import sys


sys.dont_write_bytecode=True
import registered_input_path_context_v1_20261107 as adapter
OUT=Path(__file__).resolve().parent
ROOT=next(parent for parent in(OUT,*OUT.parents)if(parent/'.git').exists())
assert(ROOT/'recovery.json').is_file()


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args()
    contract=json.loads((OUT/adapter.CONTRACT).read_bytes());adapter.validate_contract(contract)
    records=[contract[k]for k in['helper','test','originalVerifier','registry','preferences','canonicalSource']]+contract['evidenceViews']+contract['proofInputs']
    local_support={contract['helper']['path']:OUT/contract['helper']['path'],contract['test']['path']:OUT/contract['test']['path'],adapter.CONTRACT:OUT/adapter.CONTRACT}
    data={r['path']:(local_support.get(r['path'],ROOT/r['path'])).read_bytes()for r in records};data[adapter.CONTRACT]=(OUT/adapter.CONTRACT).read_bytes()
    revision='5e97a8125054eed098cd66d380fece19b39d993d'
    prepared=adapter.prepare(contract,data.get,data.get,revision)
    assert prepared['report']['ready']and prepared['report']['inputsChecked']==25
    tests=[]
    def passed(name):tests.append(dict(case=name,passed=True))
    def rejected(name,call,exception=ValueError):
        try:call()
        except exception:passed(name)
        else:raise AssertionError(name)
    names=sorted(prepared['documents']);snapshot=copy.deepcopy(prepared['documents'])
    def scenario(selected=None,mutation=None,action=None,prior_error=False):
        selected=names if selected is None else selected;calls=[];queries=[];shadow={'sourceOnlyCompilerInput':'preserved-qualified-report'}
        def base_reader(path):
            name=Path(path).relative_to(ROOT).as_posix();calls.append(('base',name))
            if name=='unrelated-projected.json':return shadow
            return prepared['documents'][name]
        def then_reader(path):
            calls.append(('then-current',Path(path).name))
            if prior_error:raise RuntimeError('authored-prior-reader-stop')
            value=base_reader(path)
            if mutation and Path(path).relative_to(ROOT).as_posix()==names[0]:value=mutation(copy.deepcopy(value))
            return value
        module=SimpleNamespace(read_json=base_reader)
        def original_main():
            paths={adapter.CANON:adapter.SOURCE_SHA}
            if action=='early-error':raise RuntimeError('authored-original-stop')
            for name in selected:
                value=module.read_json(ROOT/name)['previous'];path=value['source'];digest=value['sourceSha256']
                if action=='collision':paths[adapter.CANON]='0'*64
                if path in paths and paths[path]!=digest:raise ValueError('original V8 alias collision')
                paths[path]=digest
            assert module.read_json(ROOT/'unrelated-projected.json')is shadow
            queries.extend(sorted(paths))
            if action=='late-error':raise RuntimeError('authored-original-stop')
            if action=='reader-tamper':module.read_json=base_reader
            if action=='main-tamper':module.main=lambda:None
            return dict(passed=True,sourceCredit=0,registeredRepositoryPathsChecked=21437+len(paths))
        module.main=original_main;result=None;proof=None
        try:
            with adapter.installed(module,prepared,ROOT)as proof:
                module.read_json=then_reader
                try:
                    if action=='fabricated-proof-event':proof['events'].append(dict(path=names[-1]))
                    result=module.main()
                    if action=='twice':module.main()
                finally:module.read_json=base_reader
        finally:assert module.main is original_main and module.read_json is base_reader
        assert prepared['documents']==snapshot
        return result,proof,calls,queries
    result,proof,calls,queries=scenario();adapter.validate_accounting(result,contract)
    assert proof['passed']and len(proof['events'])==7 and queries==[adapter.CANON]
    assert len([v for v in calls if v[0]=='then-current'])==8
    assert all(e['before']==adapter.RAW and e['after']==adapter.CANON and e['allOtherFieldsIdentical']for e in proof['events'])
    passed('seven-distinct-views-canonical-one-blob-nested-V14-reader-preserved')
    passed('unrelated-projected-read-object-identity-preserved')
    passed('all-seven-source-document-objects-unchanged')
    for name,selected in[('no-events',[]),('missing-one-view',names[:-1]),('duplicate-view',names+[names[0]])]:rejected(name,lambda selected=selected:scenario(selected))
    rejected('public-proof-events-cannot-fabricate-seventh-view',lambda:scenario(names[:-1],action='fabricated-proof-event'))
    for action in['collision','reader-tamper','main-tamper','twice']:rejected(action,lambda action=action:scenario(action=action))
    for action in['early-error','late-error']:rejected(action,lambda action=action:scenario(action=action),RuntimeError)
    rejected('prior-reader-exception-is-not-suppressed',lambda:scenario(prior_error=True),RuntimeError)
    def metadata_change(document):document['newByteCredit']=1;return document
    def typed_metadata_change(document):document['newByteCredit']=False;return document
    def path_change(document):document['previous']['source']='src/elsewhere.c';return document
    def hash_change(document):document['previous']['sourceSha256']='0'*64;return document
    for name,mutation in[('prior-metadata-changed',metadata_change),('prior-metadata-type-changed',typed_metadata_change),('prior-source-path-changed',path_change),('prior-source-hash-changed',hash_change)]:rejected(name,lambda mutation=mutation:scenario(mutation=mutation))
    module=SimpleNamespace(main=lambda:None,read_json=lambda p:None);old_main=module.main;old_reader=module.read_json
    def no_call():
        with adapter.installed(module,prepared,ROOT):pass
    rejected('context-without-V8-call',no_call);assert module.main is old_main and module.read_json is old_reader
    for name,mutate in[
        ('wrong-contract-source',lambda c:c['canonicalSource'].update(path='src/elsewhere.c')),
        ('wrong-contract-source-hash',lambda c:c['canonicalSource'].update(sha256='0'*64)),
        ('omitted-proof-input',lambda c:c['proofInputs'].pop()),
        ('proof-SHA-changed',lambda c:c['proofInputs'][0].update(sha256='0'*64)),
        ('duplicate-evidence-binding',lambda c:c['evidenceViews'].append(c['evidenceViews'][0])),
        ('wrong-V8',lambda c:c['originalVerifier'].update(sha256='0'*64)),
        ('wrong-registry',lambda c:c['registry'].update(sha256='0'*64)),
        ('wrong-accounting-contract',lambda c:c['expectedAccounting'].update(canonicalRegisteredPaths=21439))]:
        value=copy.deepcopy(contract);mutate(value);rejected(name,lambda value=value:adapter.validate_contract(value))
    for name in[adapter.CANON,contract['proofInputs'][0]['path']]:
        altered=dict(data);altered[name]=data[name]+b'X';rejected('wrong-current-bytes-'+name,lambda altered=altered:adapter.prepare(contract,altered.get,data.get,revision))
        altered=dict(data);altered[name]=data[name]+b'X';rejected('wrong-committed-bytes-'+name,lambda altered=altered:adapter.prepare(contract,data.get,altered.get,revision))
    pending=dict(data)
    for record in contract['proofInputs']:pending.pop(record['path'])
    blocked=adapter.prepare(contract,data.get,pending.get,revision)
    assert not blocked['report']['ready']and len(blocked['report']['missingCommitted'])==11
    def install_pending():
        with adapter.installed(module,blocked,ROOT):pass
    rejected('uncommitted-proof-packaging-cannot-activate',install_pending)
    passed('pending-eleven-input-report-is-explicit')
    for name in['../escape','src\\unexpected.c','C:/elsewhere','bad\nline','','.','a//b','./a','bad\0name']:rejected('unsafe-path-'+repr(name),lambda name=name:adapter.safe(name))
    for name,changes in[('raw-alias-count-not-deduplicated',dict(registeredRepositoryPathsChecked=21439)),('nonzero-credit',dict(sourceCredit=1)),('underlying-audit-failed',dict(passed=False))]:
        value=dict(result);value.update(changes);rejected(name,lambda value=value:adapter.validate_accounting(value,contract))
    assert prepared['documents']==snapshot
    qualification=dict(status='pure-metadata-and-binding-tests-pass',tests=tests,counts=dict(total=len(tests),evidenceViews=7,proofInputs=11,canonicalSourceQueries=1,rawRegisteredPaths=21439,canonicalRegisteredPaths=21438),
        limits=['simulated committed-support fixture is not current Root support adoption','fake V8 only models the frozen path collection/collision loop and nested reader bindings','no original verifier, compiler, source, object or opcode execution'],compilerInvocations=0,globalAuditRun=False,sourceCredit=0)
    if args.output:
        output=args.output.resolve();assert output.is_relative_to(ROOT/'work')and not output.exists()
        with output.open('x')as stream:stream.write(json.dumps(qualification,indent=2)+'\n')
    print(json.dumps(dict(status=qualification['status'],tests=len(tests),canonicalSourceQueries=1,sourceCredit=0)))


if __name__=='__main__':main()
