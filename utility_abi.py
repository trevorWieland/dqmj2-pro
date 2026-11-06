from capstone import CS_GRP_CALL
from capstone.arm import ARM_OP_IMM, ARM_OP_MEM, ARM_OP_REG


def conditional_definitions(spec, masks):
    definitions = {f"r{index}": set() for index in range(4)}
    needed = 0
    for instruction in spec["instructions"]:
        condition = instruction.cc
        unconditional = condition in (0, 15)
        reads, writes = instruction.regs_access()
        saved = instruction.mnemonic.startswith("push") or instruction.mnemonic.startswith("stmdb") and instruction.op_str.startswith("sp!")
        read_names = set() if saved else {instruction.reg_name(register) for register in reads}
        if instruction.group(CS_GRP_CALL):
            target = instruction.operands[0].imm if instruction.operands and instruction.operands[0].type == ARM_OP_IMM else 0
            read_names.update(name for index, name in enumerate(definitions) if masks.get(target, 15) & 1 << index)
        for index, (name, known) in enumerate(definitions.items()):
            if name in read_names and 15 not in known and (unconditional or condition not in known):
                needed |= 1 << index
        write_names = {instruction.reg_name(register) for register in writes}
        if instruction.group(CS_GRP_CALL):
            write_names.update(definitions)
        for name in write_names & definitions.keys():
            if unconditional:
                definitions[name] = {15}
            else:
                definitions[name].add(condition)
                if ((condition - 1) ^ 1) + 1 in definitions[name]:
                    definitions[name] = {15}
        if instruction.update_flags or "cpsr" in write_names:
            definitions = {name: known if 15 in known else set() for name, known in definitions.items()}
    return needed


def incoming_stack_words(spec):
    delta = 0
    words = 0
    evidence = []
    for instruction in spec["instructions"]:
        if delta is None:
            break
        operands = instruction.operands
        if instruction.mnemonic.startswith("ldr"):
            for operand in operands:
                if operand.type == ARM_OP_MEM and instruction.reg_name(operand.mem.base) == "sp" and not operand.mem.index:
                    offset = delta + operand.mem.disp
                    if offset >= 0 and offset < 256:
                        words = max(words, offset // 4 + 1)
                        evidence.append({"instruction": hex(instruction.address), "entrySpOffset": offset, "slot": 4 + offset // 4})
        unconditional = instruction.cc in (0, 15)
        if instruction.mnemonic.startswith("push") or instruction.mnemonic.startswith("stmdb") and instruction.op_str.startswith("sp!"):
            count = sum(operand.type == ARM_OP_REG for operand in operands) - int(instruction.op_str.startswith("sp!"))
            delta = delta - count * 4 if unconditional else None
        elif instruction.mnemonic.startswith("pop") or instruction.mnemonic.startswith("ldm") and instruction.op_str.startswith("sp!"):
            count = sum(operand.type == ARM_OP_REG for operand in operands) - int(instruction.op_str.startswith("sp!"))
            delta = delta + count * 4 if unconditional else None
        elif len(operands) >= 3 and operands[0].type == ARM_OP_REG and instruction.reg_name(operands[0].reg) == "sp":
            if instruction.mnemonic in ("add", "sub") and operands[1].type == ARM_OP_REG and instruction.reg_name(operands[1].reg) == "sp" and operands[2].type == ARM_OP_IMM and unconditional:
                delta += operands[2].imm * (1 if instruction.mnemonic == "add" else -1)
            else:
                delta = None
        elif len(operands) == 2 and operands[0].type == ARM_OP_REG and instruction.reg_name(operands[0].reg) == "sp" and instruction.mnemonic in ("add", "sub") and operands[1].type == ARM_OP_IMM and unconditional:
            delta += operands[1].imm * (1 if instruction.mnemonic == "add" else -1)
    return words, evidence


def argument_hints(specs, forwarded_targets=None):
    forwarded_targets = forwarded_targets or {}
    masks = {spec["address"]: 0 for spec in specs}
    for _ in range(8):
        next_masks = {spec["address"]: conditional_definitions(spec, masks) for spec in specs}
        for address, target in forwarded_targets.items():
            next_masks[address] = next_masks.get(address, 0) | masks.get(target, 15)
        if next_masks == masks:
            break
        masks = next_masks
    result, stack_evidence = {}, {}
    for spec in specs:
        words, evidence = incoming_stack_words(spec)
        result[spec["address"]] = max(masks[spec["address"]].bit_length(), 4 + words if words else 0)
        if evidence:
            stack_evidence[hex(spec["address"])] = evidence
    for _ in range(8):
        for address, target in forwarded_targets.items():
            result[address] = max(result.get(address, 0), result.get(target, 4))
    return result, stack_evidence
