import hashlib
import json
import subprocess
from project import ROOT, configuration, native_dependencies, read_json, write_json, sha256, now
from inspect_sdk_sound_constants_20261106 import candidates, SOURCE, HEADER, REVISION, OUTPUT
from sdk_constant_data_codec_20261106 import encode, TYPES
from initialized_storage_protection_v2_20261106 import protected


EXPECTED = {('', 'main', 0x020d8354, 1536), ('', 'main', 0x020d8954, 724),
            ('', 'main', 0x020d8254, 256), ('', 'main', 0x020d8154, 256),
            ('dwc/utility.bin/move/child.srl', 'utility-child-arm9-main', 0x02021d94, 724),
            ('dwc/utility.bin/move/child.srl', 'utility-child-arm9-main', 0x02021c94, 256)}
DIRECTORY = 'evidence/lanes/parallel-wave20261106/sdk-sound-data'
SOURCE_ROOT = 'src/runtime/parallel_wave20261106/sdk-sound-data'


def main():
    inventory = read_json(ROOT / OUTPUT)
    assert inventory['sourceRevision'] == REVISION
    assert sha256(ROOT / SOURCE) == inventory['sourceSha256']
    assert sha256(ROOT / HEADER) == inventory['headerSha256']
    selected = [r for r in inventory['completeNativeHits'] if r['fitsZeroRecordedBodyInspectionRange']]
    assert len(selected) == 6 and sum(r['bytes'] for r in selected) == 3752
    assert {(r['program'], r['module'], int(r['address'], 0), r['bytes']) for r in selected} == EXPECTED
    config = configuration()
    native_dependencies(config)
    import ndspy.rom
    import utility_runtime
    from qualify_arm9_thumb_reference_inputs_20261105 import derive
    assert sha256(config['rom']) == config['romSha256']
    assert ndspy.rom.NintendoDSRom(config['rom'].read_bytes()).getFileByName('dwc/utility.bin') == utility_runtime.INPUT.read_bytes()
    images = {'main': derive()}
    utility_layout, products = utility_runtime.derive()
    for row in utility_layout['modules']:
        if row['id'] == 'utility-child-arm9-main':
            images[row['id']] = products[ROOT / row['binary']]
    manifest = json.loads(subprocess.check_output(['git', 'show', REVISION + ':manifest.json'], cwd=ROOT))
    modules = {row['name']: row for row in manifest['modules']}
    parsed = {row['symbol']: (row, payload) for row, payload in candidates(
        (ROOT / SOURCE).read_text(encoding='utf-8-sig'), (ROOT / HEADER).read_text(encoding='utf-8-sig'))}
    root = ROOT / SOURCE_ROOT
    assert not root.exists()
    admitted, documents, reviews, protections = [], {}, [], {}
    for row in selected:
        descriptor, payload = parsed[row['symbol']]
        assert descriptor == {k: row[k] for k in descriptor}
        assert hashlib.sha256(payload).hexdigest() == row['payloadSha256']
        module = modules[row['module']]
        assert row['processor'] == module['processor'] == 'arm9'
        assert sha256(ROOT / module['binary']) == module['sha256']
        image = images[row['module']]
        assert image == (ROOT / module['binary']).read_bytes()
        address, base = int(row['address'], 0), int(module['base'], 0)
        assert image[address - base:address - base + len(payload)] == payload
        namespace = (row['program'], row['processor'], row['module'])
        if namespace not in protections:
            protections[namespace] = protected(namespace, REVISION)
        intervals, pins = protections[namespace]
        assert not any(max(address, start) < min(address + len(payload), end) for start, end in intervals)
        width, signed, unused = TYPES[row['type']]
        values = [int.from_bytes(payload[i:i + width], 'little', signed=signed) for i in range(0, len(payload), width)]
        document = dict(version=1, kind='typed-sdk-integer-array', symbol=row['symbol'],
                        elementType=row['type'], elementCount=len(values), elements=values)
        assert encode(document) == payload
        for changed in [dict(document, elementCount=len(values) + 1), dict(document, version=2),
                        dict(document, elements=[1 << (width * 8)] + values[1:])]:
            try:
                encode(changed)
            except AssertionError:
                pass
            else:
                raise AssertionError('Invalid semantic array admitted')
        changed = dict(document, elements=list(values))
        changed['elements'][0] ^= 1
        assert len(encode(changed)) == len(payload) and encode(changed) != payload
        file_name = f'{row["module"]}-{address:08x}.json'
        documents[file_name] = document
        admitted.append(dict(program=namespace[0], processor=namespace[1], module=namespace[2],
            kind='data', mode='data', formatKind='typed-sdk-integer-array', address=hex(address), bytes=len(payload),
            targetSha256=hashlib.sha256(payload).hexdigest(), semanticSource=SOURCE_ROOT + '/' + file_name,
            publishedSymbol=row['symbol'], elementType=row['type'], elementCount=len(values),
            moduleBase=module['base'], binary=module['binary'], inputModuleSha256=module['sha256'],
            compilerProcessor='arm946e', nativeSymbol=f'native_sdk_sound_{row["module"].replace("-", "_")}_{address:08x}'))
        reviews.append(dict(address=hex(address), module=namespace[2], bytes=len(payload),
            originalRomDerivedBytesVerified=True, protectionPins=pins, protectedIntervals=len(intervals),
            schemaRejections=3, sameSizeSemanticChangeLosesNativeIdentity=True))
    root.mkdir(parents=True)
    for name, document in documents.items():
        write_json(root / name, document)
    for row in admitted:
        row['semanticSourceSha256'] = sha256(ROOT / row['semanticSource'])
    write_json(root / 'layout.json', dict(version=1, assets=admitted))
    write_json(ROOT / DIRECTORY / 'coordinator-review.json', dict(passed=True, sourceCredit=0,
        sourceRevision=REVISION, admittedObjects=6, initializedCandidateBytes=3752, ordinaryFunctionCredit=0,
        source=SOURCE, sourceSha256=inventory['sourceSha256'], header=HEADER, headerSha256=inventory['headerSha256'],
        sourceInventory=OUTPUT, sourceInventorySha256=sha256(ROOT / OUTPUT), reviews=reviews,
        generatorSha256=sha256(__file__), limitations=[
            'Storage ownership only; compilation, copied-root replay, accounting and shared acceptance remain required.',
            'SDK lookup values are preserved; native audio playback and hardware execution remain unproven.']))
    write_json(ROOT / DIRECTORY / 'data-claim.json', dict(status='coordinator-admitted-initialized-storage-no-credit',
        owner='coordinator', sourceRevision=REVISION, createdUtc=now(), functionCount=0,
        functionOwnershipGranted=False, sourceCredit=0, exclusiveSourceRoot=SOURCE_ROOT, claimedStorage=admitted))
    print(dict(passed=True, dataObjects=6, initializedCandidateBytes=3752, sourceCredit=0))


if __name__ == '__main__':
    main()
