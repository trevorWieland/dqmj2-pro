import ast
import contextlib
import hashlib
import json
import os
import statistics
import time
import uuid
from pathlib import Path
from unittest.mock import patch
from project import ROOT,read_json,write_json,sha256,now
import oracle_source_closure_20261031 as O
LANE=ROOT/'evidence/lanes/parallel-wave20261105/source-capture-performance-next'
WORK=ROOT/'work/w5cp'


def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def snapshot(root):return {p.relative_to(root).as_posix():sha256(p) for p in root.rglob('*') if p.is_file()}


def fixture(root,groups=64):
    if root.exists() or not root.is_relative_to(WORK):raise ValueError('New capture benchmark fixture root is not fresh/owned')
    root.mkdir(parents=True)
    def text(name,value):
        path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(value,encoding='utf-8')
    for name in ['run_checks.py','configure.py','validate_clean_checkout.py','common_shared.py']:text(name,"import common_shared\nVALUE='global_marker'\n")
    text('evidence/save/package_public.py',"VALUE='late_search_root'\n")
    write_json(root/'config/global.json',dict(files=[dict(path='src/shared.h',sha256='0'*64)]))
    text('src/shared.h','typedef int MeasuredWord;\n');text('work/poison.py',"VALUE='excluded_payload'\n")
    oracles=[];batches=[]
    for i in range(groups):
        prefix=f'src/family{i:03d}';py=prefix+'/module.py';source=prefix+'/unit.c';header=prefix+'/local.h';report=f'evidence/reports/report{i:03d}.json'
        body="from pathlib import Path\nimport common_shared\nfrom package_public import VALUE\nCONFIG=ROOT/'config/global.json'\ndef load():return read_json(CONFIG)\nNAMES="+repr([f'field_{j:02d}' for j in range(16)])+"\nC_SOURCE='"+source+"'\nEXCLUDED='work/poison.py'\n"
        text(py,body);text(source,'#include "local.h"\nMeasuredWord native_unit_'+str(i)+'(MeasuredWord a){return a+1;}\n');text(header,'#include "../shared.h"\n')
        write_json(root/report,dict(matches=[dict(source=source,sourceSha256=sha256(root/source),sourceDependencies=[dict(path=header,sha256=sha256(root/header))])],generatorSources=[dict(path=py,sha256=sha256(root/py))],vectors=[dict(path='missing-never-expanded.json',sha256='0'*64)]))
        batch=dict(report=report,reproduce=[py],sourceHashes={p:sha256(root/p) for p in [py,source,header,'common_shared.py']});batches.append(batch)
    write_json(root/'recovery.json',dict(oracles=oracles,batches=batches));write_json(root/'interpreted-recovery.json',dict(batches=[]))


def run(root,cached,mutation=None):
    before=snapshot(root);original_resolve=Path.resolve;original_is_file=Path.is_file;resolve_cache={};file_cache={};counts=dict(resolveCalls=0,resolveHits=0,isFileCalls=0,isFileHits=0);changed=False
    def owned(path):return str(path).lower().startswith(str(root).lower()+os.sep) or path==root
    def resolve(path,*args,**kwargs):
        key=(str(path),args,tuple(sorted(kwargs.items())));counts['resolveCalls']+=1
        if cached and owned(path) and key in resolve_cache:counts['resolveHits']+=1;return resolve_cache[key]
        value=original_resolve(path,*args,**kwargs)
        if cached and owned(path):resolve_cache[key]=value
        return value
    def is_file(path):
        key=str(path);counts['isFileCalls']+=1
        if cached and owned(path) and key in file_cache:counts['isFileHits']+=1;return file_cache[key]
        value=original_is_file(path)
        if cached and owned(path):file_cache[key]=value
        return value
    begin=time.perf_counter()
    with contextlib.ExitStack() as stack:
        stack.enter_context(patch.object(O,'ROOT',root));stack.enter_context(patch.object(O,'SEARCH',[root,root/'evidence/application',root/'evidence/encounter',root/'evidence/save',root/'nonmatching/encounter']));stack.enter_context(patch.object(Path,'resolve',resolve));stack.enter_context(patch.object(Path,'is_file',is_file));stack.enter_context(patch('builtins.print'))
        result=O.collect()
        if mutation is not None:mutation()
    elapsed=time.perf_counter()-begin
    if snapshot(root)!=before:raise ValueError('Immutable private capture input/directory epoch changed')
    return result,dict(cached=cached,elapsedSeconds=elapsed,outputSha256=digest(result),closurePaths=len(result['sourceAndEvidenceHashes']),missingRequired=result['missingRequiredPaths'],lookupCounts=counts)


def execute():
    if WORK!=ROOT/'work/w5cp' or LANE!=ROOT/'evidence/lanes/parallel-wave20261105/source-capture-performance-next':raise ValueError('New capture benchmark namespace differs')
    root=WORK/('fixture-'+uuid.uuid4().hex);fixture(root);samples=[];outputs=[]
    for cached in [False,True,True,False]:
        result,sample=run(root,cached);samples.append(sample);outputs.append(result)
    if any(value!=outputs[0] for value in outputs[1:]) or outputs[0]['missingRequiredPaths']:raise ValueError('Cached/unchanged complete collector outputs differ or baseline fixture not closed')
    controls=[]
    def equality_case(label,mutation,restore):
        mutation();old,a=run(root,False);new,b=run(root,True);restore()
        if old!=new:raise ValueError('Cached collector changed legacy required/excluded behavior: '+label)
        controls.append(dict(case=label,exactOriginalOutput=True,missingRequiredPaths=old['missingRequiredPaths'],closurePaths=len(old['sourceAndEvidenceHashes'])))
    required=root/'src/family000/module.py';saved=required.read_bytes();equality_case('missing-required-source',lambda:required.unlink(),lambda:required.write_bytes(saved))
    config=root/'config/global.json';saved_config=config.read_bytes();equality_case('required-pin-inside-static-json',lambda:write_json(config,dict(files=[dict(path='config/absent.json',sha256='0'*64)])),lambda:config.write_bytes(saved_config))
    report=root/'evidence/reports/report000.json';saved_report=report.read_bytes();equality_case('malformed-optional-report-json',lambda:report.write_text('{broken'),lambda:report.write_bytes(saved_report))
    for label,operation,restore in [('changed-captured-file',lambda:required.write_text("VALUE='tampered'\n"),lambda:required.write_bytes(saved)),('new-previously-missing-import',lambda:(root/'field_00.py').write_text('VALUE=1\n'),lambda:(root/'field_00.py').unlink()),('removed-existing-file',lambda:required.unlink(),lambda:required.write_bytes(saved))]:
        try:run(root,True,operation)
        except ValueError as error:controls.append(dict(case=label,epochGuardRejected=True,reason=str(error)))
        else:raise ValueError('Cached proof failed to reject changed fixture epoch')
        finally:restore()
    if any('/work/' in '/'+p for p in outputs[0]['sourceAndEvidenceHashes']):raise ValueError('Excluded private work was captured')
    controls.append(dict(case='excluded-work-and-vector-payloads',passed=True,poisonAndMissingVectorNotCaptured=True))
    old=statistics.median(s['elapsedSeconds'] for s in samples if not s['cached']);new=statistics.median(s['elapsedSeconds'] for s in samples if s['cached']);output=LANE/'bounded-cache-equivalence.json';write_json(output,dict(passed=True,sourceCredit=0,generatorSha256=sha256(__file__),originalCollectorSha256=sha256(ROOT/'oracle_source_closure_20261031.py'),fixture=root.relative_to(ROOT).as_posix(),fixtureFiles=len(snapshot(root)),samples=samples,exactCompleteOutputEquality=True,controls=controls,uncachedMedianSeconds=old,cachedMedianSeconds=new,observedFixtureSpeedRatio=old/new,scope='Private immutable64directory fixture exercises the unchanged collect() body with process-local Path resolution/existence memoization only; each call is fresh and the complete returned JSON is identical. No live/frozen helper/index/registry/output changes. This fixture is not a game source closure or full performance forecast.',adoptionRequires=['Fresh per-collect caches only; preserve all original resolution/search/required/contextual JSON/import/include/hash checks.','Validate captured content and relevant lookup/directory facts before returning; source workers may create unrelated files, so a broad whole-worktree frozen epoch is not an acceptable production scheduling constraint.','Handle symlink/junction/case/escaped paths conservatively and retain uncached fallback; an immutable private fixture does not prove unrestricted live filesystem equivalence.','Adopt only through a new separately qualified collector/stager version after Root review; leave active162 capture and every old pinned helper untouched.']))
    print(dict(passed=True,fixturePaths=len(outputs[0]['sourceAndEvidenceHashes']),uncachedMedianSeconds=old,cachedMedianSeconds=new,observedFixtureSpeedRatio=old/new,controls=len(controls),receipt=output.relative_to(ROOT).as_posix(),sha256=sha256(output)))


if __name__=='__main__':execute()
