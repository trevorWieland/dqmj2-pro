import copy
from contextlib import contextmanager
import hashlib
import importlib
import json
from pathlib import Path,PurePosixPath
import subprocess


CONTRACT='provenance/cohort175-registered-input-paths-v1-20261107.json'
VERIFIER='verify_committed_source_inputs_v8_20261101.py'
RAW='src\\overlays\\ov003_mode3_network_138ce8443920.c'
CANON=RAW.replace('\\','/')
SOURCE_SHA='138ce8443920c8b6b1ed4869148d6ae27b321ff1d66be4844ed72a3d21d9c8a0'
REGISTRY_SHA='f792a31d3bbe574aeced9f6146576999e4d0e28bc5517111ada5b5b8dda82629'
V8_SHA='ec18cd7d970de3b4f34499a9289c118b9f1c44eac3080ea8c92c7c363db576b2'
POLICY_SHA='c7697573f1cdbb32f4d5f89665c2ec176ba49e6817466fd42edcce31d848c2ef'
EVIDENCE_DIGEST='32e537fbe60a103534719a1e8f79730a525886a1945b2bd5784a2d93c6e8b921'
PROOF_DIGEST='dc1903603729dbcccfb7d7c0b2dfc291c5fbe7de89b90dfd9dc9bfc425bad80e'
ACCOUNTING=dict(rawRegisteredPaths=21439,canonicalRegisteredPaths=21438,distinctEvidenceViews=7,rawAndCanonicalAliasKeys=2,canonicalBlobQueries=1)


def require(value,message):
    if not value:raise ValueError(message)


def sha(raw):return hashlib.sha256(raw).hexdigest()


def canonical(value):return sha(json.dumps(value,sort_keys=True,separators=(',',':')).encode())


def safe(name):
    path=PurePosixPath(name)
    require(isinstance(name,str)and name not in('','.')and path.as_posix()==name and not path.is_absolute()and'..'not in path.parts and'\\'not in name and':'not in name and'\n'not in name and'\r'not in name and'\0'not in name,'unsafe logical input path')
    return name


def validate_contract(contract):
    require(contract['schemaVersion']==1 and contract['role']=='cohort175-exact-Windows-path-identity-context'and contract['qualificationOnly']is True and contract['sourceCredit']==0,'contract scope differs')
    require(contract['foundationSourceRevision']=='4bb9862a490f7cb71165388384adb820081d1b19','foundation differs')
    require(contract['registry']==dict(path='recovery.json',sha256=REGISTRY_SHA),'registry pin differs')
    require(contract['preferences']==dict(path='source-preferences.json',sha256=POLICY_SHA),'preference pin differs')
    require(contract['originalVerifier']==dict(path=VERIFIER,sha256=V8_SHA),'strict V8 pin differs')
    require(contract['canonicalSource']==dict(rawPath=RAW,path=CANON,sha256=SOURCE_SHA,bytes=4690),'source identity differs')
    require(len(contract['evidenceViews'])==7 and canonical(contract['evidenceViews'])==EVIDENCE_DIGEST,'seven evidence bindings differ')
    require(len(contract['proofInputs'])==11 and canonical(contract['proofInputs'])==PROOF_DIGEST,'eleven registered proof pins differ')
    require(contract['expectedAccounting']==ACCOUNTING,'deduplication accounting differs')
    require(contract['helper']['path']=='registered_input_path_context_v1_20261107.py'and contract['test']['path']=='test_registered_input_path_context.py','support paths differ')
    require(contract['helper']['sha256']==sha(Path(__file__).read_bytes()),'helper bytes differ')
    for record in[contract['helper'],contract['test'],contract['originalVerifier'],contract['registry'],contract['preferences'],contract['canonicalSource'],*contract['evidenceViews'],*contract['proofInputs']]:safe(record['path'])


def prepare(contract,read_current,read_committed,revision):
    validate_contract(contract)
    require(len(revision)==40 and all(c in'0123456789abcdef'for c in revision),'revision must be resolved')
    records=[contract[k]for k in['helper','test','originalVerifier','registry','preferences','canonicalSource']]+contract['evidenceViews']+contract['proofInputs']
    raw_contract=read_current(CONTRACT)
    require(raw_contract is not None and json.loads(raw_contract)==contract,'current contract differs')
    records=records+[dict(path=CONTRACT,sha256=sha(raw_contract))]
    current={};missing_current=[];missing_git=[]
    for record in records:
        name=record['path'];raw=read_current(name);committed=read_committed(name)
        if raw is None:missing_current.append(name)
        else:
            require(sha(raw)==record['sha256'],'current input hash differs: '+name)
            require('bytes'not in record or len(raw)==record['bytes'],'current input length differs: '+name)
            current[name]=raw
        if committed is None:missing_git.append(name)
        else:require(sha(committed)==record['sha256'],'committed input hash differs: '+name)
        if raw is not None and committed is not None:require(raw==committed,'committed/current bytes differ: '+name)
    documents={}
    if'recovery.json'in current:
        registry=json.loads(current['recovery.json']);pins={}
        for batch in registry['batches']:
            for name,digest in batch['sourceHashes'].items():
                name=name.replace('\\','/');require(name not in pins or pins[name]==digest,'registry pin collision');pins[name]=digest
        require(pins.get(CANON)==SOURCE_SHA,'canonical source is not registered')
        for record in contract['proofInputs']:
            origins=sorted(b['report']for b in registry['batches']if any(n.replace('\\','/')==record['path']and h==record['sha256']for n,h in b['sourceHashes'].items()))
            require(pins.get(record['path'])==record['sha256']and sorted(set(origins))==record['originReports'],'proof registration differs: '+record['path'])
    if'source-preferences.json'in current:
        policy=json.loads(current['source-preferences.json'])
        for record in contract['evidenceViews']:
            row=record['preference'];require(policy['preferences'].count(row)==1,'preference binding differs')
            if record['path']not in current:continue
            document=json.loads(current[record['path']])
            require(document['previous']['source']==RAW and document['previous']['sourceSha256']==SOURCE_SHA,'previous source identity differs')
            require(document['preferred']=={k:row[k]for k in('source','sourceSha256','report')},'preferred binding differs')
            require(document['identity']=={k:row[k]for k in('processor','module','mode','address','bytes','targetSha256')},'full namespace differs')
            require(document['romSha256']==policy['romSha256']and document['originalSourceUnchanged']and document['nativeBytesUnchanged']and document['newFunctionCredit']==0 and document['newByteCredit']==0,'evidence scope differs')
            documents[record['path']]=document
    report=dict(ready=not missing_current and not missing_git,revision=revision,inputsChecked=len(records),missingCurrent=missing_current,missingCommitted=missing_git,
        registrySha256=REGISTRY_SHA,originalVerifierSha256=V8_SHA,canonicalSourceSha256=SOURCE_SHA,proofInputCount=11,proofInputBytes=sum(v['bytes']for v in contract['proofInputs']),sourceCredit=0)
    return dict(report=report,documents=documents)


def project_evidence(document,expected):
    require(document==expected and canonical(document)==canonical(expected),'prior-reader evidence metadata differs')
    require(document['previous']['source']==RAW and document['previous']['sourceSha256']==SOURCE_SHA,'unqualified evidence source')
    result=copy.deepcopy(document);result['previous']['source']=CANON
    restored=copy.deepcopy(result);restored['previous']['source']=RAW
    require(restored==document and result['previous']['sourceSha256']==SOURCE_SHA,'evidence view changed other fields')
    return result


@contextmanager
def installed(module,prepared,root):
    require(prepared['report']['ready']and len(prepared['documents'])==7,'setup is pending exact committed inputs')
    root=Path(root).resolve();saved_main=module.main;saved_reader=module.read_json;events=[];state=dict(calls=0,completed=False)
    proof=dict(setup=copy.deepcopy(prepared['report']),events=[],expectedAccounting=dict(ACCOUNTING),sourceCredit=0,passed=False)
    def wrapped_main(*args,**kwargs):
        state['calls']+=1;state['completed']=False
        require(state['calls']==1 and not args and not kwargs,'strict V8 invocation differs')
        prior_reader=module.read_json
        def reader(path):
            document=prior_reader(path)
            try:name=Path(path).relative_to(root).as_posix()
            except ValueError:return document
            if name not in prepared['documents']:return document
            require(not any(event['path']==name for event in events),'duplicate evidence view')
            view=project_evidence(document,prepared['documents'][name]);events.append(dict(path=name,field='previous.source',before=RAW,after=CANON,sourceSha256=SOURCE_SHA,allOtherFieldsIdentical=True))
            return view
        module.read_json=reader
        try:result=saved_main()
        finally:
            unchanged=module.read_json is reader;module.read_json=prior_reader
            proof['events']=copy.deepcopy(events)
            require(unchanged,'nested V8 reader binding changed unexpectedly')
        require({v['path']for v in events}==set(prepared['documents'])and len(events)==7,'seven distinct exact views not observed')
        state['completed']=True;return result
    module.main=wrapped_main;success=False
    try:yield proof;success=True
    finally:
        unchanged=module.main is wrapped_main and module.read_json is saved_reader
        module.main=saved_main;module.read_json=saved_reader
        require(unchanged,'outer V8 binding changed unexpectedly')
        if success:
            require(state['calls']==1 and state['completed'],'strict V8 did not finish exactly once')
            proof['passed']=True


def validate_accounting(document,contract):
    validate_contract(contract)
    require(document['passed']is True and document['sourceCredit']==0 and document['registeredRepositoryPathsChecked']==21438,'actual V8 canonical accounting differs')
    return dict(rawLogicalAliasCount=21439,canonicalPathCount=21438,removedDuplicateKeys=1,canonicalSourceQueries=1,sourceCredit=0)


def committed_blobs(root,revision,names):
    names=sorted(set(safe(n)for n in names));query=''.join(revision+':'+n+'\n'for n in names).encode()
    raw=subprocess.run(['git','cat-file','--batch'],cwd=root,input=query,capture_output=True,check=True).stdout;cursor=0;result={}
    for name in names:
        end=raw.index(b'\n',cursor);header=raw[cursor:end];cursor=end+1
        if header.endswith(b' missing'):
            require(header==(revision+':'+name+' missing').encode(),'unexpected missing response');result[name]=None;continue
        oid,kind,length=header.split();length=int(length);require(kind==b'blob','nonblob committed input')
        data=raw[cursor:cursor+length];cursor+=length;require(len(data)==length and raw[cursor:cursor+1]==b'\n','truncated committed input');cursor+=1;result[name]=data
    require(cursor==len(raw),'extra committed response bytes')
    return result


def setup(root,contract):
    root=Path(root).resolve();validate_contract(contract)
    revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
    subprocess.run(['git','merge-base','--is-ancestor',contract['foundationSourceRevision'],revision],cwd=root,capture_output=True,check=True)
    names=[contract[k]['path']for k in['helper','test','originalVerifier','registry','preferences','canonicalSource']]+[v['path']for v in contract['evidenceViews']+contract['proofInputs']]+[CONTRACT]
    blobs=committed_blobs(root,revision,names)
    def current(name):
        path=root/safe(name)
        if not path.is_file():return None
        require(not path.is_symlink()and path.resolve().is_relative_to(root),'current input path escapes root')
        return path.read_bytes()
    return prepare(contract,current,blobs.get,revision)


@contextmanager
def validation_route(root,contract):
    root=Path(root).resolve();prepared=setup(root,contract)
    require(prepared['report']['ready'],'registered proof packaging/support setup pending')
    module=importlib.import_module(VERIFIER[:-3])
    require(Path(module.__file__).resolve()==root/VERIFIER and module.ROOT.resolve()==root,'strict V8 module owner differs')
    with installed(module,prepared,root)as proof:yield proof
