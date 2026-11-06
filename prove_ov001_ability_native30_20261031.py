import gzip
import json
import sys
from pathlib import Path

import match_runtime as compiler
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_ability_native30_cases_20261031 import vectors
from ov001_scalar_frontier07_fixture_20261030 import execute
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__

WORK = ROOT / 'work/ol30-proof'
REPORT = ROOT / 'evidence/functional/ov001-ability-native30-20261031.json'
SOURCES = [('src/overlays/ov001_20261031_ability28/flags.c',
    '8dfc73fd4fabc3aa8626079d64f2e715dd1c4b8f3431eb91f73b73ae2288ca35', 788, 0x0220FA6C),
    ('src/overlays/ov001_20261030_conditional_reroll_41e7e443b4bf.c',
    '41e7e443b4bf6a7b751c5ab0fee6c80882cf10dfcee664b5fd1a2fa9a843894e', 216, 0x02210AD0)]


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def run():
    if sys.version_info[:3] != (3, 13, 5) or __version__ != '2.1.4':
        raise ValueError('Pinned Python/Unicorn differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private input differs')
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    itcm_metadata, unused, unused = measured_module('itcm')
    candidate, source_proofs = bytearray(overlay), []
    for source_path, digest, length, address in SOURCES:
        source = ROOT / source_path
        if sha256(source) != digest:
            raise ValueError('Frozen composition source differs')
        compiler.WORK = WORK / f'{address:08x}' / 'c'
        rows, unused = compiler.compare(source, 'ov001', '2', 'off', True)
        if len(rows) != 1 or rows[0].get('compiledBytes') != length or not rows[0].get('exactAfterDeclaredRelocation'):
            raise ValueError('Composition source no longer matches')
        bindings = qualified_bindings(rows[0])
        directory = WORK / f'{address:08x}' / 'l'
        link = validate(rows[0], bindings, directory)
        linked = (directory / 'caller.bin').read_bytes()
        candidate[address - 0x021D7240:address - 0x021D7240 + length] = linked
        source_proofs.append(dict(source=source_path, sha256=digest, exactBytes=length, address=hex(address),
            comparison=rows[0], nativeSymbolEntries=bindings, isolatedLink=link, newSourceCredit=0))
    if bytes(candidate) != overlay:
        raise ValueError('Full composed original/source module images differ')
    rom = NintendoDSRom(config['rom'].read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in
        ('EnmyKindTbl.bin', 'AbilityTbl.bin', 'ActTbl.bin', 'ItemTbl.bin', 'EquipTbl.bin')}
    results, summaries = [], []
    cases = vectors()
    protocol_addresses = sorted({row['address'] for vector in cases for row in vector['protocols']})
    if 0x0203D294 in protocol_addresses or 0x0220FA6C in protocol_addresses:
        raise ValueError('RNG/top returns must not be counted in native dependency protocols')
    for index, vector in enumerate(cases):
        try:
            original = execute(main, overlay, assets, 0x0220FA6C, vector['arguments'], vector['memory'], vector['patches'],
                vector['physicalR0'], vector['seed'], vector['draws'], vector['protocols'])
            rebuilt = execute(main, bytes(candidate), assets, 0x0220FA6C, vector['arguments'], vector['memory'], vector['patches'],
                vector['physicalR0'], vector['seed'], vector['draws'], vector['protocols'])
        except Exception:
            print('Native30 failed case', index, flush=True)
            raise
        if original != rebuilt:
            raise ValueError('Native30 complete original/source execution evidence differs')
        public = {key: value for key, value in vector.items() if key not in ('memory', 'patches')}
        results.append(dict(recipe=public, result=original))
        summaries.append(dict(case=index, recipeSha256=compiler.sha(encoded(public)), resultSha256=compiler.sha(encoded(original)),
            actualReturns=2, nativeRngActualReturns=2 * len(original['rngReturns']),
            nativeDependencyActualReturns=2 * len(original['protocolReturns']), providedCalls=0,
            instructions=original['instructions'], returnWord=vector['physicalR0'], initialState=vector['initial'],
            finalState=vector['finalState'], finalFlags=vector['finalFlags'], rngDraws=len(vector['draws']),
            pcTraceSha256=original['pcTraceSha256'], writeTraceSha256=original['writeTraceSha256'],
            wholeRamSha256=original['wholeRamSha256'], stackSha256=original['stackSha256']))
        if index % 32 == 0:
            print('Native30 source/original actual returns', 2 * (index + 1), flush=True)
    control = ROOT / 'nonmatching/overlay-lane/20261031-packet28-negative/ability/source.c'
    compiler.WORK = WORK / 'wrong-mask/c'
    rows, unused = compiler.compare(control, 'ov001', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError('Native30 wrong-mask C control failed compilation')
    directory = WORK / 'wrong-mask/l'
    try:
        bad_link = validate(rows[0], qualified_bindings(rows[0]), directory)
    except ValueError as error:
        bad_link = error.args[0]
    if not isinstance(bad_link, dict) or bad_link.get('caller') != rows[0]['name']:
        raise ValueError('Native30 wrong-mask control did not genuinely link')
    bad_code, bad_overlay, vector = (directory / 'caller.bin').read_bytes(), bytearray(overlay), cases[0]
    bad_overlay[0x0220FA6C - 0x021D7240:0x0220FA6C - 0x021D7240 + len(bad_code)] = bad_code
    try:
        execute(main, bytes(bad_overlay), assets, 0x0220FA6C, vector['arguments'], vector['memory'], vector['patches'],
            vector['physicalR0'], vector['seed'], vector['draws'], vector['protocols'])
    except ValueError as error:
        mask_failure = error.args[0]
        if mask_failure != 'Order fixture full RAM/ITCM differs from independent model':
            raise ValueError(('Native30 mask control failed unexpectedly', mask_failure))
    else:
        raise ValueError('Native30 wrong-mask control unexpectedly passed')
    bad_draws = list(vector['draws'])
    bad_draws[0] = (bad_draws[0][0], (bad_draws[0][1] + 1) % bad_draws[0][0])
    try:
        execute(main, overlay, assets, 0x0220FA6C, vector['arguments'], vector['memory'], vector['patches'],
            vector['physicalR0'], vector['seed'], bad_draws, vector['protocols'])
    except ValueError as error:
        draw_failure = dict(failure=error.args[0], cause=str(error.__cause__))
        if str(error.__cause__) != 'Unexpected native RNG call/value in order fixture':
            raise ValueError(('Native30 wrong-draw prediction failed unexpectedly', draw_failure))
    else:
        raise ValueError('Native30 wrong-draw prediction unexpectedly passed')
    raw = encoded(dict(romSha256=config['romSha256'], module='ov001', address='0x0220FA6C', results=results))
    compressed = gzip.compress(raw, mtime=0)
    artifact = WORK / 'raw-traces' / (compiler.sha(compressed) + '.json.gz')
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_bytes(compressed)
    paths = ['ov001_ability_native30_cases_20261031.py', 'ov001_ability28_fixture_20261031.py',
        'ov001_scalar_frontier07_fixture_20261030.py', 'ov001_award_fixture_20261029.py',
        'ov001_award_cases_20261029.py', str(control.relative_to(ROOT)), str(control.with_name('context.h').relative_to(ROOT)),
        'src/overlays/ov001_20261031_ability28/context.h']
    report = dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], module='ov001', processor='arm9', mode='arm',
        address='0x0220FA6C', moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'],
        itcmInputSha256=itcm_metadata['sha256'], assetHashes={name: compiler.sha(data) for name, data in assets.items()},
        evidenceClass='connected original caller/conditional-reroll/native-RNG/metadata execution with independently predicted draws, returns and complete RAM effects',
        sourceFragments=source_proofs, newSourceCredit=0, acceptedSourceCredit=0, wholeModuleLinked=False,
        executions=2 * len(results), actualReturns=2 * len(results),
        nativeRngActualReturns=sum(row['nativeRngActualReturns'] for row in summaries),
        nativeDependencyActualReturns=sum(row['nativeDependencyActualReturns'] for row in summaries), providedCalls=0,
        returnCountPartition=dict(topAddress='0x0220FA6C', nativeRngAddress='0x0203D294',
            nativeDependencyAddresses=[hex(address) for address in protocol_addresses],
            mutuallyExclusiveAddressSets=True, untrackedNativeCalleeReturns='Not added to either measured return total'),
        freshMachinePerExecution=True, instructionBound=100000, maximumInstructions=max(row['instructions'] for row in summaries),
        results=summaries, rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)), sha256=compiler.sha(compressed),
            bytes=len(compressed), format='json+gzip', gzipMtime=0, uncompressedSha256=compiler.sha(raw)),
        rejectedWrongMaskSource=dict(expectedRejected=True, actualLinkComparison=bad_link, compilation=rows, failure=mask_failure, sourceCredit=0),
        rejectedWrongDrawPrediction=dict(expectedRejected=True, actualReturn=False, evidence=draw_failure, sourceCredit=0),
        inputPins=[dict(path=p, sha256=sha256(ROOT / p)) for p in paths], generatorSha256=sha256(Path(__file__)),
        limitations=['Synthetic input RNG state is explicit, not an observed current/future scene seed or persistence claim',
            'Form byte1FD is0; alternate trait/resource paths require separate qualification',
            '64-byte raw skill lists have zero termination, duplicates and full-length bounds; no valid-save or ordinary-battle scene reachability is inferred',
            'No skills128..137 contribute to the maximum-scalar dependency; their actual native lookups are checked to return0',
            'Native7B674 count semantics and actor1F0/21C scalar words are scoped to these inputs; raw ability names/masks are not interpreted',
            'Existing caller788 candidate and accepted216 reroll source are freshly compiled/linked but receive no new/duplicate credit here',
            'createdUtc is volatile; stable report identity excludes only that field'],
        reproductionCommand='python prove_ov001_ability_native30_20261031.py')
    report['deterministicContentSha256'] = compiler.sha(encoded({key: value for key, value in report.items() if key != 'createdUtc'}))
    write_json(REPORT, report)
    print(json.dumps({key: report[key] for key in ['actualReturns', 'nativeRngActualReturns', 'nativeDependencyActualReturns', 'providedCalls', 'maximumInstructions']}), flush=True)


if __name__ == '__main__':
    run()
