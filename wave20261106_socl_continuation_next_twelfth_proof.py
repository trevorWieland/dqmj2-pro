import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
import link_runtime_unit as L
import unicorn
from wave20261106_socl_continuation_next_twelfth_build import build
from wave20261106_socl_continuation_next_twelfth_models import NAMES,fixtures
from wave20261106_socl_continuation_next_twelfth_execution import run
from wave20261106_socl_continuation_next_twelfth_controls import execute as controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/twelfth'
SOURCE=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/twelfth'
WORK=ROOT/'work/w6sc/twelfth-proof'


def mutation(name,label,old,new,selected,main,header=False):
    text=(SOURCE/(name+'.c')).read_text();context=(SOURCE/'context.h').read_text();target=context if header else text
    if target.count(old)!=1 or not selected:raise ValueError('Whole-C semantic mutation ambiguous or empty')
    folder=WORK/'negative'/label;folder.mkdir(parents=True,exist_ok=True);source=folder/'source.c';source.write_text(text if header else text.replace(old,new));(folder/'context.h').write_text(context.replace(old,new) if header else context)
    row,body=build(source,folder/'build',True);rejected=[]
    for i,fixture in enumerate(selected):
        result=run(row,body,fixture,main,i)
        if not result['modelFailures']:raise ValueError(('Wrong C escaped independent model',label,fixture))
        rejected.append(dict(fixture=fixture,failures=result['modelFailures'],actualTopReturn=result['actualTopReturn'],rejectedAtObservedProtocolBoundary=result['rejectedAtObservedProtocolBoundary']))
    return dict(case=label,caller=name,old=old,new=new,headerMutation=header,proof=row,rejected=rejected)


def negatives(main):
    cases=[]
    for name,label,old,new,index in [
        ('020928f8','wrong-consume-boundary','if(count>=','if(count>',2),
        ('020928f8','wrong-released-field','context->record=0;','context->record_length=0;',2),
        ('020928f8','wrong-partial-offset','context->record_offset+=count','context->record_offset-=count',0),
        ('02092854','wrong-held-data-gate','context->record && !context->record_hold','context->record && context->record_hold',0),
        ('02092854','wrong-read-start','native_fn_02091f54(context->record+context->record_offset','native_fn_02091f54(context->record',2),
        ('02092854','wrong-wait-error','native_fn_02092174(socket)==9','native_fn_02092174(socket)==8',10),
        ('02092854','wrong-reported-remaining','*count=context->record_length-context->record_offset;','*count=context->record_length;',0),
        ('02092938','wrong-maximum-record-boundary','amount>0x4805','amount>=0x4805',18),
        ('02092938','wrong-allocation-size','native_data_021cfd0c(amount)','native_data_021cfd0c(amount+1)',10),
        ('02092938','wrong-exact-completion','if(amount>=','if(amount>',20),
        ('02092938','wrong-hold-reset','context->record_hold=0;','context->record_hold=1;',8),
        ('02092938','wrong-copy-destination','context->record+context->record_offset','context->record',14),
        ('02092938','wrong-partial-advance','context->record_offset+=amount;','context->record_offset=amount;',14),
        ('02092938','wrong-parser-hold-gate','if(!context->record_hold)','if(context->record_hold)',10)]:cases.append(mutation(name,label,old,new,[fixtures(name)[index]],main))
    return cases


def execute():
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/twelfth' or SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/twelfth' or WORK!=ROOT/'work/w6sc/twelfth-proof':raise ValueError('Exact new production source/evidence/work paths differ')
    if sys.version_info[:3]!=(3,13,5) or unicorn.__version__!='2.1.4':raise ValueError('Pinned fixture runtime differs')
    inputs=read_json(LANE/'inputs.json')
    for p in inputs['files']:
        if sha256(ROOT/p['path'])!=p['sha256']:raise ValueError('Frozen continuation input changed: '+p['path'])
    if {format(int(r['address'],0),'08x') for r in inputs['entries']}!=set(NAMES):raise ValueError('Selected whole-function subset differs')
    info,main,unused=L.measured_module('main');rows=[];traces=[];symbols={}
    for name in NAMES:
        entry=next(r for r in inputs['entries'] if int(r['address'],0)==int(name,16));row,body=build(ROOT/entry['source'],WORK/name/'positive')
        if (row['bytes'],row['targetSha256'])!=(entry['bytes'],entry['targetSha256']):raise ValueError('Admitted whole native function changed')
        for symbol,binding in row['nativeSymbolEntries'].items():
            binding.setdefault('program','')
            if symbol in symbols and symbols[symbol]!=binding:raise ValueError('Complete report-level native binding conflict')
            symbols[symbol]=binding
        offset=int(row['address'],0)-0x02000000;native=main[offset:offset+row['bytes']]
        for i,fixture in enumerate(fixtures(name)):
            original=run(row,native,fixture,main,i);source=run(row,body,fixture,main,i)
            if original!=source or original['modelFailures'] or not original['actualTopReturn']:raise ValueError(('Native/source or independent model differs',name,i,original,source))
            traces.append(dict(caller=row['address'],fixture=fixture,result=original))
        rows.append(row);print('proved',name,row['bytes'],len(fixtures(name)),flush=True)
    negative=negatives(main);control=controls(rows);write_json(LANE/'binding-layout-controls.json',control)
    raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode();artifact=LANE/'traces.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0))
    limits=['Three complete464-byte ordinary-C Thumb read/receive/consume callers use pinned measured MW2.0/sp1p6/C99/O4,p/file-IPA/inline-on-noauto with genuine full links, complete original code/pools, original ELF symbols/relocations and actual Thumb mappings. No algorithm ASM, code/register/object patch, alias or prebuilt executable compiler input.', 'Independent models cover held data, read failure/free, parser hold/clear, wait/fill/error loops, unsigned remaining/count arithmetic and offset wrap, exact consumption/null pointer, incomplete/oversized/maximum headers, allocation failure, partial/exact/excess input, native copy spans and parser ownership flags. Context2096/socket72 are minimum measured field-access layouts, not whole original allocation/type recovery or storage claims.', 'The original allocator/release slots021cfd0c/021cfd38 are canonical configured BSS references, not initialized original targets. Exact literal/origin/full caller hashes and load/BLX/result instructions independently qualify only void*(u32) and void(void*) interfaces. Runtime callback identities/registration and storage/callee credit remain zero. Fresh controlled ARM/Thumb provider ABI returns and actual wrong-tag/declaration/site controls preserve that distinction.', 'Every positive actual native/source caller executes fully to real top return, comparing all GPR/CPSR, ordered modes/register/stack arguments, exact original indirect return sites, writes, PCs and8MiB RAM plus independent complete borrowed state and guards. Network/read/copy/parser and controlled callbacks are scripted ABI boundaries; original providers are never executed. Controlled-provider ABI bodies execute only in separately identified diagnostic probes with zero native credit.', 'Fourteen actual whole wrong-C variants reject arithmetic/gates/offsets/header limit/allocation/clamping/reset/copy/parser mistakes. Original full CPU/program/module/mode/body/hash/branch/load/addend/relocation completeness, actual required callable prototypes and compiler geometry are checked. Pre-return protocol rejection remains distinct from a returned positive fixture.', 'BSS callback pointers in caller fixtures are explicitly supplied dynamic data and may be ARM or Thumb; they are not patched encoded original callback literals or asserted game targets. No general allocator semantics, deallocation lifetime, concurrent network/thread behavior or full game/platform execution is proved.', 'The adjacent204-byte write draft remains unselected/uncredited after bounded type/control-flow comparison. Earlier READYs remain immutable. Shared acceptance determines source credit; no source-only ROM or native Windows/Android execution is claimed.']
    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='main',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes'] for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,nativeSymbols={n:b['address'] for n,b in symbols.items()},nativeSymbolModules={n:b['module'] for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,negativeEvidence=negative,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=__import__('hashlib').sha256(raw).hexdigest()),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=len(rows),bytes=sum(r['bytes'] for r in rows),cases=len(traces),wrongCVariants=len(negative)),flush=True)


if __name__=='__main__':execute()
