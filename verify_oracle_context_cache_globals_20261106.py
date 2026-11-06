import ast
import inspect
from project import ROOT,write_json,sha256
import oracle_source_closure_20261031 as old
import oracle_source_closure_v2_20261106 as new
LANE=ROOT/'evidence/lanes/parallel-wave20261105/source-capture-performance-next'


def execute():
    checks=[]
    for name in ['ROOT','SEARCH','EXCLUDED','SKIP','EXTENSIONS']:
        if getattr(old,name)!=getattr(new,name):raise ValueError('New collector changed legacy scope globals: '+name)
        checks.append(dict(name=name,exact=True))
    for name in ['read_json','write_json','sha256','required_json_reads']:
        if getattr(old,name) is not getattr(new,name):raise ValueError('New collector substituted legacy input/hash/static-reader implementation: '+name)
        checks.append(dict(name=name,sameCallableObject=True))
    if sha256(ROOT/'oracle_source_closure_20261031.py')!=new.LEGACY_SHA256:raise ValueError('New collector code identity guard is stale')
    expected=ast.parse("def _parent_requires_hashes(required,parent,root,cache):\n    if required:return True\n    key=str(parent)\n    if key not in cache:\n        parts=parent.relative_to(root).parts\n        cache[key]=bool(parts and parts[0] in {'nonmatching','config'})\n    return cache[key]\n")
    if ast.dump(ast.parse(inspect.getsource(new._parent_requires_hashes)))!=ast.dump(expected):raise ValueError('Context helper includes unqualified cache/behavior')
    result=dict(passed=True,sourceCredit=0,checks=checks,legacySourceSha256=sha256(ROOT/'oracle_source_closure_20261031.py'),newSourceSha256=sha256(ROOT/'oracle_source_closure_v2_20261106.py'),staticReaderSha256=sha256(ROOT/'static_json_reads_20261031.py'),exactContextHelperAST=True,noFilesystemOrSourceContentCache=True,generatorSha256=sha256(__file__))
    write_json(LANE/'new-v2-scope-globals.json',result);print(dict(passed=True,unchangedGlobalsOrCallables=len(checks),contextHelperExact=True))


if __name__=='__main__':execute()
