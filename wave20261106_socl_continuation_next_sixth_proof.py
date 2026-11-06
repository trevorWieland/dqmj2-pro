import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
import link_runtime_unit as L
import unicorn
from wave20261106_socl_continuation_next_sixth_build import build
from wave20261106_socl_continuation_next_sixth_models import NAMES,fixtures
from wave20261106_socl_continuation_next_sixth_execution import run
from wave20261106_socl_continuation_next_sixth_controls import execute as controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/sixth'
SOURCE=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/sixth'
WORK=ROOT/'work/w6sc/sixth-proof'


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
        ('02091518','wrong-entry-width','width==3','width==2',5),
        ('02091518','wrong-method-truncation','if(value==method)','if((u16)value==method)',6),
        ('0209158c','wrong-method-count-divisor','methods/3','methods/2',2),
        ('0209158c','wrong-random-padding-boundary','challenge>=32','challenge>=31',4),
        ('0209158c','wrong-cache-flag','context->cached=0;','context->cached=1;',2),
        ('020917f8','wrong-random-seed-length','native_fn_020936f4(hash,context->randoms,64)','native_fn_020936f4(hash,context->randoms,32)',1),
        ('020917f8','wrong-inner-digest-length','native_fn_0209302c(hash,temporary,20)','native_fn_0209302c(hash,temporary,16)',2),
        ('02091864','wrong-second-salt','temporary+16,native_data_020de880','temporary+16,native_data_020de87c',0),
        ('02091864','wrong-master-length','temporary,context->master,48','temporary,context->master,32',1)]:cases.append(mutation(name,label,old,new,[fixtures(name)[index]],main))
    return cases


def execute():
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/sixth' or SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/sixth' or WORK!=ROOT/'work/w6sc/sixth-proof':raise ValueError('Exact new production source/evidence/work paths differ')
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
    limits=['Four complete364-byte ordinary-C Thumb callers are compiled with pinned MW2.0/sp1p6/C99/O4,p/file-IPA/inline-on-noauto and genuine full native links. Original names/relocations, complete code/pools, canonical CPU/program/module/mode/boundaries and actual Thumb mapping are preserved; no ordinary algorithm ASM or code/register/object/symbol patch.',
            'Method-list models cover signed empty/negative counts,2/3-byte big-endian entries, zero stride, full24-bit comparison and16-bit requested methods. Client-v2 models check early version/method rejection, int-to-u16 selection, signed division/truncation, field widths, fresh payload offsets, challenge0/1/31/32/40 zero-prefix versus direct copy and exact cache/state writes.',
            'Natural signed `/3` emits the original compiler symbol _s32_div_f. A new caller-and-full-profile-specific resolver retains that name and qualifies its original BLX origin plus canonical ARM02026144, with wrong-name/caller/flags/compiler/CPU/module/program/mode/address controls. The original compiler/parser/normalizer/linker helpers are unchanged, and no arithmetic helper body is reconstructed or executed.',
            'Seed/master models check ordered SHA1 then MD5 calls, source/temporary/destination lengths, salt byte strings, captured48-byte master plus64 random bytes, three16-byte chunks and final48-byte writeback. Standard-library digests model the primitive contracts. Context marker mutations are explicitly scripted ABI effects, not a claim to actual intermediate hash-state implementation.',
            'All positive fixtures execute only the complete original and source caller to real top returns, comparing all GPR/CPSR, ordered calls/modes/arguments/writes, PCs and8MiB RAM, with independent final data/guard and stack-payload checks. All hash/selection/version/copy/zero/divide providers remain unexecuted native ABI boundaries with zero callee credit. Selected seed callers are still scripted boundaries when master fixtures execute.',
            'ConnectionView is an independently measured minimum field-access prefix; its1112-byte source size is not an original allocation-size claim. Three terminated salt prefixes are original reference data with zero storage credit. Required prototypes, actual geometry, semantic wrong-C and copied-root controls remain mandatory. Two other sixth drafts and the SHA1 block remain uncredited.',
            'Exact original SDK names/revision remain qualified by public comparison metadata. Source credit awaits shared acceptance; this packet does not establish complete TLS security, a full source-only ROM, or native Windows/Android execution.']
    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='main',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes'] for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,nativeSymbols={n:b['address'] for n,b in symbols.items()},nativeSymbolModules={n:b['module'] for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,negativeEvidence=negative,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=__import__('hashlib').sha256(raw).hexdigest()),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=len(rows),bytes=sum(r['bytes'] for r in rows),cases=len(traces),wrongCVariants=len(negative)),flush=True)


if __name__=='__main__':execute()
