import argparse
import copy
import subprocess
import sys
from project import ROOT, read_json, write_json, sha256
from qualify_itcm_reset_reference_v1_20261106 import REPORT, qualify


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('specification')
    parser.add_argument('--register', action='store_true')
    options = parser.parse_args()
    spec = read_json(ROOT / options.specification)
    subset = copy.deepcopy(spec)
    selected = [p for p in spec['packets'] if p['report'] == REPORT]
    assert len(selected) <= 1
    proof = qualify() if selected else None
    subset['packets'] = []
    data_packets = []
    for packet in spec['packets']:
        if packet in selected:
            continue
        report = read_json(ROOT / packet['report'])
        if 'dataMatches' in report and not report.get('matches'):
            assert report['functionMatched'] == 0 and report['functionMatches'] == []
            data_packets.append(packet['report'])
        else:
            assert report['matches']
            subset['packets'].append(packet)
    path = ROOT / f'work/integration/cohort{spec["cohort"]}-main-function-reference-subset-v3.json'
    write_json(path, subset)
    command = [sys.executable, str(ROOT / 'qualify_main_arm9_reference_context_v4_20261106.py'), path.relative_to(ROOT).as_posix()]
    if options.register:
        command.append('--register')
    subprocess.run(command, cwd=ROOT, check=True)
    output = ROOT / f'evidence/verification/cohort{spec["cohort"]}-mixed-reference-inputs-20261105.json'
    document = read_json(output)
    document.update(specification=options.specification, specificationSha256=sha256(ROOT / options.specification),
        independentItcmResetReferenceQualification=proof, dataPacketsRequireSeparateTypedDataQualifier=data_packets,
        originalMainArmAndThumbQualifiersUnchanged=True, generatorSha256=sha256(__file__))
    write_json(output, document)


if __name__ == '__main__':
    main()
