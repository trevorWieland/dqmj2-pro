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
HEADER = 'typedef enum { false = 0 , true = 1 } bool ; bool get_primary_flag ( int index ) ; void set_primary_flag ( int index , bool enabled ) ;'.split()


class Parser(core.Parser):
    def statement(self):
        if self.peek() != 'bool':
            return super().statement()
        self.take('bool')
        name = self.identifier()
        self.take('=')
        self.take('get_primary_flag')
        self.take('(')
        index = self.expression()
        self.take(')')
        self.take(';')
        return ('read_flag', name, index)


def fword(value):
    return struct.unpack('<I', struct.pack('<f', value))[0]


class Backend:
    def __init__(self, base, local_base):
        self.base, self.local_base = base, local_base
        self.code = bytearray(struct.pack('<3I', 1036, 12, base + 12))
        self.allocations, self.calls, self.branches = [], [], []
        self.nodes = 0

    def emit(self, *words):
        offset = len(self.code)
        self.code.extend(struct.pack('<' + 'I' * len(words), *words))
        return offset

    def immediate_argument(self, register, value):
        self.emit(1045, 24, 1, fword(register), 2, fword(value))

    def constant(self, expression):
        return core.evaluate(expression, {'false': 0, 'true': 1})

    def flag_index(self, expression):
        value = self.constant(expression)
        if not 0 <= value < 1536:
            raise ValueError('Primary-flag index outside supported ABI domain')
        return value

    def fixup(self, offset, target, kind):
        if target < self.base or target >= 0x80000000 or target % 4:
            raise ValueError('Invalid generated branch target')
        struct.pack_into('<I', self.code, offset + 8, target)
        self.branches.append({'sitePc': self.base + offset, 'targetPc': target, 'kind': kind})

    def condition(self, expression, names):
        if expression[0] != 'binary' or expression[1] not in ('==', '!='):
            raise ValueError('Runtime conditions require a Boolean variable equality or inequality')
        left, right = expression[2], expression[3]
        if left[0] != 'variable' or left[1] not in names:
            raise ValueError('Runtime condition must read an initialized Boolean variable')
        value = self.constant(right)
        if value not in (0, 1):
            raise ValueError('Boolean comparison constant must be false or true')
        self.emit(1039 if expression[1] == '==' else 1040, 24, 0, fword(names[left[1]]), 2, fword(value))

    def block(self, statements, environment):
        names = dict(environment)
        for statement in statements:
            self.nodes += 1
            if self.nodes > 1024:
                raise ValueError('Runtime AST bound exceeded')
            kind = statement[0]
            if kind == 'read_flag':
                name = statement[1]
                if name in names or name in ('false', 'true', 'get_primary_flag', 'set_primary_flag'):
                    raise ValueError('Boolean variable shadowing is unsupported')
                index = self.flag_index(statement[2])
                slot = self.local_base + len(self.allocations)
                if slot >= 256:
                    raise ValueError('VM-local allocation exceeds the supported256-slot bank')
                names[name] = slot
                self.allocations.append({'name': name, 'slot': slot, 'vmByteOffset': 0x50 + slot * 4,
                                         'sourceType': 'bool', 'vmRepresentation': 'binary32 zero or one'})
                self.immediate_argument(0, index)
                self.emit(41, 8)
                self.emit(1045, 24, 0, fword(slot), 1, fword(0))
                self.calls.append({'api': 'get_primary_flag', 'index': index, 'resultVariable': name})
            elif kind == 'call':
                if statement[1] != 'set_primary_flag' or len(statement[2]) != 2:
                    raise ValueError('Unsupported runtime API or argument count')
                index = self.flag_index(statement[2][0])
                enabled = self.constant(statement[2][1])
                if enabled not in (0, 1):
                    raise ValueError('Setter Boolean argument must be false or true')
                self.immediate_argument(0, index)
                self.immediate_argument(1, enabled)
                self.emit(42, 8)
                self.calls.append({'api': 'set_primary_flag', 'index': index, 'enabled': enabled})
            elif kind == 'if':
                self.condition(statement[1], names)
                branch = self.emit(1038, 12, 0)
                self.block(statement[2], names)
                join = self.emit(1036, 12, 0)
                self.fixup(branch, self.base + len(self.code), 'false-to-else-or-join')
                self.block(statement[3], names)
                self.fixup(join, self.base + len(self.code), 'then-to-join')
            else:
                raise ValueError('V3 runtime subset supports Boolean getters, setters and structured if/else only')


def compile_source(source_path, base, local_base):
    source_path = Path(source_path).resolve()
    if type(base) is not int or not 0 <= base < 0x80000000 or base % 4:
        raise ValueError('Invalid function placement')
    if type(local_base) is not int or not 0 <= local_base < 256:
        raise ValueError('Invalid VM-local allocation profile')
    text = source_path.read_text(encoding='utf-8')
    include = re.match(r'\s*#include\s+"([^"\r\n]+)"\s*\n', text)
    if include is None:
        raise ValueError('One repository-local ABI include is required')
    header = (source_path.parent / include[1]).resolve()
    header.relative_to(source_path.parent)
    header_text = header.read_text(encoding='utf-8')
    directives = [line.strip() for line in header_text.splitlines() if line.lstrip().startswith('#')]
    if directives != ['#ifndef SCR_DECISION_20261029', '#define SCR_DECISION_20261029', '#endif']:
        raise ValueError('Unsupported ABI preprocessing')
    definitions = '\n'.join(line for line in header_text.splitlines() if not line.startswith('#'))
    if core.tokens(definitions) != HEADER:
        raise ValueError('Unsupported runtime ABI declarations')
    name, ast = Parser(core.tokens(text[include.end():])).function()
    if name == 'get_primary_flag':
        raise ValueError('Entry function conflicts with getter ABI')
    backend = Backend(base, local_base)
    backend.block(ast, {})
    backend.emit(1026)
    if base + len(backend.code) >= 0x80000000:
        raise ValueError('Function range overflows signed SCR address space')
    output = bytes(backend.code)
    report = {'schemaVersion': 1, 'backend': 'restricted-C99-runtime-bool-SCR-v3', 'function': name,
              'sourcePath': str(source_path), 'sourceSha256': core.digest(source_path.read_bytes()),
              'includePath': str(header), 'includeSha256': core.digest(header.read_bytes()),
              'compilerPath': str(Path(__file__).resolve()), 'compilerSha256': core.digest(Path(__file__).read_bytes()),
              'parserDependency': {'path': str(Path(core.__file__).resolve()), 'sha256': CORE_HASH},
              'pythonVersion': sys.version, 'pythonExecutableSha256': core.digest(Path(sys.executable).read_bytes()),
              'functionBase': base, 'localAllocationBase': local_base, 'variableAllocations': backend.allocations,
              'namedApiCalls': backend.calls, 'generatedBranches': backend.branches, 'parsedAst': ast,
              'outputBytes': len(output), 'outputSha256': core.digest(output),
              'runtimeVariablesSupported': 'Boolean getter results only', 'runtimeIfElseSupported': True,
              'generalCCompilerClaimed': False, 'reentrantOrInterleavedInvocationSemanticsClaimed': False,
              'scratchAllocationAbi': 'Fixed per-unit VM-local slots; serialized complete calls are the supported context'}
    return output, report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True)
    parser.add_argument('--base', type=lambda value: int(value, 0), required=True)
    parser.add_argument('--local-base', type=lambda value: int(value, 0), required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--report', required=True)
    options = parser.parse_args()
    body, report = compile_source((ROOT / options.source).resolve(), options.base, options.local_base)
    output, report_path = (ROOT / options.output).resolve(), (ROOT / options.report).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(body)
    report_path.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'function': report['function'], 'bytes': len(body), 'sha256': report['outputSha256']}))


if __name__ == '__main__':
    main()
