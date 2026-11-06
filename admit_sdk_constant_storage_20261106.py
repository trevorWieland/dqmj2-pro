import hashlib
import json
import subprocess
from project import ROOT, configuration, native_dependencies, read_json, write_json, sha256, now
from inspect_sdk_constant_arrays_20261106 import arrays, TYPES
from initialized_storage_protection_v2_20261106 import protected


def encode(document):
    assert document['version'] == 1 and document['kind'] == 'typed-sdk-integer-array'
    width, signed = TYPES[document['elementType']]
    values = document['elements']
    assert document['elementCount'] == len(values) and len(values) > 0
    low, high = (-(1 << (width * 8 - 1)), 1 << (width * 8 - 1)) if signed else (0, 1 << (width * 8))
    assert all(type(value) is int and low <= value < high for value in values)
    return b''.join(value.to_bytes(width, 'little', signed=signed) for value in values)


def main():
    revision = 'af5a4bd4f100fe5a727824a00a21e0ae3442b1a6'
    name = 'evidence/lanes/parallel-wave20261106/sdk-constant-arrays-inspection/inventory.json'
    inventory = read_json(ROOT / name)
    candidates = inventory['uniquePhysicalCandidates']
    assert inventory['sourceRevision'] == revision and len(candidates) == 3
    assert sum(row['bytes'] for row in candidates) == 562
    config = configuration()
    native_dependencies(config)
    import ndspy.rom
    import utility_runtime
    from qualify_arm9_thumb_reference_inputs_20261105 import derive
    assert sha256(config['rom']) == config['romSha256']
    assert ndspy.rom.NintendoDSRom(config['rom'].read_bytes()).getFileByName('dwc/utility.bin') == utility_runtime.INPUT.read_bytes()
    main_image = derive()
    layout, products = utility_runtime.derive()
    child = next(row for row in layout['modules'] if row['id'] == 'utility-child-arm7-main')
    child_image = products[ROOT / child['binary']]
    manifest = json.loads(subprocess.check_output(['git', 'show', revision + ':manifest.json'], cwd=ROOT))
    modules = {row['name']: row for row in manifest['modules']}
    root = ROOT / 'src/runtime/parallel_wave20261106/sdk-constant-data'
    assert not root.exists()
    admitted, documents, reviews = [], {}, []
    for row in candidates:
        source = ROOT / row['source']
        assert sha256(source) == row['sourceSha256']
        selected = [(descriptor, payload) for descriptor, payload in arrays(source.read_text(encoding='utf-8-sig'))
                    if descriptor['symbol'] == row['symbol'] and descriptor['type'] == row['type']]
        assert len(selected) == 1
        descriptor, payload = selected[0]
        assert len(payload) == row['bytes'] and hashlib.sha256(payload).hexdigest() == row['initializerSha256']
        module = modules[row['module']]
        assert sha256(ROOT / module['binary']) == module['sha256'] == row['moduleSha256']
        image = main_image if row['module'] == 'main' else child_image
        assert image == (ROOT / module['binary']).read_bytes()
        address, base = int(row['address'], 0), int(module['base'], 0)
        assert image[address - base:address - base + len(payload)] == payload
        namespace = (row['program'], row['processor'], row['module'])
        intervals, pins = protected(namespace, revision)
        assert not any(max(address, start) < min(address + len(payload), end) for start, end in intervals)
        width, signed = TYPES[row['type']]
        elements = [int.from_bytes(payload[i:i + width], 'little', signed=signed) for i in range(0, len(payload), width)]
        document = dict(version=1, kind='typed-sdk-integer-array', symbol=row['symbol'],
                        elementType=row['type'], elementCount=len(elements), elements=elements)
        assert encode(document) == payload
        negatives = 0
        for changed in [dict(document, elementCount=len(elements) + 1), dict(document, elements=elements + [0]),
                        dict(document, elements=[1 << (width * 8)] + elements[1:]), dict(document, version=2)]:
            try:
                encode(changed)
            except AssertionError:
                negatives += 1
            else:
                raise AssertionError('Invalid typed array accepted')
        changed = dict(document, elements=list(elements))
        changed['elements'][0] = elements[0] + 1 if elements[0] + 1 < (1 << (width * 8 - (1 if signed else 0))) else elements[0] - 1
        assert len(encode(changed)) == len(payload) and encode(changed) != payload
        file_name = f'{row["module"]}-{address:08x}.json'
        documents[file_name] = document
        admitted.append(dict(program=namespace[0], processor=namespace[1], module=namespace[2],
            kind='data', mode='data', formatKind='typed-sdk-integer-array', address=hex(address), bytes=len(payload),
            targetSha256=hashlib.sha256(payload).hexdigest(), semanticSource=(root / file_name).relative_to(ROOT).as_posix(),
            publishedSymbol=row['symbol'], elementType=row['type'], elementCount=len(elements)))
        reviews.append(dict(address=hex(address), module=namespace[2], bytes=len(payload), source=row['source'],
            sourceSha256=row['sourceSha256'], moduleSha256=module['sha256'], originalRomDerivedBytesVerified=True,
            protectionPins=pins, protectedIntervals=len(intervals), schemaRejections=negatives,
            sameSizeSemanticChangeLosesNativeIdentity=True))
    root.mkdir(parents=True)
    for file_name, document in documents.items():
        write_json(root / file_name, document)
    for row in admitted:
        row['semanticSourceSha256'] = sha256(ROOT / row['semanticSource'])
    directory = ROOT / 'evidence/lanes/parallel-wave20261106/sdk-constant-data'
    write_json(directory / 'coordinator-review.json', dict(passed=True, sourceCredit=0, sourceRevision=revision,
        admittedObjects=3, initializedCandidateBytes=562, ordinaryFunctionCredit=0, reviews=reviews,
        sourceInventory=name, sourceInventorySha256=sha256(ROOT / name), generatorSha256=sha256(__file__),
        limitations=['Source storage ownership only; genuine compiled objects, copied-root replay, strict accounting and shared acceptance remain required.',
                    'Published initializer meaning is preserved; no native execution, function implementation or full module credit.']))
    write_json(directory / 'data-claim.json', dict(status='coordinator-admitted-initialized-storage-no-credit',
        owner='coordinator', sourceRevision=revision, createdUtc=now(), functionCount=0, functionOwnershipGranted=False,
        sourceCredit=0, exclusiveSourceRoot=root.relative_to(ROOT).as_posix(), claimedStorage=admitted))
    print(dict(passed=True, dataObjects=3, initializedCandidateBytes=562, sourceCredit=0))


if __name__ == '__main__':
    main()
