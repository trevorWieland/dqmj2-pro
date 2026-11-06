import argparse
import hashlib
import json
import re
import struct
from pathlib import Path
import scr_c_compiler_20261029 as core

assert hashlib.sha256(Path(core.__file__).read_bytes()).hexdigest() == '8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935'
API = core.tokens('typedef enum { false = 0, true = 1 } bool; bool get_primary_flag(int index); void configure_runtime_object(float category, float first, float second, float third, float fourth, float mode, float selector);')
RESERVED = {'get_primary_flag', 'configure_runtime_object', 'false', 'true', 'bool', 'object_category'}


def fword(value):
    return struct.unpack('<I', struct.pack('<f', value))[0]


class Parser(core.Parser):
    def statement(self):
        if self.peek() == '{':
            return 'scope', self.block()
        if self.at + 1 < len(self.values) and self.values[self.at + 1] == '=':
            name = self.identifier()
            self.take('=')
            if self.peek() == 'get_primary_flag':
                self.take()
                self.take('(')
                value = self.expression()
                self.take(')')
                self.take(';')
                return 'read_flag', name, value
            value = self.expression()
            self.take(';')
            return 'assign', name, value
        return super().statement()


class Backend:
    def __init__(self, base, objects, category):
        self.base, self.objects, self.category = base, objects, category
        self.code = bytearray(struct.pack('<3I', 1036, 12, base + 12))
        self.accesses, self.calls, self.branches, self.scopes = [], [], [], []
        self.steps = 0

    def emit(self, *words):
        offset = len(self.code)
        self.code.extend(struct.pack('<' + 'I' * len(words), *words))
        return offset

    def fix(self, offset, target, kind):
        struct.pack_into('<I', self.code, offset + 8, target)
        self.branches.append({'sitePc': self.base + offset, 'targetPc': target, 'kind': kind})

    def operand(self, expression):
        if expression[0] == 'variable' and expression[1] in self.objects:
            name = expression[1]
            obj = self.objects[name]
            self.accesses.append({'name': name, **obj, 'access': 'read', 'instructionPc': self.base + len(self.code)})
            return obj['bank'], fword(obj['slot'])
        value = core.evaluate(expression, {'object_category': self.category, 'false': 0, 'true': 1})
        if abs(value) > 1 << 24:
            raise ValueError('Configuration constant must be exact binary32 integer')
        return 2, fword(value)

    def destination(self, name):
        if name not in self.objects or self.objects[name]['bank'] != 0:
            raise ValueError('Only declared module-global destination assignments supported')
        self.accesses.append({'name': name, **self.objects[name], 'access': 'write', 'instructionPc': self.base + len(self.code)})
        return self.objects[name]['slot']

    def block(self, statements):
        for node in statements:
            self.steps += 1
            if self.steps > 256:
                raise ValueError('Configuration AST bound exceeded')
            kind = node[0]
            if kind == 'assign':
                slot = self.destination(node[1])
                mode, raw = self.operand(node[2])
                self.emit(1045, 24, 0, fword(slot), mode, raw)
            elif kind == 'read_flag':
                slot = self.destination(node[1])
                write_access = self.accesses[-1]
                mode, raw = self.operand(node[2])
                if mode == 2 and not 0 <= struct.unpack('<f', struct.pack('<I', raw))[0] <= 1535:
                    raise ValueError('Primary index constant outside0..1535')
                self.emit(1045, 24, 1, fword(0), mode, raw)
                self.emit(41, 8)
                write_access['instructionPc'] = self.base + len(self.code)
                self.emit(1045, 24, 0, fword(slot), 1, fword(0))
                self.calls.append({'api': 'get_primary_flag', 'dynamicIndex': mode != 2, 'resultObject': node[1]})
            elif kind == 'call':
                if node[1] != 'configure_runtime_object' or len(node[2]) != 7:
                    raise ValueError('Only named seven-float configuration call supported')
                for index, argument in enumerate(node[2]):
                    self.emit(1045, 24, 1, fword(index), *self.operand(argument))
                self.emit(69, 8)
                self.calls.append({'api': 'configure_runtime_object', 'arguments': node[2], 'argumentBankClobbers': list(range(7))})
            elif kind == 'if':
                condition = node[1]
                if condition[0] != 'binary' or condition[1] not in ('==', '!='):
                    raise ValueError('Only scalar equality/inequality configuration conditions supported')
                self.emit(1039 if condition[1] == '==' else 1040, 24, *self.operand(condition[2]), *self.operand(condition[3]))
                false = self.emit(1038, 12, 0)
                self.block(node[2])
                finish = self.emit(1036, 12, 0)
                self.fix(false, self.base + len(self.code), 'if-false')
                self.block(node[3])
                self.fix(finish, self.base + len(self.code), 'if-join')
            elif kind == 'scope':
                start = self.base + self.emit(1024, 8)
                enter = self.emit(1036, 12, 0)
                self.fix(enter, self.base + len(self.code), 'lexical-block-entry')
                self.block(node[1])
                finish = self.emit(1036, 12, 0)
                self.fix(finish, self.base + len(self.code), 'lexical-block-exit')
                self.scopes.append({'startPc': start, 'endExclusivePc': self.base + len(self.code)})
            else:
                raise ValueError('Unsupported configuration source statement')


def compile_source(source_path, base, profile):
    if type(base) is not int or not 0 <= base < 0x80000000 or base % 4 or not isinstance(profile, dict) or set(profile) != {'objects'}:
        raise ValueError('Explicit configuration placement/object profile required')
    objects = profile['objects']
    if not isinstance(objects, dict) or not objects or any(not isinstance(name, str) or name in RESERVED or not isinstance(obj, dict)
            or set(obj) != {'bank', 'slot'} or type(obj['bank']) is not int or type(obj['slot']) is not int or obj['bank'] not in (0, 1)
            or not 0 <= obj['slot'] < (256 if obj['bank'] == 0 else 16) for name, obj in objects.items()):
        raise ValueError('Invalid explicit module/argument object')
    if len({(obj['bank'], obj['slot']) for obj in objects.values()}) != len(objects):
        raise ValueError('Aliased configuration objects')
    source = Path(source_path).resolve()
    text = source.read_text()
    include = re.match(r'\s*#include\s+"([^"\r\n]+)"\s*\n', text)
    if include is None:
        raise ValueError('One configuration ABI include required')
    header = (source.parent / include[1]).resolve()
    header.relative_to(source.parent)
    content = header.read_text()
    if [line.strip() for line in content.splitlines() if line.lstrip().startswith('#')] != [
            '#ifndef SCR_RUNTIME_CONFIGURATION_20261030', '#define SCR_RUNTIME_CONFIGURATION_20261030', '#endif']:
        raise ValueError('Configuration ABI preprocessing')
    declarations = core.Parser(core.tokens('\n'.join(line for line in content.splitlines() if not line.startswith('#'))))
    for token in ('enum', '{', 'object_category', '='):
        declarations.take(token)
    category = core.evaluate(declarations.expression(), {})
    for token in ('}', ';'):
        declarations.take(token)
    if not 0 <= category <= 255:
        raise ValueError('Configuration category must fit native byte')
    names = []
    while declarations.peek() == 'extern':
        declarations.take('extern')
        declarations.take('float')
        name = declarations.identifier()
        declarations.take(';')
        if name in names or name in RESERVED:
            raise ValueError('Duplicate/reserved configuration object declaration')
        names.append(name)
    if set(names) != set(objects) or declarations.values[declarations.at:] != API:
        raise ValueError('Typed configuration ABI/object closure differs')
    name, statements = Parser(core.tokens(text[include.end():])).function()
    if name in objects or name in RESERVED:
        raise ValueError('Configuration entry shadows declared API/object')
    backend = Backend(base, objects, category)
    backend.block(statements)
    backend.emit(1026)
    if base + len(backend.code) >= 0x80000000 or {row['name'] for row in backend.accesses} != set(objects):
        raise ValueError('Complete bounded object closure required')
    body = bytes(backend.code)
    return body, {'backend': 'restricted-C99-explicit-module-argument-configuration-SCR-v16', 'function': name,
        'sourceSha256': core.digest(source.read_bytes()), 'includeSha256': core.digest(header.read_bytes()),
        'compilerSha256': core.digest(Path(__file__).read_bytes()), 'parserSha256': core.digest(Path(core.__file__).read_bytes()),
        'functionBase': base, 'objectProfile': profile, 'objectCategory': category, 'parsedAst': statements,
        'objectAccesses': backend.accesses, 'namedApiCalls': backend.calls, 'generatedBranches': backend.branches,
        'lexicalScopes': backend.scopes, 'outputBytes': len(body), 'outputSha256': core.digest(body),
        'sourceReturnType': 'void', 'implicitPrivateReturn': True, 'generalCCompilerClaimed': False,
        'moduleAndArgumentObjectsAreNotPrivateLocals': True, 'dynamicPrimaryIndexRequiresQualifiedFiniteIntegerDomain': [0, 1535],
        'configurationFloatInputsRequireQualifiedNativeConversionDomain': True, 'opaqueGlobalDomainProofClaimed': False}


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
