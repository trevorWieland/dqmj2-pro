import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
import link_runtime_unit as L
import unicorn
from wave20261106_game_main_arm_next_third_build import build
from wave20261106_game_main_arm_next_third_models import NAMES,fixtures,run
from wave20261106_game_main_arm_next_third_controls import execute as controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/game-main-arm-next/third'
SOURCE=ROOT/'src/runtime/parallel_wave20261105/game-main-arm-next/third'
WORK=ROOT/'work/w6gm/third-proof'


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
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/game-main-arm-next/third' or SOURCE!=ROOT/'src/runtime/parallel_wave20261105/game-main-arm-next/third' or WORK!=ROOT/'work/w6gm/third-proof':raise ValueError('Exact new packet directories differ')
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
    dispatch=fixtures('0207211c');counter=fixtures('02071b28');route=fixtures('02073090');page=fixtures('0207313c')
    negatives=[mutation('wrong-record-stride','0207211c','offset=index*12','offset=index*16',[f for f in dispatch if f['index'] in [1,2]],main),
               mutation('wrong-flag-position','0207211c','1U<<(index-3)','1U<<(index-2)',[f for f in dispatch if 3<=f['index']<=9 and f['flags']==255],main),
               mutation('stale-pre-provider-counter','02071b28','u32 amount=native_fn_02065d28(native_data_020daf42[i*2]);\n        result=native_data_021c50e8.counter-amount;','u32 cached=native_data_021c50e8.counter;\n        u32 amount=native_fn_02065d28(native_data_020daf42[i*2]);\n        result=cached-amount;',[f for f in counter if f['mutate']],main),
               mutation('wrong-signed-id','02071b28','native_fn_02065d28(native_data_020daf42[i*2])','native_fn_02065d28((u8)native_data_020daf42[i*2])',counter,main),
               mutation('wrong-widget-id','02073090','native_fn_02049ad0(25)','native_fn_02049ad0(26)',route,main),
               mutation('wrong-route-option','02073090','if(option!=0)','if(option==0)',route,main),
               mutation('wrong-nibble','0207313c','native_data_021c5a24.flags.low','native_data_021c5a24.flags.high',[f for f in page if bool(f['flags']&15)!=bool(f['flags']>>4)],main),
               mutation('wrong-category-status','0207313c','status=15','status=14',[f for f in page if f['kind']==26 and f['flags']&15==0],main)]
    control=controls(rows);write_json(LANE/'binding-layout-controls.json',control)
    raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode();artifact=LANE/'traces.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0))
    limits=['Four complete ordinary-C functions/552B from exclusively admitted ARM9 main scope. Explicit pinned MW C99 and genuine whole links preserve every native instruction/pool byte, original ELF names/relocations and ARM mapping. No assembly algorithm, instruction/object/register patch, fabricated alias or shared pipeline change.',
            '57 independent original/source fixture pairs require actual caller returns, full GPR/CPSR, exact provider call/order/stack observations, writes and8MiB RAM equality. They cover dispatcher ranges/default/high unsigned index, fresh detail pointer changes, record12/raw bitmask forwarding, signed stride2 ID lookup, nine modulo32 counter debits with provider mutations, each fresh widget pointer to qualified ov000 providers, query/option branches, actual unsigned nibble layout, signed16 index and category1/2/26/default behavior.',
            'Counter fixtures use explicitly recorded synthetic bytes in private RAM for the initialized ID lookup to exercise sign boundaries; original module/data/compiler input files remain unchanged. The17-byte initialized prefix, nine stride2 reads and original signed-byte/loop words are narrowly bound to one116-byte caller, with zero data ownership/storage credit and no original complete table extent assertion.',
            'Six original BSS/data literal origins require exact immutable original inventory/load/pool/PC-relative read witnesses. One initialized data(any) record uses a new narrow validator matching the established initialized-table contract; original branch/common BSS validators remain unchanged. Original module/CPU/program/mode and same numeric address in another overlay must reject.',
            'All callees are scripted measured ABI boundaries; no native provider body executes or gains credit. Their memory/register/flag effects are deliberate fixture contracts. UI/control names, complete original allocations, asynchronous hardware behavior and untested ABI domains remain unproved; BSS views may alias and carry zero storage credit.',
            'Eight genuine wrong-C variants reject independent stride/bit/sign/freshness/widget/option/nibble/category models. Binding/data/prefix/prototype/native geometry negatives are required. Diagnostic required-prototype compilation leaves executable sections unchanged; producer flags stay fixed. No repeated broad fixture products are added beyond distinct behavior boundaries.',
            'Earlier sealed packets remain immutable. This552B subset still awaits coordinator acceptance; larger scheduling-sensitive source drafts remain uncredited and source-only copied-root replay is not a source-only whole-ROM/platform completion claim.']
    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='main',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes'] for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,nativeSymbols={n:b['address'] for n,b in symbols.items()},nativeSymbolModules={n:b['module'] for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,negativeEvidence=negatives,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=__import__('hashlib').sha256(raw).hexdigest()),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=len(rows),bytes=sum(r['bytes'] for r in rows),cases=len(traces)),flush=True)


if __name__=='__main__':execute()
