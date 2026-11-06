import json
import re
import struct
from pathlib import Path

from link_runtime_unit import measured_module
from project import ROOT, configuration, now, sha256, write_json

TARGETS = {0x021E4120: 2, 0x021E4500: 1, 0x021E46D8: 1}
WITNESSES = {
    0x021E4120: [(0xE5D7100C, 0xE1A00005), (0xE1D912F0, 0xE1DD00F8)],
    0x021E4500: [(0xE1D700FE,)],
    0x021E46D8: [(0xE1D912F4, 0xE1DD00F8)],
}


def run():
    metadata, raw, config = measured_module('ov001')
    base = 0x021D7240
    calls = {target: [] for target in TARGETS}
    for name, length, start in re.findall(r'^(\S+) kind:function\(arm,size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)$', config, re.M):
        start, length = int(start, 0), int(length, 0)
        for address in range(start, start + length, 4):
            word = struct.unpack_from('<I', raw, address - base)[0]
            if word & 0x0F000000 != 0x0B000000:
                continue
            displacement = (word & 0xFFFFFF) << 2
            if displacement & 0x2000000:
                displacement -= 0x4000000
            target = address + 8 + displacement
            if target not in TARGETS:
                continue
            following = struct.unpack_from('<4I', raw, address - base + 4)
            witness = next((row for row in WITNESSES[target] if following[:len(row)] == row), None)
            if witness is None:
                raise ValueError(('Unknown R0 consumption/overwrite after direct native call', hex(address), following))
            span = raw[address - base:address - base + 4 + len(witness) * 4]
            calls[target].append({'callerModule': 'ov001', 'callerMode': 'arm', 'caller': hex(start),
                                  'callerSymbol': name, 'callerBytes': length, 'callAddress': hex(address),
                                  'branchWord': hex(word), 'followingWordsThroughR0Overwrite': [hex(value) for value in witness],
                                  'evidenceSpanSha256': __import__('hashlib').sha256(span).hexdigest(),
                                  'r0ReadBeforeOverwrite': False})
    for target, expected_count in TARGETS.items():
        if len(calls[target]) != expected_count:
            raise ValueError('Known direct caller inventory changed; repeat qualified use analysis')
    result = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
              'processor': 'arm9', 'module': 'ov001', 'moduleInputSha256': metadata['sha256'],
              'directResultUseFacts': [{'address': hex(target), 'mode': 'arm', 'callers': rows,
                                       'knownDirectCallersDiscardR0': True, 'semanticReturnTypeProven': False}
                                      for target, rows in calls.items()],
              'physicalReturnProbeReference': 'evidence/abi/reward-scalar-returns-20261029.json',
              'physicalR0RepresentationFactsRemainValid': True, 'indirectCallersAudited': False,
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)), 'sourceCredit': 0,
              'limitations': ['Native R0 observations do not alone establish a meaningful source-language return type',
                              'Only qualified direct ARM callers within ov001 are classified; indirect/outside-module calls remain unresolved',
                              'No accepted source or prototype is changed by this audit']}
    write_json(ROOT / 'evidence/abi/reward-discarded-results-20261029.json', result)
    print(json.dumps({'targets': len(calls), 'directCalls': sum(map(len, calls.values())), 'sourceCredit': 0}))


if __name__ == '__main__':
    run()
