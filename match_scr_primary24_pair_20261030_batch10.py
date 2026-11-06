import hashlib
import json
import math
import shutil
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/scripts/20261030/batch10'
WORK = ROOT / 'work/script-source/20261030/batch10/primary24-pair'
OUTPUT = ROOT / 'evidence/matches/scripts-20261030-primary24-pair.json'
PINS = {'scr_c_compiler_20261029.py': '8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935',
 'scr_c_compiler_20261029_v4.py': '171818c7eda16c5d44e098a45ec425b268730a38e5f5696b73e19ce5e06b9de7',
 'scr_c_compiler_20261030_v6.py': 'ea44995cc5d9e13810a3d8f896b830a75b2cd42665a56b26d8289ef39df781a5',
 'scr_c_compiler_20261030_v8.py': '27e11c384c9a41979f464e0a953fee1974d5ecd4deec7b8286d369e43b08f49e',
 'nonmatching/script-source/20261029/native_scr_flags_20261029.py': 'd876d7d61fa35f379c1ead45a474f7a5f13e498a33f81421860fa38af684395d',
 'nonmatching/script-source/20261030/native_scr_primary24_pair_20261030.py': '7ab2d04c9f4262a4efe5fe389a9af40bdea3d2b935c392d4f34828ac7c35a8d9',
 'evidence/encounter/script_assets_20261029.py': '2467bfc207e2fb58d0b1b1299847b9a1667abe13c2081a4ab6342386dc7665ed',
 'evidence/encounter/vm_state_20261029.py': '13147bbe716ffe893d38440c3eb271f015648cda8aeb1c10ee0fd66afc9e63b5',
 'src/scripts/20261030/batch10/clear_primary_24_from_argument.bindings.json': '14fddc4feff309a0ca87b031003343f02c2d86660b53efbd1a959600e0800fc5',
 'src/scripts/20261030/batch10/clear_primary_24_from_argument.c': 'f188503e2292849692fdbdeffccc4994d372c168b828af13058971353ee4163e',
 'src/scripts/20261030/batch10/enable_primary_24_from_argument.bindings.json': 'cc576d300684b868ac1ec97d581701f0d4db0f23012581b631a77fd200906a6a',
 'src/scripts/20261030/batch10/enable_primary_24_from_argument.c': '6bdbc993c6a04beaa03d4547c1bc8b811b81e277a5a80fc425681632bb2a79cf',
 'src/scripts/20261030/batch10/scr_formal_decision.h': '9b48278519e63f280d410ab19cbede50b69855c962b6dc003afd1f5de05d8193'}
for path, expected in PINS.items():
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
assert sys.version_info[:3] == (3, 13, 5)
sys.path.insert(0, str(ROOT / 'evidence/encounter'))
sys.path.insert(0, str(ROOT / 'nonmatching/script-source/20261029'))
sys.path.insert(0, str(ROOT / 'nonmatching/script-source/20261030'))
import script_assets_20261029 as assets
import native_scr_primary24_pair_20261030 as fixtures
import scr_c_compiler_20261030_v8 as compiler
import unicorn


def digest(data):
    return hashlib.sha256(data).hexdigest()


def artifact(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path.read_bytes()), 'bytes': path.stat().st_size}


def operands(row):
    op, x = row['opcode'], row['argumentsRaw']
    if op == 1045:
        return [(x[1], x[2], 'write'), (x[3], x[4], 'read')]
    if 1039 <= op <= 1044:
        return [(x[1], x[2], 'read'), (x[3], x[4], 'read')]
    if 1046 <= op <= 1053:
        return [(x[i], x[i + 1], 'write' if i == 1 else 'read') for i in (1, 3, 5)]
    return [(x[1], x[2], 'read')] if op == 1035 else []


def boundary(data, unit, profile):
    start, end = unit['base'], unit['end']
    own = {r['pc']: r for r in data['instructions'] if start <= r['pc'] < end}
    assert [i for i, p in data['entries'].items() if p == start] == [102]
    assert not any(start < p < end for p in data['entries'].values())
    assert sum(r['bytes'] for r in own.values()) == end - start and own[end - 4]['opcode'] == 1026
    assert sum(r['opcode'] == 1026 for r in own.values()) == 1
    references, incoming = {name: [] for name in profile['locals']}, []
    slots = {slot: name for name, slot in profile['locals'].items()}
    reads, writes = {pc: set() for pc in own}, {pc: set() for pc in own}
    for row in data['instructions']:
        pc, op, args = row['pc'], row['opcode'], row['argumentsRaw']
        if op in (1033, 1034, 1036, 1037, 1038) and start <= args[1] < end:
            incoming.append({'sourcePc': pc, 'targetPc': args[1], 'opcode': op})
            assert not (start < args[1] < end and pc not in own)
        for mode, raw, access in operands(row):
            if mode != 0:
                continue
            value = struct.unpack('<f', struct.pack('<I', raw))[0]
            assert math.isfinite(value) and value == int(value) and 0 <= value < 256
            slot = int(value)
            if slot in slots:
                assert pc in own
                references[slots[slot]].append({'pc': pc, 'access': access})
            if pc in own:
                assert slot in slots
                (reads if access == 'read' else writes)[pc].add(slot)
    successors = {}
    for pc, row in own.items():
        op, x = row['opcode'], row['argumentsRaw']
        successors[pc] = [] if op == 1026 else [x[1]] if op == 1036 else [pc + row['bytes'], x[1]] if op == 1038 else [pc + row['bytes']]
        assert all(target in own and target > pc for target in successors[pc])
    predecessors = {pc: set() for pc in own}
    for pc, targets in successors.items():
        for target in targets:
            predecessors[target].add(pc)
    before, after = {}, {}
    for pc in sorted(own):
        before[pc] = set.intersection(*(after[p] for p in predecessors[pc])) if predecessors[pc] else set()
        assert reads[pc] <= before[pc]
        after[pc] = before[pc] | writes[pc]
    dominance = [{'pc': pc, 'readSlots': sorted(reads[pc]), 'definitelyAssignedBeforeRead': sorted(before[pc])}
                 for pc in sorted(own) if reads[pc]]
    assert own[start + 12]['argumentsRaw'][1:] == [0, compiler.prior.fword(unit['formal']), 1, 0]
    return {'entry': 102, 'startPc': start, 'endExclusivePc': end, 'bytes': end - start, 'privateReturnPc': end - 4,
        'knownIncomingReferences': incoming, 'knownSlotReferences': references, 'knownOutsideSlotReferences': 0,
        'allKnownMode0IndicesCanonical': True, 'readDominance': dominance,
        'allOwnReadsDominatedByAssignments': True, 'uninitializedDeclarationDoesNotDefineAValue': True,
        'externalInteriorEntries': 0, 'sharedReturnTailDetected': False,
        'opaqueNativeOrComputedSlotReferenceCoverageComplete': False, 'serializedCompleteCallsOnly': True}


def build(data, kind, name):
    unit, directory = fixtures.UNITS[kind], WORK / kind / 'source-only'
    directory.mkdir(parents=True, exist_ok=True)
    files = [(n, n) for n in ('scr_c_compiler_20261029.py', 'scr_c_compiler_20261029_v4.py', 'scr_c_compiler_20261030_v6.py', 'scr_c_compiler_20261030_v8.py')]
    files += [('src/scripts/20261030/batch10/' + n, n) for n in (name + '.c', 'scr_formal_decision.h', name + '.bindings.json')]
    for source, target in files:
        shutil.copyfile(ROOT / source, directory / target)
    command = [sys.executable, 'scr_c_compiler_20261030_v8.py', '--source', name + '.c', '--base', hex(unit['base']),
        '--bindings', name + '.bindings.json', '--output', 'generated.scrfunc', '--report', 'build.json']
    result = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=30, check=True)
    body = (directory / 'generated.scrfunc').read_bytes()
    assert body == data['code'][unit['base']:unit['end']]
    rebuilt = data['script'][:4100 + unit['base']] + body + data['script'][4100 + unit['end']:]
    assert rebuilt == data['script']
    output = WORK / kind / 'rebuilt.scr'
    output.write_bytes(rebuilt)
    return rebuilt, {'command': command, 'cwd': str(directory), 'exitCode': result.returncode, 'stdout': result.stdout.strip(),
        'inputs': [artifact(directory / target) for unused, target in files], 'emittedBody': artifact(directory / 'generated.scrfunc'),
        'compilerReport': artifact(directory / 'build.json'), 'compilerEvidence': json.loads((directory / 'build.json').read_text()),
        'rebuiltImage': artifact(output), 'originalBytecodeCompilerInput': False}


def controls(kind, name, profile):
    directory = ROOT / 'nonmatching/script-source/20261030/batch10-controls' / kind
    directory.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE / 'scr_formal_decision.h', directory / 'scr_formal_decision.h')
    text = (SOURCE / (name + '.c')).read_text()
    alias = json.loads(json.dumps(profile))
    alias['locals']['state'] = alias['locals']['request']
    tests = [('alias', text, alias), ('missing_formal', text, {'locals': {'state': profile['locals']['state']}, 'globals': {}}),
        ('formal_bool', text.replace('float request)', 'bool request)'), profile),
        ('bad_numeric_index', text.replace('get_numeric_state(3)', 'get_numeric_state(88)'), profile),
        ('bad_primary_index', text.replace('set_primary_flag(24', 'set_primary_flag(1536'), profile),
        ('shadow_formal', text.replace('{\n', '{\n    float request;\n', 1), profile),
        ('getter_type', text.replace('float state', 'bool state'), profile)]
    if kind == 'clear':
        tests += [('uninitialized_read', text.replace('state = get_numeric_state(0);', ''), profile),
            ('branch_definition_escapes', text.replace('    float state;\n', '    float state;\n    if (state == 2) { set_primary_flag(24, false); }\n'), profile),
            ('conditional_assignment_not_global_dominance', text.replace('    float state;\n',
                '    float state;\n    if (request == 8) { state = get_numeric_state(0); }\n    if (state == 2) { set_primary_flag(24, false); }\n'), profile)]
    rejected = []
    for label, source, bindings in tests:
        path = directory / (label + '.c')
        path.write_text(source)
        try:
            compiler.compile_source(path, fixtures.UNITS[kind]['base'], bindings)
        except ValueError as error:
            rejected.append({'name': label, 'source': artifact(path), 'bindings': bindings, 'error': str(error), 'rejectedBeforeOutput': True})
        else:
            raise AssertionError('Invalid formal-decision source accepted: ' + label)
    return {'rejectedSourceProfiles': rejected, 'sourceCredit': 0}


def main():
    assert unicorn.__version__ == '2.1.4'
    for image, sha in ((fixtures.native.MAIN, fixtures.native.MAIN_HASH), (fixtures.native.OVERLAY, fixtures.native.OVERLAY_HASH),
                       (fixtures.native.ITCM, fixtures.native.ITCM_HASH)):
        assert digest(image) == sha
    WORK.mkdir(parents=True, exist_ok=True)
    units = []
    rom, files = assets.original_files()
    for kind, name in (('enable', 'enable_primary_24_from_argument'), ('clear', 'clear_primary_24_from_argument')):
        unit = fixtures.UNITS[kind]
        data = assets.load(ROOT / 'extract/files' / unit['asset'])
        profile = json.loads((SOURCE / (name + '.bindings.json')).read_text())
        boundaries = boundary(data, unit, profile)
        rebuilt, source_build = build(data, kind, name)
        negative = controls(kind, name, profile)
        original, recompiled = fixtures.run(data['script'], kind), fixtures.run(rebuilt, kind)
        assert original == recompiled
        own = {r['pc'] for r in data['instructions'] if unit['base'] <= r['pc'] < unit['end']}
        executed = {s['pc'] for c in original['cases'] for key in ('first', 'second') for s in c[key]['trace']}
        assert own == executed
        units.append({'kind': kind, 'asset': data['asset'], 'archiveSha256': data['assetSha256'], 'scriptSha256': data['scriptSha256'],
            'codeSha256': digest(data['code']), 'romFileRange': list(files[unit['asset']]), 'boundariesAndStorage': boundaries,
            'matchedRange': {'startPc': unit['base'], 'endExclusivePc': unit['end'], 'bytes': unit['end'] - unit['base'],
                             'sha256': digest(data['code'][unit['base']:unit['end']])},
            'source': 'src/scripts/20261030/batch10/' + name + '.c', 'sourceOnlyBuild': source_build,
            'compilerControls': negative, 'differential': original, 'allOwnRecordsExecuted': True,
            'executedOwnRecordPcs': sorted(executed), 'sourceDefinitionCount': 1, 'completeFunctionInstances': 1,
            'pairedNativeReturningCalls': original['actualReturningCalls'] * 2,
            'pairedCompleteOwnEntryExecutions': original['freshMachines'] * 4,
            'prefixNativeReturningCalls': original['prefixActualReturningCalls'] * 2,
            'prefixOuterEntryReturnCredit': 0, 'prefixAdditionalSourceCredit': 0,
            'originalScaffoldingBytes': len(rebuilt) - (unit['end'] - unit['base']), 'scaffoldingSourceCredit': 0})
    report = {'schemaVersion': 1, 'generator': Path(__file__).relative_to(ROOT).as_posix(), 'generatorSha256': digest(Path(__file__).read_bytes()),
        'evidenceClass': 'ordinary-C-complete-formal-primary24-set-clear-SCR-source-match', 'romSha256': assets.ROM_HASH,
        'sourceClosure': [{'path': n, 'sha256': s} for n, s in PINS.items()], 'reproductionCommand': 'python match_scr_primary24_pair_20261030_batch10.py',
        'units': units, 'sourceDefinitionCount': 2, 'completeFunctionInstances': 2, 'qualifiedScriptRangeBytes': 1016,
        'pairedNativeReturningCalls': sum(u['pairedNativeReturningCalls'] for u in units),
        'pairedCompleteOwnEntryExecutions': sum(u['pairedCompleteOwnEntryExecutions'] for u in units),
        'pairedPrefixNativeReturningCalls': sum(u['prefixNativeReturningCalls'] for u in units),
        'nativeExecutableByteCredit': 0, 'completeImagesRecovered': 0, 'nativeFunctionStubs': 0, 'postFaultStateUsedForProof': False,
        'allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared': True, 'wholeRomSourceMatch': False,
        'limitations': ['Only two complete functions totaling1016B; all remaining native/script/assets are zero-credit scaffolding',
            'Formal inputs come from argument0, not direct context0; source caller-prefix proof is separately synthetic and excludes outer termination',
            'Source uninitialized declarations emit no stores; every source read is independently dominated by an actual assignment',
            'No known encoded outside slot reference exists; opaque/native/computed references remain unresolved',
            'Raw primary24 predicates/set/clear operations have no assigned story, area, access or encounter-renewal meaning']}
    OUTPUT.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'report': str(OUTPUT), 'bytes': 1016, 'completeOwnEntryExecutions': report['pairedCompleteOwnEntryExecutions'],
                      'nativeReturns': report['pairedNativeReturningCalls'], 'prefixNativeReturns': report['pairedPrefixNativeReturningCalls']}))


if __name__ == '__main__':
    main()
