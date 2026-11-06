import hashlib
import shutil
import subprocess
import tarfile
from pathlib import Path
from project import ROOT, read_json, sha256

REFERENCES = ROOT / 'evidence/verification/cohort101-tracked-readonly-references-20261101.json'


def materialize(target):
    target = target.resolve()
    if target.exists() or target.is_relative_to(ROOT) or ROOT.is_relative_to(target):
        raise ValueError('Fresh checkout requires a new separate private directory')
    revision = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    names = subprocess.run(['git', 'ls-tree', '-r', '--name-only', '-z', revision], cwd=ROOT,
        capture_output=True, check=True).stdout.decode().split('\0')
    paths = [Path(name) for name in names if name]
    allowed = {row['path']: row['sha256'] for row in read_json(REFERENCES)['files']}
    assert len(allowed) == 10
    excluded = {'build', 'work', 'extract', 'asm', 'logs', 'inputs', 'tools', 'deps', '.git', '__pycache__'}
    observed = set()
    for path in paths:
        if path.is_absolute() or '..' in path.parts:
            raise ValueError('Escaping tracked source path')
        name = path.as_posix()
        if path.parts[0] in excluded:
            if name not in allowed or not name.startswith('deps/msl-') or path.suffix not in ['.c', '.h', '']:
                raise ValueError('Unapproved tracked dependency/cache/input: ' + name)
            payload = subprocess.run(['git', 'show', revision + ':' + name], cwd=ROOT, capture_output=True, check=True).stdout
            assert hashlib.sha256(payload).hexdigest() == allowed[name] == sha256(ROOT / name)
            observed.add(name)
    assert observed == set(allowed)
    target.mkdir(parents=True)
    archive = target / '.source-snapshot.tar'
    subprocess.run(['git', 'archive', '--format=tar', '--output=' + str(archive), revision], cwd=ROOT, check=True)
    with tarfile.open(archive) as stream:
        for member in stream.getmembers():
            if not (target / member.name).resolve().is_relative_to(target) or member.issym() or member.islnk():
                raise ValueError('Escaping archive path or dependency link')
        stream.extractall(target, filter='data')
    archive.unlink()
    sources = []
    for path in paths:
        name = path.as_posix()
        sources.append(dict(path=name, sha256=sha256(target / path),
            kind='third-party-reference' if name in allowed else 'committed-source-or-evidence'))
    inputs = []
    for directory in ['tools', 'deps', 'inputs']:
        for source in (ROOT / directory).rglob('*'):
            if not source.is_file() or '__pycache__' in source.parts:
                continue
            if source.is_symlink():
                raise ValueError('Fresh dependencies cannot use links')
            relative = source.relative_to(ROOT)
            destination = target / relative
            if relative.as_posix() in allowed:
                assert sha256(destination) == sha256(source) == allowed[relative.as_posix()]
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            inputs.append(dict(path=relative.as_posix(), sha256=sha256(destination)))
    subprocess.run(['git', 'init', '--quiet', str(target)], check=True)
    return dict(sourceRevision=revision, sourceFromCommittedTree=True, sourceFiles=sources, inputFiles=inputs,
        copiedCachedObjects=0, copiedGeneratedExtraction=False, dependencyLinks=0,
        materializer=Path(__file__).name, materializerSha256=sha256(__file__),
        readonlyReferenceManifest=REFERENCES.relative_to(ROOT).as_posix(), readonlyReferenceManifestSha256=sha256(REFERENCES),
        approvedTrackedReferenceFiles=len(allowed), referenceSourceCredit=0)
