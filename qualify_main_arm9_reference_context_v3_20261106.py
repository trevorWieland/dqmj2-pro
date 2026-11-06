import argparse
import copy
import subprocess
import sys
from project import ROOT, read_json, write_json, sha256


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('specification')
    parser.add_argument('--register', action='store_true')
    options = parser.parse_args()
    spec = read_json(ROOT / options.specification)
    extra = ['--register'] if options.register else []
    subprocess.run([sys.executable, str(ROOT / 'qualify_arm9_thumb_reference_context_v3_20261106.py'), options.specification, *extra], cwd=ROOT, check=True)
    arm = copy.deepcopy(spec)
    arm['packets'] = []
    for packet in spec['packets']:
        report = read_json(ROOT / packet['report'])
        modes = {r['mode'] for r in report['matches']}
        assert modes in [{'arm'}, {'thumb'}]
        if modes == {'arm'}:
            arm['packets'].append(packet)
    subset = ROOT / f'work/integration/cohort{spec["cohort"]}-arm-reference-subset.json'
    subset.parent.mkdir(parents=True, exist_ok=True)
    write_json(subset, arm)
    subprocess.run([sys.executable, str(ROOT / 'qualify_arm9_reference_packets_v2_20261105.py'), subset.relative_to(ROOT).as_posix(), *extra], cwd=ROOT, check=True)
    reports = [f'evidence/verification/cohort{spec["cohort"]}-thumb-reference-inputs-20261105.json',
        f'evidence/verification/cohort{spec["cohort"]}-arm9-reference-packets-v2-20261105.json']
    assert all(read_json(ROOT / path)['passed'] for path in reports)
    write_json(ROOT / f'evidence/verification/cohort{spec["cohort"]}-mixed-reference-inputs-20261105.json', dict(
        passed=True, sourceCredit=0, specification=options.specification,
        specificationSha256=sha256(ROOT / options.specification), registered=options.register,
        armOnlyVerifierUnchanged=True, independentThumbModeAndLinkedByteProofRequired=True,
        reports=[dict(path=p, sha256=sha256(ROOT / p)) for p in reports]))
    print(dict(passed=True, cohort=spec['cohort'], registered=options.register))


if __name__ == '__main__':
    main()
