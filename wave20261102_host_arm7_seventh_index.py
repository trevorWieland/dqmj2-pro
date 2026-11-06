import json
import struct
import hashlib
import match_arm7
import arm7_runtime
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
from capstone.arm import ARM_OP_MEM, ARM_REG_PC
from project import ROOT, sha256


def layout():
    return arm7_runtime.derive((ROOT / 'extract/arm7/arm7.bin').read_bytes())


def candidates():
    image = (ROOT / 'extract/arm7/arm7.bin').read_bytes()
    modules = {r['id']: r for r in arm7_runtime.derive(image)['modules']}
    inventory = json.loads((ROOT / 'evidence/arm7/ghidra-runtime-inventory.json').read_text())
    if not inventory.get('runtimeMappingCanonical') or inventory['sha256'] != arm7_runtime.IMAGE_HASH:
        raise ValueError('Host ARM7 inventory uses a different original runtime image')
    entries = {int(r['address'], 0) for r in inventory['functions']}
    result = []
    for function in inventory['functions']:
        if len(function['ranges']) != 1 or function['bodyBytes'] < 2:
            continue
        module = modules[function['module']]
        raw = image[module['inputFileOffset']:module['inputFileOffset'] + module['bytes']]
        base, address = int(module['base'], 0), int(function['address'], 0)
        first, end = [int(x, 0) for x in function['ranges'][0]]
        if first != address:
            continue
        decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB if function['mode'] == 'thumb' else CS_MODE_ARM)
        decoder.detail = True
        instructions = list(decoder.disasm(raw[first - base:end - base], first))
        if sum(i.size for i in instructions) != end - first:
            continue
        pools = {}
        for instruction in instructions:
            for operand in instruction.operands:
                if operand.type == ARM_OP_MEM and operand.mem.base == ARM_REG_PC:
                    at = ((instruction.address + 4) & ~3 if function['mode'] == 'thumb' else instruction.address + 8) + operand.mem.disp
                    if not address <= at <= base + len(raw) - 4:
                        break
                    pools[at] = struct.unpack_from('<I', raw, at - base)[0]
                    end = max(end, at + 4)
        if any(address < entry < end for entry in entries) or end > base + len(raw):
            continue
        result.append(dict(program='', processor='arm7', module=module['id'], mode=function['mode'], address=address,
            base=base, bytes=end - address, binary=module['binary'], inputModuleSha256=module['sha256'],
            instructions=instructions, pools=pools, name='native_host_' + module['id'].replace('-', '_') + '_%08x' % address))
    return result


def accepted_spec(entry):
    spec = match_arm7.accepted_spec(entry, instructions=True)
    spec.update(program='', name=entry['name'])
    return spec


def mandatory_inputs():
    return [dict(path=name, sha256=sha256(ROOT / name)) for name in ['evidence/arm7/ghidra-runtime-inventory.json', 'project.json']]
