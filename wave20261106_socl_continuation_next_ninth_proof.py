import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
import link_runtime_unit as L
import unicorn
from wave20261106_socl_continuation_next_ninth_build import build
from wave20261106_socl_continuation_next_ninth_models import NAMES,fixtures
from wave20261106_socl_continuation_next_ninth_execution import run
from wave20261106_socl_continuation_next_ninth_controls import execute as controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/ninth'
SOURCE=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/ninth'
WORK=ROOT/'work/w6sc/ninth-proof'


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
        ('02092778','wrong-initial-error','result==9','result==8',0),
        ('02092778','wrong-completion-or','result==4 || context->reuse','result==4 && context->reuse',1),
        ('02092778','wrong-late-cache-flag','if(context->cached)','if(context->reuse)',8),
        ('02092778','wrong-port-IP-order','context,socket->ip,socket->port','context,socket->port,socket->ip',2),
        ('02092778','wrong-final-state','context->state=8;','context->state=7;',1),
        ('02092b50','wrong-shutdown-state','context->state==8','context->state==7',2),
        ('02092b50','wrong-alert-byte','temporary[5]=1;','temporary[5]=2;',2),
        ('02092b50','wrong-final-clear','context->state=0;','context->state=1;',0),
        ('02092b50','wrong-context-reread','context->state=0;','socket->ssl->state=0;',3),
        ('02092bf0','wrong-cache-boundary','>957','>=957',1),
        ('02092bf0','wrong-signed-cache-age','(s32)(now-native_data_021d1748[i].when)','(u32)(now-native_data_021d1748[i].when)',3),
        ('02092bf0','wrong-nonzero-valid','native_data_021d1748[i].valid &&','native_data_021d1748[i].valid==1 &&',1),
        ('02092bf0','wrong-socket-age-boundary','>239','>240',4),
        ('02092bf0','wrong-signed-socket-age','(s32)(now-socket->when)','(u32)(now-socket->when)',8),
        ('02092bf0','wrong-nonzero-secured','socket->secured &&','socket->secured==1 &&',4),
        ('02092bf0','wrong-socket-state','socket->state==2','socket->state==1',4),
        ('02092bf0','missing-thread-tail','thread=thread->next','thread=0',4)]:cases.append(mutation(name,label,old,new,[fixtures(name)[index]],main))
    return cases


def execute():
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/ninth' or SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/ninth' or WORK!=ROOT/'work/w6sc/ninth-proof':raise ValueError('Exact new production source/evidence/work paths differ')
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
    limits=['Three complete376-byte ordinary-C Thumb connection/shutdown/periodic callers use measured pinned MW2.0/sp1p6/C99/O4,p/file-IPA/inline-on-noauto, genuine complete links, unchanged original ELF names/relocations and exact full native body/pools. Existing compiler/parser/normalizer/linker files remain unchanged; no code/object/register patch, algorithm ASM or fabricated alias.', 'Original BSS021d1748 and020e33e4 are external field-access references only. Exact canonical kind/base/literal/origin/full caller hashes and independently decoded stride92/bound4 and thread first+8/next+104/socket+164 instructions are checked. Session minimum accessed367 versus chosen layout368 is explicit; complete original allocations and all BSS/storage/authorship credit remain unproved/zero.', 'Independent negotiation models cover error/loop/nonzero completion, resumed/fresh branches, late cache flag and exact IP/16-bit port rereads, captured context across provider mutation, send/wait ordering and final state. Shutdown models cover raw state bytes, exact seven alert bytes, modeled encrypted output/register plus fifth stack argument, and captured context across callback mutation.', 'Periodic models cover exact signed32 modular age comparisons,957/958 session and239/240 socket boundaries, wrap/negative ages, raw nonzero flag bytes, all measured socket/thread gates, callback-mutated traversal links, fresh thread-list read after IRQ restore, and exact opaque32-bit IRQ cookie. List/context structs are borrowed measured access views, not broader object validity/type/allocation recovery.', 'Every positive fixture executes only the entire actual native/source caller to real top returns and compares all GPR/CPSR, ordered calls/modes/register and stack arguments, writes, PCs,8MiB RAM and independent complete borrowed state/guards. IRQ/wakeup and TLS/network helpers are scripted ABI boundaries; their bodies do not execute and receive zero credit. This does not prove hardware timing, concurrency, TLS cryptography or networking.', 'Sixteen real wrong-C changes reject branch/error/cache/address ordering/state/header/context reload/signed age/boundary/flag/traversal errors. Wrong original body/import/CPU/program/module/mode/origin/hash/BSS kind/shape/field instructions, required actual caller/provider prototypes and real compiler geometry controls remain mandatory.', 'All earlier READYs are immutable. This packet awaits shared acceptance; no source-only ROM or native Windows/Android execution is claimed.']
    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='main',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes'] for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,nativeSymbols={n:b['address'] for n,b in symbols.items()},nativeSymbolModules={n:b['module'] for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,negativeEvidence=negative,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=__import__('hashlib').sha256(raw).hexdigest()),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=len(rows),bytes=sum(r['bytes'] for r in rows),cases=len(traces),wrongCVariants=len(negative)),flush=True)


if __name__=='__main__':execute()
