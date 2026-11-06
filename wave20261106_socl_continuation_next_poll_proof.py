import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
import link_runtime_unit as L
import unicorn
from wave20261106_socl_continuation_next_poll_build import build
from wave20261106_socl_continuation_next_poll_models import NAMES,fixtures
from wave20261106_socl_continuation_next_poll_execution import run
from wave20261106_socl_continuation_next_poll_controls import execute as controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/second'
SOURCE=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/second'
WORK=ROOT/'work/w6sc/poll-proof'


def mutation(name,label,old,new,selected,main,header=False):
    text=(SOURCE/(name+'.c')).read_text();context=(SOURCE/'poll.h').read_text();target=context if header else text
    if target.count(old)!=1 or not selected:raise ValueError('Whole-C semantic mutation ambiguous or empty')
    folder=WORK/'negative'/label;folder.mkdir(parents=True,exist_ok=True);source=folder/'source.c';source.write_text(text if header else text.replace(old,new));(folder/'poll.h').write_text(context.replace(old,new) if header else context)
    row,body=build(source,folder/'build',True);rejected=[]
    for i,fixture in enumerate(selected):
        result=run(row,body,fixture,main,i)
        if not result['modelFailures']:raise ValueError(('Wrong C escaped independent model',label,fixture))
        rejected.append(dict(fixture=fixture,failures=result['modelFailures'],actualTopReturn=result['actualTopReturn'],rejectedAtObservedProtocolBoundary=result['rejectedAtObservedProtocolBoundary']))
    return dict(case=label,caller=name,old=old,new=new,headerMutation=header,proof=row,rejected=rejected)


def negatives(main):
    f=fixtures('020907f4');cases=[]
    for label,old,new,selected in [
        ('wrong-error-mask','|0xe0','|0x60',[f[2]]),
        ('wrong-event-input','entry->events|','entry->revents|',[f[13]]),
        ('wrong-count-truncation','if(status)good++;','if((s16)status)good++;',[f[3]]),
        ('wrong-infinite-sentinel','timeout!=(u64)-1','timeout!=(u64)0',[f[0]]),
        ('wrong-expiration-boundary','time<=0','time<0',[f[7]]),
        ('wrong-tick-step','33513982','33449982',[f[7]]),
        ('wrong-sleep-argument','native_fn_02006b7c(1)','native_fn_02006b7c(2)',[f[1]]),
        ('wrong-result-field','entry->revents=(s16)status','entry->events=(s16)status',[f[2]])]:cases.append(mutation('020907f4',label,old,new,selected,main))
    return cases


def execute():
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/second' or SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/second' or WORK!=ROOT/'work/w6sc/poll-proof':raise ValueError('Exact new production source/evidence/work paths differ')
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
    limits=['One complete152-byte ordinary-C Thumb poll caller compiled with pinned MW2.0/sp1p6, actual C99/O4,p/file-IPA/inline-on-noauto. Genuine native link preserves original ELF names/relocations, full body/pool and actual Thumb mapping. Unchanged original relocation normalizer and strict BL/BLX witnesses remain in use.',
            'Fourteen original/source fixture pairs require actual top returns and equality of complete GPR/CPSR, calls, writes, instruction PCs and8MiB RAM. Independent models cover signed16 masks, full32-bit readiness before16-bit result truncation, caller/provider mutation ordering, zero descriptors, finite/negative/infinite64-bit timeout,523-tick boundary and borrow, and measured8-byte record layout.',
            'GetStatus and ARM Sleep are explicitly scripted ABI boundaries with caller-saved/flag clobbers, unexecuted native callee bodies and zero callee/storage credit. Finite fixtures and scripted eventual readiness bound infinite-timeout cases; no scheduler/network protocol behavior is claimed.',
            'Real wrong-C variants reject masks, input/output fields, readiness truncation, infinite sentinel, timeout boundary, tick step and Sleep arguments. Rejection at an unexpected provider boundary is recorded separately from actual top returns. Required prototypes, actual compiler geometry and original CPU/program/module/mode/entry/addend/relocation controls are retained.',
            'Pinned complete public NitroWiFi SOC source/headers provide comparison evidence; exact original SDK revision is not proved. MW compiler revision is measured by complete genuine native bytes, without using any public prebuilt binary as source/object input. Fresh copied-root replay remains pending shared acceptance and is not full source-only ROM or native-platform proof.']
    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='main',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes'] for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,nativeSymbols={n:b['address'] for n,b in symbols.items()},nativeSymbolModules={n:b['module'] for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,negativeEvidence=negative,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=__import__('hashlib').sha256(raw).hexdigest()),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=len(rows),bytes=sum(r['bytes'] for r in rows),cases=len(traces),wrongCVariants=len(negative)),flush=True)


if __name__=='__main__':execute()
