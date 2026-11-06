import hashlib
import io
import json
import urllib.request
import zipfile
from pathlib import Path
from project import ROOT, write_json, sha256

COMMIT = '8556c81d80d1c1af98a858c8f4dc951357f29139'
REPOSITORY = 'simonlindholm/decomp-permuter'


def get(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'J2P-local-tool-verification'})
    with urllib.request.urlopen(request, timeout=60) as stream:
        return stream.read()


def main():
    target = ROOT / ('tools/decomp-permuter-' + COMMIT)
    assert not target.exists()
    api = 'https://api.github.com/repos/' + REPOSITORY
    commit_data = get(api + '/commits/' + COMMIT)
    commit = json.loads(commit_data)
    assert commit['sha'] == COMMIT
    tree_data = get(api + '/git/trees/' + commit['commit']['tree']['sha'] + '?recursive=1')
    tree = json.loads(tree_data)
    assert not tree['truncated']
    assert not [entry for entry in tree['tree'] if entry['type'] == 'commit'], 'Submodules require separate pinned acquisition'
    blobs = {entry['path']: entry for entry in tree['tree'] if entry['type'] == 'blob'}
    url = 'https://codeload.github.com/' + REPOSITORY + '/zip/' + COMMIT
    data = get(url)
    archive = ROOT / ('tools/archives/decomp-permuter-' + COMMIT + '.zip')
    archive.parent.mkdir(parents=True, exist_ok=True)
    assert not archive.exists()
    archive.write_bytes(data)
    files = []
    with zipfile.ZipFile(io.BytesIO(data)) as package:
        prepared = []
        for member in package.infolist():
            if member.is_dir():
                continue
            parts = Path(member.filename.replace('\\', '/')).parts
            assert len(parts) >= 2 and '..' not in parts and ':' not in member.filename
            relative = Path(*parts[1:]).as_posix()
            destination = (target / relative).resolve()
            assert destination.is_relative_to(target.resolve()) and relative in blobs
            payload = package.read(member)
            blob = hashlib.sha1(b'blob ' + str(len(payload)).encode() + b'\0' + payload).hexdigest()
            assert blob == blobs[relative]['sha'], relative
            assert len(payload) == blobs[relative]['size'], relative
            prepared.append((destination, payload))
            files.append(dict(path=destination.relative_to(ROOT).as_posix(), bytes=len(payload),
                gitBlobSha1=blob, sha256=hashlib.sha256(payload).hexdigest()))
        assert {row['path'][len(target.relative_to(ROOT).as_posix()) + 1:] for row in files} == set(blobs)
        target.mkdir(parents=True)
        for destination, payload in prepared:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(payload)
    evidence = ROOT / 'evidence/tools/decomp-permuter-acquisition-20261101'
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / 'commit.json').write_bytes(commit_data)
    (evidence / 'tree.json').write_bytes(tree_data)
    report = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__), repository=REPOSITORY,
        commit=COMMIT, tree=commit['commit']['tree']['sha'], archive=archive.relative_to(ROOT).as_posix(),
        archiveSha256=sha256(archive), archiveBytes=len(data), sourceTreeFiles=files,
        independentGitBlobTreeChecksPassed=True, upstreamUnmodified=True, dependencyLinks=0,
        smokeTestPassed=False, adoptedForSourceAcceptance=False, sourceCredit=0,
        limitations=['Acquisition/provenance only; dependency and local smoke validation precede adoption',
            'Distributed/server features are not invoked; no project source or input is uploaded'])
    write_json(ROOT / 'evidence/tools/decomp-permuter-acquisition-20261101.json', report)
    print(dict(commit=COMMIT, files=len(files), archiveSha256=sha256(archive), adopted=False))


if __name__ == '__main__':
    main()
