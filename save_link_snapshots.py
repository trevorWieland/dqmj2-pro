import hashlib
import json
from pathlib import Path

from project import ROOT

DIRECTORY = ROOT / 'work/mechanics-save/link-artifacts'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def preserve(data, suffix):
    digest = sha(data)
    path = DIRECTORY / (digest + suffix)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != data:
            raise AssertionError('Immutable link artifact hash/path collision')
    else:
        path.write_bytes(data)
    return {'path': str(path.relative_to(ROOT)), 'sha256': digest, 'bytes': len(data)}

def freeze_link(proof):
    folder = (ROOT / proof['linkedElf']).parent
    original = folder / 'validation.json'
    raw = original.read_bytes()
    if json.loads(raw) != proof:
        raise AssertionError('Runtime link validation changed before snapshot')
    validation = preserve(raw, '.json')
    items = [(folder / 'caller.bin', proof['linkedCallerSha256']), (ROOT / proof['linkedElf'], proof['linkedElfSha256']), (ROOT / proof['lcf'], proof['lcfSha256']), (folder / 'caller.o', proof['splitObjectSha256'])]
    items += [(ROOT / row['object'], row['objectSha256']) for row in proof['bindingOnlyProbes']]
    if proof.get('generator'):
        items.append((ROOT / proof['generator'], proof['generatorSha256']))
    artifacts = []
    by_name = {}
    for path, expected in items:
        data = path.read_bytes()
        if sha(data) != expected:
            raise AssertionError(('Runtime link artifact changed before snapshot', str(path)))
        captured = preserve(data, path.suffix.lower())
        item = {'originalPath': str(path.relative_to(ROOT)), **captured}
        artifacts.append(item)
        by_name[path.name] = item
    manifest = {'schemaVersion': 1, 'caller': proof['name'], 'module': proof['module'], 'processor': proof['processor'], 'address': proof['address'], 'bytes': proof['bytes'], 'sourceObjectSha256': proof['sourceObjectSha256'], 'nativeSpanSha256': proof['nativeSpanSha256'], 'linkerSha256': proof['linkerSha256'], 'originalValidationPath': str(original.relative_to(ROOT)), 'validation': validation, 'artifacts': artifacts, 'nativeCalleeCodeOrSourceCredit': 0}
    manifest_bytes = (json.dumps(manifest, indent=2) + '\n').encode('utf-8')
    snapshot = preserve(manifest_bytes, '.json')
    return {'isolatedCallerBinary': by_name['caller.bin']['path'], 'isolatedCallerBinarySha256': by_name['caller.bin']['sha256'], 'isolatedCallerLinkValidation': validation['path'], 'isolatedCallerLinkValidationSha256': validation['sha256'], 'isolatedCallerLinkSnapshotManifest': snapshot['path'], 'isolatedCallerLinkSnapshotManifestSha256': snapshot['sha256'], 'isolatedCallerLinkedElf': by_name['linked.elf']['path'], 'isolatedCallerLinkedElfSha256': by_name['linked.elf']['sha256'], 'isolatedCallerLinkLcf': by_name['unit.lcf']['path'], 'isolatedCallerLinkLcfSha256': by_name['unit.lcf']['sha256']}
