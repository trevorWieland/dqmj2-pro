import json
from pathlib import Path
import arm7_lane_driver_leaves_native_20261030 as fixture
from project import ROOT,sha256,write_json


def main():
    input_path=ROOT/'work/arm7-bulk-20261030/lane-sdk-typed68-01/results.json'
    attempts=json.loads(input_path.read_text())['results']
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    units=[]
    for address,size in fixture.SIZES.items():
        result=next(r for r in attempts if int(r['address'],0)==address)
        row=next(r for r in result['variants'] if r.get('realLink',{}).get('exactLinkedBytes'))
        entry,proof=row['entry'],row['realLink']
        if sha256(ROOT/entry['source'])!=entry['sourceSha256'] or sha256(ROOT/entry['object'])!=entry['objectSha256']:
            raise ValueError('Current compiled source/object differs')
        for item in result['sourceDependencies']:
            if sha256(ROOT/item['path'])!=item['sha256']:
                raise ValueError('Current typed header differs')
        body=Path(proof['cwd'])/'caller.bin'
        if not body.resolve().is_relative_to(ROOT) or sha256(body)!=proof['linkedCallerSha256']:
            raise ValueError('Current real linked product differs or escapes lane')
        original=raw[address-fixture.BASE:address-fixture.BASE+size]
        if original!=body.read_bytes():
            raise ValueError('Full linked driver leaf bytes differ')
        records,visited,returns=[],set(),0
        for seed,case in enumerate(fixture.cases(address)):
            native=fixture.execute(address,original,case,seed)
            source=fixture.execute(address,body.read_bytes(),case,seed)
            if native!=source or any(not x['actualReturn'] or x['fault'] is not None for x in native['states']):
                raise ValueError('Full native/source leaf state or actual return differs')
            visited.update(native['visited'])
            here=len(native['states'])*2
            returns+=here
            records.append(dict(case=case,seed=seed,actualOriginalAndCompiledReturns=here,stateSha256=fixture.digest(repr(native).encode())))
        if not set(range(address,address+size,4)).issubset(visited):
            raise ValueError('Own instruction coverage incomplete')
        cap=fixture.execute(address,original,fixture.cases(address)[0],0,budget=1)
        if cap['states'][0]['actualReturn']:
            raise ValueError('Exhaustion counted as return')
        units.append(dict(address=hex(address),bytes=size,mode='arm',processor='arm7',program='',module='arm7-wram',
            scenarios=len(records),actualOriginalAndCompiledReturns=returns,entry=entry,realArm7Link=proof,records=records,
            allOwnInstructionAddresses=sorted(visited),meaningfulReturnContract='void; incidental R0 receives no result credit',
            independentFullMmioAndUntouchedMemoryModel=True,unsupportedControl=dict(kind='one-instruction-cap',actualReturn=False,returnCredit=0),sourceCredit=0))
    report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),fixture=Path(fixture.__file__).name,
        fixtureSha256=sha256(fixture.__file__),compileReport=input_path.relative_to(ROOT).as_posix(),compileReportSha256=sha256(input_path),
        units=units,actualOriginalAndCompiledReturns=sum(x['actualOriginalAndCompiledReturns'] for x in units),sourceCredit=0,
        limitations=['Actual CPU/MMIO memory effects only; physical sound and peripheral behavior remain unverified',
            'No providers, BIOS, emulation, game-scene or asset-legality claims',
            'Native proof consumes current hash-gated compiler/link products; final source publication still requires fresh source replay and boundary/control acceptance'])
    destination=ROOT/'evidence/attempts/arm7-lane-driver-leaves-native-20261030.json'
    write_json(destination,report)
    print(dict(report=destination.relative_to(ROOT).as_posix(),sha256=sha256(destination),returns=report['actualOriginalAndCompiledReturns'],sourceCredit=0),flush=True)


if __name__=='__main__':
    main()
