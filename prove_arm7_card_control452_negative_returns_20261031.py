import json
from pathlib import Path
import match_arm7_lane_card_control_20261031 as matcher
from project import ROOT,sha256,write_json
VALIDATOR_SHA='89c30b0501bea4a0c05ad50388ad4e30d30ac96bc62837432b183c3f9a8e3474'
REPORT='evidence/verification/arm7-lane-card-control452-controls-20261031.json'


def verify(name,pin):
    path=(ROOT/name).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file() or sha256(path)!=pin:raise ValueError('Current negative return input differs: '+str(name))
    return path


def main():
    report=json.loads((ROOT/REPORT).read_text())
    verify('validate_arm7_lane_card_control_20261031.py',VALIDATOR_SHA)
    if report['generatorSha256']!=VALIDATOR_SHA or not report['allPassed'] or len(report['controls'])!=44:
        raise ValueError('Frozen 44-control proof differs')
    rows=[];pins=json.loads(matcher.PROFILE.read_text())['matches']
    for index,record in enumerate(report['negativeRuntimeLinks']):
        pin=pins[index];address=int(pin['address'],0);directory=(ROOT/record['cwd']).resolve()
        directory.relative_to(matcher.WORK.resolve());bad=verify(directory/'caller.bin',record['linkedSha256']).read_bytes()
        verify(directory/'linked.elf',record['linkedElfSha256']);verify(directory/'unit.lcf',record['lcfSha256'])
        if len(bad)!=pin['bytes'] or matcher.digest(bad)==pin['targetSha256']:raise ValueError('Wrong C negative is not a complete changed linked product')
        fixture=matcher.fixture.receiver if index==3 else matcher.fixture.normal
        if index==0:case=dict(old=0,new=4,swap=True)
        elif index==1:case=dict(control=0x00801fff,received=0xdeadbeef)
        elif index==2:case=dict(flags=0,callback=0,argument=0)
        else:case=dict(tag=11,enabled=1,phase=0,request=0,data=16,flags=0,other=False)
        machine=fixture.setup(address,bad,case,0)
        arguments=[case['tag'],case['data'],case['enabled']] if index==3 else machine['args']
        execution=machine['invoke'](address,arguments,True,20000)
        if not execution['actualReturn']:raise ValueError('Wrong compiled C did not actually return before its independent model')
        try:fixture.execute(address,bad,case,0)
        except ValueError as error:reason=str(error)
        else:raise ValueError('Wrong C unexpectedly passed its independent model')
        rows.append(dict(name=record['name'],address=pin['address'],linkedSha256=record['linkedSha256'],case=case,executionBeforeIndependentModel=execution,
            independentModelRejected=True,reason=reason,sourceCredit=0))
    output=ROOT/'evidence/verification/arm7-card-control452-negative-returns-20261031.json'
    write_json(output,dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),controlReport=REPORT,controlReportSha256=sha256(ROOT/REPORT),
        controls=rows,actualWrongCompiledSourceReturns=len(rows),modelRejections=len(rows),allPassed=len(rows)==4,sourceCredit=0))
    print(dict(report=output.relative_to(ROOT).as_posix(),sha256=sha256(output),actualWrongCNormalReturns=len(rows),allPassed=True))


if __name__=='__main__':main()
