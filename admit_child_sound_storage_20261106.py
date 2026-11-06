import hashlib
import shutil
import struct
from project import ROOT, configuration, native_dependencies, read_json, write_json, sha256, now
from initialized_storage_protection_20261106 import protected
from child_message_data_codec_20261106 import encode as lz_encode


def commands(data, semantic):
    events, offsets, cursor = [], {}, 0

    def byte():
        nonlocal cursor
        value = data[cursor]
        cursor += 1
        return value

    def variable():
        value = 0
        for unused in range(5):
            part = byte()
            value = value << 7 | part & 127
            if part < 128:
                return value
        raise AssertionError('Oversized MML variable operand')

    while len(data) - cursor > 3 or any(data[cursor:]):
        offsets[cursor] = len(events)
        opcode = byte()
        if opcode < 128:
            velocity = byte()
            event = dict(kind='note', midiNote=opcode, velocity=velocity & 127,
                         velocityHighBit=bool(velocity & 128), ticks=variable())
        elif opcode == 0x80:
            event = dict(kind='wait', ticks=variable())
        elif opcode == 0x81:
            value = variable()
            event = dict(kind='program', bank=value >> 7, instrument=value & 127)
        elif opcode in (0x93, 0x94, 0x95):
            event = dict(kind={0x93: 'open-track', 0x94: 'jump', 0x95: 'call'}[opcode])
            if opcode == 0x93:
                event['track'] = byte()
            event['targetOffset'] = byte() | byte() << 8 | byte() << 16
        elif opcode in (0xc0, 0xc4, 0xc9, 0xce):
            value = byte()
            event = dict(kind={0xc0: 'pan', 0xc4: 'pitch-bend', 0xc9: 'portamento-key', 0xce: 'portamento-enabled'}[opcode],
                         value=value - 256 if opcode == 0xc4 and value > 127 else value)
        elif opcode == 0xfe:
            mask = byte() | byte() << 8
            event = dict(kind='allocate-tracks', tracks=[i for i in range(16) if mask >> i & 1])
        else:
            assert opcode in (0xfd, 0xff)
            event = dict(kind='return' if opcode == 0xfd else 'finish')
        events.append(event)
    for event in events:
        if 'targetOffset' in event:
            event['target'] = offsets[event.pop('targetOffset')]
    assert events == semantic['events']
    assert len(data) - cursor == semantic['measuredZeroAlignmentBytes'] and not any(data[cursor:])
    return offsets


def members(decoded, source):
    magic, bom, version, size, header, blocks = struct.unpack_from('<4sHHIHH', decoded)
    assert (magic, bom, version, size, header, blocks) == (b'SDAT', 0xfeff, 0x100, len(decoded), 64, 3)
    pairs = [struct.unpack_from('<II', decoded, 16 + 8 * i) for i in range(4)]
    assert pairs[0] == (0, 0)
    cursor = 64
    for magic, (offset, length) in zip([b'INFO', b'FAT ', b'FILE'], pairs[1:]):
        assert cursor == offset and struct.unpack_from('<4sI', decoded, offset) == (magic, length)
        cursor += length
    assert cursor == len(decoded)
    fat, unused = pairs[2]
    count = struct.unpack_from('<I', decoded, fat + 8)[0]
    assert count == len(source['files']) == 3
    event_count = instruments = waves = tokens = 0
    for index, file in enumerate(source['files']):
        at, extent, memory, reserved = struct.unpack_from('<4I', decoded, fat + 12 + index * 16)
        raw = decoded[at:at + extent]
        assert len(raw) == extent and raw[:4].decode() == file['kind']
        assert (memory, reserved) == (file['memoryPointer'], file['reservedWord'])
        assert struct.unpack_from('<HHIHH4sI', raw, 4) == (0xfeff, 0x100, extent, 16, 1, b'DATA', extent - 16)
        semantic = file['semantic']
        if file['kind'] == 'SSAR':
            base, number = struct.unpack_from('<II', raw, 24)
            assert base == 32 + 12 * number and number == len(semantic['sequences']) == 23
            offsets = commands(raw[base:], semantic['commands'])
            for i, row in enumerate(semantic['sequences']):
                start, bank, volume, channel, priority, player, reserved = struct.unpack_from('<IH4BH', raw, 32 + 12 * i)
                assert (None if start == 0xffffffff else offsets[start]) == row['firstEvent']
                assert [bank, volume, channel, priority, player, reserved] == [row[k] for k in ['bank', 'volume', 'channelPriority', 'playerPriority', 'player', 'reservedBits']]
            event_count = len(semantic['commands']['events'])
        elif file['kind'] == 'SBNK':
            number = struct.unpack_from('<I', raw, 56)[0]
            assert number == len(semantic['instruments']) == 16
            for i, row in enumerate(semantic['instruments']):
                reference = struct.unpack_from('<I', raw, 60 + 4 * i)[0]
                assert reference & 255 == (1 if row['kind'] == 'sample' else 3)
                values = struct.unpack_from('<HH6B', raw, reference >> 8)
                assert list(values) == [row[k] for k in ['waveIndex', 'waveArchiveSlot', 'originalMidiKey', 'attack', 'decay', 'sustain', 'release', 'pan']]
            instruments = number
        else:
            assert file['kind'] == 'SWAR'
            number = struct.unpack_from('<I', raw, 56)[0]
            assert number == len(semantic['waves']) == 10
            for i, wave in enumerate(semantic['waves']):
                at = struct.unpack_from('<I', raw, 60 + 4 * i)[0]
                mode, loop, rate, timer, start, length = struct.unpack_from('<BB3HI', raw, at)
                assert mode == 2 and [bool(loop), rate, timer, start, length] == [wave[k] for k in ['looped', 'sampleRate', 'timerTicks', 'loopStartWords', 'loopLengthWords']]
                adpcm = raw[at + 12:at + 12 + (start + length) * 4]
                word = struct.unpack_from('<I', adpcm)[0]
                predictor = struct.unpack_from('<h', adpcm)[0]
                assert [predictor, word >> 16 & 127, word >> 23] == [wave['adpcm'][k] for k in ['initialPredictor', 'initialStepIndex', 'reservedHeaderBits']]
                steps = [(1 - 2 * (n >> 3)) * ((n & 7) + 1) for b in adpcm[4:] for n in (b & 15, b >> 4)]
                assert steps == wave['adpcm']['signedQuantizedSteps']
                tokens += len(steps)
            waves = number
    assert (event_count, instruments, waves, tokens) == (415, 16, 10, 37448)
    return dict(typedCommands=event_count, instruments=instruments, waves=waves, independentlyCheckedAdpcmSteps=tokens)


def main():
    proposal_name = 'evidence/lanes/parallel-wave20261105/child-sdat-next/proposal.json'
    assert sha256(ROOT / proposal_name) == 'bdd567e68b7f67684cc48be8b77d1465e338b1e9abbee43ba88e50a21f53b8ac'
    proposal = read_json(ROOT / proposal_name)
    config = configuration()
    native_dependencies(config)
    import ndspy.rom
    import ndspy.lz10
    import utility_runtime
    from wave20261105_child_sdat_next_codec import encode
    assert sha256(config['rom']) == config['romSha256']
    assert ndspy.rom.NintendoDSRom(config['rom'].read_bytes()).getFileByName('dwc/utility.bin') == utility_runtime.INPUT.read_bytes()
    layout, files = utility_runtime.derive()
    module = next(row for row in layout['modules'] if row['id'] == proposal['module'])
    image = files[ROOT / module['binary']]
    assert hashlib.sha256(image).hexdigest() == proposal['inputModuleSha256'] == module['sha256']
    path = ROOT / proposal['semanticSource']['path']
    assert path.resolve().is_relative_to(ROOT / 'work/w5sd') and sha256(path) == proposal['semanticSource']['sha256']
    for pin in proposal['helperPins']:
        assert sha256(ROOT / pin['path']) == pin['sha256']
    document = read_json(path)
    address = int(proposal['address'], 0)
    native = image[address - 0x02000000:address - 0x02000000 + 13936]
    decoded = ndspy.lz10.decompress(native)
    assert encode(document['semantic']) == decoded and len(decoded) == 20960
    details = members(decoded, document['semantic'])
    encoded = lz_encode(decoded, document['compressionRecipe'])
    assert len(encoded) == 13935 and document['storageAlignment'] == 4 and document['measuredZeroAlignmentBytes'] == 1
    assert encoded + bytes(1) == native and hashlib.sha256(native).hexdigest() == proposal['targetSha256']
    namespace = (proposal['program'], proposal['processor'], proposal['module'])
    revision = 'e62f4358584bdfdad40f992d05c9eed7deec395b'
    intervals, pins = protected(namespace, revision)
    assert not any(max(address, a) < min(address + 13936, b) for a, b in intervals)
    root = ROOT / 'src/utility/parallel_wave20261105/child-sdat-next'
    assert not root.exists()
    root.mkdir(parents=True)
    source = root / '0201c140.json'
    shutil.copyfile(path, source)
    assert sha256(source) == proposal['semanticSource']['sha256']
    directory = ROOT / 'evidence/lanes/parallel-wave20261105/child-sdat-next'
    row = dict(program=namespace[0], processor=namespace[1], module=namespace[2], kind='data', mode='data',
        address=hex(address), bytes=13936, encodedAssetBytes=13935, measuredZeroAlignmentBytes=1,
        formatKind='Nitro-SDAT/SSAR/SBNK/SWAR-ADPCM', targetSha256=proposal['targetSha256'],
        semanticSource=source.relative_to(ROOT).as_posix(), semanticSourceSha256=sha256(source))
    write_json(directory / 'coordinator-review.json', dict(passed=True, sourceCredit=0, sourceRevision=revision,
        independentlyVerified=details, initializedBytes=13936, decodedBytes=20960, encodedBytes=13935,
        measuredZeroAlignmentBytes=1, originalRomToChildAutoloadVerified=True, protectionPins=pins,
        protectedIntervals=len(intervals), proposalSha256=sha256(ROOT / proposal_name),
        generatorSha256=sha256(__file__), actualHardwareAudioPlaybackProven=False))
    write_json(directory / 'data-claim.json', dict(status='coordinator-admitted-initialized-storage-no-credit',
        owner='repo_audit', sourceRevision=revision, createdUtc=now(), functionCount=0,
        functionOwnershipGranted=False, sourceCredit=0, claimedStorage=[row],
        exclusiveSourceRoot=root.relative_to(ROOT).as_posix()))
    print(dict(passed=True, dataObjects=1, initializedBytes=13936, sourceCredit=0,
               claimSha256=sha256(directory / 'data-claim.json')))


if __name__ == '__main__':
    main()
