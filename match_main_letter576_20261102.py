import gzip
import json
from pathlib import Path
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link
import match_main_oam_reference296_closed_20261101 as builder
import main_letter576_fixture_20261102 as fixture

WORK=ROOT/'work/main-letter576-qualified-20261102'
REPORT=ROOT/'evidence/matches/main-letter576-20261102.json'
SOURCE=ROOT/'src/runtime/20261102_letter576_v2/native_main_02035788.c'
HELPER=ROOT/'src/runtime/20261101_g2d796/native_main_02034ab8.c'


def main():
    config=configuration();assert sha256(config['rom'])==config['romSha256']
    metadata,image,_=measured_module('main');assert metadata['sha256']=='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
    builder.WORK=WORK;rows=[];bodies={}
    for path in[SOURCE,HELPER]:
        row,proof,body=builder.build(path,path.stem,True);assert len(body)==fixture.SPANS[int(row['address'],0)]
        row.update(exactBytes=len(body),sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceLanguage='C',genuineLinkComparison=freeze_link(proof))
        rows.append(row);bodies[int(row['address'],0)]=body
    cases=[];observed=set();pools=set();helpers=0
    for index in range(2048):
        original=fixture.execute(image,{},index);candidate=fixture.execute(image,bodies,index)
        assert original==candidate and original['modelPassed'],(index,original['context'])
        cases.append(original);observed.update(original['ownObserved']);helpers+=original['actualBitReaderReturns']*2
        for address,size,value in original['reads']:
            if fixture.ENTRY<=address and address+size<=fixture.ENTRY+576:pools.update(range(address,address+size))
    controls=[];text=SOURCE.read_text(encoding='utf-8')
    for label,old,new in[('transparency','if ( bits != 0 )','if ( bits == 0 )'),('palette','cl + bits','cl ^ bits')]:
        changed=text.replace(old,new);assert changed!=text
        wrong=ROOT/f'nonmatching/integration/20261102-letter576/{label}/source.c';wrong.parent.mkdir(parents=True,exist_ok=True)
        if wrong.exists():assert wrong.read_text(encoding='utf-8')==changed
        else:wrong.write_text(changed,encoding='utf-8')
        row,proof,body=builder.build(wrong,label,False);assert len(body)<=576
        results=[fixture.execute(image,{**bodies,fixture.ENTRY:body},i)for i in range(512)]
        rejected=sum(not r['modelPassed']for r in results);assert rejected
        controls.append(dict(label=label,source=wrong.relative_to(ROOT).as_posix(),sourceSha256=sha256(wrong),actualWrongReturns=512,
         rejected=rejected,positiveControls=512-rejected))
    try:fixture.execute(image,bodies,2,bound=1)
    except AssertionError:pass
    else:raise AssertionError('Prefix counted as return')
    own={a for a in observed if fixture.ENTRY<=a<fixture.ENTRY+576}
    missing=[hex(a)for a in range(fixture.ENTRY,fixture.ENTRY+576,4)if a not in own and a not in{p&~3 for p in pools}]
    trace=ROOT/'evidence/traces/main-letter576-20261102.json.gz';trace.write_bytes(gzip.compress(json.dumps(dict(cases=cases),sort_keys=True,separators=(',',':')).encode(),mtime=0))
    write_json(REPORT,dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),romSha256=config['romSha256'],
     processor='arm9',program='',module='main',moduleSha256=metadata['sha256'],matches=[rows[0]],matchedFunctions=1,matchedBytes=576,
     existingCompiledBitReader=rows[1],extraHelperCredit=0,
     oracle=dict(pairs=2048,actualTopReturns=4096,actualNativeBitReaderReturns=helpers,functionProviders=0,cpu='ARM946',
      ownInstructionBytesObserved=len(own)*4,generatedPoolBytes=len(pools),unobservedCodeAddresses=missing,
      completeRegistersFlagsMainInputStackOrderedReadsWritesCompared=True,independentPerPixelMsbSourceAndLsbDestinationModel=True),
     negativeControls=controls,replayDependencies=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in[Path(fixture.__file__),trace,HELPER]],
     reproductionCommand='python match_main_letter576_20261102.py',limitations=[
      'Bounded initialized MSB-first glyph bits, palette sum inside target4/8-bit pixels, clipping offsets-7/0/3/7 and explicit empty positive-edge cases',
      'Widths/heights1..16, source1/2/4/8bpp no wider than destination, padded bit stride; malformed bounds and overflowing palette sums unsupported',
      'Correct selected unsigned-int bit-reader signature and unsigned pre-shift mask; local unsigned-long rank remains target32-bit',
      'No helper extra source/data credit, real font/asset/UI/dual-screen render, Windows/Android execution, source-only ROM or full game']))
    print(dict(functions=1,bytes=576,actualReturns=4096,nativeBitReaderReturns=helpers,observedBytes=len(own)*4,poolBytes=len(pools),
     wrongReturns=1024,wrongRejected=sum(c['rejected']for c in controls),missing=missing))


if __name__=='__main__':
    main()
