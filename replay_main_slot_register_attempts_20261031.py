from project import ROOT, read_json, write_json, sha256
import match_runtime as compiler
from recover_linked_runtime import qualified_bindings
from link_runtime_unit import validate, measured_module

BASE = ROOT / 'nonmatching/main-runtime/20261031-slot-register'
WORK = ROOT / 'work/main-slot-register-20261031'
INPUT = ROOT / 'nonmatching/main-runtime/20261031-word-inputs270/seeded/func_02015c70.c'
INPUT_HASH = '297ef8adf3dc277ad03c86f8a1b8a8fc7471d742199670a910ec35a36a16bbeb'


def attempt(name, body):
    path = BASE / name / 'native_main_02015c70.c'
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != body.encode():
        raise ValueError('Earlier source experiment differs: ' + name)
    path.write_bytes(body.encode())
    compiler.WORK = WORK / name
    rows, unused = compiler.compare(path, 'main', 2, 'off', True)
    return rows


def counter_sources(base):
    result = {}
    old = 'M2C_FIELD((native_data_020ec36c + temp_r6), u8 *, 0x1D1F) = (u8) *native_data_020e68a4;'
    if old not in base:
        raise ValueError('Expected generation-byte assignment absent')
    replacement = 'generation = *native_data_020e68a4;\n        M2C_FIELD((native_data_020ec36c + temp_r6), u8 *, 0x1D1F) = generation;'
    for kind in ['u8', 'u32']:
        text = base.replace('    u8 var_r4;', f'    {kind} generation;\n    u8 var_r4;')
        text = text.replace(old, replacement)
        text = text.replace('*native_data_020e68a4 += 1;', '*native_data_020e68a4 = generation + 1;')
        result[f'cached-{kind}'] = text
    return result


def order_sources(base):
    block = base[base.index('    s32 temp_r2;'):base.index('\n\n    var_r4')]
    declarations = block.splitlines()
    orders = [declarations[:]]
    for index in range(len(declarations)):
        orders.append([declarations[index]] + declarations[:index] + declarations[index + 1:])
        orders.append(declarations[:index] + declarations[index + 1:] + [declarations[index]])
    result, seen = {}, set()
    for index, order in enumerate(orders):
        if tuple(order) in seen:
            continue
        seen.add(tuple(order))
        result[f'order-{index:02}'] = base.replace(block, '\n'.join(order))
    return result


def record_sources(base):
    result = {}
    for kind in ['u32', 's32', 'void *', 'u8 *']:
        for place in ['first', 'last', 'before-inputs']:
            declaration = f'    {kind} first_record;\n    {kind} second_record;\n'
            if place == 'first':
                text = base.replace('    u8 var_r4;', declaration + '    u8 var_r4;')
            elif place == 'last':
                text = base.replace('    void *temp_r9;', '    void *temp_r9;\n' + declaration.rstrip())
            else:
                text = base.replace('    u32 temp_r5;', declaration + '    u32 temp_r5;')
            for offset, member in [('0x1E8', 'first'), ('0x258', 'second')]:
                field = '0x1D54' if member == 'first' else '0x1D58'
                old = f'        M2C_FIELD((native_data_020ec36c + temp_r6), s32 *, {field}) = (s32) (arg1 + {offset});'
                new = f'        {member}_record = ({kind}) (arg1 + {offset});\n        M2C_FIELD((native_data_020ec36c + temp_r6), s32 *, {field}) = (s32) {member}_record;'
                text = text.replace(old, new)
            result['record-' + kind.replace(' *', '-ptr') + '-' + place] = text
    text = result['record-u32-first']
    line = '        second_record = (u32) (arg1 + 0x258);\n'
    result['overlapping-record-lifetimes'] = text.replace(line, '').replace(
        '        M2C_FIELD((native_data_020ec36c + temp_r6), s32 *, 0x1D54)',
        line + '        M2C_FIELD((native_data_020ec36c + temp_r6), s32 *, 0x1D54)')
    return result


def other_sources(base):
    result = {}
    for global_type in ['u32', 'u8 *', 'void *']:
        for arg_type in ['u32', 'u8 *', 'void *']:
            if global_type == arg_type == 'u32':
                continue
            label = global_type.replace(' *', '-ptr') + '-' + arg_type.replace(' *', '-ptr')
            text = base.replace('extern u32 native_data_020ec36c;', f'extern {global_type} native_data_020ec36c;')
            text = text.replace('native_main_02015c70(u32 arg0, u32 arg1)', f'native_main_02015c70({arg_type} arg0, {arg_type} arg1)')
            result['pointers-' + label] = text
    for kind in ['u32', 's32']:
        for counter in ['u8', 'u32']:
            text = base.replace('    u8 var_r4;', f'    {kind} var_r4;')
            result[f'index-{kind}-{counter}'] = text.replace('    u8 generation;', f'    {counter} generation;')
    return result


def main():
    if sha256(INPUT) != INPUT_HASH:
        raise ValueError('Frozen seeded input differs')
    original = INPUT.read_text(encoding='utf-8')
    word = original.replace('extern u8 native_data_020ec36c[];', 'extern u32 native_data_020ec36c;')
    word = word.replace('*native_data_020ec36c', 'native_data_020ec36c')
    variants = {'word-global': word}
    variants.update(counter_sources(word))
    variants.update(order_sources(variants['cached-u8']))
    variants.update(record_sources(variants['order-09']))
    variants.update(other_sources(variants['order-09']))
    rows = []
    for name, body in variants.items():
        rows.extend(attempt(name, body))
    compiled = [r for r in rows if 'matchingBytes' in r]
    best = max(compiled, key=lambda row: row['matchingBytes'])
    directory = WORK / 'linked-nearest'
    try:
        validate(best, qualified_bindings(best), directory)
    except ValueError as error:
        error_text = str(error)
    else:
        raise ValueError('Unexpected exact result requires independent source review')
    unused, target, unused = measured_module('main')
    linked = (directory / 'caller.bin').read_bytes()
    native = target[0x15c70:0x15c70 + 656]
    differences = [dict(address=hex(0x2015c70 + i), original=native[i:i + 4].hex(),
                        compiled=linked[i:i + 4].hex())
                   for i in range(0, 656, 4) if native[i:i + 4] != linked[i:i + 4]]
    report = dict(input=dict(path=INPUT.relative_to(ROOT).as_posix(), sha256=INPUT_HASH),
                  matches=rows, variants=len(variants), compiled=len(compiled),
                  bestSource=best['source'], matchingBytes=best['matchingBytes'], nativeBytes=656,
                  genuineLink=dict(accepted=False, error=error_text, differences=differences),
                  sourceCredit=0, registered=False, nativeExecutionCount=0,
                  limitations=['Global word/byte-generation observations are local to this function',
                               'Pointer types, SDK meanings and whole-function behavior remain unproved'])
    write_json(ROOT / 'evidence/attempts/main-slot-register-consolidated-20261031.json', report)
    print({key: report[key] for key in ['variants', 'compiled', 'matchingBytes', 'sourceCredit']})


if __name__ == '__main__':
    main()
