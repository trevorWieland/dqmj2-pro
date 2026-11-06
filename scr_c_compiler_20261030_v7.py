import argparse
import hashlib
import json
import re
from pathlib import Path
import scr_c_compiler_20261029_v4 as prior

assert hashlib.sha256(Path(prior.__file__).read_bytes()).hexdigest() == '171818c7eda16c5d44e098a45ec425b268730a38e5f5696b73e19ce5e06b9de7'
LINK_TYPES = {'reset_shared_flags': [], 'advance_world_numeric_state': [], 'refresh_shared_context': [],
              'run_world_context_updates': [], 'apply_saved_world_argument': ['float'],
              'before_primary_flag_reset': [], 'finalize_world_state': []}
HEADER = prior.HEADER[:prior.HEADER.index(';') + 1] + prior.core.tokens('''
void set_primary_flag(int index, bool enabled);
void set_numeric_state(int index, float value);
void reset_runtime_counter(float blocks);
float sample_signed_random(float bound);
bool runtime_counter_at_threshold(void);
void reset_shared_flags(void);
void advance_world_numeric_state(void);
void refresh_shared_context(void);
void run_world_context_updates(void);
void apply_saved_world_argument(float value);
void before_primary_flag_reset(void);
void finalize_world_state(void);
''')
RESERVED = set(LINK_TYPES) | {'false', 'true', 'set_primary_flag', 'set_numeric_state',
                            'reset_runtime_counter', 'sample_signed_random', 'runtime_counter_at_threshold'}


class Parser(prior.core.Parser):
    def statement(self):
        if self.peek() not in ('float', 'bool'):
            return super().statement()
        value_type, name = self.take(), self.identifier()
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
        return ('native_read', value_type, name, api, arguments)

    def unit(self):
        self.take('void')
        name = self.identifier()
        self.take('(')
        self.take('float')
        formal = self.identifier()
        self.take(')')
        body = self.block()
        if self.peek() is not None:
            raise ValueError('Exactly one reset-caller definition required')
        if name in RESERVED or formal in RESERVED or name == formal:
            raise ValueError('Reserved or shadowed reset-caller symbol')
        return name, formal, body


class Backend(prior.Backend):
    def __init__(self, base, profile, links, formal):
        super().__init__(base, profile)
        self.links, self.names = links, {}
        self.allocate(formal, 'float', 'formal-argument-0', None)
        self.emit(1045, 24, 0, prior.fword(profile[formal]), 1, prior.fword(0))

    def allocate(self, name, value_type, provenance, domain):
        if name in self.names or name in RESERVED or name not in self.profile:
            raise ValueError('Missing, shadowed or reserved reset-caller local')
        slot = self.profile[name]
        self.names[name] = {'slot': slot, 'type': value_type, 'provenance': provenance, 'domain': domain}
        self.allocations.append({'name': name, 'slot': slot, 'sourceType': value_type, 'provenance': provenance,
                                 'domain': domain, 'vmRepresentation': 'IEEE754 binary32', 'vmByteOffset': 0x50 + slot * 4})

    def argument(self, register, expression, domain=None):
        if expression[0] == 'variable' and expression[1] in self.names:
            item = self.names[expression[1]]
            if domain is not None and (item['domain'] is None or item['domain'][0] < domain[0] or item['domain'][1] > domain[1]):
                raise ValueError('Runtime argument lacks the required value-domain proof')
            self.emit(1045, 24, 1, prior.fword(register), 0, prior.fword(item['slot']))
            return {'variable': expression[1], 'slot': item['slot']}
        value = self.constant(expression)
        if domain is not None and not domain[0] <= value <= domain[1]:
            raise ValueError('Constant runtime argument outside supported domain')
        if abs(value) > 1 << 24:
            raise ValueError('Nonexact binary32 argument')
        self.immediate_argument(register, value)
        return {'constant': value}

    def call(self, name, arguments):
        if name in ('set_primary_flag', 'set_numeric_state'):
            if len(arguments) != 2:
                raise ValueError('State setter arity')
            primary = name == 'set_primary_flag'
            index = self.index(arguments[0], 1536 if primary else 88)
            self.immediate_argument(0, index)
            value = self.argument(1, arguments[1], (0, 1) if primary else (0, 255))
            self.emit(42 if primary else 40, 8)
            self.calls.append({'api': name, 'index': index, 'value': value})
        elif name == 'reset_runtime_counter':
            if len(arguments) != 1 or self.constant(arguments[0]) != 0:
                raise ValueError('Only independently qualified zero counter reset is supported')
            self.immediate_argument(0, 0)
            self.emit(43, 8)
            self.calls.append({'api': name, 'value': 0})
        elif name in self.links:
            link = self.links[name]
            if len(arguments) != len(link['argumentTypes']):
                raise ValueError('Qualified script-call arity')
            values = [self.argument(index, expression) for index, expression in enumerate(arguments)]
            site = self.base + self.emit(1033, 12, link['entryPc'])
            self.calls.append({'api': name, 'arguments': values, 'kind': 'qualified-script-call',
                               'sitePc': site, 'binding': link})
        else:
            raise ValueError('Unsupported reset-caller API')

    def block(self, statements):
        for statement in statements:
            self.nodes += 1
            if self.nodes > 2048:
                raise ValueError('Reset-caller AST bound')
            kind = statement[0]
            if kind == 'native_read':
                value_type, name, api, args = statement[1:]
                if api == 'sample_signed_random' and value_type == 'float' and len(args) == 1:
                    bound = self.constant(args[0])
                    if not 0 < bound <= 256:
                        raise ValueError('Only qualified positive byte-bounded random values supported')
                    self.allocate(name, value_type, api, [0, bound - 1])
                    self.immediate_argument(0, bound)
                    self.emit(36, 8)
                    arguments = [bound]
                elif api == 'runtime_counter_at_threshold' and value_type == 'bool' and not args:
                    self.allocate(name, value_type, api, [0, 1])
                    self.emit(48, 8)
                    arguments = []
                else:
                    raise ValueError('Unsupported typed native getter')
                self.emit(1045, 24, 0, prior.fword(self.profile[name]), 1, prior.fword(0))
                self.calls.append({'api': api, 'arguments': arguments, 'resultVariable': name})
            elif kind == 'call':
                self.call(statement[1], statement[2])
            elif kind == 'for':
                prior.core.validate_ast([statement], set(self.names) | RESERVED)
                lowerer = prior.core.Lowerer()
                lowerer.block([statement], {'false': 0, 'true': 1})
                for call in lowerer.calls:
                    self.call('set_primary_flag', [('constant', call['index']), ('constant', call['enabled'])])
            else:
                raise ValueError('Only straight-line typed calls and constant primary-reset loops supported')


def compile_source(source_path, base, profile, links):
    source = Path(source_path).resolve()
    if type(base) is not int or not 0 <= base < 0x80000000 or base % 4:
        raise ValueError('Invalid reset-caller placement')
    if not isinstance(profile, dict) or any(not isinstance(name, str) or type(slot) is not int or not 0 <= slot < 256 for name, slot in profile.items()):
        raise ValueError('Invalid reset-caller local allocation')
    if len(set(profile.values())) != len(profile):
        raise ValueError('Reset-caller local aliases')
    if not isinstance(links, dict) or set(links) != set(LINK_TYPES):
        raise ValueError('Exact named reset-caller link closure required')
    for name, item in links.items():
        if item.get('argumentTypes') != LINK_TYPES[name] or item.get('mode') != 'SCR' or item.get('vmHostProcessor') != 'ARM9':
            raise ValueError('Qualified reset-caller link ABI')
        if type(item.get('entryPc')) is not int or not 0 <= item['entryPc'] < 0x80000000 or item['entryPc'] % 4:
            raise ValueError('Invalid qualified script entry')
        if any(re.fullmatch('[0-9a-f]{64}', item.get(key, '')) is None for key in ('scriptSha256', 'codeSha256', 'rangeSha256')):
            raise ValueError('Missing qualified image/range hashes')
        if item.get('dependencyKind') not in ('qualified-original', 'source-linked'):
            raise ValueError('Qualified dependency evidence class')
    text = source.read_text(encoding='utf-8')
    include = re.match(r'\s*#include\s+"([^"\r\n]+)"\s*\n', text)
    if include is None:
        raise ValueError('One reset-caller ABI include required')
    header = (source.parent / include[1]).resolve()
    header.relative_to(source.parent)
    header_text = header.read_text(encoding='utf-8')
    directives = [line.strip() for line in header_text.splitlines() if line.lstrip().startswith('#')]
    if directives != ['#ifndef SCR_RESET_CALLER_20261030', '#define SCR_RESET_CALLER_20261030', '#endif']:
        raise ValueError('Reset-caller ABI preprocessing')
    if prior.core.tokens('\n'.join(line for line in header_text.splitlines() if not line.startswith('#'))) != HEADER:
        raise ValueError('Reset-caller native/script ABI prototypes')
    name, formal, ast = Parser(prior.core.tokens(text[include.end():])).unit()
    backend = Backend(base, profile, links, formal)
    backend.block(ast)
    if set(backend.names) != set(profile):
        raise ValueError('Unused local bindings')
    backend.emit(1026)
    if base + len(backend.code) >= 0x80000000:
        raise ValueError('Reset-caller function range overflow')
    output = bytes(backend.code)
    return output, {'backend': 'restricted-C99-reset-caller-SCR-v7', 'function': name, 'functionBase': base,
        'sourceSha256': prior.core.digest(source.read_bytes()), 'includeSha256': prior.core.digest(header.read_bytes()),
        'compilerSha256': prior.core.digest(Path(__file__).read_bytes()),
        'priorCompilerSha256': prior.core.digest(Path(prior.__file__).read_bytes()), 'parserSha256': prior.CORE_HASH,
        'formalArguments': [{'name': formal, 'sourceType': 'float', 'argumentRegister': 0, 'localSlot': profile[formal],
                             'copyRepresentation': 'raw IEEE754 binary32 bits'}],
        'namedAllocationProfile': profile, 'variableAllocations': backend.allocations,
        'namedApiCalls': backend.calls, 'qualifiedLinks': links, 'parsedAst': ast,
        'constantLoopsUnrolled': True, 'outputBytes': len(output), 'outputSha256': prior.core.digest(output),
        'generalCCompilerClaimed': False, 'calleeSourceCreditGrantedByBindings': False}


def main():
    parser = argparse.ArgumentParser()
    for name in ('source', 'locals', 'links', 'output', 'report'):
        parser.add_argument('--' + name, required=True)
    parser.add_argument('--base', type=lambda value: int(value, 0), required=True)
    options = parser.parse_args()
    body, report = compile_source(options.source, options.base, json.loads(Path(options.locals).read_text()),
                                  json.loads(Path(options.links).read_text()))
    Path(options.output).write_bytes(body)
    Path(options.report).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'function': report['function'], 'bytes': len(body), 'sha256': report['outputSha256']}))


if __name__ == '__main__':
    main()
