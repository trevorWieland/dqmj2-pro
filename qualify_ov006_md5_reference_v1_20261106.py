import copy
import hashlib
from project import ROOT, configuration, native_dependencies, read_json, write_json, sha256
from closed_c_compiler_inputs_20261105 import compiler_inputs
from qualify_explicit_c_frontend_20261102 import qualify as fresh_c99
from qualify_arm9_thumb_reference_inputs_20261105 import object_mode
from qualify_ov006_aes_reference_v1_20261106 import FLAGS, IMAGE, IMAGE_SHA
from admit_ov006_md5_resumption_v1_20261106 import validate_literal_debt
import link_runtime_unit as linker


REPORT = 'evidence/matches/cohort170-parallel-wave20261105-o-ov006-md5-first-0.json'
READY = 'evidence/lanes/parallel-wave20261106/ov006-md5-next/ready.json'
READY_SHA = 'c10264ece8c35ccd42a94bbe2f67d73c554ce736e4f3eaddd1de62abad65f541'
INPUTS = 'evidence/lanes/parallel-wave20261106/ov006-md5-next/inputs.json'
INPUTS_SHA = '379a4d7f5bccc70190fb653c699bce6c8c9e172d926c12bee09d6238fbcec35b'
OUTPUT = 'evidence/verification/cohort170-ov006-md5-reference-v1-qualification-20261106.json'
EXPECTED = {'0x21f152c': 118, '0x21f15a4': 84, '0x21f15f8': 2120}
CODE = {0x021f152c, 0x021f15f8, 0x021f1e40, 0x021f1e6c, 0x021f1e98, 0x021f1eb0}


def contract(report):
    assert sha256(ROOT / READY) == READY_SHA and sha256(ROOT / INPUTS) == INPUTS_SHA
    ready = read_json(ROOT / READY)
    assert ready['functions'] == 3 and ready['bytes'] == ready['ordinaryCBytes'] == 2322
    assert report['allPassed'] and report['romSha256'] == configuration()['romSha256']
    assert len(report['matches']) == 3 and {row['address']: row['bytes'] for row in report['matches']} == EXPECTED
    assert report['actualNativeAndSourceCallerReturns'] == 76
    assert report['suppliedCalleeSourceOrExecutionCredit'] == report['importedProviderSourceOrExecutionCredit'] == 0
    assert report['generator'] == 'wave20261106_ov006_md5_next_match.py'
    assert report['generatorSha256'] == sha256(ROOT / report['generator']) == 'e5071ab1f61900c0dfa292d1dc98ce2891a7d84bae402e1c1508de79c7a2fefd'
    identities = {row['address']: row for row in ready['identities']}
    seen_code, seen_data = set(), set()
    for row in report['matches']:
        assert (row.get('program') or '', row['processor'], row['module'], row['mode']) == ('', 'arm9', 'ov006', 'thumb')
        for key in ['address', 'bytes', 'source', 'sourceSha256', 'targetSha256']:
            assert row[key] == identities[row['address']][key]
        assert row['source'] == 'src/ov006/parallel_wave20261106/md5-next/md5.c'
        assert row['sourceSha256'] == '4bb201f332bfdbea8a5dfb79712269a692e1274f8c9368940b2ce61c77820c8d'
        assert row['sourceDependencies'] == [dict(path='src/ov006/parallel_wave20261106/md5-next/context.h',
            sha256='ae4eeff3812844242bcf529d1d5923cb117cfe7bc9a3657a5a7925afbd6bf7fd')]
        assert row['compilerFlags'] == FLAGS and row['compiler'] == 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
        assert row['ordinaryCBytes'] == row['bytes'] and row['justifiedAssemblyBytes'] == 0
        assert row['realLink']['exactCallerBytes'] and row['exactAfterDeclaredRelocation']
        assert row['outputSha256'] == row['targetSha256'] == row['realLink']['linkedCallerSha256']
        compiler_inputs(row)
        for name, binding in row['nativeSymbolEntries'].items():
            assert (binding.get('program') or '', binding['processor'], binding['module']) == ('', 'arm9', 'ov006')
            address = int(binding['address'], 0)
            if binding['kind'] == 'function':
                assert binding['mode'] == 'thumb' and address in CODE and name == f'native_ov006_{address:08x}'
                seen_code.add(address)
            else:
                assert binding['kind'] == binding['mode'] == 'data' and address == 0x0220d500
                assert name == 'native_data_ov006_0220d500'
                seen_data.add(address)
    assert seen_code == CODE and seen_data == {0x0220d500}
    arithmetic = read_json(ROOT / 'evidence/lanes/parallel-wave20261106/ov006-md5-next/arithmetic-interface.json')
    assert arithmetic['originalRecordRemainsUnchanged'] and arithmetic['objectRequiresNoMainPointerRelocationOrBinding']
    assert arithmetic['scalar'] == 0x021ac7f4 and arithmetic['md5Step'] == 36 and arithmetic['rotateLeft'] == 23
    assert arithmetic['originalInputRewrites'] == arithmetic['inventedAliases'] == 0
    return ready


def scalar_object(row):
    from elftools.elf.elffile import ELFFile
    offset = row['sectionOffset'] + (0x021f1dcc - 0x021f15f8)
    with (ROOT / row['object']).open('rb') as stream:
        elf = ELFFile(stream)
        section = elf.get_section(row['sectionIndex'])
        assert section.data()[offset:offset + 4] == (0x021ac7f4).to_bytes(4, 'little')
        relocations = [rel for sec in elf.iter_sections() if sec['sh_type'] in ['SHT_REL', 'SHT_RELA'] and
            sec['sh_info'] == row['sectionIndex'] for rel in sec.iter_relocations()]
        assert not any(rel['r_offset'] == offset for rel in relocations)
        assert len(relocations) == 2
    return dict(literalObjectOffset=offset, rawObjectScalar='0x021ac7f4', pointerRelocationsAtScalar=0,
        actualCompressionRelocations=2, originalConfiguredMainRecordPreserved=True)


def qualify():
    pins = {name: sha256(ROOT / name) for name in ['recovery.json', 'source-preferences.json', REPORT, READY, INPUTS]}
    report = read_json(ROOT / REPORT)
    ready = contract(report)
    assert all(sha256(ROOT / pin['path']) == pin['sha256'] for pin in ready['files'])
    refs = {pin['path']: pin['sha256'] for pin in read_json(ROOT / INPUTS)['files'] if pin['path'].startswith('extract/')}
    assert refs == {IMAGE: IMAGE_SHA}
    cfg = configuration(); native_dependencies(cfg)
    assert sha256(cfg['rom']) == cfg['romSha256']
    import ndspy.rom
    overlay = ndspy.rom.NintendoDSRom(cfg['rom'].read_bytes()).loadArm9Overlays([6])[6]
    image, base = bytes(overlay.data), overlay.ramAddress
    assert image == (ROOT / IMAGE).read_bytes() and hashlib.sha256(image).hexdigest() == IMAGE_SHA
    literal_debt = validate_literal_debt(image, base)
    assert image[0x0220d500 - base:0x0220d540 - base] == b'\x80' + b'\0' * 63
    proofs = []
    for row in report['matches']:
        offset = int(row['address'], 0) - base
        assert hashlib.sha256(image[offset:offset + row['bytes']]).hexdigest() == row['targetSha256']
        mode = object_mode(row)
        adjusted = copy.deepcopy(row); index = adjusted['compilerFlags'].index('-lang')
        adjusted['compilerFlags'] = adjusted['compilerFlags'][:index] + adjusted['compilerFlags'][index + 2:]
        directory = ROOT / 'work/integration/cohort170-ov006-md5-reference-v1' / row['address']
        fresh = fresh_c99(adjusted, directory / 'compile')
        entry = {**report, **row, 'object': fresh['explicitC99Object'], 'objectSha256': fresh['explicitC99ObjectSha256']}
        assert object_mode(entry) == mode
        scalar = scalar_object(entry) if row['address'] == '0x21f15f8' else None
        linked = linker.validate(entry, row['nativeSymbolEntries'], directory / 'link')
        assert all(probe['initializedCodeBytes'] == probe['nativeCalleeBytesUsed'] == probe['calleeSourceCredit'] == 0 for probe in linked['bindingOnlyProbes'])
        for name, binding in row['nativeSymbolEntries'].items():
            linker.verify_binding(name, binding)
        proofs.append(dict(address=row['address'], bytes=row['bytes'], sourceOnlyCompilerInputs=compiler_inputs(row),
            actualThumbMapping=mode, freshExplicitC99=fresh, freshGenuineNativeLink=linked, arithmeticLiteral=scalar))
    cases = []
    for key, value in [('program', 'other/child.srl'), ('processor', 'arm7'), ('module', 'ov000'),
                       ('mode', 'arm'), ('bytes', 116), ('sourceSha256', '0' * 64), ('compiler', 'unapproved.exe')]:
        candidate = copy.deepcopy(report); candidate['matches'][0][key] = value; cases.append(('wrong-' + key, candidate))
    candidate = copy.deepcopy(report); candidate['matches'].pop(); cases.append(('missing-function', candidate))
    candidate = copy.deepcopy(report); candidate['matches'][0]['compilerFlags'] = FLAGS + ['-include', 'hidden.h']; cases.append(('hidden-compiler-input', candidate))
    candidate = copy.deepcopy(report); candidate['importedProviderSourceOrExecutionCredit'] = 1; cases.append(('provider-credit', candidate))
    for key, value in [('module', 'main'), ('mode', 'arm'), ('address', '0x21ac7f4')]:
        candidate = copy.deepcopy(report); next(iter(candidate['matches'][0]['nativeSymbolEntries'].values()))[key] = value
        cases.append(('wrong-binding-' + key, candidate))
    rejected = []
    for label, candidate in cases:
        try:
            contract(candidate)
        except (AssertionError, KeyError):
            rejected.append(label)
        else:
            raise AssertionError(label)
    assert pins == {name: sha256(ROOT / name) for name in pins}
    result = dict(passed=True, sourceCredit=0, functions=3, bytes=2322, report=REPORT, reportSha256=pins[REPORT],
        originalDerivedNativeInputs=refs, freshOriginalRomOverlaySha256=IMAGE_SHA, proofs=proofs,
        independentlyProvenNativeArithmeticLiteral=literal_debt, originalMainRecordNeverRewritten=True,
        noPointerAliasAtArithmeticScalar=True, importedRuntimeOracleHelpersSourceCredit=0,
        importedOriginalProviderExecutions=report['importedOriginalProviderBodiesExecuted'],
        allOriginalRegisteredSourcesObjectsFlagsAndReportsUnchanged=True, rejectedControls=rejected,
        generatorSha256=sha256(__file__))
    write_json(ROOT / OUTPUT, result)
    return result


if __name__ == '__main__':
    result = qualify()
    print(dict(passed=True, functions=3, bytes=2322, negatives=len(result['rejectedControls']), sourceCredit=0))
