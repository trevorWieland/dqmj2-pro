from pathlib import Path
from copy import deepcopy
from project import ROOT,read_json,write_json,sha256
from prepare_source_cohort_v2_20261102 import classify_additions


def main():
    report=ROOT/'evidence/matches/main-canvas-clear284-v2-20261102.json'
    rows={i:{**row,'size':row['bytes']}for i,row in enumerate(read_json(report)['matches'])}
    measured=classify_additions(rows,set(rows))
    assert measured==dict(newOrdinaryCFunctions=2,newOrdinaryCBytes=208,newVerifiedOriginalAssemblyFunctions=1,newVerifiedOriginalAssemblyBytes=76)
    controls=[]
    for name in('missing-justification','wrong-language','false-published-assembly','ordinary-C-disguise'):
        wrong=deepcopy(rows)
        if name=='missing-justification':wrong[0].pop('assemblyJustification')
        elif name=='wrong-language':wrong[0]['sourceLanguage']='C'
        elif name=='false-published-assembly':wrong[0]['assemblyJustification']['originalExplicitAsmDeclaration']=False
        else:wrong[0].pop('assemblyJustification');wrong[0]['sourceLanguage']='C'
        try:classify_additions(wrong,set(wrong))
        except AssertionError:controls.append(dict(label=name,rejected=True))
        else:raise AssertionError(name)
    write_json(ROOT/'evidence/verification/source-language-accounting-v2-controls-20261102.json',dict(
        passed=True,sourceCredit=0,generator=Path(__file__).name,generatorSha256=sha256(__file__),measured=measured,
        controls=controls,preparerSha256=sha256(ROOT/'prepare_source_cohort_v2_20261102.py'),
        frozenPriorPreparerUnchanged=True,reproductionCommand='python check_source_language_accounting_v2_20261102.py'))
    print(measured)


if __name__=='__main__':
    main()
