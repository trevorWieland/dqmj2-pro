import argparse
import hashlib
import json
import re
from pathlib import Path
import scr_c_compiler_20261030_v6 as scalar

assert hashlib.sha256(Path(scalar.__file__).read_bytes()).hexdigest() == 'ea44995cc5d9e13810a3d8f896b830a75b2cd42665a56b26d8289ef39df781a5'
prior = scalar.prior
HEADER = prior.HEADER + prior.core.tokens('void reset_context_words(void); void set_context_word(int index, int value);')
RESERVED = prior.RESERVED | {'reset_context_words', 'set_context_word'}


class Parser(scalar.Parser):
    def statement(self):
        if self.peek() == '{':
            return ('scope', self.block())
        return super().statement()


class Backend(scalar.Backend):
    def __init__(self, *args):
        super().__init__(*args)
        self.lexical_scopes = []

    def condition(self, expression, names):
        if expression[0:2] == ('binary', '<='):
            left, right = expression[2:]
            if left[0] != 'variable' or left[1] not in names:
                raise ValueError('Context-word <= requires an initialized numeric byte')
            descriptor = names[left[1]]
            if descriptor.get('provenance') != 'get_numeric_state':
                raise ValueError('Context-word ordered relation requires numeric-byte provenance')
            value = self.constant(right)
            if abs(value) > 1 << 24:
                raise ValueError('Nonexact context-word comparison constant')
            site = self.base + self.emit(1044, 24, 0, prior.fword(descriptor['slot']), 2, prior.fword(value))
            self.object_accesses.append({'name': left[1], 'scope': descriptor['scope'], 'access': 'read',
                'sitePc': site, 'relation': '<=', 'constant': value})
            return
        super().condition(expression, names)

    def block(self, statements, environment):
        names = dict(environment)
        for statement in statements:
            self.nodes += 1
            if self.nodes > 2048:
                raise ValueError('Context-word AST bound exceeded')
            kind = statement[0]
            if kind == 'read_value':
                value_type, name, api, expression = statement[1:]
                if name in self.local_names or name in self.globals_declared or name in RESERVED:
                    raise ValueError('Context-word local shadows an object or API')
                if name not in self.profile:
                    raise ValueError('Missing context-word local allocation')
                self.local_names.add(name)
                self.allocations.append({'name': name, 'slot': self.profile[name], 'sourceType': value_type,
                    'scope': 'local', 'vmRepresentation': 'IEEE754 binary32', 'vmByteOffset': 0x50 + self.profile[name] * 4})
                self.read(name, value_type, api, expression, names, 'local')
            elif kind == 'assign_getter':
                name, api, expression = statement[1:]
                if name not in names:
                    raise ValueError('Context-word assignment requires a visible object')
                descriptor = names[name]
                self.read(name, descriptor['type'], api, expression, names, descriptor['scope'])
            elif kind == 'call':
                api, arguments = statement[1:]
                if api == 'reset_context_words':
                    if arguments:
                        raise ValueError('Context-word reset takes no arguments')
                    self.emit(162, 8)
                    self.calls.append({'api': api, 'argumentCount': 0})
                elif api == 'set_context_word':
                    if len(arguments) != 2:
                        raise ValueError('Context-word setter takes two arguments')
                    index, value = self.index(arguments[0], 16), self.constant(arguments[1])
                    if not 0 <= value <= 1 << 24:
                        raise ValueError('Context-word value must be an exact nonnegative binary32 integer')
                    self.immediate_argument(0, index)
                    self.immediate_argument(1, value)
                    self.emit(161, 8)
                    self.calls.append({'api': api, 'index': index, 'value': value})
                else:
                    if api not in prior.SETTERS or len(arguments) != 2:
                        raise ValueError('Unsupported context-word API')
                    limit, value_limit, opcode = prior.SETTERS[api]
                    index, value = self.index(arguments[0], limit), self.constant(arguments[1])
                    if not 0 <= value < value_limit:
                        raise ValueError('Context-word source setter domain')
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
            elif kind == 'scope':
                start = self.base + self.emit(1024, 8)
                entry = self.emit(1036, 12, 0)
                self.fixup(entry, self.base + len(self.code), 'lexical-block-entry')
                self.block(statement[1], names)
                finish = self.emit(1036, 12, 0)
                self.fixup(finish, self.base + len(self.code), 'lexical-block-exit')
                self.lexical_scopes.append({'startPc': start, 'endExclusivePc': self.base + len(self.code),
                    'scopeKind': 'ordinary-C-compound-statement', 'vmHeaderHasNoScalarOrPersistentEffect': True})
            else:
                raise ValueError('Unsupported context-word source statement')


def compile_source(source_path, base, profile):
    source = Path(source_path).resolve()
    if type(base) is not int or not 0 <= base < 0x80000000 or base % 4:
        raise ValueError('Invalid context-word source placement')
    if not isinstance(profile, dict) or set(profile) != {'locals', 'globals'}:
        raise ValueError('Separate context-word local/global profiles required')
    locals_profile, globals_profile = profile['locals'], profile['globals']
    if not isinstance(locals_profile, dict) or not isinstance(globals_profile, dict):
        raise ValueError('Context-word profile sections must be objects')
    combined = dict(globals_profile, **locals_profile)
    if set(locals_profile) & set(globals_profile) or len(set(combined.values())) != len(combined):
        raise ValueError('Context-word storage aliases unsupported')
    if any(not isinstance(name, str) or type(slot) is not int or not 0 <= slot < 256 for name, slot in combined.items()):
        raise ValueError('Invalid context-word slot binding')
    text = source.read_text()
    include = re.match(r'\s*#include\s+"([^"\r\n]+)"\s*\n', text)
    if include is None:
        raise ValueError('One context-word ABI include required')
    header = (source.parent / include[1]).resolve()
    header.relative_to(source.parent)
    header_text = header.read_text()
    directives = [line.strip() for line in header_text.splitlines() if line.lstrip().startswith('#')]
    if directives != ['#ifndef SCR_CONTEXT_WORDS_20261030', '#define SCR_CONTEXT_WORDS_20261030', '#endif']:
        raise ValueError('Context-word ABI preprocessing')
    definitions = '\n'.join(line for line in header_text.splitlines() if not line.startswith('#'))
    if prior.core.tokens(definitions) != HEADER:
        raise ValueError('Context-word typed native ABI')
    name, ast, globals_declared = Parser(prior.core.tokens(text[include.end():])).unit()
    if set(globals_declared) != set(globals_profile) or name in RESERVED:
        raise ValueError('Context-word declared module objects and bindings differ')
    backend = Backend(base, locals_profile, globals_profile, globals_declared)
    environment = {key: {'slot': globals_profile[key], 'type': value_type, 'scope': 'module-global', 'provenance': None}
        for key, value_type in globals_declared.items()}
    backend.block(ast, environment)
    if backend.local_names != set(locals_profile) or backend.global_writes != set(globals_profile):
        raise ValueError('Unused local or unwritten context-word module object')
    backend.emit(1026)
    if base + len(backend.code) >= 0x80000000:
        raise ValueError('Context-word source range overflow')
    body = bytes(backend.code)
    return body, {'backend': 'restricted-C99-numeric-primary-context-words-SCR-v11', 'function': name,
        'sourceSha256': prior.core.digest(source.read_bytes()), 'includeSha256': prior.core.digest(header.read_bytes()),
        'compilerSha256': prior.core.digest(Path(__file__).read_bytes()), 'priorCompilerSha256': prior.core.digest(Path(scalar.__file__).read_bytes()),
        'functionBase': base, 'allocationProfile': profile, 'localAllocations': backend.allocations,
        'objectAccesses': backend.object_accesses, 'namedApiCalls': backend.calls, 'generatedBranches': backend.branches,
        'lexicalScopes': backend.lexical_scopes, 'parsedAst': ast, 'outputBytes': len(body), 'outputSha256': prior.core.digest(body),
        'generalCCompilerClaimed': False, 'orderedComparisonsRequireNumericByteProvenance': True,
        'contextWordIndexDomain': [0, 15], 'contextWordValueDomain': [0, 1 << 24], 'generatedLabelsFromSourceOnly': True}


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
