import json
from pathlib import Path
import arm7_lane_setting_native_20261031 as fixture
from project import ROOT,sha256,write_json


def main():
    link_report=ROOT/'work/arm7-bulk-20261030/lane-main-setting-qualified/027e8ec8/report.json'
    report=json.loads(link_report.read_text())
    entry,proof=report['entry'],report['proof']
    if sha256(ROOT/entry['source'])!=entry['sourceSha256'] or sha256(ROOT/entry['object'])!=entry['objectSha256']:
        raise ValueError('Typed setting source/immutable object differs')
    product=Path(proof['cwd'])/'caller.bin'
    if not product.resolve().is_relative_to(ROOT) or sha256(product)!=proof['linkedCallerSha256']:
        raise ValueError('Current genuine linked setting body differs')
    raw=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes()
    original=raw[fixture.ADDRESS-fixture.BASE:fixture.ADDRESS-fixture.BASE+fixture.SIZE]
    rebuilt=product.read_bytes()
    if original!=rebuilt:
        raise ValueError('Complete typed setting MW-linked bytes differ')
    records,visited=[],set()
    for seed,case in enumerate(fixture.cases()):
        native=fixture.execute(original,case,seed)
        source=fixture.execute(rebuilt,case,seed)
        if native!=source or any(not state['actualReturn'] or state['fault'] is not None for state in native['states']):
            raise ValueError('Typed setting original/source full state, ordered reads/writes or actual return differs')
        visited.update(native['visited'])
        records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=len(native['states'])*2,
            originalAndCompiledStateSha256=fixture.digest(repr(native).encode())))
    if visited!=set(range(fixture.ADDRESS,fixture.ADDRESS+fixture.CODE,4)):
        raise ValueError('Typed setting own instruction coverage incomplete')
    result=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),fixture=Path(fixture.__file__).name,
        fixtureSha256=sha256(fixture.__file__),entry=entry,realArm7Link=proof,records=records,scenarios=len(records),
        actualOriginalAndCompiledReturns=sum(row['actualOriginalAndCompiledReturns'] for row in records),sourceCredit=0,
        limitations=['Current-artifact paired proof only; fresh promoted source/build, full boundary and rejection-control closure remain required',
            'Original linker refusal preserved; separately named narrow policy uses measured descriptor-produced absolute pointer word, not module BSS',
            'No assigned device-command meaning, physical hardware, natural scene/thread or complete-constructor return claim'])
    destination=ROOT/'evidence/attempts/arm7-lane-setting-source-20261031.json'
    write_json(destination,result)
    print(dict(report=destination.relative_to(ROOT).as_posix(),sha256=sha256(destination),scenarios=len(records),actualOriginalAndCompiledReturns=result['actualOriginalAndCompiledReturns'],sourceCredit=0))


if __name__=='__main__':
    main()
