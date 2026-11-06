import copy
from project import ROOT, read_json, sha256
import qualify_arm9_thumb_reference_inputs_20261105 as thumb

PINS = {
    'evidence/matches/http-explicit-interfaces-canonical-20261106.json': (
        '14b263eeb799cc66f769b8f0eadde04339e22c30d920adf753686114f702f0aa',
        'evidence/lanes/parallel-wave20261106/http-explicit-interfaces/ready.json',
        '3cc14b34688595237c1cd314f3bdcf36ae2bac91e3ba08463c1751e2eb594316',
        {'0x2099058': 152, '0x20990f0': 72, '0x2099dc8': 44, '0x209a008': 52, '0x2099df4': 392}),
    'evidence/matches/http-explicit-strncpy-canonical-20261106.json': (
        '1bc6f9a0ccd7d96ed698e863f4557cced547b4aaab9dcfb1df886ee2c530654b',
        'evidence/lanes/parallel-wave20261106/http-explicit-strncpy/ready.json',
        'fac0d85f5b750082cbaeb727ac35034525e4e754a516a5218e4ee8308f511254',
        {'0x2098b44': 244}),
}


def annotate(batches):
    projected = copy.deepcopy(batches)
    annotations = []
    for name, (report_sha, ready_name, ready_sha, expected) in PINS.items():
        assert sha256(ROOT / name) == report_sha and sha256(ROOT / ready_name) == ready_sha
        report, ready = read_json(ROOT / name), read_json(ROOT / ready_name)
        assert report['allPassed'] and report['migrationOnly'] and report['frozenMigrationReady'] == ready_name
        assert report['newByteCredit'] == report['newFunctionCredit'] == ready['newByteCredit'] == ready['newFunctionCredit'] == 0
        assert {r['address']: r['bytes'] for r in report['matches']} == expected
        assert all((r.get('program') or '', r['processor'], r['module'], r['mode']) == ('', 'arm9', 'main', 'thumb') for r in report['matches'])
        assert sha256(ROOT / ready['sourceManifest']) == ready['sourceManifestSha256']
        manifest = read_json(ROOT / ready['sourceManifest'])
        native = [r for r in manifest['files'] if r['path'] == thumb.IMAGE]
        assert native == [dict(path=thumb.IMAGE, sha256=thumb.IMAGE_SHA)]
        assert sha256(ROOT / thumb.IMAGE) == thumb.IMAGE_SHA
        assert next(r for r in report['replayDependencies'] if r['path'] == thumb.IMAGE) == native[0]
        selected = [b for b in projected if b['report'] == name]
        assert len(selected) == 1 and thumb.IMAGE not in selected[0]['sourceHashes']
        selected[0]['sourceHashes'][thumb.IMAGE] = thumb.IMAGE_SHA
        annotations.append(dict(report=name, reportSha256=report_sha, ready=ready_name, readySha256=ready_sha,
            nativeReferenceFromActualFrozenRuntimeManifest=native[0], sourceCredit=0,
            annotationIsPrivateToOriginalFullThumbQualifier=True,
            allOriginalFreshC99MappingGenuineLinksAndNamespaceChecksStillRequired=True))
    assert all(a['sourceHashes'] == b['sourceHashes'] for a, b in zip(batches, projected) if a['report'] not in PINS)
    return projected, annotations
