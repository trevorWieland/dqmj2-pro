import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import scr_c_compiler_20261029_v4 as prior

assert hashlib.sha256(Path(prior.__file__).read_bytes()).hexdigest() == '171818c7eda16c5d44e098a45ec425b268730a38e5f5696b73e19ce5e06b9de7'


class Parser(prior.Parser):
    def statement(self):
        if self.at + 1 < len(self.values) and self.values[self.at + 1] == '=':
            name = self.identifier()
            self.take('=')
            api = self.identifier()
            self.take('(')
            index = self.expression()
            self.take(')')
            self.take(';')
            return ('assign_getter', name, api, index)
        return super().statement()

    def unit(self):
        globals_declared = {}
        while self.peek() == 'extern':
            self.take()
            value_type = self.take()
            if value_type not in ('float', 'bool'):
                raise ValueError('Only typed scalar extern module objects are supported')
            name = self.identifier()
            self.take(';')
            if name in globals_declared or name in prior.RESERVED:
                raise ValueError('Duplicate or reserved module object')
            globals_declared[name] = value_type
        name, ast = self.function()
        if name in globals_declared:
            raise ValueError('Function shadows module storage')
        return name, ast, globals_declared


class Backend(prior.Backend):
    def __init__(self, base, locals_profile, globals_profile, globals_declared):
        super().__init__(base, locals_profile)
        self.globals_profile, self.globals_declared = globals_profile, globals_declared
        self.local_names, self.categories, self.global_writes, self.object_accesses = set(), {}, set(), []

    def condition(self, expression, names):
        if expression[0] != 'binary' or expression[1] not in ('==', '!=', '>='):
            raise ValueError('Scalar-state comparison requires a supported relation')
        left, right = expression[2:]
        if left[0] != 'variable' or left[1] not in names:
            raise ValueError('Condition must use a visible typed scalar')
        descriptor = names[left[1]]
        value = self.constant(right)
        if descriptor['type'] == 'bool' and value not in (0, 1):
            raise ValueError('Boolean comparison domain')
        if abs(value) > 1 << 24:
            raise ValueError('Nonexact binary32 comparison integer')
        if expression[1] not in ('==', '!=') and descriptor.get('provenance') != 'get_numeric_state':
            raise ValueError('Ordered relations require a definitely initialized byte-derived numeric state')
        opcode = {'==': 1039, '!=': 1040, '>=': 1043}[expression[1]]
        site = self.base + self.emit(opcode, 24, 0, prior.fword(descriptor['slot']), 2, prior.fword(value))
        self.object_accesses.append({'name': left[1], 'scope': descriptor['scope'], 'access': 'read',
                                    'sitePc': site, 'relation': expression[1], 'constant': value})

    def read(self, name, value_type, api, expression, names, scope):
        if api not in prior.GETTERS or prior.GETTERS[api][0] != value_type:
            raise ValueError('Assigned getter result differs from object type')
        if name in self.categories and self.categories[name] != api:
            raise ValueError('Scalar-state assignments must retain their getter provenance category')
        self.categories[name] = api
        limit, opcode = prior.GETTERS[api][1:]
        index = self.index(expression, limit)
        slot = self.globals_profile[name] if scope == 'module-global' else self.profile[name]
        names[name] = {'slot': slot, 'type': value_type, 'scope': scope, 'provenance': api}
        start = self.base + len(self.code)
        if opcode is None:
            self.emit(1045, 24, 0, prior.fword(slot), 3, prior.fword(index))
        else:
            self.immediate_argument(0, index)
            self.emit(opcode, 8)
            self.emit(1045, 24, 0, prior.fword(slot), 1, prior.fword(0))
        self.calls.append({'api': api, 'index': index, 'resultObject': name, 'scope': scope})
        self.object_accesses.append({'name': name, 'scope': scope, 'access': 'write', 'startPc': start,
                                    'storePc': self.base + len(self.code) - 24, 'getter': api, 'index': index})
        if scope == 'module-global':
            self.global_writes.add(name)

    def block(self, statements, environment):
        names = dict(environment)
        for statement in statements:
            self.nodes += 1
            if self.nodes > 2048:
                raise ValueError('Scalar-state AST bound exceeded')
            kind = statement[0]
            if kind == 'read_value':
                value_type, name, api, expression = statement[1:]
                if name in self.local_names or name in self.globals_declared or name in prior.RESERVED:
                    raise ValueError('Scalar-state local shadows an object or API')
                if name not in self.profile:
                    raise ValueError('Missing named local allocation')
                self.local_names.add(name)
                self.allocations.append({'name': name, 'slot': self.profile[name], 'sourceType': value_type,
                    'scope': 'local', 'vmRepresentation': 'IEEE754 binary32', 'vmByteOffset': 0x50 + self.profile[name] * 4})
                self.read(name, value_type, api, expression, names, 'local')
            elif kind == 'assign_getter':
                name, api, expression = statement[1:]
                if name not in names:
                    raise ValueError('Assignment target is not a visible declared object')
                descriptor = names[name]
                self.read(name, descriptor['type'], api, expression, names, descriptor['scope'])
            elif kind == 'call':
                api, arguments = statement[1:]
                if api not in prior.SETTERS or len(arguments) != 2:
                    raise ValueError('Unsupported scalar-state setter')
                limit, value_limit, opcode = prior.SETTERS[api]
                index, value = self.index(arguments[0], limit), self.constant(arguments[1])
                if not 0 <= value < value_limit:
                    raise ValueError('Scalar-state setter value domain')
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
                raise ValueError('Unsupported scalar-state statement')


def compile_source(source_path, base, profile):
    source = Path(source_path).resolve()
    if type(base) is not int or not 0 <= base < 0x80000000 or base % 4:
        raise ValueError('Invalid scalar-state placement')
    if not isinstance(profile, dict) or set(profile) != {'locals', 'globals'}:
        raise ValueError('Separate local/global binding profiles required')
    local_profile, global_profile = profile['locals'], profile['globals']
    if not isinstance(local_profile, dict) or not isinstance(global_profile, dict):
        raise ValueError('Binding profile sections must be objects')
    combined = dict(global_profile, **local_profile)
    if set(local_profile) & set(global_profile) or len(set(combined.values())) != len(combined):
        raise ValueError('Local/global storage aliases are unsupported')
    if any(not isinstance(name, str) or type(slot) is not int or not 0 <= slot < 256 for name, slot in combined.items()):
        raise ValueError('Invalid scalar-state slot binding')
    text = source.read_text()
    include = re.match(r'\s*#include\s+"([^"\r\n]+)"\s*\n', text)
    if include is None:
        raise ValueError('One local scalar-state ABI include required')
    header = (source.parent / include[1]).resolve()
    header.relative_to(source.parent)
    header_text = header.read_text()
    directives = [line.strip() for line in header_text.splitlines() if line.lstrip().startswith('#')]
    if directives != ['#ifndef SCR_SCALAR_STATE_20261030', '#define SCR_SCALAR_STATE_20261030', '#endif']:
        raise ValueError('Scalar-state ABI preprocessing')
    definitions = '\n'.join(line for line in header_text.splitlines() if not line.startswith('#'))
    if prior.core.tokens(definitions) != prior.HEADER:
        raise ValueError('Scalar-state getter/setter ABI')
    name, ast, globals_declared = Parser(prior.core.tokens(text[include.end():])).unit()
    if set(globals_declared) != set(global_profile) or name in prior.RESERVED:
        raise ValueError('Declared module objects and bindings differ')
    backend = Backend(base, local_profile, global_profile, globals_declared)
    environment = {key: {'slot': global_profile[key], 'type': value_type, 'scope': 'module-global', 'provenance': None}
                   for key, value_type in globals_declared.items()}
    backend.block(ast, environment)
    if backend.local_names != set(local_profile) or backend.global_writes != set(global_profile):
        raise ValueError('Unused local or unwritten module-global binding')
    backend.emit(1026)
    if base + len(backend.code) >= 0x80000000:
        raise ValueError('Scalar-state function range overflow')
    output = bytes(backend.code)
    global_objects = [{'name': key, 'sourceType': value_type, 'scope': 'module-global', 'slot': global_profile[key],
        'vmByteOffset': 0x50 + global_profile[key] * 4, 'lifetime': 'Per-SCR-module VM state, retained across entry calls',
        'representation': 'Logical scalar encoded as IEEE754 binary32'} for key, value_type in globals_declared.items()]
    return output, {'backend': 'restricted-C99-scalar-state-SCR-v6', 'function': name,
        'sourceSha256': prior.core.digest(source.read_bytes()), 'includeSha256': prior.core.digest(header.read_bytes()),
        'compilerSha256': prior.core.digest(Path(__file__).read_bytes()),
        'priorCompilerSha256': prior.core.digest(Path(prior.__file__).read_bytes()), 'parserSha256': prior.CORE_HASH,
        'functionBase': base, 'allocationProfile': profile, 'moduleGlobalObjects': global_objects,
        'localAllocations': backend.allocations, 'objectAccesses': backend.object_accesses,
        'namedApiCalls': backend.calls, 'generatedBranches': backend.branches, 'parsedAst': ast,
        'outputBytes': len(output), 'outputSha256': prior.core.digest(output),
        'generalCCompilerClaimed': False, 'moduleGlobalStorageMadeExplicit': True,
        'orderedRelationsDomain': 'Only definitely initialized numeric-getter byte values; arbitrary context float relations unsupported',
        'elseLayout': 'Direct structured branch, matching the measured world entry34 unit'}


def main():
    parser = argparse.ArgumentParser()
    for name in ('source', 'bindings', 'output', 'report'):
        parser.add_argument('--' + name, required=True)
    parser.add_argument('--base', type=lambda value: int(value, 0), required=True)
    options = parser.parse_args()
    profile = json.loads(Path(options.bindings).read_text())
    body, report = compile_source(options.source, options.base, profile)
    Path(options.output).write_bytes(body)
    Path(options.report).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'function': report['function'], 'bytes': len(body), 'sha256': report['outputSha256']}))


if __name__ == '__main__':
    main()
