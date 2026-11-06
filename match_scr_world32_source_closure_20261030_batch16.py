import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/script-source/20261030/batch16/world32-source-closure'
OUTPUT = ROOT / 'evidence/matches/scripts-20261030-world32-source-closure.json'
PINS = {'nonmatching/script-source/20261030/native_scr_world32_20261030.py': 'f219a4d3d54cecf482d2eaf47949033b4746b1f3b73a1afd6bd5cd92f2201b5e',
 'nonmatching/script-source/20261029/native_scr_flags_20261029.py': 'd876d7d61fa35f379c1ead45a474f7a5f13e498a33f81421860fa38af684395d',
 'evidence/encounter/script_assets_20261029.py': '2467bfc207e2fb58d0b1b1299847b9a1667abe13c2081a4ab6342386dc7665ed',
 'evidence/encounter/vm_state_20261029.py': '13147bbe716ffe893d38440c3eb271f015648cda8aeb1c10ee0fd66afc9e63b5',
 'scr_c_compiler_20261029.py': '8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935',
 'scr_c_compiler_20261029_v4.py': '171818c7eda16c5d44e098a45ec425b268730a38e5f5696b73e19ce5e06b9de7',
 'scr_c_compiler_20261030_v6.py': 'ea44995cc5d9e13810a3d8f896b830a75b2cd42665a56b26d8289ef39df781a5',
 'scr_c_compiler_20261030_v7.py': '20b9bfed558c5d4bbd2962e4f58841db473e44723c2653498139c31621edbf26',
 'scr_c_compiler_20261030_v9.py': '705c467d7edafcf9806b95f7736629895b5acc0b4b941aa462fc0a13b0bc53ba',
 'scr_c_compiler_20261030_v10.py': '80257ee6d3a118f3897ad406fde8983cc317e132cf7bd357761c44ff76253a08',
 'scr_c_compiler_20261030_v11.py': 'c30f671b25323f474b5aebd9a0b6fcd8a02055a5914ab850a51d430291d59af3',
 'scr_c_compiler_20261030_v12.py': '0452b7c010993dea523cf92fda01d72fc83a7a0aea318f33886fdc836c0bb271',
 'scr_c_compiler_20261030_v13.py': '1939e65b0a7cc49ea6c563e622f73713b032e427261380c83cb2e422a3a527d0',
 'src/scripts/20261030/batch09/reset_world_flags.c': '8c39b5b0726c72eb28e1f19c6630b5fb9edb35d83a38f089aa846fdc9e613ded',
 'src/scripts/20261030/batch09/scr_reset_caller.h': 'cff18e5316e7f739e4f2bb5c4ee6f5e9130f39821c17709c922e02f2d0a354be',
 'src/scripts/20261030/batch09/reset.locals.json': 'd9134abf671bd2338ce17a02515a9b8bd45d89b02229ba5f118563158d281f5c',
 'src/scripts/20261030/batch09/reset.links.json': 'e585d88e8196043841ece245e500dede5537f4d6aa42cf699a1b7f3b2a022acb',
 'src/scripts/20261030/batch12/clear_primary_range_450_498.c': '9e7677d28489afd7fc5b8deabfcf369d02af45b3be85a16d5a44eca9604a562a',
 'src/scripts/20261030/batch12/scr_runtime_flags.h': 'b946aa46b02ff0df705daaaee84a65f9ab8ffe267371050f33e312aafceb8575',
 'src/scripts/20261030/batch12/range.locals.json': '644c8c99da056bdebb20217dafb0b0c5610d3890ecada6ba310afe949d5b8d07',
 'src/scripts/20261030/batch08/advance_world_state.c': 'a37916359e3cd70b6df1813b7dc1e597f910d6e90691ccca38f81f31d3476259',
 'src/scripts/20261030/batch08/scr_world_state.h': '1925a586fd944285694802df3d149355be853f4a81cadb17828550bf11658b2b',
 'src/scripts/20261030/batch08/world.bindings.json': 'ed204331ed62ff1d1ac7a927758f7108607701704463f277cd3e448d576169a5',
 'src/scripts/20261030/batch13/refresh_context_words.c': '2b262d8bdaef29c941711ef7ddb2fdcdab3ebd0bd1d98788f7b17f0d42c815aa',
 'src/scripts/20261030/batch13/scr_context_words.h': 'b3387270855d7fddb3bdbdbd717ee6014118eafa471de6e9d7a7bc75945f6b9f',
 'src/scripts/20261030/batch13/context.bindings.json': '1f9e88013763ccc7f1f28917457278f1320782e56ee05cf73083b6a094b0a3db',
 'src/scripts/20261030/batch15/initialize_context_byte_rows.c': 'fa82be162b2dc89624e8c8204a5ee704a754b5b6eb1a59e2da78cfa284686364',
 'src/scripts/20261030/batch15/scr_byte_rows.h': '1bcb2ca3b8a33fb54da33d969ae2382efa788f0dd324004fcaac4157715ebf29',
 'src/scripts/20261030/batch14/apply_primary_byte_modes.c': '14e7e5ec2ce98fc448163f869e65568a0eacf5e825aab2992344e7692f3578c9',
 'src/scripts/20261030/batch14/scr_byte_mode.h': '289cf01611ce83f1c668dbecf66b9235a2a92e4841d90f63b6ede80e1e612cbb',
 'src/scripts/20261030/batch14/modes.bindings.json': '8cc7865465d92a5334323c0862fc81c65ea6bb12d5565ee1b0a58f38759323d9',
 'src/scripts/20261029/batch02/before_primary_flag_reset.c': 'c6e2d8d816a96553043687a44c00d98f3c9c3c7d98db68a290c4e8a590e86d6d',
 'src/scripts/20261029/batch02/scr_flags.h': '8f0e2b3942eb2760b8fff0031849b4738c5e16c96cfd27e2e4a269bbddc9f7fe',
 'src/scripts/20261030/batch11/select_numeric_thirty_one.c': '1a1ff545df5259a4ab11cb287840b3d10160c6e02e3afb18b9f4fc62f1cf9350',
 'src/scripts/20261030/batch11/scr_random_decision.h': '5eb96e7af41e95c4b584894d20aaf1f813925c1c101e3c1f1813b341c27abe39',
 'src/scripts/20261030/batch11/selection.bindings.json': '03d60ee3490ba935d3c750a7821469b06915576a1d60e24b393aaeccc3d1309d'}
sys.path[:0] = [str(ROOT / 'evidence/encounter'), str(ROOT / 'nonmatching/script-source/20261029'),
    str(ROOT / 'nonmatching/script-source/20261030')]
import script_assets_20261029 as assets
import native_scr_world32_20261030 as fixtures
import unicorn

UNITS = (
    ('world32', 60232, 63972, 'scr_c_compiler_20261030_v7.py', 'src/scripts/20261030/batch09',
        ('reset_world_flags.c', 'scr_reset_caller.h', 'reset.locals.json', 'reset.links.json'),
        ('--source', 'reset_world_flags.c', '--locals', 'reset.locals.json', '--links', 'source-linked.links.json')),
    ('world257', 1056, 1276, 'scr_c_compiler_20261030_v10.py', 'src/scripts/20261030/batch12',
        ('clear_primary_range_450_498.c', 'scr_runtime_flags.h', 'range.locals.json'),
        ('--source', 'clear_primary_range_450_498.c', '--locals', 'range.locals.json')),
    ('world34', 64268, 65620, 'scr_c_compiler_20261030_v6.py', 'src/scripts/20261030/batch08',
        ('advance_world_state.c', 'scr_world_state.h', 'world.bindings.json'),
        ('--source', 'advance_world_state.c', '--bindings', 'world.bindings.json')),
    ('world272', 43972, 45252, 'scr_c_compiler_20261030_v11.py', 'src/scripts/20261030/batch13',
        ('refresh_context_words.c', 'scr_context_words.h', 'context.bindings.json'),
        ('--source', 'refresh_context_words.c', '--bindings', 'context.bindings.json')),
    ('world11', 50684, 52236, 'scr_c_compiler_20261030_v13.py', 'src/scripts/20261030/batch15',
        ('initialize_context_byte_rows.c', 'scr_byte_rows.h'), ('--source', 'initialize_context_byte_rows.c')),
    ('world12', 52244, 53244, 'scr_c_compiler_20261030_v12.py', 'src/scripts/20261030/batch14',
        ('apply_primary_byte_modes.c', 'scr_byte_mode.h', 'modes.bindings.json'),
        ('--source', 'apply_primary_byte_modes.c', '--bindings', 'modes.bindings.json')),
    ('world20', 59052, 59068, 'scr_c_compiler_20261029.py', 'src/scripts/20261029/batch02',
        ('before_primary_flag_reset.c', 'scr_flags.h'), ('--source', 'before_primary_flag_reset.c')),
    ('world17', 59076, 60224, 'scr_c_compiler_20261030_v9.py', 'src/scripts/20261030/batch11',
        ('select_numeric_thirty_one.c', 'scr_random_decision.h', 'selection.bindings.json'),
        ('--source', 'select_numeric_thirty_one.c', '--bindings', 'selection.bindings.json')))
COMPILERS = ('scr_c_compiler_20261029.py', 'scr_c_compiler_20261029_v4.py', 'scr_c_compiler_20261030_v6.py',
    'scr_c_compiler_20261030_v7.py', 'scr_c_compiler_20261030_v9.py', 'scr_c_compiler_20261030_v10.py',
    'scr_c_compiler_20261030_v11.py', 'scr_c_compiler_20261030_v12.py', 'scr_c_compiler_20261030_v13.py')


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def artifact(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path.read_bytes()), 'bytes': path.stat().st_size}


def build(data):
    links = json.loads((ROOT / 'src/scripts/20261030/batch09/reset.links.json').read_text())
    previous = json.loads(json.dumps(links))
    for row in links.values():
        row['dependencyKind'] = 'source-linked'
    assert all({key: value for key, value in row.items() if key != 'dependencyKind'} ==
        {key: value for key, value in previous[name].items() if key != 'dependencyKind'} for name, row in links.items())
    rebuilt, products = bytearray(data['script']), []
    for name, start, end, compiler, source_root, names, arguments in UNITS:
        directory = WORK / name
        directory.mkdir(parents=True, exist_ok=True)
        inputs = []
        for filename in COMPILERS:
            shutil.copyfile(ROOT / filename, directory / filename)
            inputs.append(artifact(directory / filename))
        for filename in names:
            shutil.copyfile(ROOT / source_root / filename, directory / filename)
            inputs.append(artifact(directory / filename))
        derived = None
        if name == 'world32':
            target = directory / 'source-linked.links.json'
            target.write_text(json.dumps(links, indent=2) + '\n')
            derived = artifact(target)
            inputs.append(derived)
        command = [sys.executable, compiler, *arguments, '--base', hex(start), '--output', 'generated.scrfunc', '--report', 'build.json']
        result = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=30, check=True)
        body = (directory / 'generated.scrfunc').read_bytes()
        compiled = json.loads((directory / 'build.json').read_text())
        assert len(body) == end - start and body == data['code'][start:end]
        rebuilt[4100 + start:4100 + end] = body
        products.append({'name': name, 'startPc': start, 'endExclusivePc': end, 'bytes': len(body), 'sha256': digest(body),
            'command': command, 'cwd': str(directory), 'exitCode': result.returncode, 'inputs': inputs,
            'emittedBody': artifact(directory / 'generated.scrfunc'), 'compilerReport': artifact(directory / 'build.json'),
            'compilerEvidence': compiled, 'derivedLinkProfile': derived, 'originalBytecodeCompilerInput': False,
            'newSourceRangeCredit': 0, 'newSourceDefinitionCredit': 0})
    assert bytes(rebuilt) == data['script'] and sum(row['bytes'] for row in products) == 10308
    ranges = {(row['startPc'], row['endExclusivePc']) for row in products if row['name'] != 'world32'}
    assert ranges == {(row['entryPc'], row['endExclusivePc']) for row in links.values()} and len(ranges) == 7
    source_caller = products[0]['compilerEvidence']
    assert source_caller['qualifiedLinks'] == links
    target = WORK / 'world.source-linked-eight-ranges.scr'
    target.write_bytes(rebuilt)
    return bytes(rebuilt), products, {'allSevenDirectLinksSourceLinked': True, 'originalLinkProfile': previous,
        'derivedSourceLinkProfile': links, 'addressesTypesHashesUnchanged': True, 'calleeProductBytes': sum(end - start for start, end in ranges),
        'callerBytes': 3740, 'physicalReusedSourceRangeBytes': 10308, 'originalScrCalleeBodiesUsedForSevenLinks': 0,
        'knownDirectScrCallTreeOnly': True, 'opaqueNativeOrComputedGlobalClosureProven': False, 'rebuiltImage': artifact(target)}


def main():
    assert sys.version_info[:3] == (3, 13, 5) and unicorn.__version__ == '2.1.4'
    for name, pin in PINS.items():
        assert digest((ROOT / name).read_bytes()) == pin, name
    data = assets.load(ROOT / 'extract/files/world.e')
    rebuilt, products, linking = build(data)
    print(json.dumps({'stage': 'eight source ranges compiled', 'bytes': 10308, 'newSourceCredit': 0}), flush=True)
    original, recompiled = fixtures.run(data['script']), fixtures.run(rebuilt)
    assert original == recompiled
    assert all(part['entry32Returned'] and len(part['directScriptCalls']) == 7 and part['threeCallerLocalsPreservedByCallees']
        for case in original['cases'] for part in (case['first'], case['second']))
    report = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'evidenceClass': 'existing-ordinary-C-eight-range-direct-SCR-source-link-closure-proof', 'romSha256': assets.ROM_HASH,
        'sourceClosure': [{'path': name, 'sha256': pin} for name, pin in PINS.items()],
        'scriptSha256': data['scriptSha256'], 'codeSha256': digest(data['code']), 'products': products, 'sourceLinking': linking,
        'differential': original, 'pairedCompleteRootEntryExecutions': len(original['cases']) * 4,
        'pairedNativeReturningCalls': original['actualReturningCalls'] * 2, 'newSourceRangeCredit': 0, 'newSourceByteCredit': 0,
        'newSourceDefinitionCredit': 0, 'nativeSourceCredit': 0, 'completeImageCredit': 0, 'wholeRomSourceMatch': False,
        'limitations': ['Reuses eight separately proved source ranges; no new source credit', 'Only root32 known direct SCR call tree qualifies',
            'Individual callee proofs retain their own stronger branch/domain limits; this integration run does not broaden them',
            'Native VM/API bodies and all remaining original script/assets remain scaffolding for this proof',
            'No natural scene, opaque/native/computed global closure or whole-image/ROM source claim']}
    OUTPUT.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'report': str(OUTPUT), 'completeRootEntries': report['pairedCompleteRootEntryExecutions'],
        'nativeReturns': report['pairedNativeReturningCalls'], 'reusedSourceBytes': 10308, 'newSourceCredit': 0}), flush=True)


if __name__ == '__main__':
    main()
