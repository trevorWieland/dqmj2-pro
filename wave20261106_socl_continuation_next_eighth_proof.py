import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
import link_runtime_unit as L
import unicorn
from wave20261106_socl_continuation_next_eighth_build import build
from wave20261106_socl_continuation_next_eighth_models import NAMES,fixtures
from wave20261106_socl_continuation_next_eighth_execution import run
from wave20261106_socl_continuation_next_eighth_controls import execute as controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/eighth'
SOURCE=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/eighth'
WORK=ROOT/'work/w6sc/eighth-proof'


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
    for name in ['02091a68','02091afc']:
        cases.append(mutation(name,name+'-boolean-direction-narrowing','if(context->server^direction)','if(!!context->server^!!direction)',[fixtures(name)[4]],main))
        cases.append(mutation(name,name+'-wrong-inner-pad','0x36','0x35',[fixtures(name)[1]],main))
        cases.append(mutation(name,name+'-wrong-outer-pad','0x5c','0x5b',[fixtures(name)[0]],main))
        function='native_fn_0209302c' if name=='02091a68' else 'native_fn_020936f4';length=16 if name=='02091a68' else 20
        cases.append(mutation(name,name+'-wrong-inner-digest-length',function+'(hash,output,'+str(length)+')',function+'(hash,output,'+str(length-1)+')',[fixtures(name)[5]],main))
    return cases


def execute():
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/eighth' or SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/eighth' or WORK!=ROOT/'work/w6sc/eighth-proof':raise ValueError('Exact new production source/evidence/work paths differ')
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
    limits=['Two complete300-byte ordinary-C Thumb Finished callers use actual pinned MW2.0/sp1p6/C99/O4,p/file-IPA/inline-on-noauto, genuine full native links, complete code/pool hashes, original ELF names/relocations and actual Thumb mapping. No source/byte/register/object patch, algorithm ASM or prebuilt compiler input.',
            'Independent message-composition models check live MD5/SHA1 context addresses, full-width byte-server XOR32-bit direction, both four-byte role strings, captured live-transcript seed,48-byte master input,48/40-byte36/5C pads, first digest, reset, fresh second master read and16/20-byte inner digest before final overwrite. High-bit direction and output/master overlap preserve measured behavior.',
            'Each positive native/source caller executes completely to a real top return, with all GPR/CPSR, ordered calls/modes/register arguments, writes, PCs and8MiB RAM equality plus independent complete borrowed-context/output/guard and stack-pad checks. Standard-library digests model primitive contracts. Initial/update context bytes are scripted markers, not assertions about actual unfinalized native hash state.',
            'All hash and byte-fill callees are original-qualified synthetic ABI boundaries that clobber caller-saved registers/flags and remain unexecuted native bodies with zero source credit. These tests prove caller protocol under those contracts, not complete transcript processing, TLS security, cryptographic assurance or provider implementation.',
            'Two original four-byte SRVR/CLNT prefixes are reference inputs with zero data/storage credit and exact native kind/literal/origin/prefix witnesses. ConnectionView is a chosen minimum access layout, not a complete original allocation/type claim. The root-CA draft is excluded and uncredited.',
            'Wrong Boolean narrowing, inner/outer padding and digest length variants reject independent effects or observed helper ABI. Pre-return rejection is distinguished from actual returned execution. Actual C99 prototypes/geometry, strict full original namespace/branch/data/completeness negatives and copied-root replay remain enforced.',
            'All earlier READY paths are immutable. Shared acceptance determines credit; this packet is not a full source-only ROM or native Windows/Android execution proof.']
    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='main',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes'] for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,nativeSymbols={n:b['address'] for n,b in symbols.items()},nativeSymbolModules={n:b['module'] for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,negativeEvidence=negative,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=__import__('hashlib').sha256(raw).hexdigest()),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=len(rows),bytes=sum(r['bytes'] for r in rows),cases=len(traces),wrongCVariants=len(negative)),flush=True)


if __name__=='__main__':execute()
