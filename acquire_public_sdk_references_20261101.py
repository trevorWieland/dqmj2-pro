import hashlib
import io
import json
from pathlib import Path
import stat
import urllib.request
import zipfile
from project import ROOT, read_json, write_json, sha256

REFERENCES = [('NitroSystem', 'd636fb5d2b212e8736f09859fff447be2bd0ac85'),
    ('NitroSDK', 'ccbbcc8b6db4c4dbba3d503d2026978d78977840')]


def main():
    results = []
    folder = ROOT / 'evidence/research/20261101-public-sdk-reference'
    for repository, revision in REFERENCES:
        tree_path = folder / (repository + '-tree.json')
        tree = read_json(tree_path)
        assert not tree.get('truncated') and not any(row['type'] == 'commit' for row in tree['tree'])
        expected = {row['path']: row for row in tree['tree'] if row['type'] == 'blob'}
        destination = ROOT / f'deps/reference/{repository}-{revision}'
        archive = ROOT / f'tools/archives/references/{repository}-{revision}.zip'
        url = f'https://codeload.github.com/ntrtwl/{repository}/zip/{revision}'
        if not archive.exists():
            with urllib.request.urlopen(url, timeout=60) as response:
                data = response.read()
            archive.parent.mkdir(parents=True, exist_ok=True)
            archive.write_bytes(data)
        source_files = []
        with zipfile.ZipFile(io.BytesIO(archive.read_bytes())) as package:
            for entry in package.infolist():
                if entry.is_dir():
                    continue
                relative = '/'.join(entry.filename.split('/')[1:])
                assert relative in expected and relative and '..' not in Path(relative).parts
                assert not stat.S_ISLNK(entry.external_attr >> 16)
                data = package.read(entry)
                record = expected[relative]
                assert len(data) == record['size']
                assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == record['sha']
                target = (destination / relative).resolve()
                assert target.is_relative_to(destination.resolve())
                if target.exists():
                    assert target.read_bytes() == data
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(data)
                source_files.append(dict(path=target.relative_to(ROOT).as_posix(), sha256=sha256(target),
                    gitBlobSha1=record['sha'], bytes=len(data)))
        assert len(source_files) == len(expected)
        results.append(dict(repository='ntrtwl/' + repository, revision=revision, url=url,
            archive=archive.relative_to(ROOT).as_posix(), archiveSha256=sha256(archive),
            tree=tree_path.relative_to(ROOT).as_posix(), treeSha256=sha256(tree_path),
            unmodifiedFiles=source_files, allGitBlobIdentitiesVerified=True,
            cSourceFiles=sum(row['path'].endswith('.c') for row in source_files),
            sourceCredit=0, binariesOrAssemblyAdopted=False, compilerInputAdoptionProven=False))
        print(dict(repository=repository, files=len(source_files), cSources=results[-1]['cSourceFiles']), flush=True)
    write_json(ROOT / 'evidence/tools/public-sdk-reference-acquisition-20261101.json', dict(
        sourceCredit=0, generator=Path(__file__).name, generatorSha256=sha256(__file__), references=results,
        provenance='Public upstream revisions pinned by the separately hashed pokeheartgold wrap files',
        limitations=['Reference artifacts only; no function identity, historical type, matching code or SDK-version claim',
            'Unmodified archive binaries and assembly are never reconstructed source credit',
            'Any adopted C requires compatible interfaces, pinned compilation, genuine links and native/regression validation']))


if __name__ == '__main__':
    main()
