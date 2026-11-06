import ast
import copy
import inspect
import os
import shutil
import statistics
import subprocess
import time
import uuid
from pathlib import Path
from unittest.mock import patch
from project import ROOT,read_json,write_json,sha256
import oracle_source_closure_v2_20261106 as base
import oracle_source_closure_v3_20261106 as candidate
import wave20261105_source_capture_perf_bench as fixture_module
from collector_path_lookup_epoch_20261106 import PathLookupEpoch,LookupEpochChanged
WORK=ROOT/'work/w6pc'
LANE=ROOT/'evidence/lanes/parallel-wave20261106/path-lookup-next'


def ast_proof():
    a=ast.parse(inspect.getsource(base.collect)).body[0];b=ast.parse(inspect.getsource(candidate.collect)).body[0]
    expected=ast.parse("if sha256(ROOT/'oracle_source_closure_v2_20261106.py')!=V2_SHA256:raise ValueError('Pinned qualifiedv2source closure collector changed')\nlookup=PathLookupEpoch(ROOT)").body
    if ast.dump(b.body[1])!=ast.dump(expected[0]) or ast.dump(b.body[2])!=ast.dump(expected[1]):raise ValueError('New collector pin/lookup prelude differs')
    del b.body[1:3]
    tail=b.body[-3:]
    if not isinstance(tail[0],ast.Assign) or ast.dump(tail[0].targets[0])!=ast.dump(ast.Name('result',ast.Store())) or ast.dump(tail[1])!=ast.dump(ast.parse('lookup.verify()').body[0]) or ast.dump(tail[2])!=ast.dump(ast.parse('return result').body[0]):raise ValueError('New collector final guard/return differs')
    b.body[-3:]=[ast.Return(tail[0].value)];counts=dict(resolve=0,is_file=0,hash=0,read_json=0)
    class Revert(ast.NodeTransformer):
        def visit_Call(self,node):
            node=self.generic_visit(node)
            if isinstance(node.func,ast.Attribute) and isinstance(node.func.value,ast.Name) and node.func.value.id=='lookup':
                name=node.func.attr
                if name not in counts or len(node.args)!=1 or node.keywords:raise ValueError('Unqualified lookup delegation')
                counts[name]+=1
                if name in ['resolve','is_file']:return ast.Call(ast.Attribute(node.args[0],name,ast.Load()),[],[])
                node.func=ast.Name('sha256' if name=='hash' else 'read_json',ast.Load())
            return node
    b=Revert().visit(b)
    if counts!=dict(resolve=2,is_file=2,hash=2,read_json=3) or ast.dump(a)!=ast.dump(b):raise ValueError('Collector contains a delta outside explicit guarded lookup/content delegation')
    return dict(passed=True,baseSha256=sha256(ROOT/'oracle_source_closure_v2_20261106.py'),candidateSha256=sha256(ROOT/'oracle_source_closure_v3_20261106.py'),lookupSha256=sha256(ROOT/'collector_path_lookup_epoch_20261106.py'),replacedCalls=counts,allOtherCollectorASTIdentical=True,extraStatements=['Qualifiedv2code pin','Fresh run-local path/type/content facts','Final fact/content guard before unchanged result'])


def make_fixture(root):
    with patch.object(fixture_module,'WORK',WORK):fixture_module.fixture(root)
    for name in ['oracle_source_closure_20261031.py','oracle_source_closure_v2_20261106.py']:shutil.copyfile(ROOT/name,root/name)


def run(module,root):
    baseline=fixture_module.snapshot(root);lookup=[];factory=candidate.PathLookupEpoch
    def observe(value):instance=factory(value);lookup.append(instance);return instance
    begin=time.perf_counter()
    with patch.object(module,'ROOT',root),patch.object(module,'SEARCH',[root,root/'evidence/application',root/'evidence/encounter',root/'evidence/save',root/'nonmatching/encounter']),patch.object(candidate,'PathLookupEpoch',observe),patch('builtins.print'):result=module.collect()
    elapsed=time.perf_counter()-begin
    if fixture_module.snapshot(root)!=baseline:raise ValueError('Private bounded input/directory epoch changed')
    return result,dict(collector=module.__name__,elapsedSecondsIncludingAllGuards=elapsed,outputSha256=fixture_module.digest(result),paths=len(result['sourceAndEvidenceHashes']),lookup=lookup[0].summary() if lookup else None)


def controls(parent):
    rows=[]
    def root(name):path=parent/name;path.mkdir(parents=True);return path
    def rejected(name,cache,mutate):
        mutate()
        try:cache.verify()
        except LookupEpochChanged as error:rows.append(dict(case=name,rejected=True,reason=str(error)))
        else:raise ValueError('Changed lookup epoch accepted: '+name)
    r=root('missing-file');p=r/'future.py';cache=PathLookupEpoch(r);cache.resolve(p);cache.is_file(p);rejected('missing-to-file',cache,lambda:p.write_text('VALUE=1\n'))
    r=root('file-directory');p=r/'unit.py';p.write_text('VALUE=1\n');cache=PathLookupEpoch(r);cache.resolve(p);cache.is_file(p);cache.hash(p)
    def file_dir():p.unlink();p.mkdir()
    rejected('file-to-directory',cache,file_dir)
    r=root('directory-file');p=r/'parent';p.mkdir();cache=PathLookupEpoch(r);cache.resolve(p/'absent.py');cache.is_file(p/'absent.py')
    def directory_file():p.rmdir();p.write_text('not a directory')
    rejected('parent-directory-to-file',cache,directory_file)
    r=root('same-size');p=r/'unit.py';p.write_bytes(b'VALUE=1\n');saved=p.stat();cache=PathLookupEpoch(r);cache.resolve(p);cache.is_file(p);cache.hash(p)
    def same_size():p.write_bytes(b'VALUE=2\n');os.utime(p,ns=(saved.st_atime_ns,saved.st_mtime_ns))
    rejected('same-size-content-restored-mtime',cache,same_size)
    p.write_bytes(b'VALUE=1\n')
    try:cache.verify()
    except LookupEpochChanged:rows.append(dict(case='observed-change-then-restored-epoch',rejected=True))
    else:raise ValueError('Restored observed change was accepted')
    r=root('registry-change');write_json(r/'recovery.json',dict(oracles=[],batches=[]));cache=PathLookupEpoch(r);rejected('registry-content-changed',cache,lambda:write_json(r/'recovery.json',dict(oracles=[],batches=[dict(report='changed')])) )
    r=root('optional-interpreted');cache=PathLookupEpoch(r);rejected('missing-interpreted-registry-created',cache,lambda:write_json(r/'interpreted-recovery.json',dict(batches=[])))
    r=root('unrelated-neighbor');p=r/'unit.py';p.write_text('VALUE=1\n');cache=PathLookupEpoch(r);cache.resolve(p);cache.is_file(p);cache.hash(p);(r/'unreferenced-sibling.py').write_text('VALUE=2\n');cache.verify();rows.append(dict(case='unqueried-unrelated-sibling-does-not-freeze-whole-tree',passed=True))
    r=root('junction');a=r/'a';b=r/'b';a.mkdir();b.mkdir();(a/'unit.py').write_text('VALUE=1\n');shutil.copyfile(a/'unit.py',b/'unit.py');alias=r/'alias';script=r/'junction.ps1';script.write_text('param([string]$junctionPath,[string]$targetPath)\nNew-Item -ItemType Junction -Path $junctionPath -Target $targetPath | Out-Null\n')
    def junction(target):
        if not target.resolve().is_relative_to(r.resolve()) or not alias.parent.resolve().is_relative_to(r.resolve()):raise ValueError('Owned junction fixture escaped')
        result=subprocess.run(['powershell','-NoProfile','-NonInteractive','-File',str(script),str(alias),str(target)],capture_output=True,text=True)
        if result.returncode:raise ValueError(('Owned junction creation failed',result.stdout,result.stderr))
    junction(a);cache=PathLookupEpoch(r);cache.resolve(alias/'unit.py');cache.is_file(a/'unit.py');cache.hash(a/'unit.py')
    def retarget():os.rmdir(alias);junction(b)
    rejected('same-content-junction-target-changed',cache,retarget)
    return rows


def execute():
    if WORK!=ROOT/'work/w6pc' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/path-lookup-next':raise ValueError('New path-lookup experiment directories differ')
    proof=ast_proof();root=WORK/('bounded-'+uuid.uuid4().hex[:12]);make_fixture(root);samples=[];outputs=[]
    for module in [base,candidate,candidate,base]:result,sample=run(module,root);outputs.append(result);samples.append(sample)
    if any(value!=outputs[0] for value in outputs[1:]) or outputs[0]['missingRequiredPaths']:raise ValueError('Bounded complete collector output differs')
    comparisons=[]
    for name,path,changed in [('missing-required-source',root/'src/family000/module.py',None),('malformed-optional-json',root/'evidence/reports/report000.json',b'{broken')]:
        saved=path.read_bytes()
        if changed is None:path.unlink()
        else:path.write_bytes(changed)
        try:
            a,_=run(base,root);b,_=run(candidate,root)
            if a!=b:raise ValueError('Original required/invalid-input behavior differs: '+name)
            comparisons.append(dict(case=name,completeOriginalOutputEqual=True,missingRequiredPaths=a['missingRequiredPaths']))
        finally:path.write_bytes(saved)
    if any('/work/' in '/'+p for p in outputs[0]['sourceAndEvidenceHashes']):raise ValueError('Excluded fixture payload captured')
    rows=controls(WORK/('controls-'+uuid.uuid4().hex[:12]));old=statistics.median(s['elapsedSecondsIncludingAllGuards'] for s in samples if s['collector']==base.__name__);new=statistics.median(s['elapsedSecondsIncludingAllGuards'] for s in samples if s['collector']==candidate.__name__)
    receipt=dict(passed=True,sourceCredit=0,generatorSha256=sha256(__file__),astProof=proof,fixture=root.relative_to(ROOT).as_posix(),samples=samples,baseMedianSeconds=old,candidateMedianSecondsIncludingAllGuards=new,observedBoundedSpeedRatio=old/new,completeOutputsEqual=True,behaviorComparisons=comparisons,mutationControls=rows,excludedWorkAndSkippedVectorPayloadsPreserved=True,noLiveStageOrFrozenHelperChanged=True,limits=['This is a private64family fixture, not a full real-epoch equivalence or production qualification.','Every unique resolution/file-type/missing fact is recomputed; captured contents and registry/preferences/interpreted-registry hashes are checked at end, with sticky observed-change rejection.','Directory facts track queried-parent type/identity without freezing unrelated directory entries. Full immutable-snapshot inventory/content guards are also required for the real comparison.'])
    write_json(LANE/'bounded-v3-equivalence.json',receipt);print(dict(passed=True,baseMedianSeconds=old,candidateMedianSeconds=new,observedFixtureRatio=old/new,controls=len(rows),receiptSha256=sha256(LANE/'bounded-v3-equivalence.json')))


if __name__=='__main__':execute()
