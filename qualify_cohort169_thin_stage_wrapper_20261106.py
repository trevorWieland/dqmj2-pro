import ast
import copy
import runpy
import sys
from unittest.mock import patch
from project import ROOT, read_json, write_json, sha256
import stage_declared_source_package_v9_20261106 as staging


def main():
    for name, digest in staging.PINS.items():
        assert sha256(ROOT / name) == digest
    original = (ROOT / 'stage_parallel_packet_wave168_v2_20261106.py').read_text(encoding='utf-8')
    results = []
    for cohort, letter in [(169, 'n')]:
        wrapper = f'stage_parallel_packet_wave{cohort}_v2_20261106.py'
        package = f'cohort{cohort}-parallel-wave20261105-{letter}-package.json'
        source = (ROOT / wrapper).read_text(encoding='utf-8')
        reversed_source = source.replace(package, 'cohort168-parallel-wave20261105-m-package.json').replace(
            f"['cohort'] == {cohort}", "['cohort'] == 168")
        assert ast.dump(ast.parse(reversed_source)) == ast.dump(ast.parse(original))
        captured = []
        with patch.object(staging, 'main', side_effect=lambda: captured.append(list(sys.argv))), patch.object(sys, 'argv', [wrapper]):
            runpy.run_path(str(ROOT / wrapper), run_name='__main__')
        assert len(captured) == 1 and captured[0][1:] == [package]
        wrong = copy.deepcopy(read_json(ROOT / package)); wrong['cohort'] = cohort + 1
        with patch.object(staging, 'main') as downstream, patch('project.read_json', return_value=wrong), patch.object(sys, 'argv', [wrapper]):
            try:
                runpy.run_path(str(ROOT / wrapper), run_name='__main__')
            except AssertionError:
                pass
            else:
                raise AssertionError('Wrong package cohort reached staging')
            downstream.assert_not_called()
        results.append(dict(cohort=cohort, wrapper=dict(path=wrapper, sha256=sha256(ROOT / wrapper)),
            exactPackageArgument=package, actualQualifiedV9EntryPointCalledOnce=True,
            onlyPackageAndCohortLiteralChangedFrom168=True, wrongCohortRejectedBeforeDownstream=True))
    write_json(ROOT / 'evidence/verification/cohort169-thin-stage-wrapper-qualification-20261106.json',
        dict(passed=True, sourceCredit=0, actualSharedStagingNotExecuted=True,
            allQualifiedV9UnderlyingSourceCollectorAndStagePinsUnchanged=staging.PINS,
            wrappers=results, generatorSha256=sha256(__file__)))
    print(dict(passed=True, wrappers=1, sourceCredit=0))


if __name__ == '__main__':
    main()
