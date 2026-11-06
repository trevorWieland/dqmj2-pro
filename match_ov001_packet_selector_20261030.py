import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_packet_selector_cases_20261030 import ADDRESS, vectors
from ov001_turn_order_itcm_fixture_20261030 import execute
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / 'src/overlays/ov001_20261030_packet_selector_6a744ac149d3.c'
SOURCE_HASH = '6a744ac149d3517c313646b33cbdee911d4c85c6b7d6b009730b8487ae0bee81'
WORK = ROOT / 'work/ov001-command-scheduling/20261030/packet-selector-final'
REPORT = ROOT / 'evidence/matches/ov001-20261030-packet-selector01.json'


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python/Unicorn required')
    if sha256(SOURCE) != SOURCE_HASH:
        raise ValueError('Frozen packet selector source changed')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Private ROM input changed')
    compiler.WORK = WORK / 'compiler'
    rows, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', True)
    if len(rows) != 1 or not rows[0].get('exactAfterDeclaredRelocation') or rows[0]['bytes'] != 368:
        raise ValueError('Frozen packet selector no longer matches every native byte')
    row = rows[0]
    bindings = qualified_bindings(row)
    directory = WORK / 'link' / row['objectSha256']
    proof = validate(row, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'immutable-link-artifacts'
    row.update(save_link_snapshots.freeze_link(proof))
    main_metadata, main, unused = measured_module('main')
    overlay_metadata, overlay, unused = measured_module('ov001')
    itcm_metadata, unused, unused = measured_module('itcm')
    candidate = bytearray(overlay)
    candidate[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + 368] = linked
    rom = NintendoDSRom(config['rom'].read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in ('EnmyKindTbl.bin', 'AbilityTbl.bin')}
    results = []
    for vector in vectors():
        original = execute(main, overlay, assets, ADDRESS, [], vector['memory'], vector['patches'],
                           vector['expectedReturn'], vector['seed'], [])
        rebuilt = execute(main, bytes(candidate), assets, ADDRESS, [], vector['memory'], vector['patches'],
                          vector['expectedReturn'], vector['seed'], [])
        if original != rebuilt:
            raise ValueError('Native/exact-linked packet selector machine results differ')
        results.append({**{key: value for key, value in vector.items() if key not in ('memory', 'patches')},
                        'result': original})
    actual_values = sorted({change['after'] for vector in results for change in vector['actorWrites']})
    row.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=368, justifiedAssemblyBytes=0,
               signature='u32(void)', nativeSymbolEntries=bindings, isolatedCallerLink=proof,
               oracle=dict(vectors=len(results), executions=len(results) * 2, actualReturnRequired=True,
                           freshMachinePerExecution=True, hostCalleeStubs=False, instructionBound=100000,
                           wholeMappedRamItcmStackRegistersFlagsAndTracesCompared=True,
                           independentHeaderKindPeerCountByteFlagsIntentMarkerScoreAndStateModel=True,
                           rawActor1feValuesWritten=actual_values, results=results,
                           limitations=['Raw mode0 packet/header/bitmap/peer inputs are deterministic supplied components',
                                        'Accepted native headers are exercised with raw payload bytes5/127/255; real scene/network reachability remains unproved',
                                        'No IO, actual network, current state, save persistence or application integration is exercised',
                                        'Count0..3, markers0/1/128/255, equal/changed actor bytes and four native rejected-input paths are bounded',
                                        'The separate748-byte chooser default/inheritedR6 path remains unresolved and unaccepted']))
    dependencies = ['ov001_packet_selector_cases_20261030.py', 'ov001_turn_order_itcm_fixture_20261030.py',
                    'ov001_award_fixture_20261029.py']
    report = dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], matches=[row],
                  compiler=dict(path=str(compiler.COMPILER.relative_to(ROOT)), sha256=sha256(compiler.COMPILER)),
                  moduleInputSha256=overlay_metadata['sha256'], mainInputSha256=main_metadata['sha256'],
                  itcmInputSha256=itcm_metadata['sha256'],
                  inputPins=[dict(path=path, sha256=sha256(ROOT / path)) for path in dependencies],
                  generator=Path(__file__).name, generatorSha256=sha256(Path(__file__)),
                  reproductionCommand='python match_ov001_packet_selector_20261030.py')
    write_json(REPORT, report)
    abi = dict(schemaVersion=1, romSha256=config['romSha256'], processor='arm9', module='ov001', mode='arm',
               moduleInputSha256=overlay_metadata['sha256'], address='0x021e824c', nativeBytes=96,
               nativeSpanSha256=compiler.sha(overlay[0x021E824C - 0x021D7240:0x021E824C - 0x021D7240 + 96]),
               evidenceClass='Native caller/callee stack-argument and state-effect proof', sourceCredit=0,
               physicalArguments=['R0 slot', 'R1 signed action', 'R2 target-side word', 'R3 signed target-slot', 'entrySP+0 marker word'],
               reads='Fifth argument loaded at post-push SP+8; lower byte written to intent+4',
               observedCaller='ov001:ARM022030B8 loads fifth argument from raw row+4; full byte0/1/128/255 tested',
               nativeOriginalCallerExecutions=len(results), proof=str(REPORT.relative_to(ROOT)), proofSha256=sha256(REPORT),
               limits=['Positive action0/32767/65535 through this caller; negative callee-only action path remains separately qualified',
                       'Accepted source/prototypes are unchanged; this fact applies to future unmatched drafts'])
    write_json(ROOT / 'evidence/application/ov001-intent-writer-fifth-argument-20261030.json', abi)
    print(json.dumps(dict(report=str(REPORT.relative_to(ROOT)), functions=1, bytes=368,
                          actualReturns=len(results) * 2, actor1feValues=actual_values)), flush=True)


if __name__ == '__main__':
    run()
