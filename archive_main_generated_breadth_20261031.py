import argparse
from project import ROOT,read_json,write_json,sha256,configuration


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stem');args=parser.parse_args()
    report_path=(ROOT/'evidence/attempts'/f'{args.stem}.json').resolve()
    assert report_path.parent==ROOT/'evidence/attempts'
    report=read_json(report_path);assert report['finishedUtc'] and report['sourceCredit']==0
    destination=(ROOT/'generated/drafts'/args.stem).resolve();assert destination.is_relative_to(ROOT/'generated/drafts')
    copied=[]
    for row in report['results']:
        source=row.get('draftSource')
        if not source:continue
        path=(ROOT/source).resolve();assert path.is_relative_to(ROOT/'work') and path.is_file()
        relative=f"{row['mode']}-{int(row['address'],0):08x}/candidate.c";output=destination/relative
        data=path.read_bytes()
        if output.exists():assert output.read_bytes()==data
        else:output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(data)
        copied.append(dict(processor='arm9',module='main',program='',mode=row['mode'],address=row['address'],nativeBytes=row['bytes'],path=output.relative_to(ROOT).as_posix(),sha256=sha256(output),physicalLines=len(data.splitlines()),compilable=row['compilable'],bestSameOffsetBytes=row['bestSameOffsetBytes'],generatedHypothesis=True,sourceCredit=0,compilerAttempts=row.get('attempts',[]),contextContracts=row.get('qualifiedContextContracts',[])))
    output=destination/'manifest.json'
    write_json(output,dict(romSha256=configuration()['romSha256'],generator='archive_main_generated_breadth_20261031.py',generatorSha256=sha256(__file__),inputReport=report_path.relative_to(ROOT).as_posix(),inputReportSha256=sha256(report_path),sourceCredit=0,acceptedRegistryMutated=False,files=copied,limitations=['Generated candidates retain unqualified type, stack-object, boundary, helper ABI and source-semantic assumptions','Compilation and same-offset similarity do not establish executable reconstruction or gameplay correctness','Every acceptance requires individual source review, genuine linking, native-return/memory checks and preservation of earlier matches']))
    print(dict(archivedDrafts=len(copied),nativeBytes=sum(row['nativeBytes'] for row in copied),manifest=output.relative_to(ROOT).as_posix(),sourceCredit=0))


if __name__=='__main__':main()
