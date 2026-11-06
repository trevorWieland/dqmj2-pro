import subprocess
import sys
from project import ROOT, read_json, write_json, sha256
import verify_committed_source_inputs_context_v6_20261106 as original
from qualify_ov006_md5_reference_v1_20261106 import REPORT, qualify
from qualify_ov006_crypto_reference_v1_20261106 import REPORT as CRYPTO_REPORT, qualify as qualify_crypto
from qualify_ov006_md5_helpers_reference_v1_20261106 import REPORT as HELPERS_REPORT, qualify as qualify_helpers
from qualify_arm7_wm_second_context_v1_20261106 import REPORT as ARM7_REPORT, qualify as qualify_arm7
from qualify_arm7_wm_third_context_v1_20261106 import REPORT as CALLBACK_REPORT, qualify as qualify_callbacks


def main():
    cohort = int(sys.argv[sys.argv.index('--cohort') + 1])
    for name in ['verify_committed_source_inputs_context_v7_20261106.py',
                 'qualify_ov006_md5_reference_v1_20261106.py', 'qualify_ov006_crypto_reference_v1_20261106.py',
                 'qualify_ov006_md5_helpers_reference_v1_20261106.py', 'qualify_arm7_wm_second_context_v1_20261106.py',
                 'qualify_arm7_wm_third_context_v1_20261106.py']:
        assert subprocess.check_output(['git', 'show', 'HEAD:' + name], cwd=ROOT) == (ROOT / name).read_bytes()
    registry = read_json(ROOT / 'recovery.json')
    assert subprocess.check_output(['git', 'show', 'HEAD:recovery.json'], cwd=ROOT) == (ROOT / 'recovery.json').read_bytes()
    selected = [batch for batch in registry['batches'] if batch['report'] == REPORT]
    assert len(selected) == 1 and not any(path.startswith('extract/') for path in selected[0]['sourceHashes'])
    proof = qualify()
    crypto_batches = [batch for batch in registry['batches'] if batch['report'] == CRYPTO_REPORT]
    assert len(crypto_batches) == 1 and not any(path.startswith('extract/') for path in crypto_batches[0]['sourceHashes'])
    crypto_proof = qualify_crypto()
    helper_batches = [batch for batch in registry['batches'] if batch['report'] == HELPERS_REPORT]
    assert len(helper_batches) == 1 and not any(path.startswith('extract/') for path in helper_batches[0]['sourceHashes'])
    helper_proof = qualify_helpers()
    arm7_batches = [batch for batch in registry['batches'] if batch['report'] == ARM7_REPORT]
    assert len(arm7_batches) == 1
    arm7_proof = qualify_arm7()
    callback_batches = [batch for batch in registry['batches'] if batch['report'] == CALLBACK_REPORT]
    assert len(callback_batches) == 1
    callback_proof = qualify_callbacks()
    original.main()
    write_json(ROOT / f'evidence/verification/cohort{cohort}-ov006-md5-committed-source-context-v7-20261106.json',
        dict(passed=True, sourceCredit=0, allOriginalV6AndUnderlyingAuditsCompleted=True,
            exactCommittedRegistryUnprojected=True, noReferenceExclusionOrPrivateBatchProjectionNeeded=True,
            scopedMd5Proof=proof, scopedCryptoProof=crypto_proof, originalArithmeticRecordPreservedWithoutMainPointerAlias=True,
            scopedMd5HelpersProof=helper_proof,
            scopedArm7WmHelperAndCompilerProof=arm7_proof,
            scopedArm7TypedCallbackAndCompilerProof=callback_proof,
            originalSourceRegistrySha256=sha256(ROOT / 'recovery.json'), generatorSha256=sha256(__file__)))


if __name__ == '__main__':
    main()
