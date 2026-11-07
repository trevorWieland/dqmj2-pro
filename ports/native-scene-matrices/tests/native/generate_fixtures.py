import importlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode=True

def braces(values):return '{'+','.join(str(v)for v in values)+'}'


def generate(target):
    folder=Path(__file__).resolve().parents[1]
    positions=json.loads((folder/'position/copied-position-fixtures.json').read_text(encoding='utf-8'))
    scenes=json.loads((folder/'scene/copied-synthetic-fixtures-v2.json').read_text(encoding='utf-8'))
    lines=[];pointers=[]
    for i,f in enumerate(positions):
        lines.append('static const uint8_t posdata'+str(i)+'[]='+braces(f['source'])+';')
        rows=[]
        for ordinal,e in enumerate(f['expected']):
            ids=[e[k]for k in ['event','reference','submission','header','slot','parameter','opcode']]+[ordinal,e['local']]
            rows.append('{'+braces(e['xyz'])+','+braces(e['position'])+','+braces(ids)+'}')
        lines.append('static const ExpectedPosition posout'+str(i)+'[]={'+','.join(rows or['{{0},{0},{0}}'])+'};')
        pointers.append('{posdata'+str(i)+','+str(len(f['source']))+','+str(f['known'])+','+braces(f['xyz'])+',posout'+str(i)+','+str(len(rows))+','+braces(f['finalXYZ'])+','+str(f['finalKnown'])+'}')
    lines.append('static const PositionFixture position_fixtures[]={'+','.join(pointers)+'};');pointers=[]
    for i,f in enumerate(scenes):
        lines.append('static const uint8_t scenedata'+str(i)+'[]='+braces(f['data'])+';')
        lines.append('static const uint32_t sceneevents'+str(i)+'[][6]={'+','.join(braces(e)for e in f['expectedEvents'])+'};')
        snapshots=['{'+str(e['valid_slots'])+',{'+','.join(braces(m)for m in e['matrices'])+'}}'for e in f['expectedMatrices']]
        lines.append('static const ExpectedSnapshot scenesnaps'+str(i)+'[]={'+','.join(snapshots or['{0,{{0}}}'])+'};')
        pointers.append('{scenedata'+str(i)+','+str(len(f['data']))+','+braces(f['defaults'])+',sceneevents'+str(i)+','+str(len(f['expectedEvents']))+',scenesnaps'+str(i)+','+str(len(snapshots))+'}')
    lines.append('static const SceneFixture scene_fixtures[]={'+','.join(pointers)+'};');pointers=[]
    sys.path.insert(0,str(folder/'warm'))
    simple=importlib.import_module('synthetic_cases').simple
    reference=importlib.import_module('warm_api').reference
    for i in range(4):
        owner,context,entry=simple(i);output,effect=reference(owner,context,entry)
        names=[]
        for tag,value in zip(['owner','context','entry','output','effect'],[owner,context,entry,output,effect]):
            name='warm'+str(i)+tag;names.append(name)
            lines.append('static const uint8_t '+name+'[]='+braces(bytes(value))+';')
        pointers.append('{'+','.join(names)+'}')
    lines.append('static const WarmFixture warm_fixtures[]={'+','.join(pointers)+'};')
    assert len(lines)<500
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return dict(sceneModels=len(scenes),positionModels=len(positions),positionRecords=sum(len(f['expected'])for f in positions),
        sceneReferences=sum(len(f['expectedMatrices'])for f in scenes),sceneSubmissions=sum(e[5]==1 for f in scenes for e in f['expectedEvents']),warmCases=4,
        refusals=2*len(positions)+sum(bool(f['expected'])for f in positions)+8)


if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: generate_fixtures.py OUTPUT_HEADER')
    print(json.dumps(generate(Path(sys.argv[1]).resolve())))
