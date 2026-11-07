import copy
import os
from unittest.mock import patch
from project import ROOT, read_json, write_json, sha256, now
import build_modules as builder


def identity(unit):
    return tuple(unit.get(k) for k in ['module', 'kind', 'start', 'end', 'source', 'sourceSha256', 'sha256'])


def main():
    work = ROOT / 'work/mb-register-module-route-controls/fd703c20e7d0'
    original = read_json(work / 'evidence/latest.json')
    assert original['failure'].startswith('TimeoutExpired:') and '180 seconds' in original['failure']
    assert all(c['exitCode'] == 0 for c in original['commands'])
    project = read_json(ROOT / 'project.json')
    linker, dsd = ROOT / project['linker'], ROOT / project['dsd']
    assert sha256(linker) == builder.LINKER_HASH and sha256(dsd) == builder.DSD_HASH
    link_work = work / 'link-work'
    output = link_work / 'retry600-linked.elf'
    result_path = work / 'prepared-link-retry-v1.json'
    assert not result_path.exists() and not output.exists()
    inputs = {p['path']: p['sha256'] for p in original['objects']}
    for path, expected in inputs.items():
        assert sha256(path) == expected
    metadata = {name: sha256(link_work / name) for name in ['objects.txt', 'arm9.lcf', 'config.yaml']}
    baseline = read_json(ROOT / 'evidence/linking/latest.json')
    assert baseline['allModuleBytesExact'] and baseline['symbolCheckPassed']
    assert {identity(u) for u in baseline['sourceUnits']} <= {identity(u) for u in original['sourceUnits']}
    assert len(original['sourceUnits']) == len(baseline['sourceUnits']) + 2
    report = copy.deepcopy(original)
    report.pop('failure')
    report['commands'] = []
    env = dict(os.environ, LM_LICENSE_FILE=str(ROOT / project['license']))
    command = [linker, '-nostdlib', '-nodeadstrip', '-interworking', '-proc', 'arm946e',
        '-main', 'Entry', '-sym', 'on', '-map', link_work / 'arm9.lcf',
        '@' + str(link_work / 'objects.txt'), '-o', output]
    write_json(result_path, dict(state='running', sourceCredit=0, startedUtc=now(),
        actualPreviousSubprocessTerminatedAt180Seconds=True, preparedObjectInputsChecked=len(inputs),
        preparedMetadataHashes=metadata, command=list(map(str, command)), timeoutSeconds=600))
    print(dict(started=True, preparedObjects=len(inputs), timeoutSeconds=600), flush=True)
    with patch.object(builder, 'WORK', link_work):
        linked = builder.run(command, link_work, env, report, timeout=600)
        modules = builder.run([dsd, 'check', 'modules', '--config-path', link_work / 'config.yaml', '--fail'], link_work, env, report)
        symbols = linked and builder.run([dsd, 'check', 'symbols', '--config-path', link_work / 'config.yaml', '--elf-path', output, '--fail'], link_work, env, report)
        report['modules'] = []
        builder.compare_modules(report)
    assert all(sha256(path) == expected for path, expected in inputs.items())
    assert metadata == {name: sha256(link_work / name) for name in metadata}
    passed = linked and modules and symbols and len(report['modules']) == 11 and all(m['exactBytes'] for m in report['modules'])
    controls = read_json(ROOT / 'evidence/verification/mb-register-module-route-v1-qualification-20261106.json')['controls']
    assert controls['passed'] and len(controls['rejectedActualElfMutations']) == 10
    result = dict(passed=passed, sourceCredit=0, state='passed' if passed else 'failed', finishedUtc=now(),
        preparedSourceAndAllObjectInputsUnchanged=True, previousAcceptedCorpusIncluded=True,
        allBaselineSourceUnitIdentitiesPreserved=True, baselineSourceUnits=len(baseline['sourceUnits']),
        qualifiedSourceUnits=len(original['sourceUnits']), addedFunctionBytes=656, newSourceLocalBssBytes=1,
        addedInitializedStorageBytes=0, hostArm9ModuleComparisons=11, allModuleBytesExact=passed,
        strictSymbolsPassed=symbols, controls=controls, commands=report['commands'], modules=report['modules'],
        route=dict(path='mb_register_module_route_v1_20261106.py', sha256=sha256(ROOT / 'mb_register_module_route_v1_20261106.py')),
        originalFailedReportSha256=sha256(work / 'evidence/latest.json'), preparedMetadataHashes=metadata,
        privateLinkedElf=dict(path=output.relative_to(ROOT).as_posix(), sha256=sha256(output)),
        allOtherProcessorSharedGatesStillRequired=True, globalConsumerAdoptionProven=False, generatorSha256=sha256(__file__))
    write_json(result_path, result)
    write_json(ROOT / 'evidence/verification/mb-register-module-route-v2-qualification-20261106.json', result)
    print(dict(passed=passed, previousAcceptedCorpusIncluded=True, moduleComparisons=11), flush=True)
    raise SystemExit(0 if passed else 1)


if __name__ == '__main__':
    main()
