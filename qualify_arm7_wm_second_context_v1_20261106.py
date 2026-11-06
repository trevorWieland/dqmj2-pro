import copy
import hashlib
import struct
from project import ROOT, configuration, read_json, write_json, sha256
from closed_c_compiler_inputs_20261105 import compiler_inputs
from qualify_explicit_c_frontend_20261102 import qualify as fresh_c99
from elftools.elf.elffile import ELFFile
from wave20261106_arm7_wm_residual_next_second_build import FLAGS
from wave20261106_arm7_wm_residual_next_second_link import validate
from wave20261106_arm7_wm_residual_next_second_math import controls


REPORT = 'evidence/matches/cohort170-parallel-wave20261105-o-arm7-wm-residual-second-0.json'
FOLDER = 'evidence/lanes/parallel-wave20261106/arm7-wm-residual-next/second/'
EXPECTED = {'0x27e386c': 1300, '0x27e3ed0': 1444, '0x27e4be0': 916}


def contract(report):
    assert report['allPassed'] and report['actualNativeAndSourceCallerReturns'] == 132
    assert report['nativeCalleeBodiesExecutedInCallerFixtures'] == report['calleeSourceCredit'] == 0
    assert len(report['matches']) == 3 and {r['address']: r['bytes'] for r in report['matches']} == EXPECTED
    ready = read_json(ROOT / (FOLDER + 'ready.json'))
    identities = {row['address']: row for row in ready['identities']}
    for row in report['matches']:
        assert (row.get('program') or '', row['processor'], row['module'], row['mode'], row['sourceModule']) == ('', 'arm7', 'arm7-main', 'arm', 'arm7-main')
        for key in ['address', 'bytes', 'source', 'sourceSha256', 'targetSha256']:
            assert row[key] == identities[row['address']][key]
        assert row['compilerFlags'] == FLAGS and row['compiler'] == 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
        assert row['ordinaryCBytes'] == row['bytes'] and row['justifiedAssemblyBytes'] == 0
        assert row['exactAfterDeclaredRelocation'] and row['realLink']['exactCallerBytes']
        assert row['outputSha256'] == row['targetSha256'] == row['realLink']['linkedCallerSha256']
        compiler_inputs(row)
    assert sum(len(row['relocations']) for row in report['matches']) == 106
    return ready


def arm_mode(entry):
    with (ROOT / entry['object']).open('rb') as stream:
        elf = ELFFile(stream); symbols = list(elf.get_section_by_name('.symtab').iter_symbols())
        own = [s for s in symbols if s.name == entry['name']]
        assert elf.elfclass == 32 and elf.little_endian and len(own) == 1
        symbol = own[0]; start = symbol['st_value']
        assert symbol['st_info']['type'] == 'STT_FUNC' and symbol['st_size'] == entry['bytes'] and start % 4 == 0
        assert any(s.name == '$a' and s['st_shndx'] == symbol['st_shndx'] and s['st_value'] == start for s in symbols)
    return dict(mapping='$a', relocatableFunctionValue=start)


def qualify():
    fixed = {FOLDER + 'ready.json': 'f3bfa7a2c165531417591d049844dbcb24fa1b5b16079ece5d138e5603b477ec',
        FOLDER + 'inputs.json': '27c6259f46cc4e81446d4b2a4db0588048d3bd428deb533c3a72937c1fcb5898',
        FOLDER + 'compiler-helper-certificate.json': '336c4eeb493d50608a54c1d4112215a0f1cd63a8402a981668e035c0efd5426a',
        'wave20261106_arm7_wm_residual_next_second_link.py': 'c97c869a8fa33f04c2a821c48ba17b0b964cf8448f38e315d5163a12669178c1',
        'wave20261106_arm7_wm_residual_next_second_math.py': 'a15cca5c04284a8a7f9c4134c765ca4c73dbbbf33fc83430eb8a13b4d82de227'}
    assert all(sha256(ROOT / name) == digest for name, digest in fixed.items())
    pins = {name: sha256(ROOT / name) for name in [REPORT, 'recovery.json', 'source-preferences.json']}
    report = read_json(ROOT / REPORT); ready = contract(report)
    assert all(sha256(ROOT / pin['path']) == pin['sha256'] for pin in ready['files'])
    cfg = configuration(); assert sha256(cfg['rom']) == cfg['romSha256']
    rom = cfg['rom'].read_bytes()
    offset, entry, load, length = struct.unpack_from('<4I', rom, 0x30)
    assert (offset, entry, load, length) == (624640, 0x02380000, 0x02380000, 160048)
    raw = rom[offset:offset + length]
    assert struct.unpack_from('<3I', raw, 160024) == (0x037f8000, 63096, 15980)
    assert struct.unpack_from('<3I', raw, 160036) == (0x027e0000, 96388, 6504)
    layout = read_json(ROOT / 'evidence/arm7/runtime-layout.json'); modules = {}
    for module in layout['modules']:
        data = raw[module['inputFileOffset']:module['inputFileOffset'] + module['inputBytes']]
        assert data == (ROOT / module['binary']).read_bytes() and hashlib.sha256(data).hexdigest() == module['sha256']
        modules[module['name']] = data
    proofs = []
    for row in report['matches']:
        start = int(row['address'], 0) - 0x027e0000
        assert hashlib.sha256(modules['arm7-main'][start:start + row['bytes']]).hexdigest() == row['targetSha256']
        original_mode = arm_mode(row)
        adjusted = copy.deepcopy(row); index = adjusted['compilerFlags'].index('-lang')
        adjusted['compilerFlags'] = adjusted['compilerFlags'][:index] + adjusted['compilerFlags'][index + 2:]
        directory = ROOT / 'work/w6wr/second/root-context-qualification-v1' / row['address']
        fresh = fresh_c99(adjusted, directory / 'compile')
        rebuilt = {**row, 'object': fresh['explicitC99Object'], 'objectSha256': fresh['explicitC99ObjectSha256']}
        assert arm_mode(rebuilt) == original_mode
        linked, output = validate(rebuilt, directory / 'link')
        assert output == modules['arm7-main'][start:start + row['bytes']]
        assert linked['bindings'] == row['nativeSymbolEntries']
        assert all(p['initializedCodeBytes'] == p['calleeSourceCredit'] == 0 for p in linked['zeroCodeAnchors'])
        proofs.append(dict(address=row['address'], bytes=row['bytes'], freshExplicitC99=fresh, armMapping=original_mode,
            completeOriginalRelocationsAndGenuineLink=linked))
    helper_proof = controls(report['matches'])
    assert len(helper_proof['positive']) == 2 and len(helper_proof['negativeControls']) == 22
    abi = helper_proof['actualCompilerAndOriginalNativeABI']; assert abi['actualNativeOriginalHelperReturns'] == 28
    for probe in abi['probes']:
        for case in probe['cases']:
            a, b = case['a'], case['b']; assert b
            quotient = (abs(a) // abs(b)) * (-1 if (a < 0) != (b < 0) else 1) if probe['typedReturn'] == 's32' else a // b
            expected = a - quotient * b if probe['operator'] == '%' else quotient
            assert case['returned'] == expected & 0xffffffff and case['actualOriginalHelperInstructions'] > 0
    assert pins == {name: sha256(ROOT / name) for name in pins}
    assert all(sha256(ROOT / pin['path']) == pin['sha256'] for pin in ready['files'])
    result = dict(passed=True, sourceCredit=0, functions=3, bytes=3660, report=REPORT, reportSha256=pins[REPORT],
        originalRomModuleDerivation=True, originalCompilerHelperNamesAndProvidersUnchanged=True,
        actualFull106RelocationsRetained=True, proofs=proofs, helperProof=helper_proof,
        allProductionSourcesObjectsFlagsReportsAndRegistryUnchanged=True, generatorSha256=sha256(__file__))
    write_json(ROOT / 'evidence/verification/cohort170-arm7-wm-second-context-v1-qualification-20261106.json', result)
    return result


if __name__ == '__main__':
    result = qualify()
    print(dict(passed=True, functions=3, bytes=3660, originalHelperReturns=28, sourceCredit=0))
