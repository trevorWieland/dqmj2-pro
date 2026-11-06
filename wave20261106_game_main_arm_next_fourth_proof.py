import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
import link_runtime_unit as L
import unicorn
from wave20261106_game_main_arm_next_fourth_build import build
from wave20261106_game_main_arm_next_fourth_models import NAMES,fixtures,run
from wave20261106_game_main_arm_next_fourth_controls import execute as controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/game-main-arm-next/fourth'
SOURCE=ROOT/'src/runtime/parallel_wave20261105/game-main-arm-next/fourth'
WORK=ROOT/'work/w6gm/fourth-proof'


def mutation(label,name,old,new,selected,main):
    text=(SOURCE/(name+'.c')).read_text()
    if text.count(old)!=1 or not selected:raise ValueError('Semantic mutation ambiguous or empty')
    folder=WORK/'negative'/label;folder.mkdir(parents=True,exist_ok=True);source=folder/'source.c';source.write_text(text.replace(old,new));shutil.copyfile(SOURCE/'context.h',folder/'context.h')
    row,body=build(source,folder/'build',True);rejected=[]
    for ordinal,fixture in enumerate(selected):
        result=run(row,body,fixture,main,ordinal)
        if not result['modelFailures'] or not result['actualTopReturn']:raise ValueError(('Wrong whole-C logic escaped independent model',label,fixture))
        rejected.append(dict(fixture=fixture,failures=result['modelFailures'],actualTopReturn=result['actualTopReturn']))
    return dict(case=label,old=old,new=new,proof=row,rejected=rejected)


def execute():
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/game-main-arm-next/fourth' or SOURCE!=ROOT/'src/runtime/parallel_wave20261105/game-main-arm-next/fourth' or WORK!=ROOT/'work/w6gm/fourth-proof':raise ValueError('Exact new packet directories differ')
    if sys.version_info[:3]!=(3,13,5) or unicorn.__version__!='2.1.4':raise ValueError('Pinned native fixture runtime differs')
    inputs=read_json(LANE/'inputs.json')
    for pin in inputs['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Frozen game input changed: '+pin['path'])
    if {format(int(r['address'],0),'08x') for r in inputs['entries']}!=set(NAMES):raise ValueError('Selected game subset differs')
    info,main,unused=L.measured_module('main');rows=[];traces=[];symbols={}
    for name in NAMES:
        entry=next(r for r in inputs['entries'] if int(r['address'],0)==int(name,16));row,body=build(ROOT/entry['source'],WORK/name/'positive')
        if (row['targetSha256'],row['bytes'])!=(entry['targetSha256'],entry['bytes']):raise ValueError('Whole admitted native span differs')
        for binding in row['nativeSymbolEntries'].values():binding.setdefault('program','')
        for symbol,binding in row['nativeSymbolEntries'].items():
            if symbol in symbols and symbols[symbol]!=binding:raise ValueError('Report-level native symbol conflict')
            symbols[symbol]=binding
        start=int(row['address'],0)-0x02000000;native=main[start:start+row['bytes']]
        for ordinal,fixture in enumerate(fixtures(name)):
            original=run(row,native,fixture,main,ordinal);rebuilt=run(row,body,fixture,main,ordinal)
            if original!=rebuilt or original['modelFailures'] or not original['actualTopReturn']:raise ValueError(('Actual original/C caller or model differs',name,ordinal,original,rebuilt))
            traces.append(dict(address=row['address'],fixture=fixture,result=original))
        rows.append(row);print('proved',name,row['bytes'],len(fixtures(name)),flush=True)
    selected=fixtures('02072b74')
    negatives=[mutation('wrong-x-extent','02072b74','(row->x+8)*8','(row->x+7)*8',[f for f in selected if f['mask']==1 and f['x']==95],main),
               mutation('closed-y-upper-bound','02072b74','sample->y<(row->y+2)*8','sample->y<=(row->y+2)*8',[f for f in selected if f['mask']==1 and f['x']==32 and f['y']==40],main),
               mutation('wrong-predicate-index','02072b74','native_fn_02072ed4((u8)index)','native_fn_02072ed4(0)',[f for f in selected if f['mask']==3 and f['x']==96 and f['y']==64],main),
               mutation('wrong-return-index','02072b74','return (s8)index','return (s8)(index+1)',[f for f in selected if f['mask']==3 and f['x']==32 and f['y']==24 and f['allowed']],main),
               mutation('wrong-failed-status','02072b74','*status=2','*status=1',[f for f in selected if f['mask']==3 and f['x']==32 and f['y']==24 and not f['allowed']],main),
               mutation('wrong-second-response','02072b74','native_fn_0205e7a8(-1,83)','native_fn_0205e7a8(-1,82)',[f for f in selected if f['mask']==3 and f['x']==96 and f['y']==64 and f['allowed'] and f['notify']],main)]
    control=controls(rows);write_json(LANE/'binding-layout-controls.json',control)
    raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode();artifact=LANE/'traces.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0))
    limits=['One complete ordinary-C248-byte caller from the exclusively admitted main scope. Actual pinned MW C99 and full genuine links preserve every original code/pool byte, original ELF names/relocations and ARM mapping; no binary/instruction/register patch, algorithm ASM or new callable alias.',
            '51 focused original/source fixture pairs require actual top returns and equality of full GPR/CPSR, calls/stack words, writes and8MiB RAM. Two nine-byte rows, enabled masks, both axes and half-open boundaries, first-row priority/overlap, required byte-index predicate argument, raw nonzero predicate/notification words, signed index/minus-one return, all response words and aliased status output are independently modeled.',
            'The missing actual one-byte index argument to02072ed4 is recovered from the original AND/store/call sequence; all three provider bodies remain opaque scripted ABI boundaries with caller-saved/flag clobbers and zero native callee execution/source credit. Higher-level UI/action names and original complete typedefs remain unproved.',
            'The original single BSS literal retains exact original caller/pool/PC-load/zero-addend/inventory namespace witnesses through unchanged branch/common data guards. Eighteen bytes is a minimum two-row ABI view with zero original allocation/authorship/storage credit.',
            'Six real wrong-C errors reject independent geometry/argument/return/status/response models. Function/data namespace, original literal/inventory/load/stride, required prototype and actual compiler geometry negatives reject. Diagnostic required-prototype mode preserves executable sections and does not replace production flags.',
            'All prior READY source/helper/input pins remain unchanged. Adjacent380-byte updater and narrow setter scheduling drafts are uncredited after bounded type/context investigation. Fresh source-only copied-root replay still requires serialized shared acceptance for credit and is not a complete source-only ROM/platform execution claim.']
    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='main',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes'] for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,nativeSymbols={n:b['address'] for n,b in symbols.items()},nativeSymbolModules={n:b['module'] for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,negativeEvidence=negatives,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=__import__('hashlib').sha256(raw).hexdigest()),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=len(rows),bytes=sum(r['bytes'] for r in rows),cases=len(traces)),flush=True)


if __name__=='__main__':execute()
