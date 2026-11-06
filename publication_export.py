import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent
SOURCE_EXTENSIONS = {'.c', '.cpp', '.h', '.hpp', '.s', '.S', '.inc'}
SECRET = re.compile(rb'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|AKIA[0-9A-Z]{16})')


def digest(payload):
    return hashlib.sha256(payload).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def selected_path(name):
    path = PurePosixPath(name)
    if path.parts[0] in {'src', 'ports', 'oracle'}:
        return path.suffix in SOURCE_EXTENSIONS or path.suffix == '.py'
    if path.parts[0] == 'config':
        return path.suffix in {'.txt', '.yaml', '.yml', '.json', '.py'}
    if path.parts[0] == 'docs':
        return path.suffix == '.md'
    if path.parts[0] == 'deps':
        return name.startswith('deps/msl-') and (path.suffix in SOURCE_EXTENSIONS or path.name == 'LICENSE')
    if len(path.parts) == 1:
        return path.suffix == '.py' or name in {'.gitattributes', 'tools.lock.json', 'project.json'}
    return False


def read_blobs(revision, paths):
    process = subprocess.Popen(['git', 'cat-file', '--batch'], cwd=ROOT,
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    try:
        for name in paths:
            process.stdin.write((revision + ':' + name + '\n').encode())
            process.stdin.flush()
            header = process.stdout.readline().decode().strip().split()
            if len(header) != 3 or header[1] != 'blob':
                raise ValueError('Expected a regular committed file: ' + name)
            size = int(header[2])
            payload = process.stdout.read(size)
            if len(payload) != size or process.stdout.read(1) != b'\n':
                raise ValueError('Incomplete Git object: ' + name)
            yield name, payload
    finally:
        process.stdin.close()
        process.stdout.close()
        process.wait()


def emit(destination, name, payload, records):
    relative = PurePosixPath(name)
    target = (destination / Path(*relative.parts)).resolve()
    if not target.is_relative_to(destination) or '..' in relative.parts:
        raise ValueError('Unsafe public path: ' + name)
    if b'\0' in payload or SECRET.search(payload):
        raise ValueError('Binary or credential candidate requires review: ' + name)
    payload.decode('utf-8')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(payload)
    records[name] = {'sha256': digest(payload), 'bytes': len(payload)}


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--revision', required=True)
    parser.add_argument('--destination', type=Path, required=True)
    args = parser.parse_args()
    revision = git('rev-parse', args.revision + '^{commit}').decode().strip()
    destination = args.destination.resolve()
    allowed = (ROOT / 'work/publication').resolve()
    if not destination.is_relative_to(allowed) or destination == allowed:
        raise ValueError('Export must use a dedicated work/publication subdirectory')
    if destination.exists():
        raise ValueError('Export never overwrites an existing directory')
    listing = git('ls-tree', '-r', '--name-only', revision).decode().splitlines()
    paths = sorted(name for name in listing if selected_path(name))
    rows = [json.loads(line) for line in git('show', revision + ':ledger/functions.jsonl').decode().splitlines() if line]
    functions = [row for row in rows if row.get('states', {}).get('functionMatched') and row.get('states', {}).get('moduleLinked')]
    if len(functions) != 11482:
        raise ValueError('This initial export requires the closed cohort 172 snapshot')
    for row in functions:
        row['sourceUnit'] = row['sourceUnit'].replace('\\', '/')
        for dependency in row.get('sourceDependencies', []):
            dependency['path'] = dependency['path'].replace('\\', '/')
    sources = {row['sourceUnit']: row['sourceSha256'] for row in functions}
    for row in functions:
        for dependency in row.get('sourceDependencies', []):
            previous = sources.setdefault(dependency['path'], dependency['sha256'])
            if previous != dependency['sha256']:
                raise ValueError('Conflicting committed source dependency')
    missing = sorted(set(sources) - set(paths))
    if missing:
        raise ValueError('Export omits accepted source/include files: ' + repr(missing[:10]))
    records = {}
    for name, payload in read_blobs(revision, paths):
        if name in sources and digest(payload) != sources[name]:
            raise ValueError('Closed source hash mismatch: ' + name)
        emit(destination, name, payload, records)
    manifest = {'schemaVersion': 1, 'revision': revision,
                'romSha256': '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',
                'initializedDenominatorBytes': 2512636, 'acceptedInitializedBytes': 1224354,
                'acceptedFunctions': len(functions), 'sourceOnlyRomProven': False,
                'fullCleanReplayProven': False, 'functions': functions}
    emit(destination, 'public/accepted-functions.json', json_bytes(manifest), records)
    data = json.loads(git('show', revision + ':ledger/data.json'))
    emit(destination, 'public/accepted-data.json', json_bytes(data), records)
    emit(destination, '.gitignore', b'/inputs/\n/tools/\n/deps/native/\n/extract/\n/asm/\n/build/\n/work/\n/logs/\n/evidence/\n__pycache__/\n*.o\n*.elf\n*.nds\n*.srl\n*.sav\n*.zip\n*.exe\n*.dll\n*.class\n', records)
    audit = {'schemaVersion': 1, 'sourceRevision': revision,
             'policy': 'Public reconstruction sources, configuration and tools; no ROM, extracted payload, generated evidence, compiler binary or private Git history.',
             'acceptedSourceFiles': len(sources), 'files': records,
             'excludedTrackedFiles': len(listing) - len(paths),
             'publicRepositoryCreated': False, 'sourceCreditAdded': 0}
    (destination / 'public/export-audit.json').write_bytes(json_bytes(audit))
    print(json.dumps({'destination': str(destination), 'files': len(records),
                      'bytes': sum(item['bytes'] for item in records.values()),
                      'acceptedFunctions': len(functions), 'acceptedSourceFiles': len(sources)}))


if __name__ == '__main__':
    main()
