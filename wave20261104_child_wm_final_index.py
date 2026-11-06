import json
import struct
import utility_code
import utility_runtime
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
from capstone.arm import ARM_OP_MEM, ARM_REG_PC
from project import ROOT, sha256


def candidates():
    layout, files = utility_runtime.derive()
    path = ROOT / 'evidence/utility/ghidra-arm7.json'
    inventory = json.loads(path.read_text())
    if inventory.get('processor') != 'arm7' or inventory.get('program') != utility_runtime.PROGRAM:
        raise ValueError('Original ARM7 inventory CPU/program differs')
    modules = {m['id']: m for m in layout['modules'] if m['processor'] == 'arm7'}
    entries = {int(f['address'], 0) for f in inventory['functions']}
    rows = []
    for function in inventory['functions']:
        if len(function['ranges']) != 1 or function['bodyBytes'] < 2:
            continue
        module = modules[function['module']]
        raw = bytes(files[ROOT / module['binary']])
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
        if any(address < entry < end for entry in entries):
            continue
        rows.append(dict(module=module['id'], program=utility_runtime.PROGRAM, processor='arm7', mode=function['mode'],
            address=address, base=base, bytes=end - address, binary=module['binary'], inputModuleSha256=module['sha256'],
            instructions=instructions, pools=pools, name='native_' + module['id'].replace('-', '_') + '_%08x' % address))
    return rows


def mandatory_inputs():
    return [dict(path=name, sha256=sha256(ROOT / name)) for name in ['evidence/utility/ghidra-arm7.json', 'project.json']]
