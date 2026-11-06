import hashlib
import json
import re
import struct
from project import ROOT, configuration, read_json, sha256


TABLE = ROOT / 'provenance/native-alternate-entrypoints.json'


def identity(report):
    keys = ['schemaVersion', 'romSha256', 'processor', 'module', 'mode', 'moduleInputSha256',
            'parent', 'alternateEntry', 'entryPrologues', 'externalBranchReferences', 'abi', 'nativeHelper',
            'fixtures', 'reconstructedCodeBytes', 'justifiedAssemblyBytes', 'ordinaryCBytes']
    payload = {key: report[key] for key in keys}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def local_file(relative, directory):
    path = (ROOT / relative).resolve()
    if not path.is_relative_to((ROOT / directory).resolve()) or not path.is_file():
        raise ValueError('Alternate-entry evidence escapes its repository-local directory')
    return path


def verify(name, binding):
    from link_runtime_unit import measured_module
    if binding.get('processor') != 'arm9' or binding.get('program') or binding.get('mode') != 'arm' or binding.get('kind') != 'function':
        raise ValueError('Alternate entries currently require an explicitly scoped host ARM function')
    address = int(binding['address'], 0)
    suffix = re.search(r'(?:^|_)([0-9a-f]{8})$', name)
    if not suffix or int(suffix[1], 16) != address:
        raise ValueError('Alternate entry requires an explicit address-qualified native call, not an inferred compiler intrinsic')
    reference = binding['alternateEntryEvidence']
    report = read_json(local_file(reference['report'], 'evidence/entrypoints'))
    verifier = local_file(reference['verifier'], '.')
    if sha256(verifier) != reference['verifierSha256'] or identity(report) != reference['identitySha256']:
        raise ValueError('Alternate-entry verifier or stable evidence identity changed')
    module, binary, config = measured_module(binding['module'])
    if any(report[key] != value for key, value in {'processor': 'arm9', 'module': binding['module'], 'mode': 'arm',
                                                 'romSha256': configuration()['romSha256'], 'moduleInputSha256': module['sha256']}.items()):
        raise ValueError('Alternate-entry CPU/module/ROM identity changed')
    parent, entry, helper = report['parent'], report['alternateEntry'], report['nativeHelper']
    begin, size, base = int(parent['address'], 0), parent['bytes'], int(module['base'], 0)
    expected = rf'^\S+ kind:function\(arm,size=0x{size:x}\) addr:0x{begin:08x}$'
    if not re.fullmatch(expected, parent['configuredIdentity']) or parent['configuredIdentity'] not in config.splitlines():
        raise ValueError('Alternate-entry parent is not the configured native function extent')
    if int(entry['address'], 0) != address or not begin < address < begin + size or address % 4:
        raise ValueError('Alternate entry escaped its parent extent or instruction mode')
    label = re.fullmatch(r'(\S+) kind:label\(arm\) addr:0x' + f'{address:08x}', entry['configuredIdentity'])
    if label is None or entry['configuredIdentity'] not in config.splitlines() or not entry['independentPrologue']:
        raise ValueError('Alternate entry lacks its configured ARM label and independent entry evidence')
    if int(entry['sharedParentEnd'], 0) != begin + size or not address < int(entry['sharedJoinAddress'], 0) < begin + size:
        raise ValueError('Shared-entry join or parent end changed')
    if hashlib.sha256(binary[begin - base:begin - base + size]).hexdigest() != parent['spanSha256']:
        raise ValueError('Shared parent bytes changed')
    for point in (begin, address):
        code = binary[point - base:point - base + 16]
        prologue = report['entryPrologues'][hex(point)]
        word = struct.unpack_from('<I', code)[0]
        if code.hex() != prologue['bytes'] or hashlib.sha256(code).hexdigest() != prologue['sha256'] or word & 0xffff0000 != 0xe92d0000 or not word & 0x4000:
            raise ValueError('Independent native stack-entry prologue changed')
    helper_address = int(helper['address'], 0)
    if helper['configuredIdentity'] not in config.splitlines() or hashlib.sha256(binary[helper_address - base:helper_address - base + helper['bytes']]).hexdigest() != helper['spanSha256']:
        raise ValueError('Native helper fixture input changed')
    fixtures = report['fixtures']
    if not fixtures['freshMachinePerExecution'] or fixtures['actualReturns'] != fixtures['executions'] or fixtures['executions'] != len(fixtures['results']) or not fixtures['executions']:
        raise ValueError('Alternate-entry evidence does not contain actual isolated returns')
    if any(not result['actualReturn'] for result in fixtures['results']) or any(report[key] != 0 for key in ['reconstructedCodeBytes', 'justifiedAssemblyBytes', 'ordinaryCBytes']):
        raise ValueError('Alternate-entry analysis acquired invalid returns or source credit')
    if not any(int(result['entry'], 0) == address for result in fixtures['results']):
        raise ValueError('Alternate entry itself has no returning fixture')
    incoming = []
    for edge in report['externalBranchReferences']:
        if int(edge['targetAddress'], 0) != address:
            continue
        if edge['processor'] != 'arm9' or edge['targetModule'] != binding['module'] or edge['targetMode'] != 'arm':
            raise ValueError('Incoming branch crosses its declared CPU/module/mode scope')
        source, native, symbols = measured_module(edge['sourceModule'])
        location, source_base = int(edge['address'], 0), int(source['base'], 0)
        owner_address = int(edge['sourceFunctionAddress'], 0)
        owner = re.search(r'^' + re.escape(edge['sourceFunction']) + r' kind:function\(arm,size=0x([0-9a-f]+)\) addr:0x' + f'{owner_address:08x}' + r'$', symbols, re.M)
        if owner is None or not owner_address <= location < owner_address + int(owner[1], 16):
            raise ValueError('Incoming branch lacks its configured source-function extent')
        raw = native[location - source_base:location - source_base + 4]
        word = struct.unpack('<I', raw)[0]
        displacement = word & 0xffffff
        displacement -= 0x1000000 if displacement & 0x800000 else 0
        if edge['sourceMode'] != 'arm' or source['sha256'] != edge['sourceModuleSha256'] or raw.hex() != edge['instructionBytes'] or word >> 28 == 15 or word & 0x0e000000 != 0x0a000000 or location + 8 + displacement * 4 != address:
            raise ValueError('Qualified incoming native branch changed')
        incoming.append(edge)
    if not incoming:
        raise ValueError('Alternate entry lacks a qualified incoming native branch')
    return {'address': address, 'configuredNativeSymbol': label[1], 'parent': parent, 'moduleInputSha256': module['sha256'],
            'proofIdentitySha256': reference['identitySha256'], 'incomingNativeBranches': incoming,
            'bindingMethod': 'explicit measured absolute ARM alternate entry', 'calleeSourceCredit': 0}


def binding(module, address):
    if not TABLE.exists():
        return None
    table = read_json(TABLE)
    if table['romSha256'] != configuration()['romSha256']:
        raise ValueError('Alternate-entry table belongs to a different ROM')
    rows = [row for row in table['entries'] if row['module'] == module and int(row['address'], 0) == address]
    if len(rows) > 1:
        raise ValueError('Duplicate alternate-entry identities')
    return rows[0] if rows else None


def ledger_rows():
    if not TABLE.exists():
        return []
    if read_json(TABLE)['romSha256'] != configuration()['romSha256']:
        raise ValueError('Alternate-entry ledger belongs to a different ROM')
    result = []
    for entry in read_json(TABLE)['entries']:
        address = int(entry['address'], 0)
        proof = verify(f'runtime_{entry["module"]}_{address:08x}', entry)
        result.append({'id': f'{configuration()["romSha256"]}/arm9/{entry["module"]}/arm/{address:08x}',
                       'processor': 'arm9', 'module': entry['module'], 'mode': 'arm', 'address': hex(address),
                       'parentFunction': proof['parent'], 'evidence': entry['alternateEntryEvidence'],
                       'evidenceClass': 'measured-alternate-stack-entry-with-shared-native-body',
                       'reconstructedCodeBytes': 0, 'ordinaryFunctionCredit': 0, 'assemblyBytesCredited': 0})
    return result
