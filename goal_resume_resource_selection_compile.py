import re
from pathlib import Path
from project import ROOT,read_json,sha256,write_json
import match_runtime as compiler

LANE=ROOT/'evidence/lanes/parallel-wave20261107/resource-selection-source1'
SOURCE=ROOT/'src/runtime/goal_resume20261107/resource_selection'
WORK=ROOT/'work/goal-resume-20261107/resource-selection-source1'
COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/sp1p5/mwccarm.exe'


def compare(source,directory):
    source=Path(source).resolve();directory=Path(directory).resolve()
    if not source.is_relative_to(SOURCE)and not source.is_relative_to(WORK):raise ValueError('Source escaped the exclusively reassigned resource family')
    if not directory.is_relative_to(WORK):raise ValueError('Resource compiler output escaped its disjoint work root')
    claim=read_json(LANE/'claim.json')
    if sha256(LANE/'claim.json')!='8cfabd4f47bb6ef3457da5a467c959444319ad89b0d73d4b8a79de15b4d9ded1':raise ValueError('Frozen resource claim changed')
    names=re.findall(r'\bnative_main_([0-9a-f]{8})\s*\(',source.read_text())
    if len(names)!=1 or int(names[0],16)not in{int(r['address'],0)for r in claim['claimedFunctions']}:raise ValueError('Source does not define one exclusively claimed function')
    for path,expected in claim['inputPins'].items():
        if sha256(ROOT/path)!=expected:raise ValueError('Pinned original resource input changed')
    saved=compiler.WORK,compiler.FLAGS
    try:
        compiler.WORK=directory;compiler.FLAGS=[*saved[1],'-lang','c99']
        return compiler.compare(source,'main','2','on',True,compiler=COMPILER)
    finally:compiler.WORK,compiler.FLAGS=saved


def main():
    for source in sorted(SOURCE.glob('*.c')):
        rows,unused=compare(source,WORK/'initial'/source.stem)
        write_json(WORK/'initial'/(source.stem+'.json'),rows)
        print([dict(name=r.get('name'),bytes=r.get('bytes'),compiled=r.get('compiledBytes'),matching=r.get('matchingBytes'),exact=r.get('exactAfterDeclaredRelocation'),failed=r.get('compileFailed'),stdout=r.get('stdout'),stderr=r.get('stderr'))for r in rows],flush=True)


if __name__=='__main__':main()
