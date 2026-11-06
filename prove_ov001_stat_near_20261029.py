import json
import struct
import sys
from pathlib import Path

import match_runtime as compiler
from elftools.elf.elffile import ELFFile
from link_runtime_unit import LINKER, LINKER_HASH, measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_stat_initialization_fixture_20261029 import ADDRESS, execute, vectors
from prove_reward_growth_near_20261029 import observe_processes
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / 'nonmatching/ov001/20261029-actor-dependencies/021d9a04/frozen-stat-near_601f1e75fdde.c'
SOURCE_SHA256 = '601f1e75fdde10789b9ea96d45b0a89d48e73dda2dfbd707f976cae7a61458ba'
WORK = ROOT / 'work/ov001-actor-dependencies/20261029/stat-functional'
REPORT = ROOT / 'evidence/functional/ov001-stat-initialization-near-20261029.json'


def commuting_setup(native, candidate):
    differing = [i for i in range(0, 776, 4) if native[i:i + 4] != candidate[i:i + 4]]
    if differing != [0x34, 0x38]:
        raise ValueError('Near stat initializer differs outside the two expected setup instructions')
    original = struct.unpack_from('<2I', native, 0x34)
    rebuilt = struct.unpack_from('<2I', candidate, 0x34)
    if original != (0xE2880F6D, 0xE1A01006) or rebuilt != original[::-1]:
        raise ValueError('Near stat setup pair acquired other operations')
    decoded = [
        {'operation': 'ADD-immediate', 'condition': 'always', 'flagsWritten': False,
         'reads': [8], 'writes': [0], 'immediate': 436, 'memoryReadOrWritten': False},
        {'operation': 'MOV-register', 'condition': 'always', 'flagsWritten': False,
         'reads': [6], 'writes': [1], 'memoryReadOrWritten': False},
    ]
    if set(decoded[0]['writes']) & set(decoded[1]['reads'] + decoded[1]['writes']) or set(decoded[1]['writes']) & set(decoded[0]['reads']):
        raise ValueError('Near setup pair has a register dependency')
    return {'differingOffsets': differing, 'nativeWords': [hex(x) for x in original],
            'candidateWords': [hex(x) for x in rebuilt], 'decoded': decoded,
            'boundaryStateEqualForAll32BitRegisterInputs': True,
            'reason': 'Disjoint output registers, no output read by the other operation, no flags/memory/PC source, same finalPC',
            'scope': 'Execution enters at the function boundary and observes state after both instructions; asynchronous/interior observations excluded',
            'sourceMatchCredit': 0}


def link_candidate(entry, bindings):
    directory = WORK / 'link' / entry['objectSha256']
    invocations = observe_processes(LINKER)
    try:
        validate(entry, bindings, directory)
    except ValueError as error:
        rejection = error.args[0]
        if not isinstance(rejection, dict) or rejection.get('matchingBytes') != 768 or rejection.get('nativeBytes') != 776:
            raise
    else:
        raise ValueError('Nonmatching stat candidate unexpectedly passed exact validation')
    if sha256(LINKER) != LINKER_HASH or len(invocations) != 1:
        raise ValueError('Pinned genuine linker changed')
    with (directory / 'linked.elf').open('rb') as stream:
        elf = ELFFile(stream)
        symbols = list(elf.get_section_by_name('.symtab').iter_symbols())
        caller = next(symbol for symbol in symbols if symbol.name == entry['name'])
        if caller['st_value'] != ADDRESS or caller['st_size'] != 776:
            raise ValueError('Near stat caller ELF address/size changed')
        for name, binding in bindings.items():
            symbol = next(symbol for symbol in symbols if symbol.name == name)
            target = int(binding['address'], 0)
            mapping = '$t' if binding['mode'] == 'thumb' else '$a'
            if symbol['st_value'] != target or symbol['st_size'] != 0 or not any(s.name == mapping and s['st_value'] == target for s in symbols):
                raise ValueError('Near stat caller lost a zero-code qualified mode anchor')
    if any(path.stat().st_size for path in directory.glob('binding*.bin')):
        raise ValueError('Near stat mode anchor emitted initialized callee bytes')
    code = (directory / 'caller.bin').read_bytes()
    return code, {'canonicalExactValidationRejected': rejection, 'linkerSha256': sha256(LINKER),
                  'actualInvocation': {**invocations[0], 'exitCode': 0,
                      'exitCodeEvidence': 'Canonical validator reached byte comparison after checking actual linker return code0'},
                  'linkedElf': (directory / 'linked.elf').relative_to(ROOT).as_posix(),
                  'linkedElfSha256': sha256(directory / 'linked.elf'),
                  'lcf': (directory / 'unit.lcf').relative_to(ROOT).as_posix(),
                  'lcfSha256': sha256(directory / 'unit.lcf'), 'linkedCallerSha256': compiler.sha(code),
                  'zeroInitializedCalleeCodeAnchorsVerified': True}


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4' or sha256(SOURCE) != SOURCE_SHA256:
        raise ValueError('Pinned interpreter/Unicorn/frozen near source changed')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private ROM changed')
    rom = NintendoDSRom(config['rom'].read_bytes())
    blobs = {name: bytes(rom.getFileByName(name)) for name in ['ItemTbl.bin', 'EquipTbl.bin', 'EnmyKindTbl.bin']}
    compiler.WORK = WORK / 'compiler'
    compiler_invocations = observe_processes(compiler.COMPILER)
    records, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', True)
    if len(records) != 1 or records[0].get('bytes') != 776 or records[0].get('matchingBytes') != 768 or records[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Near stat source/code metrics changed')
    entry = records[0]
    if len(compiler_invocations) != 1:
        raise ValueError('Actual compiler invocation was not observed')
    bindings = qualified_bindings(entry)
    linked, link = link_candidate(entry, bindings)
    main_metadata, main, unused = measured_module('main')
    metadata, overlay, unused = measured_module('ov001')
    native = overlay[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + 776]
    commutation = commuting_setup(native, linked)
    results = []
    for vector in vectors():
        original = execute(main, overlay, native, native, blobs, vector)
        rebuilt = execute(main, overlay, linked, native, blobs, vector)
        if original != rebuilt:
            raise ValueError('Native/near stat initializer state differs')
        results.append(original)
    dependencies = ['ov001_stat_initialization_fixture_20261029.py', 'ov001_award_fixture_20261029.py',
                    'prove_reward_growth_near_20261029.py',
                    'link_runtime_unit.py', 'recover_linked_runtime.py', 'config/arm9/symbols.txt',
                    'config/arm9/overlays/ov001/symbols.txt']
    report = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': config['romSha256'],
              'processor': 'arm9', 'module': 'ov001', 'address': hex(ADDRESS), 'mode': 'arm', 'nativeBytes': 776,
              'moduleHashes': {'main': main_metadata['sha256'], 'ov001': metadata['sha256']},
              'candidate': entry, 'nativeSymbolEntries': bindings, 'realLink': link,
              'actualCompilerInvocation': {**compiler_invocations[0], 'exitCode': 0,
                  'exitCodeEvidence': 'Canonical comparer parsed the newly compiled object after checking actual compiler return code0'},
              'commutingRegisterSetupProof': commutation, 'vectors': len(results), 'actualReturns': len(results) * 2,
              'nativeRngReturns': sum(len(row['independentDraws']) for row in results) * 2,
              'nativeGameplayStubs': 0, 'nativeCalleesExecuted': True, 'freshMachinePerExecution': True,
              'independentStatModifiersHpMpScalingAndLcgModel': True,
              'sourceMatchCredit': 0, 'acceptedExactSource': False, 'wholeModuleLinked': False,
              'semanticReturnMeaningEstablished': False, 'instructionBound': 100000, 'results': results,
              'assetHashes': {name: compiler.sha(blob) for name, blob in blobs.items()},
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in dependencies],
              'limitations': ['Only768/776 bytes match; formal boundary commutation and functional vectors do not create exact source credit',
                  'The known code span is normalized only for cross-image RAM hashing; each actual full RAM image is independently checked against its own code plus modeled effects',
                  'Traits4F..56, measured item0 and bounded nonnegative stats are supported; other traits/items, negative bases, aliases and inaccessible pointers remain unsupported',
                  'No current/future scene RNG state or valid save/scene reachability is inferred',
                  'Physical R0 values are checked while source-language return meaning remains unproved',
                  'Asynchronous interrupts, breakpoints inside the swapped setup pair and interior entry are outside the commutation proof']}
    write_json(REPORT, report)
    print(json.dumps({'vectors': len(results), 'actualReturns': len(results) * 2,
                      'nativeRngReturns': report['nativeRngReturns'], 'matchingBytes': 768,
                      'sourceMatchCredit': 0, 'report': REPORT.relative_to(ROOT).as_posix()}))


if __name__ == '__main__':
    run()
