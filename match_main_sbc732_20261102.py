import gzip
import json
from pathlib import Path
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link
import match_main_oam_reference296_closed_20261101 as builder
import main_sbc732_fixture_20261102 as fixture

WORK=ROOT/'work/main-sbc732-qualified-20261102'
FOLDER=ROOT/'src/runtime/20261102_sbc732'
REPORT=ROOT/'evidence/matches/main-sbc732-20261102.json'


def main():
    config=configuration();assert sha256(config['rom'])==config['romSha256']
    meta,image,_=measured_module('main');assert meta['sha256']=='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
    builder.WORK=WORK;rows=[];bodies={};sources={}
    for path in sorted(FOLDER.glob('*.c')):
        row,proof,body=builder.build(path,path.stem,True);address=int(row['address'],0);assert len(body)==fixture.SPANS[address]
        row.update(exactBytes=len(body),sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceLanguage='C',genuineLinkComparison=freeze_link(proof))
        rows.append(row);bodies[address]=body;sources[address]=path
    assert set(bodies)==set(fixture.SPANS)and sum(map(len,bodies.values()))==732
    cases=[];observed=set();pool=set();provided=geometry=0
    for index in range(3072):
        original=fixture.execute(image,{},index);candidate=fixture.execute(image,bodies,index)
        assert original==candidate and original['modelPassed'],index
        observed.update(original['ownedObserved']);provided+=len(original['providedCalls'])*2;geometry+=len(original['geometry'])*2;cases.append(original)
        for address,size,value in original['reads']:
            if any(base<=address and address+size<=base+length for base,length in fixture.SPANS.items()):pool.update(range(address,address+size))
    controls=[]
    for label,address,old,new in[
     ('nop-step',0x0202FB48,'rs->c++;','rs->c += 2;'),
     ('return-toggle',0x0202FB70,'rs->flag |= NNS_G3D_RSFLAG_RETURN','rs->flag ^= NNS_G3D_RSFLAG_RETURN'),
     ('matrix-command',0x0202FD14,'native_fn_0202e434(0x14','native_fn_0202e434(0x15'),
     ('material-cache',0x02030268,'idxMat == rs->currentMat','idxMat != rs->currentMat'),
     ('shape-transparent',0x020303EC,'!(rs->flag & NNS_G3D_RSFLAG_MAT_TRANSPARENT)','(rs->flag & NNS_G3D_RSFLAG_MAT_TRANSPARENT)'),
     ('scale-selection',0x02031790,'if (opt == 0x00 )','if (opt != 0x00 )')]:
        text=sources[address].read_text(encoding='utf-8');changed=text.replace(old,new);assert changed!=text,label
        path=ROOT/f'nonmatching/integration/20261102-sbc732/{label}/source.c';path.parent.mkdir(parents=True,exist_ok=True)
        if path.exists():assert path.read_text(encoding='utf-8')==changed
        else:path.write_text(changed,encoding='utf-8')
        row,proof,body=builder.build(path,label,False);assert len(body)<=fixture.SPANS[address]
        bad={**bodies,address:body};indices=[i for i in range(3072)if list(fixture.SPANS)[i%6]==address]
        results=[fixture.execute(image,bad,index)for index in indices];rejected=sum(not row['modelPassed']for row in results);assert rejected
        controls.append(dict(label=label,source=path.relative_to(ROOT).as_posix(),sourceSha256=sha256(path),actualWrongReturns=len(results),rejected=rejected,positiveControls=len(results)-rejected))
    try:fixture.execute(image,bodies,0,bound=1)
    except AssertionError:pass
    else:raise AssertionError('Prefix accepted as return')
    trace=ROOT/'evidence/traces/main-sbc732-20261102.json.gz'
    trace.write_bytes(gzip.compress(json.dumps(dict(cases=cases),sort_keys=True,separators=(',',':')).encode(),mtime=0))
    missing={hex(base):[hex(a)for a in range(base,base+length,4)if a not in observed and a not in{p&~3 for p in pool}]for base,length in fixture.SPANS.items()}
    write_json(REPORT,dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),romSha256=config['romSha256'],
     processor='arm9',program='',module='main',moduleSha256=meta['sha256'],matches=rows,matchedFunctions=6,matchedBytes=732,
     oracle=dict(pairs=3072,actualTopReturns=6144,cpu='ARM946',providedCallbackCallsSeparate=provided,
      originalGeometryEntryCallsSeparate=geometry,ownInstructionBytesObserved=len(observed)*4,generatedPoolBytes=len(pool),unobservedCodeAddresses=missing,
      completeRegistersFlagsMainInputStackOrderedReadsWritesCompared=True,independentCallbackTimingGatesCursorAndCommands=True),
     negativeControls=controls,replayDependencies=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in[Path(fixture.__file__),trace]],
     reproductionCommand='python match_main_sbc732_20261102.py',limitations=[
      'Callbacks and four-way material/shape dispatch functions are explicitly supplied mutation/argument models, not reconstructed ordinary rendering logic',
      'Original geometry-buffer code writes an isolated FIFO shadow; no physical GPU, rendered geometry, DMA, timing or scene proof',
      'Bounded392-byte render state, valid three-entry dictionaries and indexed records; malformed pointer/index paths remain unsupported',
      'No callback, command table, geometry helper or data source credit; source-only ROM and full native game remain incomplete']))
    print(dict(functions=6,bytes=732,actualTopReturns=6144,providedCallbacks=provided,nativeGeometryCalls=geometry,
     observedBytes=len(observed)*4,poolBytes=len(pool),wrongReturns=3072,wrongRejected=sum(r['rejected']for r in controls),missing=missing))


if __name__=='__main__':
    main()
