from pathlib import Path
import tempfile
from project import ROOT, configuration, read_json, write_json, sha256
from parallel_status import interval, collisions
from prepare_parallel_packet_wave import reserved_storage, metadata_names, classify_metadata, mandatory_inputs, packet_identifier


def main():
    controls = []
    rom = configuration()['romSha256']
    work = ROOT / 'work/parallel-wave20261104/intake-controls'
    work.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=work) as folder:
        root = Path(folder)
        (root / 'ledger').mkdir()
        bridge = dict(program='child', processor='arm7', module='wram', address='0x1000', bytes=12)
        data = dict(module='main', address='0x2001', bytes=3, kind='data', states=dict(dataMatched=True))
        bss = dict(module='main', address='0x3000', bytes=32, kind='bss', states=dict(dataMatched=True))
        write_json(root / 'ledger/linkage.json', dict(buildSha256=rom, regions=[bridge]))
        write_json(root / 'ledger/data.json', dict(buildSha256=rom, records=[data, bss]))
        reserved = reserved_storage(root, rom)
        candidate = dict(program='child', processor='arm7', module='wram', mode='arm', address='0x1004', bytes=8)
        assert collisions([('alias', interval(candidate))], reserved)
        controls.append(dict(name='ARM-interior-alias-inside-regenerated-bridge-rejected', passed=True))
        assert collisions([('data', interval(dict(module='main', mode='arm', address='0x2000', bytes=4)))], reserved)
        controls.append(dict(name='unaligned-accepted-data-overlap-rejected', passed=True))
        for name, changed in [('other-program', dict(candidate, program='other')),
                              ('other-processor', dict(candidate, processor='arm9')),
                              ('other-overlay', dict(candidate, module='ov005'))]:
            assert not collisions([(name, interval(changed))], reserved)
            controls.append(dict(name=name + '-kept-independent', passed=True))
        assert not collisions([('bss', interval(dict(module='main', mode='arm', address='0x3000', bytes=4)))], reserved)
        controls.append(dict(name='BSS-does-not-reserve-initialized-source-bytes', passed=True))
        write_json(root / 'ledger/data.json', dict(buildSha256='0' * 64, records=[]))
        try:
            reserved_storage(root, rom)
        except ValueError:
            controls.append(dict(name='wrong-ROM-bookkeeping-rejected', passed=True))
        else:
            raise AssertionError('Wrong ROM ledger accepted')
        manifest = root / 'runtime.json'
        write_json(manifest, dict(mandatoryExternalInputs=[dict(path='compiler.h', sha256='0' * 64)]))
        initial = dict(path='runtime.json', sha256=sha256(manifest))
        try:
            mandatory_inputs([initial], root)
        except ValueError:
            controls.append(dict(name='opaque-classification-does-not-hide-missing-runtime-closure', passed=True))
        else:
            raise AssertionError('Missing actual runtime header accepted')
    opaque = metadata_names(dict(readyPackets=['ready.json'], opaqueMetadata=['attempt.json']))
    assert classify_metadata('ready.json', False, opaque)
    assert classify_metadata('attempt.json', False, opaque)
    assert not classify_metadata('compiler.h', True, opaque)
    controls.append(dict(name='READY-and-diagnostics-opaque-ordinary-source-runtime', passed=True))
    for name in ['ready.json', 'attempt.json']:
        try:
            classify_metadata(name, True, opaque)
        except ValueError:
            controls.append(dict(name='actual-runtime-' + name + '-cannot-be-opaque', passed=True))
        else:
            raise AssertionError('Runtime input archived as opaque metadata')
    for name in ['source.c', 'source.h', 'code.o', 'game.nds']:
        try:
            metadata_names(dict(readyPackets=['ready.json'], opaqueMetadata=[name]))
        except ValueError:
            controls.append(dict(name='opaque-payload-' + name + '-rejected', passed=True))
        else:
            raise AssertionError('Compiler/executable input disguised as metadata')
    actual = reserved_storage(ROOT, rom)
    aliases = read_json(ROOT / 'evidence/lanes/parallel-wave20261102/backlog-audit/frontier-linkage-reconciliation.json')['exactAliasesToExcludeBeforeDispatch']
    assert len(aliases) == 22
    assert all(collisions([('actual-interior-alias', interval(row))], actual) for row in aliases)
    controls.append(dict(name='all22-real-prior-frontier-aliases-rejected', passed=True))
    used = set()
    first, second = 'lane-a/supplement/ready.json', 'lane-b/supplement/ready.json'
    assert packet_identifier(first, 0, {}, used) == 'supplement-0'
    try:
        packet_identifier(second, 0, {}, used)
    except ValueError:
        controls.append(dict(name='nested-lane-identifier-collision-rejected-before-overwrite', passed=True))
    else:
        raise AssertionError('Two replay descriptors would overwrite each other')
    assert packet_identifier(second, 0, dict(packetIds={second: 'lane-b-supplement'}), used) == 'lane-b-supplement-0'
    controls.append(dict(name='explicit-distinct-nested-packet-identifier', passed=True))
    output = ROOT / 'evidence/lanes/parallel-wave20261104/intake-controls.json'
    write_json(output, dict(passed=True, sourceCredit=0, controls=controls,
        generator=Path(__file__).name, generatorSha256=sha256(__file__),
        preparerSha256=sha256(ROOT / 'prepare_parallel_packet_wave.py'),
        frozenProducerOrNativeInputChanges=False, originalAcceptanceGatesRemoved=False))
    print(dict(passed=True, controls=len(controls)))


if __name__ == '__main__':
    main()
