import argparse
import hashlib
import json
import math
import re
import struct
import sys
from pathlib import Path

import scr_c_compiler_20261029_v4 as prior

ROOT = Path(__file__).resolve().parent
assert hashlib.sha256(Path(prior.__file__).read_bytes()).hexdigest() == '171818c7eda16c5d44e098a45ec425b268730a38e5f5696b73e19ce5e06b9de7'
FLOAT = r'[0-9]+\.[0-9]+(?:[eE][+-]?[0-9]+)?[fF]?'
TOKEN = re.compile(r'\s+|' + FLOAT + r'|0[xX][0-9a-fA-F]+|[0-9]+|[A-Za-z_][A-Za-z_0-9]*|\+\+|<=|>=|==|!=|[{}();,=+*<>!-]')
EXTRA_GETTERS = {'get_engine_state_code': ('float', 100)}
EXTRA_CALLS = {'select_native_request': (261, 1), 'replace_native_request_scalar': (266, 1),
               'submit_native_request': (98, 5)}
HEADER = ('typedef enum { false = 0 , true = 1 } bool ; float get_context_value ( int index ) ; '
          'float get_numeric_state ( int index ) ; void set_numeric_state ( int index , int value ) ; '
          'bool get_primary_flag ( int index ) ; void set_primary_flag ( int index , bool enabled ) ; '
          'float get_engine_state_code ( void ) ; void select_native_request ( float identifier ) ; '
          'void replace_native_request_scalar ( float value ) ; '
          'void submit_native_request ( float identifier , float x , float y , float z , float value ) ; '
          'void advance_numeric_nine_when_values_match ( void ) ; void process_imported_context ( float value ) ;').split()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def tokens(text):
    values, cursor = [], 0
    for match in TOKEN.finditer(text):
        if match.start() != cursor:
            raise ValueError('Unsupported typed-call C token')
        cursor = match.end()
        if not match.group().isspace():
            values.append(match.group())
    if cursor != len(text):
        raise ValueError('Unsupported trailing typed-call C text')
    return values


class Parser(prior.Parser):
    def expression(self, minimum=0):
        if self.peek() is not None and re.fullmatch(FLOAT, self.peek()):
            return ('floating', self.take())
        return super().expression(minimum)

    def statement(self):
        if self.peek() not in ('float', 'bool'):
            return super().statement()
        kind, name = self.take(), self.identifier()
        self.take('=')
        api = self.identifier()
        self.take('(')
        arguments = []
        if self.peek() != ')':
            arguments.append(self.expression())
            while self.peek() == ',':
                self.take()
                arguments.append(self.expression())
        self.take(')')
        self.take(';')
        return ('typed_getter', kind, name, api, arguments)


def scalar(expression):
    if expression[0] == 'floating':
        value = float(expression[1].rstrip('fF'))
    elif expression[0] == 'unary' and expression[1] == '-':
        value = -scalar(expression[2])
    else:
        value = prior.core.evaluate(expression, {'false': 0, 'true': 1})
    try:
        value = struct.unpack('<f', struct.pack('<f', value))[0]
    except (OverflowError, struct.error):
        raise ValueError('Scalar literal overflows binary32') from None
    if not math.isfinite(value):
        raise ValueError('Only finite scalar literals are supported')
    return value


class Backend(prior.Backend):
    def __init__(self, base, allocation, links):
        super().__init__(base, allocation)
        self.links, self.script_calls = links, []

    def argument(self, register, expression, names):
        if expression[0] == 'variable' and expression[1] in names:
            source = names[expression[1]]
            self.emit(1045, 24, 1, prior.fword(register), 0, prior.fword(source['slot']))
        else:
            self.immediate_argument(register, scalar(expression))

    def block(self, statements, environment):
        names = dict(environment)
        for statement in statements:
            self.nodes += 1
            if self.nodes > 2048:
                raise ValueError('Typed-call AST bound exceeded')
            kind = statement[0]
            if kind == 'typed_getter':
                value_type, name, api, arguments = statement[1:]
                if name in self.allocated_names or name in prior.RESERVED or name in EXTRA_GETTERS or name in EXTRA_CALLS or name in self.links:
                    raise ValueError('Runtime declaration shadows an existing identifier')
                if name not in self.profile:
                    raise ValueError('Missing named runtime allocation')
                if api in prior.GETTERS:
                    result_type, limit, opcode = prior.GETTERS[api]
                    if len(arguments) != 1:
                        raise ValueError('Getter argument count')
                    index = self.index(arguments[0], limit)
                elif api in EXTRA_GETTERS:
                    result_type, opcode = EXTRA_GETTERS[api]
                    if arguments:
                        raise ValueError('Engine state getter takes no arguments')
                    index = None
                else:
                    raise ValueError('Unknown typed getter')
                if value_type != result_type:
                    raise ValueError('Typed getter result ABI')
                slot = self.profile[name]
                names[name] = {'slot': slot, 'type': value_type}
                self.allocated_names.add(name)
                self.allocations.append({'name': name, 'slot': slot, 'vmByteOffset': 0x50 + slot * 4,
                    'sourceType': value_type, 'vmRepresentation': 'IEEE754 binary32'})
                if opcode is None:
                    self.emit(1045, 24, 0, prior.fword(slot), 3, prior.fword(index))
                else:
                    if index is not None:
                        self.immediate_argument(0, index)
                    self.emit(opcode, 8)
                    self.emit(1045, 24, 0, prior.fword(slot), 1, prior.fword(0))
                self.calls.append({'api': api, 'index': index, 'resultVariable': name})
            elif kind == 'call':
                api, arguments = statement[1:]
                if api in self.links:
                    descriptor = self.links[api]
                    if len(arguments) != descriptor['arity']:
                        raise ValueError('Script-link argument count')
                    for register, expression in enumerate(arguments):
                        self.argument(register, expression, names)
                    site = self.base + self.emit(1033, 12, descriptor['entryPc'])
                    self.script_calls.append({'name': api, 'sitePc': site, 'entryPc': descriptor['entryPc'],
                        'arity': descriptor['arity'], 'argumentAst': arguments, 'calleeSourceCredit': 0})
                elif api in EXTRA_CALLS:
                    opcode, arity = EXTRA_CALLS[api]
                    if len(arguments) != arity:
                        raise ValueError('Native request argument count')
                    for register, expression in enumerate(arguments):
                        self.argument(register, expression, names)
                    self.emit(opcode, 8)
                    self.calls.append({'api': api, 'systemOpcode': opcode, 'argumentAst': arguments})
                elif api in prior.SETTERS:
                    if len(arguments) != 2:
                        raise ValueError('State setter argument count')
                    limit, value_limit, opcode = prior.SETTERS[api]
                    index, value = self.index(arguments[0], limit), self.constant(arguments[1])
                    if not 0 <= value < value_limit:
                        raise ValueError('Setter value domain')
                    self.immediate_argument(0, index)
                    self.immediate_argument(1, value)
                    self.emit(opcode, 8)
                    self.calls.append({'api': api, 'index': index, 'value': value})
                else:
                    raise ValueError('Unbound typed call')
            elif kind == 'if':
                self.condition(statement[1], names)
                branch = self.emit(1038, 12, 0)
                self.block(statement[2], names)
                join = self.emit(1036, 12, 0)
                self.fixup(branch, self.base + len(self.code), 'false-to-else-or-join')
                if statement[3]:
                    self.emit(1024, 8)
                    next_block = self.emit(1036, 12, 0)
                    self.fixup(next_block, self.base + len(self.code), 'else-block-entry')
                self.block(statement[3], names)
                if statement[3]:
                    next_block = self.emit(1036, 12, 0)
                    self.fixup(next_block, self.base + len(self.code), 'else-block-exit')
                self.fixup(join, self.base + len(self.code), 'then-to-join')
            else:
                raise ValueError('Unsupported typed-call statement')


def compile_source(source_path, base, allocation, links):
    source = Path(source_path).resolve()
    if type(base) is not int or base < 0 or base % 4 or base >= 0x80000000:
        raise ValueError('Invalid typed-call placement')
    if not isinstance(allocation, dict) or any(type(slot) is not int or not 0 <= slot < 256 for slot in allocation.values()):
        raise ValueError('Invalid named allocation profile')
    if len(set(allocation.values())) != len(allocation):
        raise ValueError('Aliased scalar declarations')
    expected_names = {'advance_numeric_nine_when_values_match': 0, 'process_imported_context': 1}
    if set(links) != set(expected_names):
        raise ValueError('Exact declared script-link closure required')
    for name, descriptor in links.items():
        if type(descriptor.get('arity')) is not int or descriptor.get('arity') != expected_names[name] or type(descriptor.get('entryPc')) is not int:
            raise ValueError('Script-link declaration ABI')
        if not 0 <= descriptor['entryPc'] < 0x80000000 or descriptor['entryPc'] % 4:
            raise ValueError('Invalid script-link target')
        if set(descriptor) != {'entryPc', 'arity', 'scriptSha256', 'entryId', 'calleeSourceCredit'} or descriptor['calleeSourceCredit'] != 0:
            raise ValueError('Qualified zero-credit script-link fields')
        if re.fullmatch('[0-9a-f]{64}', descriptor['scriptSha256']) is None or type(descriptor['entryId']) is not int or not 0 <= descriptor['entryId'] < 1024:
            raise ValueError('Qualified script-link identity')
    if len({descriptor['scriptSha256'] for descriptor in links.values()}) != 1:
        raise ValueError('Cross-image links require a separately verified ABI')
    text = source.read_text()
    include = re.match(r'\s*#include\s+"([^"\r\n]+)"\s*\n', text)
    if include is None:
        raise ValueError('One typed ABI include required')
    header = (source.parent / include[1]).resolve()
    header.relative_to(source.parent)
    header_text = header.read_text()
    directives = [line.strip() for line in header_text.splitlines() if line.lstrip().startswith('#')]
    if directives != ['#ifndef SCR_TYPED_CALLS_20261029', '#define SCR_TYPED_CALLS_20261029', '#endif']:
        raise ValueError('Typed ABI preprocessing')
    definitions = '\n'.join(line for line in header_text.splitlines() if not line.startswith('#'))
    if tokens(definitions) != HEADER:
        raise ValueError('Typed call declarations differ from implemented ABI')
    name, ast = Parser(tokens(text[include.end():])).function()
    if name in set(prior.RESERVED) | set(EXTRA_GETTERS) | set(EXTRA_CALLS) | set(links):
        raise ValueError('Entry function shadows declared API')
    backend = Backend(base, dict(allocation), links)
    backend.block(ast, {})
    if backend.allocated_names != set(allocation):
        raise ValueError('Unused allocation binding')
    backend.emit(1026)
    if base + len(backend.code) >= 0x80000000:
        raise ValueError('Typed function range overflow')
    output = bytes(backend.code)
    return output, {'backend': 'restricted-C99-typed-script-calls-SCR-v5', 'function': name,
        'sourceSha256': digest(source.read_bytes()), 'includeSha256': digest(header.read_bytes()),
        'compilerSha256': digest(Path(__file__).read_bytes()), 'priorCompilerSha256': digest(Path(prior.__file__).read_bytes()),
        'parserSha256': digest(Path(prior.core.__file__).read_bytes()), 'functionBase': base,
        'namedAllocationProfile': allocation, 'variableAllocations': backend.allocations, 'namedApiCalls': backend.calls,
        'scriptLinkClosure': links, 'scriptCalls': backend.script_calls, 'generatedBranches': backend.branches,
        'parsedAst': ast, 'outputBytes': len(output), 'outputSha256': digest(output),
        'generalCCompilerClaimed': False, 'ordinaryScriptCalleeSourceCredit': 0,
        'scope': 'Finite binary32 literals, fixed-slot scalar getters, declared native APIs, named qualified script calls, structured if/else'}


def main():
    parser = argparse.ArgumentParser()
    for name in ('source', 'locals', 'links', 'output', 'report'):
        parser.add_argument('--' + name, required=True)
    parser.add_argument('--base', type=lambda value: int(value, 0), required=True)
    options = parser.parse_args()
    allocation = json.loads(Path(options.locals).read_text())
    links = json.loads(Path(options.links).read_text())
    body, report = compile_source(options.source, options.base, allocation, links)
    Path(options.output).write_bytes(body)
    Path(options.report).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'function': report['function'], 'bytes': len(body), 'sha256': report['outputSha256']}))


if __name__ == '__main__':
    main()
