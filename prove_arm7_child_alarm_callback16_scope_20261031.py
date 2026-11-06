import hashlib
import json
from pathlib import Path
import match_runtime
import utility_runtime
import crossreuse_utility_c
import link_arm7_bulk_20261030 as linker
import arm7_child_alarm_engine_20261031 as original_engine
import arm7_child_alarm_callback16_scope_engine_20261031 as proposed_engine
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_CALL, CS_GRP_JUMP
from elftools.elf.elffile import ELFFile
from capstone.arm import ARM_REG_PC
from project import ROOT, write_json

WORK = ROOT / 'work/arm7-bulk-20261030/lane-child-alarm-callback16-scope-final'
REPORT = ROOT / 'evidence/attempts/child-alarm-callback16-scope-20261031.json'
ADDRESS = 0x037FD900
IDENTITY = {'processor': 'arm7', 'program': 'dwc/utility.bin/move/child.srl', 'module': 'utility-child-arm7-wram', 'mode': 'arm', 'address': hex(ADDRESS)}
BASE_LINKER_SHA = 'f9afd9a3b5142dbb2f5bec561a8a4f3d725ec4b52faba9f9d7aa7837a540922c'
PINS = ROOT / 'nonmatching/arm7-bulk/20261031/lane-child-alarm-callback16-scope-final/generator-pins.json'
PIN_SHA = '109677a1cd3f747ef84bc34bb9cdf6834943f7239dfcfbb8c28b4a96e13bd328'
ROM_SHA = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify_inputs():
    import sys
    import unicorn
    import elftools
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4' or elftools.__version__ != '0.33':
        raise ValueError('Pinned scope-analysis runtime differs')
    if digest(PINS.read_bytes()) != PIN_SHA or digest((ROOT / 'inputs/game.nds').read_bytes()) != ROM_SHA:
        raise ValueError('Original build or scope generator closure differs')
    rows = json.loads(PINS.read_text())['files']
    for row in rows:
        path = (ROOT / row['path']).resolve()
        if not path.is_relative_to(ROOT) or digest(path.read_bytes()) != row['sha256']:
            raise ValueError('Frozen scope input changed: ' + row['path'])
    return rows


def inventory():
    layout, unused = utility_runtime.derive()
    modules = {row['id']: row for row in layout['modules'] if row.get('processor') == 'arm7'}
    binaries = {name: (ROOT / row['binary']).read_bytes() for name, row in modules.items()}
    legacy = json.loads((ROOT / 'evidence/utility/ghidra-arm7.json').read_text())['functions']
    roots = [row for row in legacy if row['module'] in modules]
    raw = binaries[IDENTITY['module']]
    body = raw[ADDRESS - proposed_engine.BASE:ADDRESS - proposed_engine.BASE + 16]
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    instructions = list(decoder.disasm(body, ADDRESS))
    if digest(body) != proposed_engine.SUPPLEMENT_SHA or [row.mnemonic for row in instructions] != ['push', 'bl', 'pop', 'bx']:
        raise ValueError('Measured callback16 instruction role differs')
    if [row.op_str for row in instructions] != ['{r0, lr}', '#0x37fd910', '{r0, lr}', 'lr']:
        raise ValueError('Callback frame, R0 preservation or known handler target differs')
    if any(int(row['address'], 0) == ADDRESS for row in roots):
        raise ValueError('Entry already exists in frozen legacy inventory')
    previous = next(row for row in roots if row['module'] == IDENTITY['module'] and int(row['address'], 0) == 0x037FD86C)
    following = next(row for row in roots if row['module'] == IDENTITY['module'] and int(row['address'], 0) == 0x037FD910)
    if [[int(x, 0) for x in pair] for pair in previous['ranges']] != [[0x037FD86C, 0x037FD8E8]]:
        raise ValueError('Preceding initializer instruction/pool boundary differs')
    previous_pool = set()
    for instruction in decoder.disasm(raw[0x037FD86C - proposed_engine.BASE:0x037FD8E8 - proposed_engine.BASE], 0x037FD86C):
        for operand in instruction.operands:
            if operand.type == 3 and operand.mem.base == ARM_REG_PC:
                previous_pool.add(instruction.address + 8 + operand.mem.disp)
    if previous_pool != set(range(0x037FD8E8, ADDRESS, 4)) or following['mode'] != 'arm':
        raise ValueError('Preceding literal pool or following original ARM entry differs')
    pointers, branches, interiors, data_references = [], [], [], []
    for name, binary in binaries.items():
        base = int(modules[name]['base'], 0)
        for offset in range(0, len(binary) - 3, 4):
            word = int.from_bytes(binary[offset:offset + 4], 'little')
            if ADDRESS <= (word & ~1) < ADDRESS + 16:
                item = {'module': name, 'storageAddress': hex(base + offset), 'word': hex(word)}
                pointers.append(item)
                if word != ADDRESS:
                    interiors.append(item)
    for row in roots:
        decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB if row['mode'] == 'thumb' else CS_MODE_ARM)
        decoder.detail = True
        base = int(modules[row['module']]['base'], 0)
        for first, last in row['ranges']:
            first, last = int(first, 0), int(last, 0)
            for instruction in decoder.disasm(binaries[row['module']][first - base:last - base], first):
                for operand in instruction.operands:
                    if operand.type == 3 and operand.mem.base == ARM_REG_PC:
                        origin = ((instruction.address + 4) & ~3) if row['mode'] == 'thumb' else instruction.address + 8
                        target = origin + operand.mem.disp
                        if ADDRESS <= target < ADDRESS + 16:
                            data_references.append({'module': row['module'], 'root': row['address'], 'pc': hex(instruction.address), 'target': hex(target)})
                if not instruction.operands or instruction.operands[0].type != 2 or not (instruction.group(CS_GRP_CALL) or instruction.group(CS_GRP_JUMP)):
                    continue
                target = instruction.operands[0].imm & ~1
                if ADDRESS <= target < ADDRESS + 16:
                    item = {'module': row['module'], 'root': row['address'], 'pc': hex(instruction.address), 'target': hex(target)}
                    branches.append(item)
                    if target != ADDRESS:
                        interiors.append(item)
    if data_references:
        raise ValueError('Code/literal dual use must be reconciled before callback scope approval')
    if interiors or not any(row['storageAddress'] == '0x37fddc0' for row in pointers):
        raise ValueError('Original callback pointer producer or interior reconciliation differs')
    return {'identity': IDENTITY, 'inputModuleSha256': digest(raw), 'codeSha256': digest(body), 'bytes': 16,
        'instructionBytes': 16, 'literalBytes': 0, 'alignmentBytes': 0, 'initializedDenominatorDelta': 0,
        'precedingPoolWords': sorted(hex(value) for value in previous_pool), 'precedingRoot': previous, 'precedingFullFunctionEnds': hex(ADDRESS), 'followingRoot': following,
        'originalLoader': modules[IDENTITY['module']], 'pointerWords': pointers, 'directExternalBranches': branches,
        'unreconciledInteriorOrModeReferences': [], 'literalDataReferencesIntoProposedCode': data_references, 'nativeInstructions': [{'address': hex(row.address), 'mnemonic': row.mnemonic, 'operands': row.op_str} for row in instructions],
        'frameBytes': 8, 'measuredExtraPreservedWord': 'R0', 'ordinarySourceCredit': 0, 'originalAssemblyProvenanceVerified': False,
        'sharedInventoryOrLinkerChanged': False, 'scopeAdopted': False}


def strict_candidate_refusal():
    if digest(Path(linker.__file__).read_bytes()) != BASE_LINKER_SHA:
        raise ValueError('Frozen unknown-symbol guard changed')
    profile = ROOT / 'nonmatching/arm7-bulk/20261031/lane-child-alarm-programmer156-v1/profile.json'
    row = json.loads(profile.read_text())['results'][0]
    source = ROOT / row['source']
    if digest(source.read_bytes()) != row['sourceSha256']:
        raise ValueError('Current ordinary C hypothesis changed')
    compiler = ROOT / 'tools/mwccarm/mwccarm/1.2/sp2p3/mwccarm.exe'
    flags = match_runtime.FLAGS[:]
    flags[flags.index('-proc') + 1] = 'arm7tdmi'
    flags[flags.index('-inline') + 1] = 'all'
    flags += ['-lang', 'c99', '-opt', 'space']
    directory = WORK / 'strict-candidate'
    directory.mkdir(parents=True, exist_ok=True)
    match_runtime.WORK = directory / 'isolated-runtime'
    attempt, compiled = crossreuse_utility_c.compile_origin(row, compiler, flags, directory)
    if compiled is None:
        raise ValueError(attempt)
    derived, masks, body = compiled
    native = (ROOT / row['binary']).read_bytes()[int(row['address'], 0) - row['base']:int(row['address'], 0) - row['base'] + row['bytes']]
    excluded = {offset + index for offset, unused in masks for index in range(4)}
    if len(body) != 156 or any(a != b for index, (a, b) in enumerate(zip(body, native)) if index not in excluded):
        raise ValueError('Current full-sized C hypothesis no longer matches comparable bytes')
    with (ROOT / derived['probeObject']).open('rb') as stream:
        elf = ELFFile(stream)
        symbol = next(value for value in elf.get_section_by_name('.symtab').iter_symbols() if value.name == row['name'])
        section, offset = symbol['st_shndx'], symbol['st_value'] & ~1
    entry = dict(row, compiler=compiler.relative_to(ROOT).as_posix(), compilerSha256=digest(compiler.read_bytes()), compilerFlags=flags,
        targetSha256=digest(native), object=derived['probeObject'], objectSha256=derived['probeObjectSha256'], sectionIndex=section,
        sectionOffset=offset, relocations=[dict(value, format='SHT_RELA', explicitAddend=value['addend'],
            originalEncodedWord=body[value['offset']:value['offset'] + 4].hex()) for value in derived['relocations']])
    try:
        linker.validate(entry, directory / 'refused-real-link')
    except ValueError as failure:
        if str(failure) != 'Unqualified ARM7 native function/alternate entry: native_utility_child_arm7_arm_037fd900 0x37fd900':
            raise
        reason = str(failure)
    else:
        raise ValueError('Original unknown callback guard was bypassed')
    return {'entry': entry, 'compiledBytes': 156, 'matchingComparableBytes': len(body) - len(excluded), 'reason': reason,
        'actualGenuineMwldMatch': False, 'sourceOrByteCredit': 0, 'originalGuardPreserved': True}


def native_evidence():
    records = []
    for seed in range(16):
        machine = proposed_engine.setup({}, seed)
        cpu = machine['cpu']
        alarm = proposed_engine.DATA + 0x1000
        cpu.mem_write(alarm + 12, [0, 1, 0xFFFF, 0x10000][seed % 4].to_bytes(8, 'little'))
        cpu.mem_write(0x04000210, [0, 8, 0xFFFFFFFF][seed % 3].to_bytes(4, 'little'))
        cpu.mem_write(0x04000208, [0, 1, 0xFFFF][seed % 3].to_bytes(2, 'little'))
        producer = machine['invoke'](0x037FDD30, [alarm])
        pointer = int.from_bytes(cpu.mem_read(0x03805988, 4), 'little')
        stored_argument = int.from_bytes(cpu.mem_read(0x03805990, 4), 'little')
        argument = [stored_argument, 1, 0x80000000, 0xFFFFFFFF][seed % 4]
        result = machine['invoke'](pointer, [argument])
        if not producer['actualReturn'] or pointer != ADDRESS or stored_argument != 0 or not result['actualReturn'] or result['registers'][0] != argument:
            raise ValueError('Original producer/full callback return/R0 preservation differs')
        if not set(range(ADDRESS, ADDRESS + 16, 4)).issubset(result['visited']):
            raise ValueError('Complete proposed callback instructions not executed')
        records.append({'producer': producer, 'installedPointer': hex(pointer), 'storedArgument': stored_argument,
            'invocationArgument': argument, 'syntheticRawArgumentProbe': argument != stored_argument, 'callback': result})
    original = original_engine.setup({}, 40)['invoke'](ADDRESS, [0])
    thumb = proposed_engine.setup({}, 41)['invoke'](ADDRESS | 1, [0])
    cap = proposed_engine.setup({}, 42)['invoke'](ADDRESS, [0], 1)
    if any(value['actualReturn'] for value in (original, thumb, cap)):
        raise ValueError('Legacy scope/incorrect mode/cap acquired callback return credit')
    WORK.mkdir(parents=True, exist_ok=True)
    path = WORK / 'native-records.json'
    write_json(path, records)
    return {'cases': 16, 'actualOriginalProgrammerReturnsSeparate': 16, 'actualOriginalCallbackReturns': 16,
        'all4ArmInstructionsExecuted': True, 'record': {'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path.read_bytes())},
        'originalScopeRefusal': original, 'wrongModeRefusal': thumb, 'oneInstructionCap': cap,
        'postFaultOrCapStateExcluded': True, 'returnOrSourceCreditFromUnsupportedRuns': 0,
        'limitations': ['Actual original producer installs the pointer, then a bounded host invocation calls it; no asynchronous IRQ dispatch or scene reachability',
            'Queue is empty and timer context synthetic; nonempty original handler paths remain outside this boundary proof',
            'R0 preservation is observed, not an original assembly-language or public C API provenance claim',
            'Additional instruction permission exists only in this new read-only measurement engine; frozen inventory/linker stay unchanged']}


def proof():
    pins = verify_inputs()
    names = sorted({Path(__file__).name, PINS.relative_to(ROOT).as_posix()} | {row['path'] for row in pins})
    return {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'generatorSources': [{'path': name, 'sha256': digest((ROOT / name).read_bytes())} for name in names],
        'pinnedInputs': pins, 'romSha256': ROM_SHA, 'boundary': inventory(), 'native': native_evidence(), 'ordinaryCHypothesis': strict_candidate_refusal(),
        'baseLinkerSha256': BASE_LINKER_SHA, 'newAcceptedFunctionOrByteCredit': 0,
        'newExecutableInventoryProposalBytes': 16, 'initializedDenominatorDelta': 0, 'scopeAdopted': False}


def main():
    report = proof()
    write_json(REPORT, report)
    print(json.dumps({'report': REPORT.relative_to(ROOT).as_posix(), 'sha256': digest(REPORT.read_bytes()), 'sourceCredit': 0,
        'nativeCallbackReturns': report['native']['actualOriginalCallbackReturns'], 'strictGuard': report['ordinaryCHypothesis']['reason']}), flush=True)


if __name__ == '__main__':
    main()
