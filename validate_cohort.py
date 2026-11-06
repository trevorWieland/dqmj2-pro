import argparse
import subprocess
import sys
from project import ROOT, configuration, now, read_json, sha256, verify_inputs, write_json
from recovery_registry import verify_sources


def main(number):
    record = ROOT / f'evidence/verification/cohort-2026-10-29-{number}.json'
    cohort = read_json(record)
    registry_hash = sha256(ROOT / 'recovery.json')
    preference_path = ROOT / 'source-preferences.json'
    preference_hash = sha256(preference_path) if preference_path.is_file() else None
    if cohort.get('sourcePreferenceSha256') not in (None, preference_hash):
        raise ValueError('Source preference snapshot changed before validation')
    interpreted_registry = ROOT / 'interpreted-recovery.json'
    interpreted_hash = sha256(interpreted_registry) if interpreted_registry.is_file() else None
    if cohort.get('interpretedRegistrySha256') not in (None, interpreted_hash):
        raise ValueError('Interpreted source registry snapshot changed before validation')
    if registry_hash != cohort['sourceRegistrySha256']:
        raise ValueError('Cohort registry snapshot changed before validation')
    verify_sources()
    if interpreted_hash != (sha256(interpreted_registry) if interpreted_registry.is_file() else None):
        raise ValueError('Interpreted source registry changed during validation')
    initial_inputs = verify_inputs(configuration())
    commands = [
        ['reproduce.py'],
        ['evidence/save/native_getters.py', '--rom', str(ROOT / 'inputs/game.nds'),
         '--save', str(ROOT / 'inputs/save.sav'), '--deps', str(ROOT / 'deps/native'),
         '--output', str(ROOT / 'evidence/save/native-getter-results.json')],
        ['link_arm7.py'], ['link_utility.py', '--clean'], ['integrate.py', '--clean'],
        ['verify_build_status.py'], ['verify_linker_layout.py'],
        ['pack_exact.py', '--prepare', '--linked-rom', 'build/link-work/roundtrip.nds'],
        ['validate_packaging.py'], ['make_manifest.py'], ['audit_boundaries.py'],
        ['make_manifest.py'], ['validate_evidence.py'], ['verify_workspace.py'],
    ]
    if preference_hash:
        commands.insert(commands.index(['audit_boundaries.py']), ['verify_linked_preferences.py'])
    history = {'createdUtc': now(), 'cohort': number, 'steps': []}
    evidence = ROOT / f'evidence/verification/cohort{number}-validation-driver.json'
    for index, command in enumerate(commands):
        log = ROOT / f'logs/integration/cohort{number}-validation-{index:02d}.txt'
        log.parent.mkdir(parents=True, exist_ok=True)
        with log.open('w', encoding='utf-8') as stream:
            process = subprocess.run([sys.executable, *command], cwd=ROOT,
                                     stdout=stream, stderr=subprocess.STDOUT)
        step = {'command': command, 'exitCode': process.returncode,
                'log': log.relative_to(ROOT).as_posix(), 'logSha256': sha256(log)}
        history['steps'].append(step)
        write_json(evidence, history)
        print(step, flush=True)
        if process.returncode and command[0] != 'verify_workspace.py':
            raise RuntimeError('Cohort validation failed at ' + command[0])
    verify_sources()
    if preference_hash != (sha256(preference_path) if preference_path.is_file() else None):
        raise ValueError('Source preferences changed during validation')
    if interpreted_hash != (sha256(interpreted_registry) if interpreted_registry.is_file() else None):
        raise ValueError('Interpreted source registry changed during validation')
    if initial_inputs != verify_inputs(configuration()) or sha256(ROOT / 'recovery.json') != registry_hash:
        raise ValueError('Inputs or source registry changed during validation')
    workspace = read_json(ROOT / 'evidence/verification/workspace.json')
    changes = workspace['isolation']['observedChanges']
    if workspace['gitRemotes'] or not workspace['sourcePolicy']['passed'] or any(row['category'] != 'application' for row in changes):
        raise ValueError('Source policy or isolated baseline validation failed')
    manifest = read_json(ROOT / 'manifest.json')
    if cohort.get('interpretedInventoryRequired'):
        interpreted = manifest.get('interpretedCoverage', {})
        if not interpreted.get('inventoryAvailable') or interpreted.get('overallGameCompletionPercentage') is not None:
            raise ValueError('Current interpreted inventory is absent or misreported as overall completeness')
        for expected, actual in [('expectedInterpretedSourceUnits', 'ordinarySourceUnitsRecovered'),
                                 ('expectedInterpretedSourceBytes', 'ordinarySourceBytesRecovered'),
                                 ('expectedInterpretedSourceDefinitions', 'authoredSourceDefinitionsRecovered'),
                                 ('expectedEmptyRoutineInstances', 'emptyRoutineInstances'),
                                 ('expectedEmptyRoutineBytes', 'emptyRoutineSourceBytes'),
                                 ('expectedNonemptyRoutineInstances', 'nonemptyRoutineInstances'),
                                 ('expectedNonemptyRoutineBytes', 'nonemptyRoutineSourceBytes'),
                                 ('expectedCopyOnlyRoutineInstances', 'copyOnlyRoutineInstances'),
                                 ('expectedCopyOnlyRoutineBytes', 'copyOnlyRoutineSourceBytes'),
                                 ('expectedNonemptyNoncopyRoutineInstances', 'nonemptyNoncopyRoutineInstances'),
                                 ('expectedNonemptyNoncopyRoutineBytes', 'nonemptyNoncopyRoutineSourceBytes')]:
            if expected in cohort and cohort[expected] != interpreted[actual]:
                raise ValueError('Interpreted source credit differs from its accepted range proof')
    for expected, actual in [('expectedSourceMatchedFunctions', 'functionMatched'),
                             ('expectedSourceLinkedBytes', 'sourceLinkedBytes')]:
        if expected in cohort and cohort[expected] != manifest[actual]:
            raise ValueError('Measured accepted coverage differs from the cohort plan: ' + actual)
    negative = read_json(ROOT / 'evidence/verification/evidence-freshness.json')
    if not negative['passed'] or not manifest['exactContainerMatchWithScaffolding']:
        raise ValueError('Current match or negative acceptance evidence failed')
    if not all(row.get('linkOutput', {}).get('exactBytes') for row in manifest['modules']):
        raise ValueError('A complete initialized module comparison failed')
    product = ROOT / 'build/exact-layout.nds'
    digest = sha256(product)
    if digest != configuration()['romSha256']:
        raise ValueError('Current exact-layout ROM differs from the measured input')
    getters = read_json(ROOT / 'evidence/save/native-getter-results.json')
    if not getters['sourceFilesUnchanged']:
        raise ValueError('Getter verification changed source inputs')
    cohort.update(linksPending=False, acceptedBuildCreatedUtc=manifest['createdUtc'],
                  sourceMatchedFunctions=manifest['functionMatched'], sourceLinkedBytes=manifest['sourceLinkedBytes'],
                  manifestSha256=sha256(ROOT / 'manifest.json'),
                  moduleComparisonsExact=len(manifest['modules']),
                  exactRom={'bytes': product.stat().st_size, 'sha256': digest},
                  negativeAcceptanceChecksPassed=True, sourcePolicyPassed=True,
                  baselineAndInputsUnchanged=True, applicationObservedUnchanged=not bool(changes),
                  getterComparisons=getters['totalComparisons'],
                  getterReportSha256=sha256(ROOT / 'evidence/save/native-getter-results.json'),
                  sourceCoveragePercentage=100 * manifest['sourceLinkedBytes'] / sum(row['bytes'] for row in manifest['modules']),
                  sourceReconstructionComplete=manifest['sourceReconstructionComplete'],
                  wholeRomMatchedFromSource=manifest['wholeRomMatchedFromSource'])
    write_json(record, cohort)
    print({key: cohort[key] for key in ('linksPending', 'sourceMatchedFunctions', 'sourceLinkedBytes',
                                      'sourceCoveragePercentage', 'sourceReconstructionComplete')})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', required=True, type=int)
    main(parser.parse_args().cohort)
