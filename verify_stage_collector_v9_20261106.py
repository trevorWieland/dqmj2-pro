import contextlib
import shutil
import sys
import uuid
from pathlib import Path
from unittest.mock import patch
from project import ROOT,read_json,write_json,sha256
import oracle_source_closure_20261031 as O
import oracle_source_closure_v3_20261106 as N
import stage_declared_source_package_v7_20261102 as V7
import stage_declared_source_package_v9_20261106 as V9
import stage_verified_cohort as S
import recovery_registry as R
LANE=ROOT/'evidence/lanes/parallel-wave20261106/path-lookup-next'
WORK=ROOT/'work/w6pc'


def create(root):
    if root.exists() or not root.is_relative_to(WORK):raise ValueError('Stage compatibility fixture is not fresh/owned')
    root.mkdir(parents=True)
    def text(name,value):
        p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(value,encoding='utf-8')
    for name in ['run_checks.py','configure.py','validate_clean_checkout.py','producer.py','stage_declared_source_package_v3_20261101.py']:text(name,'VALUE=1\n')
    for name in ['oracle_source_closure_20261031.py','oracle_source_closure_v2_20261106.py']:shutil.copyfile(ROOT/name,root/name)
    text('src/unit.c','#include "local.h"\nint fixture_source(void){return VALUE;}\n');text('src/local.h','#define VALUE 1\n');text('nonmatching/probe.c','int probe(void){return 2;}\n');text('evidence/generated/ghidra999/main/02000000.generated.c','int diagnostic(void){return 3;}\n');text('tools/reference-placeholder.bin','Nonexecutable private fixture reference\n')
    files=['src/unit.c','src/local.h','producer.py','nonmatching/probe.c','evidence/generated/ghidra999/main/02000000.generated.c','tools/reference-placeholder.bin'];write_json(root/'manifest.json',dict(sourceCredit=0,files=[dict(path=n,sha256=sha256(root/n)) for n in files]))
    report='evidence/matches/fixture.json';write_json(root/report,dict(sourceCredit=0,matches=[dict(source='src/unit.c',sourceSha256=sha256(root/'src/unit.c'),sourceDependencies=[dict(path='src/local.h',sha256=sha256(root/'src/local.h'))])],generator='producer.py'))
    write_json(root/'recovery.json',dict(oracles=[],batches=[dict(report=report,reproduce=['producer.py'],sourceHashes={n:sha256(root/n) for n in ['src/unit.c','src/local.h','producer.py']})]));write_json(root/'interpreted-recovery.json',dict(batches=[]));write_json(root/'evidence/trace.json',dict(sourceCredit=0,diagnostic=True))
    write_json(root/'evidence/verification/cohort-2026-10-29-999.json',dict(linksPending=False,reports=[report],interpretedReports=[]));write_json(root/'evidence/verification/cohort999-validation-driver.json',dict(state='synthetic-routing-only-no-game-credit'))
    write_json(root/'package.json',dict(cohort=999,extra=['evidence/trace.json'],manifests=['manifest.json'],archives=[],traces=['evidence/trace.json']))


def normalize(value,root):
    if isinstance(value,bytes):return dict(nulDelimitedUtf8=value.decode('utf-8'))
    if isinstance(value,Path):value=str(value)
    if isinstance(value,str):return value.replace(str(root),'<FIXTURE_ROOT>')
    if isinstance(value,dict):return {k:normalize(v,root) for k,v in value.items()}
    if isinstance(value,(tuple,list)):return [normalize(v,root) for v in value]
    return value


def execute():
    base=WORK/('stage9-'+uuid.uuid4().hex);records=[];old_collect=O.collect;protected={n:sha256(ROOT/n) for n in V9.PINS}
    for label in ['v7','v9']:
        root=base/label;create(root);calls=[]
        def git_run(argv,*args,**kwargs):
            if argv[:2]!=['git','add']:raise ValueError('Unexpected nonstaging subprocess in compatibility fixture')
            calls.append(normalize(dict(argv=argv,args=args,kwargs=kwargs),root));return __import__('subprocess').CompletedProcess(argv,0,b'',b'')
        with contextlib.ExitStack() as stack:
            for module in [V7,S,O,N,R]:stack.enter_context(patch.object(module,'ROOT',root))
            stack.enter_context(patch.object(R,'REGISTRY',root/'recovery.json'))
            for module in [O,N]:stack.enter_context(patch.object(module,'SEARCH',[root,root/'evidence/application',root/'evidence/encounter',root/'evidence/save',root/'nonmatching/encounter']))
            stack.enter_context(patch.object(O,'collect',old_collect));stack.enter_context(patch.object(sys,'argv',['stage.py','package.json']));stack.enter_context(patch('subprocess.run',git_run));stack.enter_context(patch('builtins.print'))
            (V7 if label=='v7' else V9).main();restored=O.collect is old_collect
        record=dict(gitCalls=calls,capturedClosure=read_json(root/'evidence/verification/cohort999-captured-oracle-closure-20261031.json'),copiedDependencies=read_json(root/'evidence/verification/cohort999-copied-reference-inputs-20261101.json'),diagnostics=read_json(root/'evidence/verification/cohort999-frozen-diagnostic-sources-20261101.json'))
        if label=='v9' and not restored:raise ValueError('New stage wrapper leaked collector substitution after success')
        records.append(record)
    if records[0]!=records[1]:raise ValueError('New stage delegation changed Git payload/order or declaration/capture output')
    class Failure(Exception):pass
    def fail():raise Failure()
    with patch.object(V7,'main',fail),patch.object(O,'collect',old_collect):
        try:V9.main()
        except Failure:pass
        else:raise ValueError('Stage wrapper swallowed original failure')
        if O.collect is not old_collect:raise ValueError('Stage wrapper leaked collector substitution after failure')
    if {n:sha256(ROOT/n) for n in protected}!=protected:raise ValueError('Frozen collector/staging code changed')
    out=LANE/'stage-v9-compatibility.json';write_json(out,dict(passed=True,sourceCredit=0,generatorSha256=sha256(__file__),newStageSha256=sha256(ROOT/'stage_declared_source_package_v9_20261106.py'),unchangedLegacyPins=[dict(path=n,sha256=h) for n,h in protected.items()],realLegacyDeclaredAndVerifiedStageLogicExecuted=True,gitBoundaryOnlyMocked=True,actualGitIndexMutation=False,exactFullGitArgvStdinOrderEqual=True,exactCapturedClosureAndDeclaredReferenceDiagnosticMetadataEqual=True,collectorRestoredAfterSuccess=True,originalFailurePropagatedAndCollectorRestored=True,gitCallsPerFixture=len(records[0]['gitCalls']),routingFixtureOutputs=records[0],fixtureRoots=[(base/x).relative_to(ROOT).as_posix() for x in ['v7','v9']],fullCollectorQualification=dict(path=(LANE/'collector-v3-qualification.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'collector-v3-qualification.json')),limits=['Synthetic fixtures execute unchanged realv7/stage_verified/verify_sources and complete original/new collector bodies; onlyGitwrites are intercepted.','Full22833-source collector output equivalence is established separately. This does not adopt production or claim native source/ROM completion.']))
    print(dict(passed=True,gitCalls=len(records[0]['gitCalls']),restorationControls=2,receipt=out.relative_to(ROOT).as_posix(),sha256=sha256(out)))


if __name__=='__main__':execute()
