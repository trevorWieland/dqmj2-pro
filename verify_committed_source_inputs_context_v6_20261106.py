import subprocess
import sys
from project import ROOT, read_json, write_json, sha256
import verify_committed_source_inputs_context_v5_20261106 as original
from qualify_ov006_aes_reference_v1_20261106 import REPORT, qualify


def main():
    cohort = int(sys.argv[sys.argv.index('--cohort') + 1])
    for name in ['verify_committed_source_inputs_context_v6_20261106.py',
                 'qualify_ov006_aes_reference_v1_20261106.py']:
        assert subprocess.check_output(['git', 'show', 'HEAD:' + name], cwd=ROOT) == (ROOT / name).read_bytes()
    registry = read_json(ROOT / 'recovery.json')
    assert subprocess.check_output(['git', 'show', 'HEAD:recovery.json'], cwd=ROOT) == (ROOT / 'recovery.json').read_bytes()
    selected = [batch for batch in registry['batches'] if batch['report'] == REPORT]
    assert len(selected) == 1
    assert not any(path.startswith('extract/') for path in selected[0]['sourceHashes'])
    proof = qualify()
    original.main()
    write_json(ROOT / f'evidence/verification/cohort{cohort}-ov006-aes-committed-source-context-v6-20261106.json',
        dict(passed=True, sourceCredit=0, originalV5AndAllUnderlyingAuditsCompleted=True,
            exactCommittedRegistryUnprojected=True, nativeImageNotRegisteredAsAuthoredSource=True,
            noReferenceExclusionOrPrivateBatchProjectionNeeded=True, scopedAesProof=proof,
            originalSourceRegistrySha256=sha256(ROOT / 'recovery.json'), generatorSha256=sha256(__file__)))


if __name__ == '__main__':
    main()
