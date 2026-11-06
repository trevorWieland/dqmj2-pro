import ast
import subprocess
import sys
from pathlib import Path
from project import ROOT, read_json, sha256, write_json

SEARCH = [ROOT, ROOT / 'evidence/application', ROOT / 'evidence/encounter', ROOT / 'nonmatching/encounter', ROOT / 'evidence/save']


def code_closure(paths):
    pending = [(ROOT / path).resolve() for path in paths]
    found = set()
    while pending:
        path = pending.pop()
        if path in found:
            continue
        if not path.is_relative_to(ROOT) or not path.is_file() or path.suffix != '.py':
            raise ValueError('Invalid authored replay code: ' + str(path))
        found.add(path)
        tree = ast.parse(path.read_text(encoding='utf-8-sig'))
        for node in ast.walk(tree):
            names = [x.name for x in node.names] if isinstance(node, ast.Import) else [node.module] if isinstance(node, ast.ImportFrom) and node.module else []
            for name in names:
                for base in [path.parent, *SEARCH]:
                    candidate = base / (name.replace('.', '/') + '.py')
                    if candidate.is_file():
                        if candidate.relative_to(ROOT).parts[0] in ('deps', 'tools', 'work'):
                            break
                        pending.append(candidate.resolve())
                        break
    return sorted(path.relative_to(ROOT).as_posix() for path in found)


def seal(relative, producer):
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT / 'evidence/matches'):
        raise ValueError('Invalid report path')
    document = read_json(path)
    old_hash = sha256(path)
    count = document.get('functionMatches')
    if count is not None and not isinstance(count, list):
        if not isinstance(count, int) or count != len(document.get('matches', [])):
            raise ValueError('Ambiguous function-match summary')
        document['functionMatchesCount'] = document.pop('functionMatches')
    hashes = {row['path']: row['sha256'] for row in document.get('generatorSources', [])}
    declared = document.get('replayDependencies', [])
    for row in declared:
        target = (ROOT / row['path']).resolve()
        if not target.is_relative_to(ROOT) or sha256(target) != row['sha256']:
            raise ValueError('Stale declared replay input: ' + row['path'])
    seeds = [producer[0], Path(__file__).name]
    seeds += [row['path'] for row in declared if row['path'].endswith('.py') and row['path'].split('/')[0] not in ('deps', 'tools', 'work')]
    for name in code_closure(seeds):
        digest = sha256(ROOT / name)
        if name in hashes and hashes[name] != digest:
            raise ValueError('Frozen replay implementation changed: ' + name)
        hashes[name] = digest
    for name, digest in hashes.items():
        if sha256(ROOT / name) != digest:
            raise ValueError('Frozen dependency changed: ' + name)
    document['generatorSources'] = [{'path': name, 'sha256': digest} for name, digest in sorted(hashes.items())]
    document['replayCodeSeal'] = {'generator': Path(__file__).name, 'producerCommand': producer,
        'scope': 'Declared dependencies and recursively resolved repository-local Python imports; external runtime and inputs retain their existing gates',
        'sourceOrNativeByteCredit': 0}
    write_json(path, document)
    print({'report': relative, 'previousReportSha256': old_hash, 'sealedReportSha256': sha256(path), 'pinnedReplayCodeAndInputs': len(hashes)})


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('report')
    parser.add_argument('--existing', action='store_true')
    parser.add_argument('producer', nargs='+')
    options = parser.parse_args()
    code_closure([options.producer[0]])
    if not options.existing:
        subprocess.run([sys.executable, str(ROOT / options.producer[0]), *options.producer[1:]], cwd=ROOT, check=True)
    seal(options.report, options.producer)


if __name__ == '__main__':
    main()
