import argparse
import functools
import json
import random
import re
import struct
from pathlib import Path
from project import ROOT, configuration, now, read_json, sha256, write_json
from link_runtime_unit import measured_module, validate, verify_binding
from reuse_overlay_c import call_targets, compile_entry
from save_link_snapshots import freeze_link
import match_runtime as compiler
from elftools.elf.elffile import ELFFile


@functools.cache
def native_functions(module):
    metadata, binary, config = measured_module(module)
    functions = {int(address, 16): mode for mode, address in re.findall(
        r'^\S+ kind:function\((arm|thumb),size=0x[0-9a-f]+\) addr:0x([0-9a-f]{8})$', config, re.M)}
    return metadata, binary, functions


def qualified_bindings(entry):
    result = {}
    for relocation in entry['relocations']:
        name, address = relocation['symbol'], int(relocation['target'], 0)
        function = relocation['type'] in (1, 10, 28, 29) or name.startswith(('native_fn_', 'func_'))
        qualified = re.search(r'(?:^|_)(ov[0-9]{3})_', name)
        module = qualified[1] if qualified else entry['module'] if address >= 0x021d7240 and entry['module'].startswith('ov') else 'itcm' if 0x01ff8000 <= address < 0x02000000 else 'main'
        mode = native_functions(module)[2].get(address & ~1) if function else 'data'
        if mode is None:
            from native_alternate_entries import binding as alternate_binding
            alternate = alternate_binding(module, address & ~1)
            if alternate is None:
                raise ValueError(f'No qualified native function entry for {name} in {module}')
            verify_binding(name, alternate)
            result[name] = alternate
            continue
        binding = {'processor': 'arm9', 'module': module, 'mode': mode,
                   'kind': 'function' if function else 'data', 'address': hex(address & ~1 if function else address)}
        verify_binding(name, binding)
        if name in result and result[name] != binding:
            raise ValueError('Conflicting target identities within one source unit')
        result[name] = binding
    return result


def relocation_only_candidate(entry):
    obj = ROOT / entry['object']
    if sha256(obj) != entry['objectSha256']:
        raise ValueError('Historical object identity changed')
    with obj.open('rb') as stream:
        elf = ELFFile(stream)
        symbol = next(value for value in elf.get_section_by_name('.symtab').iter_symbols() if value.name == entry['name'])
        offset = symbol['st_value'] & ~1
        code = elf.get_section(symbol['st_shndx']).data()[offset:offset + symbol['st_size']]
    metadata, binary, functions = native_functions(entry['module'])
    start = int(entry['address'], 0) - int(metadata['base'], 0)
    native = binary[start:start + entry['bytes']]
    covered = {offset + index for row in entry['relocations'] for offset in [row['offset']] for index in range(4)}
    if len(code) != len(native) or any(a != b for index, (a, b) in enumerate(zip(code, native)) if index not in covered):
        raise ValueError('Candidate differs outside declared relocations; no source credit')


def execute_fixtures(entry, code, native, bindings):
    rng = random.Random(20261029028 + int(entry['address'], 0))
    callees = call_targets(entry, bindings)
    modes = {int(binding['address'], 0): binding['mode'] for binding in bindings.values() if binding['kind'] == 'function'}
    passed, unsupported = [], []
    for index in range(32):
        buffers = [0x03002000, 0x03004000, 0x03008000, 0x0300a000]
        memory = {address: bytes(4096) for address in buffers}
        if index % 2:
            for number, address in enumerate(buffers):
                memory[address] = struct.pack('<I', buffers[(number + 1) % 4]) * 1024
        memory[0x0301f000] = bytes(4096)
        registers = [rng.getrandbits(32) for unused in compiler.REGISTERS]
        registers[:4] = buffers if index < 16 else [index % 4, buffers[1], buffers[2], index % 7]
        registers[-2:] = [0x0301fff0, 0x04000000]
        flags = rng.getrandbits(4) << 28 | 0x10
        try:
            original = compiler.execute(native, int(entry['address'], 0), registers, memory, flags, callees, index, entry['mode'], modes)
        except AssertionError:
            raise
        except Exception as error:
            unsupported.append({'vector': index, 'nativeFailure': f'{type(error).__name__}: {error}'})
            continue
        rebuilt = compiler.execute(code, int(entry['address'], 0), registers, memory, flags, callees, index, entry['mode'], modes)
        if original != rebuilt:
            raise ValueError('Linked C differs in an actually returning isolated fixture')
        passed.append(compiler.sha(json.dumps(original, sort_keys=True).encode()))
    return {'supportedReturningVectors': len(passed), 'nativeAndCompiledReturningCalls': len(passed) * 2,
            'unsupportedVectors': unsupported, 'stateSha256': passed, 'actualReturnRequiredForSupportedVectors': True,
            'freshMachinePerExecution': True, 'instructionLimit': 2000, 'calleeEntryModesChecked': True,
            'externalCallContracts': {hex(address): {'symbol': name, 'mode': modes[address]} for address, name in callees.items()},
            'externalCalleesExecutedNatively': False,
            'limitations': ['Only caller behavior under deterministic synthetic provider contracts is exercised',
                            'Unsupported native fixtures are retained as failures of fixture coverage, not successful executions',
                            'Callee bodies, physical hardware, valid game object domains and game-level semantics are not established']}


def replay_entry(old, batch):
    source = ROOT / old['source']
    if sha256(source) != old['sourceSha256']:
        raise ValueError('Frozen source changed')
    spec = {'module': old['module'], 'name': old['name'], 'mode': old['mode']}
    rows, unused = compile_entry(source, spec, old)
    entry = next((row for row in rows if row.get('name') == old['name']), None)
    if entry is None or entry['compilerFlags'] != old['compilerFlags']:
        raise ValueError('Fresh compiler settings or caller symbol changed')
    for field in ('sourceSha256', 'address', 'mode', 'bytes', 'targetSha256'):
        if entry[field] != old[field]:
            raise ValueError('Fresh source/native identity changed: ' + field)
    bindings = qualified_bindings(entry)
    if old.get('nativeSymbolEntries') and bindings != old['nativeSymbolEntries']:
        raise ValueError('Qualified native dependency identity changed')
    directory = ROOT / 'work/runtime-recovery/linked-callers' / batch / entry['name']
    proof = validate(entry, bindings, directory)
    code = (directory / 'caller.bin').read_bytes()
    metadata, binary, functions = native_functions(entry['module'])
    start = int(entry['address'], 0) - int(metadata['base'], 0)
    native = binary[start:start + entry['bytes']]
    oracle = execute_fixtures(entry, code, native, bindings)
    for relocation in entry['relocations']:
        binding = bindings[relocation['symbol']]
        relocation.update(targetModule=binding['module'], targetMode=binding['mode'])
    return {**old, **entry, 'prelinkMatchingBytes': entry['matchingBytes'], 'matchingBytes': entry['bytes'],
            'exactAfterDeclaredRelocation': True, 'outputSha256': sha256(directory / 'caller.bin'),
            'nativeSymbolEntries': bindings, 'qualifiedDependencies': bindings, 'sourceLanguage': 'C',
            'ordinaryCOnly': True, 'realLinkInterworkingRequired': True, 'isolatedCallerRealLink': proof,
            **freeze_link(proof), 'oracle': oracle, 'linked': False,
            'calleeCodeOrSourceCredit': 0, 'sourceReconstructionComplete': False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--module', choices=['main', 'ov001', 'ov005', 'ov006'], required=True)
    parser.add_argument('--batch', required=True)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--input', type=Path, default=ROOT / 'evidence/attempts/interworking-near-candidates-20261029.json')
    options = parser.parse_args()
    if not re.fullmatch(r'[a-z0-9-]+', options.batch):
        raise ValueError('Invalid private batch name')
    path = ROOT / f'evidence/matches/{options.module}-{options.batch}.json'
    if options.verify:
        report = read_json(path)
        report['matches'] = [replay_entry(entry, options.batch) for entry in report['matches']]
    else:
        from ledger_state import collect_matches
        known, rejected = collect_matches(configuration()['romSha256'])
        spans = [(address, address + entry['size']) for (module, mode, address), entry in known.items() if module == options.module]
        reserved = read_json(ROOT / 'recovery-ownership.json').get('mainReservedRanges', []) if options.module == 'main' else []
        spans.extend((int(row['start'], 0), int(row['end'], 0)) for row in reserved)
        matches, failures = [], []
        for row in read_json((ROOT / options.input).resolve())['candidates']:
            old = row['entry']
            if old['module'] != options.module:
                continue
            start, end = int(old['address'], 0), int(old['address'], 0) + old['bytes']
            if any(start < right and left < end for left, right in spans):
                continue
            source = ROOT / old['source']
            try:
                if sha256(source) != old['sourceSha256']:
                    raise ValueError('Candidate source changed since measured compilation')
                text = source.read_text()
                if len(text.splitlines()) > 500 or re.search(r'\b(?:asm|__asm|__asm__)\b|/\*|//', text):
                    raise ValueError('Candidate is not comment-free ordinary C within the file limit')
                relocation_only_candidate(old)
                bindings = qualified_bindings(old)
                validate(old, bindings, ROOT / 'work/runtime-recovery/linked-candidates' / options.batch / old['name'])
                target = ROOT / 'src/runtime' / options.batch / (old['name'] + '.c')
                target.parent.mkdir(parents=True, exist_ok=True)
                if target.exists() and target.read_bytes() != source.read_bytes():
                    raise ValueError('A frozen source destination already differs')
                target.write_bytes(source.read_bytes())
                frozen = {**old, 'source': target.relative_to(ROOT).as_posix(), 'sourceSha256': sha256(target)}
                entry = replay_entry(frozen, options.batch)
                matches.append(entry)
                spans.append((start, end))
                print({'name': entry['name'], 'bytes': entry['bytes'], 'returningVectors': entry['oracle']['supportedReturningVectors']}, flush=True)
            except Exception as error:
                failures.append({'name': old['name'], 'input': row['input'], 'failure': f'{type(error).__name__}: {error}', 'sourceCredit': 0})
        metadata, binary, functions = native_functions(options.module)
        report = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
                  'module': options.module, 'moduleInputSha256': metadata['sha256'], 'matches': matches,
                  'attempts': failures, 'candidateInput': options.input.relative_to(ROOT).as_posix() if options.input.is_absolute() else options.input.as_posix(),
                  'candidateInputSha256': sha256((ROOT / options.input).resolve()),
                  'wholeModuleLinked': False, 'sourceReconstructionComplete': False}
    report['nativeSymbols'] = {rel['symbol']: rel['target'] for entry in report['matches'] for rel in entry['relocations']}
    write_json(path, report)
    print({'matchedFunctions': len(report['matches']), 'bytes': sum(entry['bytes'] for entry in report['matches']),
           'failedCandidates': len(report.get('attempts', [])), 'sourceReconstructionComplete': False})


if __name__ == '__main__':
    main()
