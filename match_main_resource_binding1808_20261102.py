import gzip
import json
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link
import match_main_oam_reference296_closed_20261101 as builder
import main_resource_binding_fixture_v3_20261102 as binding
import main_resource_setup_fixture_v2_20261102 as setup

WORK=ROOT/'work/main-resource-binding1808-qualified-20261102'
REPORT=ROOT/'evidence/matches/main-resource-binding1808-20261102.json'
SOURCES=[ROOT/f'src/runtime/20261102_resource_binding_v5/native_main_{a}.c'for a in['0202edfc','0202efe4','0202f250','0202bedc']]
SOURCES += [ROOT/f'src/runtime/20261102_resource_binding_v3/native_main_{a}.c'for a in['0202f170','0202f3dc']]
SOURCES += [ROOT/'src/runtime/20261102_resource_binding_v4/native_main_02031fa4.c']



def main():
    config=configuration();assert sha256(config['rom'])==config['romSha256']
    meta,image,_=measured_module('main');assert meta['sha256']=='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
    builder.WORK=WORK;rows=[];bodies={};sources={}
    for source in SOURCES:
        row,proof,body=builder.build(source,source.stem,True);address=int(row['address'],0)
        assert len(body)==binding.SPANS[address]
        row.update(exactBytes=len(body),sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceLanguage='C',genuineLinkComparison=freeze_link(proof))
        rows.append(row);bodies[address]=body;sources[address]=source
    assert set(bodies)==set(binding.SPANS)and sum(len(b)for b in bodies.values())==1808
    cases=[];observed=set();pools=set();providers=divisions=0
    for tag,fixture,count in [('binding',binding,2048),('setup',setup,2304)]:
        for index in range(count):
            original=fixture.execute(image,{},index);candidate=fixture.execute(image,bodies,index)
            assert original==candidate and original['modelPassed'],(tag,index)
            observed.update(original['ownedObserved']);providers+=len(original['providedCalls'])*2;divisions+=len(original['divisionOperations'])*2
            for address,size,value in original['reads']:
                if any(base<=address and address+size<=base+length for base,length in binding.SPANS.items()):pools.update(range(address,address+size))
            cases.append(dict(kind=tag,case=original))
    controls=[]
    for label,address,old,new,fixture in[
     ('texture-xor',0x0202EDFC,'matData->texImageParam |=','matData->texImageParam ^=',binding),
     ('palette-xor',0x0202F170,'plttBase + vramOffset','plttBase ^ vramOffset',binding),
     ('missing-texture',0x0202EFE4,'result = 0 ;','result = 1 ;',binding),
     ('allocation-format',0x02031FA4,'NNS_G3D_RESPLTT_USEPLTT4 = 0x8000','NNS_G3D_RESPLTT_USEPLTT4 = 0x4000',setup),
     ('success-return',0x02031FA4,'return 1 ;','return 0 ;',setup)]:
        text=sources[address].read_text(encoding='utf-8');changed=text.replace(old,new);assert changed!=text,(label,old)
        path=ROOT/f'nonmatching/integration/20261102-resource-binding1808/{label}/source.c';path.parent.mkdir(parents=True,exist_ok=True)
        if path.exists():assert path.read_text(encoding='utf-8')==changed
        else:path.write_text(changed,encoding='utf-8')
        row,proof,body=builder.build(path,label,False);assert len(body)<=binding.SPANS[address]
        mutated={**bodies,address:body};count=1000 if fixture is binding else 1536
        bad=[fixture.execute(image,mutated,index)for index in range(count)];rejected=sum(not row['modelPassed']for row in bad);assert rejected>0
        controls.append(dict(label=label,source=path.relative_to(ROOT).as_posix(),sourceSha256=sha256(path),actualWrongReturns=count,
         independentModelRejections=rejected,positiveControls=count-rejected,compiledBytes=len(body)))
    try:binding.execute(image,bodies,0,bound=1)
    except AssertionError:pass
    else:raise AssertionError('Bounded prefix counted as return')
    missing={hex(base):[hex(a)for a in range(base,base+length,4)if a not in observed and a not in{p&~3 for p in pools}]
     for base,length in binding.SPANS.items()}
    trace=ROOT/'evidence/traces/main-resource-binding1808-20261102.json.gz'
    trace.write_bytes(gzip.compress(json.dumps(dict(cases=cases),sort_keys=True,separators=(',',':')).encode(),mtime=0))
    write_json(REPORT,dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),romSha256=config['romSha256'],
     processor='arm9',program='',module='main',moduleSha256=meta['sha256'],matches=rows,matchedFunctions=7,matchedBytes=1808,
     oracle=dict(pairs=4352,actualTopReturns=8704,bindingFunctionProviders=0,setupProvidedBackendCallsSeparate=providers,
      modeledPositiveDivisionOperations=divisions,ownInstructionBytesObserved=len(observed)*4,generatedPoolBytes=len(pools),
      unobservedCodeAddresses=missing,allSevenCompiledBodiesInstalledTogether=True,
      completeRegistersFlagsMainInputStackReadWriteHardwareCompared=True,independentTransactionAndMaterialModels=True),
     negativeControls=controls,replayDependencies=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in[
      ROOT/'main_resource_binding_fixture_v3_20261102.py',ROOT/'main_resource_binding_fixture_20261102.py',
      ROOT/'main_resource_setup_fixture_v2_20261102.py',ROOT/'main_resource_setup_fixture_20261102.py',ROOT/'draw676_positive_divider_20261102.py',trace]],
     reproductionCommand='python match_main_resource_binding1808_20261102.py',limitations=[
      'Allocation/free callback services and texture/palette upload services are explicitly supplied with ABI clobbers and no game-RAM effects',
      'Binding executes original dictionary lookup and fixed division; positive arithmetic hardware is modeled without timing or unsupported signed/error modes',
      'Synthetic dictionaries under16 entries, up to3 models/materials/bindings, nonzero original dimensions and valid indexed records',
      'Material/texture mapping and allocation rollback are bounded component behaviors; no full resource validity, asset rendering or physical VRAM proof',
      'No additional callee/data source credit, source-only ROM, Windows execution of this group, full native game or Android device claim']))
    print(dict(functions=7,bytes=1808,actualTopReturns=8704,providedCalls=providers,divisionOperations=divisions,
     observedBytes=len(observed)*4,poolBytes=len(pools),wrongReturns=sum(r['actualWrongReturns']for r in controls),
     wrongRejected=sum(r['independentModelRejections']for r in controls),missing=missing))


if __name__=='__main__':
    main()
