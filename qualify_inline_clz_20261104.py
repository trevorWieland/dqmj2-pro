import hashlib
import re
from project import ROOT, read_json, sha256, configuration, native_dependencies
from audit_parallel_packet_union import linked_body, number


def require(condition, message):
    if not condition:
        raise ValueError(message)


def compact(value):
    return re.sub(r'\s+', '', value)


def qualify(row):
    native_dependencies(configuration())
    require(row.get('sourceLanguage') == 'c-with-original-inline-assembly', 'Mixed language required')
    reason = row['assemblyJustification']
    require(reason['kind'] == 'verified-original-sdk-inline-assembly', 'Unsupported mixed assembly kind')
    require(reason['originalSymbol'] == 'MATH_CountLeadingZerosInline', 'Unsupported inline primitive')
    require(reason['rawExecutableBytesStoredAsSource'] is False, 'Executable byte source is forbidden')
    require(reason['wholeCallerBehaviorCredit'] == reason['primitiveProbeCalleeSourceCredit'] == 0,
            'Inline qualification cannot add execution or callee credit')
    provenance_path = ROOT / reason['provenance']
    require(sha256(provenance_path) == reason['provenanceSha256'], 'Provenance changed')
    provenance = read_json(provenance_path)
    require(provenance['kind'] == reason['kind'] and provenance['originalSymbol'] == reason['originalSymbol'],
            'Primitive provenance identity differs')
    require(provenance['sourceCredit'] == 0 and provenance['ordinaryAlgorithmsRemainC'] is True,
            'Invalid provenance scope')
    require(provenance['instructionOrObjectPatches'] is False and provenance['rawExecutableBytesStoredAsSource'] is False,
            'Patched or raw primitive forbidden')
    reference = ROOT / provenance['referenceSource']
    require(sha256(reference) == provenance['referenceSourceSha256'], 'Published reference changed')
    primitive = compact(provenance['originalSourcePrimitive'])
    expected = 'SDK_INLINEu32MATH_CountLeadingZerosInline(u32x){asm{clzx,x}returnx;}'
    require(primitive == expected and primitive in compact(reference.read_text(encoding='utf-8')),
            'Published source does not contain the single CLZ primitive')
    require(provenance['primitiveInstructions'] == ['clz x, x'] and provenance['mode'] == 'arm'
            and provenance['targetProcessor'] == 'ARM946E-S', 'Unsupported instruction scope')
    source = ROOT / row['source']
    require(source.suffix == '.c' and sha256(source) == row['sourceSha256'], 'C source changed')
    assembly_token = r'\b(?:asm|__asm__|__asm)\b'
    require(not re.search(assembly_token, source.read_text(encoding='utf-8')), 'Caller contains unqualified assembly')
    pins = {pin['path']: pin['sha256'] for pin in row['sourceDependencies']}
    helpers = reason['sourceHelperPins']
    require(len(helpers) == 1 and pins.get(helpers[0]['path']) == helpers[0]['sha256'], 'Primitive header is not a compiler input')
    for name, digest in pins.items():
        path = ROOT / name
        require(sha256(path) == digest, 'Compiler header changed')
        content = path.read_text(encoding='utf-8')
        tokens = re.findall(assembly_token, content)
        if name == helpers[0]['path']:
            require(len(tokens) == 1 and primitive.replace('SDK_INLINE', 'staticinline') in compact(content),
                    'Context must retain exactly the published CLZ body')
        else:
            require(not tokens, 'Unqualified assembly in another compiler input')
    require((row.get('program') or '') == '' and row['processor'] == 'arm9'
            and row['module'] == 'main' and row['mode'] == 'arm', 'Unsupported mixed namespace')
    modules = read_json(ROOT / 'ledger/modules.json')['modules']
    module = next(item for item in modules if item['name'] == 'main' and item['processor'] == 'arm9'
                  and not item.get('program'))
    image = ROOT / module['binary']
    require(sha256(image) == module['sha256'], 'Native module changed')
    address, size = number(row['address']), row.get('size', row.get('bytes'))
    offset = address - number(module['base'])
    native = image.read_bytes()[offset:offset + size]
    require(offset >= 0 and len(native) == size and hashlib.sha256(native).hexdigest() == row['targetSha256'],
            'Original full function identity changed')
    require(sha256(ROOT / row['object']) == row['objectSha256'], 'Compiler object changed')
    link = row['realLink']
    for name, digest in [('linkedElf', 'linkedElfSha256'), ('lcf', 'lcfSha256')]:
        require(sha256(ROOT / link[name]) == link[digest], 'Genuine linker artifact changed')
    require(linked_body(ROOT / link['linkedElf'], link['name'], size, address, ROOT / link['lcf']) == native,
            'Genuine complete linked function differs')
    offsets = set()
    for region in row['justifiedAssemblyRanges']:
        start = region['offset']
        require(region.get('program', '') == '' and region['processor'] == 'arm9' and region['module'] == 'main'
                and region['mode'] == 'arm', 'Instruction namespace differs')
        require(region['bytes'] == 4 and start % 4 == 0 and 0 <= start <= size - 4 and start not in offsets
                and number(region['address']) == address + start, 'Invalid inline instruction range')
        encoded = native[start:start + 4]
        require(encoded.hex() == region['originalEncodedWord'], 'Inline encoding differs from original')
        require(int.from_bytes(encoded, 'little') & 0x0fff0ff0 == 0x016f0f10, 'Inline word is not CLZ')
        offsets.add(start)
    all_clz = {start for start in range(0, size - 3, 4)
               if int.from_bytes(native[start:start + 4], 'little') & 0x0fff0ff0 == 0x016f0f10}
    require(offsets and offsets == all_clz and reason['nativeInstructions'] == len(offsets),
            'CLZ instruction accounting is incomplete')
    assembly_bytes = len(offsets) * 4
    require(row['justifiedAssemblyBytes'] == assembly_bytes and row['ordinaryCBytes'] == size - assembly_bytes,
            'Mixed byte accounting differs')
    return dict(source=row['source'], sourceSha256=row['sourceSha256'], nativeSha256=row['targetSha256'],
                ordinaryCBytes=size - assembly_bytes, justifiedAssemblyBytes=assembly_bytes,
                originalInlineInstructionOffsets=sorted(offsets), provenanceSha256=reason['provenanceSha256'],
                wholeCallerBehaviorCredit=0, primitiveProbeCalleeSourceCredit=0, sourceCredit=0)


def classify(after, added, ordinary_classifier):
    mixed = {key for key in added if after[key].get('sourceLanguage') == 'c-with-original-inline-assembly'}
    receipts = [qualify(after[key]) for key in sorted(mixed)]
    result = ordinary_classifier(after, set(added) - mixed)
    result['newMixedSourceFunctions'] = len(mixed)
    result['newOrdinaryCBytes'] += sum(receipt['ordinaryCBytes'] for receipt in receipts)
    result['newVerifiedOriginalAssemblyBytes'] += sum(receipt['justifiedAssemblyBytes'] for receipt in receipts)
    return result, receipts
