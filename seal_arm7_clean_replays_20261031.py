import ast
import hashlib
import io
import json
from pathlib import Path
import tokenize

ROOT = Path(__file__).resolve().parent
FILES = [
    'replay_arm7_seq_main_proposed_clean_20261031.py',
    'replay_arm7_child_counter_clean_20261031.py',
    'audit_registered_validator_products_20261031.py',
    'validate_registered_validator_product_audit_20261031.py',
    'seal_arm7_clean_replays_20261031.py',
    'docs/2026-10-31-arm7-clean-proposed-and-duplicate-replays.md',
    'evidence/verification/arm7-seq-main-proposed-clean-replay-20261031.json',
    'evidence/verification/arm7-seq-main-proposed-clean-replay-first-20261031.json',
    'evidence/verification/arm7-child-counter-clean-replay-20261031.json',
    'evidence/verification/arm7-child-counter-clean-replay-first-20261031.json',
    'evidence/verification/registered-validator-products-audit-20261031.json',
    'evidence/verification/registered-validator-products-clean-x-audit-20261031.json',
    'evidence/verification/registered-validator-product-audit-controls-20261031.json',
    'evidence/attempts/arm7-seq-proposed-replay-lane-input-20261031.json',
    'evidence/attempts/registered-validator-audit-memory-limit-20261031.json',
    'evidence/attempts/registered-validator-audit-first-source-20261031.py.txt',
    'evidence/attempts/arm7-child-counter-replay-first-format-source-20261031.py.txt',
    'nonmatching/arm7-bulk/20261030/seq-main-final01/native_arm7_wram_037fff54.c',
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def constants(name, key):
    tree = ast.parse((ROOT / name).read_text())
    node = next(row for row in tree.body if isinstance(row, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == key for target in row.targets))
    return ast.literal_eval(node.value)


def main():
    required, alternatives = {}, {}
    for script in FILES[:2]:
        for name, expected in constants(script, 'FROZEN').items():
            if isinstance(expected, list):
                if sha(ROOT / name) not in expected:
                    raise ValueError('Known historical metadata hash differs: ' + name)
                alternatives[name] = expected
            else:
                required[name] = expected
        record_name = 'evidence/verification/' + ('arm7-seq-main-proposed' if 'seq_main' in script else 'arm7-child-counter') + '-clean-replay-20261031.json'
        proof = json.loads((ROOT / record_name).read_text())
        if proof['generatorSha256'] != sha(ROOT / script) or not proof['allPassed']:
            raise ValueError('Final replay does not pin the current wrapper')
        if not proof['initialWorkDirectoryEmpty'] or proof['copiedCachedProducts'] or proof['additionalFunctionOrByteCredit'] != 0:
            raise ValueError('Fresh output/source scope differs')
        if proof['frozenValidatorControls'] != 36 or len(proof['wrapperControls']) != 4:
            raise ValueError('Expected frozen and wrapper controls absent')
        if proof['actualInvocationCwd'] == str(ROOT):
            raise ValueError('Final replay must have an unrelated invocation directory')
    for name in list(required):
        if not name.endswith('/generator-pins.json'):
            continue
        pins = json.loads((ROOT / name).read_text())
        for row in pins['files']:
            prior = required.setdefault(row['path'], row['sha256'])
            if prior != row['sha256']:
                raise ValueError('Conflicting frozen baseline dependency')
    for profile in (
        'nonmatching/arm7-bulk/20261030/seq-main-final01/closure.json',
        'nonmatching/arm7-bulk/20261031/lane-child-counter-final/closure.json',
    ):
        for row in json.loads((ROOT / profile).read_text())['matches']:
            required[row['source']] = row['sourceSha256']
            required[row['compiler']] = row['compilerSha256']
            required[row['binary']] = row['inputModuleSha256']
            for dependency in row.get('sourceDependencies', []):
                required[dependency['path']] = dependency['sha256']
    for name, expected in required.items():
        if sha(ROOT / name) != expected:
            raise ValueError('Existing pinned input differs: ' + name)
    for name in FILES:
        path = ROOT / name
        if name.startswith(('work/', 'inputs/', 'tools/')) or not path.is_file():
            raise ValueError('Invalid source-only transport file: ' + name)
        if path.suffix == '.py':
            code = path.read_text()
            if len(code.splitlines()) > 500 or any(row.type == tokenize.COMMENT for row in tokenize.generate_tokens(io.StringIO(code).readline)):
                raise ValueError('Authored Python source policy differs: ' + name)
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': sha(Path(__file__)),
        'files': [{'path': name, 'sha256': sha(ROOT / name), 'bytes': (ROOT / name).stat().st_size} for name in FILES],
        'requiredExistingPinnedFiles': [{'path': name, 'sha256': value} for name, value in sorted(required.items())],
        'historicalMetadataAlternativesLeftInPlace': [{'path': name, 'sha256Alternatives': value} for name, value in sorted(alternatives.items())],
        'reproduce': [['replay_arm7_seq_main_proposed_clean_20261031.py'], ['replay_arm7_child_counter_clean_20261031.py']],
        'newReconstructedFunctions': 0, 'newReconstructedBytes': 0, 'cachedGeneratedProductsTransported': False,
        'sharedRegistryConfigLedgerPreferenceEdits': False, 'allPassed': True}
    output = ROOT / 'provenance/arm7-clean-replays-handoff-20261031.json'
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'manifest': output.relative_to(ROOT).as_posix(), 'sha256': sha(output),
        'transportFiles': len(FILES), 'existingPinnedFiles': len(required), 'allPassed': True}), flush=True)


if __name__ == '__main__':
    main()
