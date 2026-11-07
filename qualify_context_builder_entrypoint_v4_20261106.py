import ast
import runpy
import sys
import types
import uuid
from unittest.mock import patch
import build_lock
from project import ROOT, write_json, sha256


def main():
    work = ROOT / 'work/context-builder-v4-cli-controls' / uuid.uuid4().hex[:12]
    work.mkdir(parents=True)
    cases = []
    for value in [0, 1, 'exception']:
        module = types.ModuleType('build_modules')
        originals = {}
        for name in ['collect_units', 'prepare_units', 'split_symbol']:
            originals[name] = lambda *args, **kwargs: None
            setattr(module, name, originals[name])
        def fake_main():
            assert module.split_symbol is not originals['split_symbol']
            try:
                with build_lock.accepted_build():
                    raise AssertionError('Actual nested OS lock was incorrectly admitted')
            except RuntimeError as error:
                assert 'Another accepted module build is active' in str(error)
            if value == 'exception':
                raise ValueError('Intentional original-main exception')
            return value
        module.main = fake_main
        with patch.object(build_lock, 'ROOT', work / str(value)), patch.dict(sys.modules, {'build_modules': module}):
            try:
                runpy.run_path(str(ROOT / 'build_modules_context_v4_20261106.py'), run_name='__main__')
            except SystemExit as error:
                assert value != 'exception' and error.code == value
            except ValueError as error:
                assert value == 'exception' and str(error) == 'Intentional original-main exception'
            else:
                raise AssertionError('Original main return/exception did not propagate')
            assert all(getattr(module, name) is original for name, original in originals.items())
            with build_lock.accepted_build():
                pass
        cases.append(dict(originalMain=value, actualOsLockRejectsConcurrentBuild=True, cleanupAndPropagationPassed=True))
    old = (ROOT / 'integrate_context_v3_20261106.py').read_text(encoding='utf-8')
    new = (ROOT / 'integrate_context_v4_20261106.py').read_text(encoding='utf-8')
    assert ast.dump(ast.parse(old)) == ast.dump(ast.parse(new.replace('build_modules_context_v4_20261106', 'build_modules_context_v3_20261106')))
    names = ['build_modules_context_v4_20261106.py', 'integrate_context_v4_20261106.py',
        'mb_register_module_route_v1_20261106.py', 'qualified_context_builder_entrypoint_v4_20261106.py']
    write_json(ROOT / 'evidence/verification/context-builder-v4-cli-entrypoint-qualification-20261106.json',
        dict(passed=True, sourceCredit=0, actualOsLockExitAndExceptionCleanupPassed=True, cases=cases,
            originalIntegrationAstEqualExceptBuilderEntryPoint=True, allOriginalIntegrationChecksPreserved=True,
            qualifiedHashes={name: sha256(ROOT / name) for name in names}, productionAdopted=False,
            generatorSha256=sha256(__file__)))
    print(dict(passed=True, actualOsLockAndCleanupCases=3, originalIntegrationChecksPreserved=True))


if __name__ == '__main__':
    main()
