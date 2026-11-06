import gzip
import json
from pathlib import Path
import match_runtime
import main_resource_dictionary_fixture_v4_20261101 as fixture
import match_main_oam_reference296_closed_20261101 as builder
from project import ROOT,configuration,read_json,write_json,sha256
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link

ENTRIES=[(0x0202BBB4,448),(0x0202BD74,360)]
CALLERS=['src/runtime/ov001-drafts01/native_ov001_021d9424.c',
    'src/runtime/runtime08/native_main_02028cec.c','src/runtime/runtime08/native_main_02028d50.c']


def main():
    config=configuration();assert sha256(config['rom'])==config['romSha256']
    metadata,image,_=measured_module('main');builder.WORK=ROOT/'work/main-resource-dictionary808-20261101'
    matches=[];summary=[];traces=[];controls=[]
    for caller in CALLERS:
        text=(ROOT/caller).read_text(encoding='utf-8')
        assert 'extern u32 native_fn_0202bd74();'in text
        assert 's32 var_r0' in text and 'extern u8 native_data_'in text
    for entry,size in ENTRIES:
        source=ROOT/f'src/runtime/20261101_resource_dictionary/native_main_{entry:08x}.c'
        text=source.read_text(encoding='utf-8')
        row,proof,body=builder.build(source,f'correct-{entry:08x}',True)
        native=image[entry-0x02000000:entry-0x02000000+size];assert body==native
        cases=[];own=set()
        for index in range(312):
            original=fixture.execute(image,entry,native,index)
            rebuilt=fixture.execute(image,entry,body,index)
            assert original==rebuilt and original['modelPassed'],(hex(entry),index)
            own.update(original['ownedObserved']);cases.append(dict(original=original,rebuilt=rebuilt))
        malformed_original=fixture.execute(image,entry,native,5,corrupt_entry=True)
        malformed_rebuilt=fixture.execute(image,entry,body,5,corrupt_entry=True)
        assert malformed_original==malformed_rebuilt and not malformed_original['actualReturn']
        missing=sorted(set(range(entry,entry+size,4))-own)
        expected={0x0202BBB4:[0x0202BC14,0x0202BC64,0x0202BC68,0x0202BD04,0x0202BD64,0x0202BD68],
            0x0202BD74:[0x0202BDD4,0x0202BE98]}[entry]
        assert missing==expected
        before='n->val[3] ==';assert text.count(before)==2
        wrong=ROOT/f'nonmatching/integration/20261101-resource-dictionary808/{entry:08x}/source.c'
        wrong.parent.mkdir(parents=True,exist_ok=True);changed=text.replace(before,'n->val[3] !=')
        if wrong.exists():assert wrong.read_text(encoding='utf-8')==changed
        else:wrong.write_text(changed,encoding='utf-8')
        bad_row,bad_proof,bad_body=builder.build(wrong,f'wrong-{entry:08x}',False)
        wrong_cases=[fixture.execute(image,entry,bad_body,index)for index in range(156)]
        rejected=sum(not case['modelPassed']for case in wrong_cases)
        assert rejected and rejected<156 and all(case['actualReturn']for case in wrong_cases)
        controls.append(dict(entry=hex(entry),source=wrong.relative_to(ROOT).as_posix(),sourceSha256=sha256(wrong),
            compilation=bad_row,genuineLinkComparison=bad_proof,actualWrongReturns=156,
            independentLinearModelRejections=rejected,positiveControls=156-rejected,cases=wrong_cases))
        try:fixture.execute(image,entry,native,0,bound=1)
        except AssertionError:pass
        else:raise AssertionError('Instruction prefix credited as return')
        row.update(genuineLinkComparison=freeze_link(proof),exactBytes=size,
            sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceLanguage='C')
        matches.append(row)
        summary.append(dict(address=hex(entry),pairs=312,actualTopReturns=624,providedCalls=0,actualHelpers=0,
            ownInstructionBytesObserved=len(own)*4,fullFunctionLinkedBytes=size,
            defensiveGuardInstructionsNotReachedByValidImmutableCorpus=[hex(address)for address in missing],
            malformedEntryFault=malformed_original,malformedFaultReturnCredit=0))
        traces.append(dict(entry=hex(entry),cases=cases,malformedOriginal=malformed_original,malformedRebuilt=malformed_rebuilt))
    trace=ROOT/'evidence/traces/main-resource-dictionary808-20261101.json.gz';trace.parent.mkdir(parents=True,exist_ok=True)
    trace.write_bytes(gzip.compress(json.dumps(dict(traces=traces,controls=controls),sort_keys=True,separators=(',',':')).encode(),mtime=0))
    deps=[Path(fixture.__file__),Path(builder.__file__),trace,*[ROOT/path for path in CALLERS]]
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),
        romSha256=config['romSha256'],processor='arm9',program='',module='main',moduleSha256=metadata['sha256'],
        matches=matches,matchedFunctions=2,matchedBytes=808,oracle=dict(pairs=624,actualTopReturns=1248,
            providedCalls=0,actualHelperReturns=0,fullRegistersFlagsImmutableMainDataQueryStackAndReadOrderCompared=True,
            independentOracle='Linear comparison of complete sixteen-byte names, not the native Patricia walk',
            counts=fixture.COUNTS,allOwnInstructionsExecuted=False,summaries=summary),
        negativeEvidence=dict(actualWrongReturns=312,independentModelRejections=sum(row['independentLinearModelRejections']for row in controls),
            controls=[{key:value for key,value in row.items()if key!='cases'}for row in controls],
            malformedRecordFaults=4,malformedFaultReturnCredit=0,boundedPrefixReturnCredit=0),
        sourceInterface=dict(dataFunctionTypedSdkView=True,indexFunctionRawUnsignedResultSignedAddressAndUnsignedCharPointer=True,
            selectedIndexCallerSources=CALLERS,allSelectedCallerSourcesUnmodified=True,originalGameApiTypesProven=False),
        replayDependencies=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in deps],
        reproductionCommand='python match_main_resource_dictionary808_20261101.py',
        limitations=['Configured source spans match every linked byte; native valid-corpus coverage is424/448 and352/360 instruction bytes',
            'Remaining source-reconstructed guards test null/out-of-range helper inputs excluded by immutable nonnull dictionary and bounded valid nodes',
            'A bounded out-of-range Patricia entry executes the null-name guards and faults identically, with no return credit',
            'Synthetic Patricia dictionaries, empty-root malformed case, all four name words, name aliases, null query and threshold15/16 are tested',
            'Null dictionary with nonnull query, concurrent header changes, malformed pointers and unaligned word inputs remain unsupported',
            'Reference resource names are binary sixteen-byte keys; no text encoding or game asset ownership is inferred',
            'Complete module/regression acceptance pending; no source-only ROM or complete native game proof'])
    write_json(ROOT/'evidence/matches/main-resource-dictionary808-20261101.json',report)
    print(dict(functions=2,bytes=808,actualTopReturns=1248,providers=0,wrongReturns=312,
        wrongRejections=report['negativeEvidence']['independentModelRejections'],malformedFaultReturnCredit=0))


if __name__=='__main__':
    main()
