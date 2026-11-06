import gzip
import json
from pathlib import Path
import match_runtime
from project import ROOT,configuration,write_json,sha256
import match_main_oam_reference296_closed_20261101 as builder
import match_main_release704_20261101 as layouts
from main_animation_obj352_fixture_20261101 import execute,SPECS
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link

WORK=ROOT/'work/main-animation-obj352-qualified-20261101'
REPORT=ROOT/'evidence/matches/main-animation-obj352-20261101.json'
COUNTS={0x0202BF2C:1152,0x0202BFE0:1536,0x0202C054:1152,0x020364DC:1089}


def main():
    WORK.mkdir(parents=True,exist_ok=True);builder.WORK=WORK;layouts.WORK=WORK
    config=configuration();assert sha256(config['rom'])==config['romSha256']
    metadata,image,unused=measured_module('main');assert sha256(ROOT/metadata['binary'])=='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
    matches=[];summaries=[];traces=[];controls=[];witnesses=[];bodies={}
    for entry,size in SPECS.items():
        source=ROOT/f'src/runtime/20261101_animation_obj352/native_main_{entry:08x}.c'
        row,proof,body=builder.build(source,f'correct-{entry:08x}',True);assert row['bytes']==size;bodies[entry]=body
        row.update(exactBytes=size,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceLanguage='C',genuineLinkComparison=freeze_link(proof));matches.append(row)
        if entry==0x0202BF2C:
            expressions=['sizeof(u32)','sizeof(NNSG3dResFileHeader)','sizeof(NNSG3dResDataBlockHeader)','sizeof(NNSG3dResDict)',
             '(u32)&((NNSG3dResFileHeader*)0)->headerSize','(u32)&((NNSG3dResAnmSet*)0)->dict',
             '(u32)&((NNSG3dResDict*)0)->numEntry','(u32)&((NNSG3dResDict*)0)->ofsEntry','(u32)&((NNSG3dResDictEntryHeader*)0)->data']
            witnesses.append(layouts.witness(source,row,expressions,[4,16,8,12,12,8,1,6,4],'animation-set'))
        if entry==0x0202BFE0:
            expressions=['sizeof(u32)','sizeof(s32)','sizeof(NNSG3dResTexPatAnm)','sizeof(NNSG3dResDictTexPatAnmData)',
             'sizeof(NNSG3dResTexPatAnmFV)','(u32)&((NNSG3dResTexPatAnm*)0)->dict',
             '(u32)&((NNSG3dResDictTexPatAnmData*)0)->ratioDataFrame','(u32)&((NNSG3dResDictTexPatAnmData*)0)->offset']
            witnesses.append(layouts.witness(source,row,expressions,[4,4,24,8,4,12,4,6],'texture-animation'))
    for row in matches:
        entry=int(row['address'],0);size=SPECS[entry];source=ROOT/row['source'];cases=[];own=set();helpers=0
        for index in range(COUNTS[entry]):
            native=execute(image,entry,{},index);rebuilt=execute(image,entry,bodies,index)
            assert native==rebuilt and native['modelPassed'],(hex(entry),index,native)
            own.update(native['ownedObserved']);helpers+=native['actualNativeHelperReturns']*2;cases.append(native)
        missing=sorted(set(range(entry,entry+size,4))-own);assert not missing,(hex(entry),missing)
        trace=ROOT/f'evidence/traces/main-animation-obj352-{entry:08x}-20261101.json.gz';trace.parent.mkdir(parents=True,exist_ok=True)
        trace.write_bytes(gzip.compress(json.dumps(dict(cases=cases,actualTopReturns=COUNTS[entry]*2),sort_keys=True,separators=(',',':')).encode(),mtime=0))
        traces.append(dict(path=trace.relative_to(ROOT).as_posix(),sha256=sha256(trace)))
        summaries.append(dict(address=f'0x{entry:08X}',pairs=COUNTS[entry],actualTopReturns=COUNTS[entry]*2,
         actualNativeHelperReturnsSeparate=helpers,instructionBytesObserved=size))
        text=source.read_text(encoding='utf-8')
        replacements={0x0202BF2C:('anmSetData->offset','anmSetData->offset + 4'),0x0202BFE0:('<= frame','< frame'),
         0x0202C054:('idx < dict->numEntry','idx <= dict->numEntry'),0x020364DC:('w / 8','w / 4')}
        old,new=replacements[entry];wrong=text.replace(old,new);assert wrong!=text
        bad=WORK/f'wrong-{entry:08x}.c';bad.write_text(wrong,encoding='utf-8')
        bad_row,bad_proof,bad_body=builder.build(bad,f'wrong-{entry:08x}',False)
        variant=dict(bodies);variant[entry]=bad_body;results=[execute(image,entry,variant,index)for index in range(COUNTS[entry])]
        rejected=sum(not item['modelPassed']for item in results);assert rejected>0
        controls.append(dict(address=f'0x{entry:08X}',actualWrongCReturns=COUNTS[entry],rejected=rejected,
         positiveControls=COUNTS[entry]-rejected,sourceSha256=sha256(bad),objectSha256=bad_row['objectSha256']))
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),romSha256=config['romSha256'],
     processor='arm9',program='',module='main',moduleSha256=metadata['sha256'],matches=matches,matchedFunctions=4,matchedBytes=352,
     oracle=dict(pairs=sum(COUNTS.values()),actualTopReturns=sum(COUNTS.values())*2,
      actualNativeHelperReturnsSeparate=sum(s['actualNativeHelperReturnsSeparate']for s in summaries),providedCalls=0,
      allOwnInstructionBytesObserved=352,independentModels=['offset-table pointer result','linear rightmost frame selection','minimum rectangle partition over 12 legal sprite shapes'],
      fullRegistersFlagsMainDataStackReadsWritesCallsCompared=True),summaries=summaries,layoutWitnesses=witnesses,
     negativeControls=controls,replayDependencies=traces,reproductionCommand='python match_main_animation_obj352_20261101.py',
     sourceOrigin=dict(referenceRevision='d636fb5d2b212e8736f09859fff447be2bd0ac85',historicalSdkRevisionProven=False,
      scalarWidth=32,animationResourceRawWordFacadePreservesThreeSelectedConsumers=True),
     limitations=['Synthetic bounded offset tables and sorted texture keyframes; no malformed pointer, invalid texture index, complete binary-format validity or game scene claim',
      'Texture prediction stays inside its table; sprite dimensions 0..32 tiles and minimum guillotine partition model only',
      'No full Windows game, source-only ROM or Android device proof'])
    write_json(REPORT,report);print(dict(functions=4,bytes=352,pairs=report['oracle']['pairs'],actualTopReturns=report['oracle']['actualTopReturns'],providers=0))


if __name__=='__main__':
    main()
