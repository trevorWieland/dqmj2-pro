import copy
import hashlib
import re
import struct
from project import ROOT, configuration, read_json, sha256, write_json
from link_runtime_unit import measured_module
import prove_main_unsigned64_entries_20261030 as model
import verify_main_20261029_div64_entry as existing
import native_alternate_entries as policy



def qualify_thumb(edge):
    module, binary, config = measured_module(edge['sourceModule'])
    def require(value):
        if not value:
            raise ValueError('Thumb incoming entry identity/encoding differs')
    require(edge['processor'] == 'arm9' and edge['sourceMode'] == 'thumb' and edge['targetMode'] == 'arm')
    require(edge['targetModule'] == 'main' and int(edge['targetAddress'], 0) in (0x020260DC, 0x020260E8))
    require(module['sha256'] == edge['sourceModuleSha256'])
    first, address = int(edge['sourceFunctionAddress'], 0), int(edge['address'], 0)
    owner = re.search(r'^' + re.escape(edge['sourceFunction']) + r' kind:function\(thumb,size=0x([0-9a-f]+)\) addr:0x' + f'{first:08x}' + r'$', config, re.M)
    require(owner is not None and first <= address and address + 4 <= first + int(owner[1], 16))
    offset = address - int(module['base'], 0)
    raw = binary[offset:offset + 4]
    require(raw.hex() == edge['instructionBytes'])
    high, low = struct.unpack('<HH', raw)
    require(high & 0xF800 == 0xF000 and low & 0xF800 == 0xE800 and not low & 1)
    displacement = (high & 0x7FF) << 12 | (low & 0x7FF) << 1
    if displacement & 0x400000:
        displacement -= 0x800000
    require(((address + 4) & ~3) + displacement == int(edge['targetAddress'], 0))
    return dict(edge, configuredThumbOwnerVerified=True, originalThumbBlxTargetVerified=True)

def main():
    metadata, binary, config = measured_module('main')
    initial = read_json(ROOT / 'evidence/entrypoints/main-unsigned64-initial-model-20261030.json')
    pairs = [(int(row['numerator'], 0), int(row['denominator'], 0)) for row in initial['rows'] if row['entry'] == '0x20260dc']
    results = []
    for entry in [0x020260DC, 0x020260E8]:
        for a, b in pairs:
            for thumb in [False, True]:
                for masks in [0, 0xC0]:
                    result = model.execute(binary, entry, a, b, len(results), thumb, masks)
                    results.append(dict(result, entry=hex(entry), numerator=hex(a), denominator=hex(b)))
    existing.PARENT, existing.ALTERNATE, existing.PARENT_SIZE = 0x020260DC, 0x020260E8, 72
    edges = existing.external_references()
    arm_edges = [e for e in edges if e['sourceMode'] == 'arm']
    thumb_edges = [qualify_thumb(e) for e in edges if e['sourceMode'] == 'thumb']
    assert len(thumb_edges) == 40
    assert sum(int(e['targetAddress'], 0) == 0x020260E8 for e in thumb_edges) == 2
    for index, edge in enumerate(thumb_edges):
        bad = dict(edge, instructionBytes='00000000')
        try:
            qualify_thumb(bad)
        except ValueError:
            pass
        else:
            raise AssertionError('ChangedThumbBlxAccepted')
    parent_line = 'func_020260dc kind:function(arm,size=0x48) addr:0x020260dc'
    alternate_line = '.L_020260e8 kind:label(arm) addr:0x020260e8'
    helper_line = 'func_02026350 kind:function(arm,size=0x1e4) addr:0x02026350'
    assert all(x in config.splitlines() for x in [parent_line, alternate_line, helper_line])
    prologues = {}
    for entry in [0x020260DC, 0x020260E8]:
        data = binary[entry - 0x02000000:entry - 0x02000000 + 16]
        prologues[hex(entry)] = {'bytes': data.hex(), 'sha256': hashlib.sha256(data).hexdigest()}
    report = {'schemaVersion': 1, 'romSha256': configuration()['romSha256'], 'processor': 'arm9', 'module': 'main', 'mode': 'arm',
              'moduleInputSha256': metadata['sha256'], 'parent': dict(initial['parent']),
              'alternateEntry': {'address': '0x020260e8', 'configuredIdentity': alternate_line, 'independentPrologue': True,
                  'sharedJoinAddress': '0x020260f0', 'sharedParentEnd': '0x02026124', 'separateExecutableBytesCredited': 0},
              'entryPrologues': prologues, 'externalBranchReferences': arm_edges,
              'abi': {'inputWords': ['R0 numerator low', 'R1 numerator high', 'R2 denominator low', 'R3 denominator high'],
                      'resultWords': ['R0 result low', 'R1 result high'], 'entryRoles': {'0x20260dc': 'unsigned64 quotient', '0x20260e8': 'unsigned64 remainder'},
                      'preserved': 'R4-R11/SP/LR', 'clobberedOrUnspecified': ['R2', 'R3', 'R12', 'NZCV'],
                      'zeroDivisor': 'Original numerator passes through at both entries',
                      'genericIncomingValidatorScope': 'Configured ARM incoming branches only',
                      'additionalQualifiedThumbIncomingReferences': thumb_edges,
                      'completeNativeBranchScanCount': len(edges), 'thumbEncodingRejectionControls': 40},
              'nativeHelper': {'address': '0x02026350', 'bytes': 484, 'configuredIdentity': helper_line,
                  'spanSha256': hashlib.sha256(binary[0x26350:0x26534]).hexdigest(), 'sourceCredit': 0,
                  'actualFastSubentry': '0x02026358'},
              'fixtures': {'operandPairs': len(pairs), 'executions': len(results), 'actualReturns': len(results),
                           'freshMachinePerExecution': True, 'instructionLimit': 200000, 'results': results},
              'reconstructedCodeBytes': 0, 'justifiedAssemblyBytes': 0, 'ordinaryCBytes': 0,
              'generatorSources': [{'path': p, 'sha256': sha256(ROOT / p)} for p in
                  ['verify_main_unsigned64_entry_20261030.py', 'prove_main_unsigned64_entries_20261030.py',
                   'verify_main_20261029_div64_entry.py', 'native_alternate_entries.py']],
              'limitations': ['Entry/ABI evidence does not establish original vendor names or original assembly provenance',
                              'No new function, executable byte, assembly or source credit',
                              'Actual alternate-binding activation is deferred outside the frozen cohort62 gate']}
    destination = ROOT / 'evidence/entrypoints/main-unsigned64-entry-20261030.json'
    write_json(destination, report)
    binding = {'processor': 'arm9', 'module': 'main', 'mode': 'arm', 'kind': 'function', 'address': '0x020260e8',
               'alternateEntryEvidence': {'report': destination.relative_to(ROOT).as_posix(), 'identitySha256': policy.identity(report),
                   'verifier': 'verify_main_unsigned64_entry_20261030.py', 'verifierSha256': sha256(ROOT / 'verify_main_unsigned64_entry_20261030.py')}}
    temporary = ROOT / 'work/main-unsigned64-entry-20261030/proposed-table.json'
    temporary.parent.mkdir(parents=True, exist_ok=True)
    table = read_json(policy.TABLE)
    present = [e for e in table['entries'] if e['module'] == 'main' and int(e['address'], 0) == 0x020260E8]
    if present:
        assert present == [binding], 'Active unsigned64 binding differs from fresh qualification'
    else:
        table['entries'].append(binding)
    write_json(temporary, table)
    original = policy.TABLE
    try:
        policy.TABLE = temporary
        result = policy.verify('native_fn_020260e8', binding)
    finally:
        policy.TABLE = original
    write_json(ROOT / 'evidence/verification/main-unsigned64-entry-proposed-binding-20261030.json',
               {'sourceCredit': 0, 'bindingActivated': False, 'originalTableUnchanged': True, 'qualifiedProposedBinding': binding,
                'actualNativeReturns': len(results), 'incomingNativeBranches': len(result['incomingNativeBranches']),
                'reportSha256': sha256(destination)})
    print({'actualNativeReturns': len(results), 'sourceCredit': 0, 'incomingBranches': len(result['incomingNativeBranches']), 'bindingActivated': False})


if __name__ == '__main__':
    main()
