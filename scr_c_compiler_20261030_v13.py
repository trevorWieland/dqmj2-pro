import argparse
import hashlib
import json
import re
import struct
from pathlib import Path
import scr_c_compiler_20261029 as core

assert hashlib.sha256(Path(core.__file__).read_bytes()).hexdigest() == '8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935'
HEADER = core.tokens('void set_context_byte_row(int index, int a, int b, int c, int d);')


def fword(value):
    return struct.unpack('<I', struct.pack('<f', value))[0]


def compile_source(source_path, base):
    source = Path(source_path).resolve()
    if type(base) is not int or not 0 <= base < 0x80000000 or base % 4:
        raise ValueError('Invalid byte-row configuration placement')
    text = source.read_text()
    include = re.match(r'\s*#include\s+"([^"\r\n]+)"\s*\n', text)
    if include is None:
        raise ValueError('One byte-row configuration include required')
    header = (source.parent / include[1]).resolve()
    header.relative_to(source.parent)
    header_text = header.read_text()
    directives = [line.strip() for line in header_text.splitlines() if line.lstrip().startswith('#')]
    if directives != ['#ifndef SCR_BYTE_ROWS_20261030', '#define SCR_BYTE_ROWS_20261030', '#endif']:
        raise ValueError('Byte-row ABI preprocessing')
    definitions = '\n'.join(line for line in header_text.splitlines() if not line.startswith('#'))
    if core.tokens(definitions) != HEADER:
        raise ValueError('Typed five-int byte-row ABI required')
    name, ast = core.Parser(core.tokens(text[include.end():])).function()
    if name in ('set_context_byte_row', 'true', 'false'):
        raise ValueError('Configuration definition shadows an API or constant')
    if not 1 <= len(ast) <= 256:
        raise ValueError('Nonempty bounded configuration body required')
    code = bytearray(struct.pack('<3I', 1036, 12, base + 12))
    calls = []
    for statement in ast:
        if statement[0:2] != ('call', 'set_context_byte_row') or len(statement[2]) != 5:
            raise ValueError('Only named five-argument byte-row calls supported')
        values = [core.evaluate(expression, {}) for expression in statement[2]]
        if not 0 <= values[0] < 19 or any(not 0 <= value <= 255 for value in values[1:]):
            raise ValueError('Logical index0..18 and four byte values required')
        start = base + len(code)
        for index, value in enumerate(values):
            code.extend(struct.pack('<6I', 1045, 24, 1, fword(index), 2, fword(value)))
        code.extend(struct.pack('<2I', 102, 8))
        calls.append({'api': 'set_context_byte_row', 'logicalIndex': values[0], 'bytes': values[1:],
            'startPc': start, 'systemPc': base + len(code) - 8})
    code.extend(struct.pack('<I', 1026))
    if base + len(code) >= 0x80000000:
        raise ValueError('Byte-row configuration range overflow')
    body = bytes(code)
    return body, {'backend': 'restricted-C99-native-byte-row-configuration-SCR-v13', 'function': name,
        'sourceSha256': core.digest(source.read_bytes()), 'includeSha256': core.digest(header.read_bytes()),
        'compilerSha256': core.digest(Path(__file__).read_bytes()), 'parserSha256': core.digest(Path(core.__file__).read_bytes()),
        'functionBase': base, 'parsedAst': ast, 'namedApiCalls': calls, 'outputBytes': len(body), 'outputSha256': core.digest(body),
        'generalCCompilerClaimed': False, 'configurationOnly': True, 'sourceContainsBranches': False,
        'logicalIndexDomain': [0, 18], 'byteValueDomain': [0, 255], 'nativeApiSourceCredit': 0}


def main():
    parser = argparse.ArgumentParser()
    for name in ('source', 'output', 'report'):
        parser.add_argument('--' + name, required=True)
    parser.add_argument('--base', type=lambda value: int(value, 0), required=True)
    options = parser.parse_args()
    body, report = compile_source(options.source, options.base)
    Path(options.output).write_bytes(body)
    Path(options.report).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'bytes': len(body), 'sha256': report['outputSha256']}))


if __name__ == '__main__':
    main()
