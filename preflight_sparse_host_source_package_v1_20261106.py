import argparse
import contextlib
import json
import sys
from pathlib import Path
from unittest.mock import patch
from project import ROOT, read_json, write_json, sha256
import build_modules as builder


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('specification')
    parser.add_argument('--label', required=True)
    options = parser.parse_args()
    assert options.label and all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in options.label)
    spec_path = ROOT / options.specification
    specification_hash = sha256(spec_path)
    spec = read_json(spec_path)
    reports, expected, source_pins = [], [], {}
    for packet in spec['packets']:
        path = ROOT / packet['report']
        report = read_json(path)
        if report.get('program') or report.get('processor') == 'arm7' or report.get('module', '').startswith('arm7'):
            continue
        rows = report.get('matches', report.get('functionMatches', [])) + report.get('dataMatches', [])
        assert rows
        for row in rows:
            item = {**report, **row}
            assert not item.get('program') and item.get('processor', 'arm9') == 'arm9'
            assert not item['module'].startswith('utility-')
            assert item.get('exactBytes') or item.get('exactAfterDeclaredRelocation')
            assert sha256(ROOT / item['source']) == item['sourceSha256']
            assert sha256(ROOT / item['object']) == item['objectSha256']
            for key in ['source', 'object']:
                source_pins[item[key]] = item[key + 'Sha256']
            expected.append((item['module'], item['name'], int(item['address'], 0), item.get('bytes', item.get('size'))))
        reports.append(path)
        source_pins[packet['report']] = sha256(path)
    assert reports and len(expected) == len(set(expected))
    work = ROOT / 'build' / ('sparse-host-' + options.label)
    evidence = ROOT / 'evidence/verification' / ('sparse-host-' + options.label)
    assert not work.exists() and not evidence.exists()
    work.mkdir(parents=True)
    base = work / 'base-units.json'
    write_json(base, dict(schemaVersion=1, units=[], nativeSymbols={}))
    context_needed = any(name == 'native_main_0209770c' for module, name, address, size in expected)
    route = contextlib.nullcontext()
    context_qualification = None
    if context_needed:
        from qualified_auth_context_guard_v2_20261106 import verify
        from auth_context_route_v2_20261106 import module_route
        context_qualification = verify()
        route = module_route(builder)
    arguments = ['build_modules.py', '--source-units', base.relative_to(ROOT).as_posix()]
    for report in reports:
        arguments.extend(['--source-matches', report.relative_to(ROOT).as_posix()])
    with patch.object(builder, 'WORK', work), patch.object(builder, 'EVIDENCE', evidence), patch.object(sys, 'argv', arguments), route:
        result = builder.main()
    assert result == 0
    linked = read_json(evidence / 'latest.json')
    assert linked['allModuleBytesExact'] and linked['symbolCheckPassed'] and linked['mixedScaffoldingRomBuilt']
    assert len(linked['modules']) == 11 and all(row['exactBytes'] for row in linked['modules'])
    actual = [(row['module'], row.get('function', row.get('symbol')), int(row['start'], 0), int(row['end'], 0) - int(row['start'], 0))
              for row in linked['sourceUnits']]
    assert sorted(actual) == sorted(expected)
    assert sha256(spec_path) == specification_hash
    for path, expected_hash in source_pins.items():
        assert sha256(ROOT / path) == expected_hash
    receipt = dict(passed=True, sourceCredit=0, sharedAcceptanceCredit=0,
        specification=options.specification, specificationSha256=specification_hash,
        sparseCandidateUnits=len(actual), sparseCandidateInitializedBytes=sum(row[3] for row in actual),
        complete11HostModuleBytesExact=True, completeHostSymbolChecksPassed=True,
        allCandidateSourceObjectsAndReportsUnchanged=True, originalBuilderMainAndChecksRetained=True,
        privateBuild=work.relative_to(ROOT).as_posix(), privateEvidence=evidence.relative_to(ROOT).as_posix(),
        constructedScaffoldingRomSha256=linked['mixedScaffoldingRomSha256'],
        contextQualification=context_qualification, generatorSha256=sha256(Path(__file__)),
        limitations=['Only the candidate host units replace original executable scaffolding in this preflight',
                    'Accepted-source coexistence, ARM7 and embedded programs, regressions, exact-ROM normalization, capture and committed audits remain shared requirements',
                    'No original ROM hash equality or source-only ROM proof is claimed'])
    write_json(evidence / 'qualification.json', receipt)
    print(json.dumps(dict(passed=True, units=len(actual), initializedBytes=sum(row[3] for row in actual), exactHostModules=11, sourceCredit=0)))


if __name__ == '__main__':
    main()
