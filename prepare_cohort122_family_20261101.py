import argparse
from project import ROOT, read_json, write_json, sha256


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--arm-manifest',required=True)
    parser.add_argument('--arm-report',required=True)
    parser.add_argument('--arm-producer',required=True)
    parser.add_argument('--arm-validator',required=True)
    parser.add_argument('--arm-control-report',required=True)
    parser.add_argument('--arm-archive',required=True)
    options=parser.parse_args()
    manifests=['provenance/main-oam-reference296-closed-ready-20261101.json',
        'provenance/handoffs/ov006-render712-exact-word-stack-interfaces-20261101.json',
        'evidence/lanes/save-core/page-word225-ready-20261101.json',options.arm_manifest,
        'provenance/arm7-core133-large1272-functional-handoff-20261101.json',
        'evidence/lanes/save-core/broader-source215-ready-20261101.json',
        'provenance/public-sdk-reference-research-ready-v4-20261101.json',
        'provenance/clean106-interpreted-order-research-ready-20261101.json',
        'provenance/main-oam-standalone-four-research-ready-20261101.json']
    counts={}
    for name in manifests:
        fields={}
        for field,rows in read_json(ROOT/name).items():
            if ('required'in field.lower()or'existing'in field.lower())and isinstance(rows,list):
                if not all(isinstance(row,dict)and'path'in row and'sha256'in row for row in rows):continue
                for row in rows:assert sha256(ROOT/row['path'])==row['sha256'],row['path']
                fields[field]=len(rows)
        counts[name]=fields
    write_json(ROOT/'evidence/verification/cohort122-family-existing-inputs-20261101.json',dict(passed=True,packets=counts))
    packets=[dict(report='evidence/matches/main-oam-reference296-closed-20261101.json',
        producer=['match_main_oam_reference296_closed_20261101.py'],directProducer=False),
        dict(report='evidence/matches/ov006-20261101-render712.json',
        producer=['match_ov006_render712_20261101.py'],directProducer=False),
        dict(report='evidence/matches/mechanics-save-20261101-lane-page-word.json',
        producer=['match_mechanics_save_20261101_lane_page_word.py'],directProducer=False),
        dict(report=options.arm_report,producer=[options.arm_producer],directProducer=True)]
    migration_addresses={0x020624B0,0x0206DCD0,0x020624D0}
    additions=[];migrations=[]
    for packet in packets:
        for row in read_json(ROOT/packet['report'])['matches']:
            item={key:row[key]for key in ['module','mode','address','bytes']}
            if packet['report'].endswith('lane-page-word.json')and int(row['address'],0)in migration_addresses:
                migrations.append(dict(**item,reason='Coordinated raw-word setter and both accepted caller declarations; original byte source/proofs preserved, zero new matching credit'))
            else:additions.append(item)
    assert len(additions)==6 and sum(row['bytes']for row in additions)==1664
    assert len(migrations)==3 and sum(row['bytes']for row in migrations)==428
    write_json(ROOT/'cohort122-family-specification-20261101.json',dict(cohort=122,previousAcceptedCohort=121,
        migrations=migrations,packets=packets,expectedAdditions=additions,originalChecksRetained=True,
        postSealCommands=[[options.arm_validator],['validate_arm7_core133_large1272_functional_20261101.py'],
            ['replay_save_core_breadth215_20261101.py'],
            ['evidence/application/save_core_controller_default210_20261101.py'],
            ['evidence/application/save_core_stack_stride213_20261101.py']],
        oracles=[dict(report=options.arm_control_report,reproduce=[options.arm_validator])]))
    write_json(ROOT/'cohort122-family-package-20261101.json',dict(cohort=122,manifests=manifests,
        archives=['ov006-render712-20261101','save-page-word225-20261101',options.arm_archive,
            'arm7-core133-large1272-20261101','save-broader-source215-20261101'],traces=[],
        extra=['prepare_cohort122_family_20261101.py','stage_cohort122_family_20261101.py',
            'cohort122-family-specification-20261101.json','docs/2026-11-01-cohort122-family-sources-and-interface-migrations.md',
            'evidence/verification/cohort122-family-existing-inputs-20261101.json',
            'evidence/verification/cohort122-render712-existing-inputs-20261101.json',
            'evidence/verification/cohort122-page225-existing-inputs-20261101.json',
            'evidence/verification/cohort122-arm7-large133-existing-inputs-20261101.json',
            'evidence/verification/cohort122-save-broader215-existing-inputs-20261101.json']))
    print(dict(newFunctionCandidates=6,initializedBytes=1664,zeroByteMigrations=3,migrationBytes=428))


if __name__=='__main__':
    main()
