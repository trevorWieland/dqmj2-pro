import copy
import hashlib
from project import ROOT, configuration, native_dependencies, read_json, write_json, sha256
from closed_c_compiler_inputs_20261105 import compiler_inputs
from qualify_explicit_c_frontend_20261102 import qualify as fresh_c99
from qualify_arm9_thumb_reference_inputs_20261105 import object_mode
from qualify_ov006_aes_reference_v1_20261106 import FLAGS, IMAGE, IMAGE_SHA
import link_runtime_unit as linker


REPORT = 'evidence/matches/cohort170-parallel-wave20261105-o-ov006-md5-helpers-first-0.json'
READY = 'evidence/lanes/parallel-wave20261106/ov006-md5-helper-next/ready.json'
INPUTS = 'evidence/lanes/parallel-wave20261106/ov006-md5-helper-next/inputs.json'
EXPECTED = {'0x21f1e40': 44, '0x21f1e6c': 42, '0x21f1e98': 22, '0x21f1eb0': 22}


def contract(report):
    assert sha256(ROOT / READY) == 'fbc8f24c1abceb11946b93ef289346f47a650747952bb14a21391b39c806e157'
    assert sha256(ROOT / INPUTS) == '120b3cbaaace9668c0a514eb9f512d8f800964512abe0f165eff844c8155050d'
    ready = read_json(ROOT / READY)
    assert ready['functions'] == 4 and ready['bytes'] == ready['ordinaryCBytes'] == 130
    assert report['allPassed'] and report['romSha256'] == configuration()['romSha256']
    assert len(report['matches']) == 4 and {row['address']: row['bytes'] for row in report['matches']} == EXPECTED
    assert report['actualNativeAndSourceCallerReturns'] == 92
    assert report['importedProviderSourceOrExecutionCredit'] == 0 and not report['importedOriginalProviderBodiesExecuted']
    assert report['generator'] == 'wave20261106_ov006_md5_helper_next_match.py'
    assert report['generatorSha256'] == sha256(ROOT / report['generator']) == '107a0dc71516701fa3103581d5c864eb025aacbd21b58edb6686b7b07a47739c'
    identities = {row['address']: row for row in ready['identities']}
    for row in report['matches']:
        assert (row.get('program') or '', row['processor'], row['module'], row['mode']) == ('', 'arm9', 'ov006', 'thumb')
        for key in ['address', 'bytes', 'source', 'sourceSha256', 'targetSha256']:
            assert row[key] == identities[row['address']][key]
        assert row['source'] == 'src/ov006/parallel_wave20261106/md5-helper-next/helpers.c'
        assert row['sourceSha256'] == '83b6eaa9487cce136e449082eee8b1c8ab4bb39741d398663a1434884d21204d'
        assert row['sourceDependencies'] == [dict(path='src/ov006/parallel_wave20261106/md5-helper-next/context.h',
            sha256='a74dc33898c81ebd9f52fa7f1c3a519f61035caa3f73b37c6874a5a61ab930d0')]
        assert row['compilerFlags'] == FLAGS and row['compiler'] == 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
        assert row['ordinaryCBytes'] == row['bytes'] and row['justifiedAssemblyBytes'] == 0
        assert not row['nativeSymbolEntries'] and not row['relocations'] and not row['realLink']['originalRelocations']
        assert row['realLink']['exactCallerBytes'] and row['exactAfterDeclaredRelocation']
        assert row['outputSha256'] == row['targetSha256'] == row['realLink']['linkedCallerSha256']
        compiler_inputs(row)
    return ready


def qualify():
    pins = {name: sha256(ROOT / name) for name in ['recovery.json', 'source-preferences.json', REPORT, READY, INPUTS]}
    report = read_json(ROOT / REPORT); ready = contract(report)
    assert all(sha256(ROOT / pin['path']) == pin['sha256'] for pin in ready['files'])
    cfg = configuration(); native_dependencies(cfg)
    import ndspy.rom
    overlay = ndspy.rom.NintendoDSRom(cfg['rom'].read_bytes()).loadArm9Overlays([6])[6]
    image, base = bytes(overlay.data), overlay.ramAddress
    assert image == (ROOT / IMAGE).read_bytes() and hashlib.sha256(image).hexdigest() == IMAGE_SHA
    refs = {pin['path']: pin['sha256'] for pin in read_json(ROOT / INPUTS)['files'] if pin['path'].startswith('extract/')}
    assert refs == {IMAGE: IMAGE_SHA}
    proofs = []
    for row in report['matches']:
        start = int(row['address'], 0) - base
        assert hashlib.sha256(image[start:start + row['bytes']]).hexdigest() == row['targetSha256']
        original_mode = object_mode(row)
        adjusted = copy.deepcopy(row); index = adjusted['compilerFlags'].index('-lang')
        adjusted['compilerFlags'] = adjusted['compilerFlags'][:index] + adjusted['compilerFlags'][index + 2:]
        directory = ROOT / 'work/integration/cohort170-ov006-md5-helpers-reference-v1' / row['address']
        fresh = fresh_c99(adjusted, directory / 'compile')
        entry = {**report, **row, 'object': fresh['explicitC99Object'], 'objectSha256': fresh['explicitC99ObjectSha256']}
        assert object_mode(entry) == original_mode
        linked = linker.validate(entry, {}, directory / 'link')
        assert not linked['originalRelocations'] and not linked['bindingOnlyProbes']
        proofs.append(dict(address=row['address'], bytes=row['bytes'], sourceOnlyCompilerInputs=compiler_inputs(row),
            actualThumbMapping=original_mode, freshExplicitC99=fresh, freshGenuineNativeLink=linked))
    candidates = []
    for field, value in [('program', 'other.srl'), ('processor', 'arm7'), ('module', 'ov000'), ('mode', 'arm'),
                         ('bytes', 42), ('sourceSha256', '0' * 64), ('sourceDependencies', []),
                         ('nativeSymbolEntries', {'hidden': {}}), ('relocations', [{'offset': 0}]),
                         ('compilerFlags', FLAGS + ['-include', 'hidden.h'])]:
        candidate = copy.deepcopy(report); candidate['matches'][0][field] = value; candidates.append(('wrong-' + field, candidate))
    rejected = []
    for label, candidate in candidates:
        try:
            contract(candidate)
        except (AssertionError, KeyError):
            rejected.append(label)
        else:
            raise AssertionError(label)
    assert pins == {name: sha256(ROOT / name) for name in pins}
    result = dict(passed=True, sourceCredit=0, functions=4, bytes=130, report=REPORT, reportSha256=pins[REPORT],
        originalDerivedNativeInputs=refs, proofs=proofs, providerOrStorageCredit=0, rejectedControls=rejected,
        actualSourcesObjectsFlagsReportsAndRegistryUnchanged=True, generatorSha256=sha256(__file__))
    write_json(ROOT / 'evidence/verification/cohort170-ov006-md5-helpers-reference-v1-qualification-20261106.json', result)
    return result


if __name__ == '__main__':
    result = qualify()
    print(dict(passed=True, functions=4, bytes=130, negatives=len(result['rejectedControls']), sourceCredit=0))
