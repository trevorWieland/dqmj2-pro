import copy
import subprocess
from contextlib import contextmanager
from unittest.mock import patch
from project import ROOT, configuration, read_json, write_json, sha256
from closed_c_compiler_inputs_20261105 import compiler_inputs
from qualify_explicit_c_frontend_20261102 import qualify as qualify_c99
import qualify_arm9_overlay_reference_inputs_20261105 as overlay
import link_runtime_unit as linker

REPORT = 'evidence/matches/cohort167-parallel-wave20261105-l-game-main-arm-next-third-0.json'
REPORT_SHA = 'ac3335b83cd49812a76376a5092dc4691ba84213e734c69a6e7f09b2d8048599'
READY = 'evidence/lanes/parallel-wave20261105/game-main-arm-next/third/ready.json'
READY_SHA = '2a86eb13a7423aa9195d112cc950da360b0d26da71b41cb07bcfb3df4bc731d9'
EXPECTED = {'0x207211c': 152, '0x2071b28': 116, '0x2073090': 172, '0x207313c': 112}
PROOF = 'evidence/verification/cohort167-game-overlay-reference-route-v1-qualification-20261106.json'
FLAGS = ['-O2', '-enum', 'int', '-char', 'signed', '-str', 'noreuse', '-proc', 'arm946e',
         '-gccext,on', '-fp', 'soft', '-inline', 'on', '-Cpp_exceptions', 'off', '-RTTI', 'off',
         '-interworking', '-w', 'off', '-sym', 'on', '-gccinc', '-nolink', '-msgstyle', 'gcc',
         '-lang', 'c99', '-opt', 'speed']


def contract(batch, report):
    assert batch['report'] == REPORT and report['allPassed']
    assert report['romSha256'] == overlay.ROM_SHA
    assert {r['address']: r['bytes'] for r in report['matches']} == EXPECTED
    assert len(report['matches']) == 4
    assert [p for p in batch['sourceHashes'] if p.startswith('extract/')] == [overlay.REFERENCE]
    assert batch['sourceHashes'][overlay.REFERENCE] == overlay.REFERENCE_SHA
    for row in report['matches']:
        assert (row.get('program') or '', row['processor'], row['module'], row['mode']) == ('', 'arm9', 'main', 'arm')
        assert row['compilerFlags'] == FLAGS and row['bytes'] == EXPECTED[row['address']]
        assert row['realLink']['exactCallerBytes'] and row['exactAfterDeclaredRelocation']
        assert row['targetSha256'] == row['outputSha256'] == row['realLink']['linkedCallerSha256']
        compiler_inputs(row)
    bindings = report['nativeSymbolBindings']
    selected = {name: b for name, b in bindings.items() if b['module'] == 'ov000'}
    assert len(selected) == 5
    assert {b['address'] for b in selected.values()} == {'0x2215698', '0x22162c0', '0x2216664', '0x2215078', '0x21e7b9c'}
    assert all((b.get('program') or '', b['processor'], b['mode'], b['kind']) == ('', 'arm9', 'arm', 'function') for b in selected.values())
    return selected


def qualify():
    assert sha256(ROOT / REPORT) == REPORT_SHA and sha256(ROOT / READY) == READY_SHA
    assert sha256(ROOT / 'link_runtime_unit.py') == '3b4425e3711f116cafc3211a3abd8ad9288d81984c4029bce8e6f033070ddff0'
    registry = read_json(ROOT / 'recovery.json')
    assert subprocess.check_output(['git', 'show', 'HEAD:recovery.json'], cwd=ROOT) == (ROOT / 'recovery.json').read_bytes()
    assert subprocess.check_output(['git', 'show', 'HEAD:' + REPORT], cwd=ROOT) == (ROOT / REPORT).read_bytes()
    batch = next(b for b in registry['batches'] if b['report'] == REPORT)
    report = read_json(ROOT / REPORT)
    providers = contract(batch, report)
    cfg = configuration()
    seed = read_json(ROOT / 'provenance/seed-manifest.json')
    native = overlay.derive(cfg['rom'].read_bytes(), (ROOT / overlay.REFERENCE).read_bytes(), seed)
    baseline = {n: sha256(ROOT / n) for n in ['recovery.json', 'source-preferences.json', REPORT, READY]}
    rows = []
    for row in report['matches']:
        directory = ROOT / 'work/integration/cohort167-game-overlay-reference-v1' / row['address']
        adjusted = copy.deepcopy(row)
        index = adjusted['compilerFlags'].index('-lang')
        adjusted['compilerFlags'] = adjusted['compilerFlags'][:index] + adjusted['compilerFlags'][index + 2:]
        fresh = qualify_c99(adjusted, directory / 'compile')
        linked_entry = {**report, **row, 'object': fresh['explicitC99Object'],
                        'objectSha256': fresh['explicitC99ObjectSha256']}
        linked = linker.validate(linked_entry, row['nativeSymbolEntries'], directory / 'link')
        rows.append(dict(address=row['address'], bytes=row['bytes'], sourceOnlyCompilerInput=compiler_inputs(row),
            freshC99=fresh, freshGenuineNativeLink=linked))
    for name, binding in providers.items():
        linker.verify_binding(name, binding)
    negatives = []
    mutations = []
    m = copy.deepcopy(batch); m['report'] = 'evidence/matches/unapproved.json'; mutations.append(('wrong-consumer', m, report))
    m = copy.deepcopy(batch); m['sourceHashes'][overlay.REFERENCE] = '0' * 64; mutations.append(('wrong-image-hash', m, report))
    m = copy.deepcopy(batch); m['sourceHashes']['extract/arm9_overlays/ov001.bin'] = '0' * 64; mutations.append(('extra-image', m, report))
    m = copy.deepcopy(report); m['allPassed'] = False; mutations.append(('failed-report', batch, m))
    m = copy.deepcopy(report); m['romSha256'] = '0' * 64; mutations.append(('wrong-rom', batch, m))
    m = copy.deepcopy(report); m['matches'].pop(); mutations.append(('missing-caller', batch, m))
    for key, value in [('processor', 'arm7'), ('module', 'ov000'), ('mode', 'thumb'), ('program', 'child')]:
        m = copy.deepcopy(report); m['matches'][0][key] = value; mutations.append(('wrong-' + key, batch, m))
    m = copy.deepcopy(report); m['matches'][0]['compilerFlags'] = FLAGS + ['-include', 'unapproved.h']; mutations.append(('hidden-compiler-input', batch, m))
    m = copy.deepcopy(report); next(b for b in m['nativeSymbolBindings'].values() if b['module'] == 'ov000')['mode'] = 'thumb'; mutations.append(('wrong-overlay-provider-mode', batch, m))
    for label, candidate, document in mutations:
        try:
            contract(candidate, document)
        except (AssertionError, KeyError):
            negatives.append(label)
        else:
            raise AssertionError(label)
    assert all(sha256(ROOT / n) == h for n, h in baseline.items())
    proof = dict(passed=True, sourceCredit=0, report=REPORT, reportSha256=REPORT_SHA,
        ready=dict(path=READY, sha256=READY_SHA), functions=4, bytes=552,
        freshlyDerivedOriginalOverlay=native, originalOverlayProviders=providers, proofs=rows,
        rejectedControls=negatives, actualRegistrySourcesObjectsFlagsAndReportsUnchanged=True,
        noNativeImageIsACompilerOrLinkerInput=True, overlayProviderBodiesOrStorageCredit=0,
        generatorSha256=sha256(__file__))
    write_json(ROOT / PROOF, proof)
    return proof


@contextmanager
def route():
    proof = qualify()
    original = overlay.project_batches

    def projected(actual, report, declared):
        assert sum(b['report'] == REPORT for b in actual) == 1
        copies = copy.deepcopy(actual)
        selected = next(b for b in copies if b['report'] == REPORT)
        contract(selected, read_json(ROOT / REPORT))
        del selected['sourceHashes'][overlay.REFERENCE]
        return original(copies, report, declared)

    with patch.object(overlay, 'project_batches', projected):
        yield proof


if __name__ == '__main__':
    result = qualify()
    print(dict(passed=True, callers=4, bytes=552, negatives=len(result['rejectedControls']), sourceCredit=0))
