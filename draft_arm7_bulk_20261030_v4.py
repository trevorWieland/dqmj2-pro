import argparse
import concurrent.futures
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
import audit_arm7_bulk_20261030 as inventory
import draft_arm7 as host
import draft_utility as child
import arm7_bulk_source_policy_20261030 as source_policy
import utility_abi
import probe_arm7_profiles_20261030 as compiler

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/arm7-bulk-20261030'
M2C = ROOT / 'tools/m2c/m2c-c632946b8cfbe8fce442b522dba92dfa72f1f317/m2c.py'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def configure(specs, program):
    functions = {spec['address']: spec for spec in specs}
    arguments, stack = utility_abi.argument_hints(specs)
    host.FUNCTIONS, host.ARGUMENTS = functions, arguments
    host.OPTIONS = SimpleNamespace(register_order=True, native_scalar_widths=True, repair_call_prototypes=True,
        measured_stack_buffers=True, byte_addresses=True)
    child.FUNCTIONS, child.ARGUMENTS = {'arm7': functions}, {'arm7': arguments}
    child.OPTIONS = SimpleNamespace(scalar_globals=True, register_order=True, reverse_register_order=False,
        fixed_work_areas=False, direct_increments=False, typed_globals=False)
    return {'argumentCounts': {hex(address): value for address, value in arguments.items()}, 'stackEvidence': stack,
        'provisionalAbiHypothesesOnly': True, 'program': program}


def draft(spec, batch, program):
    adapter = child
    directory = WORK / batch / spec['module'] / format(spec['address'], '08x')
    directory.mkdir(parents=True, exist_ok=True)
    name = spec.get('name', 'native_' + spec['module'].replace('-', '_') + '_' + format(spec['address'], '08x'))
    spec = dict(spec, name=name, processor='arm7', mode=spec.get('mode', 'arm'), program=program)
    result = {'module': spec['module'], 'program': program, 'processor': 'arm7', 'mode': spec['mode'], 'address': hex(spec['address']),
        'bytes': spec['bytes'], 'inputModuleSha256': spec['inputModuleSha256'], 'name': name, 'variants': [], 'sourceCredit': 0}
    try:
        assembly, targets, data, declarations = adapter.assembly(spec)
    except Exception as error:
        result['assemblyConversionFailure'] = type(error).__name__ + ': ' + str(error)
        return result
    assembly_path = directory / 'generated-native.s'
    assembly_path.write_text(assembly)
    result['generatedAssembly'] = {'path': assembly_path.relative_to(ROOT).as_posix(), 'sha256': digest(assembly_path.read_bytes()), 'sourceCredit': 0}
    for returns in ('u32', 'void'):
        context = directory / (returns + '-context.c')
        context.write_text(adapter.PRELUDE + '\n'.join(declarations) + '\nextern ' + returns + ' ' + adapter.symbol(spec) + '();\n')
        command = [sys.executable, str(M2C), '--target', 'arm-mwcc-c', '--context', str(context), '--globals', 'none', '--no-cache',
            '--valid-syntax', '--comment-style', 'none', '-f', adapter.symbol(spec), str(assembly_path)]
        record = {'returnHypothesis': returns, 'command': command, 'cwd': str(ROOT), 'contextSha256': digest(context.read_bytes())}
        result['variants'].append(record)
        try:
            process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=45,
                env=dict(os.environ, PYTHONPATH=str(ROOT / 'tools/m2c-python')))
            record.update(exitCode=process.returncode, stdout=process.stdout, stderr=process.stderr)
            if process.returncode:
                continue
            source_policy.require(process.stdout, process.stderr)
            text = adapter.recovered_source(process.stdout, spec, targets, data)
            source_policy.require(text, process.stderr)
            if re.search(r'\bNULL\b', text) and '#define NULL' not in text:
                text = '#define NULL ((void *)0)\n' + text
            if not program:
                text = re.sub(r'\b(native_utility_child_arm7_)', 'native_host_arm7_', text)
            if re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b', text) or len(text.splitlines()) > 500:
                raise ValueError('Ordinary C/physical-line policy failure')
            output = ROOT / 'nonmatching/arm7-bulk/20261030' / batch / spec['module']
            output.mkdir(parents=True, exist_ok=True)
            source = output / (name + '-' + returns + '-' + digest(text.encode())[:12] + '.c')
            if source.exists() and source.read_text() != text:
                raise ValueError('Refusing to overwrite a different broad draft')
            source.write_text(text)
            record.update(source=source.relative_to(ROOT).as_posix(), sourceSha256=digest(source.read_bytes()), ordinaryCHypothesis=True,
                argumentAndReturnContractsStillProvisional=True, sourceCredit=0)
            row = {key: spec[key] for key in ('program', 'processor', 'module', 'name', 'mode', 'bytes', 'binary', 'base', 'inputModuleSha256')}
            row['address'] = hex(spec['address'])
            origin = {'source': record['source'], 'sourceSha256': record['sourceSha256']}
            record['initialCompilerProbe'] = compiler.compile_source(row, origin, source, compiler.PROFILES[0], directory)
        except Exception as error:
            record['failure'] = type(error).__name__ + ': ' + str(error)
    (directory / 'draft.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', required=True)
    parser.add_argument('--namespace', choices=('host', 'child'), required=True)
    parser.add_argument('--limit', type=int, default=240)
    parser.add_argument('--max-bytes', type=int, default=4096)
    parser.add_argument('--offset', type=int, default=0)
    args = parser.parse_args()
    if not re.fullmatch('[a-z0-9-]+', args.batch):
        raise ValueError('Exclusive simple batch required')
    directory = WORK / args.batch
    directory.mkdir(parents=True, exist_ok=True)
    if (directory / 'results.json').exists():
        raise ValueError('Choose a new broad drafting batch')
    program = '' if args.namespace == 'host' else 'dwc/utility.bin/move/child.srl'
    current = json.loads((WORK / 'inventory.json').read_text())
    eligible = {(row['program'], row['module'], int(row['address'], 0), row['mode']): row for row in current['remainingHeuristicCandidates']}
    all_specs = [spec for spec in inventory.specs() if spec.get('program', '') == program]
    context = configure(all_specs, program)
    (directory / 'argument-context.json').write_text(json.dumps(context, indent=2) + '\n')
    selected = [spec for spec in all_specs if inventory.identity(spec) in eligible and spec['bytes'] <= args.max_bytes]
    selected.sort(key=lambda spec: (bool(eligible[inventory.identity(spec)]['sourceDrafts']), -spec['bytes']))
    selected = selected[args.offset:args.offset + args.limit]
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(lambda spec: draft(spec, args.batch, program), selected):
            results.append(result)
            compiled = [row for row in result['variants'] if row.get('initialCompilerProbe', {}).get('exitCode') == 0]
            if len(results) % 20 == 0 or any(row.get('initialCompilerProbe', {}).get('relocationOnlyCandidate') for row in result['variants']):
                print(json.dumps({'processed': len(results), 'module': result['module'], 'address': result['address'], 'bytes': result['bytes'],
                    'compileableVariants': len(compiled), 'relocationOnlyCandidate': any(row.get('initialCompilerProbe', {}).get('relocationOnlyCandidate') for row in result['variants'])}), flush=True)
    candidates = [row['initialCompilerProbe'] for result in results for row in result['variants'] if row.get('initialCompilerProbe', {}).get('relocationOnlyCandidate')]
    report = {'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()), 'program': program, 'results': results,
        'relocationOnlyCandidates': candidates, 'sourceCredit': 0, 'generatedAssemblySourceCredit': 0, 'newExactMatchCredit': 0,
        'abiHypothesesOnly': True, 'actualFullLinkBoundaryAbiAndNativeChecksStillRequired': True}
    (directory / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'functionsDrafted': sum(any(row.get('source') for row in result['variants']) for result in results),
        'functionsCompileable': sum(any(row.get('initialCompilerProbe', {}).get('exitCode') == 0 for row in result['variants']) for result in results),
        'relocationOnlyCandidates': len(candidates), 'sourceCredit': 0}), flush=True)


if __name__ == '__main__':
    main()
