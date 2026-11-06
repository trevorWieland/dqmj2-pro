import gzip
import json
from pathlib import Path
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link
import match_main_oam_reference296_closed_20261101 as builder
import main_joint_blend1004_fixture_20261102 as fixture

WORK=ROOT/'work/main-joint-blend1004-qualified-20261102'
REPORT=ROOT/'evidence/matches/main-joint-blend1004-20261102.json'
SOURCE=ROOT/'src/runtime/20261102_joint_blend1004_v2/native_main_0202de74.c'


def main():
    config=configuration();assert sha256(config['rom'])==config['romSha256']
    metadata,image,_=measured_module('main');assert metadata['sha256']=='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
    builder.WORK=WORK;row,proof,body=builder.build(SOURCE,SOURCE.stem,True);assert len(body)==1004
    row.update(exactBytes=1004,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceLanguage='C',genuineLinkComparison=freeze_link(proof))
    bodies={fixture.ENTRY:body};cases=[];excluded=[];observed=set();pools=set();hardware=helper_returns=callbacks=0
    for index in range(2048):
        try:fixture.inputs(index)
        except fixture.DegenerateRotation as error:excluded.append(dict(index=index,reason=str(error)));continue
        original=fixture.execute(image,{},index);candidate=fixture.execute(image,bodies,index)
        assert original==candidate and original['modelPassed'],(index,original['context'])
        cases.append(original);observed.update(original['ownObserved']);hardware+=len(original['hardwareOperations'])*2
        helper_returns+=len(original['actualHelperReturns'])*2;callbacks+=len(original['suppliedCallbacks'])*2
        for address,size,value in original['reads']:
            if fixture.ENTRY<=address and address+size<=fixture.ENTRY+1004:pools.update(range(address,address+size))
    controls=[];text=SOURCE.read_text(encoding='utf-8')
    for label,old,new in[('false-return','return 0 ;','return 1 ;'),
     ('disabled-map','NNS_G3D_ANMOBJ_MAPDATA_DISABLED  = 0x0200','NNS_G3D_ANMOBJ_MAPDATA_DISABLED  = 0x0400')]:
        changed=text.replace(old,new);assert changed!=text
        wrong=ROOT/f'nonmatching/integration/20261102-joint-blend1004/{label}/source.c';wrong.parent.mkdir(parents=True,exist_ok=True)
        if wrong.exists():assert wrong.read_text(encoding='utf-8')==changed
        else:wrong.write_text(changed,encoding='utf-8')
        bad_row,bad_proof,bad_body=builder.build(wrong,label,False);assert len(bad_body)<=1004
        results=[fixture.execute(image,{fixture.ENTRY:bad_body},c['index'])for c in cases]
        rejected=sum(not row['modelPassed']for row in results);assert rejected
        controls.append(dict(label=label,source=wrong.relative_to(ROOT).as_posix(),sourceSha256=sha256(wrong),
         actualWrongReturns=len(results),rejected=rejected,positiveControls=len(results)-rejected))
    try:fixture.execute(image,bodies,0,bound=1)
    except AssertionError:pass
    else:raise AssertionError('Prefix counted as return')
    own={a for a in observed if fixture.ENTRY<=a<fixture.ENTRY+1004}
    missing=[hex(a)for a in range(fixture.ENTRY,fixture.ENTRY+1004,4)if a not in own and a not in{p&~3 for p in pools}]
    trace=ROOT/'evidence/traces/main-joint-blend1004-20261102.json.gz'
    trace.write_bytes(gzip.compress(json.dumps(dict(cases=cases),sort_keys=True,separators=(',',':')).encode(),mtime=0))
    write_json(REPORT,dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),romSha256=config['romSha256'],
     processor='arm9',program='',module='main',moduleSha256=metadata['sha256'],matches=[row],matchedFunctions=1,matchedBytes=1004,
     oracle=dict(pairs=len(cases),actualTopReturns=2*len(cases),actualNativeHelperReturns=helper_returns,explicitSuppliedCallbackCalls=callbacks,cpu='ARM946',
      ownInstructionBytesObserved=len(own)*4,generatedPoolBytes=len(pools),unobservedCodeAddresses=missing,
      actualModeledHardwareOperations=hardware,completeRegistersFlagsMainInputStackOrderedReadsWritesCompared=True,
      independentListFilteringWeightingResultFlagsAndQuantizedAxes=True,excludedInputs=excluded),
     negativeControls=controls,replayDependencies=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in[Path(fixture.__file__),trace]],
     reproductionCommand='python match_main_joint_blend1004_20261102.py',limitations=[
      'Synthetic0..4-node initialized lists and node0..4 with bounded signed ratios; supplied callback outputs are actual88-byte initialized result records',
      'Original memory/cross/normalization/scale/division helper instructions execute; callbacks supply typed result data with volatile register/flag clobbers',
      'Cases requiring an uninitialized first-node fallback basis or zero normalization denominator are excluded before execution',
      'Math hardware completes immediately; no timing/interrupt/error path or complete animation scene claim',
      'Correct selected division/blend-scale prototypes preserve bytes; callee bodies and data receive no extra credit',
      'No source-only ROM, native Windows execution of this group, full game or Android device proof']))
    print(dict(functions=1,bytes=1004,pairs=len(cases),actualReturns=2*len(cases),nativeHelpers=helper_returns,
     callbacks=callbacks,hardwareOperations=hardware,observedBytes=len(own)*4,poolBytes=len(pools),
     wrongReturns=sum(c['actualWrongReturns']for c in controls),wrongRejected=sum(c['rejected']for c in controls),excluded=len(excluded),missing=missing))


if __name__=='__main__':
    main()
