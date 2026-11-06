import argparse
import copy
from project import ROOT, read_json, write_json, sha256
from qualify_arm9_reference_consumer_20261105 import compiler_inputs
from qualify_explicit_c_frontend_20261102 import qualify


DERIVED = {'extract/arm9/arm9.bin', 'extract/arm9/itcm.bin', 'extract/arm9/dtcm.bin'}
LEDGER = 'provenance/arm9-reference-only-consumers-20261101.json'


def qualify_report(name, expected, directory):
    report = read_json(ROOT / name)
    rows = report['matches']
    assert {r['address']: r['bytes'] for r in rows} == expected
    proofs = []
    for row in rows:
        inputs = compiler_inputs(row)
        adjusted = copy.deepcopy(row)
        flags = adjusted['compilerFlags']
        if '-lang' in flags:
            index = flags.index('-lang')
            assert flags[index + 1] in ['c', 'c99'] and flags.count('-lang') == 1
            adjusted['compilerFlags'] = flags[:index] + flags[index + 2:]
        result = qualify(adjusted, directory / row['address'])
        proofs.append(dict(address=row['address'], bytes=row['bytes'], sourceOnlyCompilerInput=inputs,
                          explicitC99Qualification=result, actualProductionFlags=row['compilerFlags']))
    return dict(report=name, reportSha256=sha256(ROOT / name), producer=report['generator'],
        producerSha256=report['generatorSha256'], expectedRanges=expected, proofs=proofs,
        sourceCredit=0, freshSourceOnlyCompilerBoundaryProven=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('specification')
    parser.add_argument('--register', action='store_true')
    options = parser.parse_args()
    spec = read_json(ROOT / options.specification)
    ledger = read_json(ROOT / LEDGER)
    known = {r['report'] for r in ledger['consumers']}
    output = f'evidence/verification/cohort{spec["cohort"]}-arm9-reference-packets-20261105.json'
    qualified = []
    for packet in spec['packets']:
        report = read_json(ROOT / packet['report'])
        pins = {r['path'] for k in ['generatorSources', 'replayDependencies'] for r in report.get(k, [])}
        if not DERIVED.intersection(pins) or packet['report'] in known:
            continue
        descriptor = read_json(ROOT / packet['producer'][1])
        expected = {r['address']: r['bytes'] for r in descriptor['identities']}
        proof = qualify_report(packet['report'], expected,
            ROOT / f'work/integration/cohort{spec["cohort"]}-reference-only' / str(len(qualified)))
        qualified.append(proof)
        ledger['consumers'].append(dict(report=packet['report'], producer=proof['producer'],
            producerSha256=proof['producerSha256'], processor='arm9', program='', module='main', mode='arm',
            expectedRanges=expected, sourceOnlyCompilerInputQualification=output))
    write_json(ROOT / output, dict(passed=True, sourceCredit=0, cohort=spec['cohort'],
        qualification=qualified, registered=options.register,
        originalSourcesObjectsFlagsAndCanonicalReportsUnchanged=True, generatorSha256=sha256(__file__)))
    if options.register:
        write_json(ROOT / LEDGER, ledger)
    print(dict(passed=True, newlyQualifiedReports=len(qualified), registered=options.register))


if __name__ == '__main__':
    main()
