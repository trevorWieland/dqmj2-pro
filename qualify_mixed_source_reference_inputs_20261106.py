import argparse
import copy
import subprocess
import sys
from project import ROOT, read_json, write_json, sha256
from qualify_child_message_data_additions_20261106 import identity


def partition(spec):
    functions, data = [], []
    found = {}
    for packet in spec['packets']:
        report = read_json(ROOT / packet['report'])
        if report.get('matches'):
            assert not report.get('dataMatches')
            functions.append(packet)
            continue
        assert report['functionMatched'] == 0 and report.get('functionMatches') == []
        assert not report.get('matches') and report['dataMatches']
        for field in ['ordinaryFunctionCredit', 'executableSectionBytes']:
            assert field not in report or report[field] == 0
        for row in report['dataMatches']:
            assert row['kind'] == row['mode'] == 'data'
            assert row['ordinaryFunctionCredit'] == row['executableSectionBytes'] == 0
            assert row['relocations'] == [] and row['allocatedZeroFillBytes'] == 0
            assert row['bytes'] == row['size'] == row['compiledBytes'] == row['initializedBytes']
            key = identity(row)
            assert key not in found
            found[key] = row['bytes']
        data.append(packet)
    wanted = {identity(row): row['bytes'] for row in spec['expectedDataAdditions']}
    assert len(wanted) == len(spec['expectedDataAdditions']) and wanted == found
    assert len(functions) + len(data) == len(spec['packets'])
    return functions, data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('specification')
    parser.add_argument('--register', action='store_true')
    args = parser.parse_args()
    spec = read_json(ROOT / args.specification)
    before = sha256(ROOT / args.specification)
    functions, data = partition(spec)
    subset = copy.deepcopy(spec)
    subset['packets'] = functions
    subset['expectedDataAdditions'] = []
    path = ROOT / f'work/integration/cohort{spec["cohort"]}-function-reference-subset-20261106.json'
    write_json(path, subset)
    command = [sys.executable, str(ROOT / 'qualify_mixed_arm9_reference_inputs_20261105.py'),
               path.relative_to(ROOT).as_posix()]
    if args.register:
        command.append('--register')
    subprocess.run(command, cwd=ROOT, check=True)
    assert sha256(ROOT / args.specification) == before
    original = ROOT / f'evidence/verification/cohort{spec["cohort"]}-mixed-reference-inputs-20261105.json'
    assert read_json(original)['passed']
    write_json(ROOT / f'evidence/verification/cohort{spec["cohort"]}-typed-data-reference-transport-20261106.json',
        dict(passed=True, sourceCredit=0, specification=args.specification, specificationSha256=before,
             originalFunctionVerifierUnchanged=True, originalFunctionVerifierReportSha256=sha256(original),
             functionPacketCount=len(functions), dataOnlyPacketCount=len(data),
             exactDataMembershipChecked=True, dataObjectQualificationRequiredByVersionedPreparer=True,
             functionSubset=path.relative_to(ROOT).as_posix(), functionSubsetSha256=sha256(path),
             generatorSha256=sha256(__file__)))
    print(dict(passed=True, functionsPackets=len(functions), dataOnlyPackets=len(data), sourceCredit=0))


if __name__ == '__main__':
    main()
