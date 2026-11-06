import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
import link_runtime_unit as L
import unicorn
from wave20261106_game_main_arm_next_fifth_build import build
from wave20261106_game_main_arm_next_fifth_models import NAMES,fixtures,run
from wave20261106_game_main_arm_next_fifth_controls import execute as controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/game-main-arm-next/fifth'
SOURCE=ROOT/'src/runtime/parallel_wave20261105/game-main-arm-next/fifth'
WORK=ROOT/'work/w6gm/fifth-proof'


def mutation(label,old,new,selected,main):
    text=(SOURCE/'0207154c.c').read_text()
    if text.count(old)!=1 or not selected:raise ValueError('Initializer mutation ambiguous or empty')
    folder=WORK/'negative'/label;folder.mkdir(parents=True,exist_ok=True);source=folder/'source.c';source.write_text(text.replace(old,new));shutil.copyfile(SOURCE/'initializer.h',folder/'initializer.h')
    row,body=build(source,folder/'build',True);rejected=[]
    for ordinal,fixture in enumerate(selected):
        result=run(row,body,fixture,main,ordinal)
        if not result['modelFailures'] or not result['actualTopReturn']:raise ValueError(('Wrong initializer escaped model',label,fixture))
        rejected.append(dict(fixture=fixture,failures=result['modelFailures'],actualTopReturn=result['actualTopReturn']))
    return dict(case=label,old=old,new=new,proof=row,rejected=rejected)


def execute():
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/game-main-arm-next/fifth' or SOURCE!=ROOT/'src/runtime/parallel_wave20261105/game-main-arm-next/fifth' or WORK!=ROOT/'work/w6gm/fifth-proof':raise ValueError('Exact new initializer paths differ')
    if sys.version_info[:3]!=(3,13,5) or unicorn.__version__!='2.1.4':raise ValueError('Pinned fixture runtime differs')
    inputs=read_json(LANE/'inputs.json')
    for pin in inputs['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Frozen initializer input changed: '+pin['path'])
    if {format(int(r['address'],0),'08x') for r in inputs['entries']}!=set(NAMES):raise ValueError('Selected initializer differs')
    info,main,unused=L.measured_module('main');rows=[];traces=[];symbols={}
    for name in NAMES:
        entry=next(r for r in inputs['entries'] if int(r['address'],0)==int(name,16));row,body=build(ROOT/entry['source'],WORK/name/'positive')
        if (row['targetSha256'],row['bytes'])!=(entry['targetSha256'],entry['bytes']):raise ValueError('Admitted complete initializer differs')
        for symbol,binding in row['nativeSymbolEntries'].items():
            binding.setdefault('program','')
            if symbol in symbols and symbols[symbol]!=binding:raise ValueError('Report native symbol conflict')
            symbols[symbol]=binding
        start=int(row['address'],0)-0x02000000;native=main[start:start+row['bytes']]
        for ordinal,fixture in enumerate(fixtures(name)):
            original=run(row,native,fixture,main,ordinal);rebuilt=run(row,body,fixture,main,ordinal)
            if original!=rebuilt or original['modelFailures'] or not original['actualTopReturn']:raise ValueError(('Native/C initializer or model differs',ordinal,original,rebuilt))
            traces.append(dict(address=row['address'],fixture=fixture,result=original))
        rows.append(row);print('proved',name,row['bytes'],len(fixtures(name)),flush=True)
    selected=fixtures('0207154c')
    negatives=[mutation('wrong-row','&context->rows[1]','&context->rows[2]',selected,main),
               mutation('wrong-option',',59,0,2,',',59,0,3,',selected,main),
               mutation('discard-fresh-base','context->cursor25c+=amount;','context->cursor25c=amount;',[f for f in selected if f['allocated']!=0],main),
               mutation('wrong-name','native_fn_0205ff80(path);',"path[0]='X';native_fn_0205ff80(path);",selected,main)]
    control=controls(rows);write_json(LANE/'binding-layout-controls.json',control)
    raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode();artifact=LANE/'traces.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0))
    limits=['One complete ordinary-C92-byte resource initializer from the exclusive32-function main claim. Actual pinned MW C99 and full genuine native links preserve the complete function, original ELF names/relocations and ARM mapping. No binary/instruction/register patch, algorithm ASM or new callable alias.',
            'Eight focused original/source fixture pairs require actual top returns and full GPR/CPSR, calls/stack words, writes and8MiB RAM equality. Independent checks cover the terminated resource name, row1 at offset1c, allocator parameters59/0/2, provider mutations before and during allocation, fresh cursor addition modulo32 and untouched context bytes.',
            'All five imported bodies remain opaque scripted ABI boundaries with caller-saved/flag clobbers and zero native callee execution/source credit. The C function has void return type; raw returned registers are machine observations, not a promised semantic return value.',
            'The one initialized string reference has exact original caller/hash/pool/PC-load/zero-addend/inventory witnesses. Its22-byte terminated ASCII prefix is a validation reference with zero data/authorship/storage credit. The608-byte context is only a minimum ABI view.',
            'Four real wrong-C variants reject independent row/option/fresh-read/name models. CPU/program/module/mode/origin/data/prototype and actual compiler geometry negatives reject. Required-prototype diagnostics preserve executable sections and do not replace production flags.',
            'Neighboring960/992-byte typed state drafts and all other unselected residuals remain uncredited. Earlier frozen packets are unchanged. Copied-root source replay requires serialized coordinator acceptance and is not a complete source-only ROM/platform proof.']
    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='main',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes'] for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,nativeSymbols={n:b['address'] for n,b in symbols.items()},nativeSymbolModules={n:b['module'] for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,negativeEvidence=negatives,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=__import__('hashlib').sha256(raw).hexdigest()),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=len(rows),bytes=sum(r['bytes'] for r in rows),cases=len(traces)),flush=True)


if __name__=='__main__':execute()
