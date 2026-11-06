import copy
import hashlib
import re
from project import ROOT, configuration, native_dependencies, read_json, write_json, sha256
from closed_c_compiler_inputs_20261105 import compiler_inputs
from qualify_explicit_c_frontend_20261102 import qualify as fresh_c99
from qualify_arm9_thumb_reference_inputs_20261105 import object_mode
from admit_aes_table_storage_v1_20261106 import tables, multiply
import link_runtime_unit as linker


REPORT = 'evidence/matches/cohort169-parallel-wave20261105-n-ov006-aes-first-0.json'
READY = 'evidence/lanes/parallel-wave20261106/ov006-aes-next/ready.json'
READY_SHA = '165378d3551b36c3af7728d6b1aaeac0c67eb559d302f1fb59c25203367f701c'
INPUTS = 'evidence/lanes/parallel-wave20261106/ov006-aes-next/inputs.json'
INPUTS_SHA = '8983d97b9b2145735b7fbc327ce11c5f646b84f742fc3d153bf0ad577a3fac78'
IMAGE = 'extract/arm9_overlays/ov006.bin'
IMAGE_SHA = 'fb9cb28ea400207bda442e3265da73af994866cf3a6c352b46a11db59835d341'
OUTPUT = 'evidence/verification/cohort169-ov006-aes-reference-v1-qualification-20261106.json'
FLAGS = ['-O4,p', '-enum', 'int', '-char', 'signed', '-str', 'noreuse', '-proc', 'arm946e',
    '-gccext,on', '-fp', 'soft', '-inline', 'on,noauto', '-Cpp_exceptions', 'off', '-RTTI', 'off',
    '-interworking', '-w', 'off', '-sym', 'on', '-gccinc', '-nolink', '-msgstyle', 'gcc',
    '-ipa', 'file', '-lang', 'c99', '-thumb']
EXPECTED = {'0x21f0944': 696, '0x21f0bfc': 400, '0x21f0d8c': 956, '0x21f1148': 956}
DATA = {0x02208890, 0x022088b8, 0x02208cb8, 0x022090b8, 0x022094b8,
        0x022098b8, 0x02209cb8, 0x0220a0b8, 0x0220a4b8, 0x0220a8b8, 0x0220acb8}


def contract(report):
    assert sha256(ROOT / READY) == READY_SHA and sha256(ROOT / INPUTS) == INPUTS_SHA
    ready = read_json(ROOT / READY)
    assert ready['functions'] == 4 and ready['bytes'] == ready['ordinaryCBytes'] == 3008
    assert report['allPassed'] and report['romSha256'] == configuration()['romSha256']
    assert {row['address']: row['bytes'] for row in report['matches']} == EXPECTED and len(report['matches']) == 4
    assert report['actualNativeAndSourceCallerReturns'] == 112 and report['suppliedCalleeSourceOrExecutionCredit'] == 0
    assert report['generator'] == 'wave20261106_ov006_aes_next_match.py'
    assert report['generatorSha256'] == sha256(ROOT / report['generator']) == '33e3c6261516f28033a72ed9fb657077170ef2818f83ad390474a3427e78afbf'
    identities = {row['address']: row for row in ready['identities']}
    observed_data, observed_code = set(), set()
    for row in report['matches']:
        assert (row.get('program') or '', row['processor'], row['module'], row['mode']) == ('', 'arm9', 'ov006', 'thumb')
        for key in ['address', 'bytes', 'source', 'sourceSha256', 'targetSha256']:
            assert row[key] == identities[row['address']][key]
        assert row['source'] == 'src/ov006/parallel_wave20261106/aes-next/rijndael.c'
        assert row['sourceSha256'] == 'f19ad4227e13991adfa185942ae4f53d8580beaf4cccd47b76c89ff49e8e8f5b'
        assert row['sourceDependencies'] == [dict(path='src/ov006/parallel_wave20261106/aes-next/context.h',
            sha256='eb7268cef7f533ad4d8f0d425a74bbc6ae0d49fbba73cbab2a6b8107eb3ee9ff')]
        assert row['compilerFlags'] == FLAGS and row['compiler'] == 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
        assert row['ordinaryCBytes'] == row['bytes'] and row['justifiedAssemblyBytes'] == 0
        assert row['realLink']['exactCallerBytes'] and row['exactAfterDeclaredRelocation']
        assert row['outputSha256'] == row['targetSha256'] == row['realLink']['linkedCallerSha256']
        compiler_inputs(row)
        for name, binding in row['nativeSymbolEntries'].items():
            assert (binding.get('program') or '', binding['processor'], binding['module']) == ('', 'arm9', 'ov006')
            address = int(binding['address'], 0)
            if binding['kind'] == 'data':
                assert address in DATA and binding['mode'] == 'data'
                assert name == f'native_data_ov006_{address:08x}'
                observed_data.add(address)
            else:
                assert row['address'] == '0x21f0bfc' and name == 'native_ov006_021f0944'
                assert address == 0x021f0944 and binding['kind'] == 'function' and binding['mode'] == 'thumb'
                observed_code.add(address)
    assert observed_data == DATA and observed_code == {0x021f0944}
    provider = read_json(ROOT / 'evidence/lanes/parallel-wave20261106/ov006-aes-next/code-provider-interface.json')
    assert provider['nativeReferenceExecutesOriginalKeyEnc'] and provider['rebuiltExecutionRequiresFreshGenuineCompiledKeyEnc']
    assert provider['unselectedCodeProvidersExecuted'] == provider['extraCalleeCredit'] == 0
    assert provider['codeProvider']['selectedInThisSamePacket']
    return ready


def qualify():
    pinned = {name: sha256(ROOT / name) for name in ['recovery.json', 'source-preferences.json', REPORT, READY, INPUTS]}
    report = read_json(ROOT / REPORT)
    ready = contract(report)
    for pin in ready['files']:
        assert sha256(ROOT / pin['path']) == pin['sha256']
    refs = {pin['path']: pin['sha256'] for pin in read_json(ROOT / INPUTS)['files'] if pin['path'].startswith('extract/')}
    assert refs == {IMAGE: IMAGE_SHA}
    cfg = configuration(); native_dependencies(cfg)
    assert sha256(cfg['rom']) == cfg['romSha256'] == '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'
    import ndspy.rom
    overlay = ndspy.rom.NintendoDSRom(cfg['rom'].read_bytes()).loadArm9Overlays([6])[6]
    image, base = bytes(overlay.data), overlay.ramAddress
    assert base == 0x021d7240 and image == (ROOT / IMAGE).read_bytes()
    assert hashlib.sha256(image).hexdigest() == IMAGE_SHA
    tables_generated = tables()
    table_proposal = read_json(ROOT / 'evidence/lanes/parallel-wave20261106/structured-table-read-only/aes-proposal.json')
    for row in table_proposal['objects']:
        start = int(row['address'], 0) - base
        payload = b''.join(word.to_bytes(4, 'little') for word in tables_generated[row['primarySymbol']])
        assert image[start:start + len(payload)] == payload
    round_constants, value = [], 1
    for unused in range(10):
        round_constants.append(value << 24); value = multiply(value, 2)
    payload = b''.join(word.to_bytes(4, 'little') for word in round_constants)
    assert image[0x02208890 - base:0x02208890 - base + 40] == payload
    assert hashlib.sha256(payload).hexdigest() == 'e47588a34ad373c5b8486c13d0a9b42dae24acb6ea58dae259a3ef2a68c49106'
    proofs = []
    for row in report['matches']:
        offset = int(row['address'], 0) - base
        assert hashlib.sha256(image[offset:offset + row['bytes']]).hexdigest() == row['targetSha256']
        mode = object_mode(row)
        adjusted = copy.deepcopy(row); index = adjusted['compilerFlags'].index('-lang')
        adjusted['compilerFlags'] = adjusted['compilerFlags'][:index] + adjusted['compilerFlags'][index + 2:]
        directory = ROOT / 'work/integration/cohort169-ov006-aes-reference-v1' / row['address']
        fresh = fresh_c99(adjusted, directory / 'compile')
        entry = {**report, **row, 'object': fresh['explicitC99Object'], 'objectSha256': fresh['explicitC99ObjectSha256']}
        assert object_mode(entry) == mode
        linked = linker.validate(entry, row['nativeSymbolEntries'], directory / 'link')
        assert all(probe['initializedCodeBytes'] == probe['nativeCalleeBytesUsed'] == probe['calleeSourceCredit'] == 0 for probe in linked['bindingOnlyProbes'])
        for name, binding in row['nativeSymbolEntries'].items():
            linker.verify_binding(name, binding)
        proofs.append(dict(address=row['address'], bytes=row['bytes'], sourceOnlyCompilerInputs=compiler_inputs(row),
            actualThumbMapping=mode, freshExplicitC99=fresh, freshGenuineNativeLink=linked))
    cases = []
    for key, value in [('program', 'other/child.srl'), ('processor', 'arm7'), ('module', 'ov000'),
                       ('mode', 'arm'), ('bytes', 692), ('sourceSha256', '0' * 64)]:
        candidate = copy.deepcopy(report); candidate['matches'][0][key] = value; cases.append(('wrong-' + key, candidate))
    candidate = copy.deepcopy(report); candidate['matches'].pop(); cases.append(('missing-function', candidate))
    candidate = copy.deepcopy(report); candidate['allPassed'] = False; cases.append(('failed-report', candidate))
    candidate = copy.deepcopy(report); candidate['matches'][0]['compilerFlags'] = FLAGS + ['-include', 'hidden.h']; cases.append(('hidden-compiler-input', candidate))
    candidate = copy.deepcopy(report); candidate['matches'][0]['compiler'] = 'unapproved.exe'; cases.append(('wrong-compiler', candidate))
    candidate = copy.deepcopy(report); candidate['suppliedCalleeSourceOrExecutionCredit'] = 696; cases.append(('duplicate-provider-credit', candidate))
    for key, value in [('module', 'ov000'), ('mode', 'arm'), ('address', '0x2208894')]:
        candidate = copy.deepcopy(report)
        next(iter(candidate['matches'][0]['nativeSymbolEntries'].values()))[key] = value
        cases.append(('wrong-provider-' + key, candidate))
    rejected = []
    for label, candidate in cases:
        try:
            contract(candidate)
        except (AssertionError, KeyError):
            rejected.append(label)
        else:
            raise AssertionError(label)
    assert pinned == {name: sha256(ROOT / name) for name in pinned}
    proof = dict(passed=True, sourceCredit=0, report=REPORT, reportSha256=pinned[REPORT],
        ready=dict(path=READY, sha256=READY_SHA), inputManifest=dict(path=INPUTS, sha256=INPUTS_SHA),
        functions=4, bytes=3008, originalDerivedNativeInputs=refs, sourceAndHeaderCompilerInputsOnly=True,
        freshOriginalRomOverlaySha256=IMAGE_SHA, independentTableBytes=10240, independentRconBytes=40,
        importedStorageCredit=0, selectedKeyEncProviderCountedOnce=True, unselectedCodeProvidersExecuted=0,
        proofs=proofs, rejectedControls=rejected, actualRegistrySourcesObjectsFlagsAndReportsUnchanged=True,
        generatorSha256=sha256(__file__))
    write_json(ROOT / OUTPUT, proof)
    return proof


if __name__ == '__main__':
    result = qualify()
    print(dict(passed=True, functions=4, bytes=3008, negatives=len(result['rejectedControls']), sourceCredit=0))
