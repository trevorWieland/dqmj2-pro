import gzip
import json
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
import match_runtime as C
import unicorn
from wave20261102_host_arm7_sixth_slice import functions
from wave20261106_arm7_wm_residual_next_third_build import SOURCE,LANE,WORK,build_all
from wave20261106_arm7_wm_residual_next_third_models import fixtures
from wave20261106_arm7_wm_residual_next_third_execution import run
from wave20261106_arm7_wm_residual_next_third_controls import execute as controls


def negative_cases():
    allFixtures=fixtures()
    def choose(entry,**fields):return [f for f in allFixtures if f['entry']==entry and all(f.get(k)==v for k,v in fields.items())][:3]
    return [
      (0x027e03d0,'pReq->retryLimit = 7','pReq->retryLimit = 6',choose(0x027e03d0,code=0)),
      (0x027e03d0,'status->wep_flag == 0','status->wep_flag != 0',choose(0x027e03d0,wep=1,code=0)),
      (0x027e0520,'rssiIndex + 1','rssiIndex + 2',choose(0x027e0520,index=31)),
      (0x027e0520,'rssiHistory[native_host_arm7_data_027f7884.rssiIndex]','rssiHistory[native_host_arm7_data_027f7884.rssiIndex^1]',choose(0x027e0520,index=0)),
      (0x027e5c5c,'status->v_tsf_bak != status->v_tsf','status->v_tsf_bak == status->v_tsf',choose(0x027e5c5c,tsf=1,bak=1,remain=0)),
      (0x027e5c5c,'status->VSyncFlag = 1','status->VSyncFlag = 0',choose(0x027e5c5c,tsf=1,bak=1,remain=0)),
      (0x027e5dc0,'status->VSyncFlag = 0','status->VSyncFlag = 1',choose(0x027e5dc0,vcount=207,remain=127)),
      (0x027e5e80,'status->mp_flag == 1','status->mp_flag != 0',choose(0x027e5e80,flag=2)),
      (0x027e5e80,'(now - last) >','(now - last) >=',choose(0x027e5e80,lifetime=1,last=100,now=100)),
      (0x027e5f98,'status->valarm_counter >= 60','status->valarm_counter > 60',choose(0x027e5f98,counter=60,vcount=203)),
      (0x027e5f98,'vcount < 210','vcount <= 210',choose(0x027e5f98,counter=60,vcount=210))]



def wrong_c(case,ordinal,images):
    entry,old,new,selected=case;function='native_host_arm7_main_'+format(entry,'08x') if isinstance(entry,int) else entry;directory=WORK/'wrong-c'/str(ordinal)
    if not selected:raise ValueError('Meaningful wrong-C fixture selection empty')
    directory.mkdir(parents=True,exist_ok=True)
    sourceDir=SOURCE/format(entry,'08x');directory=directory/format(entry,'08x');directory.mkdir(parents=True,exist_ok=True)
    for p in sourceDir.iterdir():
        if p.is_file():(directory/p.name).write_bytes(p.read_bytes())
    found=[]
    for path in directory.iterdir():
        if path.suffix not in ['.c','.h']:continue
        text=path.read_text()
        for f in functions(text):
            if f['name']==function:found.append((path,text,f))
    if len(found)!=1:raise ValueError('Wrong-C target function is not unique')
    path,text,fragment=found[0];start,end=fragment['start'],fragment['end'];part=text[start:end]
    if part.count(old)!=1:raise ValueError(('Meaningful ordinary-C mutation ambiguous',function,old,part.count(old)))
    path.write_text(text[:start]+part.replace(old,new)+text[end:]);affected={'native_host_arm7_main_'+format(f['entry'],'08x') for f in selected};rows,outputs=build_all(directory/'build',{next(iter(affected)):directory/'main.c'},affected,affected);by={int(r['address'],0):r for r in rows};reject=[]
    for n,f in enumerate(selected):
        row=by[f['entry']]
        try:
            result=run(row,outputs[row['name']],f,images,n)
            if not result['modelFailures']:raise ValueError(('Wrong-C failed to alter independently modeled behavior',function,old,n))
            reject.append(dict(ordinal=n,actualTopReturn=result['actualTopReturn'],modelFailures=result['modelFailures']))
        except unicorn.UcError as error:reject.append(dict(ordinal=n,actualTopReturn=False,rejectedAtMemoryBoundary=True,error=str(error)))
    return dict(case=ordinal,function=function,old=old,new=new,genuinelyLinkedWrongC=rows,fixtures=selected,rejected=reject,abortedRunsAreNotCallerReturns=True)


def execute():
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261106/wm-residual-next/third' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/arm7-wm-residual-next/third' or WORK!=ROOT/'work/w6wr/third':raise ValueError('New WM port proof source/evidence/work scope changed')
    if unicorn.__version__!='2.1.4':raise ValueError('Pinned actual native unit runtime differs')
    inputs=read_json(LANE/'inputs.json')
    for p in inputs['files']:
        if sha256(ROOT/p['path'])!=p['sha256']:raise ValueError('Frozen actual WM port compiler/source/native/runtime input changed: '+p['path'])
    rows,outputs=build_all(WORK/'proof-positive');by={int(r['address'],0):r for r in rows};images=[(int(m['base'],0),(ROOT/m['binary']).read_bytes()) for m in read_json(ROOT/'evidence/arm7/runtime-layout.json')['modules']];traces=[];coverage={r['address']:set() for r in rows}
    for n,f in enumerate(fixtures()):
        row=by[f['entry']];image=(ROOT/row['binary']).read_bytes();native=image[f['entry']-row['base']:f['entry']-row['base']+row['bytes']];original=run(row,native,f,images,n);rebuilt=run(row,outputs[row['name']],f,images,n)
        if original!=rebuilt or original['modelFailures'] or not original['actualTopReturn']:
            write_json(WORK/'fixture-failure.json',dict(ordinal=n,fixture=f,original=original,rebuilt=rebuilt));raise ValueError('Independent complete WM port caller/model mismatch')
        coverage[row['address']].update(a for a in original['pcs'] if f['entry']<=a<f['entry']+row['bytes']);traces.append(dict(ordinal=n,fixture=f,result=original))
    print(dict(positiveNativeSourcePairs=len(traces),functions=len(rows),bytes=sum(r['bytes'] for r in rows)),flush=True);negative=[wrong_c(case,n,images) for n,case in enumerate(negative_cases())];controlled=controls(rows);write_json(LANE/'controls.json',controlled);raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode();artifact=LANE/'traces.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0));covered=[dict(address=address,originalInstructionBytes=4*len(pcs),completeNativeSpanBytes=by[int(address,0)]['bytes']) for address,pcs in coverage.items()]
    limits=[
      'Six complete admitted host ARM7-main ARMv4T WM functions,1416 whole bytes. Closed readable ordinary C and headers compile with actual2.0/base O4,s/on,noauto/file-IPA/-lang c99 and genuinely link all37 original relocation/addend records. Borrowed wmspW and OSVAlarm are accurate typed extern declarations, with no new source-owned BSS/static storage.',
      '131 independent original/source caller pairs cover complete request-all fields/WEP/SSID masks/result propagation, RSSI ring/pool wrapping, child VTSF/frame remainder arithmetic, VCOUNT adjustment boundaries and signed callback counts, MP lifetime64-bit subtraction/wrap/equality/message allocation and enqueue outcomes, parent VCOUNT counter and low/high TSF rollover reads. Exact full borrowed regions and controlled MMIO sequences/writes are independently predicted.',
      'Synthetic video/WiFi/TSF pages are controlled arithmetic/register witnesses only, with no DS/radio/timer/scheduler/hardware execution claim. All imported bodies and scheduled callback bodies execute0 in these caller fixtures; imported callbacks/callees and borrowed storage receive0 source credit.',
      'Five exact original ABS32 callback words are qualified as existing canonical ARM7-main ARM function pointers, with actual C99 typed pointer objects/genuine zero-code STT_FUNC/$a anchors and CPU/program/module/sourceModule/mode/provider/origin/addend/entry/caller-hash negatives. Undefined production symbols remain actual MW STT_NOTYPE; no original source object/symbol/relocation rewrite or alternate entry aliases.',
      'Meaningful genuinely linked wrong-C, exact original binding/per-origin boundary/geometry/prototype/fresh actual ABI and independent C99 whole-body/relocation/genuine-link checks are required. Source-only and canonical copied-root rebuilds must pass before READY; all earlier packets remain immutable and accepted source credit awaits shared coordinator acceptance.']
    symbols={}
    for row in rows:
        for name,binding in row['nativeSymbolEntries'].items():
            if name in symbols and symbols[name]!=binding:raise ValueError('Conflicting report-level complete original ARM7 bindings')
            symbols[name]=binding
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm7',program='',module='arm7-main',allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes'] for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecutedInCallerFixtures=0,nativeSymbols={n:b['address']for n,b in symbols.items()},nativeSymbolModules={n:b['module']for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,calleeSourceCredit=0,externalStorageCredit=0,fixtureInstructionCoverage=covered,fixtureCoveredOriginalInstructionBytes=sum(r['originalInstructionBytes'] for r in covered),negativeEvidence=negative,controls=dict(path=(LANE/'controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'controls.json')),inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(__file__),limits=limits)
    write_json(LANE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairedCases=len(traces),genuineWrongC=len(negative),boundedInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':execute()
