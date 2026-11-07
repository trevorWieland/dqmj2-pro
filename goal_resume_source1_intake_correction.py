from project import ROOT, read_json, sha256, write_json
from recovery_registry import entries


def main():
    lane=ROOT/'evidence/lanes/parallel-wave20261106/goal-resume-source-1/resource-display'
    original=lane/'ready.json'
    ready=read_json(original)
    for pin in ready['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:
            raise ValueError('Frozen source/proof input changed')
    report_path=ROOT/ready['packets'][0]['report']
    report=read_json(report_path)
    rows=entries(report)
    if not rows or any(not row.get('exactAfterDeclaredRelocation') or not row.get('realLink',{}).get('exactCallerBytes') for row in rows):
        raise ValueError('Canonical caller matching/link proof is incomplete')
    count,total=len(rows),sum(row['bytes'] for row in rows)
    if (count,total)!=(1,116) or ready['bytes']!=total:
        raise ValueError('Canonical resource-display extent differs')
    replacement=dict(ready)
    replacement.update(functions=count,bytes=total,matchingCandidateBytes=total,
        sourceCreditPendingIntegrator=total,acceptedSourceCredit=0,
        supersedes=dict(path=original.relative_to(ROOT).as_posix(),sha256=sha256(original)),
        correction='Only intake-summary pending bytes corrected from148 to canonical116. Frozen source, producer, inputs, native/link/behavior/copy evidence and canonical report remain unchanged.')
    replacement['files']=[*ready['files'],dict(path=original.relative_to(ROOT).as_posix(),sha256=sha256(original),role='superseded-intake-metadata'),
        dict(path='goal_resume_source1_intake_correction.py',sha256=sha256(ROOT/'goal_resume_source1_intake_correction.py'),role='metadata-correction-generator')]
    target=lane/'ready-summary-corrected.json'
    write_json(target,replacement)
    write_json(lane.parent/'resource-display-supersession.json',dict(status='superseded-intake-summary-only',sourceCredit=0,
        priorReady=replacement['supersedes'],replacementReady=dict(path=target.relative_to(ROOT).as_posix(),sha256=sha256(target)),
        canonicalReport=dict(path=report_path.relative_to(ROOT).as_posix(),sha256=sha256(report_path)),functions=count,bytes=total))
    print(dict(ready=target.relative_to(ROOT).as_posix(),functions=count,bytes=total,pendingBytes=total,sourceCredit=0),flush=True)


if __name__=='__main__':
    main()
