import argparse
import hashlib
import json
import re
import struct
from pathlib import Path
import scr_c_compiler_20261029 as core

assert hashlib.sha256(Path(core.__file__).read_bytes()).hexdigest() == '8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935'
HEADER = core.tokens('typedef enum { false = 0, true = 1 } bool; bool get_primary_flag(int index); void set_primary_flag(int index, bool enabled);')
RESERVED = {'get_primary_flag', 'set_primary_flag', 'false', 'true'}


def fword(value):
    return struct.unpack('<I', struct.pack('<f', value))[0]


class Parser(core.Parser):
    def statement(self):
        if self.peek() == '{':
            return ('scope', self.block())
        if self.peek() in ('float', 'bool'):
            value_type, name = self.take(), self.identifier()
            if self.peek() == ';':
                self.take(';')
                return ('declare', value_type, name, None)
            self.take('=')
            expression = self.expression()
            self.take(';')
            return ('declare', value_type, name, expression)
        if self.peek() == 'return':
            self.take()
            expression = self.expression()
            self.take(';')
            return ('return_value', expression)
        if self.at + 1 < len(self.values) and self.values[self.at + 1] == '=':
            name = self.identifier()
            self.take('=')
            if self.peek() == 'get_primary_flag':
                self.take()
                self.take('(')
                expression = self.expression()
                self.take(')')
                self.take(';')
                return ('read_flag', name, expression)
            expression = self.expression()
            self.take(';')
            return ('assign', name, expression)
        return super().statement()

    def unit(self):
        globals_declared = []
        while self.peek() == 'extern':
            self.take()
            self.take('float')
            name = self.identifier()
            self.take(';')
            if name in RESERVED or name in globals_declared:
                raise ValueError('Duplicate/reserved module-global float')
            globals_declared.append(name)
        self.take('float')
        name = self.identifier()
        self.take('(')
        self.take('float')
        formal = self.identifier()
        self.take(')')
        statements = self.block()
        if self.peek() is not None or name in RESERVED or formal in RESERVED or name == formal or formal in globals_declared:
            raise ValueError('One non-shadowed float-return/float-formal definition required')
        return name, formal, statements, globals_declared


class Backend:
    def __init__(self, base, profile, globals_declared):
        self.base, self.profile = base, profile
        self.code = bytearray(struct.pack('<3I', 1036, 12, base + 12))
        self.names = {name: {'type': 'float', 'slot': profile['globals'][name], 'scope': 'module-global', 'assigned': True}
            for name in globals_declared}
        self.locals, self.accesses, self.branches, self.calls, self.scopes = set(), [], [], [], []
        self.nodes, self.return_count = 0, 0

    def emit(self, *values):
        offset = len(self.code)
        self.code.extend(struct.pack('<' + 'I' * len(values), *values))
        return offset

    def fix(self, offset, target, kind):
        struct.pack_into('<I', self.code, offset + 8, target)
        self.branches.append({'sitePc': self.base + offset, 'targetPc': target, 'kind': kind})

    def operand(self, expression, names):
        if expression[0] == 'variable' and expression[1] not in ('false', 'true'):
            name = expression[1]
            if name not in names or not names[name]['assigned']:
                raise ValueError('Scalar read requires a declared assigned object')
            self.accesses.append({'name': name, 'slot': names[name]['slot'], 'scope': names[name]['scope'],
                'access': 'read', 'instructionPc': self.base + len(self.code)})
            return 0, fword(names[name]['slot'])
        value = core.evaluate(expression, {'false': 0, 'true': 1})
        if abs(value) > 1 << 24:
            raise ValueError('Scalar constant must be an exact binary32 integer')
        return 2, fword(value)

    def assign(self, name, expression, names):
        if name not in names or names[name]['scope'] != 'local':
            raise ValueError('Only declared local assignment supported')
        mode, raw = self.operand(expression, names)
        self.emit(1045, 24, 0, fword(names[name]['slot']), mode, raw)
        names[name] = dict(names[name], assigned=True)
        self.accesses.append({'name': name, 'slot': names[name]['slot'], 'scope': 'local', 'access': 'write',
            'instructionPc': self.base + len(self.code) - 24})

    def primary_index(self, expression, names):
        mode, raw = self.operand(expression, names)
        if mode == 2:
            value = struct.unpack('<f', struct.pack('<I', raw))[0]
            if not 0 <= value <= 1535 or value != int(value):
                raise ValueError('Constant primary index outside0..1535')
        return mode, raw

    def declare(self, value_type, name, expression, names):
        if name in names or name in self.locals or name in RESERVED or name not in self.profile['locals']:
            raise ValueError('Missing/shadowed/reserved local object')
        names[name] = {'type': value_type, 'slot': self.profile['locals'][name], 'scope': 'local', 'assigned': False}
        self.locals.add(name)
        if expression is not None:
            self.assign(name, expression, names)

    def chain(self, node, names):
        joins = []
        while True:
            condition = node[1]
            if condition[0] != 'binary' or condition[1] not in ('==', '!='):
                raise ValueError('Only scalar equality/inequality conditions supported')
            left, right = self.operand(condition[2], names), self.operand(condition[3], names)
            self.emit(1039 if condition[1] == '==' else 1040, 24, *left, *right)
            branch = self.emit(1038, 12, 0)
            self.block(node[2], names)
            joins.append(self.emit(1036, 12, 0))
            self.fix(branch, self.base + len(self.code), 'false-to-next-else-branch')
            if len(node[3]) == 1 and node[3][0][0] == 'if':
                node = node[3][0]
                continue
            self.block(node[3], names)
            break
        for join in joins:
            self.fix(join, self.base + len(self.code), 'then-to-shared-structured-join')

    def block(self, statements, environment):
        names = dict(environment)
        for node in statements:
            self.nodes += 1
            if self.nodes > 2048:
                raise ValueError('Scalar AST bound exceeded')
            kind = node[0]
            if kind == 'declare':
                self.declare(*node[1:], names)
            elif kind == 'assign':
                self.assign(node[1], node[2], names)
            elif kind == 'read_flag':
                name, expression = node[1:]
                if name not in names or names[name]['type'] != 'bool' or names[name]['scope'] != 'local':
                    raise ValueError('Primary getter requires a declared Boolean local')
                mode, raw = self.primary_index(expression, names)
                self.emit(1045, 24, 1, fword(0), mode, raw)
                self.emit(41, 8)
                self.emit(1045, 24, 0, fword(names[name]['slot']), 1, fword(0))
                names[name] = dict(names[name], assigned=True)
                self.accesses.append({'name': name, 'slot': names[name]['slot'], 'scope': 'local', 'access': 'write',
                    'instructionPc': self.base + len(self.code) - 24})
                self.calls.append({'api': 'get_primary_flag', 'dynamicIndex': mode == 0, 'resultObject': name})
            elif kind == 'call':
                if node[1] != 'set_primary_flag' or len(node[2]) != 2:
                    raise ValueError('Only named primary setter calls supported')
                mode, raw = self.primary_index(node[2][0], names)
                enabled = core.evaluate(node[2][1], {'false': 0, 'true': 1})
                if enabled not in (0, 1):
                    raise ValueError('Boolean primary setter value required')
                self.emit(1045, 24, 1, fword(0), mode, raw)
                self.emit(1045, 24, 1, fword(1), 2, fword(enabled))
                self.emit(42, 8)
                self.calls.append({'api': 'set_primary_flag', 'dynamicIndex': mode == 0, 'enabled': enabled})
            elif kind == 'if':
                self.chain(node, names)
            elif kind == 'scope':
                start = self.base + self.emit(1024, 8)
                entry = self.emit(1036, 12, 0)
                self.fix(entry, self.base + len(self.code), 'lexical-block-entry')
                self.block(node[1], names)
                finish = self.emit(1036, 12, 0)
                self.fix(finish, self.base + len(self.code), 'lexical-block-exit')
                self.scopes.append({'startPc': start, 'endExclusivePc': self.base + len(self.code)})
            elif kind == 'return_value':
                mode, raw = self.operand(node[1], names)
                self.emit(1045, 24, 1, fword(0), mode, raw)
                self.emit(1026)
                self.return_count += 1
            else:
                raise ValueError('Unsupported scalar-return statement')


def compile_source(source_path, base, profile):
    source = Path(source_path).resolve()
    if type(base) is not int or not 0 <= base < 0x80000000 or base % 4:
        raise ValueError('Invalid scalar-return placement')
    if not isinstance(profile, dict) or set(profile) != {'locals', 'globals'}:
        raise ValueError('Separate scalar-return local/global bindings required')
    locals_profile, globals_profile = profile['locals'], profile['globals']
    combined = dict(globals_profile, **locals_profile)
    if set(locals_profile) & set(globals_profile) or len(set(combined.values())) != len(combined) or any(
            not isinstance(name, str) or type(slot) is not int or not 0 <= slot < 256 for name, slot in combined.items()):
        raise ValueError('Invalid or aliased scalar-return storage')
    text = source.read_text()
    include = re.match(r'\s*#include\s+"([^"\r\n]+)"\s*\n', text)
    if include is None:
        raise ValueError('One scalar-return ABI include required')
    header = (source.parent / include[1]).resolve()
    header.relative_to(source.parent)
    content = header.read_text()
    if [line.strip() for line in content.splitlines() if line.lstrip().startswith('#')] != [
            '#ifndef SCR_REGISTERED_FLAGS_20261030', '#define SCR_REGISTERED_FLAGS_20261030', '#endif']:
        raise ValueError('Scalar-return ABI preprocessing')
    if core.tokens('\n'.join(line for line in content.splitlines() if not line.startswith('#'))) != HEADER:
        raise ValueError('Typed primary APIs required')
    name, formal, statements, globals_declared = Parser(core.tokens(text[include.end():])).unit()
    if set(globals_declared) != set(globals_profile) or name in globals_declared:
        raise ValueError('Scalar-return module object declaration closure')
    if not statements or statements[-1][0] != 'return_value' or any(node[0] == 'return_value' for node in statements[:-1]):
        raise ValueError('Exactly one final scalar return required')
    backend = Backend(base, profile, globals_declared)
    backend.declare('float', formal, None, backend.names)
    backend.emit(1045, 24, 0, fword(locals_profile[formal]), 1, fword(0))
    backend.names[formal]['assigned'] = True
    backend.block(statements, backend.names)
    if backend.locals != set(locals_profile) or backend.return_count != 1:
        raise ValueError('Complete local/return source closure required')
    body = bytes(backend.code)
    if base + len(body) >= 0x80000000:
        raise ValueError('Scalar-return range overflow')
    return body, {'backend': 'restricted-C99-registered-dynamic-primary-scalar-return-SCR-v14', 'function': name,
        'sourceSha256': core.digest(source.read_bytes()), 'includeSha256': core.digest(header.read_bytes()),
        'compilerSha256': core.digest(Path(__file__).read_bytes()), 'parserSha256': core.digest(Path(core.__file__).read_bytes()),
        'functionBase': base, 'allocationProfile': profile, 'formal': formal, 'formalCopyRepresentation': 'raw IEEE754 binary32 bits',
        'sourceReturnType': 'float', 'returnConvention': 'VM argument register0 raw binary32', 'parsedAst': statements,
        'moduleGlobalObjects': globals_declared, 'objectAccesses': backend.accesses, 'namedApiCalls': backend.calls,
        'generatedBranches': backend.branches, 'lexicalScopes': backend.scopes, 'outputBytes': len(body), 'outputSha256': core.digest(body),
        'generalCCompilerClaimed': False, 'dynamicPrimaryIndexRequiresQualifiedFiniteIntegerDomain': [0, 1535],
        'floatEqualityUsesNativeVmComparison': True, 'opaqueGlobalDomainProofClaimed': False}


def main():
    parser = argparse.ArgumentParser()
    for name in ('source', 'bindings', 'output', 'report'):
        parser.add_argument('--' + name, required=True)
    parser.add_argument('--base', type=lambda value: int(value, 0), required=True)
    options = parser.parse_args()
    body, report = compile_source(options.source, options.base, json.loads(Path(options.bindings).read_text()))
    Path(options.output).write_bytes(body)
    Path(options.report).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'bytes': len(body), 'sha256': report['outputSha256']}))


if __name__ == '__main__':
    main()
