import ast
import copy
from project import ROOT, write_json, sha256
from qualified_source_selection_guard_20261106 import verify


def normalize(tree):
    tree = copy.deepcopy(tree)
    removed = [0, 0, 0]
    tree.body = [node for node in tree.body if not (
        isinstance(node, ast.ImportFrom) and node.module == 'qualified_source_selection_guard_20261106')]
    for function in tree.body:
        if isinstance(function, ast.FunctionDef) and function.name == 'main':
            kept = []
            for node in function.body:
                if isinstance(node, ast.Assign) and len(node.targets) == 1:
                    target = node.targets[0]
                    if isinstance(target, ast.Name) and target.id == 'selection_delegation':
                        removed[0] += 1
                        continue
                    if isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name) and target.value.id == 'result' and isinstance(target.slice, ast.Constant) and target.slice.value == 'sourceSelectionDelegation':
                        removed[1] += 1
                        continue
                kept.append(node)
            function.body = kept
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and node.value == 'verify_source_selection_v2_20261106.py':
            node.value = 'verify_source_selection.py'
            removed[2] += 1
    assert removed == [1, 1, 1]
    return ast.dump(tree, include_attributes=False)


def main():
    delegation = verify()
    old = ast.dump(ast.parse((ROOT / 'run_source_cohort_20261101.py').read_text(encoding='utf-8')), include_attributes=False)
    new = ast.parse((ROOT / 'run_source_cohort_v2_20261106.py').read_text(encoding='utf-8'))
    assert normalize(new) == old
    controls = []
    changed = copy.deepcopy(new)
    next(node for node in changed.body if isinstance(node, ast.FunctionDef) and node.name == 'main').body.append(ast.parse('steps = []').body[0])
    assert normalize(changed) != old
    controls.append('removed-or-altered-shared-pipeline-detected')
    changed = copy.deepcopy(new)
    for node in ast.walk(changed):
        if isinstance(node, ast.Constant) and node.value == 'verify_workspace.py':
            node.value = 'unqualified-workspace.py'
    assert normalize(changed) != old
    controls.append('changed-original-workspace-exception-detected')
    routes = []
    for prior, current in [('25', '28'), ('27', '29')]:
        old_name, new_name = f'run_next_source_package_v{prior}_20261106.py', f'run_next_source_package_v{current}_20261106.py'
        restored = (ROOT / new_name).read_text(encoding='utf-8').replace('v' + current, 'v' + prior).replace('run_source_cohort_v2_20261106.py', 'run_source_cohort_20261101.py')
        assert ast.dump(ast.parse(restored)) == ast.dump(ast.parse((ROOT / old_name).read_text(encoding='utf-8')))
        routes.append(dict(original=old_name, qualified=new_name, originalSha256=sha256(ROOT / old_name), qualifiedSha256=sha256(ROOT / new_name)))
    write_json(ROOT / 'evidence/verification/qualified-source-selection-stage-routing-20261106.json',
        dict(passed=True, sourceCredit=0, delegation=delegation, exactOriginalDriverASTAfterReversingOneRoutingChangeAndRemovingGuardMetadata=True,
             originalSixteenStageOrderFlagsFailureHandlingAndManifestAssertionsPreserved=True,
             originalDriverSha256=sha256(ROOT / 'run_source_cohort_20261101.py'),
             newDriverSha256=sha256(ROOT / 'run_source_cohort_v2_20261106.py'), controls=controls,
             continuationRoutes=routes, generatorSha256=sha256(__file__)))
    print(dict(passed=True, controls=len(controls), qualifiedRoutes=len(routes), sourceCredit=0))


if __name__ == '__main__':
    main()
