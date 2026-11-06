import argparse
import hashlib
import json
import re
from pathlib import Path
import scr_c_compiler_20261030_v6 as scalar

assert hashlib.sha256(Path(scalar.__file__).read_bytes()).hexdigest() == 'ea44995cc5d9e13810a3d8f896b830a75b2cd42665a56b26d8289ef39df781a5'
prior = scalar.prior


class Parser(scalar.Parser):
    def statement(self):
        if self.peek() in ('float', 'bool') and self.at + 2 < len(self.values) and self.values[self.at + 2] == ';':
            value_type, name = self.take(), self.identifier()
            self.take(';')
            return ('uninitialized_local', value_type, name)
        return super().statement()

    def function(self):
        self.take('void')
        name = self.identifier()
        self.take('(')
        self.take('float')
        self.formal = self.identifier()
        self.take(')')
        body = self.block()
        if self.peek() is not None or name in prior.RESERVED or self.formal in prior.RESERVED or name == self.formal:
            raise ValueError('One non-shadowed float-formal decision definition required')
        return name, body


class Backend(scalar.Backend):
    def declare_local(self, name, value_type, names):
        if name in self.local_names or name in self.globals_declared or name in prior.RESERVED or name not in self.profile:
            raise ValueError('Missing, shadowed or reserved formal-decision local')
        self.local_names.add(name)
        names[name] = {'slot': self.profile[name], 'type': value_type, 'scope': 'local', 'provenance': None}
        self.allocations.append({'name': name, 'slot': self.profile[name], 'sourceType': value_type,
            'scope': 'local', 'vmRepresentation': 'IEEE754 binary32', 'vmByteOffset': 0x50 + self.profile[name] * 4,
            'declarationEmitsStore': False})

    def prepare_formal(self, formal, names):
        self.declare_local(formal, 'float', names)
        names[formal]['provenance'] = 'formal-argument-0'
        self.emit(1045, 24, 0, prior.fword(self.profile[formal]), 1, prior.fword(0))
        self.object_accesses.append({'name': formal, 'scope': 'local', 'access': 'write', 'storePc': self.base + 12,
                                    'source': 'formal-argument-0', 'representation': 'raw IEEE754 binary32 bits'})

    def condition(self, expression, names):
        if expression[0] == 'binary' and expression[2][0] == 'variable':
            descriptor = names.get(expression[2][1])
            if descriptor is not None and descriptor['scope'] == 'local' and descriptor.get('provenance') is None:
                raise ValueError('Uninitialized C automatic local read')
        super().condition(expression, names)

    def block(self, statements, environment):
        names = dict(environment)
        for statement in statements:
            self.nodes += 1
            if self.nodes > 2048:
                raise ValueError('Formal-decision AST bound')
            kind = statement[0]
            if kind == 'uninitialized_local':
                self.declare_local(statement[2], statement[1], names)
            elif kind == 'read_value':
                value_type, name, api, expression = statement[1:]
                self.declare_local(name, value_type, names)
                self.read(name, value_type, api, expression, names, 'local')
            elif kind == 'assign_getter':
                name, api, expression = statement[1:]
                if name not in names:
                    raise ValueError('Assignment target is not a visible declared object')
                descriptor = names[name]
                self.read(name, descriptor['type'], api, expression, names, descriptor['scope'])
            elif kind == 'call':
                api, arguments = statement[1:]
                if len(arguments) != 2:
                    raise ValueError('Byte-mode setter requires two arguments')
                if api == 'select_context_byte_mode':
                    limit, value_limit, opcode = 19, 4, 103
                elif api in prior.SETTERS:
                    limit, value_limit, opcode = prior.SETTERS[api]
                else:
                    raise ValueError('Unsupported byte-mode setter')
                index, value = self.index(arguments[0], limit), self.constant(arguments[1])
                if not 0 <= value < value_limit:
                    raise ValueError('Formal-decision setter domain')
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
                raise ValueError('Unsupported formal-decision statement')


def compile_source(source_path, base, profile):
    source = Path(source_path).resolve()
    if type(base) is not int or not 0 <= base < 0x80000000 or base % 4:
        raise ValueError('Invalid formal-decision placement')
    if not isinstance(profile, dict) or set(profile) != {'locals', 'globals'}:
        raise ValueError('Separate local/global profiles required')
    local_profile, global_profile = profile['locals'], profile['globals']
    if not isinstance(local_profile, dict) or not isinstance(global_profile, dict):
        raise ValueError('Local/global profile sections must be objects')
    combined = dict(global_profile, **local_profile)
    if set(local_profile) & set(global_profile) or len(set(combined.values())) != len(combined):
        raise ValueError('Formal-decision storage aliases')
    if any(not isinstance(name, str) or type(slot) is not int or not 0 <= slot < 256 for name, slot in combined.items()):
        raise ValueError('Invalid formal-decision slot allocation')
    text = source.read_text(encoding='utf-8')
    include = re.match(r'\s*#include\s+"([^"\r\n]+)"\s*\n', text)
    if include is None:
        raise ValueError('One formal-decision ABI include required')
    header = (source.parent / include[1]).resolve()
    header.relative_to(source.parent)
    header_text = header.read_text(encoding='utf-8')
    directives = [line.strip() for line in header_text.splitlines() if line.lstrip().startswith('#')]
    if directives != ['#ifndef SCR_BYTE_MODE_20261030', '#define SCR_BYTE_MODE_20261030', '#endif']:
        raise ValueError('Formal-decision ABI preprocessing')
    if prior.core.tokens('\n'.join(line for line in header_text.splitlines() if not line.startswith('#'))) != prior.HEADER + prior.core.tokens('void select_context_byte_mode(int index, int mode);'):
        raise ValueError('Formal-decision getter/setter ABI')
    parser = Parser(prior.core.tokens(text[include.end():]))
    name, ast, globals_declared = parser.unit()
    if set(globals_declared) != set(global_profile) or name in prior.RESERVED or parser.formal in globals_declared:
        raise ValueError('Formal/module-object declaration closure')
    backend = Backend(base, local_profile, global_profile, globals_declared)
    environment = {key: {'slot': global_profile[key], 'type': value_type, 'scope': 'module-global', 'provenance': None}
                   for key, value_type in globals_declared.items()}
    backend.prepare_formal(parser.formal, environment)
    backend.block(ast, environment)
    if backend.local_names != set(local_profile) or backend.global_writes != set(global_profile):
        raise ValueError('Unused local or unwritten module-global binding')
    backend.emit(1026)
    if base + len(backend.code) >= 0x80000000:
        raise ValueError('Formal-decision function overflow')
    output = bytes(backend.code)
    return output, {'backend': 'restricted-C99-float-formal-primary-byte-mode-SCR-v12', 'function': name,
        'sourceSha256': prior.core.digest(source.read_bytes()), 'includeSha256': prior.core.digest(header.read_bytes()),
        'compilerSha256': prior.core.digest(Path(__file__).read_bytes()),
        'priorCompilerSha256': prior.core.digest(Path(scalar.__file__).read_bytes()), 'parserSha256': prior.CORE_HASH,
        'functionBase': base, 'allocationProfile': profile, 'localAllocations': backend.allocations,
        'formalArguments': [{'name': parser.formal, 'sourceType': 'float', 'argumentRegister': 0,
            'slot': local_profile[parser.formal], 'copyRepresentation': 'raw IEEE754 binary32 bits'}],
        'objectAccesses': backend.object_accesses, 'namedApiCalls': backend.calls,
        'generatedBranches': backend.branches, 'parsedAst': ast, 'outputBytes': len(output),
        'outputSha256': prior.core.digest(output), 'generalCCompilerClaimed': False,
        'uninitializedLocalReadsRejected': True, 'uninitializedDeclarationsEmitNoStore': True,
        'branchLocalInitializationNotAssumedOutsideBranch': True, 'byteModeLogicalIndexDomain': [0, 18], 'byteModeDomain': [0, 3]}


def main():
    parser = argparse.ArgumentParser()
    for name in ('source', 'bindings', 'output', 'report'):
        parser.add_argument('--' + name, required=True)
    parser.add_argument('--base', type=lambda value: int(value, 0), required=True)
    options = parser.parse_args()
    body, report = compile_source(options.source, options.base, json.loads(Path(options.bindings).read_text()))
    Path(options.output).write_bytes(body)
    Path(options.report).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'function': report['function'], 'bytes': len(body), 'sha256': report['outputSha256']}))


if __name__ == '__main__':
    main()
