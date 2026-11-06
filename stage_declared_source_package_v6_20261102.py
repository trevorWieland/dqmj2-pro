import argparse
import re
import subprocess
import sys
from project import ROOT, read_json, write_json, sha256
import oracle_source_closure_20261031
import stage_verified_cohort


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('configuration')
    options = parser.parse_args()
    configuration = read_json(ROOT / options.configuration)
    cohort = configuration['cohort']
    extra = [options.configuration, 'stage_declared_source_package_v3_20261101.py', *configuration['extra']]
    declared, dependencies, diagnostic = set(), [], []
    for name in configuration['manifests']:
        extra.append(name)
        for row in read_json(ROOT / name)['files']:
            relative = row['path'].replace(chr(92), '/')
            path = (ROOT / relative).resolve()
            assert path.is_relative_to(ROOT) and path.is_file()
            if relative.split('/')[0] in ['deps', 'tools', 'inputs']:
                assert sha256(path) == row['sha256']
                dependencies.append(dict(path=relative, sha256=sha256(path)))
                continue
            assert relative.split('/')[0] not in stage_verified_cohort.EXCLUDED
            assert path.suffix.lower() not in ['.bin', '.nds', '.sav', '.o', '.exe', '.dll']
            declared.add(relative)
            if (relative.startswith('nonmatching/') or relative.startswith('evidence/generated/ghidra497/') or relative.startswith('evidence/generated/ghidra543/') or (re.fullmatch(r'evidence/generated/ghidra[0-9]+/[a-z0-9_-]+/[0-9a-f]{8}\.generated\.c', relative) is not None and read_json(ROOT / name).get('sourceCredit') == 0)) and sha256(path) == row['sha256']:
                diagnostic.append(dict(path=relative, sha256=sha256(path), pinManifest=name, pinManifestSha256=sha256(ROOT / name)))
    for preserved in configuration.get('preservedResearchReplayInputs',[]):
        assert preserved['sourceCredit']==0 and preserved['reason']=='unchanged-worker-CRCRLF-research-input'
        relative=preserved['path'];assert relative in declared
        manifest=preserved['pinManifest'];assert manifest in configuration['manifests']
        pins={r['path'].replace(chr(92),'/'):r['sha256']for r in read_json(ROOT/manifest)['files']}
        assert pins[relative]==preserved['sha256']==sha256(ROOT/relative)
        blob=subprocess.run(['git','show',preserved['workerCommit']+':'+relative],cwd=ROOT,capture_output=True,check=True).stdout
        assert blob==(ROOT/relative).read_bytes()and b'\r\r\n'in blob
        diagnostic.append(dict(path=relative,sha256=sha256(ROOT/relative),pinManifest=manifest,pinManifestSha256=sha256(ROOT/manifest),
            workerCommit=preserved['workerCommit'],sourceCredit=0,classification='unchanged-archived-research-replay'))
    dependency_path = f'evidence/verification/cohort{cohort}-copied-reference-inputs-20261101.json'
    diagnostic_path = f'evidence/verification/cohort{cohort}-frozen-diagnostic-sources-20261101.json'
    write_json(ROOT / dependency_path, dict(copiedDependencies=dependencies,
        committedAsAuthoredSource=False, copiedByFreshInputSnapshot=True, sourceCredit=0))
    write_json(ROOT / diagnostic_path, dict(frozenDiagnosticSources=diagnostic, sourceCredit=0,
        scope='Exact handoff-pinned nonmatching or Ghidra-generated diagnostics; no positive source credit'))
    extra.extend([*declared, dependency_path, diagnostic_path])
    for label in configuration['archives']:
        folder = ROOT / 'provenance/handoffs' / label
        assert folder.is_dir()
        extra.extend(path.relative_to(ROOT).as_posix() for path in folder.glob('*.json'))
    for name in configuration.get('archivedEvidenceDirectories', []):
        folder = (ROOT / name).resolve()
        assert folder.is_relative_to(ROOT / 'evidence')
        extra.extend(path.relative_to(ROOT).as_posix() for path in folder.glob('*.json'))
    extra.extend(path.relative_to(ROOT).as_posix() for path in (ROOT / 'evidence/verification').glob(f'cohort{cohort}-*20261101.json'))
    assert all((ROOT / name).is_file() for name in extra)
    staged_paths = sorted(declared | set(configuration.get('traces', [])))
    subprocess.run(['git', 'add', '--pathspec-from-file=-', '--pathspec-file-nul'],
        input=('\0'.join(staged_paths) + '\0').encode('utf-8'), cwd=ROOT, check=True)
    original = oracle_source_closure_20261031.collect

    def captured_collect():
        result = original()
        write_json(ROOT / f'evidence/verification/cohort{cohort}-captured-oracle-closure-20261031.json', result)
        return result

    oracle_source_closure_20261031.collect = captured_collect
    sys.argv = ['stage_verified_cohort.py', '--cohort', str(cohort), '--extra', *sorted(set(extra))]
    stage_verified_cohort.main()
    subprocess.run(['git', 'add', '--', f'evidence/verification/cohort{cohort}-captured-oracle-closure-20261031.json'], cwd=ROOT, check=True)


if __name__ == '__main__':
    main()
