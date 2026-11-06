import gzip
import json
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
import match_runtime as C
import unicorn
from wave20261102_host_arm7_sixth_slice import functions
from wave20261106_arm7_wm_residual_next_fourth_build import SOURCE,LANE,WORK,build_all
from wave20261106_arm7_wm_residual_next_fourth_models import fixtures
from wave20261106_arm7_wm_residual_next_fourth_execution import run
from wave20261106_arm7_wm_residual_next_fourth_controls import execute as controls


def negative_cases():
    allFixtures=fixtures()
    def choose(entry,**fields):return [f for f in allFixtures if f['entry']==entry and all(f.get(k)==v for k,v in fields.items())][:3]
    return [
      (0x027e2a90,'status->mp_flag == 1','status->mp_flag != 0',choose(0x027e2a90,mp=2)),
      (0x027e2a90,'status->pparam.entryFlag = 0','status->pparam.entryFlag = 1',choose(0x027e2a90,state=7)),
      (0x027e2a90,'sizeof(status->childMacAddress)','sizeof(status->childMacAddress)-2',choose(0x027e2a90,fail='none')),
      (0x027e2a90,'status->state != WM_STATE_CHILD','0',choose(0x027e2a90,mutateState=True)),
      (0x027e2a90,'auth_retry < 2','auth_retry < 1',[f for f in allFixtures if f['kind']=='reset'and f['codes']==[7,0]]),
      (0x027e2a90,'status->wep_flag = 0','status->wep_flag = 1',choose(0x027e2a90,station=16)),
      (0x027e2a90,'0x14 ,','0x0a ,',choose(0x027e2a90,station=17,mode=0)),
      (0x027e3850,'wm_rssi_pool << 1','wm_rssi_pool << 0',choose(0x027e3850,pool=32768)),
      (0x027e3850,'rssi_pool >> 16','rssi_pool >> 15',choose(0x027e3850,pool=32768))]



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
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261106/wm-residual-next/fourth' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/arm7-wm-residual-next/fourth' or WORK!=ROOT/'work/w6wr/fourth':raise ValueError('New WM port proof source/evidence/work scope changed')
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
      'Two complete admitted host ARM7-main ARMv4T functions,1032 whole bytes: Reset1004 and RSSI pool28. Closed readable ordinary C/headers compile with actual2.0/base O4,s/on,noauto/file-IPA/-lang c99 and genuinely link all30 unchanged original relocation/addend records.',
      'The pinned primary Reset body is adapted only by the independently measured status.state==8 guard before each child deauthentication retry, matching original027e2ca4..027e2cac exactly. No allocation/profile search, original object/register/instruction/symbol/relocation patch or algorithm ASM is used. The unused-parent-discriminator behavior outside assigning parent/child states is retained as historical source uncertainty; caller fixture preconditions explicitly require that discriminator assigned.',
      '83 independent original/source caller pairs cover parent/child and MP transitions, exactTRUE cleanup versus other values, sparse child/parent disconnection pointers, all station/mode switch paths, wireless failure stages, retry7/12 versus other failures, asynchronous state change that stops the next retry, final flags/callback and RSSI pool upper-bit folding. These fixtures do not establish Reset behavior outside the stated initializing-state precondition.',
      'Every imported body executes0 in returning caller fixtures; wireless/error/copy/IRQ/message providers are controlled explicit contracts, not full callee/device/scheduler/game/platform execution. Borrowed WMStatus/WMSPWork/OSSystemWork and all anchors/storage receive0 source credit.',
      'Meaningful genuine wrong-C, all original namespace/mode/origin/addend/binding and per-origin instruction/literal negatives, actual compiler geometry/prototype/ABI and independent C99 whole-body/relocation/full links are mandatory. Source-only and canonical copied-root replay must pass before READY. All earlier packets remain immutable; source credit awaits shared acceptance.']
    symbols={}
    for row in rows:
        for name,binding in row['nativeSymbolEntries'].items():
            if name in symbols and symbols[name]!=binding:raise ValueError('Conflicting report-level complete original ARM7 bindings')
            symbols[name]=binding
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm7',program='',module='arm7-main',allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes'] for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecutedInCallerFixtures=0,nativeSymbols={n:b['address']for n,b in symbols.items()},nativeSymbolModules={n:b['module']for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,calleeSourceCredit=0,externalStorageCredit=0,fixtureInstructionCoverage=covered,fixtureCoveredOriginalInstructionBytes=sum(r['originalInstructionBytes'] for r in covered),negativeEvidence=negative,controls=dict(path=(LANE/'controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'controls.json')),inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(__file__),limits=limits)
    write_json(LANE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairedCases=len(traces),genuineWrongC=len(negative),boundedInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':execute()
