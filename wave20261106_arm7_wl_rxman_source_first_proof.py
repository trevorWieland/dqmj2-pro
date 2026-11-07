import gzip
import json
from pathlib import Path
import match_runtime as C
import unicorn
from project import ROOT,read_json,write_json,sha256,configuration
from wave20261106_arm7_wl_rxman_source_first_build import SOURCE,LANE,WORK,build_all
from wave20261106_arm7_wl_rxman_source_first_models import fixtures
from wave20261106_arm7_wl_rxman_source_first_execution import run
from wave20261106_arm7_wl_rxman_source_first_controls import execute as controls


def negative_cases():
    values=fixtures()
    def choose(**fields):return[f for f in values if all(f.get(k)==v for k,v in fields.items())][:1]
    return[
      (0x27f3f40,'pCounter->rx.multicast++;','pCounter->rx.multicast+=2;',choose(multicast=True)),
      (0x27f3f40,' / (0x0001 << 4)) - 1);',' / (0x0001 << 4)) - 2);',choose(fragments=0)),
      (0x27f3f40,'pCounter->rx.duplicateErr++;','pCounter->rx.duplicateErr+=2;',choose(duplicate=True)),
      (0x27f3f40,'pFrm->FirmHeader.CamAdrs = 0;','pFrm->FirmHeader.CamAdrs = 1;',choose(cam=255,mode=1,subtype=11)),
      (0x27f3f40,'RxManCtrl).Count) != 0','RxManCtrl).Count) == 0',choose(remaining=0,empty=False))]


def wrong_c(case,ordinal,images):
    entry,old,new,selected=case;tag=format(entry,'08x');name='native_host_arm7_main_'+tag;directory=WORK/'wrong-c'/str(ordinal)/tag
    if not selected:raise ValueError(('Meaningful wrong-C selection empty',name,old))
    directory.mkdir(parents=True,exist_ok=True)
    for path in (SOURCE/tag).iterdir():
        if path.is_file():(directory/path.name).write_bytes(path.read_bytes())
    path=directory/'main.c';text=path.read_text()
    if text.count(old)!=1:raise ValueError(('Meaningful ordinary C mutation not unique',name,old,text.count(old)))
    path.write_text(text.replace(old,new));rows,outputs=build_all(directory/'build',{name:path},{name},{name});row=rows[0];rejected=[]
    for number,f in enumerate(selected):
        try:
            result=run(row,outputs[name],f,images,number)
            if not result['modelFailures']:raise ValueError(('Wrong C did not alter modeled behavior',name,old))
            rejected.append(dict(actualTopReturn=result['actualTopReturn'],modelFailures=result['modelFailures']))
        except unicorn.UcError as error:rejected.append(dict(actualTopReturn=False,rejectedAtMemoryBoundary=True,error=str(error)))
    return dict(case=ordinal,function=name,old=old,new=new,genuinelyLinkedWrongC=rows,fixtures=selected,rejected=rejected,abortedRunsAreNotCallerReturns=True)


def execute():
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261106/wl-rxman-next/first' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/arm7-wl-rxman-next/first' or WORK!=ROOT/'work/w6rxm/first':raise ValueError('Exact newly owned PM source/evidence/work scope differs')
    if unicorn.__version__!='2.1.4':raise ValueError('Actual native ARMv4T fixture runtime differs')
    inputs=read_json(LANE/'inputs.json')
    for pin in inputs['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Frozen actual PM compiler/source/native/runtime input changed: '+pin['path'])
    rows,outputs=build_all(WORK/'proof-positive')
    from closed_c_compiler_inputs_20261105 import compiler_inputs
    for row in rows:compiler_inputs(row)
    by={int(r['address'],0):r for r in rows};images=[(int(m['base'],0),(ROOT/m['binary']).read_bytes())for m in read_json(ROOT/'evidence/arm7/runtime-layout.json')['modules']];traces=[];coverage={r['address']:set()for r in rows}
    for number,f in enumerate(fixtures()):
        row=by[f['entry']];image=(ROOT/row['binary']).read_bytes();native=image[f['entry']-row['base']:f['entry']-row['base']+row['bytes']];original=run(row,native,f,images,number);rebuilt=run(row,outputs[row['name']],f,images,number)
        if original!=rebuilt or original['modelFailures']or not original['actualTopReturn']:
            write_json(WORK/'fixture-failure.json',dict(ordinal=number,fixture=f,original=original,rebuilt=rebuilt));raise ValueError('Independent complete PM caller/model mismatch')
        coverage[row['address']].update(pc for pc in original['pcs']if f['entry']<=pc<f['entry']+row['bytes']);traces.append(dict(ordinal=number,fixture=f,result=original))
    print(dict(positiveNativeSourcePairs=len(traces),functions=len(rows),bytes=sum(r['bytes']for r in rows)),flush=True)
    negative=[wrong_c(case,number,images)for number,case in enumerate(negative_cases())];controlled=controls(rows);write_json(LANE/'controls.json',controlled);raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode();artifact=LANE/'traces.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0));symbols={}
    for row in rows:
        for name,binding in row['nativeSymbolEntries'].items():
            if name in symbols and symbols[name]!=binding:raise ValueError('Conflicting complete report-level ARM7 PM symbols')
            symbols[name]=binding
    covered=[dict(address=address,originalInstructionBytes=4*len(pcs),completeNativeSpanBytes=by[int(address,0)]['bytes'])for address,pcs in coverage.items()]
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],program='',processor='arm7',module='arm7-main',allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes']for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecutedInCallerFixtures=0,nativeSymbols={n:b['address']for n,b in symbols.items()},nativeSymbolModules={n:b['module']for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,calleeSourceCredit=0,externalStorageCredit=0,fixtureInstructionCoverage=covered,fixtureCoveredOriginalInstructionBytes=sum(r['originalInstructionBytes']for r in covered),negativeEvidence=negative,controls=dict(path=(LANE/'controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'controls.json')),inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(__file__),limits=[
      'One complete HOST ARM7-main ARMv4T published RxManCtrlTask caller1716B,1704instruction+12literal bytes;61actual PC24/-8 call relocations preserved by genuine source/split/MWlink. Same-TU measured2.0/sp1p5 C99/O4/inline-on/fileIPA,closed ordinary C plus published helpers needed for natural inlining,zero assembler/object/instruction patch.',
      '84 independent original/source pairs compare all GPRs,CPSR,callee-saved registers/SP,ordered writes/imports and every byte of synthetic1684-byte WL state/528-byte packet and request/confirmation/output buffers. Empty queue,all outer type/mode/subtype dispatch branches,255/zero/nonnull station IDs,counter wrap/zero fragments,duplicate sequence and post-provider queue-count rereads are bounded caller contracts.',
      'Provider frame-control mutation verifies type/subtype values captured before lookup versus power-management bit reread later. Inlined PS-Poll covers old-class gates and both priority queues;association/reassociation cover inactive states,MAC mismatch and error-confirmation paths;reassociation-request covers exact length10/11 and duplicate/deauthentication allocation/send early paths.',
      'Successful association/capability/element-checker/AID and full reassociation validation paths remain outside semantic fixture coverage;dynamic instruction coverage is reported separately from complete byte/link equality. All imported provider bodies execute0instructions and earn0source/storage credit.',
      'The fixed wlMan pointer word/globalWL views,borrowed queues/frames/callback buffers have0new storage ownership/credit. All source-visible sizes are compiler consumed views,not proof of complete native allocation. Caller C export isvoid;incidental CPU return registers are compared without invented portable return meaning.',
      'No physicalWiFi/radio/IRQ/device/network/timing/concurrency/game execution or complete portableABI claim. Ordinary shared acceptance alone grants source credit;independent models/genuine mutants/fresh layouts/strict prototypes/native bindings/boundaries/canonical copied-root proof remain mandatory.'
 ])
    write_json(LANE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairedCases=len(traces),genuineWrongC=len(negative),boundedInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':execute()
