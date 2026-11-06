import hashlib
import re
from project import ROOT, configuration, native_dependencies, read_json, sha256, write_json
native_dependencies(configuration())
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_CC_AL, ARM_INS_B, ARM_INS_POP, ARM_REG_PC
from link_runtime_unit import measured_module

ADDRESS, TAIL, END = 0x0201D470, 0x0201D5CC, 0x0201D5D4


def reachable(instructions):
    decoded = {item.address: item for item in instructions}
    pending, visited, returns = [ADDRESS], set(), []
    while pending:
        address = pending.pop()
        if address in visited:
            continue
        item = decoded[address]
        visited.add(address)
        edges = []
        conditional = item.cc != ARM_CC_AL
        if item.id == ARM_INS_B:
            target = item.operands[0].imm
            assert ADDRESS <= target < END
            edges.append(target)
            if conditional:
                edges.append(address + 4)
        elif item.id == ARM_INS_POP and any(operand.reg == ARM_REG_PC for operand in item.operands):
            returns.append({'address': hex(address), 'conditional': conditional})
            if conditional:
                edges.append(address + 4)
        else:
            edges.append(address + 4)
        for edge in edges:
            assert edge in decoded
        pending.extend(edges)
    return visited, returns


def main():
    metadata, binary, config = measured_module('main')
    base = int(metadata['base'], 0)
    body = binary[ADDRESS - base:END - base]
    assert len(body) == 356
    assert hashlib.sha256(body).hexdigest() == 'b141b23c4db8e2a07817182a4c268a1ac80a7a0a3650b07018f51109b324188e'
    entries = [(int(size, 0), int(address, 0)) for size, address in re.findall(r'^\S+ kind:function\(arm,size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)$', config, re.M)]
    legacy = (348, ADDRESS) in entries and (8, TAIL) in entries
    merged = (356, ADDRESS) in entries and bool(re.search(r'^func_0201d5cc kind:label\(arm\) addr:0x0201d5cc$', config, re.M))
    assert legacy != merged
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    instructions = list(decoder.disasm(body, ADDRESS))
    assert len(instructions) == 89 and all(item.size == 4 for item in instructions)
    visited, returns = reachable(instructions)
    assert TAIL not in visited and TAIL + 4 not in visited
    preceding = instructions[-3]
    assert preceding.id == ARM_INS_B and preceding.cc == ARM_CC_AL
    assert ADDRESS <= preceding.operands[0].imm < TAIL
    assert instructions[-1].id == ARM_INS_POP
    branch_hits = []
    for offset in range(0, len(binary) - 3, 4):
        word = int.from_bytes(binary[offset:offset + 4], 'little')
        if word & 0x0E000000 != 0x0A000000:
            continue
        displacement = (word & 0xFFFFFF) << 2
        if displacement & 0x02000000:
            displacement -= 0x04000000
        if word >> 28 == 15:
            displacement |= (word >> 23) & 2
        target = (base + offset + 8 + displacement) & 0xFFFFFFFF
        if TAIL <= target < END:
            branch_hits.append({'from': hex(base + offset), 'to': hex(target)})
    assert not branch_hits
    pointers = []
    for module in read_json(ROOT / 'provenance/seed-manifest.json')['modules']:
        data = (ROOT / module['binary']).read_bytes()
        for offset in range(0, len(data) - 3, 4):
            word = int.from_bytes(data[offset:offset + 4], 'little')
            if TAIL <= (word & ~1) < END:
                pointers.append({'module': module['name'], 'offset': hex(offset), 'value': hex(word)})
    fixture = read_json(ROOT / 'evidence/functional/main-heap-sort-exact-candidate-20261030.json')
    assert fixture['sourceCredit'] == 0 and fixture['genuineLinkExact356OriginalBytes']
    assert sha256(ROOT / fixture['source']) == fixture['sourceSha256']
    report = {'romSha256': configuration()['romSha256'], 'processor': 'arm9', 'module': 'main', 'mode': 'arm',
              'inputModuleSha256': metadata['sha256'], 'address': hex(ADDRESS), 'combinedBytes': len(body),
              'combinedSha256': hashlib.sha256(body).hexdigest(), 'legacyEntries': [{'address': hex(ADDRESS), 'bytes': 348}, {'address': hex(TAIL), 'bytes': 8}],
              'armInstructions': len(instructions), 'entryReachableInstructions': len(visited),
              'unreachableInstructions': [hex(item.address) for item in instructions if item.address not in visited],
              'conditionalAndUnconditionalReturns': returns, 'mainAlignedImmediateBranchesIntoTail': branch_hits,
              'arm9InitializedAlignedPointerCandidatesIntoTail': pointers,
              'exactCandidateEvidence': 'evidence/functional/main-heap-sort-exact-candidate-20261030.json',
              'exactCandidateEvidenceSha256': sha256(ROOT / 'evidence/functional/main-heap-sort-exact-candidate-20261030.json'),
              'normalEntryActualReturns': fixture['actualOriginalAndSourceReturns'],
              'configsOrAcceptedSourcesChanged': False, 'sourceCredit': 0,
              'review': 'Compiler-owned unreachable epilogue within the full 356-byte C function; retain tail identity as a fragment during migration',
              'limitations': ['Normal callback returns are assumed in the static CFG',
                  'Unaligned pointers, computed targets, Thumb calls and nonstandard indirect continuations are not universally excluded',
                  'Pointer-word candidates require instruction/data role review if present',
                  'Boundary migration and registered source acceptance are separate from this review']}
    write_json(ROOT / 'evidence/attempts/main-heap-sort-exact-boundary-review-20261030.json', report)
    print({'instructions': len(instructions), 'reachable': len(visited), 'tailReachable': TAIL in visited,
           'pointerCandidates': len(pointers), 'configChanged': False, 'sourceCredit': 0})


if __name__ == '__main__':
    main()
