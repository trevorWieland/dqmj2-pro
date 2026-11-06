import json
from collections import Counter
from pathlib import Path
import arm7_lane_alarm_selector_native_20261031 as fixture
from project import ROOT,sha256,write_json


def main():
    path=ROOT/'work/arm7-bulk-20261030/lane-main-alarm-selector-base/027e5bac/report.json'
    current=json.loads(path.read_text())
    entry,proof=current['entry'],current['proof']
    if sha256(ROOT/entry['source'])!=entry['sourceSha256'] or sha256(ROOT/entry['object'])!=entry['objectSha256']:
        raise ValueError('Current typed selector source/immutable object differs')
    product=Path(proof['cwd'])/'caller.bin'
    if not product.resolve().is_relative_to(ROOT) or sha256(product)!=proof['linkedCallerSha256']:
        raise ValueError('Current genuine linked selector differs')
    raw=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes()
    original=raw[fixture.ADDRESS-fixture.BASE:fixture.ADDRESS-fixture.BASE+fixture.SIZE]
    rebuilt=product.read_bytes()
    if original!=rebuilt:
        raise ValueError('Full typed selector linked bytes differ')
    records,visited,nested=[],set(),Counter()
    for seed,case in enumerate(fixture.cases()):
        native=fixture.execute(original,case,seed)
        source=fixture.execute(rebuilt,case,seed)
        if native!=source or len(native['states'])!=case['passes'] or any(not state['actualReturn'] or state['fault'] is not None for state in native['states']):
            raise ValueError('Selector full original/source machine state or supported return differs')
        visited.update(native['visited'])
        for state in native['states']:
            nested.update({a:n*2 for a,n in state['actualFunctionReturns'].items() if int(a,0)!=fixture.ADDRESS})
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=len(native['states'])*2,
            actualOriginalPrerequisiteReturns=len(native['prerequisites'])*2,stateSha256=fixture.qualified.digest(repr(native).encode())))
    own=set(range(fixture.ADDRESS,fixture.ADDRESS+fixture.CODE,4))
    if not own.issubset(visited):
        raise ValueError('Selector own instruction coverage incomplete: '+repr([hex(a) for a in sorted(own-visited)]))
    cap=fixture.execute(original,fixture.cases()[0],0,budget=1)
    if cap['states'][0]['actualReturn']:
        raise ValueError('Selector exhaustion received return credit')
    report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),fixture=Path(fixture.__file__).name,
        fixtureSha256=sha256(fixture.__file__),entry=entry,realArm7Link=proof,scenarios=len(records),records=records,
        actualOriginalAndCompiledReturns=sum(row['actualOriginalAndCompiledReturns'] for row in records),
        actualOriginalPrerequisiteReturns=sum(row['actualOriginalPrerequisiteReturns'] for row in records),
        actualSeparatelyObservedNestedReturns=dict(sorted(nested.items())),allOwnInstructionAddresses=sorted(own),sourceCredit=0,
        limitations=['Current-artifact source proof only; fresh promoted input closure, full boundary and rejection controls remain required',
            'Real subsystem/object initialization and conditional pending alarm run first; no function/service providers',
            'Existing accepted helper contracts are u32 returns and signed16 count/delay; wrapper raw return words have no assigned application meaning',
            'Callback addresses are zero-credit original bindings; callbacks are not executed and their complete ABI/source remain unclaimed',
            'Disposable VCOUNT/IRQ/MMIO contexts include explicitly synthetic65535; physical display/timing and scene/thread reachability are unproved'])
    destination=ROOT/'evidence/attempts/arm7-lane-alarm-selector-source-20261031.json'
    write_json(destination,report)
    print(dict(report=destination.relative_to(ROOT).as_posix(),sha256=sha256(destination),scenarios=len(records),returns=report['actualOriginalAndCompiledReturns'],sourceCredit=0))


if __name__=='__main__':
    main()
