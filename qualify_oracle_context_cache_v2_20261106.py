import ast
import copy
import inspect
import statistics
import time
import uuid
from pathlib import Path
from unittest.mock import patch
from project import ROOT,write_json,sha256
import oracle_source_closure_20261031 as old
import oracle_source_closure_v2_20261106 as new
from wave20261105_source_capture_perf_bench import fixture,snapshot,digest,WORK,LANE


def ast_proof():
    original=ast.parse(inspect.getsource(old.collect)).body[0];candidate=ast.parse(inspect.getsource(new.collect)).body[0];guard=ast.parse("if sha256(ROOT/'oracle_source_closure_20261031.py')!=LEGACY_SHA256:raise ValueError('Pinned legacy source closure collector changed')").body[0];cache=ast.parse('parent_context={}').body[0]
    if ast.dump(candidate.body[0])!=ast.dump(guard) or ast.dump(candidate.body[1])!=ast.dump(cache):raise ValueError('New collector guard/cache prelude differs')
    candidate.body=candidate.body[2:];calls=0;expression=ast.parse("required_hashes or parent.relative_to(ROOT).parts and parent.relative_to(ROOT).parts[0] in {'nonmatching','config'}",mode='eval').body;expected=ast.dump(ast.parse('_parent_requires_hashes(required_hashes,parent,ROOT,parent_context)',mode='eval').body)
    class Revert(ast.NodeTransformer):
        def visit_Call(self,node):
            nonlocal calls
            if ast.dump(node)==expected:calls+=1;return copy.deepcopy(expression)
            return self.generic_visit(node)
    candidate=Revert().visit(candidate)
    if calls!=1 or ast.dump(candidate)!=ast.dump(original):raise ValueError('New collector contains an unqualified semantic delta outside one pure-context expression')
    return dict(passed=True,legacySourceSha256=sha256(ROOT/'oracle_source_closure_20261031.py'),newSourceSha256=sha256(ROOT/'oracle_source_closure_v2_20261106.py'),exactExpressionReplacements=1,extraStatements=['Pinned legacy code identity guard','Fresh per-invocation pure-context dictionary'],allOtherCollectorASTIdentical=True,filesystemOrContentOrRegistryCaches=False)


def controls():
    cache={};rows=[];root=ROOT/'work/w5cp/context-control-root'
    for required,parent in [(False,root),(False,root/'config'),(False,root/'nonmatching/x'),(False,root/'evidence/reports'),(True,root/'evidence/reports'),(False,root/'Config')]:
        parts=parent.relative_to(root).parts;expected=bool(required or parts and parts[0] in {'nonmatching','config'});actual=new._parent_requires_hashes(required,parent,root,cache)
        if actual!=expected:raise ValueError('New lexical context/short-circuit/exact-case behavior differs')
        rows.append(dict(required=required,parent=parent.relative_to(root).as_posix(),expected=expected,exact=True))
    try:new._parent_requires_hashes(False,root.parent,root,cache)
    except ValueError:rows.append(dict(case='outside-root-parent',sameOriginalValueError=True))
    else:raise ValueError('New context cache weakened parent boundary')
    return rows


def execute():
    proof=ast_proof();rows=controls();root=WORK/('qualified-v2-'+uuid.uuid4().hex);fixture(root,8);(root/'oracle_source_closure_20261031.py').write_bytes((ROOT/'oracle_source_closure_20261031.py').read_bytes());baseline=snapshot(root);samples=[];outputs=[]
    for module in [old,new,new,old]:
        start=time.perf_counter()
        with patch.object(module,'ROOT',root),patch.object(module,'SEARCH',[root,root/'evidence/application',root/'evidence/encounter',root/'evidence/save',root/'nonmatching/encounter']),patch('builtins.print'):result=module.collect()
        elapsed=time.perf_counter()-start;outputs.append(result);samples.append(dict(collector=module.__name__,elapsedSeconds=elapsed,outputSha256=digest(result),closurePaths=len(result['sourceAndEvidenceHashes'])))
        if snapshot(root)!=baseline:raise ValueError('Qualified-v2 fixture epoch changed')
    if any(r!=outputs[0] for r in outputs[1:]):raise ValueError('Actual new-v2 collector output differs from original')
    write_json(LANE/'new-v2-ast-and-controls.json',dict(passed=True,sourceCredit=0,astProof=proof,contextControls=rows,actualVersionFixtureSamples=samples,completeOriginalOutputsEqual=True,generatorSha256=sha256(__file__),notFullRealEpochProof=True))
    print(dict(passed=True,contextControls=len(rows),exactASTDeltaSites=1,fixturePaths=len(outputs[0]['sourceAndEvidenceHashes']),newCollectorSha256=proof['newSourceSha256']))


if __name__=='__main__':execute()
