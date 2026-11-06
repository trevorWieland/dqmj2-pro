from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
import match_ov000_latch786_20261101 as native

ORIGINAL=ROOT/'evidence/matches/ov000-20261101-latch786-zero-credit.json'
REPORT=ROOT/'evidence/matches/ov000-latch786-registered-shape-20261102.json'


def document():
    report=read_json(ORIGINAL);row=dict(report['candidate'])
    assert report['candidateNewFunctions']==report['candidateNewBytes']==0
    assert report['pairs']==496 and report['actualReturns']==992 and row['bytes']==1460
    assert sha256(ROOT/row['source'])==row['sourceSha256']
    row.update(genuineLinkComparison=report['genuineLinkComparison'],sourceOnlyCompilerInput=True,
     originalObjectScaffolding=False,sourceLanguage='C',newFunctionCredit=0,newByteCredit=0)
    dependencies=[dict(path=ORIGINAL.relative_to(ROOT).as_posix(),sha256=sha256(ORIGINAL))]
    dependencies.extend(item['trace']for item in report['results'])
    dependencies.append(dict(path=native.SOURCE.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(native.SOURCE.with_name('context.h'))))
    write_json(REPORT,dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),
     romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov000',moduleSha256=report['moduleSha256'],
     matches=[row],candidateNewFunctions=0,candidateNewBytes=0,existingSourceAlternativeBytes=1460,
     oracle=dict(actualTopReturns=992,actualNativeDependencyReturnsSeparate=report['nativeDependencyActualReturns'],
      providedCallsSeparate=report['providedCalls'],observedOwnCodeBytes=report['observedOwnCodeBytes'],
      preparationActualReturnsSeparate=report['preparationActualReturns']),replayDependencies=dependencies,
     reproductionCommand='python match_ov000_latch786_registration_20261102.py',limitations=report['limits']))
    print('786 normalized registration shape; unchanged source body and1460bytes, zero new coverage')


def main():
    native.main();document()


if __name__=='__main__':
    main()
