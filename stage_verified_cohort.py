import argparse
import ast
import subprocess
from project import ROOT, read_json
from recovery_registry import verify_sources

EXCLUDED = {'build', 'tools', 'deps', 'inputs', 'work', 'extract', 'asm', 'logs', '.git'}
SKIP_KEYS = {'differential', 'cases', 'vectors', 'traces', 'results', 'allExecutionResults', 'allExecutionTraces'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True)
    parser.add_argument('--extra', nargs='*', default=[])
    args = parser.parse_args()
    plan_path = f'evidence/verification/cohort-2026-10-29-{args.cohort}.json'
    plan = read_json(ROOT / plan_path)
    if plan['linksPending']:
        raise ValueError('Cannot stage an unaccepted source cohort')
    verify_sources()
    paths = set()

    def add(relative):
        if not isinstance(relative, str):
            return
        file = (ROOT / relative).resolve()
        if not file.is_relative_to(ROOT) or not file.is_file():
            return
        name = file.relative_to(ROOT).as_posix()
        if name.startswith('evidence/encounter/script-cfg-20261029/'):
            return
        if name.split('/')[0] not in EXCLUDED and file.suffix.lower() in ('.c', '.cpp', '.h', '.inc', '.py', '.json', '.md', '.txt', '.s'):
            paths.add(name)

    def gather(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key in ('source', 'path', 'generator', 'oracleGenerator', 'fixture'):
                    add(item)
                if key in ('additionalFixtureGenerators', 'reproductionCommand'):
                    for token in item if isinstance(item, list) else str(item).split():
                        if isinstance(token, str) and token.endswith('.py'):
                            add(token)
                if key not in SKIP_KEYS:
                    gather(item)
        elif isinstance(value, list):
            for item in value:
                gather(item)

    for relative in [plan_path, f'evidence/verification/cohort{args.cohort}-validation-driver.json', *args.extra, *plan['reports']]:
        if not (ROOT / relative).is_file():
            raise ValueError('Required source/evidence is absent: ' + relative)
        add(relative)
    report_paths = list(dict.fromkeys([*plan['reports'], *plan.get('interpretedReports', []),
                                       *[path for path in args.extra if path.endswith('.json')]]))
    for relative in report_paths:
        add(relative)
        gather(read_json(ROOT / relative))
    registries = [ROOT / 'recovery.json', ROOT / 'interpreted-recovery.json']
    for registry in registries:
        if not registry.is_file():
            continue
        for batch in read_json(registry)['batches']:
            if batch['report'] in report_paths:
                for relative in batch['sourceHashes']:
                    add(relative)
                add(batch['reproduce'][0])
    preference_path = ROOT / 'source-preferences.json'
    if preference_path.is_file():
        add('source-preferences.json')
        for preference in read_json(preference_path)['preferences']:
            add(preference['evidence'])
            migration = read_json(ROOT / preference['evidence'])
            for version in [migration['previous'], migration['preferred']]:
                add(version['source'])
                add(version['report'])

    search = [ROOT, ROOT / 'evidence/application', ROOT / 'evidence/encounter', ROOT / 'nonmatching/encounter', ROOT / 'evidence/save']
    queue, seen = [ROOT / p for p in paths if p.endswith('.py')], set()
    while queue:
        file = queue.pop()
        if file in seen:
            continue
        seen.add(file)
        tree = ast.parse(file.read_text(encoding='utf-8-sig'))
        for node in ast.walk(tree):
            names = [item.name for item in node.names] if isinstance(node, ast.Import) else [node.module] if isinstance(node, ast.ImportFrom) and node.module else []
            for name in names:
                for base in [file.parent, *search]:
                    candidate = base / (name.replace('.', '/') + '.py')
                    if candidate.is_file():
                        add(candidate.relative_to(ROOT).as_posix())
                        queue.append(candidate)
                        break
    from oracle_source_closure_20261031 import collect
    oracle_closure = collect()
    if oracle_closure['missingRequiredPaths']:
        raise ValueError('Registered oracle inputs are missing')
    paths.update(oracle_closure['sourceAndEvidenceHashes'])
    subprocess.run(['git', 'add', '-u'], cwd=ROOT, check=True)
    subprocess.run(['git', 'add', '--pathspec-from-file=-', '--pathspec-file-nul'],
                   input=b''.join(path.encode('utf-8') + bytes([0]) for path in sorted(paths)),
                   cwd=ROOT, check=True)
    print({'cohort': args.cohort, 'closurePaths': len(paths), 'pythonFilesInspected': len(seen)})


if __name__ == '__main__':
    main()
