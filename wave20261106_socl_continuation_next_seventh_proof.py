import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
import link_runtime_unit as L
import unicorn
from wave20261106_socl_continuation_next_seventh_build import build
from wave20261106_socl_continuation_next_seventh_models import NAMES,fixtures
from wave20261106_socl_continuation_next_seventh_execution import run
from wave20261106_socl_continuation_next_seventh_controls import execute as controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/seventh'
SOURCE=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/seventh'
WORK=ROOT/'work/w6sc/seventh-proof'


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
    for name,label,old,new,index,header in [
        ('020909c8','wrong-IP-match','entry->ip==ip','entry->ip!=ip',1,False),
        ('020909c8','wrong-hit-flag','context->cached=1;','context->cached=0;',2,False),
        ('020909c8','wrong-tick-shift','>>16','>>32',2,False),
        ('020909c8','wrong-64bit-tick-prototype','extern u64 native_fn_02007a9c','extern u32 native_fn_02007a9c',2,True),
        ('02090a3c','wrong-invalid-slot-priority','biggest=(u32)-1;','biggest=0;',1,False),
        ('02090a3c','wrong-signed-age','now-entry->when>biggest','(s32)(now-entry->when)>(s32)biggest',6,False),
        ('02090a3c','missing-nonzero-IP-gate','entry->valid && ip && ip==entry->ip','entry->valid && ip==entry->ip',3,False),
        ('02090ae8','wrong-session-comparison','!native_fn_0201b248','native_fn_0201b248',1,False),
        ('02090ae8','missing-first-match-stop','break;','',3,False),
        ('02090ae8','wrong-invalidated-byte','entry->valid=0;','entry->padding=0;',2,False)]:cases.append(mutation(name,label,old,new,[fixtures(name)[index]],main,header))
    return cases


def execute():
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/seventh' or SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/seventh' or WORK!=ROOT/'work/w6sc/seventh-proof':raise ValueError('Exact new production source/evidence/work paths differ')
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
    limits=['Three complete360-byte ordinary-C Thumb cache callers use actual pinned MW2.0/sp1p6/C99/O4,p/file-IPA/inline-on-noauto with genuine complete native links, original ELF names/relocations, exact full native bodies/pools and actual Thumb mapping. Existing compiler/parser/normalizer/linker code remains unchanged; no code/register/object patch or algorithm ASM.',
            'Original configured BSS021d1748 is only an external reference. The qualifier checks exact canonical BSS kind/base/literal/origin/full caller hashes and independently decodes record-stride92 and loop-bound4 instructions.367 bytes are within measured field-access coverage;368 bytes are the chosen four-record C layout, including a final unaccessed padding byte. Full original allocation size is unproved and BSS/initialized/storage/authorship credit is zero.',
            'Focused independent cache models cover miss/first/last/duplicate/invalid matches, raw nonzero-valid bytes, exact16-bit port/full32-bit IP, zero IP/port replacement gates, first-invalid priority, oldest unsigned age, age wrap/sentinel behavior, default slot and preservation of other records/padding. A borrowed overlapping access-view fixture also checks observed copy/store ordering without claiming original game-object validity.',
            'Every positive fixture executes only the entire admitted native/source caller to a real top return, comparing all GPR/CPSR, ordered calls/modes/register arguments, writes, PCs and8MiB RAM plus independent memory/guard state. Tick fixtures explicitly return64-bit values in R0/R1 and test32-bit truncation after shift16. IRQ disable/restore preserve the complete opaque32-bit saved cookie.',
            'IRQ/tick/copy/compare are explicitly scripted ABI boundaries; no native provider body executes or receives credit. The ordered IRQ call protocol is checked, not physical interrupt/timer hardware. Copied and compared bytes are modeled at the exact original argument spans. Context/record structs are measured access views, not whole allocation/type recovery claims.',
            'Real wrong-C/type changes reject match, flags, tick shift/return width, invalid priority, signed-age conversion, zero-IP gates, comparison polarity, missing first-stop and wrong invalidated byte. Some variants reject before top return at an observed provider boundary; this is recorded separately. Strict wrong-BSS/type/shape/namespace/native evidence, prototypes and actual compiler geometry controls are retained.',
            'All earlier READYs remain immutable. This source awaits shared acceptance and is not complete TLS-cache security, source-only ROM or native Windows/Android proof.']
    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='main',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes'] for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,nativeSymbols={n:b['address'] for n,b in symbols.items()},nativeSymbolModules={n:b['module'] for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,negativeEvidence=negative,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=__import__('hashlib').sha256(raw).hexdigest()),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=len(rows),bytes=sum(r['bytes'] for r in rows),cases=len(traces),wrongCVariants=len(negative)),flush=True)


if __name__=='__main__':execute()
