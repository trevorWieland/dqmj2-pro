import argparse
import hashlib
import json
import re
import struct
from pathlib import Path
import scr_c_compiler_20261029 as core

assert hashlib.sha256(Path(core.__file__).read_bytes()).hexdigest() == '8b53fa5a1586f06e14cdb5929cf6d05a2733e92e09c92f6c671235d4df07d935'


class Parser(core.Parser):
    def statement(self):
        name = self.identifier()
        self.take('=')
        expression = self.expression()
        self.take(';')
        return 'assign', name, expression


def compile_source(source_path, base, profile):
    if type(base) is not int or not 0 <= base < 0x80000000 or base % 4:
        raise ValueError('Invalid global-initializer placement')
    if not isinstance(profile, dict) or set(profile) != {'globals'} or not isinstance(profile['globals'], dict) or not profile['globals']:
        raise ValueError('Explicit nonempty module-global binding profile required')
    mapping = profile['globals']
    if any(not isinstance(name, str) or type(slot) is not int or not 0 <= slot < 256 for name, slot in mapping.items()) or len(set(mapping.values())) != len(mapping):
        raise ValueError('Invalid or aliased module-global storage')
    source = Path(source_path).resolve()
    text = source.read_text()
    include = re.match(r'\s*#include\s+"([^"\r\n]+)"\s*\n', text)
    if include is None:
        raise ValueError('One module-global declaration include required')
    header = (source.parent / include[1]).resolve()
    header.relative_to(source.parent)
    content = header.read_text()
    if [line.strip() for line in content.splitlines() if line.lstrip().startswith('#')] != [
            '#ifndef SCR_REGISTERED_GLOBALS_20261030', '#define SCR_REGISTERED_GLOBALS_20261030', '#endif']:
        raise ValueError('Module-global declaration preprocessing')
    declarations = core.Parser(core.tokens('\n'.join(line for line in content.splitlines() if not line.startswith('#'))))
    objects = []
    while declarations.peek() is not None:
        declarations.take('extern')
        declarations.take('float')
        name = declarations.identifier()
        declarations.take(';')
        if name in objects:
            raise ValueError('Duplicate module-global declaration')
        objects.append(name)
    if set(objects) != set(mapping):
        raise ValueError('Module-global declaration/binding closure differs')
    name, statements = Parser(core.tokens(text[include.end():])).function()
    if name in objects or not 0 < len(statements) <= 256:
        raise ValueError('Non-shadowed bounded global initializer required')
    code = bytearray(struct.pack('<3I', 1036, 12, base + 12))
    stores = []
    for kind, target, expression in statements:
        if kind != 'assign' or target not in mapping:
            raise ValueError('Only declared module-global assignments supported')
        value = core.evaluate(expression, {})
        if abs(value) > 1 << 24:
            raise ValueError('Initializer integer must be exactly representable binary32')
        raw = struct.unpack('<I', struct.pack('<f', value))[0]
        pc = base + len(code)
        code.extend(struct.pack('<6I', 1045, 24, 0, struct.unpack('<I', struct.pack('<f', mapping[target]))[0], 2, raw))
        stores.append({'name': target, 'slot': mapping[target], 'instructionPc': pc, 'rawFloatWord': raw})
    code.extend(struct.pack('<I', 1026))
    if base + len(code) >= 0x80000000:
        raise ValueError('Global-initializer range overflow')
    body = bytes(code)
    return body, {'backend': 'restricted-C99-module-global-float-initializer-SCR-v15', 'function': name,
        'sourceSha256': core.digest(source.read_bytes()), 'includeSha256': core.digest(header.read_bytes()),
        'compilerSha256': core.digest(Path(__file__).read_bytes()), 'parserSha256': core.digest(Path(core.__file__).read_bytes()),
        'functionBase': base, 'bindingProfile': profile, 'moduleGlobalObjects': objects, 'orderedGlobalStores': stores,
        'parsedAst': statements, 'outputBytes': len(body), 'outputSha256': core.digest(body), 'sourceReturnType': 'void',
        'implicitPrivateReturn': True, 'generalCCompilerClaimed': False, 'moduleGlobalsAreNotPrivateLocals': True,
        'opaqueGlobalDomainProofClaimed': False, 'initializationOnly': True, 'branchDecisionLogicClaimed': False}


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
