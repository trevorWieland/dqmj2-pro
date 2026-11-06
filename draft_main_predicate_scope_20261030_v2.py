import concurrent.futures
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
import arm7_bulk_source_policy_20261030 as policy
import crossreuse_utility_c
import draft_utility
import link_runtime_unit
import match_runtime
import recover_linked_runtime
from recovery_registry import entries
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/main-predicate-scope-20261030/campaign02'
SOURCE = ROOT / 'nonmatching/main-predicate-scope/20261030/campaign02'
M2C = ROOT / 'tools/m2c/m2c-c632946b8cfbe8fce442b522dba92dfa72f1f317/m2c.py'
EXCLUDED = ((0x02062000, 0x0207D000), (0x02034F90, 0x02034FF0), (0x02035018, 0x02035108), (0x0207F1EC, 0x0207F254))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def compile_profiles():
    rows = []
    for version in ('2.0/base', '2.0/sp1p5', '2.0/sp1p6'):
        compiler = ROOT / 'tools/mwccarm/mwccarm' / version / 'mwccarm.exe'
        if digest(compiler.read_bytes()) != match_runtime.COMPILER_PINS[compiler.relative_to(ROOT).as_posix()]:
            raise ValueError('Pinned main compiler changed')
        for level, inline, speed in ((2, 'off', False), (2, 'off', True), (2, 'on', True), (3, 'off', True), (4, 'off', True), (4, 'on', True)):
            flags = match_runtime.FLAGS[:]
            flags[0] = '-O' + str(level)
            flags[flags.index('-inline') + 1] = inline
            if speed:
                flags += ['-opt', 'speed']
            rows.append((compiler, flags))
    return rows


def bindings(entry, native):
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    rows = []
    for rel in entry['relocations']:
        if rel['type'] not in (1, 28, 29):
            raise ValueError('Main no-literal scope acquired an unqualified relocation')
        pc = int(entry['address'], 0) + rel['offset']
        instruction = next(decoder.disasm(native[rel['offset']:rel['offset'] + 4], pc), None)
        if instruction is None or not instruction.operands or instruction.operands[0].type != 2:
            raise ValueError('Original main branch relocation is not immediate')
        rows.append(dict(rel, target=hex(instruction.operands[0].imm & 0xFFFFFFFF)))
    entry['relocations'] = rows
    return recover_linked_runtime.qualified_bindings(entry)


def draft(spec, input_hash, compiler_settings):
    directory = WORK / format(spec['address'], '08x')
    directory.mkdir(parents=True, exist_ok=True)
    result = {'module': 'main', 'processor': 'arm9', 'program': '', 'address': hex(spec['address']), 'bytes': spec['bytes'], 'mode': 'arm',
        'variants': [], 'sourceCredit': 0, 'normalMainLinkAndNativeRequired': True}
    assembly, targets, data, declarations = draft_utility.assembly(spec)
    asm = directory / 'generated-native.s'
    asm.write_text(assembly)
    for returns in ('u32', 'void'):
        context = directory / (returns + '-context.c')
        context.write_text(draft_utility.PRELUDE + '\n'.join(declarations) + '\nextern ' + returns + ' ' + draft_utility.symbol(spec) + '();\n')
        command = [sys.executable, str(M2C), '--target', 'arm-mwcc-c', '--context', str(context), '--globals', 'none', '--no-cache',
            '--valid-syntax', '--comment-style', 'none', '-f', draft_utility.symbol(spec), str(asm)]
        variant = {'returnHypothesis': returns, 'command': command, 'cwd': str(ROOT), 'compilerAttempts': [], 'sourceCredit': 0}
        result['variants'].append(variant)
        try:
            process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=45,
                env=dict(os.environ, PYTHONPATH=str(ROOT / 'tools/m2c-python')))
            variant.update(exitCode=process.returncode, stdout=process.stdout, stderr=process.stderr)
            if process.returncode:
                continue
            policy.require(process.stdout, process.stderr)
            text = draft_utility.recovered_source(process.stdout, spec, targets, data)
            text = re.sub(r'\bnative_utility_child_arm9_(?:arm|thumb)_([0-9a-f]{8})\b', r'native_fn_\1', text)
            text = re.sub(r'\bnative_utility_child_arm9_data_([0-9a-f]{8})\b', r'native_data_\1', text)
            if 'NULL' in text and '#define NULL' not in text:
                text = '#define NULL ((void *)0)\n' + text
            policy.require(text, process.stderr)
            source = SOURCE / (spec['name'] + '-' + returns + '-' + digest(text.encode())[:12] + '.c')
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_text(text)
            variant.update(source=source.relative_to(ROOT).as_posix(), sourceSha256=digest(source.read_bytes()))
            raw = (ROOT / spec['binary']).read_bytes()
            native = raw[spec['address'] - spec['base']:spec['address'] - spec['base'] + spec['bytes']]
            for compiler, flags in compiler_settings:
                origin = {'source': variant['source'], 'sourceSha256': variant['sourceSha256'], 'name': spec['name']}
                key = digest(json.dumps([str(compiler), flags]).encode())[:16]
                output = directory / (returns + '-' + key)
                output.mkdir(parents=True, exist_ok=True)
                attempt, compiled = crossreuse_utility_c.compile_origin(origin, compiler, flags, output)
                variant['compilerAttempts'].append(attempt)
                if compiled is None:
                    continue
                derived, offsets, body = compiled
                ignored = {offset + byte for offset, mask in offsets for byte in range(4)}
                eligible = len(body) == len(native) and all(left == right for index, (left, right) in enumerate(zip(body, native)) if index not in ignored)
                attempt.update(nativeBytes=len(native), matchingBytes=sum(left == right for left, right in zip(body, native)), relocationOnlyCandidate=eligible)
                if not eligible:
                    continue
                entry = dict(origin, processor='arm9', program='', module='main', mode='arm', address=hex(spec['address']), bytes=spec['bytes'],
                    inputModuleSha256=input_hash, targetSha256=digest(native), compiler=compiler.relative_to(ROOT).as_posix(), compilerFlags=flags,
                    compilerSha256=digest(compiler.read_bytes()), object=derived['probeObject'], objectSha256=derived['probeObjectSha256'],
                    sourceDependencies=[], sourceLanguage='C', originalObjectScaffolding=False, wholeModuleLinked=False,
                    relocations=[{'offset': row['offset'], 'type': row['type'], 'symbol': row['symbol'], 'format': 'SHT_RELA',
                        'addend': row['addend'], 'explicitAddend': row['addend'], 'originalEncodedWord': body[row['offset']:row['offset'] + 4].hex()} for row in derived['relocations']])
                try:
                    qualified = bindings(entry, native)
                    proof = link_runtime_unit.validate(entry, qualified, output / 'real-main-link')
                    linked = (ROOT / proof['binary']).read_bytes() if 'binary' in proof else None
                    result.setdefault('realLinkCandidates', []).append({'entry': entry, 'qualifiedBindings': qualified, 'proof': proof,
                        'sourceCredit': 0, 'nativeAndCallContractAndBoundaryProofStillRequired': True})
                    print(json.dumps({'main': entry['address'], 'bytes': entry['bytes'], 'realMainLinkExact': True}), flush=True)
                    break
                except Exception as error:
                    attempt['realMainLinkFailure'] = type(error).__name__ + ': ' + str(error)
        except Exception as error:
            variant['failure'] = type(error).__name__ + ': ' + str(error)
    (directory / 'draft.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


def main():
    scope = json.loads((ROOT / 'work/arm9-predicate-scope-20261030/scope-v2.json').read_text())
    metadata, raw, config = link_runtime_unit.measured_module('main')
    input_hash = digest(raw)
    if scope['mainModuleSha256'] != input_hash:
        raise ValueError('Main scope differs from measured input')
    modes = {int(address, 0): mode for mode, address in re.findall(r'^\S+ kind:function\((arm|thumb),size=0x[0-9a-f]+\) addr:(0x[0-9a-f]{8})$', config, re.M)}
    draft_utility.FUNCTIONS = {'arm9': {address: {'mode': mode} for address, mode in modes.items()}}
    draft_utility.ARGUMENTS = {'arm9': {int(address, 0): row['count'] for address, row in scope['contextArgumentHints'].items() if row['analysis']['prototypeHintUsable']}}
    draft_utility.OPTIONS = SimpleNamespace(scalar_globals=True, register_order=True, reverse_register_order=False,
        fixed_work_areas=False, direct_increments=False, typed_globals=False)
    occupied = []
    for batch in json.loads((ROOT / 'recovery.json').read_text())['batches']:
        for row in entries(json.loads((ROOT / batch['report']).read_text())):
            if row.get('module') == 'main' and not row.get('program') and isinstance(row.get('bytes', row.get('size')), int):
                address = int(row['address'], 0)
                occupied.append((address, address + row.get('bytes', row.get('size'))))
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    specs = []
    for row in scope['functions']:
        address, size = int(row['address'], 0), row['bytes']
        if not row['analysis']['prototypeHintUsable'] or any(first < address + size and address < last for first, last in EXCLUDED + tuple(occupied)):
            continue
        specs.append({'module': 'main', 'program': '', 'processor': 'arm9', 'mode': 'arm', 'address': address, 'bytes': size,
            'binary': 'extract/arm9/arm9.bin', 'base': 0x02000000, 'name': 'native_main_' + format(address, '08x'),
            'instructions': list(decoder.disasm(raw[address - 0x02000000:address - 0x02000000 + size], address))})
    WORK.mkdir(parents=True, exist_ok=True)
    profiles = compile_profiles()
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(lambda spec: draft(spec, input_hash, profiles), specs))
    report = {'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()), 'results': results,
        'realLinkCandidates': [row for result in results for row in result.get('realLinkCandidates', [])], 'sourceCredit': 0,
        'assemblyScaffoldingCredit': 0, 'sourceBoundaryAbiAndActualNativeProofRequiredBeforePublication': True}
    (WORK / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'functionsConsidered': len(results), 'functionsDrafted': sum(any(row.get('source') for row in result['variants']) for result in results),
        'realMainLinkCandidates': len(report['realLinkCandidates']), 'sourceCredit': 0}), flush=True)


if __name__ == '__main__':
    main()
