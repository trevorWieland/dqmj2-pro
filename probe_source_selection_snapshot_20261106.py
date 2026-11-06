import ast
import contextlib
import copy
import hashlib
import inspect
import json
import stat
import time
import uuid
from pathlib import Path
from unittest.mock import patch
from project import ROOT,configuration,read_json,write_json,sha256,now
import source_selection as P
import recovery_registry as R
import ledger_state as L
import source_dependencies as D
import verify_source_selection as V
WORK=ROOT/'work/w6ps'
LANE=ROOT/'evidence/lanes/parallel-wave20261106/selection-snapshot-next'
ORIGINAL_PREF=P.preferences
ORIGINAL_BATCHES=R.batches
ORIGINAL_SHA=sha256


class EpochChanged(ValueError):pass


class Tracker:
    def __init__(self):self.hashes={};self.facts={};self.resolutions={};self.observedChange=False
    def private(self,p):return p.is_relative_to(WORK.resolve()) or p.is_relative_to(LANE.resolve())
    def record(self,path,digest):
        raw=Path(path);p=raw.resolve()
        if self.private(p):return digest
        if p in self.hashes and self.hashes[p]!=digest:self.observedChange=True;raise EpochChanged('Recorded source-selection input content changed')
        self.hashes[p]=digest;self.facts[p]=self.fact(p);self.resolutions[str(raw)]=str(p);return digest
    def fact(self,p):
        s=p.stat();return (stat.S_IFMT(s.st_mode),s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_dev,s.st_ino)
    def hash(self,p):return self.record(p,ORIGINAL_SHA(p))
    def read(self,p):
        before=ORIGINAL_SHA(p);result=read_json(p)
        if ORIGINAL_SHA(p)!=before:self.observedChange=True;raise EpochChanged('Source-selection JSON changed during read')
        self.record(p,before);return result
    def verify(self):
        if self.observedChange:raise EpochChanged('Source-selection input change was observed even if restored')
        for raw,target in self.resolutions.items():
            if str(Path(raw).resolve())!=target:raise EpochChanged('Source-selection path target changed')
        for p,digest in self.hashes.items():
            if not p.is_file() or ORIGINAL_SHA(p)!=digest:raise EpochChanged('Source-selection final input SHA differs')


class Snapshot:
    def __init__(self,namespace,tracker):
        self.namespace=namespace;self.tracker=tracker;self.hits=0;self.registryHits=0;self.policy=P.POLICY;self.registry=R.REGISTRY
        self.registrySha=tracker.hash(self.registry);self.policySha=tracker.hash(self.policy);begin=time.perf_counter()
        self.registryRows=tracker.read(self.registry)['batches']
        with patch.object(P,'sha256',tracker.hash),patch.object(P,'read_json',tracker.read):self.policies=ORIGINAL_PREF(namespace)
        self.policyFacts={p:tracker.fact(p) for p in tracker.hashes};self.buildSeconds=time.perf_counter()-begin;self.quickChecks=0
    def quick(self):
        self.quickChecks+=1
        if ORIGINAL_SHA(self.registry)!=self.registrySha or ORIGINAL_SHA(self.policy)!=self.policySha:self.tracker.observedChange=True;raise EpochChanged('Run-local source-selection registry/policy snapshot changed')
        for p,fact in self.policyFacts.items():
            try:actual=self.tracker.fact(p)
            except OSError:self.tracker.observedChange=True;raise EpochChanged('Run-local policy dependency missing/type changed')
            if actual!=fact:self.tracker.observedChange=True;raise EpochChanged('Run-local policy dependency metadata changed; exact final SHA still required')
    def preferences(self,namespace,path=P.POLICY):
        if namespace!=self.namespace or path!=self.policy:return ORIGINAL_PREF(namespace,path)
        self.quick();self.hits+=1;return copy.deepcopy(self.policies)
    def batches(self):
        self.quick();self.registryHits+=1;return copy.deepcopy(self.registryRows)


def projected(root,keys,label):
    tree=ast.parse(inspect.getsource(V.main));changes=dict(loop=0,work=0,output=0)
    class Projection(ast.NodeTransformer):
        def visit_For(self,node):
            self.generic_visit(node)
            if ast.unparse(node.target)=='(identity, preference)' and ast.unparse(node.iter)=='policies.items()':node.iter=ast.Call(func=ast.Name(id='_probe_items',ctx=ast.Load()),args=[ast.Name(id='policies',ctx=ast.Load())],keywords=[]);changes['loop']+=1
            return node
        def visit_Constant(self,node):
            if node.value=='work/source-selection-negatives':changes['work']+=1;return ast.copy_location(ast.Constant(value=(root/'negatives'/label).relative_to(ROOT).as_posix()),node)
            if node.value=='evidence/verification/source-selection-negatives-20261030.json':changes['output']+=1;return ast.copy_location(ast.Constant(value=(root/(label+'.json')).relative_to(ROOT).as_posix()),node)
            return node
    tree=Projection().visit(tree)
    if changes!=dict(loop=1,work=1,output=1):raise ValueError('Original verifier no longer has exactly the3bounded-probe projection sites')
    namespace=dict(V.__dict__);namespace['_probe_items']=lambda policies:[(key,policies[key]) for key in keys];exec(compile(ast.fix_missing_locations(tree),'<private-source-selection-projection>','exec'),namespace);return namespace['main'],namespace,changes


def normalize(value,root,label):
    if isinstance(value,str):return value.replace((root/'negatives'/label).relative_to(ROOT).as_posix(),'<PRIVATE_NEGATIVES>')
    if isinstance(value,list):return [normalize(v,root,label) for v in value]
    if isinstance(value,dict):return {k:normalize(v,root,label) for k,v in value.items()}
    return value


def execute():
    if WORK!=ROOT/'work/w6ps' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/selection-snapshot-next':raise ValueError('New bounded private policy-snapshot paths differ')
    namespace=configuration()['romSha256'];root=WORK/uuid.uuid4().hex[:12]
    if root.exists():raise ValueError('Bounded policy probe root is not fresh')
    root.mkdir(parents=True);tracker=Tracker();sourcePins={n:sha256(ROOT/n) for n in ['verify_source_selection.py','source_selection.py','ledger_state.py','recovery_registry.py','source_dependencies.py','project.py','project.json']};snapshot=Snapshot(namespace,tracker);scores=[]
    for key,pref in snapshot.policies.items():
        audit=read_json(ROOT/pref['evidence']);wanted={audit['previous']['report'],audit['preferred']['report']};rows=[r for r in snapshot.registryRows if r['report'] in wanted]
        if len(rows)!=2:raise ValueError('Real preference lacks both retained registered reports')
        scores.append((sum((ROOT/r['report']).stat().st_size for r in rows),key))
    canonical=('main','arm',0x02065dec);keys=[canonical]+[key for size,key in sorted(scores) if key!=canonical][:7];samples=[];results=[]
    for label,cached in [('original',False),('snapshot',True)]:
        main,globals,projection=projected(root,keys,label);begin=time.perf_counter()
        with contextlib.ExitStack() as stack:
            stack.enter_context(patch.object(L,'read_json',tracker.read));stack.enter_context(patch.object(L,'sha256',tracker.hash));stack.enter_context(patch.object(D,'sha256',tracker.hash));stack.enter_context(patch('builtins.print'))
            if cached:stack.enter_context(patch.object(P,'preferences',snapshot.preferences));globals['batches']=snapshot.batches
            main()
        elapsed=time.perf_counter()-begin;tracker.verify();result=read_json(root/(label+'.json'));results.append(normalize(result,root,label));samples.append(dict(label=label,elapsedSeconds=elapsed,sourcePreferences=129,probedPreferencePairs=len(keys),reportOrders=2*len(keys),controls=len(result['controls']),passed=result['passed']))
    if results[0]!=results[1] or not results[0]['passed']:raise ValueError('Guarded bounded preference snapshot changed original verifier outputs/control reasons/order')
    tracker.verify()
    if {n:sha256(ROOT/n) for n in sourcePins}!=sourcePins:raise EpochChanged('Pinned original selection/collector/support implementation changed')
    total=samples[1]['elapsedSeconds']+snapshot.buildSeconds;receipt=dict(passed=True,sourceCredit=0,root=root.relative_to(ROOT).as_posix(),boundedRealCorpus=True,policyCount=len(snapshot.policies),probedKeys=[list(k) for k in keys],originalVerifierProjectionOnly=projection,allOriginalNegativeAndEnforceCasesExecuted=True,exactOriginalPrivateOutputAndReasonOrderEqual=True,samples=samples,snapshotConstructionSeconds=snapshot.buildSeconds,cachedTotalIncludingConstructionSeconds=total,observedBoundedSpeedRatio=samples[0]['elapsedSeconds']/total,defaultPolicyCacheHits=snapshot.hits,outerRegistrySnapshotHits=snapshot.registryHits,perHitPolicyRegistryHashAndMetadataChecks=snapshot.quickChecks,sourceObjectDependencyChecksUncached=True,allRecordedFinalContentAndResolutionGuardsPassed=True,trackedFiles=len(tracker.hashes),trackedPathResolutions=len(tracker.resolutions),inputPins=[dict(path=n,sha256=h) for n,h in sourcePins.items()],registrySha256=snapshot.registrySha,policySha256=snapshot.policySha,generatorSha256=sha256(__file__),productionAdoption=False,limits=['Bounded8real preference pairs/16report orders, not all129/258; all9original policy negatives and2enforcement controls run unchanged. No live source/registry/preference/index/core changes or canonical report output.','Only the loop bound and private negative/output directories are projected in the original verifier; original collect_matches/choose/enforce/source-object-dependency checks remain intact.','Policy/registry validation snapshot is run-local and default-path-only; custom negative policies call the original preferences implementation. Metadata facts are change detectors, not integrity proof; final exact SHA and path-target checks are mandatory.','Further missing/filetype/target/same-size-content/restored-epoch controls and full real-output equivalence are required before any production proposal.'] )
    write_json(LANE/'bounded-real-policy-equivalence.json',receipt);print(dict(passed=True,originalSeconds=samples[0]['elapsedSeconds'],snapshotSeconds=samples[1]['elapsedSeconds'],constructionSeconds=snapshot.buildSeconds,observedBoundedSpeedRatio=receipt['observedBoundedSpeedRatio'],controls=samples[0]['controls'],trackedFiles=len(tracker.hashes),receiptSha256=sha256(LANE/'bounded-real-policy-equivalence.json')))


if __name__=='__main__':execute()
