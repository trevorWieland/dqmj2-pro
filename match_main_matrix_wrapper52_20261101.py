import gzip
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import match_runtime as compiler
from main_matrix_wrapper52_fixture_20261101 import ENTRY,SIZE,LOWER,LOWER_SIZE,execute
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import measured_module,validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link

WORK = ROOT/'work/matrix-wrapper52-20261101'


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
    source=ROOT/'src/runtime/20261101_matrix_wrapper52/native_main_02001114.c'
    row,proof,body=build(source,'positive',True)
    native=image[ENTRY-0x02000000:ENTRY-0x02000000+SIZE]
    assert body==native
    cases,observed,helpers,controls=[],set(),set(),[]
    for index in range(512):
        first,second=execute(image,native,index),execute(image,body,index)
        assert first==second
        observed.update(first['observed']);helpers.update(first['helperObserved'])
        cases.append(dict(index=index,original=first,candidate=second))
    assert len(observed)==52 and len(helpers)==192
    for number,(before,after)in enumerate([('destination[10] = source[10];','destination[10] = source[9];'),
        ('native_fn_02000d0c(source,destination,x,y,z);','native_fn_02000d0c(source,destination,x,y,y);')]):
        text=source.read_text();assert text.count(before)==1
        path=ROOT/f'nonmatching/integration/20261101-matrix-wrapper-controls/{number}/source.c';path.parent.mkdir(parents=True,exist_ok=True)
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
    raw=json.dumps(cases,sort_keys=True,separators=(',',':')).encode();trace=ROOT/'evidence/traces/main-matrix-wrapper52-20261101.json.gz';trace.parent.mkdir(parents=True,exist_ok=True);trace.write_bytes(gzip.compress(raw,mtime=0))
    row.update(genuineLinkComparison=freeze_link(proof),exactBytes=52,sourceOnlyCompilerInput=True,originalObjectScaffolding=False)
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),fixture='main_matrix_wrapper52_fixture_20261101.py',fixtureSha256=sha256(ROOT/'main_matrix_wrapper52_fixture_20261101.py'),
        romSha256=config['romSha256'],processor='arm9',program='',module='main',moduleSha256=metadata['sha256'],matches=[row],matchedFunctions=1,matchedBytes=52,
        nativeDependencies=[dict(processor='arm9',program='',module='main',mode='arm',address=hex(LOWER),bytes=LOWER_SIZE,targetSha256=hashlib.sha256(image[LOWER-0x02000000:LOWER-0x02000000+LOWER_SIZE]).hexdigest())],
        oracle=dict(pairs=512,actualTopReturns=1024,actualNativeDependencyReturns=1024,suppliedCalls=0,ownCodeBytesObserved=52,helperCodeBytesObserved=192,
            actualReturnRequired=True,fullPagesStackCpuAndOrderedStores=True,fifthStackWordForwardingCompared=True,
            independentModel='Nine sequential signed64 products shifted12 and truncated32; three copied words; exact in-place/partial-overlap ordering',
            traceArchive=dict(path=trace.relative_to(ROOT).as_posix(),sha256=sha256(trace),decodedSha256=hashlib.sha256(raw).hexdigest())),
        negativeEvidence=dict(compiledReturningControls=controls,exhaustedPrefixReturnCredit=0),
        replayDependencies=[dict(path=trace.relative_to(ROOT).as_posix(),sha256=sha256(trace))],
        reproductionCommand='python match_main_matrix_wrapper52_20261101.py',
        limitations=['Synthetic mapped12-word inputs and outputs, disjoint/in-place/four-byte and12-byte overlap cases',
            'Observed fixed-point operation is independently modeled; original formal types and scene availability remain unproved',
            'Original192-byte lower routine executes but receives zero duplicate source credit',
            'No malformed pointers, concurrency, hardware, full module acceptance or source-only game proof'])
    write_json(ROOT/'evidence/matches/main-matrix-wrapper52-20261101.json',report)
    print(dict(newFunctions=1,newBytes=52,actualTopReturns=1024,originalLowerReturns=1024,wrongReturns=192,
        independentRejections=sum(x['independentRejections']for x in controls),suppliedCalls=0))


if __name__=='__main__':main()
