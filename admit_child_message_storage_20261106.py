import hashlib
import json
import subprocess
from project import ROOT, read_json, write_json, sha256, configuration, native_dependencies, now
from child_message_data_codec_20261106 import c_source


NAMESPACE = ('dwc/utility.bin/move/child.srl', 'arm9', 'utility-child-arm9-main')


def namespace(row, parent=None):
    parent = parent or {}
    module = row.get('module', parent.get('module', ''))
    program = row.get('program', parent.get('program', '')) or ''
    if module.startswith('utility-child-'):
        program = NAMESPACE[0]
    processor = row.get('processor', parent.get('processor')) or ('arm7' if 'arm7' in module else 'arm9')
    return program, processor, module


def main():
    config = configuration()
    native_dependencies(config)
    import ndspy.bmg as bmg
    revision = '9d4c697530ff885ba928e1a4395ab1422f113e3b'
    def committed(name):
        return subprocess.check_output(['git', 'show', revision + ':' + name], cwd=ROOT)
    assert json.loads(committed('evidence/verification/cohort160-expanded-source-closure-20261101.json'))['passed']
    ledger = [json.loads(line) for line in committed('ledger/functions.jsonl').splitlines()]
    by_id = {row['id']: row for row in ledger}
    protections, pins = [], []
    def add(row, kind, parent=None):
        if namespace(row, parent) != NAMESPACE:
            return
        size = row.get('storedBytes', row.get('bytes', row.get('size')))
        if size is None or int(size) == 0:
            return
        assert row.get('address') and int(size) > 0
        begin = int(row['address'], 0)
        protections.append(dict(start=begin, end=begin + int(size), kind=kind))
    for row in ledger:
        add(row, 'committed-function-positive-extent')
    for name, key in [('ledger/data.json', 'records'), ('ledger/linkage.json', 'regions')]:
        raw = committed(name)
        pins.append(dict(gitObject=revision + ':' + name, sha256=hashlib.sha256(raw).hexdigest()))
        for row in json.loads(raw)[key]:
            add(row, name)
    for path in sorted((ROOT / 'evidence/lanes').rglob('claim.json')):
        claim = read_json(path)
        pins.append(dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)))
        entries = claim.get('claimedFunctions', claim.get('functions'))
        assert isinstance(entries, list) or namespace(claim) != NAMESPACE
        for item in entries or []:
            if isinstance(item, str):
                assert item in by_id or namespace(claim) != NAMESPACE
                if item not in by_id:
                    continue
                item = by_id[item]
            assert isinstance(item, dict)
            if not item.get('address') and item.get('id') in by_id:
                item = {**by_id[item['id']], **item}
            add(item, path.relative_to(ROOT).as_posix(), claim)
    for path in sorted(ROOT.glob('cohort16[123]-*-specification.json')):
        pins.append(dict(path=path.name, sha256=sha256(path)))
        for row in read_json(path)['expectedAdditions']:
            add(row, 'pending-source-union')
    name = 'evidence/lanes/parallel-wave20261102/native-backlog/boundary-work.json'
    pins.append(dict(path=name, sha256=sha256(ROOT / name)))
    for group in read_json(ROOT / name)['groups']:
        for entry in group['entries']:
            for fragment in entry['ghidraBodyRanges']:
                for owner in fragment['physicalOwningModules']:
                    add(dict(group, module=owner, address=fragment['start'], bytes=fragment['bytes']), 'native-body-fragment')
    for path in sorted((ROOT / 'evidence/lanes').rglob('data-claim.json')):
        claim = read_json(path)
        for row in claim['claimedStorage']:
            add(row, path.relative_to(ROOT).as_posix())
    report_name = 'evidence/lanes/parallel-wave20261105/source95-data-inspection/semantic-roundtrip.json'
    report = read_json(ROOT / report_name)
    assert report['passed'] and report['encodedBytes'] == 3799
    native_path = ROOT / report['originalModule']['path']
    assert sha256(native_path) == report['originalModule']['sha256']
    native = native_path.read_bytes()
    directory = ROOT / 'src/utility/parallel_wave20261105/child-message-data'
    assert not directory.exists()
    storage, documents = [], []
    for asset in report['assets']:
        path = ROOT / asset['sourcePath']
        assert sha256(path) == asset['sourceSha256']
        old = read_json(path)
        document = dict(version=1, source=old['source'], compressionRecipe=old['compressionRecipe'], storageAlignment=4)
        address = int(asset['address'], 0)
        code, payload, encoded_size, alignment_size = c_source(document, f'native_child_message_data_{address:08x}', bmg)
        assert len(code.splitlines()) <= 500 and encoded_size == asset['bytes']
        assert hashlib.sha256(payload[:encoded_size]).hexdigest() == asset['originalEncodedSha256']
        assert native[address - 0x02000000:address - 0x02000000 + len(payload)] == payload
        assert not [p for p in protections if max(address, p['start']) < min(address + len(payload), p['end'])]
        storage.append(dict(program=NAMESPACE[0], processor=NAMESPACE[1], module=NAMESPACE[2], mode='data',
            kind='data', address=hex(address), bytes=len(payload), encodedAssetBytes=encoded_size,
            measuredZeroAlignmentBytes=alignment_size, targetSha256=hashlib.sha256(payload).hexdigest(),
            semanticSource=(directory / f'{address:08x}.json').relative_to(ROOT).as_posix()))
        documents.append(document)
    assert len(storage) == 8 and sum(row['bytes'] for row in storage) == 3808
    directory.mkdir(parents=True)
    for row, document in zip(storage, documents):
        path = ROOT / row['semanticSource']
        path.write_text(json.dumps(document, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
        row['semanticSourceSha256'] = sha256(path)
    evidence = ROOT / 'evidence/lanes/parallel-wave20261105/child-message-data'
    write_json(evidence / 'data-claim.json', dict(status='coordinator-admitted-initialized-storage-no-credit',
        owner='coordinator', sourceRevision=revision, createdUtc=now(), exclusiveSourceRoot=directory.relative_to(ROOT).as_posix(),
        sourceCredit=0, functionCount=0, claimedStorage=storage, functionOwnershipGranted=False))
    write_json(evidence / 'admission-review.json', dict(passed=True, sourceCredit=0, sourceRevision=revision,
        protectedRanges=len(protections), intersections=[], protectionPins=pins, assets=storage,
        originalModuleSha256=sha256(native_path), initializedBytes=3808, encodedAssetBytes=3799,
        measuredZeroAlignmentBytes=9, executableBytes=0, generatorSha256=sha256(__file__)))
    print(dict(passed=True, storageObjects=8, initializedBytes=3808, sourceCredit=0, functionCount=0))


if __name__ == '__main__':
    main()
