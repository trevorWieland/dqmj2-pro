from pathlib import Path
import json
import subprocess
from project import ROOT, read_json, write_json, sha256


def main():
    package_name = 'cohort149-parallel-wave20261102-next-package.json'
    package = read_json(ROOT / package_name)
    plan_name = 'evidence/verification/cohort-2026-10-29-149.json'
    plan = read_json(ROOT / plan_name)
    extra = {package_name, 'stage_declared_source_package_v3_20261101.py', *package['extra']}
    declared = set()
    for name in package['manifests']:
        extra.add(name)
        for row in read_json(ROOT / name)['files']:
            relative = row['path'].replace(chr(92), '/')
            if relative.split('/')[0] not in ['deps', 'tools', 'inputs']:
                declared.add(relative)
    extra.update(declared)
    extra.update(['evidence/verification/cohort149-copied-reference-inputs-20261101.json',
        'evidence/verification/cohort149-frozen-diagnostic-sources-20261101.json'])
    assert not package['archives'] and not package.get('archivedEvidenceDirectories')
    extra.update(path.relative_to(ROOT).as_posix() for path in (ROOT / 'evidence/verification').glob('cohort149-*20261101.json'))
    report_paths = sorted({*plan['reports'], *plan.get('interpretedReports', []), *[path for path in extra if path.endswith('.json')]})
    opaque = set(package['traces'])
    assert not opaque.intersection(report_paths)
    unsafe = []
    import stage_verified_cohort
    actual_skip = set(stage_verified_cohort.SKIP_KEYS)
    def exact_gather(value, origin):
        if isinstance(value, dict):
            for key, child in value.items():
                if key in ('source', 'path') and isinstance(child, str) and 'evidence/lanes/parallel-wave20261102/main-sdk-third/exploration-headers/' in child:
                    unsafe.append(dict(report=origin, field=key, value=child))
                if key not in actual_skip:
                    exact_gather(child, origin)
        elif isinstance(value, list):
            for child in value:
                exact_gather(child, origin)
    for name in report_paths:
        exact_gather(read_json(ROOT / name), name)
    assert not unsafe
    closure_name = 'evidence/verification/cohort149-captured-oracle-closure-20261031.json'
    closure = read_json(ROOT / closure_name)
    pinned = closure['sourceAndEvidenceHashes']
    indexed = json.loads(subprocess.check_output(['git', 'show', ':' + closure_name], cwd=ROOT))
    assert pinned == indexed['sourceAndEvidenceHashes'] and len(pinned) == 17609
    mismatches = [name for name, digest in pinned.items() if not (ROOT / name).is_file() or sha256(ROOT / name) != digest]
    assert not mismatches
    assert not opaque.intersection(pinned)
    result = dict(passed=True, sourceCredit=0, packageSha256=sha256(ROOT / package_name),
        recursiveReportPathsChecked=len(report_paths), explicitUnselectedExplorationHeaderReferences=unsafe,
        opaqueArtifacts=len(opaque), opaqueArchivedJsons=sum(name.startswith('evidence/attempts/') for name in opaque),
        opaqueArtifactsAbsentFromRecursiveReportPaths=True, opaqueArtifactsAbsentFromNativeClosure=True,
        capturedNativeClosurePins=len(pinned), nativeClosurePinMapEqualsPreviouslyStagedSnapshot=True,
        actualNativeClosureContentHashesUnchanged=True, nativeClosureMismatches=mismatches,
        capturedNativeClosureSha256=sha256(ROOT / closure_name),
        noBroadUnselectedResearchRuntimeDependency=True, originalArchiveBytesUneditedByAudit=True,
        indexMutations=0, stagerInvocations=0, registryMutations=0, generatorSha256=sha256(Path(__file__)))
    output = ROOT / 'evidence/verification/parallel-wave20261102/cohort149-final-opaque-report-paths-audit.json'
    assert not output.exists()
    write_json(output, result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
