import gzip
import json
from pathlib import Path
import match_runtime
import main_cell_oam868_fixture_v3_20261101 as fixture
import match_main_oam_reference296_closed_20261101 as builder
from project import ROOT,configuration,read_json,write_json,sha256
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link

SOURCE=ROOT/'src/runtime/20261101_cell_oam868_named/native_main_0203519c.c'


def main():
    config=configuration();assert sha256(config['rom'])==config['romSha256']
    builder.WORK=ROOT/'work/main-cell-oam868-v2-20261101'
    row,proof,body=builder.build(SOURCE,'correct',True)
    metadata,image,_=measured_module('main');native=image[0x3519C:0x3519C+868];assert body==native
    snapshot=read_json(ROOT/'evidence/verification/accepted-cohort123-identities-v2-20261101.json')['functions']
    for path in {r['source']for r in snapshot if r['source'].endswith('.c')}:
        assert 'native_fn_0203519c'not in(ROOT/path).read_text(encoding='utf-8'),path
    cases=[];own=set();pool=set()
    for index in range(686):
        original=fixture.execute(image,native,index);rebuilt=fixture.execute(image,body,index)
        assert original==rebuilt and original['modelPassed'],index
        own.update(original['ownedObserved'])
        for address,size,value in original['reads']:
            if fixture.ENTRY<=address and address+size<=fixture.ENTRY+868:pool.update(range(address,address+size))
        cases.append(dict(original=original,rebuilt=rebuilt))
    instructions={byte for word in own for byte in range(word,word+4)}
    unvisited=set(range(fixture.ENTRY,fixture.ENTRY+868))-(instructions|pool)
    assert unvisited==set(range(0x02035390,0x0203539C))
    assert not instructions&pool and len(instructions)==832 and len(pool)==24
    text=SOURCE.read_text(encoding='utf-8')
    controls=[]
    for label,before,after in [('attribute-copy','pDst->attr2 = pSrc->attr2','pDst->attr2 = pSrc->attr1'),
        ('x-rounding','objTrans.x + 0x800','objTrans.x + 0x000')]:
        assert text.count(before)==1
        source=ROOT/f'nonmatching/integration/20261101-cell-oam868/{label}/source.c'
        source.parent.mkdir(parents=True,exist_ok=True);changed=text.replace(before,after)
        if source.exists():assert source.read_text(encoding='utf-8')==changed
        else:source.write_text(changed,encoding='utf-8')
        bad_row,bad_proof,bad_body=builder.build(source,'wrong-'+label,False)
        records=[fixture.execute(image,bad_body,index)for index in range(343)]
        rejected=sum(not record['modelPassed']for record in records)
        assert rejected and rejected<343 and all(record['actualReturn']for record in records)
        controls.append(dict(label=label,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),
            compilation=bad_row,genuineLinkComparison=bad_proof,actualWrongReturns=343,
            independentModelRejections=rejected,positiveControls=343-rejected,cases=records))
    try:fixture.execute(image,native,0,bound=1)
    except AssertionError:pass
    else:raise AssertionError('Instruction prefix received return credit')
    trace=ROOT/'evidence/traces/main-cell-oam868-v2-20261101.json.gz';trace.parent.mkdir(parents=True,exist_ok=True)
    trace.write_bytes(gzip.compress(json.dumps(dict(cases=cases,controls=controls),sort_keys=True,separators=(',',':')).encode(),mtime=0))
    row.update(genuineLinkComparison=freeze_link(proof),exactBytes=868,sourceOnlyCompilerInput=True,
        originalObjectScaffolding=False,sourceLanguage='C')
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),
        romSha256=config['romSha256'],processor='arm9',program='',module='main',moduleSha256=metadata['sha256'],
        matches=[row],matchedFunctions=1,matchedBytes=868,oracle=dict(pairs=686,actualTopReturns=1372,
            actualHelperReturns=0,providedCalls=0,instructionBytesObserved=len(instructions),poolBytesObserved=len(pool),allOwnInstructionsExecuted=False,
            unvisitedSourceReconstructedGuardRange=['0x02035390','0x0203539c'],
            guard='G2_SetOBJEffect non-affine arm is excluded because this caller supplies only100/300 affine effects',
            fullRegistersFlagsImmutableMainDataStackArgsReadAndWriteOrderCompared=True,
            incomingArgumentWrite='Only exact idempotent4-byte store to initialSP+8 allowed; incoming words remain byte-identical',
            originalNativeFrameBytes=72,copiedCount='min(source count, destination halfword capacity)',
            matrixProfiles=fixture.MATRICES,translationProfiles=fixture.TRANSLATIONS),
        negativeEvidence=dict(actualWrongReturns=686,independentModelRejections=sum(r['independentModelRejections']for r in controls),
            controls=[{k:v for k,v in r.items()if k!='cases'}for r in controls],boundedPrefixReturnCredit=0),
        replayDependencies=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in [Path(fixture.__file__),Path(builder.__file__),trace,
            ROOT/'evidence/verification/accepted-cohort123-identities-v2-20261101.json']],
        sourceOrigin=dict(referenceAssisted=True,headerOrLibcPlaceholderInputs=False,ordinaryStructuredC=True,
            selectedIncomingCCallers=0,originalApiTypesProven=False,explicitOriginalReadOnlyTableBindings=True,
            recoveredOriginalTableDataCredit=0),
        reproductionCommand='python match_main_cell_oam868_v2_20261101.py',
        limitations=['All868 linked bytes are exact; valid immutable cases execute832 instruction bytes and24 literals; the12-byte non-affine helper arm is reconstructed but unreachable for this caller',
            'Disjoint source/cell/matrix/translation/destination buffers, source counts0..16 and valid halfword capacities',
            'Sprite shape0..2,size0..3,affine index0..31,bounded fixed-point matrices/translations and full-word Boolean flags',
            'Seven declared arguments/four registers/three stack words; actual incoming Boolean-word rewrite is idempotent',
            'Original width/height tables are measured data, not reconstructed executable or data credit',
            'No malformed pointers,aliasing,shape3,invalid affine indices,overflowing fixed-point arithmetic or renderer/device claim',
            'Source spans genuinely match but complete module/regression/source-package acceptance remains pending'])
    write_json(ROOT/'evidence/matches/main-cell-oam868-v2-20261101.json',report)
    print(dict(functions=1,bytes=868,actualTopReturns=1372,providers=0,ownInstructions=len(instructions),pool=len(pool),
        wrongReturns=686,wrongRejections=report['negativeEvidence']['independentModelRejections']))


if __name__=='__main__':
    main()
