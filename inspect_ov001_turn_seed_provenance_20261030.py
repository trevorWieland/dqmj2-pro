import json
from pathlib import Path

import match_runtime as compiler
from link_runtime_unit import measured_module
from project import ROOT, configuration, now, sha256, write_json


def run():
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured ROM differs')
    images = {name: measured_module(name) for name in ('main', 'ov001')}

    def identity(module, address, size, signature):
        metadata, body, unused = images[module]
        base = 0x02000000 if module == 'main' else 0x021D7240
        span = body[address - base:address - base + size]
        if len(span) != size:
            raise ValueError('Native seed identity lies outside its measured module')
        return dict(processor='arm9', module=module, moduleInputSha256=metadata['sha256'], mode='arm',
                    address=hex(address), bytes=size, spanSha256=compiler.sha(span), signature=signature)

    packet_source = ROOT / 'src/overlays/ov001_20261030_packet_selector_6a744ac149d3.c'
    parent_source = ROOT / 'src/overlays/ov001_20261030_turn_start_7b881c7cb50c.c'
    if sha256(packet_source) != '6a744ac149d3517c313646b33cbdee911d4c85c6b7d6b009730b8487ae0bee81':
        raise ValueError('Frozen packet source changed')
    if sha256(parent_source) != '7b881c7cb50c45e1e770065e83ddae5aa71d303147136761c68c4a9a0d7e4b95':
        raise ValueError('Frozen ordinary parent source changed')
    packet = identity('ov001', 0x022030B8, 368, 'u32(void)')
    packet.update(source=str(packet_source.relative_to(ROOT)), sourceSha256=sha256(packet_source),
                  sourceMatchReport='evidence/matches/ov001-20261030-packet-selector01.json',
                  measured='After original packet validation, stores packet word+0x18 from first packet when selector0<selector1, otherwise second packet')
    parent = identity('ov001', 0x021DE598, 172, 'u32(void)')
    parent.update(source=str(parent_source.relative_to(ROOT)), sourceSha256=sha256(parent_source),
                  sourceMatchReport='evidence/matches/ov001-20261030-turn-start01.json',
                  measured='When the original main predicate reports raw scene2, obtains context+C and passes it to the original RNG setter before ordering draws')
    entries = []
    for item in (packet, parent):
        report = json.loads((ROOT / item['sourceMatchReport']).read_text())
        entry = next(row for row in report['matches'] if int(row['address'], 0) == int(item['address'], 0))
        if report['romSha256'] != config['romSha256'] or entry['sourceSha256'] != item['sourceSha256']:
            raise ValueError('Current measured component report differs from its qualified source')
        entries.append(entry)
    packet_oracle, parent_oracle = [entry['oracle'] for entry in entries]
    seed_returns = 2 * sum(sum(row['address'] == '0x203d2ec' for row in result['result']['protocolReturns'])
                           for result in parent_oracle['results'])
    evidence = dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'],
                    evidenceClass='Measured native component dataflow with exact C and genuine caller links',
                    sourceCredit=0, packetSelector=packet, ordinaryTurnParent=parent,
                    scenePredicate=identity('main', 0x02044508, 24, 'u32(void)'),
                    rawSceneGetter=identity('main', 0x020443EC, 16, 'u32(void)'),
                    contextSetter=identity('main', 0x02044564, 24, 'u32(u32)'),
                    contextGetter=identity('main', 0x0204457C, 16, 'u32(void)'),
                    rngSetter=identity('main', 0x0203D2EC, 24, 'u32(u32)'),
                    fields=[dict(address='0x020f69e8', representation='u8', measured='Raw scene; predicate is true exactly for value2'),
                            dict(address='0x020f69d0', representation='u32', measured='Main context0x020F69C4+C; stored by packet selector and read by ordinary turn parent'),
                            dict(address='0x020f6044', representation='u32', measured='Global LCG state; setter always stores its argument and returns the prior full word')],
                    nativeEvidence=dict(packetVectors=packet_oracle['vectors'], packetTopReturns=packet_oracle['executions'],
                                        parentVectors=parent_oracle['vectors'], parentTopReturns=parent_oracle['executions'],
                                        actualSeedSetterReturns=seed_returns,
                                        actualParentRngReturns=parent_oracle['nativeRngActualReturns'],
                                        suppliedOldAndContextSeedDiffer=all(row['originalRng'] != row['seedContextWord']
                                            for row in parent_oracle['results'] if row['seedReplaced']),
                                        nativeGetterSetterReturnAndStoreChecks=True,
                                        hostProviders=False, independentlyModeledFullRam=True),
                    limitations=['Packet and parent native components are separately exercised; an uninterrupted ordinary scene chain has not been observed',
                                 'Synthetic validated packet buffers and raw scene components do not establish a legal network session',
                                 'No current or future game seed, save persistence, initial context provenance or full combat result is inferred',
                                 'Healthy actor scoring and unresolved inherited-register paths are not exercised by the blocked-parent corpus',
                                 'This dataflow proof adds zero function, source-byte or callee implementation credit'],
                    generator=Path(__file__).name, generatorSha256=sha256(Path(__file__)),
                    reproductionCommand='python inspect_ov001_turn_seed_provenance_20261030.py')
    write_json(ROOT / 'evidence/application/ov001-packet-context-turn-seed-20261030.json', evidence)


if __name__ == '__main__':
    run()
