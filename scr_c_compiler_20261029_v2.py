import argparse
import hashlib
import json
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOKEN = re.compile(r'\s+|0[xX][0-9a-fA-F]+|[0-9]+|[A-Za-z_][A-Za-z_0-9]*|\+\+|<=|>=|==|!=|[{}();,=+*<>!-]')
HEADER = 'typedef enum { false = 0 , true = 1 } bool ; void set_primary_flag ( int index , bool enabled ) ; void before_primary_flag_reset ( void ) ;'.split()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def tokens(text):
    result, cursor = [], 0
    for match in TOKEN.finditer(text):
        if match.start() != cursor:
            raise ValueError('Unsupported C token at character ' + str(cursor))
        cursor = match.end()
        if not match.group().isspace():
            result.append(match.group())
    if cursor != len(text):
        raise ValueError('Unsupported trailing C text')
    return result


class Parser:
    def __init__(self, values):
        self.values, self.at = values, 0

    def peek(self):
        return self.values[self.at] if self.at < len(self.values) else None

    def take(self, expected=None):
        value = self.peek()
        if value is None or expected is not None and value != expected:
            raise ValueError('Expected ' + str(expected) + ' at token ' + str(self.at))
        self.at += 1
        return value

    def identifier(self):
        value = self.take()
        if not re.fullmatch('[A-Za-z_][A-Za-z_0-9]*', value):
            raise ValueError('Expected identifier')
        if value in ('void', 'int', 'for', 'if', 'else', 'return', 'typedef', 'enum', 'while', 'do',
                     'break', 'continue', 'switch', 'case', 'default', 'static', 'extern', 'const',
                     'unsigned', 'signed', 'char', 'short', 'long', 'float', 'double', 'struct', 'union',
                     'auto', 'register', 'restrict', 'sizeof', 'volatile', 'inline', 'goto',
                     '_Bool', '_Complex', '_Imaginary'):
            raise ValueError('C keyword cannot be used as an identifier')
        return value

    def expression(self, minimum=0):
        token = self.take()
        if token == '(':
            node = self.expression()
            self.take(')')
        elif token in ('-', '!'):
            node = ('unary', token, self.expression(5))
        elif re.fullmatch('0[xX][0-9a-fA-F]+|[0-9]+', token):
            if len(token) > 1 and token[0] == '0' and not token.startswith(('0x', '0X')):
                raise ValueError('Only decimal and hexadecimal integer literals are supported')
            node = ('constant', int(token, 0) if token.startswith(('0x', '0X')) else int(token))
        elif re.fullmatch('[A-Za-z_][A-Za-z_0-9]*', token):
            node = ('variable', token)
        else:
            raise ValueError('Unsupported expression')
        precedence = {'==': 1, '!=': 1, '<': 2, '>': 2, '<=': 2, '>=': 2, '+': 3, '-': 3, '*': 4}
        while self.peek() in precedence and precedence[self.peek()] >= minimum:
            operation = self.take()
            node = ('binary', operation, node, self.expression(precedence[operation] + 1))
        return node

    def block(self):
        self.take('{')
        result = []
        while self.peek() != '}':
            result.append(self.statement())
        self.take('}')
        return result

    def statement(self):
        token = self.peek()
        if token == 'int':
            self.take()
            name = self.identifier()
            self.take('=')
            value = self.expression()
            self.take(';')
            return ('declare', name, value)
        if token == 'for':
            self.take()
            self.take('(')
            self.take('int')
            name = self.identifier()
            self.take('=')
            start = self.expression()
            self.take(';')
            condition = self.expression()
            self.take(';')
            self.take('++')
            if self.identifier() != name:
                raise ValueError('For-loop increment variable must match its declaration')
            self.take(')')
            return ('for', name, start, condition, self.block())
        if token == 'if':
            self.take()
            self.take('(')
            condition = self.expression()
            self.take(')')
            yes = self.block()
            no = []
            if self.peek() == 'else':
                self.take()
                no = self.block()
            return ('if', condition, yes, no)
        if token == 'return':
            self.take()
            self.take(';')
            return ('return',)
        name = self.identifier()
        self.take('(')
        arguments = []
        if self.peek() != ')':
            arguments.append(self.expression())
            while self.peek() == ',':
                self.take()
                arguments.append(self.expression())
        self.take(')')
        self.take(';')
        return ('call', name, arguments)

    def function(self):
        self.take('void')
        name = self.identifier()
        if name in ('false', 'true', 'bool', 'set_primary_flag'):
            raise ValueError('Entry function conflicts with an ABI declaration')
        self.take('(')
        self.take('void')
        self.take(')')
        body = self.block()
        if self.peek() is not None:
            raise ValueError('Only one void function is supported per source unit')
        return name, body


def checked(value):
    if not -(1 << 31) <= value < 1 << 31:
        raise ValueError('Signed32 compile-time arithmetic overflow')
    return value


def evaluate(node, environment):
    if node[0] == 'constant':
        return checked(node[1])
    if node[0] == 'variable':
        if node[1] not in environment:
            raise ValueError('Unknown compile-time variable ' + node[1])
        return environment[node[1]]
    if node[0] == 'unary':
        value = evaluate(node[2], environment)
        return checked(-value) if node[1] == '-' else int(not value)
    left, right = evaluate(node[2], environment), evaluate(node[3], environment)
    operation = node[1]
    if operation in ('+', '-', '*'):
        return checked(left + right if operation == '+' else left - right if operation == '-' else left * right)
    return int({'==': left == right, '!=': left != right, '<': left < right,
                '>': left > right, '<=': left <= right, '>=': left >= right}[operation])


class Lowerer:
    def __init__(self, bindings):
        self.calls, self.steps = [], 0
        self.bindings = bindings

    def block(self, statements, environment):
        local = dict(environment)
        for statement in statements:
            self.steps += 1
            if self.steps > 10000:
                raise ValueError('Compile-time evaluation bound exceeded')
            kind = statement[0]
            if kind == 'return':
                return True
            if kind == 'declare':
                if statement[1] in local:
                    raise ValueError('Variable shadowing is unsupported')
                local[statement[1]] = evaluate(statement[2], local)
            elif kind == 'if':
                if self.block(statement[2] if evaluate(statement[1], local) else statement[3], local):
                    return True
            elif kind == 'for':
                name = statement[1]
                if name in local:
                    raise ValueError('Loop variable shadowing is unsupported')
                iteration = dict(local)
                iteration[name] = evaluate(statement[2], local)
                count = 0
                while evaluate(statement[3], iteration):
                    count += 1
                    if count > 1024:
                        raise ValueError('Constant-loop unrolling bound exceeded')
                    if self.block(statement[4], iteration):
                        return True
                    iteration[name] = checked(iteration[name] + 1)
            elif kind == 'call':
                if statement[1] == 'before_primary_flag_reset':
                    if statement[2] or statement[1] not in self.bindings:
                        raise ValueError('Script call requires a bound zero-argument declaration')
                    self.calls.append({'api': statement[1], 'targetPc': self.bindings[statement[1]]})
                    if len(self.calls) > 1024:
                        raise ValueError('Emitted-call bound exceeded')
                    continue
                if statement[1] != 'set_primary_flag' or len(statement[2]) != 2:
                    raise ValueError('Unsupported runtime API or argument count')
                index, enabled = (evaluate(value, local) for value in statement[2])
                if not 0 <= index < 1536 or enabled not in (0, 1):
                    raise ValueError('Primary-flag argument outside the supported ABI domain')
                self.calls.append({'api': statement[1], 'index': index, 'enabled': enabled})
                if len(self.calls) > 1024:
                    raise ValueError('Emitted-call bound exceeded')
        return False


def validate_expression(node, names):
    if node[0] == 'variable' and node[1] not in names:
        raise ValueError('Undeclared C variable ' + node[1])
    for child in node[2:] if node[0] in ('binary', 'unary') else ():
        validate_expression(child, names)


def validate_ast(statements, names):
    local = set(names)
    for statement in statements:
        kind = statement[0]
        if kind == 'call':
            if (statement[1], len(statement[2])) not in (('set_primary_flag', 2), ('before_primary_flag_reset', 0)):
                raise ValueError('Unsupported declared runtime API')
            for argument in statement[2]:
                validate_expression(argument, local)
        elif kind in ('declare', 'for'):
            if statement[1] in local or statement[1] in ('set_primary_flag', 'before_primary_flag_reset'):
                raise ValueError('Variable shadowing is unsupported')
            validate_expression(statement[2], local)
            if kind == 'declare':
                local.add(statement[1])
            else:
                validate_expression(statement[3], local | {statement[1]})
                validate_ast(statement[4], local | {statement[1]})
        elif kind == 'if':
            validate_expression(statement[1], local)
            validate_ast(statement[2], local)
            validate_ast(statement[3], local)


def compile_source(source_path, base, bindings=None):
    bindings = {} if bindings is None else dict(bindings)
    if any(name != "before_primary_flag_reset" or type(target) is not int or not 0 <= target < 0x80000000 or target % 4 for name, target in bindings.items()):
        raise ValueError("Unsupported, unaligned or out-of-range script binding")
    source_path = Path(source_path).resolve()
    text = source_path.read_text(encoding='utf-8')
    include = re.match(r'\s*#include\s+"([^"\r\n]+)"\s*\n', text)
    if include is None:
        raise ValueError('One explicit repository-local quoted ABI include is required')
    header = (source_path.parent / include[1]).resolve()
    header.relative_to(source_path.parent)
    header_text = header.read_text(encoding='utf-8')
    directives = [line.strip() for line in header_text.splitlines() if line.lstrip().startswith('#')]
    if directives != ['#ifndef SCR_FLAGS_20261029', '#define SCR_FLAGS_20261029', '#endif']:
        raise ValueError('Only the verified ABI include guard is supported')
    definitions = '\n'.join(line for line in header_text.splitlines() if not line.startswith('#'))
    if tokens(definitions) != HEADER:
        raise ValueError('Unsupported ABI declarations')
    name, ast = Parser(tokens(text[include.end():])).function()
    validate_ast(ast, {'false', 'true'})
    lowerer = Lowerer(bindings)
    lowerer.block(ast, {'false': 0, 'true': 1})
    if base < 0 or base % 4 or base + 16 + sum(56 if call["api"] == "set_primary_flag" else 12 for call in lowerer.calls) > 0x7FFFFFFF:
        raise ValueError('Invalid SCR function placement')
    output = bytearray(struct.pack('<3I', 1036, 12, base + 12))
    for call in lowerer.calls:
        if call['api'] == 'before_primary_flag_reset':
            output.extend(struct.pack('<3I', 1033, 12, call['targetPc']))
            continue
        for register, value in enumerate((call['index'], call['enabled'])):
            register_bits = struct.unpack('<I', struct.pack('<f', register))[0]
            value_bits = struct.unpack('<I', struct.pack('<f', value))[0]
            output.extend(struct.pack('<6I', 1045, 24, 1, register_bits, 2, value_bits))
        output.extend(struct.pack('<2I', 42, 8))
    output.extend(struct.pack('<I', 1026))
    report = {'schemaVersion': 1, 'function': name, 'sourceSha256': digest(source_path.read_bytes()),
              'sourcePath': str(source_path), 'includePath': str(header), 'includeSha256': digest(header.read_bytes()),
              'compilerPath': str(Path(__file__).resolve()), 'compilerSha256': digest(Path(__file__).read_bytes()),
              'pythonVersion': sys.version, 'pythonExecutableSha256': digest(Path(sys.executable).read_bytes()),
              'backend': 'restricted-C99-constant-evaluation-SCR-flags-and-calls-v2', 'functionBase': base,
              'scriptBindings': bindings, 'constantLoopsUnrolled': True, 'evaluatedAst': ast, 'loweredNamedCalls': lowerer.calls,
              'outputBytes': len(output), 'outputSha256': digest(output),
              'runtimeVariablesSupported': False, 'generalCCompilerClaimed': False}
    return bytes(output), report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True)
    parser.add_argument('--base', type=lambda value: int(value, 0), required=True)
    parser.add_argument('--bindings')
    parser.add_argument('--output', required=True)
    parser.add_argument('--report', required=True)
    options = parser.parse_args()
    source = (ROOT / options.source).resolve()
    binding_path = (ROOT / options.bindings).resolve() if options.bindings else None
    bindings = json.loads(binding_path.read_text()) if binding_path else {}
    body, report = compile_source(source, options.base, bindings)
    report['bindingInput'] = None if binding_path is None else {'path': str(binding_path), 'sha256': digest(binding_path.read_bytes())}
    output, report_path = (ROOT / options.output).resolve(), (ROOT / options.report).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(body)
    report_path.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'function': report['function'], 'bytes': len(body), 'sha256': report['outputSha256']}))


if __name__ == '__main__':
    main()
