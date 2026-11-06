import contextlib
import hashlib
import json
import time
import uuid
from unittest.mock import patch
from project import ROOT,read_json,write_json,sha256,configuration,now
import source_selection as P
import ledger_state as L
import source_dependencies as D
from probe_source_selection_snapshot_20261106 import Tracker,EpochChanged,WORK,LANE,projected,normalize
from guard_source_selection_snapshot_20261106 import GuardedSnapshot


def execute():
    if WORK!=ROOT/'work/w6ps' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/selection-snapshot-next':raise ValueError('Full private source-selection comparator scope differs')
    root=WORK/('full-'+uuid.uuid4().hex[:12]);root.mkdir(parents=True);namespace=configuration()['romSha256'];tracker=Tracker();sourceNames=['verify_source_selection.py','source_selection.py','ledger_state.py','recovery_registry.py','source_dependencies.py','project.py','project.json','guard_source_selection_snapshot_20261106.py','probe_source_selection_snapshot_20261106.py'];pins={n:sha256(ROOT/n) for n in sourceNames};started=now();snapshot=GuardedSnapshot(namespace,tracker);keys=list(snapshot.policies);samples=[];results=[]
    if len(keys)!=129:raise EpochChanged('Current measured preference count changed before full comparison')
    write_json(root/'state.json',dict(status='full-original-verifier-running',sourceCredit=0,startedUtc=started,policyCount=129,registrySha256=snapshot.registrySha,policySha256=snapshot.policySha))
    originalCurrent=L.current;progress=dict(calls=0)
    def current(path,expected):
        result=originalCurrent(path,expected);progress['calls']+=1
        if progress['calls']%1000==0:print(dict(originalCurrentChecks=progress['calls']),flush=True)
        return result
    for label,cached in [('original',False),('snapshot',True)]:
        main,globals,projection=projected(root,keys,label);begin=time.perf_counter();write_json(root/'state.json',dict(status='full-'+label+'-verifier-running',sourceCredit=0,startedUtc=started,policyCount=129,registrySha256=snapshot.registrySha,policySha256=snapshot.policySha))
        with contextlib.ExitStack() as stack:
            stack.enter_context(patch.object(L,'read_json',tracker.read));stack.enter_context(patch.object(L,'sha256',tracker.hash));stack.enter_context(patch.object(D,'sha256',tracker.hash));stack.enter_context(patch.object(L,'current',current))
            if cached:stack.enter_context(patch.object(P,'preferences',snapshot.preferences));globals['batches']=snapshot.batches
            main()
        elapsed=time.perf_counter()-begin;snapshot.verify();result=read_json(root/(label+'.json'));normalized=normalize(result,root,label);results.append(normalized);samples.append(dict(label=label,elapsedSeconds=elapsed,preferences=len(keys),reportOrders=2*len(keys),controls=len(result['controls']),passed=result['passed'],normalizedOutputSha256=hashlib.sha256(json.dumps(normalized,sort_keys=True,separators=(',',':')).encode()).hexdigest(),privateOutputSha256=sha256(root/(label+'.json'))));print(samples[-1],flush=True)
    if results[0]!=results[1] or not results[0]['passed']:raise ValueError('Full original and guarded snapshot verifier output/negative reason/order differs')
    snapshot.verify()
    if {n:sha256(ROOT/n) for n in pins}!=pins:raise EpochChanged('Original source-selection/support implementations changed')
    guarded=samples[1]['elapsedSeconds']+snapshot.buildSeconds;a=samples[0]['elapsedSeconds'];receipt=dict(passed=True,sourceCredit=0,completeReal129Preference258OrderComparison=True,allOriginal269ControlsExecuted=True,exactOriginalNormalizedOutputEqual=True,onlyProjectionSites=projection,projectionMeaning='Loop iterates exactly the same full129policy keys/order; only private negative/output paths differ from original. No semantic/validation/registry/report/source/object logic changed.',privateRoot=root.relative_to(ROOT).as_posix(),startedUtc=started,finishedUtc=now(),samples=samples,snapshotBuildSeconds=snapshot.buildSeconds,snapshotTotalIncludingConstructionSeconds=guarded,observedFullSpeedRatio=a/guarded,savedSeconds=a-guarded,timeReductionPercent=100*(a-guarded)/a,defaultPolicyCacheHits=snapshot.defaultHits,outerRegistrySnapshotHits=snapshot.registryHits,uncachedCustomNegativePolicyCalls=snapshot.customCalls,originalFreshSourceObjectChecks=progress['calls'],sourceObjectDependencyFreshnessUncached=True,trackedFiles=len(tracker.hashes),trackedResolutionFacts=len(tracker.resolutions)+len(snapshot.localFacts),allFinalRegistryPolicySourceObjectDependencyReportHashAndResolutionGuardsPassed=True,registrySha256=snapshot.registrySha,policySha256=snapshot.policySha,sourcePins=[dict(path=n,sha256=h) for n,h in pins.items()],genuineGuardControls=dict(path=(LANE/'snapshot-guard-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'snapshot-guard-controls.json')),generatorSha256=sha256(__file__),productionAdopted=False,noCanonicalReportOrSharedJobOrIndexMutated=True,limits=['This comparison ran original verifier logic on the live real input epoch but wrote only new private work outputs; all observed input bytes and paths were guarded before/after. Any source/registry/policy change fails the comparison rather than accepting a stale snapshot.','One original-then-snapshot timing pair with concurrent machine work, not a universal throughput forecast. Snapshot construction is included in reported optimized cost.','Default validated policy and outer registry rows only are memoized. Custom negative policies, report-order overrides and all source/object/header/dependency/choose/enforce checks remain original and uncached.','No original verifier/preferences/registry/collector/stage code or production wrapper was edited. A separately reviewed new production version is still required.'])
    write_json(LANE/'full-real-selection-equivalence.json',receipt);write_json(root/'state.json',dict(status='complete-full-output-equivalence',sourceCredit=0,receiptSha256=sha256(LANE/'full-real-selection-equivalence.json')));print(dict(passed=True,originalSeconds=a,guardedTotalSeconds=guarded,observedFullSpeedRatio=a/guarded,savedSeconds=a-guarded,controls=len(results[0]['controls']),receiptSha256=sha256(LANE/'full-real-selection-equivalence.json')),flush=True)


if __name__=='__main__':execute()
