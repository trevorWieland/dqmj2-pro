import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
import link_runtime_unit as L
import unicorn
from wave20261106_game_main_arm_next_first_build import build
from wave20261106_game_main_arm_next_first_models import NAMES,fixtures,run
from wave20261106_game_main_arm_next_first_controls import execute as controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/game-main-arm-next/first'
SOURCE=ROOT/'src/runtime/parallel_wave20261105/game-main-arm-next/first'
WORK=ROOT/'work/w6gm/first-proof'


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
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/game-main-arm-next/first' or SOURCE!=ROOT/'src/runtime/parallel_wave20261105/game-main-arm-next/first' or WORK!=ROOT/'work/w6gm/first-proof':raise ValueError('Exact new packet directories differ')
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
    selected=fixtures('020720a4')
    negatives=[mutation('wrong-record-stride','020720a4','offset=index*12','offset=index*16',[f for f in selected if f['index']!=0],main),
               mutation('wrong-required-forwarded-arguments','020720a4','if(native_fn_020625bc()!=0)native_fn_0207211c(2,first,second);\n    else native_fn_0207211c(1,first,second);','if(native_fn_020625bc()!=0)native_fn_0207211c(2,second,first);\n    else native_fn_0207211c(1,second,first);',selected,main),
               mutation('wrong-predicate-branch','020720a4','native_fn_020625bc()!=0','native_fn_020625bc()==0',selected,main),
               mutation('wrong-first-mapping','020725e8','case 5:return 6','case 5:return 7',[dict(value=5)],main),
               mutation('wrong-second-mapping','020726d8','case 5:return 7','case 5:return 6',[dict(value=5)],main)]
    control=controls(rows);write_json(LANE/'binding-layout-controls.json',control)
    raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode();artifact=LANE/'traces.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0))
    limits=['Three complete ordinary-C functions/564B from exclusively admitted32/14732B ARM9 main card. Actual pinned MW C99 compilation and complete genuine links preserve original ELF names, original relocation payloads, ARM mapping and every native byte; no binary/instruction/register patches or algorithm ASM.',
            'Two unsigned switch mappings exercise all0..31 inputs plus unsigned high/default sentinels. The caller exercises10 measured12-byte records, both duplicate branches and both predicate branches with boundary raw word arguments. Every original/rebuilt run must actually return and agrees on full GPR/CPSR, provider calls/stack words, writes and8MiB RAM.',
            'Providers model only measured call/ABI boundaries, deliberately clobber caller-saved registers/flags and mutate context memory. Zero actual native callee bodies execute or gain source credit; semantic UI/layout names and complete original allocation remain unproved. ContextPrefix is only a136-byte ABI view, with pointer32/word32/record12/prefix16 compilation facts.',
            'Five genuine wrong-C variants reject through independent argument/stride/branch/mapping models. Original CPU/program/module/address/mode/function bindings, actual missing prototypes and actual malformed layout controls reject. Diagnostic -requireprotos/-w error recompilation leaves executable sections unchanged; production flags remain unchanged.',
            'Remaining29 functions/14168B are exclusively reserved and uncredited, including parked208B scheduling-only candidate and two giants. Serialized coordinator acceptance is required before source credit; no source-only ROM or platform execution claim.']
    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='main',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes'] for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,nativeSymbols={n:b['address'] for n,b in symbols.items()},nativeSymbolModules={n:b['module'] for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,negativeEvidence=negatives,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=__import__('hashlib').sha256(raw).hexdigest()),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=len(rows),bytes=sum(r['bytes'] for r in rows),cases=len(traces)),flush=True)


if __name__=='__main__':execute()
