from project import ROOT,write_json,sha256
from audit_selected_c_initialization_20261031 import worker,CLANG


def main():
    directory=ROOT/'work/initialization-audit-calibration-20261031';directory.mkdir(parents=True,exist_ok=True)
    rows=[]
    for name,body,diagnostic in [
        ('conditional','int sample(int x){int value;if(x)value=1;return value;}\n',True),
        ('initialized','int sample(int x){int value=0;if(x)value=1;return value;}\n',False)]:
        path=directory/(name+'.c');path.write_text(body,encoding='utf-8')
        result=worker((path.relative_to(ROOT).as_posix(),sha256(path)))
        assert result['frontendAccepted'] and bool(result['initializationDiagnostics'])==diagnostic
        rows.append(result)
    report=dict(sourceCredit=0,compilerSha256=sha256(CLANG),generatorSha256=sha256(__file__),controls=rows,passed=True,
        limitations=['Independent frontend diagnostic calibration only; no game/native execution or correctness credit'])
    write_json(ROOT/'evidence/verification/c-initialization-audit-calibration-20261031.json',report)
    print(dict(controls=2,passed=True,sourceCredit=0))


if __name__=='__main__':main()
