import base64
import hashlib
import json
from pathlib import Path
from project import ROOT, read_json, sha256, write_json


def main():
    archived, envelopes = [], []
    for folder in sorted((ROOT / 'evidence/attempts').glob('cohort149-initial-ov006-mode-binding*')):
        receipt = read_json(folder / 'receipt.json')
        assert receipt['failurePreserved'] and not receipt['liveFilesChanged'] and receipt['sourceCredit'] == 0
        for row in receipt['files']:
            path = ROOT / row['archived']
            assert sha256(path) == row['archivedSha256']
            if row['originalSha256'] != row['archivedSha256']:
                envelope = read_json(path)
                raw = base64.b64decode(envelope['originalBytesBase64'], validate=True)
                assert hashlib.sha256(raw).hexdigest() == envelope['originalSha256'] == row['originalSha256']
                assert envelope['sourceCredit'] == 0
                envelopes.append(path.relative_to(ROOT).as_posix())
            archived.append(dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)))
    assert len(archived) == 15 and len(envelopes) == 3
    lane = ROOT / 'evidence/lanes/parallel-wave20261102/ov006'
    diagnosis = read_json(lane / 'global-link-diagnosis149.json')
    for snapshot in diagnosis['snapshots'].values():
        assert sha256(ROOT / snapshot['path']) == snapshot['sha256']
    native = (ROOT / diagnosis['snapshots']['nativeOverlay']['path']).read_bytes()
    failed = (ROOT / diagnosis['snapshots']['globalOverlay']['path']).read_bytes()
    differences = [index for index, values in enumerate(zip(native, failed)) if values[0] != values[1]]
    assert len(native) == len(failed) and len(differences) == diagnosis['wholeOverlayDiffBytes'] == 2
    assert all(0x021eddf4 - 0x021d7240 <= index < 0x021eddf4 - 0x021d7240 + 34 for index in differences)
    assert diagnosis['otherFifteenPacketExtentsExact'] and diagnosis['isolatedCallerExactlyNative']
    assert not diagnosis['globalOriginalInputsAndWorkerPinsChanged']
    shadow = read_json(lane / 'typed-global-shadow149.json')
    assert shadow['linkerExitCode'] == 0 and shadow['allComparedModulesExact'] and len(shadow['comparisons']) == 11
    assert all(row['differentBytes'] == 0 and row['bytes'] == row['nativeBytes'] and row['actualSha256'] == row['nativeSha256'] for row in shadow['comparisons'])
    assert shadow['objectInputsStableThroughoutLink'] and shadow['stagedCallerInstructionAndLiteralBytesUnchanged'] and not shadow['instructionOrObjectPatches']
    assert shadow['sourceObjectSha256'] == diagnosis['snapshots']['sourceObject']['sha256']
    assert len(shadow['originalRelocations']) == len(shadow['qualifiedRelocations']) == 2
    for earlier, later in zip(shadow['originalRelocations'], shadow['qualifiedRelocations']):
        assert {k: v for k, v in earlier.items() if k != 'symbol'} == {k: v for k, v in later.items() if k != 'symbol'}
    for snapshot in shadow['privateProofSnapshots']:
        assert sha256(ROOT / snapshot['path']) == snapshot['sha256']
    result = dict(passed=True, sourceCredit=0, scope='Read-only forensic archive and typed-mode repair proof audit',
        archivedFailureArtifacts=archived, originalTextByteEnvelopesVerified=envelopes,
        failedOverlayDifferentBytes=2, failedDifferenceOffsets=differences, completeIsolatedCallerAlreadyExact=True,
        shadowInitializedModulesExact=11, shadowDifferentBytes=0, originalCompilerObjectAndRelocationPayloadsUnchanged=True,
        initializedInstructionOrLiteralPatches=False, privateShadowSnapshotHashesVerified=len(shadow['privateProofSnapshots']),
        sourceOnlyRomProven=False, fullFreshReplayProven=False, generatorSha256=sha256(Path(__file__)))
    write_json(ROOT / 'evidence/verification/parallel-wave20261102/mode-binding-provenance-audit.json', result)
    print(json.dumps({k: v for k, v in result.items() if k not in ['archivedFailureArtifacts', 'originalTextByteEnvelopesVerified']}, indent=2))


if __name__ == '__main__':
    main()
