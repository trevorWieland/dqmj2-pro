import hashlib
import json
import shutil
import struct
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/scripts/20261029/batch06'
WORK = ROOT / 'work/script-source/20261029/batch06/captures'
OUTPUT = ROOT / 'evidence/matches/scripts-20261029-captures.json'
PINS = {'scr_c_compiler_20261029.py': '8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935',
 'scr_c_compiler_20261029_v4.py': '171818c7eda16c5d44e098a45ec425b268730a38e5f5696b73e19ce5e06b9de7',
 'build_scr_captures_20261029_batch06.py': 'e395d329a5555b0615b0d46a3d97a98b3811bdcc83b806e3753851f6d020c9b7',
 'audit_scr_captures_20261029_batch06.py': 'fc80779acc1f97ae8cdae500be2030ea0eea4b78f9d0d1b6b2b97014ce454612',
 'src/scripts/20261029/batch06/scr_numeric.h': 'dd9083a3b944895fa04c96a6dc41900e7d9d1923842f1f420ea253ff854a3bcf',
 'nonmatching/script-source/20261029/native_scr_flags_20261029.py': 'd876d7d61fa35f379c1ead45a474f7a5f13e498a33f81421860fa38af684395d',
 'nonmatching/script-source/20261029/native_scr_captures_20261029.py': '46c2cb5ab59d6fc4a39a500420acd8fef8ae0c60007fcb809406c2241d9fa1eb',
 'evidence/encounter/script_assets_20261029.py': '2467bfc207e2fb58d0b1b1299847b9a1667abe13c2081a4ab6342386dc7665ed',
 'evidence/encounter/vm_state_20261029.py': '13147bbe716ffe893d38440c3eb271f015648cda8aeb1c10ee0fd66afc9e63b5',
 'src/scripts/20261029/batch06/capture_context_0.c': '727c04a3d21ef01656514deac1decb5c573b54176fbbce549f7905b0ac9e02df',
 'src/scripts/20261029/batch06/capture_context_0_and_context_1.c': '6dedcd4bcd096fe73b8b5255cc048c904be04572f4a03b7e9507c03d3c83cdd8',
 'src/scripts/20261029/batch06/capture_context_0_and_numeric_0_and_numeric_20.c': 'bdb4977ce51c9ffd8c58da0ecc2022239f883bfc37718e2ab2ec2f46e82563fe',
 'src/scripts/20261029/batch06/capture_numeric_0.c': '2e0797259169a3237f51182e762905954e22883d6d502e7c7a5a1652d8cc3c55',
 'src/scripts/20261029/batch06/capture_numeric_0_and_numeric_10.c': '3b034a1a8534a6b67ba0f0cc127054188d70ae1918777bd90c94b691b65b2a29',
 'src/scripts/20261029/batch06/capture_numeric_0_and_numeric_20.c': '74a29dc4eacc66968c7e77eb3e8040834d8eabb361347522389ecb331fd8ca2e',
 'src/scripts/20261029/batch06/capture_numeric_0_and_numeric_3.c': '116584ec0e1002d8069b3ca8af4c6356d82959a9c150ff88196c64aef1051e8f',
 'src/scripts/20261029/batch06/capture_numeric_0_and_numeric_3_and_numeric_4.c': 'f6ab0d7c409fa9fc10fe5981955db9cfc4ffe51b258ab77612385e3a31844a85',
 'src/scripts/20261029/batch06/capture_numeric_0_and_numeric_5.c': '45b061c866958005491c74671d1eea413fa473c20de33e2ef329ed52c8e0106f',
 'src/scripts/20261029/batch06/capture_numeric_0_and_numeric_9.c': 'c2bc51a962c10ce63b7dbf3ca65d1220a7507b578cfcffe9481eb30a700bb6b9',
 'evidence/encounter/scr-capture-source-layout-20261029.json': '73578cd3a74da3fa59b513b030ca4beea649e47a013198fd1d31737d8a378e0a',
 'evidence/encounter/scr-v4-candidates-20261029-batch06.json': '769b197a673fe8e067c79299b31d53f88873ed333fd1d651f53eab1221a3b9bf'}
for path, expected in PINS.items():
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
assert sys.version_info[:3] == (3, 13, 5)
sys.path.insert(0, str(ROOT / 'evidence/encounter'))
sys.path.insert(0, str(ROOT / 'nonmatching/script-source/20261029'))
import script_assets_20261029 as assets
import native_scr_captures_20261029 as fixtures
import audit_scr_captures_20261029_batch06 as auditor
import scr_c_compiler_20261029_v4 as compiler
import unicorn


def digest(data):
    return hashlib.sha256(data).hexdigest()


def artifact(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'bytes': path.stat().st_size, 'sha256': digest(path.read_bytes())}


def build(manifest):
    directory = WORK / 'source-only'
    directory.mkdir(parents=True, exist_ok=True)
    files = [('scr_c_compiler_20261029.py', 'scr_c_compiler_20261029.py'),
             ('scr_c_compiler_20261029_v4.py', 'scr_c_compiler_20261029_v4.py'),
             ('build_scr_captures_20261029_batch06.py', 'build_scr_captures_20261029_batch06.py'),
             ('src/scripts/20261029/batch06/scr_numeric.h', 'scr_numeric.h')]
    files += [(family['source'], Path(family['source']).name) for family in manifest['families']]
    for source, target in files:
        shutil.copyfile(ROOT / source, directory / target)
    layout = [{'scriptSha256': unit['scriptSha256'], 'startPc': unit['startPc'],
               'sourceName': Path(unit['source']).name, 'allocation': unit['namedAllocation']} for unit in manifest['units']]
    layout_path = directory / 'layout.json'
    layout_path.write_text(json.dumps(layout, indent=2) + '\n')
    command = [sys.executable, str(directory / 'build_scr_captures_20261029_batch06.py'),
               '--layout', 'layout.json', '--output', 'products.json']
    result = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=90, check=True)
    products_path = directory / 'products.json'
    product_report = json.loads(products_path.read_text())
    assert product_report['originalBytecodeCompilerInput'] is False
    products = {(item['scriptSha256'], item['startPc']): item for item in product_report['products']}
    assert len(products) == len(manifest['units']) == 115
    return products, {'command': command, 'cwd': str(directory), 'exitCode': result.returncode,
        'stdout': result.stdout.strip(), 'sourceOnlyInputs': [artifact(directory / name) for unused, name in files],
        'layout': artifact(layout_path), 'products': artifact(products_path), 'originalBytecodeCompilerInput': False}


def main():
    assert unicorn.__version__ == '2.1.4'
    for image, expected in ((fixtures.native.MAIN, fixtures.native.MAIN_HASH),
                            (fixtures.native.OVERLAY, fixtures.native.OVERLAY_HASH), (fixtures.native.ITCM, fixtures.native.ITCM_HASH)):
        assert digest(image) == expected
    WORK.mkdir(parents=True, exist_ok=True)
    manifest_path = ROOT / 'evidence/encounter/scr-capture-source-layout-20261029.json'
    manifest = json.loads(manifest_path.read_text())
    audit = auditor.audit()
    current = {(row['scriptSha256'], row['startPc']): row for row in audit['instances']}
    for unit in manifest['units']:
        row = current[(unit['scriptSha256'], unit['startPc'])]
        assert not row['unresolvedOutsideReads']
        assert row['slotReferences'] == {int(slot): refs for slot, refs in unit['slotReferences'].items()}
        assert list(row['namedAllocation'].values()) == list(unit['namedAllocation'].values())
    products, build_report = build(manifest)
    grouped = defaultdict(list)
    for unit in manifest['units']:
        grouped[unit['asset']].append(unit)
    modules, calls, machines, ordinal = [], 0, 0, 0
    rom, files = assets.original_files()
    for asset, units in sorted(grouped.items()):
        data = assets.load(ROOT / asset)
        rebuilt = bytearray(data['script'])
        ranges = []
        for unit in sorted(units, key=lambda row: row['startPc']):
            base, end = unit['startPc'], unit['endExclusivePc']
            product = products[(data['scriptSha256'], base)]
            body = bytes.fromhex(product['bodyHex'])
            assert body == data['code'][base:end] and digest(body) == unit['bodySha256']
            assert product['compilerReport']['namedAllocationProfile'] == unit['namedAllocation']
            rebuilt[4100 + base:4100 + end] = body
            ranges.append({'startPc': base, 'endExclusivePc': end, 'bytes': len(body), 'sha256': digest(body),
                'mode': 'SCR', 'vmHostProcessor': 'ARM9', 'source': unit['source'], 'family': unit['family'],
                'entryAliases': unit['entryAliases'], 'allocation': unit['namedAllocation'], 'apis': unit['apis'],
                'emittedBodyHex': body.hex(), 'slotReferences': unit['slotReferences'],
                'unresolvedOutsideReads': [], 'sourceFunction': unit['sourceFunction'],
                'privateReturnPc': end - 4, 'externalInteriorEntries': 0, 'sharedReturnTailDetected': False,
                'productKey': [data['scriptSha256'], base], 'nativeCases': []})
        assert bytes(rebuilt) == data['script']
        for unit, match in zip(sorted(units, key=lambda row: row['startPc']), ranges):
            for thread in range(4):
                for variant in range(3):
                    ordinal += 1
                    seed = 2026103036000 + ordinal
                    original = fixtures.execute(data['script'], unit, thread, variant, seed)
                    recompiled = fixtures.execute(bytes(rebuilt), unit, thread, variant, seed)
                    assert original == recompiled
                    match['nativeCases'].append(original)
                    calls += original['actualReturningCalls']
                    machines += 1
        interval = files[Path(asset).name]
        raw = (ROOT / asset).read_bytes()
        assert raw == rom[interval[0]:interval[1]]
        members = []
        for index in range(assets.u32(raw, 4)):
            offset, length = struct.unpack_from('<II', raw, 8 + index * 40 + 32)
            stored = raw[offset:offset + length]
            assert assets.ash(stored) == data['script']
            members.append({'index': index, 'storedOffset': offset, 'storedBytes': length,
                            'storedSha256': digest(stored), 'scriptSha256': data['scriptSha256']})
        modules.append({'asset': asset, 'archiveSha256': data['assetSha256'], 'scriptSha256': data['scriptSha256'],
            'codeSha256': digest(data['code']), 'entryTableSha256': digest(data['script'][4:4100]),
            'romFileRange': list(interval), 'members': members, 'matchedRanges': ranges,
            'originalScaffoldingBytes': len(rebuilt) - sum(match['bytes'] for match in ranges),
            'scaffoldingSourceCredit': 0, 'rebuiltDecodedImageEqualsOriginal': True, 'wholeImageReconstructed': False})
    assert machines == 115 * 12
    negatives = []
    for family in manifest['families']:
        unit = next(unit for unit in manifest['units'] if unit['family'] == family['name'])
        wrong = dict(unit['namedAllocation'])
        wrong[next(iter(wrong))] = next(slot for slot in range(256) if slot not in wrong.values())
        body, unused = compiler.compile_source(ROOT / family['source'], unit['startPc'], wrong)
        assert body != bytes.fromhex(products[(unit['scriptSha256'], unit['startPc'])]['bodyHex'])
        negatives.append({'family': family['name'], 'wrongValidAllocationChangesBytes': True})
    report = {'schemaVersion': 1, 'generator': Path(__file__).relative_to(ROOT).as_posix(),
        'generatorSha256': digest(Path(__file__).read_bytes()), 'evidenceClass': 'ordinary-C-fixed-slot-input-capture-SCR-source-matches',
        'reproductionCommand': 'python match_scr_captures_20261029_batch06.py', 'romSha256': assets.ROM_HASH,
        'sourceClosure': [{'path': path, 'sha256': sha} for path, sha in PINS.items()],
        'sourceOnlyBuild': build_report, 'manifest': artifact(manifest_path),
        'currentOutsideReferenceAudit': audit, 'modules': modules,
        'sourceDefinitionFamilies': manifest['families'], 'newAuthoredDefinitions': len(manifest['families']),
        'uniqueApiShapeFamilies': len({tuple(api[0] for api in family['apis']) for family in manifest['families']}),
        'sourceDefinitionGroupsAreNotDistinctControlFlowLogicClaims': True,
        'completeFunctionInstances': 115, 'qualifiedScriptRangeBytes': 7368, 'newSubstantiveDecisionLogicBytes': 0,
        'fixedSlotAbi': manifest['abi'], 'actualReturningCallsPerImplementation': calls,
        'actualReturningCallsTotal': calls * 2, 'freshMachinesPerImplementation': machines,
        'allGeneralRegistersCpsrOrderedCpuStoresPersistentAndVmStateCompared': True,
        'wrongAllocationControls': negatives, 'nativeFunctionStubs': 0, 'completeImagesRecovered': 0,
        'ordinaryNativeExecutableByteCredit': 0, 'wholeRomSourceMatch': False,
        'heldUnits': manifest['heldUnits'], 'heldUnitSourceCredit': 0,
        'limitations': ['Input capture only; zero new substantive decisions or gameplay meaning',
            'C declarations are explicitly bound VM-register outputs and remain stored after RET; this is not a portable private-auto-variable ABI',
            'Every selected slot has its complete known direct references and conservative initialization qualification exported',
            'One128B unit with three unreconciled live-in reads remains excluded; no source or byte credit',
            'Native opaque/computed references and reentrant or concurrent scheduling semantics remain incomplete',
            'Per-unit proof covers all four VM threads and raw binary32 signed-zero/NaN/infinity/finite inputs with numeric0/255/distinct bytes',
            'Remaining script/native/container bytes and all member aliases remain zero additional source credit']}
    OUTPUT.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'report': str(OUTPUT), 'instances': 115, 'bytes': 7368, 'copyFamilies': len(manifest['families']),
                      'substantiveDecisionBytes': 0, 'actualReturns': calls * 2, 'freshMachinesPerImplementation': machines}))


if __name__ == '__main__':
    main()
