import hashlib
import itertools
import struct
from project import ROOT, configuration, native_dependencies, now, write_json
from ledger_state import collect_matches
from link_runtime_unit import measured_module
from recover_linked_runtime import replay_entry


def main():
    native_dependencies(configuration())
    from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
    from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
    from capstone.arm import ARM_OP_MEM, ARM_REG_PC
    metadata, main_binary, config = measured_module('main')
    overlay, overlay_binary, symbols = measured_module('ov001')
    known, rejected = collect_matches(configuration()['romSha256'])
    rebuilt, proofs = {}, []
    for address in [0x021e4ac4, 0x021e4afc]:
        old = known[('ov001', 'arm', address)]
        entry = replay_entry({**old, 'address': hex(address), 'bytes': old['size']}, 'application-stock-guards-20261029')
        rebuilt[address] = (ROOT / entry['isolatedCallerBinary']).read_bytes()
        proofs.append({key: entry[key] for key in ['address', 'source', 'sourceSha256', 'objectSha256', 'isolatedCallerLinkSnapshotManifest']})
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    def literal(getter, size):
        values = []
        for instruction in decoder.disasm(main_binary[getter - 0x02000000:getter - 0x02000000 + size], getter):
            if len(instruction.operands) > 1:
                operand = instruction.operands[1]
                if operand.type == ARM_OP_MEM and operand.mem.base == ARM_REG_PC:
                    offset = instruction.address + 8 + operand.mem.disp - 0x02000000
                    values.append(struct.unpack_from('<I', main_binary, offset)[0])
        if len(values) != 1:
            raise ValueError('Getter no longer has one measured literal base')
        return values[0]
    active_base, reserve_base, records = literal(0x02062a68, 16), literal(0x02062a78, 16), literal(0x02062b00, 12)
    layouts = [(0, 0, 0), (17, 0, 0), (0, 17, 0), (0, 0, 17), (17, 17, 17), (8, 9, 10)]
    results = []
    for identity, active, reserve, byte33 in itertools.product([0, 17], layouts, layouts, [0, 1, 2, 127, 128, 255]):
        expected = identity != 0 and identity not in active and identity not in reserve and byte33 == 0
        pair = []
        for compiled in [False, True]:
            engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
            engine.mem_map(0x02000000, 0x800000)
            engine.mem_write(0x02000000, main_binary)
            engine.mem_write(int(overlay['base'], 0), overlay_binary)
            if compiled:
                for address, code in rebuilt.items():
                    engine.mem_write(address, code)
            engine.mem_write(active_base, struct.pack('<3I', *active))
            engine.mem_write(reserve_base, struct.pack('<3I', *reserve))
            engine.mem_write(records + 0x14, struct.pack('<I', identity))
            engine.mem_write(records + 0x33, bytes([byte33]))
            engine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            engine.reg_write(UC_ARM_REG_LR, 0x027ff800)
            writes, reads, visited = [], [], []
            engine.hook_add(UC_HOOK_MEM_READ, lambda uc, access, address, size, value, user: reads.append((address, size)))
            engine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, user: writes.append((address, size, value)))
            def stop(uc, pc, size, user):
                visited.append(pc)
                if pc in (0x021e4c88, 0x021e4e7c):
                    uc.emu_stop()
            engine.hook_add(UC_HOOK_CODE, stop)
            engine.emu_start(0x021e4c34, 0x027ff800, count=2000)
            pc = engine.reg_read(UC_ARM_REG_PC)
            if pc not in (0x021e4c88, 0x021e4e7c) or (pc == 0x021e4c88) != expected:
                raise ValueError('Native stock guard decision or termination differs')
            byte_read = (records + 0x33, 1) in reads
            if byte_read != (identity != 0 and identity not in active and identity not in reserve):
                raise ValueError('Conditional record-byte read differs')
            if any(not 0x027f0000 <= address < 0x02800000 for address, size, value in writes):
                raise ValueError('Guard changed persistent state')
            state = {'boundary': hex(pc), 'byte33Read': byte_read, 'reads': reads, 'writes': writes,
                     'persistentSha256': hashlib.sha256(bytes(engine.mem_read(0x021bd51c, 0x39d8))).hexdigest()}
            pair.append(state)
        if pair[0] != pair[1]:
            raise ValueError('Recompiled membership helpers changed the stock guard')
        results.append({'identity': identity, 'active': active, 'reserve': reserve, 'recordOffset0x33': byte33,
                        'awardBodyReached': expected, 'recordByteRead': pair[0]['byte33Read']})
    report = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
              'processor': 'arm9', 'module': 'ov001', 'mode': 'arm', 'moduleInputSha256': overlay['sha256'],
              'entry': '0x21e4c34', 'activeMembershipEntry': '0x21e4ac4', 'reserveMembershipEntry': '0x21e4afc',
              'functionBytes': 636, 'nativeSpanSha256': hashlib.sha256(overlay_binary[0x021e4c34 - int(overlay['base'], 0):0x021e4eb0 - int(overlay['base'], 0)]).hexdigest(),
              'activeArray': hex(active_base), 'reserveArray': hex(reserve_base), 'recordArray': hex(records),
              'recordFieldOffset': '0x33', 'recordFieldDecimalOffset': 51, 'recordFieldWidth': 1,
              'vectors': len(results), 'freshExecutions': len(results) * 2, 'actualRoutineReturns': 0,
              'verifiedGuardBoundaryExecutions': len(results) * 2, 'matchingMembershipSources': proofs,
              'predicate': 'id != 0 and id absent from active and reserve triplets and record[0x33] == 0',
              'results': results, 'newSourceCredit': 0,
              'limitations': ['Stops at measured guard/skip boundaries; does not execute full reward or claim full-routine return',
                              'Only the two already matched membership helpers are replaced with reconstructed source',
                              'Field0x33 gameplay meaning and writer lifecycle remain unproved; do not treat it as decimal offset33',
                              'Synthetic formations do not establish scene initialization, ordinary encounter reachability or reward timing']}
    write_json(ROOT / 'evidence/application/stock-reward-guards-20261029.json', report)
    print({'vectors': len(results), 'guardBoundaryExecutions': len(results) * 2, 'actualRoutineReturns': 0, 'newSourceCredit': 0})


if __name__ == '__main__':
    main()
