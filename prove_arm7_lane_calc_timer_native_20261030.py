import json
from pathlib import Path
import arm7_lane_calc_timer_native_20261030 as fixture
from project import ROOT,sha256,write_json


def main():
    path=ROOT/'work/arm7-bulk-20261030/lane-sdk-typed68-01/results.json'
    rows=json.loads(path.read_text())['results']
    unit=next(x for x in rows if int(x['address'],0)==fixture.ADDRESS)
    row=next(x for x in unit['variants'] if x.get('realLink',{}).get('exactLinkedBytes'))
    entry,proof=row['entry'],row['realLink']
    if sha256(ROOT/entry['source'])!=entry['sourceSha256'] or sha256(ROOT/entry['object'])!=entry['objectSha256']:
        raise ValueError('Current typed timer source/object differs')
    for item in unit['sourceDependencies']:
        if sha256(ROOT/item['path'])!=item['sha256']:
            raise ValueError('Current timer source include closure differs')
    product=Path(proof['cwd'])/'caller.bin'
    if not product.resolve().is_relative_to(ROOT) or sha256(product)!=proof['linkedCallerSha256']:
        raise ValueError('Current genuine linked timer differs')
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    original=raw[fixture.ADDRESS-fixture.BASE:fixture.ADDRESS-fixture.BASE+fixture.SIZE]
    rebuilt=product.read_bytes()
    if original!=rebuilt:
        raise ValueError('Full linked timer source range differs')
    records,visited=[],set()
    for seed,case in enumerate(fixture.cases()):
        native=fixture.execute(original,case,seed)
        source=fixture.execute(rebuilt,case,seed)
        if native!=source or not native['actualReturn'] or native['fault'] is not None:
            raise ValueError('Timer original/source full machine or supported return differs')
        visited.update(native['visited'])
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=2,stateSha256=fixture.digest(repr(native).encode())))
    own=set(range(fixture.ADDRESS,fixture.ADDRESS+fixture.CODE,4))
    if not own.issubset(visited):
        raise ValueError('Timer instruction coverage incomplete: '+repr([hex(x) for x in sorted(own-visited)]))
    unsupported=fixture.execute(original,dict(fixture.cases()[0],service=None),991)
    if unsupported['actualReturn'] or unsupported['externalFailure'] is None:
        raise ValueError('Missing original BIOS received false return credit')
    cap=fixture.execute(original,fixture.cases()[0],1,budget=1)
    if cap['actualReturn']:
        raise ValueError('Timer exhaustion received return credit')
    report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),fixture=Path(fixture.__file__).name,fixtureSha256=sha256(fixture.__file__),
        entry=entry,realArm7Link=proof,scenarios=len(records),syntheticServiceOriginalAndCompiledReturns=len(records)*2,
        actualOriginalVeneerReturns=len(records)*2,originalBiosExecutionCredit=0,sourceCredit=0,records=records,
        ownInstructionAddresses=sorted(own),unsupportedControls=[dict(kind='unprovided-original-bios',actualReturn=False,returnCredit=0),dict(kind='instruction-cap',actualReturn=False,returnCredit=0)],
        limitations=['Only R0 is replaced at the measured original Thumb SVC27; original veneer returns normally; no BIOS input is sought or executed',
            'Synthetic service input0..767/output0..65535 does not establish actual BIOS table contents or clobbers',
            'The independent model checks full signed timer words, unsigned64 multiplication and bounded defined shifts',
            'Right-shift counts64 or greater, extreme normalization loops, game assets and device behavior remain outside this source-domain proof'])
    destination=ROOT/'evidence/attempts/arm7-lane-calc-timer-native-20261030.json'
    write_json(destination,report)
    print(dict(report=destination.relative_to(ROOT).as_posix(),sha256=sha256(destination),scenarios=len(records),syntheticReturns=len(records)*2,sourceCredit=0),flush=True)


if __name__=='__main__':
    main()
