import argparse
import hashlib
import json
import re
import struct
import sys
from pathlib import Path

import scr_c_compiler_20261029 as core

ROOT = Path(__file__).resolve().parent
CORE_HASH = '8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935'
assert hashlib.sha256(Path(core.__file__).read_bytes()).hexdigest() == CORE_HASH
HEADER = 'typedef enum { false = 0 , true = 1 } bool ; float get_context_value ( int index ) ; float get_numeric_state ( int index ) ; void set_numeric_state ( int index , int value ) ; bool get_primary_flag ( int index ) ; void set_primary_flag ( int index , bool enabled ) ;'.split()
GETTERS = {'get_primary_flag': ('bool', 1536, 41), 'get_numeric_state': ('float', 88, 39),
           'get_context_value': ('float', 8, None)}
SETTERS = {'set_primary_flag': (1536, 2, 42), 'set_numeric_state': (88, 256, 40)}
RESERVED = set(GETTERS) | set(SETTERS) | {'false', 'true'}


class Parser(core.Parser):
    def statement(self):
        if self.peek() not in ('bool', 'float'):
            return super().statement()
        value_type = self.take()
        name = self.identifier()
        self.take('=')
        api = self.identifier()
        self.take('(')
        index = self.expression()
        self.take(')')
        self.take(';')
        return ('read_value', value_type, name, api, index)


def fword(value):
    return struct.unpack('<I', struct.pack('<f', value))[0]


class Backend:
    def __init__(self, base, allocation):
        self.base, self.profile = base, allocation
        self.code = bytearray(struct.pack('<3I', 1036, 12, base + 12))
        self.allocations, self.calls, self.branches = [], [], []
        self.allocated_names, self.nodes = set(), 0

    def emit(self, *words):
        offset = len(self.code)
        self.code.extend(struct.pack('<' + 'I' * len(words), *words))
        return offset

    def constant(self, expression):
        return core.evaluate(expression, {'false': 0, 'true': 1})

    def index(self, expression, limit):
        value = self.constant(expression)
        if not 0 <= value < limit:
            raise ValueError('Runtime API index outside supported domain')
        return value

    def immediate_argument(self, register, value):
        self.emit(1045, 24, 1, fword(register), 2, fword(value))

    def fixup(self, offset, target, kind):
        if target < self.base or target >= 0x80000000 or target % 4:
            raise ValueError('Invalid generated branch target')
        struct.pack_into('<I', self.code, offset + 8, target)
        self.branches.append({'sitePc': self.base + offset, 'targetPc': target, 'kind': kind})

    def condition(self, expression, names):
        if expression[0] != 'binary' or expression[1] not in ('==', '!='):
            raise ValueError('Runtime condition requires equality or inequality')
        left, right = expression[2], expression[3]
        if left[0] != 'variable' or left[1] not in names:
            raise ValueError('Runtime condition must read an initialized scalar variable')
        descriptor = names[left[1]]
        value = self.constant(right)
        if descriptor['type'] == 'bool' and value not in (0, 1):
            raise ValueError('Boolean comparison requires false or true')
        if abs(value) > 1 << 24:
            raise ValueError('Float comparison integer must be exactly representable in binary32')
        self.emit(1039 if expression[1] == '==' else 1040, 24, 0, fword(descriptor['slot']), 2, fword(value))

    def block(self, statements, environment):
        names = dict(environment)
        for statement in statements:
            self.nodes += 1
            if self.nodes > 1024:
                raise ValueError('Runtime AST bound exceeded')
            kind = statement[0]
            if kind == 'read_value':
                value_type, name, api, index_expression = statement[1:]
                if api not in GETTERS or GETTERS[api][0] != value_type:
                    raise ValueError('Getter name or result type does not match its declared ABI')
                if name in self.allocated_names or name in RESERVED:
                    raise ValueError('Runtime variable shadowing is unsupported')
                if name not in self.profile:
                    raise ValueError('Runtime variable is missing a named allocation')
                limit, opcode = GETTERS[api][1:]
                index = self.index(index_expression, limit)
                slot = self.profile[name]
                names[name] = {'slot': slot, 'type': value_type}
                self.allocated_names.add(name)
                self.allocations.append({'name': name, 'slot': slot, 'vmByteOffset': 0x50 + slot * 4,
                                         'sourceType': value_type, 'vmRepresentation': 'IEEE754 binary32'})
                if opcode is None:
                    self.emit(1045, 24, 0, fword(slot), 3, fword(index))
                else:
                    self.immediate_argument(0, index)
                    self.emit(opcode, 8)
                    self.emit(1045, 24, 0, fword(slot), 1, fword(0))
                self.calls.append({'api': api, 'index': index, 'resultVariable': name})
            elif kind == 'call':
                api = statement[1]
                if api not in SETTERS or len(statement[2]) != 2:
                    raise ValueError('Unsupported runtime API or argument count')
                limit, value_limit, opcode = SETTERS[api]
                index = self.index(statement[2][0], limit)
                value = self.constant(statement[2][1])
                if not 0 <= value < value_limit:
                    raise ValueError('Setter value outside the supported Boolean or byte domain')
                self.immediate_argument(0, index)
                self.immediate_argument(1, value)
                self.emit(opcode, 8)
                self.calls.append({'api': api, 'index': index, 'value': value})
            elif kind == 'if':
                self.condition(statement[1], names)
                branch = self.emit(1038, 12, 0)
                self.block(statement[2], names)
                join = self.emit(1036, 12, 0)
                self.fixup(branch, self.base + len(self.code), 'false-to-else-or-join')
                self.block(statement[3], names)
                self.fixup(join, self.base + len(self.code), 'then-to-join')
            else:
                raise ValueError('V4 supports typed getter declarations, constant setters and nested if/else only')


def compile_source(source_path, base, allocation):
    source_path = Path(source_path).resolve()
    if type(base) is not int or not 0 <= base < 0x80000000 or base % 4:
        raise ValueError('Invalid function placement')
    if not isinstance(allocation, dict) or any(not isinstance(name, str) or type(slot) is not int
            or not 0 <= slot < 256 for name, slot in allocation.items()):
        raise ValueError('Invalid named VM-local allocation profile')
    if len(set(allocation.values())) != len(allocation):
        raise ValueError('Distinct scalar declarations require distinct VM-local slots')
    text = source_path.read_text(encoding='utf-8')
    include = re.match(r'\s*#include\s+"([^"\r\n]+)"\s*\n', text)
    if include is None:
        raise ValueError('One repository-local ABI include is required')
    header = (source_path.parent / include[1]).resolve()
    header.relative_to(source_path.parent)
    header_text = header.read_text(encoding='utf-8')
    directives = [line.strip() for line in header_text.splitlines() if line.lstrip().startswith('#')]
    if directives != ['#ifndef SCR_NUMERIC_20261029', '#define SCR_NUMERIC_20261029', '#endif']:
        raise ValueError('Unsupported ABI preprocessing')
    definitions = '\n'.join(line for line in header_text.splitlines() if not line.startswith('#'))
    if core.tokens(definitions) != HEADER:
        raise ValueError('Unsupported numeric runtime ABI declarations')
    name, ast = Parser(core.tokens(text[include.end():])).function()
    if name in RESERVED:
        raise ValueError('Entry function conflicts with runtime ABI')
    backend = Backend(base, dict(allocation))
    backend.block(ast, {})
    if backend.allocated_names != set(allocation):
        raise ValueError('Allocation profile contains undeclared source variables')
    backend.emit(1026)
    if base + len(backend.code) >= 0x80000000:
        raise ValueError('Function range overflows signed SCR address space')
    output = bytes(backend.code)
    report = {'schemaVersion': 1, 'backend': 'restricted-C99-runtime-scalar-SCR-v4', 'function': name,
              'sourcePath': str(source_path), 'sourceSha256': core.digest(source_path.read_bytes()),
              'includePath': str(header), 'includeSha256': core.digest(header.read_bytes()),
              'compilerPath': str(Path(__file__).resolve()), 'compilerSha256': core.digest(Path(__file__).read_bytes()),
              'parserDependency': {'path': str(Path(core.__file__).resolve()), 'sha256': CORE_HASH},
              'pythonVersion': sys.version, 'pythonExecutableSha256': core.digest(Path(sys.executable).read_bytes()),
              'functionBase': base, 'namedAllocationProfile': allocation, 'variableAllocations': backend.allocations,
              'namedApiCalls': backend.calls, 'generatedBranches': backend.branches, 'parsedAst': ast,
              'outputBytes': len(output), 'outputSha256': core.digest(output),
              'generalCCompilerClaimed': False, 'interleavedOrReentrantSemanticsClaimed': False,
              'scalarAbi': 'Binary32 VM words; numeric getters yield exact bytes; context input is a raw binary32 value'}
    return output, report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True)
    parser.add_argument('--base', type=lambda value: int(value, 0), required=True)
    parser.add_argument('--locals', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--report', required=True)
    options = parser.parse_args()
    profile = (ROOT / options.locals).resolve()
    allocation = json.loads(profile.read_text())
    body, report = compile_source((ROOT / options.source).resolve(), options.base, allocation)
    report['allocationInput'] = {'path': str(profile), 'sha256': core.digest(profile.read_bytes())}
    output, report_path = (ROOT / options.output).resolve(), (ROOT / options.report).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(body)
    report_path.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'function': report['function'], 'bytes': len(body), 'sha256': report['outputSha256']}))


if __name__ == '__main__':
    main()
