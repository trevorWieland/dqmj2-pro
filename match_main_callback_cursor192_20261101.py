import gzip
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import match_runtime as compiler
from main_callback_cursor192_fixture_20261101 import ENTRY,SIZE,IRQ,execute
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import measured_module,validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link

WORK = ROOT/'work/callback-cursor192-20261101'


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
    source=ROOT/'src/runtime/20261101_callback_cursor192/native_main_0200a81c.c'
    row,proof,body=build(source,'positive',True)
    native=image[ENTRY-0x02000000:ENTRY-0x02000000+SIZE]
    assert body==native
    cases,observed,helpers,controls=[],set(),set(),[]
    for index in range(512):
        first,second=execute(image,native,index),execute(image,body,index)
        assert first==second
        observed.update(first['observed']);helpers.update(first['helperObserved'])
        cases.append(dict(index=index,original=first,candidate=second))
    assert len(observed)==192 and len(helpers)==44
    for number,(before,after)in enumerate([('cursor->offset += length;', 'cursor->offset += length * 2;'),
        ('state->flags &= ~0x200U;', 'state->flags |= 0x200U;')]):
        text=source.read_text();assert text.count(before)==1
        path=ROOT/f'nonmatching/integration/20261101-callback-cursor-controls/{number}/source.c';path.parent.mkdir(parents=True,exist_ok=True)
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
    try:execute(image,native,6,bound=256,permanent=True)
    except AssertionError:pass
    else:raise AssertionError('Permanent wait is not a return')
    raw=json.dumps(cases,sort_keys=True,separators=(',',':')).encode();trace=ROOT/'evidence/traces/main-callback-cursor192-20261101.json.gz';trace.parent.mkdir(parents=True,exist_ok=True);trace.write_bytes(gzip.compress(raw,mtime=0))
    row.update(genuineLinkComparison=freeze_link(proof),exactBytes=192,sourceOnlyCompilerInput=True,originalObjectScaffolding=False)
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),fixture='main_callback_cursor192_fixture_20261101.py',fixtureSha256=sha256(ROOT/'main_callback_cursor192_fixture_20261101.py'),
        romSha256=config['romSha256'],processor='arm9',program='',module='main',moduleSha256=metadata['sha256'],matches=[row],matchedFunctions=1,matchedBytes=192,
        nativeDependencies=[dict(processor='arm9',program='',module='main',mode='arm',address=hex(start),bytes=width,targetSha256=hashlib.sha256(image[start-0x02000000:start-0x02000000+width]).hexdigest())for start,width in IRQ.items()],
        oracle=dict(pairs=512,actualTopReturns=1024,actualNativeDependencyReturns=sum(x['original']['actualNativeDependencyReturns']*2 for x in cases),
            suppliedCalls=sum(x['original']['suppliedCalls']*2 for x in cases),ownCodeBytesObserved=192,helperCodeBytesObserved=44,
            providedServices=['Dynamic four-word operation callback at026A0000','Original scheduler sleep entry020068D4'],
            actualReturnRequired=True,fullPagesStackCpuAndOrderedStores=True,callbackFourPhysicalWordsCompared=True,
            independentModel='Busy-bit lifecycle; callback/sleep changes to live cursor/result; finite wait completion; unsigned offset wrap on every result path',
            traceArchive=dict(path=trace.relative_to(ROOT).as_posix(),sha256=sha256(trace),decodedSha256=hashlib.sha256(raw).hexdigest())),
        negativeEvidence=dict(compiledReturningControls=controls,exhaustedPrefixReturnCredit=0,permanentWaitReturnOrErrorCredit=0),
        replayDependencies=[dict(path=trace.relative_to(ROOT).as_posix(),sha256=sha256(trace))],
        reproductionCommand='python match_main_callback_cursor192_20261101.py',
        limitations=['Operation callback and sleep are explicit stateful service providers, not recovered native closures',
            'Only finite0..3 sleeps; permanent wait and instruction exhaustion carry no completion/error/post-state credit',
            'Measured scalar fields and four physical callback words; original aggregate/public API names remain hypotheses',
            'Actual original IRQ helpers execute without providers and receive no duplicate source credit',
            'No malformed callback pointers, real scheduler/concurrency, full module or source-only host-game proof'])
    write_json(ROOT/'evidence/matches/main-callback-cursor192-20261101.json',report)
    print(dict(newFunctions=1,newBytes=192,actualTopReturns=1024,originalLowerReturns=report['oracle']['actualNativeDependencyReturns'],wrongReturns=192,
        independentRejections=sum(x['independentRejections']for x in controls),suppliedCalls=report['oracle']['suppliedCalls']))


if __name__=='__main__':main()
