import gzip
import json
from pathlib import Path
from project import ROOT,configuration,write_json,sha256
import match_main_oam_reference296_closed_20261101 as builder
import match_main_release704_20261101 as layouts
from main_draw676_fixture_20261102 import execute,ENTRY,CALLBACKS
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link

WORK=ROOT/'work/main-draw676-qualified-20261102'
SOURCE=ROOT/'src/runtime/20261102_draw676/native_main_0202dafc.c'
REPORT=ROOT/'evidence/matches/main-draw676-20261102.json'


def main():
    WORK.mkdir(parents=True,exist_ok=True);builder.WORK=WORK;layouts.WORK=WORK
    config=configuration();assert sha256(config['rom'])==config['romSha256']
    meta,image,unused=measured_module('main');assert meta['sha256']=='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
    row,proof,body=builder.build(SOURCE,'correct',True);assert row['bytes']==676
    row.update(exactBytes=676,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceLanguage='C',genuineLinkComparison=freeze_link(proof))
    expressions=['sizeof(NNSG3dResMatData)','sizeof(NNSG3dResShpData)','sizeof(NNSG3dMatAnmResult)',
     '(u32)&((NNSG3dResMdl*)0)->info.posScale','(u32)&((NNSG3dResMdl*)0)->info.invPosScale',
     '(u32)&((NNSG3dResMatData*)0)->flag','(u32)&((NNSG3dMatAnmResult*)0)->origWidth']
    witness=layouts.witness(SOURCE,row,expressions,[44,16,56,28,32,30,44],'drawing-resource-layout')
    original=image[ENTRY-0x02000000:ENTRY-0x02000000+676];cases=[];observed=set();pool=set();callback_entries=set();completions=0;divisions=0
    for index in range(2048):
        native=execute(image,original,index);candidate=execute(image,body,index)
        assert native==candidate and native['modelPassed'],(index,native['context'])
        observed.update(native['ownedObserved']);completions+=native['nativeEntryCompletions']*2
        divisions+=len(native['modeledPositiveDivisionOperations'])*2
        callback_entries.update(f['entry']for f in native['textureFields']);cases.append(native)
        for address,size,value in native['reads']:
            if ENTRY<=address and address+size<=ENTRY+676:pool.update(range(address,address+size))
    assert callback_entries==set(CALLBACKS)
    missing=sorted(set(range(ENTRY,ENTRY+676,4))-observed-{a&~3 for a in pool})
    trace=ROOT/'evidence/traces/main-draw676-20261102.json.gz';trace.parent.mkdir(parents=True,exist_ok=True)
    trace.write_bytes(gzip.compress(json.dumps(dict(cases=cases,actualTopReturns=4096),sort_keys=True,separators=(',',':')).encode(),mtime=0))
    controls=[];text=SOURCE.read_text(encoding='utf-8')
    for label,old,new in [('wireframe','cmd[3] &= ~0x001f0000','cmd[3] |= 0x001f0000'),
     ('scale-command','native_fn_0202e434(0x1b','native_fn_0202e434(0x1c'),
     ('texture-width','dummy.origWidth = mat->origWidth;','dummy.origWidth = mat->origHeight;')]:
        wrong=text.replace(old,new);assert wrong!=text
        path=WORK/(label+'.c');path.write_text(wrong,encoding='utf-8');bad_row,bad_proof,bad=builder.build(path,label,False)
        rows=[execute(image,bad,index)for index in range(2048)];rejected=sum(not r['modelPassed']for r in rows);assert rejected>0
        controls.append(dict(label=label,actualWrongReturns=2048,rejected=rejected,positiveControls=2048-rejected,
         sourceSha256=sha256(path),objectSha256=bad_row['objectSha256']))
    try:execute(image,original,0,bound=1)
    except AssertionError:pass
    else:raise AssertionError('Instruction prefix accepted as return')
    write_json(REPORT,dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),romSha256=config['romSha256'],
     processor='arm9',program='',module='main',moduleSha256=meta['sha256'],matches=[row],matchedFunctions=1,matchedBytes=676,
     layoutWitness=witness,oracle=dict(pairs=2048,actualTopReturns=4096,functionProviders=0,cpu='ARM946',
      nativeLogicalEntryCompletionsSeparate=completions,physicalHelperReturnsNotInferredFromTails=True,
      modeledPositiveDivisionOperations=divisions,originalTextureCallbacksObserved=sorted(callback_entries),
      instructionBytesObserved=len(observed)*4,generatedPoolBytes=len(pool),missingCodeAddresses=[hex(a)for a in missing],
      independentOwnCommandsAndInitializedCallbackFields=True,completeRegistersFlagsMainInputStackFifoReadWriteComparison=True),
     negativeControls=controls,replayDependencies=[dict(path=trace.relative_to(ROOT).as_posix(),sha256=sha256(trace))],
     reproductionCommand='python match_main_draw676_20261102.py',limitations=[
      'Positive numerator/nonzero-positive-denominator divider modes0/1/2 are modeled as immediate mathematical results; no negative/zero divisor, busy timing, IRQ or actual device claim',
      'All four texture callbacks, CPU transfer and their calc functions execute original code; only their supplied initialized input fields and top-owned command routing have independent models',
      'Texture matrix outputs are differential native/source observations, not an independent derivation of all callback mathematics',
      'Synthetic three-entry material/shape dictionaries and bounded aligned display lists; no complete asset validation, malformed pointer, DMA path or rendered scene proof',
      'No callback/helper/data source credit, source-only ROM, full native Windows game or Android execution proof']))
    print(dict(functions=1,bytes=676,pairs=2048,actualTopReturns=4096,logicalHelperCompletions=completions,
     hardwareDivisionOperations=divisions,observedBytes=len(observed)*4,poolBytes=len(pool),missing=missing,
     wrongActualReturns=6144,wrongRejected=sum(c['rejected']for c in controls)))


if __name__=='__main__':
    main()
