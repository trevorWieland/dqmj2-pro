import argparse
from project import ROOT, read_json, write_json, sha256


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--save-manifest', required=True)
    parser.add_argument('--save-report', required=True)
    parser.add_argument('--save-producer', required=True)
    parser.add_argument('--save-archive', required=True)
    options = parser.parse_args()
    manifests = ['provenance/main-explicit-call-words244-coherent-ready-20261101.json',
        'provenance/arm7-core126-state76-handoff-20261101.json',
        'provenance/handoffs/ov005-record682-exact-record-conversion-20261101.json',
        'provenance/handoffs/ov005-record670-private-functional-source-20261101.json',
        'evidence/lanes/save-core/row-builder176-ready-v2-20261101.json',
        'evidence/lanes/save-core/byte-variadic-context187-ready-20261101.json',
        'provenance/arm7-core127-helper128-functional-handoff-20261101.json',
        'provenance/local-permuter-research-ready-20261101.json', options.save_manifest]
    counts = {}
    for name in manifests:
        fields = {}
        for field, rows in read_json(ROOT / name).items():
            if ('required' in field.lower() or 'existing' in field.lower()) and isinstance(rows, list):
                if not all(isinstance(row, dict) and 'path' in row and 'sha256' in row for row in rows):
                    continue
                for row in rows:
                    assert sha256(ROOT / row['path']) == row['sha256'], row['path']
                fields[field] = len(rows)
        counts[name] = fields
    write_json(ROOT / 'evidence/verification/cohort120-parallel-existing-inputs-20261101.json',
        dict(passed=True, packets=counts))
    packets = [dict(report='evidence/matches/main-explicit-call-words244-coherent-20261101.json',
        producer=['match_main_explicit_call_words244_coherent_20261101.py'], directProducer=False),
        dict(report='evidence/matches/arm7-core126-state76-20261101.json',
        producer=['match_arm7_core126_state76_20261101.py'], directProducer=True),
        dict(report='evidence/matches/ov005-20261101-record682.json',
        producer=['match_ov005_record682_20261101.py'], directProducer=False),
        dict(report=options.save_report, producer=[options.save_producer], directProducer=False)]
    additions = [{key: row[key] for key in ['module', 'mode', 'address', 'bytes']}
        for packet in packets for row in read_json(ROOT / packet['report'])['matches']]
    assert len(additions) == 7 and sum(row['bytes'] for row in additions) == 1584
    specification = dict(cohort=120, previousAcceptedCohort=119, migrations=[], packets=packets,
        expectedAdditions=additions, originalChecksRetained=True,
        postSealCommands=[['validate_arm7_core126_state76_20261101.py'],
            ['validate_arm7_core126_state76_boundary_20261101.py'],
            ['validate_arm7_core127_helper128_functional_20261101.py'],
            ['prove_ov005_record670_20261101.py'],
            ['evidence/application/save_core_row_builder176_20261101.py'],
            ['experiment_save_core_variadic_context187_20261101.py']],
        oracles=[dict(report='evidence/verification/arm7-core126-state76-controls-20261101.json',
            reproduce=['validate_arm7_core126_state76_20261101.py'])])
    write_json(ROOT / 'cohort120-parallel-specification-20261101.json', specification)
    extra = ['prepare_cohort120_parallel_20261101.py', 'stage_cohort120_parallel_20261101.py',
        'cohort120-parallel-specification-20261101.json',
        'docs/2026-11-01-cohort120-parallel-source-and-breadth.md',
        'main_explicit_call_words244_fixture_20261101.py',
        'evidence/verification/cohort120-parallel-existing-inputs-20261101.json',
        'evidence/verification/cohort120-new-lane-existing-inputs-20261101.json',
        'evidence/verification/cohort120-record682-existing-inputs-20261101.json',
        'evidence/verification/cohort120-helper128-existing-inputs-20261101.json',
        'evidence/verification/cohort120-save-resource-slot-existing-inputs-20261101.json']
    write_json(ROOT / 'cohort120-parallel-package-20261101.json', dict(cohort=120,
        manifests=manifests, archives=['arm7-core126-state76-20261101', 'ov005-record682-20261101',
            'ov005-record670-20261101', 'save-row-builder176-20261101',
            'save-byte-variadic187-20261101', 'arm7-core127-helper128-20261101', options.save_archive],
        extra=extra, traces=[]))
    print(dict(functionCandidates=len(additions), initializedBytes=sum(row['bytes'] for row in additions)))


if __name__ == '__main__':
    main()
