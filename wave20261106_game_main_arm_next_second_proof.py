import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
import link_runtime_unit as L
import unicorn
from wave20261106_game_main_arm_next_second_build import build
from wave20261106_game_main_arm_next_second_models import NAMES,fixtures,run
from wave20261106_game_main_arm_next_second_controls import execute as controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/game-main-arm-next/second'
SOURCE=ROOT/'src/runtime/parallel_wave20261105/game-main-arm-next/second'
WORK=ROOT/'work/w6gm/second-proof'


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
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/game-main-arm-next/second' or SOURCE!=ROOT/'src/runtime/parallel_wave20261105/game-main-arm-next/second' or WORK!=ROOT/'work/w6gm/second-proof':raise ValueError('Exact new packet directories differ')
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
    selected=fixtures('02072568')
    signed=fixtures('020728ec');point=fixtures('02072de8')
    negatives=[mutation('wrong-word-change-test','02072568','if(previous==value)return','if(previous!=value)return',selected,main),
               mutation('wrong-signed-byte','020728ec','native_fn_02049ad0(native_data_021c5a11[index].value)','native_fn_02049ad0((u8)native_data_021c5a11[index].value)',[f for f in signed if f['first']>=128],main),
               mutation('wrong-widget-field','020728ec','widget->field5=','widget->prefix[4]=',signed[:8],main),
               mutation('wrong-coordinate-scale','02072de8','point.x=native_data_021c5a13[object->index].value*8','point.x=native_data_021c5a13[object->index].value*4',[f for f in point if f['x']!=0],main),
               mutation('wrong-option-inversion','02072de8','if(option!=0)','if(option==0)',point,main),
               mutation('wrong-component-offset','02072de8','native_fn_0204b380((u8 *)object+8,0)','native_fn_0204b380((u8 *)object+12,0)',point,main)]
    control=controls(rows);write_json(LANE/'binding-layout-controls.json',control)
    raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode();artifact=LANE/'traces.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0))
    limits=['Three complete ordinary-C functions/232B from exclusively admitted ARM9 main scope; pinned explicit C99 and genuine MW links preserve full native code/pool bytes, original ELF relocations/names and ARM mapping. No ordinary logic ASM, binary patches, aliases or global pipeline changes.',
            '160 original/rebuilt fixture pairs require actual caller returns, full GPR/CPSR, provider calls/stack words, writes and8MiB RAM equality. They cover full32-bit equality/update/invalidation, signed8 provider arguments and fresh post-provider field reads,9-byte column indices0..7, byte coordinates scaled to signed16 points, mutable object index and opaque provider effects, both option branches and final provider-result forwarding.',
            'Original five storage literals are qualified by unchanged strict branch/data validators plus exact immutable caller/ABS32/zero-addend/load/inventory/actual ARM PC-read witnesses. BSS/byte-column/word tables are zero-credit bindings; no complete allocation, original data authorship or storage credit is asserted.',
            'Seven provider bodies are modeled at measured call/ABI boundaries only, with caller-saved/flag clobbers and scripted memory effects; none execute or gain source credit. Semantic widget/point names are provisional ABI views. Additional uncredited scheduling-sensitive routines remain outside the closed subset.',
            'Six real wrong-C changes must fail independent word/sign/field/scale/option/component models. CPU/program/module/mode/address/kind, original literal/pool/inventory/load/stride/extent/storage mutations, required-prototype diagnostics and actual native geometry negatives reject; production compiler flags remain unchanged.',
            'All earlier packet pins stay immutable. Source-only copied roots rebuild every object and full genuine link without copying cached work; serialized shared acceptance is required for credit and no full source-only ROM/platform execution is claimed.']
    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='main',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes'] for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,nativeSymbols={n:b['address'] for n,b in symbols.items()},nativeSymbolModules={n:b['module'] for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,negativeEvidence=negatives,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=__import__('hashlib').sha256(raw).hexdigest()),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=len(rows),bytes=sum(r['bytes'] for r in rows),cases=len(traces)),flush=True)


if __name__=='__main__':execute()
