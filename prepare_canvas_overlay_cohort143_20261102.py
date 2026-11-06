from project import ROOT, read_json, write_json, sha256


def main():
    name = 'cohort143-canvas-overlay-and-thumb-20261102'
    reports = [
        ('evidence/matches/main-canvas-areas1224-v2-20261102.json', 'match_main_canvas_areas1224_v2_20261102.py'),
        ('evidence/matches/ov000-20261102-helpers885.json', 'match_ov000_helpers885_20261102.py'),
        ('evidence/matches/arm7-sdk365-measure-task624-20261102.json', 'validate_arm7_sdk366_measure_task_20261102.py'),
        ('evidence/matches/mechanics-save-20261102-lane-thumb-context432.json', 'match_mechanics_save_20261102_lane_thumb_context432.py'),
    ]
    manifests = [
        'provenance/main-canvas-areas1224-windows-ready-20261102.json',
        'provenance/handoffs/ov000-helpers885-ready-20261102.json',
        'evidence/lanes/save-core/large416-ready-20261102.json',
        'evidence/lanes/save-core/large422-ready-20261102.json',
        'provenance/handoffs/ov000-geometry877-ready-20261102.json',
        'provenance/handoffs/ov000-geometry881-ready-20261102.json',
        'evidence/lanes/save-core/analysis-assembly433-ready-20261102.json',
        'provenance/arm7-sdk368-measure-task624-handoff-20261102.json',
        'evidence/lanes/save-core/thumb-context432-ready-20261102.json',
    ]
    archives = [
        'ov000-helpers885-20261102', 'save-core-large416-20261102',
        'save-core-large422-20261102', 'ov000-geometry877-20261102',
        'ov000-geometry881-20261102', 'save-core-analysis-assembly433-20261102',
        'arm7-sdk368-measure-task624-20261102', 'save-core-thumb-context432-20261102',
    ]
    receipts = [
        'main-canvas-areas1224-v2-parent-isolated-replay',
        'ov000-helpers885-independent-replay', 'save-core-large416-independent-replay',
        'save-core-large422-independent-replay', 'ov000-geometry877-independent-replay',
        'ov000-geometry881-independent-replay', 'save-core-analysis-assembly433-independent-replay',
        'arm7-sdk368-independent-replay', 'save-core-thumb-context432-independent-replay',
    ]
    specification = dict(cohort=143, previousAcceptedCohort=142, migrations=[],
        packets=[dict(report=report, producer=[producer], directProducer=False) for report, producer in reports],
        expectedAdditions=[dict(module=row['module'], mode=row.get('mode', 'arm'),
            address=row['address'], bytes=row['bytes'])
            for report, _ in reports for row in read_json(ROOT / report)['matches']],
        originalChecksRetained=True,
        postSealCommands=[['check_main_canvas_areas1224_v2_windows32_20261102.py']],
        oracles=[dict(report='evidence/ports/main-canvas-areas1224-v2-windows32-20261102.json',
            reproduce=['check_main_canvas_areas1224_v2_windows32_20261102.py'])])
    write_json(ROOT / (name + '-specification.json'), specification)
    stage = 'stage_canvas_overlay_cohort143_20261102.py'
    document = 'docs/2026-11-02-cohort143-canvas-overlay-and-thumb.md'
    extras = [name + '-specification.json', stage, document, __file__.split('\\')[-1],
        'record_cohort143_independent_replays_20261102.py',
        'docs/2026-11-02-application-integration-evidence-update-v2.md',
        *['evidence/verification/' + item + '-20261102.json' for item in receipts]]
    preserved = []
    for manifest in manifests:
        for row in read_json(ROOT / manifest)['files']:
            path = ROOT / row['path'].replace(chr(92), '/')
            if path.suffix == '.py' and b'\r\r\n' in path.read_bytes():
                assert manifest.startswith('evidence/lanes/save-core/')
                commit = {'large416-ready-20261102.json': 'e06cf0b30267c1e3ab10c4cd0e6ce6b135fbbd54',
                    'large422-ready-20261102.json': 'efd6243a1719d09fcdc6693925c993fd8be0504c'}[path_key(manifest)]
                preserved.append(dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path),
                    pinManifest=manifest, workerCommit=commit, sourceCredit=0,
                    reason='unchanged-worker-CRCRLF-research-input'))
    write_json(ROOT / (name + '-package.json'), dict(cohort=143, manifests=manifests,
        archives=archives, traces=[], extra=extras, preservedResearchReplayInputs=preserved))
    (ROOT / stage).write_text("import sys\nimport stage_declared_source_package_v7_20261102 as staging\n\n\nif __name__ == '__main__':\n    sys.argv = [sys.argv[0], '" + name + "-package.json']\n    staging.main()\n", encoding='utf-8')
    print(dict(cohort=143, preparedFunctions=len(specification['expectedAdditions']),
        preparedBytes=sum(row['bytes'] for row in specification['expectedAdditions']),
        preservedResearchReplayInputs=len(preserved), registryMutated=False))


def path_key(name):
    return name.split('/')[-1]


if __name__ == '__main__':
    main()
