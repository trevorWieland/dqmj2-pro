import argparse
from pathlib import Path
from project import ROOT, read_json, write_json, sha256
from prepare_parallel_packet_wave import EXCLUDED, mandatory_inputs
from seal_recovery_evidence_20261031 import code_closure
from source_packet_contracts import local
from replay_frozen_runtime import mapping_context

TEXT = {'.py','.c','.cpp','.h','.inc','.s','.json','.txt','.csv','.md'}

def create(specification, intake_configuration, document=None):
    spec = read_json(local(specification))
    intake = read_json(local(intake_configuration))
    cohort = spec['cohort']
    declared, private, copied = {}, {}, {}
    replacements, snapshots, contexts = {}, set(), {}
    for packet in spec['packets']:
        descriptor_name = packet['producer'][1]
        descriptor = read_json(local(descriptor_name))
        if not descriptor.get('runtimeInputMapping'):
            continue
        if descriptor['producer'] != ['replay_frozen_runtime.py', descriptor['runtimeInputMapping']]:
            raise ValueError('Runtime input mapping must be owned by its explicit replay adapter')
        mapping = read_json(local(descriptor['runtimeInputMapping']))
        context = mapping_context(mapping)
        snapshot = context.snapshot.relative_to(ROOT).as_posix()
        replacement = (snapshot, mapping['expectedSha256'])
        previous = replacements.setdefault(mapping['fromPath'], replacement)
        if previous != replacement:
            raise ValueError('Conflicting frozen runtime input mappings')
        snapshots.add(snapshot)
        contexts[descriptor_name] = mapping
    def include(name, expected=None):
        if name in replacements:
            snapshot, frozen = replacements[name]
            if expected != frozen:
                raise ValueError('Logical frozen input requires its exact original pin')
            name = snapshot
        path = local(name)
        name = path.relative_to(ROOT).as_posix()
        digest = sha256(path)
        if expected is not None and digest != expected:
            raise ValueError('Source package pin differs: '+name)
        root = Path(name).parts[0]
        if root in EXCLUDED or path.suffix.lower() not in TEXT:
            private[name] = digest
            if root in {'deps','tools','inputs'}:
                copied[name] = digest
            return
        if name in declared and declared[name] != digest:
            raise ValueError('Conflicting source package pins')
        declared[name] = digest
    include(specification)
    if document:
        include(document)
    for item in intake['readyPackets']:
        ready = read_json(local(item['path']))
        include(item['path'],item['sha256'])
        produced = {packet['report'] for packet in ready['packets']}
        for pin in ready['files']:
            include(pin['path'],None if pin['path'] in produced else pin['sha256'])
    for item in intake.get('requiredCorrections',[]):
        include(item['path'],item['sha256'])
    for packet in spec['packets']:
        include(packet['report'])
        descriptor_name = packet['producer'][1]
        include(descriptor_name)
        descriptor = read_json(local(descriptor_name))
        if descriptor.get('runtimeInputMapping'):
            include(descriptor['runtimeInputMapping'])
        if descriptor_name in contexts:
            with mapping_context(contexts[descriptor_name]):
                mandatory = mandatory_inputs(descriptor['frozenInputs'])
        else:
            mandatory = mandatory_inputs(descriptor['frozenInputs'])
        for pin in mandatory:
            include(pin['path'],pin['sha256'])
        report = read_json(local(packet['report']))
        for pin in report.get('generatorSources',[]):
            include(pin['path'],pin['sha256'])
        for row in report.get('matches',[]) + report.get('dataMatches',[]):
            include(row['source'],row['sourceSha256'])
            for pin in row.get('sourceDependencies',[]):
                include(pin['path'],pin['sha256'])
    support = ['source_packet_package.py','prepare_source_packet_cohort.py','source_cohort_transaction.py',
        'run_source_packet_cohort.py','finish_source_packet_cohort.py','staged_git_checks.py']
    for name in code_closure(support):
        include(name)
    manifest = f'provenance/cohort{cohort}-source-packet-files.json'
    copies = f'provenance/cohort{cohort}-source-packet-copied-inputs.json'
    write_json(ROOT/manifest,dict(sourceCredit=0,producedReportPinsDescribePreSealHandoff=True,
        files=[dict(path=name,sha256=value) for name,value in sorted(declared.items())],
        privateComparisonInputs=[dict(path=name,sha256=value) for name,value in sorted(private.items())],
        privateRuntimeInputs=[dict(path=name,sha256=private[name],committedAsAuthoredSource=False,
            copiedByFreshInputSnapshot=True,sourceCredit=0) for name in sorted(snapshots)],
        executableInputsCommitted=False))
    write_json(ROOT/copies,dict(sourceCredit=0,committedAsAuthoredSource=False,
        files=[dict(path=name,sha256=value) for name,value in sorted(copied.items())]))
    package = f'cohort{cohort}-source-packet-package.json'
    write_json(ROOT/package,dict(cohort=cohort,manifests=[manifest,copies],archives=[],traces=[],
        extra=[*support,specification,f'evidence/verification/cohort-2026-10-29-{cohort}.json']))
    return dict(package=package,declaredTextFiles=len(declared),privateComparisonFiles=len(private),copiedToolInputs=len(copied),sourceCredit=0)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('specification')
    parser.add_argument('intake_configuration')
    parser.add_argument('--document')
    args = parser.parse_args()
    print(create(args.specification,args.intake_configuration,args.document))

if __name__ == '__main__':
    main()
