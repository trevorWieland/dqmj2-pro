import gzip
import json
from pathlib import Path
from project import ROOT,configuration,write_json,sha256
import match_main_oam_reference296_closed_20261101 as builder
import match_main_release704_20261101 as layouts
from main_joint_scale336_fixture_20261102 import execute,ENTRY
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link

WORK=ROOT/'work/main-joint-scale336-qualified-20261102'
SOURCE=ROOT/'src/runtime/20261102_joint_scale336/native_main_0202c84c.c'
REPORT=ROOT/'evidence/matches/main-joint-scale336-20261102.json'


def main():
    builder.WORK=WORK;layouts.WORK=WORK;WORK.mkdir(parents=True,exist_ok=True)
    config=configuration();assert sha256(config['rom'])==config['romSha256']
    meta,image,unused=measured_module('main');assert meta['sha256']=='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
    row,proof,body=builder.build(SOURCE,'correct',True);assert row['bytes']==336
    row.update(exactBytes=336,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceLanguage='C',genuineLinkComparison=freeze_link(proof))
    expressions=['sizeof(NNSG3dRS)','sizeof(NNSG3dRSOnGlb)','sizeof(NNSG3dJntAnmResult)',
     '(u32)&((NNSG3dRS*)0)->isScaleCacheOne','(u32)&((NNSG3dRSOnGlb*)0)->scaleCache',
     '(u32)&((NNSG3dRSOnGlb*)0)->scaleCache[0].inv','sizeof(((NNSG3dRSOnGlb*)0)->scaleCache[0])']
    witness=layouts.witness(SOURCE,row,expressions,[392,11520,88,196,3584,3596,24],'joint-scale-state')
    original=image[ENTRY-0x02000000:ENTRY-0x02000000+336];cases=[];seen=set();pool=set()
    for index in range(2048):
        native=execute(image,original,index);rebuilt=execute(image,body,index)
        assert native==rebuilt and native['modelPassed'],index
        seen.update(native['ownedObserved']);cases.append(native)
        for address,size,value in native['reads']:
            if ENTRY<=address and address+size<=ENTRY+336:pool.update(range(address,address+size))
    missing=sorted(set(range(ENTRY,ENTRY+336,4))-seen-{a&~3 for a in pool});assert not missing,missing
    trace=ROOT/'evidence/traces/main-joint-scale336-20261102.json.gz';trace.parent.mkdir(parents=True,exist_ok=True)
    trace.write_bytes(gzip.compress(json.dumps(dict(cases=cases,actualTopReturns=4096),sort_keys=True,separators=(',',':')).encode(),mtime=0))
    text=SOURCE.read_text(encoding='utf-8');controls=[]
    mutations=[('final-flag','pResult->flag |= NNS_G3D_JNTANM_RESULTFLAG_SCALEEX1_ONE;','pResult->flag |= NNS_G3D_JNTANM_RESULTFLAG_SCALEEX0_ONE;'),
     ('toggle-cache-bit','vec[idx >> 5] |= 1U','vec[idx >> 5] ^= 1U'),
     ('inverse-component','scaleCache[nodeID].inv.y = *(p + 4);','scaleCache[nodeID].inv.z = *(p + 4);')]
    for label,old,new in mutations:
        wrong=text.replace(old,new);assert wrong!=text
        path=WORK/(label+'.c');path.write_text(wrong,encoding='utf-8');bad_row,bad_proof,bad=builder.build(path,label,False)
        rows=[execute(image,bad,index)for index in range(2048)];rejected=sum(not r['modelPassed']for r in rows);assert rejected>0
        controls.append(dict(label=label,actualWrongReturns=2048,rejected=rejected,positiveControls=2048-rejected,
         sourceSha256=sha256(path),objectSha256=bad_row['objectSha256']))
    try:execute(image,original,0,bound=1)
    except AssertionError:pass
    else:raise AssertionError('Instruction prefix accepted as return')
    write_json(REPORT,dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),romSha256=config['romSha256'],
     processor='arm9',program='',module='main',moduleSha256=meta['sha256'],matches=[row],matchedFunctions=1,matchedBytes=336,
     layoutWitness=witness,oracle=dict(cpu='ARM946',pairs=2048,actualTopReturns=4096,providedCalls=0,actualNativeHelperReturns=0,
      instructionBytesObserved=len(seen)*4,generatedPoolBytes=len(pool),allOwnCodeAndPoolObserved=True,
      completeRegisterFlagsMainInputStackReadWriteComparison=True,independentFlagsBitmapsCacheAndSameParentModels=True),
     negativeControls=controls,replayDependencies=[dict(path=trace.relative_to(ROOT).as_posix(),sha256=sha256(trace))],
     reproductionCommand='python match_main_joint_scale336_20261102.py',
     limitations=['Node/parent0..63, aligned disjoint synthetic result/scale/state/cache, no malformed out-of-array or concurrent contexts',
      'Input scale pointer can be null only when the selected release code never dereferences it; no API/debug-assert policy inferred',
      'Original global storage receives no data credit; source-only modules, full Windows game and Android execution remain unproved']))
    print(dict(functions=1,bytes=336,pairs=2048,actualTopReturns=4096,wrongActualReturns=6144,
     wrongRejected=sum(c['rejected']for c in controls),instructionBytes=len(seen)*4,poolBytes=len(pool)))


if __name__=='__main__':
    main()
