import copy
import hashlib
from project import ROOT, configuration, native_dependencies, read_json, write_json, sha256
from closed_c_compiler_inputs_20261105 import compiler_inputs
from qualify_explicit_c_frontend_20261102 import qualify as fresh_c99
from qualify_arm9_thumb_reference_inputs_20261105 import object_mode, derive as derive_main
from qualify_ov006_aes_reference_v1_20261106 import FLAGS, IMAGE, IMAGE_SHA
import link_runtime_unit as linker


REPORT = 'evidence/matches/cohort170-parallel-wave20261105-o-ov006-crypto-utility-first-0.json'
READY = 'evidence/lanes/parallel-wave20261106/ov006-crypto-utility-next/first/ready.json'
INPUTS = 'evidence/lanes/parallel-wave20261106/ov006-crypto-utility-next/first/inputs.json'
ABI = 'evidence/lanes/parallel-wave20261106/ov006-crypto-utility-next/runtime-helper-abi.json'
EXPECTED = {'0x21ed86c': 98, '0x21ed8d0': 44, '0x21ed8fc': 62, '0x21ed964': 54, '0x21f08fc': 70}
BINDINGS = {
    '0x21ed86c': {'_u32_div_f': ('main', 'arm', 0x02026350)},
    '0x21ed8d0': {'native_ov006_021ed8fc': ('ov006', 'thumb', 0x021ed8fc)},
    '0x21ed8fc': {'_u32_div_f': ('main', 'arm', 0x02026350)},
    '0x21ed964': {'native_ov006_021ed99c': ('ov006', 'thumb', 0x021ed99c)}, '0x21f08fc': {}}


def contract(report):
    assert sha256(ROOT / READY) == '6e9dac2d98b58b93f8cb905f5c772bc761ef902e80676e8cbca27b61471cdea3'
    assert sha256(ROOT / INPUTS) == '724dd13be6781b844a63a712ebe4e005ec809dd56beae1ef91d9b2714c5b18b6'
    ready = read_json(ROOT / READY)
    assert ready['functions'] == 5 and ready['bytes'] == ready['ordinaryCBytes'] == 328
    assert report['allPassed'] and report['romSha256'] == configuration()['romSha256']
    assert len(report['matches']) == 5 and {row['address']: row['bytes'] for row in report['matches']} == EXPECTED
    assert report['actualNativeAndSourceCallerReturns'] == 70
    assert report['suppliedCalleeSourceOrExecutionCredit'] == report['importedProviderSourceOrExecutionCredit'] == 0
    assert report['generator'] == 'wave20261106_ov006_crypto_utility_next_first_match.py'
    assert report['generatorSha256'] == sha256(ROOT / report['generator']) == 'e2e4cd4b634d8a689dc0097d394567eebf493b8cc0c5e544d94c55049563e78e'
    identities = {row['address']: row for row in ready['identities']}
    for row in report['matches']:
        assert (row.get('program') or '', row['processor'], row['module'], row['mode']) == ('', 'arm9', 'ov006', 'thumb')
        for key in ['address', 'bytes', 'source', 'sourceSha256', 'targetSha256']:
            assert row[key] == identities[row['address']][key]
        assert row['source'] == 'src/ov006/parallel_wave20261106/crypto-utility-next/first/crypto.c'
        assert row['sourceSha256'] == 'b0f10f3538508e79e66a0f3b8c736a1eb7f35e533371b0435da7837f06c74a0a'
        assert row['sourceDependencies'] == [dict(path='src/ov006/parallel_wave20261106/crypto-utility-next/first/context.h',
            sha256='5a6fb917762205fa4628546324b9285e9ec4c379ea4b77ba4922e53448df2df8')]
        assert row['compilerFlags'] == FLAGS and row['compiler'] == 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
        assert row['ordinaryCBytes'] == row['bytes'] and row['justifiedAssemblyBytes'] == 0
        assert row['realLink']['exactCallerBytes'] and row['exactAfterDeclaredRelocation']
        assert row['outputSha256'] == row['targetSha256'] == row['realLink']['linkedCallerSha256']
        compiler_inputs(row)
        assert set(row['nativeSymbolEntries']) == set(BINDINGS[row['address']])
        for name, binding in row['nativeSymbolEntries'].items():
            assert (binding.get('program') or '', binding['processor'], binding['kind']) == ('', 'arm9', 'function')
            assert (binding['module'], binding['mode'], int(binding['address'], 0)) == BINDINGS[row['address']][name]
    return ready


def qualify():
    pins = {name: sha256(ROOT / name) for name in ['recovery.json', 'source-preferences.json', REPORT, READY, INPUTS, ABI]}
    report = read_json(ROOT / REPORT); ready = contract(report)
    assert all(sha256(ROOT / pin['path']) == pin['sha256'] for pin in ready['files'])
    assert pins[ABI] == 'd5b8743537544baf5a3a8bdca9be23d894b6d6e19119080c28eedb7d95adaefd'
    main_image = derive_main()
    cfg = configuration(); native_dependencies(cfg)
    import ndspy.rom
    overlay = ndspy.rom.NintendoDSRom(cfg['rom'].read_bytes()).loadArm9Overlays([6])[6]
    image, base = bytes(overlay.data), overlay.ramAddress
    assert image == (ROOT / IMAGE).read_bytes() and hashlib.sha256(image).hexdigest() == IMAGE_SHA
    refs = {pin['path']: pin['sha256'] for pin in read_json(ROOT / INPUTS)['files'] if pin['path'].startswith('extract/')}
    assert refs == {IMAGE: IMAGE_SHA, 'extract/arm9/arm9.bin': hashlib.sha256(main_image).hexdigest()}
    abi = read_json(ROOT / ABI)
    assert abi['allPassed'] and not abi['mainInteriorEntryAliasesAuthorized'] and abi['sourceOrExecutionCredit'] == 0
    assert {int(helper['address'], 0): helper['bytes'] for helper in abi['helpers']} == {0x02026124: 32, 0x02026350: 484}
    cases = 0
    for helper in abi['helpers']:
        start = int(helper['address'], 0) - 0x02000000
        assert hashlib.sha256(main_image[start:start + helper['bytes']]).hexdigest() == helper['nativeSpanSha256']
        for case in helper['cases']:
            args = case['arguments']
            if int(helper['address'], 0) == 0x02026124:
                value = ((args[0] | args[1] << 32) * (args[2] | args[3] << 32)) & ((1 << 64) - 1)
                result = value & 0xffffffff, value >> 32
            else:
                assert args[1] > 0
                result = args[0] // args[1], args[0] % args[1]
            assert (case['r0'], case['r1']) == result and case['calleeSavedAndStackPointerPreserved']
            cases += 1
    assert cases == 168
    proofs = []
    for row in report['matches']:
        start = int(row['address'], 0) - base
        assert hashlib.sha256(image[start:start + row['bytes']]).hexdigest() == row['targetSha256']
        original_mode = object_mode(row)
        adjusted = copy.deepcopy(row); index = adjusted['compilerFlags'].index('-lang')
        adjusted['compilerFlags'] = adjusted['compilerFlags'][:index] + adjusted['compilerFlags'][index + 2:]
        directory = ROOT / 'work/integration/cohort170-ov006-crypto-reference-v1' / row['address']
        fresh = fresh_c99(adjusted, directory / 'compile')
        entry = {**report, **row, 'object': fresh['explicitC99Object'], 'objectSha256': fresh['explicitC99ObjectSha256']}
        assert object_mode(entry) == original_mode
        linked = linker.validate(entry, row['nativeSymbolEntries'], directory / 'link')
        assert all(probe['initializedCodeBytes'] == probe['nativeCalleeBytesUsed'] == probe['calleeSourceCredit'] == 0 for probe in linked['bindingOnlyProbes'])
        proofs.append(dict(address=row['address'], bytes=row['bytes'], sourceOnlyCompilerInputs=compiler_inputs(row),
            actualThumbMapping=original_mode, freshExplicitC99=fresh, freshGenuineNativeLink=linked))
    candidates = []
    for field, value in [('processor', 'arm7'), ('module', 'ov000'), ('mode', 'arm'), ('bytes', 96), ('sourceSha256', '0' * 64)]:
        candidate = copy.deepcopy(report); candidate['matches'][0][field] = value; candidates.append(('wrong-' + field, candidate))
    for field, value in [('processor', 'arm7'), ('module', 'ov006'), ('mode', 'thumb'), ('address', '0x2026354')]:
        candidate = copy.deepcopy(report); candidate['matches'][0]['nativeSymbolEntries']['_u32_div_f'][field] = value
        candidates.append(('wrong-provider-' + field, candidate))
    candidate = copy.deepcopy(report); candidate['matches'][0]['nativeSymbolEntries']['native_div_alias'] = candidate['matches'][0]['nativeSymbolEntries'].pop('_u32_div_f'); candidates.append(('rewritten-compiler-symbol', candidate))
    candidate = copy.deepcopy(report); candidate['matches'][0]['compilerFlags'] = FLAGS + ['-include', 'hidden.h']; candidates.append(('hidden-compiler-input', candidate))
    rejected = []
    for label, candidate in candidates:
        try:
            contract(candidate)
        except (AssertionError, KeyError):
            rejected.append(label)
        else:
            raise AssertionError(label)
    assert pins == {name: sha256(ROOT / name) for name in pins}
    result = dict(passed=True, sourceCredit=0, functions=5, bytes=328, report=REPORT, reportSha256=pins[REPORT],
        originalDerivedNativeInputs=refs, helperAbiCasesIndependentlyChecked=168, proofs=proofs,
        actualCompilerImportNamePreserved='_u32_div_f', providerOrStorageCredit=0, rejectedControls=rejected,
        actualSourcesObjectsFlagsReportsAndRegistryUnchanged=True, generatorSha256=sha256(__file__))
    write_json(ROOT / 'evidence/verification/cohort170-ov006-crypto-reference-v1-qualification-20261106.json', result)
    return result


if __name__ == '__main__':
    result = qualify()
    print(dict(passed=True, functions=5, bytes=328, negatives=len(result['rejectedControls']), sourceCredit=0))
