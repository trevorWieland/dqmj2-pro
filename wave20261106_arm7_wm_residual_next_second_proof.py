import gzip
import json
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
import match_runtime as C
import unicorn
from wave20261102_host_arm7_sixth_slice import functions
from wave20261106_arm7_wm_residual_next_second_build import SOURCE,LANE,WORK,build_all
from wave20261106_arm7_wm_residual_next_second_models import fixtures
from wave20261106_arm7_wm_residual_next_second_execution import run
from wave20261106_arm7_wm_residual_next_second_controls import execute as controls


def negative_cases():
    allFixtures=fixtures()
    def choose(entry,**fields):return [f for f in allFixtures if f['entry']==entry and all(f.get(k)==v for k,v in fields.items())and(entry!=0x027e386c or all(f.get(k)==v for k,v in dict(state=2,channels=3,enabled=65535,pointer=0x0230a000,size=512,misc=0).items()))][:3]
    return [
      (0x027e386c,'scanChannelList <<= 1','scanChannelList <<= 0',choose(0x027e386c,fail='none',state=2,found=0)),
      (0x027e386c,'ssidMatchLength <= 32','ssidMatchLength < 32',choose(0x027e386c,fail='none',scanType=2,found=0)),
      (0x027e386c,'callback->bssDescCount = 0','callback->bssDescCount = 1',choose(0x027e386c,fail='none',state=2,found=0)),
      (0x027e386c,'if (scanSsidLength > 0)','if (scanSsidLength == 0)',choose(0x027e386c,fail='none',found=2)),
      (0x027e3ed0,'status->state != WM_STATE_IDLE','status->state == WM_STATE_IDLE',choose(0x027e3ed0,state=2,misc=0,attribute=1,channel=1,enabled=65535,fail='params')),
      (0x027e3ed0,'p->connectPInfo.gameInfoLength >= 16','p->connectPInfo.gameInfoLength >= 17',choose(0x027e3ed0,attribute=0)),
      (0x027e3ed0,'10 * 1000 / p->connectPInfo.beaconPeriod','10 * 100 / p->connectPInfo.beaconPeriod',choose(0x027e3ed0,fail='beacon',period=100)),
      (0x027e4be0,'status->mp_pingCounter = 60','status->mp_pingCounter = 59',choose(0x027e4be0,state=8,small=False,allowed=0x3fff)),
      (0x027e4be0,'recvBuf + recvBufSize','recvBuf + recvBufSize+4',choose(0x027e4be0,state=8,small=False,allowed=0x3fff)),
      (0x027e4be0,'(1 + 15 )','(1 + 14 )',choose(0x027e4be0,state=8,small=False,allowed=0x3fff)),
      (0x027e4be0,'status->mp_flag = 1','status->mp_flag = 0',choose(0x027e4be0,state=8,small=False,allowed=0x3fff))]



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
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261106/wm-residual-next/second' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/arm7-wm-residual-next/second' or WORK!=ROOT/'work/w6wr/second':raise ValueError('New WM port proof source/evidence/work scope changed')
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
      'Three complete admitted host ARM7-main ARMv4T WM callers,3660 whole bytes. Closed readable ordinary C and headers compile with actual2.0/base O4,s/on,noauto/file-IPA/-lang c99 and genuinely link all106 unchanged original ELF relocation records/addends through qualified original ARM anchors.',
      '66 independent original/source caller pairs cover scan legal/illegal states and channel/buffer validation, station/class/power/preamble/mask errors, all four scan modes/SSID mask boundaries, zero/one/two scan results, variable descriptor sizes/alignment/SSID repair/RSSI boundaries; MP size/channel validation, queue cleanup, nested IRQ/parameter contexts, child/parent success, every16 timestamp and post-success wireless errors; connect state/entry/channel/rate/preamble and parameter/beacon/class/power prefix paths.',
      'Connect caller fixtures deliberately stop before join/authenticate/associate; those later native instructions remain independently complete byte/relocation/genuine-link matches without behavioral fixture coverage. Caller fixtures execute zero imported bodies and claim no radio/hardware/scheduler/provider/storage/platform reconstruction.',
      'Separate genuine C99 signed/unsigned quotient/remainder ABI probes execute actual original ARM7-wram helpers at only the exact canonical entries, checking28 returning compiler/native-helper runs. Helper4-byte entry witnesses are not inferred function extents; helper code/source credit0. Original _u32_div_f/_s32_div_f ELF symbols are unchanged, with no ARM9 fallback, object/relocation rewrite or invented callable aliases.',
      'Meaningful genuinely linked wrong-C, exact original binding/CPU/program/module/mode/provider/origin/addend/hash/profile/sourceModule negatives, per-origin boundary negatives, geometry/prototype/actual ABI and independent C99 whole-body/relocation/full-link replays are mandatory. Source-only and canonical copied-root rebuilds must pass before READY. All prior packets remain immutable; source credit awaits shared acceptance.']
    symbols={}
    for row in rows:
        for name,binding in row['nativeSymbolEntries'].items():
            if name in symbols and symbols[name]!=binding:raise ValueError('Conflicting report-level complete original ARM7 bindings')
            symbols[name]=binding
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm7',program='',module='arm7-main',allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes'] for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecutedInCallerFixtures=0,nativeSymbols={n:b['address']for n,b in symbols.items()},nativeSymbolModules={n:b['module']for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,calleeSourceCredit=0,externalStorageCredit=0,fixtureInstructionCoverage=covered,fixtureCoveredOriginalInstructionBytes=sum(r['originalInstructionBytes'] for r in covered),negativeEvidence=negative,controls=dict(path=(LANE/'controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'controls.json')),inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(__file__),limits=limits)
    write_json(LANE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairedCases=len(traces),genuineWrongC=len(negative),boundedInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':execute()
