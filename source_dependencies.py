import re
from pathlib import Path
from project import ROOT, sha256


def dependency_hashes(item, report=None):
    result = {}
    for document in (report or {}, item):
        for entry in document.get('sourceDependencies', []):
            relative = Path(entry['path'])
            target = (ROOT / relative).resolve()
            digest = entry['sha256']
            if relative.is_absolute() or not target.is_relative_to((ROOT / 'src').resolve()) or not re.fullmatch(r'[0-9a-f]{64}', digest):
                raise ValueError('Source dependency must be a hashed repository-local authored file')
            name = target.relative_to(ROOT).as_posix()
            if name in result and result[name] != digest:
                raise ValueError('Conflicting source dependency identities')
            result[name] = digest
    return result


def dependencies_current(item, report=None):
    dependencies = dependency_hashes(item, report)
    if not all((ROOT / path).is_file() and sha256(ROOT / path) == expected for path, expected in dependencies.items()):
        return False
    source = item.get('source', (report or {}).get('source'))
    if not source:
        return not dependencies
    pending, visited = [(ROOT / source).resolve()], set()
    declared = {(ROOT / path).resolve() for path in dependencies}
    while pending:
        path = pending.pop()
        if path in visited:
            continue
        visited.add(path)
        if path.suffix.lower() not in ('.c', '.cpp', '.cc', '.h', '.hpp', '.inc'):
            continue
        try:
            text = path.read_text(encoding='utf-8-sig')
        except OSError:
            return False
        for name in re.findall(r'^\s*#\s*include\s*"([^"\n]+)"', text, re.M):
            included = (path.parent / name).resolve()
            if included not in declared:
                return False
            pending.append(included)
    return True
