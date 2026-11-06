import hashlib
import re
from pathlib import Path
from project import ROOT, configuration, read_json, write_json, sha256
from link_runtime_unit import measured_module
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
from capstone.arm import ARM_OP_REG, ARM_OP_MEM, ARM_CC_AL, ARM_CC_INVALID


def prefix_inputs(image, address, mode, size):
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB if mode == 'thumb' else CS_MODE_ARM)
    decoder.detail = True
    raw = image[address - 0x02000000:address - 0x02000000 + min(size, 48)]
    origins = {f'r{index}': {index} for index in range(4)}
    evidence, visited, stop = [], [], 'prefix-limit'
    for instruction in decoder.disasm(raw, address):
        name = instruction.mnemonic
        visited.append(dict(address=hex(instruction.address), mnemonic=name, operands=instruction.op_str))
        if instruction.cc not in [ARM_CC_AL, ARM_CC_INVALID] or name == 'it':
            stop = 'conditional-prefix'
            break
        if name in ['bx', 'pop', 'ldm', 'ldmia'] and ('lr' in instruction.op_str or 'pc' in instruction.op_str):
            stop = 'return-or-indirect-control'
            break
        if name in ['b', 'bl', 'blx', 'bx', 'svc', 'swi', 'bkpt']:
            stop = 'branch-or-system-boundary'
            break
        reads, writes = instruction.regs_access()
        read_names = [instruction.reg_name(register) for register in reads]
        write_names = [instruction.reg_name(register) for register in writes]
        dependencies = set().union(*(origins.get(register, set()) for register in read_names))
        consumed = set()
        kinds = []
        for operand in instruction.operands:
            if operand.type == ARM_OP_MEM:
                for register in [operand.mem.base, operand.mem.index]:
                    consumed.update(origins.get(instruction.reg_name(register), set()))
                kinds.append('memory-address-dependency')
        if name.startswith('str'):
            consumed.update(dependencies)
            kinds.append('stored-value-dependency')
        if name in ['cmp', 'cmn', 'tst', 'teq']:
            consumed.update(dependencies)
            kinds.append('condition-dependency')
        if consumed:
            evidence.append(dict(kind=kinds, inputs=sorted(consumed), instruction=visited[-1]))
        for register in write_names:
            origins[register] = set() if name.startswith(('ldr', 'pop', 'ldm')) else set(dependencies)
        if len(visited) >= 10:
            break
    return dict(physicalInputDependencies=sorted(set().union(*(set(row['inputs']) for row in evidence))),
        evidence=evidence, visitedPrefix=visited, stop=stop,
        targetPrefixSha256=hashlib.sha256(raw).hexdigest(), formalCParametersProven=False)


def main():
    snapshot = ROOT / 'evidence/verification/accepted-cohort105-identities-v2-20261101.json'
    functions = read_json(snapshot)['functions']
    namespace = configuration()
    assert sha256(namespace['rom']) == namespace['romSha256']
    metadata, image, unused = measured_module('main')
    main_functions = [row for row in functions if row['processor'] == 'arm9' and not row.get('program') and row['module'] == 'main']
    targets = {row['address']: row for row in main_functions}
    sources = {}
    for row in main_functions:
        if Path(row['source']).suffix.lower() in ['.c', '.cpp']:
            sources.setdefault(row['source'], []).append(row)
    calls, flagged, excluded = [], [], []
    pattern = re.compile(r'\bnative_fn_([0-9a-fA-F]{8})\s*\(\s*\)')
    for relative, owners in sorted(sources.items()):
        owner = owners[0]
        assert all(row['sourceSha256'] == owner['sourceSha256'] for row in owners)
        path = ROOT / relative
        assert sha256(path) == owner['sourceSha256']
        text = path.read_text(encoding='utf-8')
        for match in pattern.finditer(text):
            start = text.rfind('\n', 0, match.start()) + 1
            line = text[start:text.find('\n', match.end()) if '\n' in text[match.end():] else len(text)]
            if line.lstrip().startswith(('extern ', '#', 'typedef ')):
                continue
            address = int(match.group(1), 16)
            if not 0x02000000 <= address < 0x02000000 + len(image):
                excluded.append(dict(source=relative, target=hex(address), reason='outside-measured-main'))
                continue
            known = targets.get(address)
            mode = known['mode'] if known else 'arm'
            size = known['bytes'] if known else 48
            analysis = prefix_inputs(image, address, mode, size)
            row = dict(processor='arm9', program='', module='main', caller=hex(owner['address']) if len(owners) == 1 else None,
                sourceUnitAcceptedFunctions=[dict(address=hex(x['address']),mode=x['mode'],bytes=x['bytes'])for x in owners],
                source=relative, sourceSha256=sha256(path), line=text.count('\n', 0, match.start()) + 1,
                zeroArgumentCall=match.group(), target=hex(address), targetMode=mode,
                acceptedTargetBoundaryKnown=bool(known), unknownTargetArmModeAssumed=not bool(known),
                cArgumentCount=0, nativePrefixAnalysis=analysis, apiMismatchProven=False)
            calls.append(row)
            if analysis['physicalInputDependencies']:
                flagged.append(row)
    assert any(row['target'] == '0x20850a0' and row['source'] == 'src/runtime/runtime08/native_main_0204a04c.c' for row in flagged)
    assert not any(row['target'] in ['0x203d30c','0x203d320','0x203d334'] for row in flagged)
    report = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__),
        romSha256=namespace['romSha256'], moduleSha256=metadata['sha256'],
        acceptedSnapshot=snapshot.relative_to(ROOT).as_posix(), acceptedSnapshotSha256=sha256(snapshot),
        acceptedSourceFilesInspected=len(sources), zeroArgumentCallsInspected=len(calls),
        potentialPhysicalInputMismatches=len(flagged), flagged=flagged, allInspectedCalls=calls,
        excluded=excluded, sourceCredit=0, acceptedSourceOrRegistryChanged=False,
        limitations=['This conservative straight-line prefix audit identifies review candidates, not proven API defects',
            'Return-register origin alone and stack-save reads are excluded; register copies propagate origins to later address/condition uses',
            'Conditional instructions, calls and unresolved control flow stop prefix analysis',
            'Unknown target mode defaults to an explicitly unverified ARM hypothesis',
            'Function boundaries and native input dependencies still require contextual execution',
            'Only direct native_fn hexadecimal calls with zero visible arguments in accepted105 ARM9 main source are inspected',
            'It does not prove complete argument lists, formal types, stack arguments, indirect calls or portable C correctness'])
    write_json(ROOT / 'evidence/abi/zero-argument-main-audit-20261101.json', report)
    print(dict(sourceFiles=len(sources), calls=len(calls), reviewCandidates=len(flagged), sourceCredit=0))


if __name__ == '__main__':
    main()
