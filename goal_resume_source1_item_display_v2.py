from pathlib import Path
from project import ROOT, read_json, sha256, write_json
import goal_resume_source1_item_display_proof as proof


def main():
    proof.LANE=ROOT/'evidence/lanes/parallel-wave20261106/goal-resume-source-1/item-display-v2'
    proof.WORK=ROOT/'work/goal-resume-20261106/source-1/item-display-v2-proof'
    proof.main()
    path=proof.LANE/'match.json'
    report=read_json(path)
    count=report.pop('functionMatches')
    if count!=len(report['matches']) or count!=1:
        raise ValueError('Item-display function-count schema is inconsistent')
    report['functionMatchesCount']=count
    report['delegatedProducer']=dict(path=report['producer'],sha256=report['producerSha256'])
    report['producer']=Path(__file__).name
    report['producerSha256']=sha256(Path(__file__))
    write_json(path,report)


if __name__=='__main__':
    main()
