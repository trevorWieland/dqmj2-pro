import gzip
import json
from pathlib import Path
import match_runtime
import main_oam_three_ram_fixture_v3_20261101 as fixture
import match_main_oam_reference296_closed_20261101 as builder
from project import ROOT, configuration, read_json, write_json, sha256
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link


ENTRIES=[(0x02036C78,348,216),(0x02036DD4,208,360),(0x02036EA4,196,108)]


def main():
    config=configuration();assert sha256(config['rom'])==config['romSha256']
    metadata,image,_=measured_module('main')
    accepted=read_json(ROOT/'evidence/verification/accepted-cohort121-identities-v2-20261101.json')
    selected=set(row['source']for row in accepted['functions']if row['source'].endswith('.c'))
    for path in selected:
        text=(ROOT/path).read_text(encoding='utf-8')
        assert not any('native_fn_'+f'{address:08x}'in text for address,_,_ in ENTRIES),path
    builder.WORK=ROOT/'work/main-oam-ram-three752-20261101'
    matches=[];traces=[];controls=[];summaries=[];dependencies=[]
    for address,size,count in ENTRIES:
        source=ROOT/f'src/runtime/20261101_oam_ram_family/native_main_{address:08x}.c'
        text=source.read_text(encoding='utf-8')
        assert len(text.splitlines())<=500 and '#include'not in text and 'ctrdgi_'not in text
        row,proof,body=builder.build(source,f'correct-{address:08x}',True)
        assert len(body)==size and body==image[address-0x02000000:address-0x02000000+size]
        cases=[];own=set();pools=set()
        for index in range(count):
            original=fixture.execute(image,address,body,index)
            rebuilt=fixture.execute(image,address,body,index)
            assert original==rebuilt and original['modelPassed'],(hex(address),index,original)
            own.update(original['ownedObserved'])
            for location,length,value in original['reads']:
                if address<=location and location+length<=address+size:pools.update(range(location,location+length))
            cases.append(dict(original=original,rebuilt=rebuilt))
        instruction_bytes={byte for word in own for byte in range(word,word+4)}
        assert not instruction_bytes & pools
        assert instruction_bytes|pools==set(range(address,address+size)),(hex(address),len(instruction_bytes),len(pools),size)
        if address==0x02036C78:before,after='pMan->bFastTransferEnable = 1','pMan->bFastTransferEnable = 0'
        elif address==0x02036DD4:before,after='pOam->attr2','pOam->attr1'
        else:before,after='mtx->_00 >> 4','mtx->_00 >> 5'
        assert text.count(before)==1
        wrong=ROOT/f'nonmatching/integration/20261101-oam-ram-three752/{address:08x}/source.c'
        wrong.parent.mkdir(parents=True,exist_ok=True);changed=text.replace(before,after)
        if wrong.exists():assert wrong.read_text(encoding='utf-8')==changed
        else:wrong.write_text(changed,encoding='utf-8')
        bad_row,bad_proof,bad_body=builder.build(wrong,f'wrong-{address:08x}',False)
        bad_cases=[fixture.execute(image,address,bad_body,index)for index in range(count)]
        rejected=sum(not case['modelPassed']for case in bad_cases)
        assert rejected and rejected<count and all(case['actualReturn']for case in bad_cases)
        control=dict(address=hex(address),source=wrong.relative_to(ROOT).as_posix(),sourceSha256=sha256(wrong),
            compilation=bad_row,genuineLinkComparison=bad_proof,actualWrongReturns=count,
            independentModelRejections=rejected,unchangedPositives=count-rejected)
        controls.append(control)
        try:fixture.execute(image,address,body,0,bound=1)
        except AssertionError:pass
        else:raise AssertionError('Instruction prefix admitted as actual return')
        row.update(genuineLinkComparison=freeze_link(proof),exactBytes=size,
            sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceLanguage='C')
        matches.append(row)
        summaries.append(dict(address=hex(address),pairs=count,actualTopReturns=count*2,
            actualNativeReturnsSeparate=sum(case['original']['actualNativeReturns']*2 for case in cases),providedCalls=0,
            ownInstructionBytesObserved=len(instruction_bytes),ownPoolBytesRead=len(pools)))
        traces.append(dict(address=hex(address),cases=cases,negative=dict(control=control,cases=bad_cases)))
        dependencies.append(dict(path=wrong.relative_to(ROOT).as_posix(),sha256=sha256(wrong)))
        print(dict(address=hex(address),pairs=count,bytes=size,wrongRejections=rejected),flush=True)
    trace=ROOT/'evidence/traces/main-oam-ram-three752-20261101.json.gz'
    trace.parent.mkdir(parents=True,exist_ok=True)
    trace.write_bytes(gzip.compress(json.dumps(traces,sort_keys=True,separators=(',',':')).encode(),mtime=0))
    dependencies.extend(dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in [Path(fixture.__file__),Path(builder.__file__),trace,
        ROOT/'evidence/verification/accepted-cohort121-identities-v2-20261101.json'])
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),
        romSha256=config['romSha256'],processor='arm9',program='',module='main',moduleSha256=metadata['sha256'],
        matches=matches,matchedFunctions=3,matchedBytes=752,oracle=dict(summaries=summaries,
            actualTopReturns=sum(row['actualTopReturns']for row in summaries),providedCalls=0,
            actualNativeReturnsSeparate=sum(row['actualNativeReturnsSeparate']for row in summaries),
            fullRegistersFlagsStackDataOrderedReadsAndWritesCompared=True,allOwnInstructionsAndPoolBytesObserved=True),
        negativeEvidence=dict(controls=controls,actualWrongReturns=sum(row['actualWrongReturns']for row in controls),
            independentModelRejections=sum(row['independentModelRejections']for row in controls),boundedPrefixCredit=0),
        replayDependencies=dependencies,sourceOrigin=dict(referenceAssisted=True,noHeaderPlaceholders=True,
            publicSdkFormalViewsRetained=True,selectedCIncomingCallersFound=0,callerSnapshot=121,
            originalGameApiTypesProven=False,manualReviewRemovedUnrelatedFlashDeclarationAndReleaseNoops=True),
        reproductionCommand='python match_main_oam_ram_three752_20261101.py',
        limitations=['Disjoint manager/source/cache buffers; aliases and concurrency remain unsupported',
            'Constructor banks0..2, aligned first/count within128 attributes/32 affine slots, both reservation failures including retained partial effects',
            'Entry bounded valid/invalid capacities, zero/full/oversized halfword counts; affine signed32 matrices with native arithmetic shift',
            'Original halfword fill instructions actually return but earn no additional source credit',
            'SDK signature evidence and measured word layouts do not establish historical game SDK version',
            'Complete module/regression acceptance remains pending; no source-only ROM, rendering or complete native game claim'])
    write_json(ROOT/'evidence/matches/main-oam-ram-three752-20261101.json',report)
    print(dict(functions=3,bytes=752,actualTopReturns=report['oracle']['actualTopReturns'],
        actualHelperReturns=report['oracle']['actualNativeReturnsSeparate'],providedCalls=0,
        wrongReturns=report['negativeEvidence']['actualWrongReturns'],wrongRejections=report['negativeEvidence']['independentModelRejections']))


if __name__=='__main__':
    main()
