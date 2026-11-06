import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
import link_runtime_unit as L
import unicorn
from wave20261106_socl_continuation_next_third_build import build
from wave20261106_socl_continuation_next_third_models import NAMES,fixtures
from wave20261106_socl_continuation_next_third_execution import run
from wave20261106_socl_continuation_next_third_controls import execute as controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/third'
SOURCE=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/third'
WORK=ROOT/'work/w6sc/third-proof'


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
        ('02090c18','missing-length-overflow','if(value&0xff000000)return -1;','',7),
        ('02090c18','wrong-cursor-commit','*cursor=next;','*cursor=next-1;',1),
        ('02090c60','wrong-full-name-boundary','>=255','>255',5),
        ('02090c60','wrong-name-separator',"*destination++=',';","*destination++=';';",2),
        ('02090cac','wrong-year-pivot','year<50','year<49',0),
        ('02090cac','wrong-date-combination','return (year<<16)+((text[0]*10+text[1]-528)<<8)+(text[2]*10+text[3]-528);','return (year<<16)|((text[0]*10+text[1]-528)<<8)|(text[2]*10+text[3]-528);',8),
        ('020937dc','wrong-key-wrap-boundary','++cursor>=length','++cursor>length',1),
        ('020937dc','wrong-initial-permutation','state[index]=(u8)index','state[index]=(u8)(index+1)',2),
        ('02093824','missing-output-index-narrowing','state[(u8)(first+second)]','state[first+second]',5),
        ('02093824','wrong-state-writeback','context->y=y;','context->y=0;',2)]:cases.append(mutation(name,label,old,new,[fixtures(name)[index]],main))
    return cases


def execute():
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/third' or SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/third' or WORK!=ROOT/'work/w6sc/third-proof':raise ValueError('Exact new production source/evidence/work paths differ')
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
    limits=['Five complete408-byte ordinary-C Thumb leaf callers use measured MW2.0/sp1p6/C99/O4,p/file-IPA/inline-on-noauto, genuine full native links and actual Thumb mapping. Full original body/pool hashes, CPU/program/module/mode, canonical entries and complete empty relocation sets are revalidated. No prebuilt binary/object, code/register patch, algorithm ASM or alias is used.',
            'Independent native/source models cover variable-length big-endian length decoding, overflow without cursor commit versus a successfully decoded all-ones result with cursor commit, zero length-of-length and pointer/input overlap; bounded byte-count string append with signed bytes, existing-name limit, delimiter insertion, negative length and overlapping input/output.',
            'The measured old-name254 path writes the space at255 and terminator at256; this behavior is retained using borrowed fixture storage and is not silently corrected. Date models cover49/50 century pivot, alternate four-digit input tags, arithmetic field carry and absence of digit/calendar validation.',
            'Byte-state models check complete256-byte initialization/permutation, zero/negative/one/255/256/257-byte key lengths, byte key cursor wrap, mutable key/state alias, zero/negative/one/multiple-byte encryption, state/data alias and byte-index wrap. Every fixture executes the entire original and reconstructed caller to a real top return, with full registers/CPSR/writes/PCs/RAM comparison, independent final-memory/scalar models and bounded reads/writes.',
            'These leaf functions have no imported calls, native callee execution or callee/storage credit. RC4View is a measured258-byte access prefix; original total allocation/alignment is not established by it. Models are focused behavior/ABI evidence under the pinned DS compiler and do not establish complete TLS/ASN.1/date validation, cryptographic security or native Windows/Android execution.',
            'Public NitroWiFi archive metadata was read only for comparison type/local-context evidence; its ARM3.0 build does not establish the ROM compiler/revision or original names. No archive is consumed by the production builder. The52-byte ring helper remains partial and excluded. Shared acceptance and a full source-only ROM proof remain separate.']
    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='main',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes'] for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,nativeSymbols={n:b['address'] for n,b in symbols.items()},nativeSymbolModules={n:b['module'] for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,negativeEvidence=negative,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=__import__('hashlib').sha256(raw).hexdigest()),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=len(rows),bytes=sum(r['bytes'] for r in rows),cases=len(traces),wrongCVariants=len(negative)),flush=True)


if __name__=='__main__':execute()
