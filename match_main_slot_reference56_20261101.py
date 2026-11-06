import gzip
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import match_runtime as compiler
from main_slot_reference56_fixture_20261101 import ENTRY,SIZE,LOWER,execute
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import measured_module,validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link

WORK = ROOT/'work/slot-reference56-20261101'


def build(source, label, exact):
    compiler.WORK = WORK / label / 'compile'
    rows, unused = compiler.compare(source, 'main', 2, 'off')
    assert len(rows) == 1 and not rows[0].get('compileFailed')
    row = rows[0]
    try:
        proof = validate(row, qualified_bindings(row), WORK / label / 'link')
    except ValueError as error:
        if exact:
            raise
        assert not exact and isinstance(error.args[0], dict)
        proof = error.args[0]
    return row, proof, (WORK / label / 'link/caller.bin').read_bytes()



def main():
    config=configuration();assert sha256(config['rom'])==config['romSha256']
    metadata,image,unused=measured_module('main')
    source=ROOT/'src/runtime/20261101_slot_reference56/native_main_0203a650.c'
    row,proof,body=build(source,'positive',True)
    native=image[ENTRY-0x02000000:ENTRY-0x02000000+SIZE]
    assert body==native
    cases,observed,helpers,controls=[],set(),set(),[]
    for index in range(512):
        first,second=execute(image,native,index),execute(image,body,index)
        assert first==second
        observed.update(first['observed']);helpers.update(first['helperObserved'])
        cases.append(dict(index=index,original=first,candidate=second))
    assert len(observed)==56 and len(helpers)>=128
    for number,(before,after)in enumerate([('state->references += 1;', 'state->references += 2;'),
        ('native_fn_0203b5d8(state, count, slots) == 0', 'native_fn_0203b5d8(state, count, slots) != 0')]):
        text=source.read_text();assert text.count(before)==1
        path=ROOT/f'nonmatching/integration/20261101-slot-reference-controls/{number}/source.c';path.parent.mkdir(parents=True,exist_ok=True)
        changed=text.replace(before,after)
        if path.exists():assert path.read_text()==changed
        path.write_text(changed,encoding='utf-8')
        bad,badproof,badbody=build(path,f'negative-{number}',False)
        results=[execute(image,badbody,index,require_model=False)for index in range(96)]
        rejected=sum(not x['modelPassed']for x in results);assert rejected>0
        controls.append(dict(compilation=bad,genuineLinkComparison=badproof,actualReturns=96,independentRejections=rejected,
            unchangedPositiveCases=96-rejected,cases=results))
    try:execute(image,native,0,bound=1)
    except AssertionError:pass
    else:raise AssertionError('Prefix is not a return')
    raw=json.dumps(cases,sort_keys=True,separators=(',',':')).encode();trace=ROOT/'evidence/traces/main-slot-reference56-20261101.json.gz';trace.parent.mkdir(parents=True,exist_ok=True);trace.write_bytes(gzip.compress(raw,mtime=0))
    row.update(genuineLinkComparison=freeze_link(proof),exactBytes=56,sourceOnlyCompilerInput=True,originalObjectScaffolding=False)
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),fixture='main_slot_reference56_fixture_20261101.py',fixtureSha256=sha256(ROOT/'main_slot_reference56_fixture_20261101.py'),
        romSha256=config['romSha256'],processor='arm9',program='',module='main',moduleSha256=metadata['sha256'],matches=[row],matchedFunctions=1,matchedBytes=56,
        nativeDependencies=[dict(processor='arm9',program='',module='main',mode='arm',address=hex(start),bytes=width,targetSha256=hashlib.sha256(image[start-0x02000000:start-0x02000000+width]).hexdigest())for start,width in LOWER.items()],
        oracle=dict(pairs=512,actualTopReturns=1024,actualNativeDependencyReturns=sum(x['original']['actualNativeDependencyReturns']*2 for x in cases),suppliedCalls=0,ownCodeBytesObserved=56,helperCodeBytesObserved=len(helpers),
            actualReturnRequired=True,fullPagesStackCpuAndOrderedStores=True,threePhysicalArgumentWordsCompared=True,
            independentModel='Unsigned reference-count wrap; sequential alias-aware byte copying and post-store mask reads; zero-mask success and occupied-mask failure',
            traceArchive=dict(path=trace.relative_to(ROOT).as_posix(),sha256=sha256(trace),decodedSha256=hashlib.sha256(raw).hexdigest())),
        negativeEvidence=dict(compiledReturningControls=controls,exhaustedPrefixReturnCredit=0),
        replayDependencies=[dict(path=trace.relative_to(ROOT).as_posix(),sha256=sha256(trace))],
        reproductionCommand='python match_main_slot_reference56_20261101.py',
        limitations=['Original initializer96 executes but remains source-unmatched and receives zero source credit',
            'Only zero-mask success and occupied-mask failure are supported; free nonzero masks reach an unqualified queue/send closure',
            'Negative signed counts and bounded0..32 slots, mapped disjoint and one-byte/in-place aliases; original formal names and game availability unproved',
            'All own code is observed; helper coverage is reported separately and does not claim all initializer/reservation paths',
            'No malformed pointers, concurrency, hardware, full module acceptance or source-only game proof'])
    write_json(ROOT/'evidence/matches/main-slot-reference56-20261101.json',report)
    print(dict(newFunctions=1,newBytes=56,actualTopReturns=1024,originalLowerReturns=report['oracle']['actualNativeDependencyReturns'],wrongReturns=192,
        independentRejections=sum(x['independentRejections']for x in controls),suppliedCalls=0))


if __name__=='__main__':main()
