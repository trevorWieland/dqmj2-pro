import re


REG = r"r(?:1[0-2]|[0-9])"
MEMORY = re.compile(r"^(ldr(?:sb|sh|b|h)?|str(?:b|h)?)\s+("+REG+r"),\s*\[("+REG+r")(.*?)\](!?)$")
LITERAL = re.compile(r"^ldr\s+("+REG+r"),\s*(\.L_[0-9a-f]+)$")


def observations(assembly):
    pools = dict(re.findall(r"^(\.L_[0-9a-f]+):\s*\.word\s+(data_[A-Za-z0-9_]+)\s*$", assembly, re.M))
    lines = [line.strip() for line in assembly.splitlines()]
    writes = {}
    for line in lines:
        match = re.match(r"([a-z]+)\s+("+REG+r")\b", line)
        if match and not match[1].startswith(('str', 'stm', 'cmp', 'cmn', 'tst', 'teq')):
            writes.setdefault(match[2], []).append(line)
    stable = {}
    for register, instructions in writes.items():
        if int(register[1:]) not in range(4, 12) or len(instructions) != 1:
            continue
        literal = LITERAL.fullmatch(instructions[0])
        if literal and literal[2] in pools:
            stable[register] = pools[literal[2]]
    state, found = {}, {}
    for line in lines:
        if line.startswith('.L_') and ':' in line:
            state = {register: symbol for register, symbol in state.items() if register in stable}
            continue
        literal = LITERAL.fullmatch(line)
        if literal:
            if literal[2] in pools:
                state[literal[1]] = pools[literal[2]]
            else:
                state.pop(literal[1], None)
            continue
        memory = MEMORY.fullmatch(line)
        if memory:
            opcode, destination, base, offset, writeback = memory.groups()
            if base in state:
                scalar = {'ldrb':'u8', 'ldrsb':'s8', 'ldrh':'u16', 'ldrsh':'s16', 'strb':'u8', 'strh':'u16'}.get(opcode, 'u32')
                size = int(scalar[1:]) // 8
                immediate = re.fullmatch(r'(?:,\s*#(-?(?:0x[0-9a-f]+|[0-9]+)))?', offset)
                indexed = re.fullmatch(r',\s*'+REG+r'(?:,\s*lsl\s*#(0x[0-9a-f]+|[0-9]+))?', offset)
                aligned = bool(immediate and int(immediate[1] or '0', 0) % size == 0)
                aligned |= bool(indexed and (1 << int(indexed[1] or '0', 0)) >= size)
                found.setdefault(state[base], []).append({'instruction':line, 'scalar':scalar, 'aligned':aligned, 'writeback':bool(writeback)})
            if opcode.startswith('ldr'):
                state.pop(destination, None)
            if writeback:
                state.pop(base, None)
            continue
        if re.match(r'blx?\s', line):
            state = {register:symbol for register,symbol in state.items() if int(register[1:]) in range(4, 12)}
            continue
        if re.match(r'b(?:eq|ne|cs|cc|mi|pl|vs|vc|hi|ls|ge|lt|gt|le)?\s', line):
            state = {register:symbol for register,symbol in state.items() if register in stable}
            continue
        match = re.match(r'([a-z]+)\s+('+REG+r')\b', line)
        if match and not match[1].startswith(('str','stm','cmp','cmn','tst','teq')):
            state.pop(match[2], None)
    return found


def apply(context, assembly):
    accepted, rejected = [], []
    for symbol, accesses in observations(assembly).items():
        sizes = {int(row['scalar'][1:]) for row in accesses}
        if len(sizes) != 1 or any(not row['aligned'] or row['writeback'] for row in accesses):
            rejected.append({'symbol':symbol, 'accesses':accesses, 'reason':'mixed widths, unaligned addressing, or writeback'})
            continue
        bits = next(iter(sizes))
        scalar = ('s' if any(row['scalar'].startswith('s') for row in accesses) else 'u') + str(bits)
        declaration = f'extern u8 {symbol}[];'
        if declaration not in context or scalar == 'u8':
            continue
        context = context.replace(declaration, f'extern {scalar} {symbol}[];')
        accepted.append({'symbol':symbol, 'scalar':scalar, 'accesses':accesses, 'evidenceClass':'observed-native-access-width hypothesis', 'wholeObjectExtentProven':False})
    return context, accepted, rejected


def preserve_declarations(source, contexts):
    for row in contexts:
        symbol = row['symbol'].removeprefix('data_')
        source = source.replace(f'extern u8 native_data_{symbol}[];', f'extern {row["scalar"]} native_data_{symbol}[];')
    return source
