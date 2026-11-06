import gzip
import json
import shutil
import sys
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
import link_runtime_unit as L
import unicorn
from wave20261106_socl_continuation_next_fifth_build import build
from wave20261106_socl_continuation_next_fifth_models import NAMES,fixtures,verify_reference_tables
from wave20261106_socl_continuation_next_fifth_execution import run
from wave20261106_socl_continuation_next_fifth_controls import execute as controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/fifth'
SOURCE=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/fifth'
WORK=ROOT/'work/w6sc/fifth-proof'


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
    for label,old,new in [
        ('wrong-boolean-function','#define F(b,c,d) (((c)^(d))&(b))^(d)','#define F(b,c,d) (((c)^(d))|(b))^(d)'),
        ('wrong-first-rotation','STEP(F,a,b,c,d,7)','STEP(F,a,b,c,d,8)'),
        ('missing-state-accumulation','context->state[0]+=a;','context->state[0]=a;'),
        ('wrong-decoder-byte-count','native_fn_02092ca8(x,input,64)','native_fn_02092ca8(x,input,60)'),
        ('wrong-message-word','native_data_020de898[i]','native_data_020de898[(i+1)&63]')]:cases.append(mutation('02092cb8',label,old,new,[fixtures('02092cb8')[0]],main))
    return cases


def reference_controls(row,body,native,main):
    cases=[]
    for label,offset in [('message-word-index',0xde898),('sine-derived-constant',0xde918)]:
        altered=bytearray(main);altered[offset]^=1;altered=bytes(altered)
        try:verify_reference_tables(altered)
        except ValueError as error:reason=str(error)
        else:raise ValueError('Changed semantic native reference table admitted')
        fixture=fixtures('02092cb8')[0];original=run(row,native,fixture,altered,0);source=run(row,body,fixture,altered,0)
        if original!=source or not original['actualTopReturn'] or not original['modelFailures']:raise ValueError('Independent model failed to distinguish shared wrong reference data')
        cases.append(dict(case=label,semanticRegenerationRejected=True,reason=reason,nativeAndSourceStillByteAndTraceIdentical=True,independentModelRejected=True,actualNativeAndSourceTopReturns=2,modelFailures=original['modelFailures'],fileBytesChanged=False,sourceCredit=0))
    return cases


def execute():
    if LANE!=ROOT/'evidence/lanes/parallel-wave20261105/socl-continuation-next/fifth' or SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/fifth' or WORK!=ROOT/'work/w6sc/fifth-proof':raise ValueError('Exact new production source/evidence/work paths differ')
    if sys.version_info[:3]!=(3,13,5) or unicorn.__version__!='2.1.4':raise ValueError('Pinned fixture runtime differs')
    inputs=read_json(LANE/'inputs.json')
    for p in inputs['files']:
        if sha256(ROOT/p['path'])!=p['sha256']:raise ValueError('Frozen continuation input changed: '+p['path'])
    if {format(int(r['address'],0),'08x') for r in inputs['entries']}!=set(NAMES):raise ValueError('Selected whole-function subset differs')
    info,main,unused=L.measured_module('main');verify_reference_tables(main);rows=[];traces=[];symbols={}
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
    negative=negatives(main);control=controls(rows);control['sharedWrongReferenceTables']=reference_controls(row,body,native,main);write_json(LANE/'binding-layout-controls.json',control)
    raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode();artifact=LANE/'traces.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0))
    limits=['One complete836-byte ordinary-C Thumb compression caller uses measured MW2.0/sp1p6/C99/O4,p/file-IPA/inline-on-noauto and a genuine full native link, with original ELF names/relocations, complete code/pool bytes and actual Thumb mapping. Source is readable four-round word arithmetic; no ordinary-logic ASM, object/register/code patch or prebuilt object input.',
            'Seven complete native/source caller fixtures require actual top returns and equality of full GPR/CPSR, ordered calls/arguments/mode, writes, PCs and8MiB RAM. An independent iterative64-step32-bit model checks complete state, unchanged borrowed context/input/guards, word wrap, all-ones/zero states, block/context alias and aligned input offsets. Four padded single-block cases also match the standard-library digest.',
            'All64 message indices and64 sine-derived constants are independently regenerated and checked against actual native views. Those64-byte and256-byte original initialized views are reference inputs with zero data/storage credit. Their full native prefix hashes, canonical data kinds, literal origins/words and widths are checked with strict wrong-kind/namespace/addend/native-data controls.',
            'The original Thumb little-endian64-byte decode entry is an explicitly scripted ABI boundary that populates the exact measured local word buffer, clobbers caller-saved registers/flags and receives zero execution/source credit. The complete caller executes; no native decode/copy callee body executes. The model does not establish complete TLS or cryptographic security.',
            'Real wrong-C Boolean/rotation/state/message-word/decoder-count variants reject independent state or observed helper ABI. Failure before a top return is recorded separately. Required caller/provider prototypes, actual compiler geometry and original CPU/program/module/mode/entry/complete relocation guards remain enforced.',
            'This is one compression function with original external constant tables retained, not a full source-only ROM or platform execution proof. Exact library revision/original names remain qualified. All earlier READY inputs remain immutable; source credit awaits serialized shared acceptance.']
    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='main',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes'] for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,nativeSymbols={n:b['address'] for n,b in symbols.items()},nativeSymbolModules={n:b['module'] for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,negativeEvidence=negative,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=__import__('hashlib').sha256(raw).hexdigest()),producer=Path(__file__).name,producerSha256=sha256(Path(__file__)),limits=limits))
    print(dict(functions=len(rows),bytes=sum(r['bytes'] for r in rows),cases=len(traces),wrongCVariants=len(negative)),flush=True)


if __name__=='__main__':execute()
