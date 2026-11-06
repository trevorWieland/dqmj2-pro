from pathlib import Path
from project import ROOT,configuration,write_json,sha256

EXPECTED={
 'extract/arm7/runtime/arm7-main.bin':'ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416',
 'extract/arm7/runtime/arm7-wram.bin':'e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'}


def main():
    config=configuration();assert sha256(config['rom'])==config['romSha256']
    rows=[]
    for name,expected in EXPECTED.items():
        actual=sha256(ROOT/name);assert actual==expected,(name,actual)
        rows.append(dict(path=name,sha256=actual))
    write_json(ROOT/'evidence/verification/arm7-native-runtime-inputs-20261101.json',dict(passed=True,
        sourceCredit=0,generator=Path(__file__).name,generatorSha256=sha256(__file__),
        romSha256=config['romSha256'],verifiedInputs=rows,allNativeHelperBytesRequiredUnchanged=True,
        scope='Independent integrator input gate, including original WRAM used by Counter504 fill oracle'))
    print(dict(verifiedNativeModules=len(rows),passed=True,sourceCredit=0))


if __name__=='__main__':
    main()
