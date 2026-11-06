import json
import os
import subprocess
import sys
import uuid
from project import ROOT,read_json,write_json,sha256,now
from compare_oracle_context_cache_real_20261106 import verify_snapshot
from qualify_oracle_path_cache_v3_20261106 import WORK,LANE,ast_proof


METADATA=ROOT/'work/w5cp/real162-52b00d71'


def execute():
    if WORK!=ROOT/'work/w6pc' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/path-lookup-next':raise ValueError('New full path-cache comparator directories differ')
    snapshot=verify_snapshot(METADATA);proof=ast_proof();bounded=read_json(LANE/'bounded-v3-equivalence.json')
    if not bounded['passed'] or bounded['astProof']!=proof or bounded['observedBoundedSpeedRatio']<=1:raise ValueError('Bounded prerequisite not qualified/faster')
    baseline=read_json(METADATA/'v2-closure.json');baselineTiming=read_json(METADATA/'v2-timing.json')
    if baseline['missingRequiredPaths'] or len(baseline['sourceAndEvidenceHashes'])!=22833 or sha256(METADATA/'v2-closure.json')!='33c6cb2ca2e601eb675b1e9c8d751927e0ead32282acb01fde92edab40c30f69':raise ValueError('Qualified fullv2baseline output differs')
    root=ROOT/snapshot['root'];output=WORK/('full-'+uuid.uuid4().hex[:12]);output.mkdir(parents=True);launcher=output/'launch.py';names=['oracle_source_closure_v2_20261106.py','oracle_source_closure_v3_20261106.py','collector_path_lookup_epoch_20261106.py','qualify_oracle_path_cache_v3_20261106.py','compare_oracle_path_cache_real_20261106.py'];pins={n:sha256(ROOT/n) for n in names};started=now()
    code="import sys,time,importlib.util\nfrom pathlib import Path\nsys.path.insert(0,sys.argv[1]);sys.path.insert(1,sys.argv[2])\nfrom project import write_json,sha256\nspec=importlib.util.spec_from_file_location('candidate_path_collector',Path(sys.argv[2])/'oracle_source_closure_v3_20261106.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)\nfactory=module.PathLookupEpoch;observed=[]\ndef observe(root):\n value=factory(root);observed.append(value);return value\nmodule.PathLookupEpoch=observe\nstart=time.perf_counter();result=module.collect();elapsed=time.perf_counter()-start\nif len(observed)!=1 or observed[0].observedChange:raise ValueError('Expected one fresh successful lookup epoch')\nwrite_json(Path(sys.argv[3]),result);write_json(Path(sys.argv[4]),dict(elapsedSecondsIncludingConstructorAndFinalGuards=elapsed,paths=len(result['sourceAndEvidenceHashes']),missingRequiredPaths=result['missingRequiredPaths'],outputSha256=sha256(sys.argv[3]),lookupFacts=observed[0].summary()))\n"
    launcher.write_text(code,encoding='utf-8');command=[sys.executable,str(launcher),str(root),str(ROOT),str(output/'v3-closure.json'),str(output/'v3-timing.json')];log=output/'v3.log';write_json(output/'state.json',dict(status='running-full-v3-readonly-snapshot',sourceCredit=0,startedUtc=started,command=command,sourcePins=pins,snapshotSha256=sha256(METADATA/'snapshot.json')));print(dict(started=True,output=output.relative_to(ROOT).as_posix(),log=log.relative_to(ROOT).as_posix()),flush=True)
    with log.open('w',encoding='utf-8') as stream:process=subprocess.run(command,cwd=root,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=stream,stderr=subprocess.STDOUT)
    if process.returncode:raise ValueError('Full guarded path-cache collector failed; original log retained: '+str(log))
    verify_snapshot(METADATA)
    if {n:sha256(ROOT/n) for n in pins}!=pins:raise ValueError('New comparator/collector implementations changed during full run')
    result=read_json(output/'v3-closure.json');timing=read_json(output/'v3-timing.json')
    if result!=baseline or sha256(output/'v3-closure.json')!=sha256(METADATA/'v2-closure.json'):raise ValueError('Complete full22833-source closure output is not byte-identical')
    receipt=dict(passed=True,sourceCredit=0,startedUtc=started,finishedUtc=now(),sourceCommit=snapshot['sourceCommit'],privateOutput=output.relative_to(ROOT).as_posix(),snapshot=dict(path=(METADATA/'snapshot.json').relative_to(ROOT).as_posix(),sha256=sha256(METADATA/'snapshot.json'),files=len(snapshot['pins']),bytes=sum(p['bytes'] for p in snapshot['pins'])),baseline=dict(outputSha256=sha256(METADATA/'v2-closure.json'),timing=baselineTiming),candidate=timing,completeOutputByteIdentical=True,sourceAndRegistryAndPreferenceAndInterpretedAndDirectoryEpochGuardsPassed=True,lookupResolutionTypeMissDirectoryContentFinalGuardsPassed=True,stickyObservedChangeGuardPassed=True,sourcePins=pins,astProof=proof,boundedReceipt=dict(path=(LANE/'bounded-v3-equivalence.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'bounded-v3-equivalence.json')),productionAdopted=False,noSnapshotOrLiveInputOrStageOrIndexWrites=True,historicalBaselineRatio=baselineTiming['elapsedSeconds']/timing['elapsedSecondsIncludingConstructorAndFinalGuards'],limits=['Complete real22833-source output is compared against the previous qualifiedv2run on the exact same immutable22836-file snapshot, whose full content/directory inventory is independently verified before and after.','The historical1150secondv2baseline and newv3timing were not a consecutive paired run; concurrent machine load, cache warmth and Python set traversal order can differ. The historical ratio is descriptive, not a production speed forecast.','The only launcher instrumentation observes construction of the actual PathLookupEpoch class to report its final counters; collector and guards execute unchanged.','Actual captured content hashes are never cached. Every unique queried resolution, file/missing/type/identity and queried-parent directory type/identity fact is recomputed before return; unrelated unqueried siblings do not freeze the live tree.'])
    write_json(LANE/'full-real-v3-equivalence.json',receipt);write_json(output/'state.json',dict(status='passed-full-output-byte-equivalence',sourceCredit=0,receiptSha256=sha256(LANE/'full-real-v3-equivalence.json')));print(dict(passed=True,paths=22833,elapsedSeconds=timing['elapsedSecondsIncludingConstructorAndFinalGuards'],historicalRatio=receipt['historicalBaselineRatio'],receiptSha256=sha256(LANE/'full-real-v3-equivalence.json')),flush=True)


if __name__=='__main__':execute()
