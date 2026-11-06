import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
import link_runtime_unit as L
import unicorn
from wave20261106_socl_continuation_next_thirteenth_build import build
from wave20261106_socl_continuation_next_thirteenth_models import NAMES,fixtures
from wave20261106_socl_continuation_next_thirteenth_execution import run
from wave20261106_socl_continuation_next_thirteenth_controls import execute as controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/thirteenth'
SOURCE=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/thirteenth'
WORK=ROOT/'work/w6sc/thirteenth-proof'


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
        ('02091de0','wrong-secret-field','*send_secret,*send_key','*send_key,*send_secret',1,True),
        ('02091de0','wrong-record-type-span','native_fn_0209302c(hash,input,1)','native_fn_0209302c(hash,input,2)',1,False),
        ('02091de0','wrong-inner-digest-length','native_fn_0209302c(hash,payload+length,16)','native_fn_0209302c(hash,payload+length,15)',2,False),
        ('02091de0','wrong-appended-length','length+=16;','length+=15;',0,False),
        ('02091de0','wrong-cipher-context','native_fn_02093824(context->send_cipher','native_fn_02093824(context->send_sequence',5,False),
        ('02091de0','wrong-sequence-end','context->send_sequence+8','context->send_sequence+7',0,False),
        ('02091de0','wrong-high-record-length','input[3]=length>>8','input[3]=length>>7',7,False),
        ('02091de0','wrong-returned-length','return length+5;','return length+4;',3,False),
        ('02092380','wrong-allocation-size','native_data_021cfd0c(131)','native_data_021cfd0c(130)',1,False),
        ('02092380','wrong-allocation-error-state','context->state=9;','context->state=8;',0,False),
        ('02092380','wrong-counter-clear','native_fn_02008d78(context->send_sequence','native_fn_02008d78(context->sequence',1,False),
        ('02092380','wrong-finished-header','buffer[14]=36;','buffer[14]=35;',1,False),
        ('02092380','wrong-backup-extent','native_fn_02008e0c(&context->md5live,&context->md5tmp,88)','native_fn_02008e0c(&context->md5live,&context->md5tmp,84)',1,False),
        ('02092380','wrong-backup-restore','native_fn_02008e0c(&context->md5tmp,&context->md5live,88)','native_fn_02008e0c(&context->md5live,&context->md5tmp,88)',1,False),
        ('02092380','wrong-transcript-start','native_fn_02091f98(context,buffer+11,40)','native_fn_02091f98(context,buffer+10,40)',1,False),
        ('02092380','wrong-network-span','buffer,length+6,0,0,socket','buffer,length+5,0,0,socket',2,False)]:cases.append(mutation(name,label,old,new,[fixtures(name)[index]],main,header))
    return cases


def execute():
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/thirteenth' or SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/thirteenth' or WORK!=ROOT/'work/w6sc/thirteenth-proof':raise ValueError('Exact new production source/evidence/work paths differ')
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
    limits=['Two complete612-byte ordinary-C Thumb send-record/MAC and Finished-sender callers use pinned measured MW2.0/sp1p6/C99/O4,p/file-IPA/inline-on-noauto with genuine full native links, exact original code/pools, original ELF names/relocations and actual Thumb mappings. No algorithm ASM, source-byte/register/object patch, fabricated alias or prebuilt executable compiler input.', 'Independent record models cover MD5/SHA1 secret/pad/sequence/type/length/payload composition, zero/one/64/257-byte messages, fresh outer secret pointer, in-place inner/final MAC append, header length, exact cipher-context/payload spans and big-endian sequence wrap. Other method values0/3/FFFF follow the actual no-MAC branch. Cipher output is an explicitly scripted fixture transform, not actual native cipher execution or assurance.', 'Finished-sender models cover allocation failure, context captured before allocator mutation, exact two record headers and Finished handshake prefix, send-counter clear, complete88/92-byte live-hash backup/restore around independently scripted16/20-byte results, transcript order, encoded-length/network register plus fifth stack argument and release order. Scripted Finished results/hash-state markers are arbitrary contract fixtures, not assertions about actual unfinalized native crypto state.', 'Both original dynamic allocator/release slots are canonical BSS access references with exact literal/origin/full-body/load/BLX/result proofs. Controlled fresh ARM/Thumb ABI returns, wrong runtime tags/site/declarations/access views qualify interfaces only; original runtime callback identities/registration, BSS/storage and callee source credit remain zero.', 'Every positive actual native/source caller executes fully to real top return and compares all GPR/CPSR, ordered original-qualified or explicitly controlled callback modes/register/stack arguments/return sites, writes, PCs,8MiB RAM and complete independent borrowed state/guards and stack-pad checks. Original hash/cipher/fill/copy/counter/Finished/transcript/network/callback bodies remain unexecuted synthetic ABI boundaries.', 'Sixteen real wrong-C/type variants reject secret fields/spans/digest/length/cipher/counter/header/allocation/state/backup/transcript/network mistakes. Required actual entry/provider prototypes, native compiler geometry and strict complete original namespace/body/hash/branch/load/addend/relocation and callback controls remain mandatory. Pre-return protocol rejection is distinguished from a returned positive caller.', 'All context/socket/cipher storage is a minimum measured borrowed access view with zero data/storage credit. This is not complete TLS/security, physical networking/concurrency, full source-only ROM or native Windows/Android proof. The adjacent276-byte ClientHello draft is excluded/uncredited; all previous READYs remain immutable and shared acceptance determines credit.']
    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='main',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes'] for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,nativeSymbols={n:b['address'] for n,b in symbols.items()},nativeSymbolModules={n:b['module'] for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,negativeEvidence=negative,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=__import__('hashlib').sha256(raw).hexdigest()),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=len(rows),bytes=sum(r['bytes'] for r in rows),cases=len(traces),wrongCVariants=len(negative)),flush=True)


if __name__=='__main__':execute()
