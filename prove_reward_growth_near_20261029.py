import json
import struct
import sys
from pathlib import Path

import match_runtime as compiler
import prove_reward_return_abi_20261029 as model
from elftools.elf.elffile import ELFFile
from link_runtime_unit import LINKER, LINKER_HASH, measured_module, validate
from ov001_award_cases_20261029 import assets
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCE_PREFIX = ROOT / 'nonmatching/ov001/20261029-reward-helpers01/021e4120'
WORK = ROOT / 'work/ov001-reward-growth-near/20261029'
REPORT = ROOT / 'evidence/functional/ov001-growth-near-20261029.json'
ADDRESS = 0x021E4120
SOURCE_SHA256 = 'c061995c9c9f1ff8726553e0efbcd55d814c94813479a76af698e46dbaa78930'


def observe_processes(executable):
    observed_commands = []

    def audited(event, arguments):
        if event == 'subprocess.Popen':
            command = arguments[1]
            matching = command.startswith((str(executable) + ' ', '"' + str(executable) + '" ')) if isinstance(command, str) else Path(command[0]).resolve() == executable.resolve()
            if matching:
                observed_commands.append({'command': command, 'cwd': str(arguments[2])})

    sys.addaudithook(audited)
    return observed_commands


def link_candidate(entry, bindings):
    directory = WORK / 'link' / entry['objectSha256']
    observed_commands = observe_processes(LINKER)
    try:
        validate(entry, bindings, directory)
    except ValueError as error:
        rejection = error.args[0]
        if not isinstance(rejection, dict) or rejection.get('matchingBytes') != 961:
            raise
    else:
        raise ValueError('Near candidate unexpectedly accepted as an exact caller')
    if len(observed_commands) != 1 or sha256(LINKER) != LINKER_HASH:
        raise ValueError('Near caller actual linker command/pin was not observed')
    code = (directory / 'caller.bin').read_bytes()
    elf_path = directory / 'linked.elf'
    with elf_path.open('rb') as stream:
        elf = ELFFile(stream)
        symbols = list(elf.get_section_by_name('.symtab').iter_symbols())
        caller = next(symbol for symbol in symbols if symbol.name == entry['name'])
        if caller['st_value'] != ADDRESS or caller['st_size'] != 992:
            raise ValueError('Near caller ELF address/size changed')
        for name, binding in bindings.items():
            symbol = next(symbol for symbol in symbols if symbol.name == name)
            mapping = '$t' if binding['mode'] == 'thumb' else '$a'
            target = int(binding['address'], 0)
            if symbol['st_value'] != target or symbol['st_size'] != 0:
                raise ValueError('Near caller mode anchor acquired code or changed address')
            if not any(symbol.name == mapping and symbol['st_value'] == target for symbol in symbols):
                raise ValueError('Near caller mode anchor lost qualified mapping')
    if any(path.stat().st_size for path in directory.glob('binding*.bin')):
        raise ValueError('Near caller anchor emitted initialized callee bytes')
    return code, {'canonicalExactValidationRejected': rejection,
                  'actualLinkerInvocation': {**observed_commands[0], 'exitCode': 0,
                      'exitCodeEvidence': 'Canonical validator reached byte comparison after checking actual linker return code0'},
                  'linkerSha256': sha256(LINKER),
                  'linkedElf': elf_path.relative_to(ROOT).as_posix(), 'linkedElfSha256': sha256(elf_path),
                  'lcf': (directory / 'unit.lcf').relative_to(ROOT).as_posix(),
                  'lcfSha256': sha256(directory / 'unit.lcf'),
                  'linkedCallerSha256': compiler.sha(code), 'zeroCalleeCodeModeAnchorsVerified': True}


def cases(blobs):
    for null_table in (False, True):
        for species in [1, 4, 20, 33]:
            for level in ([1, 100] if null_table else [1, 10, 11, 40, 41, 50, 51, 100]):
                for variant in range(3):
                    if null_table:
                        flags = struct.unpack_from('<H', blobs['EnmyKindTbl.bin'][8:], species * 100 + 4)[0]
                        size = ((flags >> 8) & 15) // 3
                        numerator, denominator = (3, 2) if size == 1 else (2, 1) if size == 2 else (1, 1)
                        missing_gain = model.scale(model.divide(-numerator + denominator - 1, denominator), variant)
                        base, parent = [missing_gain] * 6, [0] * 6
                    else:
                        base, parent = model.growth(blobs, species, variant, level)
                    before = [0, 32767, -32768, 20, -20, 32767 if null_table else 32767 - base[5]]
                    final = [model.short(model.short(old + first) + second) for old, first, second in zip(before, base, parent)]
                    expected = model.short(before[5] + base[5]) + parent[5]
                    record = bytearray(0x84)
                    struct.pack_into('<IhB', record, 0x14, 5000, species, variant)
                    struct.pack_into('<hh', record, 0x40, 1, 4)
                    record[0x4C], record[0x4D] = 0, 1
                    memory = [(model.ROSTER, bytes(100 * 0x84)), (model.ROSTER, bytes(record)),
                              (model.OUTPUT, struct.pack('<6h', *before))]
                    if null_table:
                        memory.append((0x02238D58, bytes(4)))
                    yield {'species': species, 'level': level, 'variant': variant,
                           'nullAbilityTable': null_table, 'initialStats': before,
                           'baseGrowth': base, 'parentGrowth': parent, 'finalStats': final,
                           'physicalR0Expected': expected, 'semanticReturnMeaningEstablished': False}, memory


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python/Unicorn required')
    sources = list(SOURCE_PREFIX.glob('frozen-growth961_*.c'))
    if len(sources) != 1 or sha256(sources[0]) != SOURCE_SHA256:
        raise ValueError('Frozen preferred source identity changed')
    compiler.WORK = WORK / 'compiler'
    compiler_invocations = observe_processes(compiler.COMPILER)
    records, unused = compiler.compare(sources[0], 'ov001', '2', 'off', True)
    if len(records) != 1 or records[0].get('matchingBytes') != 961 or records[0].get('compiledBytes') != 992 or records[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Frozen near-match metrics changed')
    entry = records[0]
    if len(compiler_invocations) != 1:
        raise ValueError('Actual near-source compiler invocation was not observed')
    bindings = qualified_bindings(entry)
    code, link = link_candidate(entry, bindings)
    main_metadata, main, unused = measured_module('main')
    metadata, overlay, unused = measured_module('ov001')
    original = overlay[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + 992]
    if len(code) != 992 or sum(a == b for a, b in zip(code, original)) != 961:
        raise ValueError('Real linked near-match metrics changed')
    rebuilt = bytearray(overlay)
    rebuilt[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + 992] = code
    blobs = assets()
    results = []
    for index, (case, memory) in enumerate(cases(blobs)):
        patches = [(model.OUTPUT, struct.pack('<6h', *case['finalStats']))]
        arguments = [model.OUTPUT, 5000, case['level']]
        original_result = model.execute(main, overlay, blobs, ADDRESS, arguments, memory, patches,
                                        case['physicalR0Expected'], 202610304400 + index)
        source_result = model.execute(main, bytes(rebuilt), blobs, ADDRESS, arguments, memory, patches,
                                      case['physicalR0Expected'], 202610304400 + index)
        differences = [key for key in original_result if original_result[key] != source_result[key]]
        allowed = {'wholeRamSha256', 'writeTraceSha256', 'pcTraceSha256', 'instructions'}
        if set(differences) - allowed:
            raise ValueError(('Near source behavior differs beyond explicit code/scheduling effects', differences))
        results.append({'case': case, 'native': original_result, 'rebuilt': source_result,
                        'differingMeasurements': differences, 'independentWholeRamEffectsPassOnEachSide': True,
                        'allGeneralRegistersFlagsAndFinalStackIdentical': True})
    dependencies = ['prove_reward_return_abi_20261029.py', 'ov001_award_cases_20261029.py',
                    'ov001_award_fixture_20261029.py', 'link_runtime_unit.py', 'recover_linked_runtime.py',
                    'config/arm9/symbols.txt', 'config/arm9/overlays/ov001/symbols.txt']
    report = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
              'processor': 'arm9', 'module': 'ov001', 'address': hex(ADDRESS), 'mode': 'arm', 'nativeBytes': 992,
              'moduleHashes': {'main': main_metadata['sha256'], 'ov001': metadata['sha256']},
              'nativeSpanSha256': compiler.sha(original), 'candidate': entry, 'nativeSymbolEntries': bindings,
              'actualCompilerInvocation': {**compiler_invocations[0], 'exitCode': 0,
                  'exitCodeEvidence': 'Canonical comparer parsed the newly compiled ELF after checking actual compiler return code0'},
              'realLink': link, 'vectors': len(results), 'actualReturns': len(results) * 2,
              'nativeGameplayStubs': 0, 'freshIsolatedMachinePerExecution': True,
              'nativeCalleesExecuted': True, 'independentSixStatAndPhysicalR0Model': True,
              'supportedErrorPath': 'Null AbilityTbl pointer returns signed-1 from native ability lookup; signed scaling/narrowing is modeled',
              'sourceMatchCredit': 0, 'acceptedExactSource': False, 'wholeModuleLinked': False,
              'semanticReturnMeaningEstablished': False, 'directKnownCallersDiscardR0': True,
              'instructionBound': 100000, 'results': results,
              'assetHashes': {name: compiler.sha(blob) for name, blob in blobs.items()},
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in dependencies],
              'limitations': ['961/992 matching bytes remain a nonmatching approximation with zero accepted source credit',
                              'Program code bytes differ; each complete RAM image is independently checked against its own input plus modeled output changes',
                              'Stack-write timing may differ; final complete stack, registers and flags are compared',
                              'Synthetic component states do not establish valid save records or whole-scene reachability',
                              'Other variants, levels, curve IDs, missing roster IDs, null kind table and arbitrary aliases remain unsupported']}
    write_json(REPORT, report)
    print(json.dumps({'vectors': len(results), 'actualReturns': len(results) * 2, 'matchingBytes': 961,
                      'sourceMatchCredit': 0, 'report': REPORT.relative_to(ROOT).as_posix()}))


if __name__ == '__main__':
    run()
