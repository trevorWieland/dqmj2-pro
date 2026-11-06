import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
import link_runtime_unit as L
import unicorn
from wave20261106_socl_continuation_next_build import build
from wave20261106_socl_continuation_next_models import NAMES,fixtures
from wave20261106_socl_continuation_next_execution import run
from wave20261106_socl_continuation_next_controls import execute as controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/first'
SOURCE=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/first'
WORK=ROOT/'work/w6sc/first-proof'


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
    cases=[];a=fixtures('0209075c');b=fixtures('02090794');c=fixtures('0209088c')
    cases.append(mutation('0209075c','wrong-zero-address-test','if(h==0)','if(h!=0)',[f for f in a if f['host']==1],main))
    cases.append(mutation('0209075c','wrong-high-octet','h>>24','h>>16',[f for f in a if f['host']==0xaabbccdd],main))
    cases.append(mutation('02090794','wrong-family','family!=2','family!=3',[f for f in b if f['family']==2 and f['length']==16],main))
    cases.append(mutation('02090794','wrong-final-octet','bytes[0]','bytes[1]',[f for f in b if f['alias']],main))
    cases.append(mutation('0209088c','wrong-not-created-result','return -39','return -38',[f for f in c if f['invalid']==0 and f['mode']==0 and f['state']==0],main))
    cases.append(mutation('0209088c','wrong-TCP-predicate','if(!socket_tcp(socket))','if(socket_tcp(socket))',[f for f in c if f['mode']==4 and f['state']==1],main))
    cases.append(mutation('0209088c','missing-primary-volatile-state','volatile s16 state','s16 state',[f for f in c if f['mode']==4 and f['state']==1],main,True))
    for name in ['0209302c','020936f4']:
        rows=fixtures(name);carry=[f for f in rows if f['low']==0xfffffff8 and f['length']==1];equal=[f for f in rows if f['low']==0 and f['length']==64]
        cases.append(mutation(name,name+'-missing-carry','if(context->low<(length<<3))context->high++;','',carry,main))
        cases.append(mutation(name,name+'-wrong-full-block-boundary','length>=remaining','length>remaining',equal,main))
    for name,last in [('020930ac',16),('02093774',20)]:
        rows=fixtures(name);cases.append(mutation(name,name+'-wrong-padding-boundary','index<56','index<=56',[f for f in rows if ((f['low']>>3)&63)==56],main))
        cases.append(mutation(name,name+'-truncated-digest','context->state,'+str(last),'context->state,'+str(last-4),[rows[0]],main))
    return cases


def execute():
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/first' or SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/first' or WORK!=ROOT/'work/w6sc/first-proof':raise ValueError('Exact new production source/evidence/work paths differ')
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
    limits=['Seven complete ordinary-C Thumb callers/634bytes, actual pinned base MW C99/file-IPA and genuine links preserve complete code/pools, ELF names/relocations and Thumb mapping. The unchanged original BL/BLX normalizer/parsers and strict original call/data witnesses remain in use; no code/register/object patches, algorithm ASM or new alias.',
            'Focused original/source caller fixtures require actual returns and equality of full GPR/CPSR, calls including vararg stack words, writes, PCs and8MiB RAM. Models check IPv4 zero/byte order, address-family/output-length gates, source/output alias, decimal octets, signed socket mode and volatile signed16 state reads/results.',
            'Shared4-word/5-word block-context models check counter carry/wrap, zero/partial/equal/multiple64-byte blocks, exact input/buffer call slices, guard bytes, padding boundary55/56/63, counter serialization and complete16/20-byte output sequencing. Transform/provider behavior is explicitly scripted; no complete MD5/SHA1/TLS primitive or protocol behavior is established by these wrappers.',
            'All imported native bodies are unexecuted ABI boundaries with caller-saved/flag clobbers and zero callee source/execution credit. Two update bodies are independently reconstructed as selected rows, but finalizer fixtures still treat their calls as scripted boundaries. Void-return functions promise no semantic R0 result; raw registers are machine observations.',
            'Three original initialized prefixes are reference inputs only:12-byte terminated IPv4 format and two64-byte80/zero padding views. Their exact caller/origin/mode/load/inventory/native hashes are checked with zero data/storage/authorship credit. Contexts are minimum measured ABI views, not proven original typedef/object allocation sizes.',
            'Real wrong-C/volatile changes reject independent scalar, byte-order, length, state-read, carry, block/padding and output-length checks. Some wrong-argument variants stop at the explicitly observed ABI rejection boundary and are not counted as returned executions. Namespace/relocation/completeness/data/prototype/compiler-layout controls remain strict.',
            'The public NitroWiFi source/headers are pinned comparison evidence; exact library revision/name correspondence beyond measured agreements remains unproved. Poll152 and RC4 drafts remain uncredited. All old READYs/claims are preserved. Fresh copied-root source replay still needs serialized shared acceptance and is not a whole source-only ROM/native-platform proof.']
    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='main',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes'] for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,nativeSymbols={n:b['address'] for n,b in symbols.items()},nativeSymbolModules={n:b['module'] for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,negativeEvidence=negative,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=__import__('hashlib').sha256(raw).hexdigest()),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=len(rows),bytes=sum(r['bytes'] for r in rows),cases=len(traces),wrongCVariants=len(negative)),flush=True)


if __name__=='__main__':execute()
