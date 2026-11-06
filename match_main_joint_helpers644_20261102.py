import gzip
import json
from pathlib import Path
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link
import match_main_oam_reference296_closed_20261101 as builder
import main_joint_helpers644_fixture_20261102 as fixture

WORK=ROOT/'work/main-joint-helpers644-qualified-20261102'
REPORT=ROOT/'evidence/matches/main-joint-helpers644-20261102.json'
SOURCES=[ROOT/'src/math/20261102_vector_normalize280/native_main_02002618.c',
 ROOT/'src/runtime/20261102_joint_decode364_v3/native_main_020337c4.c']


def main():
    config=configuration();assert sha256(config['rom'])==config['romSha256']
    metadata,image,_=measured_module('main');assert metadata['sha256']=='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
    expected_table=bytes(v for i in range(9)for v in[r*3+c for r in range(3)for c in range(3)if r!=i//3 and c!=i%3])
    assert image[0xD90AC:0xD90AC+36]==expected_table
    builder.WORK=WORK;bodies={};rows=[];sources={}
    for path in SOURCES:
        row,proof,body=builder.build(path,path.stem,True);address=int(row['address'],0);assert len(body)==fixture.SPANS[address]
        row.update(exactBytes=len(body),sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceLanguage='C',genuineLinkComparison=freeze_link(proof))
        rows.append(row);bodies[address]=body;sources[address]=path
    cases=[];observed=set();pools=set();operations=0
    for index in range(9216):
        original=fixture.execute(image,{},index);candidate=fixture.execute(image,bodies,index)
        assert original==candidate and original['modelPassed'],(index,original['context'])
        cases.append(original);observed.update(original['ownObserved']);operations+=len(original['hardwareOperations'])*2
        for address,size,value in original['reads']:
            if any(base<=address and address+size<=base+length for base,length in fixture.SPANS.items()):pools.update(range(address,address+size))
    controls=[]
    for address,old,new in[(0x02002618,'1LL << (12 + 12 + 32 )','1LL << (12 + 12 + 31 )'),
     (0x020337C4,'NNS_G3D_JNTANM_PIVOTINFO_SIGN_REVC       = 0x0020','NNS_G3D_JNTANM_PIVOTINFO_SIGN_REVC       = 0x0040')]:
        path=sources[address];text=path.read_text(encoding='utf-8');changed=text.replace(old,new);assert changed!=text
        label=f'helper-{address:08x}';wrong=ROOT/f'nonmatching/integration/20261102-joint-helpers644/{label}/source.c';wrong.parent.mkdir(parents=True,exist_ok=True)
        if wrong.exists():assert wrong.read_text(encoding='utf-8')==changed
        else:wrong.write_text(changed,encoding='utf-8')
        row,proof,body=builder.build(wrong,label,False);assert len(body)<=fixture.SPANS[address]
        bad={**bodies,address:body};kind=0 if address==0x02002618 else 1
        results=[fixture.execute(image,bad,i)for i in range(kind,9216,2)];rejected=sum(not row['modelPassed']for row in results);assert rejected
        controls.append(dict(label=label,source=wrong.relative_to(ROOT).as_posix(),sourceSha256=sha256(wrong),
         actualWrongReturns=len(results),rejected=rejected,positiveControls=len(results)-rejected))
    try:fixture.execute(image,bodies,0,bound=1)
    except AssertionError:pass
    else:raise AssertionError('Prefix counted as return')
    missing={hex(base):[hex(a)for a in range(base,base+n,4)if a not in observed and a not in{p&~3 for p in pools}]for base,n in fixture.SPANS.items()}
    trace=ROOT/'evidence/traces/main-joint-helpers644-20261102.json.gz'
    trace.write_bytes(gzip.compress(json.dumps(dict(cases=cases),sort_keys=True,separators=(',',':')).encode(),mtime=0))
    write_json(REPORT,dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),romSha256=config['romSha256'],
     processor='arm9',program='',module='main',moduleSha256=metadata['sha256'],matches=rows,matchedFunctions=2,matchedBytes=644,
     oracle=dict(pairs=9216,actualTopReturns=18432,functionProviders=0,cpu='ARM946',ownInstructionBytesObserved=len(observed)*4,
      generatedPoolBytes=len(pools),unobservedCodeAddresses=missing,actualModeledHardwareOperations=operations,
      completeRegistersFlagsMainInputStackOrderedReadsWritesCompared=True,independentGeometryAndIntegerRootModels=True),
     originalPivotTable=dict(address='0x020d90ac',bytes=36,sha256=sha256_bytes(expected_table),extraDataCredit=0),
     negativeControls=controls,replayDependencies=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in[Path(fixture.__file__),trace]],
     reproductionCommand='python match_main_joint_helpers644_20261102.py',limitations=[
      'Nonzero bounded vectors, identical/disjoint output and valid nine pivot indices with eight sign combinations or packed rotation codes',
      'Division64/64 and square-root64 hardware complete immediately; no timing/busy/interrupt/coherency or zero-vector error claim',
      'Original36-byte pivot table independently agrees with row/column geometry but receives no extra data source credit',
      'Target32-bit unsigned-long and pointers; Windows/Android source portability or full animation scene not proved',
      'No source-only ROM, complete native Windows game or Android device execution']))
    print(dict(functions=2,bytes=644,actualReturns=18432,hardwareOperations=operations,observedBytes=len(observed)*4,
     poolBytes=len(pools),wrongReturns=9216,wrongRejected=sum(c['rejected']for c in controls),missing=missing))


def sha256_bytes(data):
    import hashlib
    return hashlib.sha256(data).hexdigest()


if __name__=='__main__':
    main()
