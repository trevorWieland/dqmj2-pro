import argparse
import hashlib
import json
import re
from pathlib import Path
import scr_c_compiler_20261030_v16 as previous

assert hashlib.sha256(Path(previous.__file__).read_bytes()).hexdigest() == '84ff9e84b8085d8776c623ec92c9b3e7ace9e9daa90420297f54b8090fb6f5b7'
core, fword = previous.core, previous.fword
API = core.tokens('float get_unoccupied_native_record_count(void);')
RESERVED = previous.RESERVED | {'get_unoccupied_native_record_count'}


class Parser(previous.Parser):
    def statement(self):
        if self.peek() == 'return':
            self.take()
            value = self.expression()
            self.take(';')
            return 'return_value', value
        if self.at + 2 < len(self.values) and self.values[self.at + 1:self.at + 3] == ['=', 'get_unoccupied_native_record_count']:
            name = self.identifier()
            for token in ('=', 'get_unoccupied_native_record_count', '(', ')', ';'):
                self.take(token)
            return 'read_count', name
        return super().statement()

    def function(self):
        self.take('float')
        name = self.identifier()
        for token in ('(', 'void', ')'):
            self.take(token)
        statements = self.block()
        if self.peek() is not None:
            raise ValueError('One float-return/no-formal definition required')
        return name, statements


class Backend(previous.Backend):
    def __init__(self, base, objects):
        super().__init__(base, objects, 0)
        self.returns = 0

    def operand(self, expression):
        if expression[0] == 'variable' and expression[1] in self.objects:
            return super().operand(expression)
        value = core.evaluate(expression, {})
        if abs(value) > 1 << 24:
            raise ValueError('Capacity constant must be exact binary32 integer')
        return 2, fword(value)

    def block(self, statements):
        for node in statements:
            self.steps += 1
            if self.steps > 256:
                raise ValueError('Capacity AST bound exceeded')
            kind = node[0]
            if kind == 'read_count':
                slot = self.destination(node[1])
                write = self.accesses[-1]
                self.emit(187, 8)
                write['instructionPc'] = self.base + len(self.code)
                self.emit(1045, 24, 0, fword(slot), 1, fword(0))
                self.calls.append({'api': 'get_unoccupied_native_record_count', 'arguments': [], 'argumentBankClobbers': [0], 'resultObject': node[1]})
            elif kind == 'return_value':
                self.emit(1045, 24, 1, fword(0), *self.operand(node[1]))
                self.emit(1026)
                self.returns += 1
            elif kind == 'if':
                condition = node[1]
                if condition[0] != 'binary' or condition[1] not in ('==', '!=', '<='):
                    raise ValueError('Only capacity scalar equality/inequality/less-equal supported')
                self.emit({'==': 1039, '!=': 1040, '<=': 1044}[condition[1]], 24, *self.operand(condition[2]), *self.operand(condition[3]))
                false = self.emit(1038, 12, 0)
                self.block(node[2])
                finish = self.emit(1036, 12, 0)
                self.fix(false, self.base + len(self.code), 'if-false')
                self.block(node[3])
                self.fix(finish, self.base + len(self.code), 'if-join')
            elif kind == 'assign':
                super().block([node])
            else:
                raise ValueError('Unsupported capacity statement')


def compile_source(source_path, base, profile):
    if type(base) is not int or not 0 <= base < 0x80000000 or base % 4 or not isinstance(profile, dict) or set(profile) != {'objects'}:
        raise ValueError('Explicit capacity placement/object profile required')
    objects = profile['objects']
    if not isinstance(objects, dict) or not objects or any(not isinstance(name, str) or name in RESERVED or not isinstance(obj, dict)
            or set(obj) != {'bank', 'slot'} or type(obj['bank']) is not int or type(obj['slot']) is not int or obj['bank'] not in (0, 1)
            or not 0 <= obj['slot'] < (256 if obj['bank'] == 0 else 16) for name, obj in objects.items()):
        raise ValueError('Invalid explicit capacity module/argument object')
    if len({(obj['bank'], obj['slot']) for obj in objects.values()}) != len(objects):
        raise ValueError('Aliased capacity objects')
    source = Path(source_path).resolve()
    text = source.read_text()
    include = re.match(r'\s*#include\s+"([^"\r\n]+)"\s*\n', text)
    if include is None:
        raise ValueError('One capacity ABI include required')
    header = (source.parent / include[1]).resolve()
    header.relative_to(source.parent)
    content = header.read_text()
    if [line.strip() for line in content.splitlines() if line.lstrip().startswith('#')] != [
            '#ifndef SCR_RECORD_CAPACITY_20261030', '#define SCR_RECORD_CAPACITY_20261030', '#endif']:
        raise ValueError('Capacity ABI preprocessing')
    declarations = core.Parser(core.tokens('\n'.join(line for line in content.splitlines() if not line.startswith('#'))))
    names = []
    while declarations.peek() == 'extern':
        declarations.take('extern')
        declarations.take('float')
        name = declarations.identifier()
        declarations.take(';')
        if name in names or name in RESERVED:
            raise ValueError('Duplicate/reserved capacity object declaration')
        names.append(name)
    if set(names) != set(objects) or declarations.values[declarations.at:] != API:
        raise ValueError('Typed capacity ABI/object closure differs')
    name, statements = Parser(core.tokens(text[include.end():])).function()
    if name in objects or name in RESERVED or not statements or statements[-1][0] != 'return_value':
        raise ValueError('Non-shadowed capacity definition with final return required')

    def contains_return(rows):
        return any(node[0] == 'return_value' or node[0] == 'if' and (contains_return(node[2]) or contains_return(node[3])) for node in rows)

    if contains_return(statements[:-1]):
        raise ValueError('Exactly one final capacity return required')
    backend = Backend(base, objects)
    backend.block(statements)
    if backend.returns != 1 or base + len(backend.code) >= 0x80000000 or {row['name'] for row in backend.accesses} != set(objects):
        raise ValueError('Complete bounded capacity object/return closure required')
    body = bytes(backend.code)
    return body, {'backend': 'restricted-C99-explicit-module-native-record-capacity-SCR-v17', 'function': name,
        'sourceSha256': core.digest(source.read_bytes()), 'includeSha256': core.digest(header.read_bytes()),
        'compilerSha256': core.digest(Path(__file__).read_bytes()), 'parentCompilerSha256': core.digest(Path(previous.__file__).read_bytes()),
        'parserSha256': core.digest(Path(core.__file__).read_bytes()), 'functionBase': base, 'objectProfile': profile, 'parsedAst': statements,
        'objectAccesses': backend.accesses, 'namedApiCalls': backend.calls, 'generatedBranches': backend.branches,
        'outputBytes': len(body), 'outputSha256': core.digest(body), 'sourceReturnType': 'float', 'returnConvention': 'VM argument register0 raw binary32',
        'generalCCompilerClaimed': False, 'moduleAndArgumentObjectsAreNotPrivateLocals': True, 'opaqueGlobalDomainProofClaimed': False}


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
