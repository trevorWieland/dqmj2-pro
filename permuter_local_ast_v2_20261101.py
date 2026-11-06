import copy
import importlib
import re
import sys
import types
from project import ROOT, read_json, sha256

COMMIT = '8556c81d80d1c1af98a858c8f4dc951357f29139'
TOOL = ROOT / ('tools/decomp-permuter-' + COMMIT)
ALLOWED = {'perm_temp_for_expr', 'perm_expand_expr', 'perm_reorder_stmts', 'perm_reorder_decls',
    'perm_cast_simple', 'perm_split_assignment', 'perm_condition', 'perm_commutative',
    'perm_compound_assignment', 'perm_factor_mult', 'perm_factor_shift', 'perm_add_sub', 'perm_inequalities'}
_API = None


def load_api():
    global _API
    if _API is not None:
        return _API
    pin = read_json(ROOT / 'evidence/tools/decomp-permuter-acquisition-20261101.json')
    assert pin['commit'] == COMMIT and pin['independentGitBlobTreeChecksPassed'] and pin['upstreamUnmodified']
    for row in pin['sourceTreeFiles']:
        assert sha256(ROOT / row['path']) == row['sha256'], row['path']
    sys.path.insert(0, str(TOOL))
    package = types.ModuleType('j2p_permuter_local')
    package.__path__ = [str(TOOL / 'src')]
    sys.modules[package.__name__] = package
    api = importlib.import_module('j2p_permuter_local.randomizer')
    ast = importlib.import_module('j2p_permuter_local.ast_util')
    assert not any('.net' in name or '.compiler' in name or '.scorer' in name
        for name in sys.modules if name.startswith(package.__name__))
    _API = api, ast
    return _API


def mutate(text, function, seed, steps=1):
    assert 1 <= steps <= 8
    api, ast = load_api()
    syntax = ast.parse_c(text)
    original = ast.extract_fn(syntax, function)[0]
    ast.normalize_ast(original, syntax)
    weights = {method.__name__: float(method.__name__ in ALLOWED) for method in api.RANDOMIZATION_PASSES}
    randomizer = api.Randomizer(weights, seed)
    syntax = copy.deepcopy(syntax)
    for unused in range(steps):
        randomizer.randomize(syntax, function)
    result = ast.to_c(syntax)
    assert len(result.splitlines()) <= 500
    assert not re.search(r'\b(?:asm|__asm|__asm__|volatile|register)\b', result)
    assert len(re.findall(r'\b' + re.escape(function) + r'\s*\(', result)) == 1
    return result
