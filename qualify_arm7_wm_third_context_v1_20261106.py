import copy
import hashlib
import struct
from project import ROOT, configuration, read_json, write_json, sha256
from qualify_arm7_wm_second_context_v1_20261106 import arm_mode, fresh_c99, compiler_inputs
from wave20261106_arm7_wm_residual_next_third_build import FLAGS
from wave20261106_arm7_wm_residual_next_third_link import validate
from wave20261106_arm7_wm_residual_next_third_callbacks import qualify as callback, controls
from wave20261106_arm7_wm_residual_next_third_callback_probes import execute as pointer_probes
import link_arm7_bulk_20261030 as original


REPORT = 'evidence/matches/cohort170-parallel-wave20261105-o-arm7-wm-residual-third-0.json'
FOLDER = 'evidence/lanes/parallel-wave20261106/arm7-wm-residual-next/third/'
EXPECTED = {'0x27e03d0': 336, '0x27e0520': 68, '0x27e5c5c': 356, '0x27e5dc0': 192, '0x27e5e80': 280, '0x27e5f98': 184}


def qualify():
    fixed = {FOLDER + 'ready.json': '6dd45fa236736ed1f41bf12855c5a2f5116d4c313e928b9e0638c67ce81aa815',
        FOLDER + 'inputs.json': '785e5951920639085905383e331f018198b931ed23d50fd984dd1c5bae847f7a',
        FOLDER + 'callback-certificate.json': '5966167fe93696584faa97998136a2cb8d3fa5a018d5583fb24057afba86d0fd',
        'wave20261106_arm7_wm_residual_next_third_callbacks.py': 'ce9c1d23c036e2930562649004f9e9072f367dd3c6df057b230fc91cd9bdac06',
        'wave20261106_arm7_wm_residual_next_third_link.py': '48025ac8313bdf402dc28970f493e90b37725bbd6134eacebe4fe93e760bd27a',
        'wave20261106_arm7_wm_residual_next_third_callback_probes.py': '8f20fdb33f997d0472b28d080bd1cbc7dc22be0c5dc1676c5cdbcb5c8f5ad5a0'}
    assert all(sha256(ROOT / name) == digest for name, digest in fixed.items())
    pins = {name: sha256(ROOT / name) for name in [REPORT, 'recovery.json', 'source-preferences.json', original.__file__]}
    report = read_json(ROOT / REPORT); ready = read_json(ROOT / (FOLDER + 'ready.json'))
    assert report['allPassed'] and report['actualNativeAndSourceCallerReturns'] == 262
    assert report['nativeCalleeBodiesExecutedInCallerFixtures'] == report['calleeSourceCredit'] == 0
    assert len(report['matches']) == 6 and {r['address']: r['bytes'] for r in report['matches']} == EXPECTED
    assert all(sha256(ROOT / pin['path']) == pin['sha256'] for pin in ready['files'])
    identities = {r['address']: r for r in ready['identities']}
    cfg = configuration(); assert sha256(cfg['rom']) == cfg['romSha256']; rom = cfg['rom'].read_bytes()
    offset, entry, load, length = struct.unpack_from('<4I', rom, 0x30)
    assert (offset, entry, load, length) == (624640, 0x02380000, 0x02380000, 160048)
    raw = rom[offset:offset + length]; image = raw[63636:160024]
    assert image == (ROOT / 'extract/arm7/runtime/arm7-main.bin').read_bytes()
    modules, functions = original.namespace(''); sites = read_json(ROOT / (FOLDER + 'callback-certificate.json'))['callbacks']
    proofs = []; delta = []
    for row in report['matches']:
        assert (row.get('program') or '', row['processor'], row['module'], row['mode'], row['sourceModule']) == ('', 'arm7', 'arm7-main', 'arm', 'arm7-main')
        for key in ['address', 'bytes', 'source', 'sourceSha256', 'targetSha256']:
            assert row[key] == identities[row['address']][key]
        assert row['compilerFlags'] == FLAGS and row['ordinaryCBytes'] == row['bytes'] and row['justifiedAssemblyBytes'] == 0
        compiler_inputs(row); arm_mode(row)
        start = int(row['address'], 0) - 0x027e0000; native = image[start:start + row['bytes']]
        assert hashlib.sha256(native).hexdigest() == row['targetSha256']
        derived = original.derive_bindings(row, native, functions, modules)
        for site in [site for site in sites if site['callerAddress'] == row['address']]:
            matches = [rel for rel in row['relocations'] if int(row['address'], 0) + rel['offset'] == int(site['origin'], 0)]
            assert len(matches) == 1
            binding, proof = callback(row, matches[0], functions, modules)
            delta.append(dict(originalHeuristic=derived[site['symbol']], typedCanonicalBinding=binding, proof=proof))
            derived[site['symbol']] = binding
        assert derived == row['nativeSymbolEntries']
        adjusted = copy.deepcopy(row); index = adjusted['compilerFlags'].index('-lang')
        adjusted['compilerFlags'] = adjusted['compilerFlags'][:index] + adjusted['compilerFlags'][index + 2:]
        directory = ROOT / 'work/w6wr/third/root-context-qualification-v1' / row['address']
        fresh = fresh_c99(adjusted, directory / 'compile')
        rebuilt = {**row, 'object': fresh['explicitC99Object'], 'objectSha256': fresh['explicitC99ObjectSha256']}
        assert arm_mode(rebuilt) == arm_mode(row)
        linked, output = validate(rebuilt, directory / 'link')
        assert output == native and linked['bindings'] == row['nativeSymbolEntries']
        assert all(p['initializedCodeBytes'] == p['calleeSourceCredit'] == 0 for p in linked['zeroCodeAnchors'])
        proofs.append(dict(address=row['address'], bytes=row['bytes'], freshExplicitC99=fresh, genuineLink=linked))
    assert len(delta) == 5 and sum(len(row['relocations']) for row in report['matches']) == 37
    controlled = controls(report['matches']); assert len(controlled['negativeControls']) == 60
    pointers = pointer_probes(report['matches'])
    assert pointers['uniqueCallbackTargets'] == 4 and sum(len(p['negativeControls']) for p in pointers['witnesses']) == 8
    assert pins == {name: sha256(ROOT / name) for name in pins}
    assert all(sha256(ROOT / pin['path']) == pin['sha256'] for pin in ready['files'])
    result = dict(passed=True, sourceCredit=0, functions=6, bytes=1416, report=REPORT, reportSha256=pins[REPORT],
        originalRawRomMainSliceVerified=True, typedOriginalFiveCallbackSites=delta, proofs=proofs,
        callbackControls=controlled, actualC99PointerWitnesses=pointers,
        originalDeriverAndProductionObjectsSourcesFlagsReportsRegistryUnchanged=True,
        noGlobalProductionRoutingOrNewCallableAliases=True, generatorSha256=sha256(__file__))
    write_json(ROOT / 'evidence/verification/cohort170-arm7-wm-third-context-v1-qualification-20261106.json', result)
    return result


if __name__ == '__main__':
    qualify(); print(dict(passed=True, functions=6, bytes=1416, typedCallbackSites=5, sourceCredit=0))
