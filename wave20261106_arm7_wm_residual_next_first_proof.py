import gzip
import json
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
import match_runtime as C
import unicorn
from wave20261102_host_arm7_sixth_slice import functions
from wave20261106_arm7_wm_residual_next_first_build import SOURCE,LANE,WORK,build_all
from wave20261106_arm7_wm_residual_next_first_models import fixtures
from wave20261106_arm7_wm_residual_next_first_execution import run
from wave20261106_arm7_wm_residual_next_first_controls import execute as controls


def negative_cases():
    allFixtures=fixtures()
    def choose(entry,**fields):return [f for f in allFixtures if f['entry']==entry and all(f.get(k)==v for k,v in fields.items())][:3]
    return [
      (0x027e2f5c,'0x0001 << parentChannel','0x0002 << parentChannel',choose(0x027e2f5c,channel=15,enabled=65535,code=0)),
      (0x027e2f5c,'status->pparam.maxEntry','status->pparam.maxEntry+1',choose(0x027e2f5c,enabled=65535,code=0)),
      (0x027e2f5c,'(status->pparam), 64','(status->pparam), 62',choose(0x027e2f5c,enabled=65535,code=0)),
      (0x027e2eac,'status->state != WM_STATE_IDLE','status->state == WM_STATE_IDLE',choose(0x027e2eac,state=2)),
      (0x027e2eac,'status->state = WM_STATE_READY','status->state = WM_STATE_IDLE',choose(0x027e2eac,state=2,code=0)),
      (0x027e2eac,'PM_LED_PATTERN_ON','PM_LED_PATTERN_ON+1',choose(0x027e2eac,state=2,code=0)),
      (0x027e5790,'mpLifeTime == 0','mpLifeTime == 1',choose(0x027e5790,lifetime=0,code=0)),
      (0x027e5790,'037fd21c() | 1','037fd21c() | 0',choose(0x027e5790,tick=0,code=0)),
      (0x027e5790,'i < 1 + 15','i < 1 + 14',choose(0x027e5790,code=0)),
      (0x027e5a98,'cb->apiid = WM_APIID_INIT_W_COUNTER','cb->apiid = WM_APIID_INIT_W_COUNTER+1',choose(0x027e5a98,code=0)),
      (0x027e5b00,'), 180)', '), 176)',choose(0x027e5b00,code=0)),
      (0x027e5b00,'cb->apiid = WM_APIID_GET_W_COUNTER','cb->apiid = WM_APIID_GET_W_COUNTER+1',choose(0x027e5b00,code=0))]



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
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261106/wm-residual-next/first' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/arm7-wm-residual-next/first' or WORK!=ROOT/'work/w6wr/first':raise ValueError('New WM port proof source/evidence/work scope changed')
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
      'Five complete admitted host ARM7-main ARMv4T WM request functions,904 whole bytes. Closed readable ordinary C and headers compile with actual2.0/base O4,s/on,noauto/file-IPA/-lang c99 and genuinely link every unchanged original ELF relocation/addend through zero-code original ARM anchors.',
      '52 independent original/source caller pairs cover parent64-byte copy before channel validation/maxEntry16, End illegal-state/wireless failure/STOP-to-READY LED ordering, lifetime low16 narrowing/0/FFFF/64-bit tick arithmetic and16 full64-bit receive timestamps, counter initialization/results and exact180-byte counter copy preserving callback padding/canaries. All modeled imported bodies execute0.',
      'The TI925T ARMv4T caller harness checks actual returning GPR/CPSR/SP/writes/full8MiB RAM and128KiB WRAM hashes, bounded frame/data writes, every exact provider address/ARM state/argument word and independently predicted complete borrowed regions. Scripted providers model no hardware,radio,scheduler,callee-body or platform behavior.',
      'Twelve genuinely linked wrong-C controls, all original relocation binding/mode/namespace/addend controls, complete per-origin instruction/literal controls, three geometry negatives, fresh actual signed/unsigned/pointer/64-bit ABI probes, actual required-prototype negatives and independent C99 whole-body/relocation/full-link replay are mandatory. Aborted wrong-C cases are not returning callers.',
      'Original module images are comparison/execution reference only, never original executable compiler inputs. Minimal immutable static boundary/layout/native/source/tool inputs are production dependencies. Historical admission/proposal/claim epochs and SDK materialization remain diagnostic provenance. All prior packets remain immutable; accepted source credit awaits shared coordinator acceptance.']
    symbols={}
    for row in rows:
        for name,binding in row['nativeSymbolEntries'].items():
            if name in symbols and symbols[name]!=binding:raise ValueError('Conflicting report-level complete original ARM7 bindings')
            symbols[name]=binding
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm7',program='',module='arm7-main',allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes'] for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecutedInCallerFixtures=0,nativeSymbols={n:b['address']for n,b in symbols.items()},nativeSymbolModules={n:b['module']for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,calleeSourceCredit=0,externalStorageCredit=0,fixtureInstructionCoverage=covered,fixtureCoveredOriginalInstructionBytes=sum(r['originalInstructionBytes'] for r in covered),negativeEvidence=negative,controls=dict(path=(LANE/'controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'controls.json')),inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(__file__),limits=limits)
    write_json(LANE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairedCases=len(traces),genuineWrongC=len(negative),boundedInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':execute()
