import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
import link_runtime_unit as L
import unicorn
from wave20261106_socl_continuation_next_fourth_build import build
from wave20261106_socl_continuation_next_fourth_models import NAMES,fixtures
from wave20261106_socl_continuation_next_fourth_execution import run
from wave20261106_socl_continuation_next_fourth_controls import execute as controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/fourth'
SOURCE=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/fourth'
WORK=ROOT/'work/w6sc/fourth-proof'


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
        ('020938b8','missing-full-carry','carry=(s32)(value>>16);','carry=0;',-1),
        ('020938b8','wrong-inplace-tail-policy','output!=left && output!=right','output!=left || output!=right',4),
        ('02093930','wrong-carry-shift','carry=value>>16','carry=value>>15',-1),
        ('02093930','missing-tail-word','for(index++;index<digits;index++)','for(index+=2;index<digits;index++)',3),
        ('02093998','wrong-borrow-sign','borrow=(s32)value>>16','borrow=(s32)(value>>16)',3),
        ('02093a18','missing-borrow','borrow=(value>>16)&1','borrow=(value>>16)&0',3),
        ('02093a6c','wrong-limb-significance','for(index=digits-1;index>=0;index--)','for(index=0;index<digits;index++)',4),
        ('02093ac0','missing-product-truncation','index<digits-outer','index<digits',4),
        ('02093b2c','missing-upper-product-carry','output[index++]=(u16)carry','output[index++]=0',-1),
        ('02093b7c','wrong-doubling-overflow-bound','value<=0x7fff8000','value<=0x7fffffff',5),
        ('02093b7c','wrong-diagonal-high-word','output[inner+1]=(u16)(value>>16)','output[inner+1]=(u16)(value>>15)',3)]:cases.append(mutation(name,label,old,new,[fixtures(name)[index]],main))
    return cases


def execute():
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/fourth' or SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/fourth' or WORK!=ROOT/'work/w6sc/fourth-proof':raise ValueError('Exact new production source/evidence/work paths differ')
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
    limits=['Eight complete860-byte ordinary-C Thumb callers use measured MW2.0/sp1p6/C99/O4,p/file-IPA/inline-on-noauto with genuine full native links, original ELF names/relocations and actual Thumb mapping. Exact original CPU/program/module/mode/body/pool/hash/inventory/relocation witnesses and unchanged normalizer remain enforced.',
            'Independent halfword and arbitrary-precision integer models cross-check add/subtract, small-scalar operations, most-significant-first comparison, truncated multiplication and squaring. Focused fixtures cover empty/negative digit counts where applicable, zero/one/full-width values, carry/borrow chains, ignored top carry, preserved tail words, distinct/in-place buffers, zero-fill ordering, odd truncation and the7fff8000 doubling threshold.',
            'Every positive fixture executes only the complete admitted original and source caller to a real top return, comparing full GPR/CPSR, ordered calls/modes/register arguments, caller/provider writes, instruction PCs and8MiB RAM. Models independently check state at each external boundary, final complete borrowed memory/guards and mathematical results. Reads/writes are fenced to the measured caller frame/body and borrowed arrays.',
            'CountDigits, ARM zero-fill and AddPart are explicitly scripted, individually original-qualified ABI boundaries with caller-saved/flag clobbers. No native callee body executes or receives source/storage credit. Their observed ordered contracts are modeled, not broader arbitrary callback behavior. Caller models do not establish complete RSA/modular arithmetic or cryptographic security.',
            'Real wrong-C controls reject lost carry/borrow, skipped tail copy, inplace zero-fill, reversed limb significance, missing truncation, dropped upper product carry, wrong diagonal shift and unsafe doubling. Rejection at an unexpected provider boundary is recorded separately from an actual top return. Callable prototypes and actual16/32-bit signed/unsigned geometry receive compiler controls.',
            'Public archive type metadata was read only as qualified comparison evidence, with no public binary passed to the producer/compiler/linker. Exact original library names/revision remain unproved. All earlier READYs remain immutable; source credit awaits shared acceptance, and scoped copied-root replay is not a full source-only ROM/native-platform result.']
    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='main',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes'] for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,nativeSymbols={n:b['address'] for n,b in symbols.items()},nativeSymbolModules={n:b['module'] for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,negativeEvidence=negative,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=__import__('hashlib').sha256(raw).hexdigest()),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=len(rows),bytes=sum(r['bytes'] for r in rows),cases=len(traces),wrongCVariants=len(negative)),flush=True)


if __name__=='__main__':execute()
