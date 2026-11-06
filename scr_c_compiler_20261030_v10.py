import argparse
import hashlib
import json
import re
import struct
from pathlib import Path
import scr_c_compiler_20261029 as core

assert hashlib.sha256(Path(core.__file__).read_bytes()).hexdigest() == '8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935'


def word(value):
    return struct.unpack('<I', struct.pack('<f', value))[0]


def compile_source(source_path, base, allocation):
    source = Path(source_path).resolve()
    if type(base) is not int or not 0 <= base < 0x80000000 or base % 4:
        raise ValueError('Invalid runtime-loop placement')
    text = source.read_text(encoding='utf-8')
    include = re.match(r'\s*#include\s+"([^"\r\n]+)"\s*\n', text)
    if include is None:
        raise ValueError('One runtime-loop ABI include required')
    header = (source.parent / include[1]).resolve()
    header.relative_to(source.parent)
    header_text = header.read_text(encoding='utf-8')
    directives = [line.strip() for line in header_text.splitlines() if line.lstrip().startswith('#')]
    if directives != ['#ifndef SCR_RUNTIME_FLAGS_20261030', '#define SCR_RUNTIME_FLAGS_20261030', '#endif']:
        raise ValueError('Runtime-loop ABI preprocessing')
    if core.tokens('\n'.join(line for line in header_text.splitlines() if not line.startswith('#'))) != core.HEADER:
        raise ValueError('Runtime-loop primary setter ABI')
    name, ast = core.Parser(core.tokens(text[include.end():])).function()
    core.validate_ast(ast, {'false', 'true'})
    if len(ast) != 1 or ast[0][0] != 'for':
        raise ValueError('One constant-bounded ordinary C for loop required')
    loop = ast[0]
    variable, start_expr, condition, body = loop[1:]
    start = core.evaluate(start_expr, {'false': 0, 'true': 1})
    if condition[0:2] != ('binary', '<') or condition[2] != ('variable', variable):
        raise ValueError('Runtime loop requires counter < constant upper bound')
    end = core.evaluate(condition[3], {'false': 0, 'true': 1})
    if not 0 <= start < end <= 1536:
        raise ValueError('Only nonempty finite primary-index loops are supported')
    if len(body) != 1 or body[0][0:2] != ('call', 'set_primary_flag') or len(body[0][2]) != 2:
        raise ValueError('Runtime loop body must be one named primary setter')
    if body[0][2][0] != ('variable', variable):
        raise ValueError('Primary setter index must be the loop counter')
    enabled = core.evaluate(body[0][2][1], {'false': 0, 'true': 1})
    if enabled not in (0, 1):
        raise ValueError('Runtime-loop Boolean setter value')
    if not isinstance(allocation, dict) or set(allocation) != {variable} or type(allocation[variable]) is not int or not 0 <= allocation[variable] < 256:
        raise ValueError('Exactly one valid named runtime counter allocation required')
    slot = allocation[variable]
    code, fixups = bytearray(), []
    def emit(*values):
        offset = len(code)
        code.extend(struct.pack('<' + 'I' * len(values), *values))
        return offset
    def bind(offset, target, kind):
        struct.pack_into('<I', code, offset + 8, target)
        fixups.append({'sitePc': base + offset, 'targetPc': target, 'kind': kind})
    entry = emit(1036, 12, 0)
    bind(entry, base + len(code), 'entry-to-initialization')
    emit(1045, 24, 0, word(slot), 2, word(start))
    emit(1024, 8)
    loop_entry = base + len(code)
    body_jump = emit(1036, 12, 0)
    bind(body_jump, base + len(code), 'loop-entry-to-body')
    emit(1045, 24, 1, word(0), 0, word(slot))
    emit(1045, 24, 1, word(1), 2, word(enabled))
    emit(42, 8)
    emit(1046, 32, 0, word(slot), 0, word(slot), 2, word(1))
    emit(1044, 24, 2, word(end), 0, word(slot))
    condition_branch = emit(1038, 12, 0)
    exit_jump = emit(1036, 12, 0)
    compiler_join = emit(1036, 12, 0)
    back_pc = base + len(code)
    bind(condition_branch, back_pc, 'continue-while-counter-below-bound')
    bind(compiler_join, back_pc, 'unreachable-join-after-exit')
    emit(1036, 12, loop_entry)
    return_pc = base + len(code)
    bind(exit_jump, return_pc, 'loop-exit-to-private-return')
    emit(1026)
    if base + len(code) >= 0x80000000:
        raise ValueError('Runtime-loop function overflow')
    output = bytes(code)
    return output, {'backend': 'restricted-C99-constant-bounded-runtime-primary-loop-SCR-v10', 'function': name,
        'functionBase': base, 'sourceSha256': core.digest(source.read_bytes()), 'includeSha256': core.digest(header.read_bytes()),
        'compilerSha256': core.digest(Path(__file__).read_bytes()), 'parserSha256': core.digest(Path(core.__file__).read_bytes()),
        'parsedAst': ast, 'allocationProfile': allocation, 'counter': {'name': variable, 'slot': slot, 'sourceType': 'int',
            'vmRepresentation': 'exact integer values represented as IEEE754 binary32', 'start': start, 'endExclusive': end,
            'step': 1, 'iterations': end - start, 'finalValue': end, 'allIntegerValuesExactlyRepresentable': True},
        'setter': {'api': 'set_primary_flag', 'enabled': enabled, 'indices': list(range(start, end))},
        'runtimeLoop': True, 'constantLoopUnrolled': False, 'entryNonemptyConditionStaticallyProven': True,
        'generatedBranches': fixups, 'privateReturnPc': return_pc, 'unreachableCompilerJoinPc': base + compiler_join,
        'outputBytes': len(output), 'outputSha256': core.digest(output), 'generalCCompilerClaimed': False}


def main():
    parser = argparse.ArgumentParser()
    for name in ('source', 'locals', 'output', 'report'):
        parser.add_argument('--' + name, required=True)
    parser.add_argument('--base', type=lambda value: int(value, 0), required=True)
    options = parser.parse_args()
    body, report = compile_source(options.source, options.base, json.loads(Path(options.locals).read_text()))
    Path(options.output).write_bytes(body)
    Path(options.report).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'function': report['function'], 'bytes': len(body), 'sha256': report['outputSha256']}))


if __name__ == '__main__':
    main()
