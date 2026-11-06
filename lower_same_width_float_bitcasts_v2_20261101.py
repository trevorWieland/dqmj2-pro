import re

PREFIX = ('typedef union { float value; int word; unsigned int unsigned_word; } J2pReinterpret32;\n'
    'typedef char J2pReinterpret32WidthCheck[(sizeof(float) == 4 && sizeof(int) == 4 && sizeof(unsigned int) == 4) ? 1 : -1];\n')
MACRO = re.compile(r'\bM2C_BITWISE\s*\(')
NONCODE = re.compile(r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', re.S)


def code_mask(text):
    return NONCODE.sub(lambda match: ' ' * len(match.group()), text)


def closing(text, opening):
    text = code_mask(text)
    depth = 0
    for index in range(opening, len(text)):
        char = text[index]
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
            if depth == 0:
                return index
    raise ValueError('Unbalanced reinterpret expression')


def unwrap(expression):
    expression = expression.strip()
    while expression.startswith('(') and closing(expression, 0) == len(expression) - 1:
        expression = expression[1:-1].strip()
    return expression


def macro_arguments(expression):
    opening = expression.index('(')
    end = closing(expression, opening)
    if end != len(expression) - 1:
        raise ValueError('Reinterpret macro is not a complete expression')
    content = expression[opening + 1:end]
    match = re.match(r'\s*([A-Za-z_]\w*)\s*,', content)
    if not match:
        raise ValueError('Unsupported reinterpret target syntax')
    return match.group(1), content[match.end():].strip()


def infer_type(expression, function_returns, variables):
    expression = unwrap(expression)
    if MACRO.match(expression):
        return macro_arguments(expression)[0]
    cast = re.match(r'^\(\s*(f32|s32|u32|f64|s64|u64)\s*\)', expression)
    if cast:
        return cast.group(1)
    call = re.match(r'^([A-Za-z_]\w*)\s*\(', expression)
    if call and closing(expression, expression.index('(')) == len(expression) - 1:
        name = call.group(1)
        if name not in function_returns:
            raise ValueError('No explicitly supplied return type for reinterpret operand: ' + name)
        return function_returns[name]
    if re.fullmatch(r'[A-Za-z_]\w*', expression) and expression in variables:
        return variables[expression]
    raise ValueError('Reinterpret operand width/type is not explicit: ' + expression)


def lower(text, function_returns, variable_types=None):
    if 'J2pReinterpret32' in text:
        raise ValueError('Reserved reinterpret type name is already present')
    variables = dict(variable_types or {})
    for kind, name in re.findall(r'\b(f32|s32|u32|f64|s64|u64)\s+([A-Za-z_]\w*)\s*(?=[;,=)])', code_mask(text)):
        if name in variables and variables[name] != kind:
            raise ValueError('Conflicting local operand type: ' + name)
        variables[name] = kind
    records = []
    def fragment(value):
        parts, position = [], 0
        while True:
            match = MACRO.search(code_mask(value), position)
            if not match:
                parts.append(value[position:])
                return ''.join(parts)
            opening = value.index('(', match.start())
            end = closing(value, opening)
            original = value[match.start():end + 1]
            destination, operand = macro_arguments(original)
            source = infer_type(operand, function_returns, variables)
            if (source, destination) not in [('f32', 's32'), ('s32', 'f32'), ('f32', 'u32'), ('u32', 'f32')]:
                raise ValueError('Only explicit equal-width f32/s32/u32 reinterpretation is supported: ' + source + ' -> ' + destination)
            inner = unwrap(operand)
            if MACRO.match(inner):
                inner_destination, inner_operand = macro_arguments(inner)
                inner_source = infer_type(inner_operand, function_returns, variables)
            else:
                inner_destination, inner_source = None, None
            if inner_destination == source and inner_source == destination:
                replacement = '(' + fragment(inner_operand) + ')'
                kind, count = 'inverse-pair-cancelled', 2
            else:
                rewritten = fragment(operand)
                input_member = 'value' if source == 'f32' else 'word' if source == 's32' else 'unsigned_word'
                output_member = 'value' if destination == 'f32' else 'word' if destination == 's32' else 'unsigned_word'
                replacement = '((J2pReinterpret32){ .' + input_member + ' = (' + rewritten + ') }).' + output_member
                kind, count = 'union-reinterpret', 1
            records.append(dict(sourceType=source, destinationType=destination, original=original,
                replacement=replacement, kind=kind, originalCastCount=count))
            parts.extend([value[position:match.start()], replacement])
            position = end + 1
    result = fragment(text)
    if any(record['kind'] == 'union-reinterpret' for record in records):
        result = PREFIX + result
    return result, records
