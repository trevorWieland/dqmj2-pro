from project import ROOT, read_json, write_json, sha256
from prepare_parallel_packet_wave import mandatory_inputs


EXPECTED = {
    'first': ('2fa8e82ac19ff25c727c6059e7c3fe7ee14a5ca90a00167404f138e62c277847',
              '5412ed502a7f7e4852d9af13bc65f89609f6990f04410a376fa0423f0e375d5a', 5, 638),
    'second': ('4b91af69ef03d0436c3538004bf8a82a9c754fb70f820ae321ef5d4a1270c467',
               '28c267e37042bbc0598307257339a4b6e86e737778e350351b2a7395f3e80d24', 8, 882)}


def main():
    proofs = []
    for label, (ready_sha, inputs_sha, functions, size) in EXPECTED.items():
        directory = ROOT / 'evidence/lanes/parallel-wave20261106/auth-resume-next' / label
        ready_path = directory / 'ready.json'; ready = read_json(ready_path)
        assert sha256(ready_path) == ready_sha
        descriptor_pin = ready['canonicalDescriptor']; descriptor = read_json(ROOT / descriptor_pin['path'])
        assert sha256(ROOT / descriptor_pin['path']) == descriptor_pin['sha256']
        input_path = (directory / 'inputs.json').relative_to(ROOT).as_posix()
        assert sha256(ROOT / input_path) == inputs_sha
        assert {'path': input_path, 'sha256': inputs_sha} in descriptor['frozenInputs']
        mandatory = {pin['path']: pin['sha256'] for pin in mandatory_inputs(descriptor['frozenInputs'])}
        for pin in read_json(ROOT / input_path)['files']:
            assert pin['path'] not in mandatory or mandatory[pin['path']] == pin['sha256']
            assert sha256(ROOT / pin['path']) == pin['sha256']
            mandatory[pin['path']] = pin['sha256']
        worker = descriptor['workerReport']
        assert worker == ready['packets'][0]['report'] and worker not in mandatory
        observations = [pin for pin in ready['files'] if pin['path'] == worker]
        assert len(observations) == 1
        other_pins = [pin for pin in ready['files'] if pin['path'] != worker]
        assert all(sha256(ROOT / pin['path']) == pin['sha256'] for pin in other_pins)
        assert ready['functions'] == functions and ready['bytes'] == size
        report = read_json(ROOT / worker)
        assert report['allPassed'] and len(report['matches']) == functions
        identities = {row['address']: row for row in ready['identities']}
        assert sum(row['bytes'] for row in report['matches']) == size
        for row in report['matches']:
            identity = identities[row['address']]
            for key in ['program', 'processor', 'module', 'mode', 'address', 'bytes', 'source', 'sourceSha256', 'targetSha256']:
                assert (row.get(key) or '') == (identity.get(key) or '')
            assert row['sourceSha256'] == sha256(ROOT / row['source'])
            assert row['exactAfterDeclaredRelocation'] and row['realLink']['exactCallerBytes']
            assert row['outputSha256'] == row['targetSha256'] == row['realLink']['linkedCallerSha256']
        proofs.append(dict(packet=label, readySha256=ready_sha, immutableInputManifestSha256=inputs_sha,
            verifiedImmutableManifestAndExternalInputs=len(mandatory), unchangedOtherReadyPins=len(other_pins),
            generatedWorkerObservation=dict(path=worker, originalObservationSha256=observations[0]['sha256'],
                currentObservationSha256=sha256(ROOT / worker)),
            workerReportIsNotAnImmutableCompilerOrReplayInput=True, functions=functions, bytes=size))
    result = dict(passed=True, sourceCredit=0, sourceOrInputExceptions=0,
        frozenReadysSourcesAndInputPinsUnchanged=True, generatedOutputsNotRestoredOrAddedToInputExclusions=True,
        proofs=proofs, generatorSha256=sha256(__file__))
    write_json(ROOT / 'evidence/verification/auth-resume-ready-output-roles-v1-20261106.json', result)
    print(dict(passed=True, packets=2, sourceCredit=0, sourceOrInputExceptions=0))


if __name__ == '__main__':
    main()
