from pathlib import Path
import arm7_lane_setting_native_20261031 as fixture
from project import ROOT,sha256,write_json


def main():
    raw=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes()
    body=raw[fixture.ADDRESS-fixture.BASE:fixture.ADDRESS-fixture.BASE+fixture.SIZE]
    records,visited=[],set()
    returns=0
    for seed,case in enumerate(fixture.cases()):
        native=fixture.execute(body,case,seed)
        if any(not state['actualReturn'] or state['fault'] is not None for state in native['states']):
            raise ValueError('Supported setting context did not actually return')
        visited.update(native['visited'])
        returns+=len(native['states'])
        records.append(dict(case=case,actualNativeReturns=len(native['states']),seed=seed,stateSha256=fixture.digest(repr(native).encode())))
    if visited!=set(range(fixture.ADDRESS,fixture.ADDRESS+fixture.CODE,4)):
        raise ValueError('Own setting instruction coverage incomplete')
    unsupported=fixture.execute(body,dict(value=1,pointer=0,passes=1),991)
    cap=fixture.execute(body,fixture.cases()[0],992,budget=1)
    if unsupported['states'][0]['actualReturn'] or unsupported['states'][0]['fault'] is None or cap['states'][0]['actualReturn']:
        raise ValueError('Malformed-pointer/exhaustion context received false supported return credit')
    report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),fixture=Path(fixture.__file__).name,
        fixtureSha256=sha256(fixture.__file__),program='',processor='arm7',module='arm7-main',mode='arm',address=hex(fixture.ADDRESS),bytes=fixture.SIZE,
        inputModuleSha256=fixture.digest(raw),targetSha256=fixture.digest(body),records=records,sourceCredit=0,
        actualNativeReturns=returns,originalAndCompiledReturns=0,allOwnInstructionAddresses=sorted(visited),
        externalReadOnlyPointerBinding=dict(address=hex(fixture.POINTER),kind='synthetically supplied pointer; producer/module ownership unresolved'),
        unsupportedControls=[dict(kind='null-target-pointer',actualReturn=False,fault=unsupported['states'][0]['fault'],returnCredit=0),
            dict(kind='instruction-exhaustion',actualReturn=False,returnCredit=0)],
        limitations=['Native original only; typed candidate is not accepted and frozen standard linker rejects external pointer0380FFF4',
            'Return0 versus5 and ordered stores are raw native behavior, not an assigned device command or application policy',
            'Logical word inputs, synthetic RAM backing and disposable MMIO only; no physical register, device, caller-lifecycle or ordinary reachability claim'])
    path=ROOT/'evidence/attempts/arm7-lane-setting-native-20261031.json'
    write_json(path,report)
    print(dict(report=path.relative_to(ROOT).as_posix(),sha256=sha256(path),scenarios=len(records),actualNativeReturns=returns,sourceCredit=0))


if __name__=='__main__':
    main()
