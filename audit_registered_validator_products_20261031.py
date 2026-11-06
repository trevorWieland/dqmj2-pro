import argparse
import ast
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from strings(child)


def work_product(text):
    clean = text.replace('\\', '/')
    if clean.startswith('work/'):
        result = clean
    elif '/work/' in clean and re.match(r'^[A-Za-z]:/', clean):
        result = 'work/' + clean.split('/work/', 1)[1]
    else:
        return None
    if Path(result).suffix.lower() not in ('.o', '.elf', '.bin', '.lcf', '.ld', '.json'):
        return None
    return result


def module_facts(path):
    tree = ast.parse(path.read_text(encoding='utf-8-sig'))
    paths = sorted({row.value for row in ast.walk(tree) if isinstance(row, ast.Constant)
        and isinstance(row.value, str) and row.value.endswith('.json')
        and row.value.startswith(('evidence/', 'provenance/', 'nonmatching/'))})
    gates = []
    calls = []
    for row in ast.walk(tree):
        if not isinstance(row, ast.Call):
            continue
        expression = ast.unparse(row.func)
        if re.search(r'\.(?:main|build|publish|replay)$', expression):
            calls.append({'line': row.lineno, 'call': expression})
        if not row.args or not re.search(r'(?:verify|check|current|hash|digest)', expression, re.I):
            continue
        first = ast.unparse(row.args[0])
        if re.search(r'\[.(?:object|probeObject|objectPath|linkedElf|lcf).\]|caller\.bin|linked\.elf', first):
            gates.append({'line': row.lineno, 'call': expression, 'argument': first})
    imports = []
    for row in tree.body:
        if isinstance(row, ast.Import):
            imports.extend(item.name for item in row.names)
        elif isinstance(row, ast.ImportFrom) and row.module:
            imports.append(row.module)
    return {'path': path.name, 'sha256': digest(path), 'literalJsonInputsOrOutputs': paths,
        'productChecks': sorted(gates, key=lambda item: item['line']),
        'producerOrMainCalls': sorted(calls, key=lambda item: item['line']), 'imports': imports}


def commands(registry):
    found = []
    for kind in ('batches', 'oracles'):
        for index, row in enumerate(registry.get(kind, [])):
            command = row.get('reproduce', [])
            if isinstance(command, list) and command:
                found.append({'kind': kind, 'index': index, 'report': row.get('report'), 'argv': command})
    return found


def audit(repository, cold, output):
    registry_path = repository / 'recovery.json'
    registry = json.loads(registry_path.read_text())
    all_commands = commands(registry)
    registered_scripts = {Path(text).name for row in all_commands for text in row['argv'] if isinstance(text, str) and text.endswith('.py')}
    module_cache, json_cache = {}, {}

    def facts(name):
        if name not in module_cache:
            module_cache[name] = module_facts(repository / name)
        return module_cache[name]

    def report(name):
        if name not in json_cache:
            p = repository / name
            try:
                if p.stat().st_size > 8 * 1024 * 1024:
                    json_cache[name] = {'largeReportWithheld': p.stat().st_size}
                else:
                    payload = json.loads(p.read_text())
                    generated, references = set(), set()
                    for text in strings(payload):
                        product = work_product(text)
                        if product:
                            generated.add(product)
                        if text.startswith(('evidence/', 'provenance/')) and text.endswith('.json'):
                            references.add(text)
                    json_cache[name] = {'generator': payload.get('generator') if isinstance(payload, dict) else None,
                        'products': sorted(generated), 'references': sorted(references), 'sha256': digest(p)}
            except (OSError, ValueError):
                json_cache[name] = None
        return json_cache[name]

    rows = []
    for command in all_commands:
        if command['kind'] != 'oracles':
            continue
        entrypoints = [text for text in command['argv'] if isinstance(text, str) and text.endswith('.py') and (repository / text).is_file()]
        modules = set(entrypoints)
        for name in list(modules):
            for imported in facts(name)['imports']:
                candidate = imported.replace('.', '/') + '.py'
                if (repository / candidate).is_file() and (candidate.startswith(('validate_', 'verify_', 'replay_')) or candidate.endswith('_sources.py')):
                    modules.add(candidate)
        inputs = set()
        for name in modules:
            inputs.update(facts(name)['literalJsonInputsOrOutputs'])
        if command['report']:
            inputs.add(command['report'])
        checks = [{'module': name, **item} for name in sorted(modules) for item in facts(name)['productChecks']]
        if not checks:
            inputs = set()
        for name in list(inputs):
            payload = report(name)
            if payload is not None:
                for text in payload.get('references', []):
                    if (repository / text).is_file():
                        inputs.add(text)
        products, producers, source_reports, withheld = set(), set(), [], []
        for name in sorted(inputs):
            payload = report(name)
            if payload is None:
                continue
            if payload.get('largeReportWithheld'):
                withheld.append({'path': name, 'bytes': payload['largeReportWithheld']})
                continue
            generated = payload['products']
            if generated:
                products.update(generated)
                producer = payload.get('generator') if isinstance(payload, dict) else None
                if isinstance(producer, str):
                    producers.add(producer)
                source_reports.append({'path': name, 'sha256': payload['sha256'], 'generator': producer, 'workProducts': len(generated)})
        missing = sorted(name for name in products if not (cold / name).is_file())
        unmatched = sorted(name for name in producers if name.endswith('.py') and name not in registered_scripts)
        if missing and checks and unmatched:
            status = 'requires-producer-order-review'
        elif missing and checks:
            status = 'missing-products-with-registered-producer-or-indirect-regeneration'
        elif missing:
            status = 'missing-products-no-direct-object-check-recognized'
        elif not checks:
            status = 'no-direct-product-gate-recognized'
        elif withheld:
            status = 'large-reports-require-targeted-review'
        else:
            status = 'no-missing-products-found'
        rows.append({**command, 'status': status, 'scannedModules': [facts(name) for name in sorted(modules)],
            'referencedGeneratedReports': source_reports, 'directProductChecks': checks,
            'largeReportsWithheld': withheld,
            'producersNotDirectlyRegistered': unmatched, 'referencedWorkProductCount': len(products),
            'missingColdWorkProducts': missing})
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__)),
        'registry': str(registry_path), 'registrySha256': digest(registry_path), 'readOnlyColdCheckout': str(cold),
        'actualInvocationCwd': str(Path.cwd()), 'registeredCommands': len(all_commands), 'oraclesAudited': len(rows),
        'statusCounts': {key: sum(row['status'] == key for row in rows) for key in sorted({row['status'] for row in rows})},
        'oracles': rows, 'sourceAcceptanceCredit': 0,
        'limitations': ['Static AST and JSON-reference audit identifies candidates, not proof that every missing product is read on a supported validation path',
            'Registered-producer presence alone does not prove execution order or all indirect dependency closures',
            'Cold checkout was read only; already successful earlier commands may have created products there',
            'JSON reports larger than 8 MiB are explicitly withheld for targeted review; reports without recognized direct product gates are not parsed',
            'Dynamic imports, computed report names and indirect product-check helpers require targeted follow-up']}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'report': str(output), 'sha256': digest(output), 'oraclesAudited': len(rows), 'statusCounts': result['statusCounts']}), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repository', required=True, type=Path)
    parser.add_argument('--cold-checkout', required=True, type=Path)
    parser.add_argument('--output', type=Path, default=ROOT / 'evidence/verification/registered-validator-products-audit-20261031.json')
    args = parser.parse_args()
    audit(args.repository.resolve(), args.cold_checkout.resolve(), args.output.resolve())


if __name__ == '__main__':
    main()
