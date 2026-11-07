import copy
import hashlib
import struct
from project import ROOT, configuration, read_json, write_json, sha256
from closed_c_compiler_inputs_20261105 import compiler_inputs
from qualify_arm7_wm_second_context_v1_20261106 import arm_mode
from qualify_explicit_c_frontend_20261102 import qualify as fresh_c99
from wave20261106_arm7_wl_driver_timing_source_first_build import FLAGS
from wave20261106_arm7_wl_driver_timing_source_first_link import validate
import link_arm7_bulk_20261030 as original

REPORT = 'evidence/matches/cohort173-parallel-wave20261105-r-arm7-driver-timing-first-0.json'
FOLDER = 'evidence/lanes/parallel-wave20261106/arm7-wl-driver-timing-next/first/'
EXPECTED = {'0x27e97bc':336, '0x27e9d88':180, '0x27eab68':132,
    '0x27eaaf8':112, '0x27e9e3c':100, '0x27e89ec':464}


def qualify():
    assert sha256(ROOT / (FOLDER + 'ready.json')) == 'a55ced212f485b42d9deea07c8663484d08b96695e0ec7b5dae400fdd2686aef'
    report, ready = read_json(ROOT / REPORT), read_json(ROOT / (FOLDER + 'ready.json'))
    assert report['allPassed'] and {r['address']:r['bytes'] for r in report['matches']} == EXPECTED
    assert all(sha256(ROOT / p['path']) == p['sha256'] for p in ready['files'])
    before = {name:sha256(ROOT / name) for name in [REPORT, 'recovery.json', 'source-preferences.json', 'link_arm7_bulk_20261030.py']}
    cfg = configuration()
    assert sha256(cfg['rom']) == cfg['romSha256']
    rom = cfg['rom'].read_bytes()
    offset, entry, load, length = struct.unpack_from('<4I', rom, 0x30)
    assert (offset, entry, load, length) == (624640, 0x02380000, 0x02380000, 160048)
    raw = rom[offset:offset + length]
    assert struct.unpack_from('<3I', raw, 160036) == (0x027e0000, 96388, 6504)
    image = raw[63636:160024]
    assert image == (ROOT / 'extract/arm7/runtime/arm7-main.bin').read_bytes()
    identities = {r['address']:r for r in ready['identities']}
    proofs = []
    for row in report['matches']:
        assert (row.get('program') or '', row['processor'], row['module'], row['mode'], row['sourceModule']) == ('', 'arm7', 'arm7-main', 'arm', 'arm7-main')
        for key in ['address','bytes','source','sourceSha256','targetSha256']:
            assert row[key] == identities[row['address']][key]
        assert row['compilerFlags'] == FLAGS and row['ordinaryCBytes'] == row['bytes'] and row['justifiedAssemblyBytes'] == 0
        compiler_inputs(row)
        mode = arm_mode(row)
        native = image[int(row['address'],0)-0x027e0000:int(row['address'],0)-0x027e0000+row['bytes']]
        assert hashlib.sha256(native).hexdigest() == row['targetSha256']
        adjusted = copy.deepcopy(row)
        index = adjusted['compilerFlags'].index('-lang')
        adjusted['compilerFlags'] = adjusted['compilerFlags'][:index] + adjusted['compilerFlags'][index+2:]
        directory = ROOT / 'work/w6wdt/first/root-context-qualification-v1' / row['address']
        fresh = fresh_c99(adjusted, directory / 'compile')
        rebuilt = dict(row, object=fresh['explicitC99Object'], objectSha256=fresh['explicitC99ObjectSha256'])
        assert arm_mode(rebuilt) == mode
        linked, output = validate(rebuilt, directory / 'link')
        assert output == native and linked['bindings'] == row['nativeSymbolEntries']
        assert all(p['initializedCodeBytes'] == p['calleeSourceCredit'] == 0 for p in linked['zeroCodeAnchors'])
        proofs.append(dict(address=row['address'], bytes=row['bytes'], compilerInputPureC=True,
            freshExplicitC99=fresh, originalMode=mode, completeGenuineLink=linked))
    assert sum(len(r['relocations']) for r in report['matches']) == 71
    callback = read_json(ROOT / (FOLDER + 'callback-qualification-proposal.json'))
    assert len(callback['negativeControls']) == 17 and callback['actualLeafAndTypedPointerABI']['actualNativeAndFreshLeafReturns'] == 10
    assert len(callback['actualLeafAndTypedPointerABI']['negativeActualC']) == 3
    assert before == {name:sha256(ROOT / name) for name in before}
    result = dict(passed=True, sourceCredit=0, functions=6, bytes=1324,
        report=REPORT, reportSha256=before[REPORT], rawRomAutoloadImageVerified=True,
        completeFreshC99AndGenuineModeTypedLinks=proofs, exactCallbackImportAndMathAndTableChecksRetained=True,
        canonicalInventoryOriginalDeriverAndProductionInputsUnchanged=True, generatorSha256=sha256(__file__))
    write_json(ROOT / 'evidence/verification/cohort173-arm7-driver-context-v1-qualification-20261106.json', result)
    return result


if __name__ == '__main__':
    qualify()
    print(dict(passed=True, functions=6, bytes=1324, sourceCredit=0))
