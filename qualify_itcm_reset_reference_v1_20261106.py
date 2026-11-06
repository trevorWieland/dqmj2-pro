import copy
import hashlib
import subprocess
from project import ROOT, configuration, native_dependencies, read_json, write_json, sha256
from closed_c_compiler_inputs_20261105 import compiler_inputs
from qualify_explicit_c_frontend_20261102 import qualify as fresh_c99
from qualify_arm9_overlay_reference_inputs_20261105 import arm_mapping
from qualify_arm9_thumb_reference_inputs_20261105 import derive as derive_main, IMAGE, IMAGE_SHA
import link_runtime_unit as linker

REPORT = 'evidence/matches/cohort168-parallel-wave20261105-m-itcm-reset-first-0.json'
READY = 'evidence/lanes/parallel-wave20261105/itcm-reset-next/ready.json'
READY_SHA = '05af2b4591202fd99bc301cc980d1b5b027b3d4a842fb86c8dfc47edfa059bb9'
INPUTS = 'evidence/lanes/parallel-wave20261105/itcm-reset-next/package-inputs-v3.json'
INPUTS_SHA = 'dc1bc3f336b9e0f2a38b2193bc78239a6dce97b51167d8052ef0b399ef83ff0f'
ITCM = 'extract/arm9/itcm.bin'
OUTPUT = 'evidence/verification/cohort168-itcm-reset-reference-v1-qualification-20261106.json'
FLAGS = ['-O4,p', '-enum', 'int', '-char', 'signed', '-str', 'noreuse', '-proc', 'arm946e',
         '-gccext,on', '-fp', 'soft', '-inline', 'on,noauto', '-Cpp_exceptions', 'off', '-RTTI', 'off',
         '-interworking', '-w', 'off', '-sym', 'on', '-gccinc', '-nolink', '-msgstyle', 'gcc',
         '-ipa', 'file', '-lang', 'c99']


def contract(report):
    ready = read_json(ROOT / READY)
    assert sha256(ROOT / READY) == READY_SHA and sha256(ROOT / INPUTS) == INPUTS_SHA
    assert report['allPassed'] and report['romSha256'] == configuration()['romSha256']
    assert len(report['matches']) == 1 and report['module'] == 'itcm'
    row = report['matches'][0]
    for key in ['program', 'processor', 'module', 'mode', 'address', 'bytes', 'source', 'sourceSha256', 'targetSha256']:
        assert row[key] == ready['identities'][0][key]
    assert row['compilerFlags'] == FLAGS and row['compiler'] == 'tools/mwccarm/mwccarm/2.0/sp1p6/mwccarm.exe'
    assert row['ordinaryCBytes'] == 168 and row['justifiedAssemblyBytes'] == 0
    assert row['realLink']['exactCallerBytes'] and row['exactAfterDeclaredRelocation']
    assert row['outputSha256'] == row['targetSha256'] == row['realLink']['linkedCallerSha256']
    assert report['packageInputManifest'] == INPUTS and report['packageInputManifestSha256'] == INPUTS_SHA
    assert report['nativeCalleeBodiesExecuted'] == report['actualNativeAndSourceCallerReturns'] == 0
    assert report['actualNativeAndSourcePartialStops'] == 64
    inputs = {p['path']: p['sha256'] for p in read_json(ROOT / INPUTS)['files']}
    for item in [dict(path=row['source'], sha256=row['sourceSha256']), *row['sourceDependencies']]:
        assert inputs[item['path']] == item['sha256'] == sha256(ROOT / item['path'])
    compiler_inputs(row)
    return row


def qualify():
    snapshot = {n: sha256(ROOT / n) for n in ['recovery.json', 'source-preferences.json', REPORT, READY, INPUTS]}
    report = read_json(ROOT / REPORT)
    row = contract(report)
    cfg = configuration(); native_dependencies(cfg)
    assert sha256(cfg['rom']) == cfg['romSha256'] == '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'
    import ndspy.rom
    import ndspy.code
    nds = ndspy.rom.NintendoDSRom(cfg['rom'].read_bytes())
    sections = ndspy.code.MainCodeFile(nds.arm9, nds.arm9RamAddress)
    selected = [s for s in sections.sections if s.ramAddress == 0x01ff8000]
    assert len(selected) == 1 and len(selected[0].data) == 30880 and not selected[0].implicit
    data = bytes(selected[0].data)
    assert (ROOT / ITCM).read_bytes() == data
    assert derive_main() == (ROOT / IMAGE).read_bytes() and sha256(ROOT / IMAGE) == IMAGE_SHA
    start = int(row['address'], 0) - 0x01ff8000
    assert hashlib.sha256(data[start:start + 168]).hexdigest() == row['targetSha256']
    native_refs = {p['path']: p['sha256'] for p in read_json(ROOT / INPUTS)['files'] if p['path'].startswith('extract/')}
    assert native_refs == {IMAGE: IMAGE_SHA, ITCM: hashlib.sha256(data).hexdigest()}
    mode = arm_mapping(ROOT / row['object'], row['name'])
    assert mode['functionBytes'] == 168 and mode['mode'] == 'arm'
    adjusted = copy.deepcopy(row); i = adjusted['compilerFlags'].index('-lang')
    adjusted['compilerFlags'] = adjusted['compilerFlags'][:i] + adjusted['compilerFlags'][i + 2:]
    folder = ROOT / 'work/integration/cohort168-itcm-reference-v1'
    fresh = fresh_c99(adjusted, folder / 'compile')
    assert arm_mapping(ROOT / fresh['explicitC99Object'], row['name']) == mode
    entry = {**report, **row, 'object': fresh['explicitC99Object'], 'objectSha256': fresh['explicitC99ObjectSha256']}
    linked = linker.validate(entry, row['nativeSymbolEntries'], folder / 'link')
    rejected = []
    mutations = []
    for key, value in [('processor', 'arm7'), ('module', 'main'), ('program', 'child'), ('mode', 'thumb'), ('bytes', 164), ('targetSha256', '0' * 64)]:
        m = copy.deepcopy(report); m['matches'][0][key] = value; mutations.append(('wrong-' + key, m))
    m = copy.deepcopy(report); m['allPassed'] = False; mutations.append(('failed-report', m))
    m = copy.deepcopy(report); m['matches'][0]['compilerFlags'] = FLAGS + ['-include', 'hidden.h']; mutations.append(('hidden-compiler-input', m))
    m = copy.deepcopy(report); m['matches'][0]['compiler'] = 'unapproved.exe'; mutations.append(('wrong-compiler-profile', m))
    m = copy.deepcopy(report); m['nativeCalleeBodiesExecuted'] = 1; mutations.append(('provider-execution-credit', m))
    for label, candidate in mutations:
        try:
            contract(candidate)
        except (AssertionError, KeyError):
            rejected.append(label)
        else:
            raise AssertionError(label)
    assert all(sha256(ROOT / n) == h for n, h in snapshot.items())
    proof = dict(passed=True, sourceCredit=0, report=REPORT, reportSha256=snapshot[REPORT], ready=READY,
        readySha256=READY_SHA, inputManifest=INPUTS, inputManifestSha256=INPUTS_SHA,
        functions=1, bytes=168, namespace=dict(program='', processor='arm9', module='itcm', mode='arm'),
        originalDerivedNativeInputs=native_refs, originalItcmLoadAddress='0x1ff8000', originalItcmBytes=len(data),
        sourceOnlyCompilerInput=compiler_inputs(row), actualCompilerMode=mode,
        freshExplicitC99=fresh, freshGenuineNativeLink=linked, rejectedControls=rejected,
        nativeProviderBodyInstructionsExecuted=0, actualCompleteReturns=0, actualPartialStops=64,
        actualRegistrySourcesHeadersObjectsFlagsAndReportsUnchanged=True, generatorSha256=sha256(__file__))
    write_json(ROOT / OUTPUT, proof)
    return proof


if __name__ == '__main__':
    proof = qualify()
    print(dict(passed=True, functions=1, bytes=168, rejectedControls=len(proof['rejectedControls']), sourceCredit=0))
