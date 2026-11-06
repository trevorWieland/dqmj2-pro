import json
from pathlib import Path
import arm7_lane_child_counter_native_20261031 as fixture
from project import ROOT,sha256,write_json


def main():
    path=ROOT/'work/arm7-bulk-20261030/lane-child-counter76/037fddcc/report.json'
    current=json.loads(path.read_text())
    entry,proof=current['entry'],current['proof']
    if sha256(ROOT/entry['source'])!=entry['sourceSha256'] or sha256(ROOT/entry['object'])!=entry['objectSha256']:
        raise ValueError('Typed child counter source/object changed')
    product=Path(proof['cwd'])/'caller.bin'
    if not product.resolve().is_relative_to(ROOT) or sha256(product)!=proof['linkedCallerSha256']:
        raise ValueError('Current genuine child counter linked body differs')
    raw=(ROOT/entry['binary']).read_bytes()
    original=raw[fixture.ADDRESS-fixture.BASE:fixture.ADDRESS-fixture.BASE+fixture.SIZE]
    rebuilt=product.read_bytes()
    if original!=rebuilt:
        raise ValueError('Typed child counter whole linked body differs')
    records,visited=[],set()
    for seed,case in enumerate(fixture.cases()):
        native=fixture.execute(original,case,seed)
        source=fixture.execute(rebuilt,case,seed)
        if native!=source or len(native['states'])!=case['passes'] or any(not state['actualReturn'] or state['fault'] is not None for state in native['states']):
            raise ValueError('Child counter original/source complete machine/return differs')
        visited.update(native['visited'])
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=len(native['states'])*2,
            stateSha256=fixture.digest(repr(native).encode())))
    own=set(range(fixture.ADDRESS,fixture.ADDRESS+fixture.CODE,4))
    if not own.issubset(visited):
        raise ValueError('Child counter own instruction coverage incomplete')
    cap=fixture.execute(original,fixture.cases()[0],0,budget=1)
    if cap['states'][0]['actualReturn']:
        raise ValueError('Child counter exhaustion received return credit')
    report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),fixture=Path(fixture.__file__).name,
        fixtureSha256=sha256(fixture.__file__),entry=entry,realArm7Link=proof,scenarios=len(records),records=records,
        actualOriginalAndCompiledReturns=sum(row['actualOriginalAndCompiledReturns'] for row in records),
        allOwnInstructionAddresses=sorted(own),sourceCredit=0,
        limitations=['Current-artifact source proof; fresh promoted closure, qualified complete boundaries and rejection controls remain required',
            'Independent signed-word comparison/u32 wrap/ordered-store/NZCV/IRQ model; actual original IRQ helpers execute without providers',
            'Utility child program namespace is independent of host; counter/sample receive no physical timing, frame or scene meaning',
            'No asynchronous interrupt, complete program, BIOS, device or helper-source credit'])
    destination=ROOT/'evidence/attempts/arm7-lane-child-counter-source-20261031.json'
    write_json(destination,report)
    print(dict(report=destination.relative_to(ROOT).as_posix(),sha256=sha256(destination),scenarios=len(records),returns=report['actualOriginalAndCompiledReturns'],sourceCredit=0))


if __name__=='__main__':
    main()
