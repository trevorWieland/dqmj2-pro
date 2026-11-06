import json
import re
import struct
from pathlib import Path

from link_runtime_unit import measured_module
from project import ROOT, configuration, now, read_json, sha256, write_json

REPORT = ROOT / 'evidence/application/ov001-enemy-initialization-context-20261029.json'


def span(module, address):
    metadata, raw, config = measured_module(module)
    match = re.search(r'^\S+ kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:0x' + f'{address:08x}' + '$', config, re.M)
    if not match:
        raise ValueError('Caller context lacks a qualified native function boundary')
    size = int(match[2], 0)
    offset = address - int(metadata['base'], 0)
    return {'processor': 'arm9', 'module': module, 'address': hex(address), 'mode': match[1],
            'bytes': size, 'spanSha256': __import__('hashlib').sha256(raw[offset:offset + size]).hexdigest()}, raw, metadata


def run():
    main_entry, main, main_metadata = span('main', 0x02043418)
    overlay_entry, unused, overlay_metadata = span('ov001', 0x021E88E4)
    secondary_entry, unused, unused_metadata = span('ov001', 0x021E8D28)
    observed = []
    for address, target, opcode in [(0x020434CC, 0x021E88E4, 0xEB069504), (0x020434E4, 0x021E8D28, 0xEB06960F)]:
        word = struct.unpack_from('<I', main, address - 0x02000000)[0]
        delta = ((word & 0xFFFFFF) ^ 0x800000) - 0x800000
        if word != opcode or address + 8 + delta * 4 != target:
            raise ValueError('Ordinary enemy initializer direct call changed')
        observed.append({'sourceModule': 'main', 'sourceMode': 'arm', 'address': hex(address),
                         'opcode': hex(word), 'targetModule': 'ov001', 'targetMode': 'arm', 'target': hex(target)})
    witnesses = {}
    for address, count in [(0x0204346C, 12), (0x020434B8, 13), (0x02064998, 5), (0x020649C0, 5), (0x02064978, 8)]:
        witnesses[hex(address)] = [hex(word) for word in struct.unpack_from('<' + 'I' * count, main, address - 0x02000000)]
    if struct.unpack_from('<I', main, 0x649A8)[0] != 0x021C1544 or struct.unpack_from('<I', main, 0x649D0)[0] != 0x021C1544:
        raise ValueError('Enemy slot memory mapping changed')
    if struct.unpack_from('<II', main, 0x64990) != (0x021C0EF4, 0x18E4):
        raise ValueError('Broader prepared-battle clear mapping changed')
    snapshot = ROOT / 'evidence/application/enemy-initialization-app-references-20261029.json'
    references = read_json(snapshot)['readOnlyReferenceHashes']
    if len(references) != 3 or any(not re.fullmatch('[0-9a-f]{64}', row['sha256']) for row in references):
        raise ValueError('Local read-only application reference snapshot is malformed')
    report = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
              'moduleHashes': {'main': main_metadata['sha256'], 'ov001': overlay_metadata['sha256']},
              'caller': main_entry, 'callees': [overlay_entry, secondary_entry], 'measuredDirectCalls': observed,
              'nativeInstructionWords': witnesses,
              'preparedEnemySlots': {'base': '0x021c1544', 'stride': 528, 'slots': 3,
                  'identityGetter': 'main/arm/02064998', 'pointerGetter': 'main/arm/020649c0',
                  'identityOffset': 0, 'speciesOffset': 46, 'existingVariantOffset': 48},
              'ordinaryCallerSequence': [
                  'Read three prepared slot IDs using main02064998 and pass them to ov001021D9124(team1, IDs)',
                  'For each nonnegative prepared slot ID, obtain its destination via main020649C0 and row via ov001021D924C',
                  'Copy row species to destination+2E, preserve the existing variant byte at+30, copy metadata from row2/3 to+AD/+AE',
                  'Store native main02062B9C(species, variant) result at destination+AB',
                  'Call ov001021E88E4(destination, row)',
                  'Call main02063628 with the resulting species and variant; this body writes progression bitsets',
                  'Call ov001021E8D28(destination, row)',
                  'Populate native trait/derived blocks via main0207B460,0207C078,02044FF4 and conditional0207C2B8',
                  'Call main020433C8(row), count initialized slots, close row preparation via ov001021D9214'],
              'resetEvidence': {'entry': 'main/arm/02064978', 'base': '0x021c0ef4', 'bytes': 6372,
                  'effect': 'Tail-call native memset with byte0 across the broader prepared-battle buffer'},
              'variantPrerequisite': 'The ordinary caller preserves destination+30; it does not establish a universal initial variant0',
              'functionalEvidence': 'evidence/matches/ov001-20261029-enemy-initialize01.json',
              'measuredStaticSequenceOnly': True, 'ordinaryCallerExecutedHere': False,
              'currentSceneStateOrRngValueEstablished': False, 'sourceMatchCredit': 0,
              'applicationReferences': references,
              'applicationReferenceSnapshot': {'path': snapshot.relative_to(ROOT).as_posix(), 'sha256': sha256(snapshot)},
              'functionalReplayDependsOnApplication': False,
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'limitations': ['The original main caller is inspected, not reconstructed or executed by this context trace',
                  'Overlay001 must be the loaded target program for these main addresses to have the qualified meanings',
                  'Row-loader IO, encounter selector predecessors and persistent progression effects remain separate work',
                  'Prepared buffer reset alone does not establish valid enemy IDs or the actual scene variant/RNG state',
                  'Indirect and Thumb caller coverage is not certified by these two measured ARM call witnesses']}
    write_json(REPORT, report)
    print(json.dumps({'ordinaryCaller': 'main/arm/02043418', 'measuredCalls': len(observed), 'sourceMatchCredit': 0}))


if __name__ == '__main__':
    run()
