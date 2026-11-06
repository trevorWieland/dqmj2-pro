import copy
import hashlib
import json
import runpy
import subprocess
import sys
from unittest.mock import patch
import project
import stage_declared_source_package_v9_20261106 as staging
from project import ROOT, read_json, write_json, sha256


def membership(spec):
    fields = ['expectedAdditions', 'expectedDataAdditions', 'migrations', 'packets', 'postSealCommands']
    return hashlib.sha256(json.dumps({k: spec.get(k) for k in fields}, sort_keys=True).encode()).hexdigest()


def main():
    archive = ROOT / 'evidence/attempts/cohort165-thin-stage-route-failure-20261106/verbatim-inputs.json'
    assert not archive.exists()
    preserved, outputs, controls = {}, [], []
    protected = {p: sha256(ROOT / p) for p in ['recovery.json', 'source-preferences.json']}
    for number, suffix in [(165, 'j'), (166, 'k'), (167, 'l')]:
        cfg_name = f'provenance/parallel-wave20261105-{suffix}-packets.json'
        cfg = read_json(ROOT / cfg_name)
        spec_name = cfg['name'] + '-specification.json'
        package_name = cfg['name'] + '-package.json'
        old, new = f'stage_parallel_packet_wave{number}.py', f'stage_parallel_packet_wave{number}_v2_20261106.py'
        assert cfg['cohort'] == number and cfg['stage'] == old
        spec, package = read_json(ROOT / spec_name), read_json(ROOT / package_name)
        assert package['cohort'] == spec['cohort'] == number
        for name in [cfg_name, package_name, old]:
            preserved[name] = dict(sha256=sha256(ROOT / name), text=(ROOT / name).read_text(encoding='utf-8'))
        calls = []
        def target():
            assert sys.argv[1:] == [package_name]
            assert read_json(ROOT / sys.argv[1])['cohort'] == number
            calls.append(copy.deepcopy(sys.argv[1:]))
        with patch.object(staging, 'main', target):
            runpy.run_path(str(ROOT / new), run_name='__main__')
        assert calls == [[package_name]]
        try:
            with patch.object(staging, 'main', target):
                runpy.run_path(str(ROOT / old), run_name='__main__')
        except (AssertionError, FileNotFoundError):
            controls.append(dict(cohort=number, case='old-wrong-package-route', rejected=True))
        else:
            raise AssertionError('Incorrect historical stage route accepted')
        reader = project.read_json
        def wrong_cohort(path):
            value = reader(path)
            return dict(value, cohort=number + 1) if path == ROOT / package_name else value
        try:
            with patch.object(project, 'read_json', wrong_cohort), patch.object(staging, 'main', target):
                runpy.run_path(str(ROOT / new), run_name='__main__')
        except AssertionError:
            controls.append(dict(cohort=number, case='package-cohort-disagrees', rejected=True))
        else:
            raise AssertionError('Wrong package cohort accepted')
        assert calls == [[package_name]]
        cfg['stage'] = new
        receipt = f'evidence/verification/cohort{number}-thin-stage-route-correction-20261106.json'
        for name in [new, 'qualify_parallel_package_stage_routes_20261106.py', receipt, archive.relative_to(ROOT).as_posix()]:
            if name not in package['extra']:
                package['extra'].append(name)
            if name not in cfg['extra']:
                cfg['extra'].append(name)
        for name in [receipt, archive.relative_to(ROOT).as_posix()]:
            if name not in cfg['opaqueMetadata']:
                cfg['opaqueMetadata'].append(name)
        outputs.append((number, cfg_name, cfg, spec_name, membership(spec), package_name, package, new, receipt))
    failure_names = ['evidence/verification/cohort165-continuation-driver-v28-20261105.json',
                     'logs/integration/cohort165-expanded-v28-continuation-04-20261101.txt',
                     'logs/integration/cohort165-stage-20261101.txt']
    for name in failure_names:
        preserved[name] = dict(sha256=sha256(ROOT / name), text=(ROOT / name).read_text(encoding='utf-8'))
    assert not (ROOT / 'evidence/verification/cohort165-captured-oracle-closure-20261031.json').exists()
    subprocess.run([sys.executable, str(ROOT / 'freeze_stage_collector_v9_20261106.py'), '--verify'], cwd=ROOT, check=True)
    write_json(archive, dict(sourceCredit=0, originalFailurePreserved=True, originalThinWrappersUnmodified=True,
                            captureHadNotStarted=True, files=preserved))
    for number, cfg_name, cfg, spec_name, digest, package_name, package, new, receipt in outputs:
        assert digest == membership(read_json(ROOT / spec_name))
        write_json(ROOT / cfg_name, cfg)
        write_json(ROOT / package_name, package)
        write_json(ROOT / receipt, dict(passed=True, sourceCredit=0, cohort=number,
            correctedWrapper=new, correctedWrapperSha256=sha256(ROOT / new), package=package_name,
            packageSha256=sha256(ROOT / package_name), sourceMembershipSha256=digest,
            thinRoutingOnly=True, collectorV9UnchangedAndQualificationVerified=True,
            negativeControls=[c for c in controls if c['cohort'] == number],
            failureArchive=archive.relative_to(ROOT).as_posix(), failureArchiveSha256=sha256(archive),
            generatorSha256=sha256(__file__)))
    assert all(sha256(ROOT / p) == h for p, h in protected.items())
    print(dict(passed=True, correctedThinRoutes=3, negativeControls=len(controls), sourceCredit=0))


if __name__ == '__main__':
    main()
