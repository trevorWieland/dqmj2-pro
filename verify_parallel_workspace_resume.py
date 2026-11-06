from copy import deepcopy
from project import ROOT, write_json
from resume_parallel_workspace_gate import validate


def main():
    failed = dict(state='failed', steps=[dict(command=['original.py'], exitCode=0) for _ in range(15)]
        + [dict(command=['verify_workspace.py'], exitCode=1)])
    relocation = dict(originalDiagnosticsPreserved=True, matchedSourceInputsChanged=False)
    validate(failed, relocation)
    controls = [dict(name='only-final-workspace-gate-resumes', passed=True)]
    cases = []
    value = deepcopy(failed)
    value['state'] = 'running'
    cases.append(('running-pipeline', value, relocation))
    value = deepcopy(failed)
    value['steps'].pop()
    cases.append(('incomplete-gates', value, relocation))
    value = deepcopy(failed)
    value['steps'][14]['exitCode'] = 1
    cases.append(('earlier-integrity-failure', value, relocation))
    value = deepcopy(failed)
    value['steps'][15]['command'] = ['integrate.py']
    cases.append(('module-failure-cannot-resume-as-policy', value, relocation))
    value = deepcopy(failed)
    value['steps'][15]['exitCode'] = 0
    cases.append(('no-failed-gate', value, relocation))
    cases.append(('changed-matching-inputs', failed, dict(relocation, matchedSourceInputsChanged=True)))
    cases.append(('lost-diagnostics', failed, dict(relocation, originalDiagnosticsPreserved=False)))
    for name, driver, move in cases:
        try:
            validate(driver, move)
        except ValueError:
            controls.append(dict(name=name, rejected=True))
        else:
            raise AssertionError('Unsafe workspace-only resume accepted: ' + name)
    write_json(ROOT / 'evidence/verification/parallel-wave20261102/workspace-resume-controls.json',
        dict(passed=True, sourceCredit=0, controls=controls, originalAcceptanceGatesRemoved=False))
    print(dict(passed=True, controls=len(controls)))


if __name__ == '__main__':
    main()
