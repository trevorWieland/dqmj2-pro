from capstone import CS_GRP_CALL
from capstone.arm import ARM_OP_IMM, ARM_OP_MEM, ARM_OP_REG, ARM_REG_PC
from functools import lru_cache
import re
import utility_runtime


@lru_cache(maxsize=1)
def runtime_allocations():
    return utility_runtime.derive()[0]["modules"]


def fixed_work_area(spec, address):
    return 0x02000000 <= address < 0x08000000 and not any(module["processor"] == spec["processor"] and
        int(module["base"], 0) <= address < int(module["runtimeEnd"], 0) for module in runtime_allocations())


def fixed_references(text, spec):
    references = []
    pattern = r"^#define (native_utility_child_(arm7|arm9)_data_[0-9a-f]{8}) \(\(volatile (u8|u16|u32) \*\)(0x[0-9a-f]+)\)$"
    for match in re.finditer(pattern, text, re.M):
        name, processor, scalar, target = match.groups()
        address = int(target, 0)
        if processor != spec["processor"] or not fixed_work_area(spec, address):
            raise ValueError("Typed fixed-area C reference escapes the declared CPU allocation scope")
        references.append({"symbol": name, "address": hex(address), "scalarBytes": int(scalar[1:]) // 8,
                           "sourceForm": "typed volatile C pointer to measured fixed address outside this CPU's initialized/BSS modules",
                           "program": utility_runtime.PROGRAM, "processor": processor, "moduleAllocation": "outside canonical initialized and BSS ranges"})
    return references


def scalar_arrays(spec, data):
    values = set(data.values())
    aliases, accesses = {}, {value: set() for value in values}
    for instruction in spec["instructions"]:
        operands = instruction.operands
        before = dict(aliases)
        for operand in operands:
            if operand.type == ARM_OP_MEM and operand.mem.base in before and not operand.mem.index:
                target, offset = before[operand.mem.base]
                access = instruction.mnemonic
                width = 1 if access.startswith(("ldrb", "ldrsb", "strb")) else 2 if access.startswith(("ldrh", "ldrsh", "strh")) else 4
                accesses[target].add((offset + operand.mem.disp, width))
        _, writes = instruction.regs_access()
        for register in writes:
            aliases.pop(register, None)
        if instruction.group(CS_GRP_CALL):
            aliases = {register: value for register, value in aliases.items() if instruction.reg_name(register) not in ("r0", "r1", "r2", "r3", "ip")}
        if instruction.cc not in (0, 15):
            continue
        if len(operands) == 2 and instruction.mnemonic == "ldr" and operands[0].type == ARM_OP_REG and operands[1].type == ARM_OP_MEM and operands[1].mem.base == ARM_REG_PC:
            location = ((instruction.address + 4) & ~3 if spec["mode"] == "thumb" else instruction.address + 8) + operands[1].mem.disp
            target = spec["pools"].get(location)
            if target in values:
                aliases[operands[0].reg] = (target, 0)
        elif len(operands) == 2 and instruction.mnemonic in ("mov", "movs") and operands[0].type == ARM_OP_REG and operands[1].type == ARM_OP_REG and operands[1].reg in before:
            aliases[operands[0].reg] = before[operands[1].reg]
        elif len(operands) == 3 and instruction.mnemonic in ("add", "sub") and operands[0].type == ARM_OP_REG and operands[1].type == ARM_OP_REG and operands[2].type == ARM_OP_IMM and operands[1].reg in before:
            target, offset = before[operands[1].reg]
            aliases[operands[0].reg] = (target, offset + operands[2].imm * (1 if instruction.mnemonic == "add" else -1))
    return {label: f"u{next(iter(accesses[target]))[1] * 8}" if len(accesses[target]) == 1 and next(iter(accesses[target]))[0] == 0 else "u8"
            for label, target in data.items()}
