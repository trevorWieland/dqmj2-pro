import gzip
import json
from pathlib import Path
import match_runtime as compiler
import main_oam_apply_connected_fixture_v2_20261101 as fixture
import match_main_oam_reference296_closed_20261101 as sdk_builder
from project import ROOT, configuration, read_json, write_json, sha256
from link_runtime_unit import measured_module,validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link

WORK=ROOT/'work/main-oam-apply-connected516-20261101'


def caller_build(source,label):
    compiler.WORK=WORK/label/'compile'
    rows,_=compiler.compare(source,'main',2,'off');assert len(rows)==1
    row=rows[0];directory=WORK/label/'link'
    proof=validate(row,qualified_bindings(row),directory)
    return row,proof,(directory/'caller.bin').read_bytes()


def main():
    config=configuration();assert sha256(config['rom'])==config['romSha256']
    sdk_builder.WORK=WORK
    source=ROOT/'src/runtime/20261101_oam_apply_abi/native_main_02036f68.c'
    caller=ROOT/'src/runtime/20261101_oam_apply_abi/native_main_020489c4.c'
    original_caller=ROOT/'src/runtime/runtime05/native_main_020489c4.c'
    assert 'extern void native_fn_02036f68(s32);'in caller.read_text(encoding='utf-8')
    assert 'void native_main_02036f68(signed int raw)'in source.read_text(encoding='utf-8')
    apply_row,apply_proof,apply_body=sdk_builder.build(source,'apply',True)
    caller_row,caller_proof,caller_body=caller_build(caller,'caller')
    reset_row,reset_proof,reset_body=sdk_builder.build(sdk_builder.SOURCE,'reset-dependency',True)
    metadata,image,_=measured_module('main')
    bodies={fixture.APPLY:apply_body,fixture.RESET:reset_body,fixture.CALLER:caller_body}
    native={base:image[base-0x02000000:base-0x02000000+len(body)]for base,body in bodies.items()}
    assert bodies==native
    traces=[];own=set();reads=set();nested=0
    for connected in [False,True]:
        for index in range(96):
            original=fixture.execute(image,native,index,connected)
            rebuilt=fixture.execute(image,bodies,index,connected)
            assert original==rebuilt and original['modelPassed'],(connected,index,original)
            own.update(original['ownedObserved']);nested+=original['actualNestedReturns']*2
            for address,size,value in original['reads']:reads.update(range(address,address+size))
            traces.append(dict(original=original,rebuilt=rebuilt))
    coverage=[]
    for base,size in [(fixture.APPLY,516),(fixture.CALLER,44)]:
        instructions={byte for word in own if base<=word<base+size for byte in range(word,word+4)}
        pool=(reads & set(range(base,base+size)))-instructions
        assert instructions|pool==set(range(base,base+size)),(hex(base),len(instructions),len(pool))
        coverage.append(dict(address=hex(base),instructionBytesObserved=len(instructions),poolBytesObserved=len(pool)))
    text=source.read_text(encoding='utf-8')
    mutations=[('attribute-width','sizeof(u16) * 3','sizeof(u16) * 2'),
        ('affine-offset','offset += sizeof(u16) * 3','offset += sizeof(u16) * 2')]
    controls=[]
    for label,before,after in mutations:
        occurrences=text.count(before);assert occurrences==(2 if label=='attribute-width'else 1)
        if label=='attribute-width':changed=text.replace('pFrom, offset, sizeof(u16) * 3','pFrom, offset, sizeof(u16) * 2')
        else:changed=text.replace(before,after)
        assert changed!=text
        wrong=ROOT/f'nonmatching/integration/20261101-oam-apply516/{label}/source.c'
        wrong.parent.mkdir(parents=True,exist_ok=True)
        if wrong.exists():assert wrong.read_text(encoding='utf-8')==changed
        else:wrong.write_text(changed,encoding='utf-8')
        row,proof,body=sdk_builder.build(wrong,'wrong-'+label,False)
        bad={**bodies,fixture.APPLY:body}
        cases=[fixture.execute(image,bad,index,False)for index in range(96)]
        rejected=sum(not case['modelPassed']for case in cases)
        assert rejected and rejected<96 and all(case['actualReturn']for case in cases)
        controls.append(dict(label=label,source=wrong.relative_to(ROOT).as_posix(),sourceSha256=sha256(wrong),
            compilation=row,genuineLinkComparison=proof,actualWrongReturns=96,independentModelRejections=rejected,
            unchangedPositives=96-rejected,cases=cases))
    try:fixture.execute(image,bodies,0,True,bound=1)
    except AssertionError:pass
    else:raise AssertionError('Instruction prefix admitted as returning caller')
    trace=ROOT/'evidence/traces/main-oam-apply-connected516-20261101.json.gz';trace.parent.mkdir(parents=True,exist_ok=True)
    trace.write_bytes(gzip.compress(json.dumps(dict(traces=traces,controls=controls),sort_keys=True,separators=(',',':')).encode(),mtime=0))
    for row,proof,size in [(apply_row,apply_proof,516),(caller_row,caller_proof,44)]:
        row.update(genuineLinkComparison=freeze_link(proof),exactBytes=size,sourceOnlyCompilerInput=True,
            originalObjectScaffolding=False,sourceLanguage='C')
    dependency=dict(compilation=reset_row,genuineLinkComparison=freeze_link(reset_proof),alreadySelectedFunction=True,newByteCredit=0)
    dependencies=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in
        [Path(fixture.__file__),Path(sdk_builder.__file__),sdk_builder.SOURCE,trace,original_caller]]
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),
        romSha256=config['romSha256'],processor='arm9',program='',module='main',moduleSha256=metadata['sha256'],
        matches=[apply_row,caller_row],matchedFunctions=2,matchedBytes=560,newCandidateFunctions=1,newCandidateBytes=516,
        migrationFunctions=1,migrationBytes=44,reconstructedDependency=dependency,replayDependencies=dependencies,
        oracle=dict(directPairs=96,connectedPairs=96,actualTopReturns=384,actualNestedReturnsSeparate=nested,providedCalls=0,
            completeRegistersFlagsStackMainCacheOamOrderedReadsAndWritesCompared=True,coverage=coverage,
            dmaWord=0xFFFFFFFF,actualHardwareInstructionsAndMmioStores=True,physicalDeviceBehaviorProven=False),
        negativeEvidence=dict(actualWrongReturns=192,independentModelRejections=sum(row['independentModelRejections']for row in controls),
            controls=[{k:v for k,v in row.items()if k!='cases'}for row in controls],boundedPrefixCredit=0),
        sourceInterface=dict(applyReturn='void',applyArgument='signed int raw address',
            callerUsesVoidApplyAndSignedWordResetPrototypes=True,originalCallerSourceUnmodified=True,
            directPhysicalR0ComparedButNotAssignedApiMeaning=True,wholeModuleAcceptancePending=True),
        reproductionCommand='python match_main_oam_apply_connected516_20261101.py',
        limitations=['DMA wordFFFFFFFF selects original CPU-copy fallback; actual DMA register/device paths unproved',
            'Original cache instructions and OAM-address stores execute in isolated Unicorn RAM, not a physical renderer',
            'Two synthetic nonnegative caller indices qualify address arithmetic without asserting game object count or ownership',
            'Banks0/1 hardware transfer and bank2 fast default-flush path only; bank2 slow null callbacks unsupported',
            'Bounded disjoint buffers and reserved windows; aliases, asynchronous devices and malformed pointers unsupported',
            'Caller44 is an existing-source declaration migration with zero new byte credit; Reset296 is already selected',
            'No source-only ROM, complete Windows game or Android device execution established'])
    write_json(ROOT/'evidence/matches/main-oam-apply-connected516-20261101.json',report)
    print(dict(newFunctions=1,newBytes=516,migratedBytes=44,actualTopReturns=384,nestedReturns=nested,
        providedCalls=0,wrongReturns=192,wrongRejections=report['negativeEvidence']['independentModelRejections']))


if __name__=='__main__':
    main()
