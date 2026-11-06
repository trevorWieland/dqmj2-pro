import argparse
import ast
import copy
import runpy
import sys
from unittest.mock import patch
from project import ROOT, read_json, write_json, sha256
import stage_declared_source_package_v9_20261106 as staging


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('configuration'); options = parser.parse_args()
    cfg = read_json(ROOT / options.configuration); cohort = cfg['cohort']; assert cohort >= 171
    for name, digest in staging.PINS.items():
        assert sha256(ROOT / name) == digest
    wrapper, package = cfg['stage'], cfg['name'] + '-package.json'
    baseline_name = 'stage_parallel_packet_wave170_v2_20261106.py'
    baseline_package = 'cohort170-parallel-wave20261105-o-package.json'
    original = (ROOT / baseline_name).read_text(encoding='utf-8')
    candidate = (ROOT / wrapper).read_text(encoding='utf-8')
    reversed_source = candidate.replace(package, baseline_package).replace(f"['cohort'] == {cohort}", "['cohort'] == 170")
    assert ast.dump(ast.parse(reversed_source)) == ast.dump(ast.parse(original))
    calls = []
    with patch.object(staging, 'main', side_effect=lambda: calls.append(list(sys.argv))), patch.object(sys, 'argv', [wrapper]):
        runpy.run_path(str(ROOT / wrapper), run_name='__main__')
    assert len(calls) == 1 and calls[0][1:] == [package]
    wrong = copy.deepcopy(read_json(ROOT / package)); wrong['cohort'] = cohort + 1
    with patch.object(staging, 'main') as downstream, patch('project.read_json', return_value=wrong), patch.object(sys, 'argv', [wrapper]):
        try:
            runpy.run_path(str(ROOT / wrapper), run_name='__main__')
        except AssertionError:
            pass
        else:
            raise AssertionError('Wrong cohort reached actual shared staging')
        downstream.assert_not_called()
    result = dict(passed=True, sourceCredit=0, wrapper=dict(path=wrapper, sha256=sha256(ROOT / wrapper)),
        baseline=dict(path=baseline_name, sha256=sha256(ROOT / baseline_name)), exactPackageArgument=package,
        onlyPackageAndCohortLiteralChanges=True, actualQualifiedV9EntryPointCalledExactlyOnce=True,
        wrongCohortRejectedBeforeDownstream=True, allQualifiedV9UnderlyingPinsUnchanged=staging.PINS,
        actualSharedStagingNotExecuted=True, generatorSha256=sha256(__file__))
    write_json(ROOT / f'evidence/verification/cohort{cohort}-thin-function-queue-stage-v1-20261106.json', result)
    print(dict(passed=True, cohort=cohort, sourceCredit=0))


if __name__ == '__main__':
    main()
