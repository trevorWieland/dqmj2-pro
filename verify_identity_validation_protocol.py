import hashlib
import json
import struct

from project import ROOT, configuration, native_dependencies, verify_inputs, write_json

CONFIG = configuration()
native_dependencies(CONFIG)
from unicorn import UC_HOOK_CODE
from link_runtime_unit import validate as validate_link
from save_link_snapshots import freeze_link
import re
import mechanics_save_identity_library_oracle as library_model
import mechanics_save_section3_identity_oracle as caller_model
from mechanics_save_identity_core_thumb_oracle import expected_code

LIBRARY_REPORT = 'evidence/matches/mechanics-save-identity-library.json'
CORE_REPORT = 'evidence/matches/mechanics-save-identity-core-thumb.json'
VALUES_REPORT = 'evidence/matches/mechanics-save-identity-values-thumb.json'
VALIDATOR_REPORT = 'evidence/matches/mechanics-save-identity-validator-thumb.json'
ROOT_REPORT = 'evidence/matches/main-thumb-runtime02.json'
EQUALITY_REPORT = 'evidence/matches/mechanics-save-identity-equal-thumb.json'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def linked_matches(path, arm, rom_hash):
    report = json.loads((ROOT / path).read_text(encoding='utf-8'))
    if report['romSha256'] != rom_hash:
        raise AssertionError('Identity code protocol report namespace differs')
    result = {}
    for row in report['matches']:
        if sha((ROOT / row['source']).read_bytes()) != row['sourceSha256'] or sha((ROOT / row['object']).read_bytes()) != row['objectSha256']:
            raise AssertionError('Identity code protocol source/object differs')
        binary = (ROOT / row['isolatedCallerBinary']).read_bytes()
        proof = (ROOT / row['isolatedCallerLinkValidation']).read_bytes()
        validation = json.loads(proof)
        if sha(binary) != row['isolatedCallerBinarySha256'] or sha(proof) != row['isolatedCallerLinkValidationSha256'] or validation['sourceObjectSha256'] != row['objectSha256'] or not validation['exactCallerBytes'] or validation['calleeCodeOrSourceCredit'] != 0:
            raise AssertionError('Identity code protocol actual MW link proof differs')
        address = int(row['address'], 16)
        if binary != arm[address - 0x02000000:address - 0x02000000 + row['bytes']]:
            raise AssertionError('Identity code protocol caller native bytes differ')
        result[row['name']] = (row, binary)
    return result

def linked_root_helpers(arm):
    wanted = {0x02096ed0, 0x02096cdc, 0x02096ce8, 0x02096cf8, 0x02096da4, 0x02096ca8, 0x02096cbc, 0x02097198, 0x02097178}
    report = json.loads((ROOT / ROOT_REPORT).read_text(encoding='utf-8'))
    symbols = (ROOT / 'config/arm9/symbols.txt').read_text()
    result = {}
    for original in report['matches']:
        address = int(original['address'], 0)
        if address not in wanted:
            continue
        row = dict(original)
        bindings = {}
        for relocation in row['relocations']:
            target = int(relocation['target'], 0) & ~1
            match = re.search(r'kind:function\((arm|thumb),size=0x[0-9a-f]+\) addr:0x' + f'{target:08x}' + r'$', symbols, re.M)
            if not match:
                raise AssertionError('Identity validation protocol unqualified root function target')
            bindings[relocation['symbol']] = {'address': hex(target), 'mode': match[1], 'module': 'main', 'processor': 'arm9', 'kind': 'function'}
        row.update(freeze_link(validate_link(row, bindings)))
        code = (ROOT / row['isolatedCallerBinary']).read_bytes()
        if code != arm[address - 0x02000000:address - 0x02000000 + row['bytes']]:
            raise AssertionError('Identity validation root caller bytes differ')
        result[row['name']] = (row, code)
    if {int(row['address'], 0) for row, code in result.values()} != wanted:
        raise AssertionError('Identity validation root C helpers incomplete')
    return result

def independent_codes(machine):
    result = {}
    for identity in range(1, 66):
        code = expected_code(identity, 0, 1)
        result[identity] = (struct.pack('<III', 0x1000, code & 0xffffffff, code >> 32), f'{code:012d}'.encode())
    return result

def main():
    inputs = verify_inputs(CONFIG)
    arm = (ROOT / 'extract/arm9/arm9.bin').read_bytes()
    if sha(arm) != 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f':
        raise AssertionError('Identity code protocol ARM9 identity differs')
    library = linked_matches(LIBRARY_REPORT, arm, inputs['rom']['sha256'])
    core = linked_matches(CORE_REPORT, arm, inputs['rom']['sha256'])
    values = linked_matches(VALUES_REPORT, arm, inputs['rom']['sha256'])
    validator = linked_matches(VALIDATOR_REPORT, arm, inputs['rom']['sha256'])
    helpers = linked_root_helpers(arm)
    equality = linked_matches(EQUALITY_REPORT, arm, inputs['rom']['sha256'])
    compiler_check = json.loads((ROOT / EQUALITY_REPORT).read_text(encoding='utf-8'))['independentCompilerValidation']
    if sha((ROOT / compiler_check['report']).read_bytes()) != compiler_check['sha256']:
        raise AssertionError('Identity equality independent compiler validation differs')
    additions = {**core, **values, **validator, **helpers, **equality}
    origins = {**{name: CORE_REPORT for name in core}, **{name: VALUES_REPORT for name in values}, **{name: VALIDATOR_REPORT for name in validator}, **{name: ROOT_REPORT for name in helpers}, **{name: EQUALITY_REPORT for name in equality}}
    addresses = {int(row['address'], 16) for row, code in additions.values()}
    required = {int(row['address'], 0) for row, code in core.values()} | {0x02096ee4, 0x02096f50, 0x02096ed0, 0x02096ce8, 0x02096da4, 0x02096c6c, 0x02096cdc, 0x02096cf8, 0x02097198, 0x020973d8}
    base_loader = library_model.dependencies
    base_codes = caller_model.generate_codes
    base_machine = caller_model.Uc
    loaded = {}
    contexts = []
    def composed_loader(arm_bytes, rom_hash, matches):
        functions = base_loader(arm_bytes, rom_hash, matches)
        for function in functions.values():
            if function['report'] is None:
                function['report'] = LIBRARY_REPORT
        for row, binary in {**library, **additions}.values():
            functions[int(row['address'], 16)] = {**row, 'code': binary, 'report': origins.get(row['name'], LIBRARY_REPORT)}
        loaded.update(functions)
        return functions
    def tracked_machine(*args, **kwargs):
        machine = base_machine(*args, **kwargs)
        state = {'seen': set()}
        def hook(uc, address, size, context):
            if address in addresses:
                context['seen'].add(address)
        machine.hook_add(UC_HOOK_CODE, hook, state)
        contexts.append(state)
        return machine
    library_model.dependencies = composed_loader
    caller_model.generate_codes = independent_codes
    caller_model.Uc = tracked_machine
    try:
        oracle = library_model.validate(arm, CONFIG['save'].read_bytes(), library, ROOT)
    finally:
        library_model.dependencies = base_loader
        caller_model.generate_codes = base_codes
        caller_model.Uc = base_machine
    if len(contexts) != 2 or any(not required <= state['seen'] for state in contexts):
        raise AssertionError(('Identity code protocol core entries absent', contexts))
    oracle['reusedAcceptedSources'] = [{key: value for key, value in function.items() if key != 'code'} for function in loaded.values()]
    oracle['sourcePatchedFunctions'] = len(loaded)
    oracle['independentCompilerValidation'] = compiler_check
    oracle['requiredExecutedSourceEntries'] = [hex(address) for address in sorted(required)]
    oracle['observedSourceEntriesByEngine'] = [[hex(address) for address in sorted(state['seen'])] for state in contexts]
    oracle['syntheticIdentityCodes']['fixtureMethod'] = 'Independent Python hashlib MD5 projection and explicit12-byte constructor model; no native generator call'
    oracle['retainedNativeEntries'] = [row for row in oracle['retainedNativeEntries'] if int(row['address'], 16) not in addresses]
    oracle['limitations'] = ['The43 C bodies compose the constructor, new validator, accepted value/parser helpers and root identity fields with ARM library bridges and earlier saved-record callers.', 'MD5/CRC and remaining data/memory primitives remain native; independent expected code values remove reliance on native-generated fixtures.', 'Actual SDK data-service control remains offline, while positive data results remain the separately counted caller contracts.', 'This protocol adds no function credit, online legality, decoded profile meanings or semantic-partition bytes.']
    source = 'verify_identity_validation_protocol.py'
    report = {'schemaVersion': 1, 'romSha256': inputs['rom']['sha256'], 'saveSha256': inputs['save']['sha256'], 'arm9Sha256': sha(arm), 'matches': [], 'oracleSource': source, 'oracleSourceSha256': sha((ROOT / source).read_bytes()), 'oracle': oracle, 'independentModelSources': [{'source': path, 'sha256': sha((ROOT / path).read_bytes())} for path in ('mechanics_save_identity_core_thumb_oracle.py', 'mechanics_save_identity_library_oracle.py', 'mechanics_save_section3_identity_oracle.py')], 'inputsUnchanged': verify_inputs(CONFIG) == inputs}
    write_json(ROOT / 'evidence/matches/mechanics-save-identity-validation-protocol.json', report)
    print(json.dumps({'cases': oracle['cases'], 'calls': oracle['nativeAndRecompiledCalls'], 'sourcePatchedFunctions': len(loaded), 'requiredEntriesVerified': len(required)}))

if __name__ == '__main__':
    main()
