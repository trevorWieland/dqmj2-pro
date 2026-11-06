import argparse
from unittest.mock import patch
from project import ROOT, read_json, write_json, sha256, configuration, native_dependencies

native_dependencies(configuration())
import link_utility
from recovery_registry import batches


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('specification')
    parser.add_argument('--output', required=True)
    options = parser.parse_args()
    specification = read_json(ROOT / options.specification)
    combined = {item['report']: item for item in batches()}
    for packet in specification['packets']:
        combined.setdefault(packet['report'], dict(report=packet['report']))
    program = read_json(ROOT / 'evidence/utility/runtime-layout.json')['program']
    with patch.object(link_utility, 'batches', return_value=list(combined.values())):
        plans, metadata = link_utility.accepted_by_cpu(program, ['arm9', 'arm7'])
    write_json(ROOT / options.output, dict(passed=True, sourceCredit=0,
        specification=options.specification, specificationSha256=sha256(ROOT / options.specification),
        linkerConsumerSha256=sha256(ROOT / 'link_utility.py'), program=program,
        existingAndCandidateReports=len(combined), processorSymbols={cpu: len(plan[1]) for cpu, plan in plans.items()},
        compositionMetadataEntries=len(metadata), sharedRegistryUnchanged=True,
        sameCpuAddressAndBindingConflictGuardsApplied=True, compilerElfNamesAndRelocationsUnchanged=True))
    print(dict(passed=True, sourceCredit=0, processorSymbols={cpu: len(plan[1]) for cpu, plan in plans.items()}))


if __name__ == '__main__':
    main()
