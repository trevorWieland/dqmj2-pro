import hashlib
import re
import struct
from project import ROOT, configuration, native_dependencies, now, write_json
from ledger_state import collect_matches
from link_runtime_unit import measured_module


TARGETS = [('ov001', 0x021e49d0), ('ov001', 0x021e485c), ('ov001', 0x021e4c34),
           ('ov001', 0x021fbe70), ('ov001', 0x022095f4), ('ov000', 0x02229100),
           ('ov000', 0x0222900c), ('main', 0x02076d70), ('main', 0x02062f3c),
           ('main', 0x02078978), ('main', 0x0207aebc)]


def functions(config):
    pattern = r'^(\S+) kind:function\((arm|thumb),size=0x([0-9a-f]+)[^)]*\) addr:0x([0-9a-f]+)$'
    return [{'name': name, 'mode': mode, 'bytes': int(size, 16), 'address': int(address, 16)}
            for name, mode, size, address in re.findall(pattern, config, re.M)]


def main():
    native_dependencies(configuration())
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
    from capstone.arm import ARM_OP_IMM, ARM_OP_MEM, ARM_REG_PC, ARM_INS_B, ARM_INS_BL, ARM_INS_BLX, ARM_INS_LDR
    known, rejected = collect_matches(configuration()['romSha256'])
    modules = {name: measured_module(name) for name in ['main', 'ov000', 'ov001']}
    incoming, outgoing, literals, nodes = [], [], [], []
    for module, (metadata, binary, config) in modules.items():
        base = int(metadata['base'], 0)
        decoders = {'arm': Cs(CS_ARCH_ARM, CS_MODE_ARM), 'thumb': Cs(CS_ARCH_ARM, CS_MODE_THUMB)}
        for decoder in decoders.values():
            decoder.detail = True
        for function in functions(config):
            address, mode, size = function['address'], function['mode'], function['bytes']
            offset = address - base
            code = binary[offset:offset + size]
            requested = (module, address) in TARGETS
            if requested:
                matched = known.get((module, mode, address), {})
                nodes.append({'processor': 'arm9', 'module': module, 'moduleInputSha256': metadata['sha256'],
                              'address': hex(address), 'mode': mode, 'bytes': size,
                              'nativeSpanSha256': hashlib.sha256(code).hexdigest(),
                              'matchedSource': matched.get('source'), 'signatureVerified': False})
            for instruction in decoders[mode].disasm(code, address):
                identity = {'processor': 'arm9', 'sourceModule': module, 'sourceModuleSha256': metadata['sha256'],
                            'sourceFunction': hex(address), 'sourceFunctionBytes': size, 'sourceMode': mode,
                            'address': hex(instruction.address), 'instructionBytes': instruction.bytes.hex(),
                            'mnemonic': instruction.mnemonic, 'operands': instruction.op_str}
                if instruction.id in (ARM_INS_B, ARM_INS_BL, ARM_INS_BLX):
                    if len(instruction.operands) == 1 and instruction.operands[0].type == ARM_OP_IMM:
                        target = instruction.operands[0].imm & ~1
                        target_modules = [name for name, point in TARGETS if point == target and (module == name or name == 'main' or module == 'main')]
                        if target_modules:
                            incoming.append({**identity, 'targetAddress': hex(target), 'targetModuleCandidates': target_modules,
                                             'overlayContextProven': module != 'main' or target_modules == ['main']})
                        if requested:
                            outgoing.append({**identity, 'targetAddress': hex(target),
                                             'targetModule': 'main' if target < 0x021d7240 else module})
                if instruction.id == ARM_INS_LDR and len(instruction.operands) >= 2:
                    operand = instruction.operands[1]
                    if operand.type == ARM_OP_MEM and operand.mem.base == ARM_REG_PC:
                        pc = instruction.address + 8 if mode == 'arm' else (instruction.address + 4) & ~3
                        literal = pc + operand.mem.disp - base
                        if 0 <= literal <= len(binary) - 4 and struct.unpack_from('<I', binary, literal)[0] == 0x020f6044:
                            literals.append({**identity, 'globalAddress': '0x20f6044', 'literalAddress': hex(base + literal),
                                             'accessRole': 'literal pointer load; read/write and lifecycle meaning require tracing'})
    report = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
              'targets': nodes, 'incomingDirectBranches': incoming, 'outgoingDirectBranches': outgoing,
              'rngLiteralReferences': literals, 'sourceCredit': 0,
              'limitations': ['Direct branches do not establish ordinary scene reachability or state initialization',
                              'Indirect dispatch, computed address references and unrecognized instruction/data boundaries remain unresolved',
                              'Main-to-overlay numeric targets require loaded-overlay context; module identities are never inferred from an address alone']}
    write_json(ROOT / 'evidence/application/native-entry-traces-20261029.json', report)
    print({'targetBoundaries': len(nodes), 'incomingBranches': len(incoming), 'rngLiteralReferences': len(literals), 'sourceCredit': 0})


if __name__ == '__main__':
    main()
