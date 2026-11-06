import argparse
import concurrent.futures
import shutil
import subprocess
from pathlib import Path
from project import ROOT, read_json, sha256, write_json

DIRECTORIES = ['tools/mwccarm', 'tools/m2c', 'tools/m2c-python',
               'deps/native', 'deps/references', 'deps/sdk-reference',
               'inputs', 'extract/arm7', 'extract/arm9', 'extract/arm9_overlays', 'extract/utility', 'asm']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('lane', choices=['arm7', 'overlays', 'save-core'])
    args = parser.parse_args()
    base = ROOT.parent / 'j2p-recovery-lanes'
    target = (base / args.lane).resolve()
    assert target.is_relative_to(base.resolve()) and target != ROOT.resolve()
    assert (target / '.git').is_file() and (target / 'project.py').is_file()
    revision = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=target, check=True, capture_output=True, text=True).stdout.strip()
    paths = set()
    for name in DIRECTORIES:
        source = ROOT / name
        if not source.exists():
            continue
        for path in source.rglob('*'):
            if '__pycache__' in path.parts or '.git' in path.parts:
                continue
            if path.is_symlink() or path.is_junction():
                raise ValueError('Lane inputs must be explicit local files: ' + str(path))
            if path.is_file():
                paths.add(path.relative_to(ROOT).as_posix())
    paths.update(path.relative_to(ROOT).as_posix() for path in (ROOT / 'tools').iterdir() if path.is_file())

    def copy(relative):
        source, destination = ROOT / relative, target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        before = sha256(source)
        shutil.copy2(source, destination)
        assert sha256(destination) == before and sha256(source) == before
        return {'path': relative, 'sha256': before, 'bytes': destination.stat().st_size}

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        copied = list(pool.map(copy, sorted(paths)))
    snapshot = read_json(ROOT / 'recovery.json')
    write_json(target / 'evidence/verification/lane-integrator-registry-snapshot-20261030.json', snapshot)
    document = {'lane': args.lane, 'worktree': str(target), 'sourceRevision': revision,
                'sourceRepository': str(ROOT), 'copiedInputs': copied, 'junctionDependencies': 0,
                'generatedAssemblyAndExtractionSourceCredit': 0, 'compilerJobsRecommended': 3,
                'acceptedRegistryOwnedByIntegrator': True,
                'limitations': ['Development lane only; final acceptance requires integrator replay and module/ROM comparison',
                                'Copied extraction and assembly are measured scaffolding, never reconstructed source',
                                'The registry snapshot reserves integrator ranges; it is not a new source registration']}
    path = target / 'evidence/verification/lane-bootstrap-20261030.json'
    write_json(path, document)
    write_json(ROOT / f'evidence/verification/recovery-lane-{args.lane}-bootstrap-20261030.json', document)
    print({'lane': args.lane, 'filesCopiedAndHashed': len(copied), 'bytesCopied': sum(row['bytes'] for row in copied),
           'localDependencies': True, 'sourceCredit': 0}, flush=True)


if __name__ == '__main__':
    main()
