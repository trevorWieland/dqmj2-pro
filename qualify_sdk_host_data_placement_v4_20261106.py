import copy
from project import ROOT, read_json, write_json, sha256
from replay_sdk_host_data_placement_v4_20261106 import placement


def main():
    linked = read_json(ROOT / 'evidence/verification/sdk-host-placement-v4-preflight/latest.json')
    assert linked['allModuleBytesExact'] and linked['symbolCheckPassed'] and len(linked['modules']) == 11
    assert linked['mixedScaffoldingRomBuilt']
    assert len(linked['sourceUnits']) == 6 and sum(r['compiledBytes'] for r in linked['sourceUnits']) == 3094
    proofs, controls, descriptors = [], [], []
    for category in ['constant', 'sound']:
        name = f'provenance/cohort166-sdk-{category}-data-host-placement-v4-20261106.json'
        descriptor = read_json(ROOT / name)
        prior = read_json(ROOT / descriptor['originalNamespaceDescriptor'])
        before = read_json(ROOT / prior['output'])['dataMatches']
        after = read_json(ROOT / descriptor['output'])['dataMatches']
        assert len(before) == len(after)
        descriptors.append(dict(path=name, sha256=sha256(ROOT / name)))
        for original, changed in zip(before, after):
            expected, proof = placement(original, descriptor)
            assert expected == changed
            assert {k: v for k, v in changed.items() if k not in ['nativeAlias', 'nativeDataDeclaration']} == original
            proofs.append(proof)
        if category == 'sound':
            sample, sample_descriptor = copy.deepcopy(before[0]), descriptor
    variants = [('program', 'child.srl'), ('processor', 'arm7'), ('module', 'ov000'),
                ('kind', 'function'), ('mode', 'arm'), ('address', '0x20d8356'),
                ('bytes', 1540), ('targetSha256', '0' * 64), ('exactBytes', False), ('nativeAlias', 'invented')]
    for key, value in variants:
        row = copy.deepcopy(sample)
        row[key] = value
        try:
            placement(row, sample_descriptor)
        except AssertionError:
            controls.append(dict(case=key, rejected=True))
        else:
            raise AssertionError('Incorrect placement accepted: ' + key)
    for key in ['originalConfiguredSymbolsSha256', 'dataClaimSha256']:
        descriptor = copy.deepcopy(sample_descriptor)
        descriptor[key] = '0' * 64
        try:
            placement(sample, descriptor)
        except AssertionError:
            controls.append(dict(case=key, rejected=True))
        else:
            raise AssertionError('Incorrect declaration evidence accepted: ' + key)
    assert len(proofs) == 6 and sum(p['generatedConfigOnlyDataDeclaration'] is not None for p in proofs) == 2
    receipt = dict(passed=True, sourceCredit=0, dataAcceptanceCredit=0, hostObjects=6, initializedBytes=3094,
        all11Arm9ModuleBytesExact=True, symbolChecksPassed=True, scaffoldingRomConstructed=True,
        constructedRomSha256=linked['mixedScaffoldingRomSha256'], originalLengthShaRomCheckPerformed=False,
        originalBuilderMainAndChecksUnchanged=True, isolatedGeneratedWorkAndEvidence=True,
        productionReportUntouched=True, wholeSourceObjectFlagsNativeHashesAndRelocationsUnchanged=True,
        actualCExportsUnchanged=True, configuredDataAliases=4, generatedConfigOnlyMeasuredDataBoundaryDeclarations=2,
        placementProofs=proofs, negativeControls=controls, descriptors=descriptors,
        fullPrivateBuild='evidence/verification/sdk-host-placement-v4-preflight/latest.json',
        fullPrivateBuildSha256=sha256(ROOT / 'evidence/verification/sdk-host-placement-v4-preflight/latest.json'),
        generatorSha256=sha256(ROOT / 'qualify_sdk_host_data_placement_v4_20261106.py'),
        transportSha256=sha256(ROOT / 'replay_sdk_host_data_placement_v4_20261106.py'),
        limitations=['The private builder checks 11 host ARM9 modules; all 20 runtime modules require the shared sequence',
                    'The raw constructed ROM still requires the existing exact-ROM stage; no original ROM hash equality is claimed',
                    'Two initial observation assertions expected all20 rather than11 host modules and raw ROM hash equality; original outputs are preserved'])
    write_json(ROOT / 'evidence/verification/sdk-host-data-placement-v4-qualification-20261106.json', receipt)
    print(dict(passed=True, hostObjects=6, initializedBytes=3094, negativeControls=len(controls), exactHostModules=11))


if __name__ == '__main__':
    main()
