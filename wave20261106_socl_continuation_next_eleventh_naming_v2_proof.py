import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
import link_runtime_unit as L
import unicorn
from wave20261106_socl_continuation_next_eleventh_naming_v2_build import build
from wave20261106_socl_continuation_next_eleventh_naming_v2_models import NAMES,fixtures
from wave20261106_socl_continuation_next_eleventh_naming_v2_execution import run
from wave20261106_socl_continuation_next_eleventh_naming_v2_controls import execute as controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/eleventh-naming-v2'
SOURCE=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/eleventh-naming-v2'
WORK=ROOT/'work/w6sc/eleventh-naming-v2-proof'


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
        ('020911b0','wrong-public-key-algorithm-sentinel','context->pub_algorithm==-1','context->pub_algorithm<0',7),
        ('020911b0','wrong-nonzero-certificate-flag','context->date_ok?0','context->date_ok==1?0',5),
        ('020911b0','wrong-full-status-width','return flags|native_fn_0209108c','return flags|(u8)native_fn_0209108c',6),
        ('020911b0','wrong-root-gate','if(!root)','if(root)',3),
        ('020911b0','wrong-digest-storage-length','context->certificate_hash_length=16;','context->certificate_hash_length=15;',3),
        ('02091c5c','wrong-record-length-high','length-=16;input[3]=length>>8','length-=16;input[3]=length>>7',3),
        ('02091c5c','wrong-inner-pad','native_fn_02008d78(padding,0x36,48)','native_fn_02008d78(padding,0x35,48)',0),
        ('02091c5c','wrong-outer-pad','native_fn_02008d78(padding,0x5c,40)','native_fn_02008d78(padding,0x5b,40)',4),
        ('02091c5c','wrong-inner-digest-width','native_fn_020936f4(hash,digest,20)','native_fn_020936f4(hash,digest,19)',6),
        ('02091c5c','wrong-MAC-comparison','if(native_fn_0201b248','if(!native_fn_0201b248',0),
        ('02091c5c','wrong-sequence-end','context->sequence+8','context->sequence+7',4),
        ('02091c5c','wrong-returned-record-size','return length+5;','return length+4;',1)]:cases.append(mutation(name,label,old,new,[fixtures(name)[index]],main))
    return cases


def execute():
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/eleventh-naming-v2' or SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/eleventh-naming-v2' or WORK!=ROOT/'work/w6sc/eleventh-naming-v2-proof':raise ValueError('Exact new production source/evidence/work paths differ')
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
    limits=['Two complete584-byte ordinary-C Thumb certificate-dispatch and record-MAC callers use pinned measured MW2.0/sp1p6/C99/O4,p/file-IPA/inline-on-noauto, genuine full native links, original object symbols/relocations and complete native body/pool hashes. Existing compiler/parser/normalizer/linker files remain unchanged, with no instruction/register/object patches, algorithm ASM, alias or prebuilt executable compiler input.', 'The certificate caller checks raw nonzero flag bytes, exactFFFFFFFF public-key-algorithm sentinel versus other signed values,3/4 hash selection, exact digest storage/length, missing root and full32-bit status OR/captured flags. Public-reference names/type facts are hypotheses corroborated by measured native field/body evidence; external root/signature providers remain opaque.', 'The record caller uses the measured domain method4 or5, complete decrypted length at least the corresponding16/20-byte MAC and valid borrowed buffers. Its original out-of-domain branch contains uninitialized local MAC data/length; fixtures and behavioral claims exclude that domain. Full original machine bytes still match. Header length rewriting, secret/pad/sequence/type/length/payload composition, fresh outer secret reads, inner/outer digests, match/mismatch state and big-endian sequence wrap are checked.', 'Each actual native/source caller executes fully to real top return, comparing all GPR/CPSR, ordered provider modes/arguments, writes, PCs and8MiB RAM plus independent complete borrowed-memory/guard and exact stack pad/digest checks. Python standard-library hashes model cryptographic primitive contracts; scripted hash-context marker bytes do not assert actual unfinalized native hash state.', 'All hash/fill/decrypt/compare/counter/root/signature bodies are explicitly scripted ABI boundaries, never executed native callees and receive zero credit. This proves caller behavior under those contracts, not TLS security, actual certificate trust/RSA, decryption, cryptographic assurance or networking. ConnectionView is a measured minimum field-access layout; no complete original allocation, storage or data credit is claimed.', 'Twelve whole wrong-C variants reject sentinel/narrowed flag/status/root/hash length/header/padding/inner digest/comparison/sequence/return errors. Required actual entry/provider prototypes, actual compiler geometry and strict original full body/CPU/program/module/mode/entry/origin/addend/native bytes/relocation completeness negatives remain mandatory. Observed pre-return protocol rejection is distinguished from actual successful returns.', 'All prior READYs and the parked division/SHA1/session parser remain unchanged. Shared acceptance determines source credit; no source-only ROM or native Windows/Android execution is claimed.']
    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='main',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes'] for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,nativeSymbols={n:b['address'] for n,b in symbols.items()},nativeSymbolModules={n:b['module'] for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,negativeEvidence=negative,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=__import__('hashlib').sha256(raw).hexdigest()),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=len(rows),bytes=sum(r['bytes'] for r in rows),cases=len(traces),wrongCVariants=len(negative)),flush=True)


if __name__=='__main__':execute()
