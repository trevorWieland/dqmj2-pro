import json
from collections import Counter
from pathlib import Path
import arm7_lane_skip_native_20261031 as fixture
from project import ROOT,sha256,write_json


def main():
    path=ROOT/'work/arm7-bulk-20261030/lane-sdk-typed68-01/results.json'
    unit=next(row for row in json.loads(path.read_text())['results'] if int(row['address'],0)==fixture.ADDRESS)
    variant=next(row for row in unit['variants'] if row.get('realLink',{}).get('exactLinkedBytes'))
    entry,proof=variant['entry'],variant['realLink']
    for path,expected in ((entry['source'],entry['sourceSha256']),(entry['object'],entry['objectSha256'])):
        if sha256(ROOT/path)!=expected:
            raise ValueError('Current typed skip source/object differs')
    for item in unit['sourceDependencies']:
        if sha256(ROOT/item['path'])!=item['sha256']:
            raise ValueError('Current typed skip source include differs')
    product=Path(proof['cwd'])/'caller.bin'
    if not product.resolve().is_relative_to(ROOT) or sha256(product)!=proof['linkedCallerSha256']:
        raise ValueError('Current genuine linked skip body differs')
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    original=raw[fixture.ADDRESS-fixture.BASE:fixture.ADDRESS-fixture.BASE+fixture.SIZE]
    rebuilt=product.read_bytes()
    if original!=rebuilt:
        raise ValueError('Complete genuine linked skip range differs')
    records,visited,nested=[],set(),Counter()
    for seed,case in enumerate(fixture.cases()):
        native=fixture.execute(original,case,seed)
        source=fixture.execute(rebuilt,case,seed)
        if native!=source or len(native['states'])!=case['passes'] or any(not row['actualReturn'] or row['fault'] is not None for row in native['states']):
            raise ValueError('Skip original/source complete machine state or supported actual return differs')
        visited.update(native['visited'])
        for state in native['states']:
            nested.update({address:count*2 for address,count in state['actualFunctionReturns'].items() if int(address,0)!=fixture.ADDRESS})
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=2*len(native['states']),
            actualOriginalPrerequisiteReturns=len(native['prerequisites'])*2,
            completedIterations=[state['expectedCompletedIterations'] for state in native['states']],
            originalAndCompiledStateSha256=fixture.digest(repr(native).encode()),
            actualInstructionsPerInvocation=[state['instructions'] for state in native['states']]))
        if seed%24==0:
            print(json.dumps(dict(processed=seed+1)),flush=True)
    own=set(range(fixture.ADDRESS,fixture.ADDRESS+fixture.CODE,4))
    if not own.issubset(visited):
        raise ValueError('Own skip instruction coverage incomplete: '+repr([hex(a) for a in sorted(own-visited)]))
    cap=fixture.execute(original,fixture.cases()[0],0,budget=1)
    if cap['states'][0]['actualReturn']:
        raise ValueError('Instruction exhaustion received false actual-return credit')
    report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),fixture=Path(fixture.__file__).name,
        fixtureSha256=sha256(fixture.__file__),inventorySha256=sha256(ROOT/'evidence/arm7/ghidra-runtime-inventory.json'),
        entry=entry,realArm7Link=proof,sourceCredit=0,scenarios=len(records),
        providerFreeOriginalAndCompiledReturns=sum(row['actualOriginalAndCompiledReturns'] for row in records),
        actualOriginalPrerequisiteReturns=sum(row['actualOriginalPrerequisiteReturns'] for row in records),
        actualSeparatelyObservedNestedReturns=dict(sorted(nested.items())),allOwnInstructionAddresses=sorted(own),
        records=records,unsupportedControls=[dict(kind='instruction-cap',actualReturn=False,returnCredit=0)],
        limitations=['Original alarm/sequence and conditional track constructors execute before explicit synthetic contexts',
            'All original timer/alarm/tick helpers execute against zero-clock disposable MMIO; no function/service provider replacement',
            'Only synthetic no-channel wait/end streams and logical player0..15 are qualified; assets, BIOS, physical timing and scene reachability remain unproved',
            'Independent model covers ordered direct calls, complete-iteration counter/wrap, wait, slot and active-state effects; opaque helper memory effects are compared original/source, not assigned meanings',
            'No ordinary helper source, full-module or whole-game credit'])
    destination=ROOT/'evidence/attempts/arm7-lane-skip-native-20261031.json'
    write_json(destination,report)
    print(json.dumps(dict(report=destination.relative_to(ROOT).as_posix(),sha256=sha256(destination),scenarios=len(records),
        providerFreeReturns=report['providerFreeOriginalAndCompiledReturns'],sourceCredit=0)),flush=True)


if __name__=='__main__':
    main()
