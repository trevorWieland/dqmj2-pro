import argparse
import ast
import concurrent.futures
import hashlib
import inspect
import json
import os
import re
import subprocess
import sys
from types import SimpleNamespace
from project import ROOT, read_json, sha256, write_json

BASE = ROOT / 'nonmatching/overlay-lane/20261102-battle835'
PLAN = ROOT / 'evidence/attempts/ov006-breadth835-plan-20261102.json'
TARGETS = [(int(row['address'], 0), row['bytes']) for row in read_json(PLAN)['selected']]
SNAPSHOT = ROOT / read_json(PLAN)['snapshot']


def options():
    return SimpleNamespace(module='ov006', thumb=False, source_returns=False, word_args=True, abi_slots=True, register_order=False, stack_buffers=True, direct_increments=False, typed_globals=False)


def measured_word_views(text, prefix='func_'):
    edits = []
    contracts = [('0205d790', 1), ('ov001_021db438', 2), ('ov001_021db8d0', 1), ('ov001_021e1950', 4), ('ov001_021eeb70', 1)]
    for suffix, count in contracts:
        name = prefix + suffix
        pattern = r'extern [^;\n]*\b' + re.escape(name) + r'\([^;]*\);'
        match = re.search(pattern, text)
        if match:
            declaration = 'extern u32 ' + name + '(' + ','.join(['u32'] * count) + ');'
            edits.append(dict(symbol=name, before=match.group(0), after=declaration, qualification='Measured raw incoming-word view; original formal types and complete downstream contracts remain separate.'))
            text = text[:match.start()] + declaration + text[match.end():]
    return text, edits


def source_word_hypotheses(context):
    import source_word_inputs_20261031 as W
    catalogue = read_json(ROOT / 'evidence/verification/source-word-inputs83-20261031.json')
    references = set(re.findall(r'\b(?:func|native_fn)_(?:(?:ov\d{3})_)?([0-9a-f]{8})\b', context))
    rows = []
    rejected = []
    for row in catalogue['functions']:
        if f"{row['identity']['address']:08x}" not in references:
            continue
        path = ROOT / row['source']
        if not path.is_file() or sha256(path) != row['sourceSha256']:
            rejected.append(dict(identity=row['identity'], source=row['source'], reason='Local historical source absent or hash differs; projection skipped.'))
            continue
        rows.append(row)
    result, edits = W.apply_context(context, dict(functions=rows), processor='arm9', program='')
    return result, edits, rejected


def prepare():
    import draft_runtime as D
    import qualified_call_contexts_20261031 as Q
    from link_runtime_unit import measured_module
    if (BASE / 'queue.json').exists():
        raise ValueError('835 queue already exists')
    D.OPTIONS = options()
    D.WORK = ROOT / 'work/ol835/prepare'
    D.inputs()
    moduleInfo, image, _ = measured_module('ov006')
    accepted = read_json(SNAPSHOT)['functions']
    entries = []
    for address, size in TARGETS:
        for row in accepted:
            if row.get('module') == 'ov006' and row.get('processor') == 'arm9' and not row.get('program'):
                other = int(str(row['address']), 0)
                length = row.get('bytes') or 0
                if other == address or max(address, other) < min(address + size, other + length):
                    raise ValueError(('835 accepted overlap', row))
        original = f'func_ov006_{address:08x}'
        assembly, context = D.FUNCTION_INPUTS[original]
        context, edits = Q.apply(context, 'ov006', Q.catalogue())
        context, wordEdits = measured_word_views(context)
        context, sourceWordEdits, skippedSourceWords = source_word_hypotheses(context)
        directory = BASE / f'{address:08x}'
        directory.mkdir(parents=True, exist_ok=True)
        (directory / 'input.s').write_text(assembly)
        (directory / 'context.c').write_text(context)
        profiles = ['strong']
        if address == 0x021E6A6C:
            prototype = f'extern u32 {original}(u32,u32,u32,u32,u32,u32,u32);'
            physical = context.replace(f'extern u32 {original}();', prototype)
            if physical == context:
                raise ValueError('835 own physical prototype absent')
            (directory / 'physical7-context.c').write_text(physical)
            profiles.append('physical7')
        entries.append(dict(processor='arm9', program='', module='ov006', mode='arm', address=hex(address), bytes=size, original=original, moduleSha256=moduleInfo['sha256'], nativeSpanSha256=hashlib.sha256(image[address - 0x021D7240:address - 0x021D7240 + size]).hexdigest(), directory=directory.relative_to(ROOT).as_posix(), profiles=profiles, strongEdits=edits, measuredWordViews=wordEdits, sourceWordHypotheses=sourceWordEdits, skippedSourceViews=skippedSourceWords, inputFiles=[dict(path=p.relative_to(ROOT).as_posix(), sha256=sha256(p)) for p in directory.iterdir() if p.is_file()], sourceCredit=0))
    write_json(BASE / 'queue.json', dict(schemaVersion=1, sourceCredit=0, acceptedSnapshot=SNAPSHOT.relative_to(ROOT).as_posix(), acceptedSnapshotSha256=sha256(SNAPSHOT), functions=entries, originalFrontendSha256=sha256(ROOT / 'draft_runtime.py'), limits=['All source remains unaccepted hypotheses.', 'E6A6C minimum seven raw physical words follows frame1D0 and loadSP+1D8; original formal types/aggregate layout and remaining inputs unqualified.']))


def unrestricted_source_text(D, text, original):
    tree = ast.parse(inspect.getsource(D.source_text))
    function = tree.body[0]
    removed = []
    for node in function.body:
        if isinstance(node, ast.If) and any(isinstance(child, ast.Constant) and child.value == 'Recovered routine exceeds physical-line limit before refactoring' for child in ast.walk(node)):
            removed.append(node)
    if len(removed) != 1:
        raise ValueError('835 local pre-fragment guard shape changed')
    function.body = [node for node in function.body if node not in removed]
    namespace = dict(D.__dict__)
    exec(compile(tree, '<835-local-large-file-adapter>', 'exec'), namespace)
    return namespace['source_text'](text, original)



def compile_hypothesis(source, entry, profile):
    import match_runtime as c
    from link_runtime_unit import validate
    from recover_linked_runtime import qualified_bindings
    from elftools.elf.elffile import ELFFile
    attempts = []
    target = f"native_ov006_{int(entry['address'], 0):08x}"
    for speed in [False, True]:
        directory = ROOT / 'work/ol835' / entry['address'][2:] / profile / str(speed)
        c.WORK = directory / 'compile'
        attempt = dict(speed=speed, sourceCredit=0, semanticTested=False)
        try:
            rows, unused = c.compare(source, 'ov006', '2', 'off', speed)
            attempt['rows'] = []
            for row in rows:
                record = dict(source=row, compilerSucceeded=not row.get('compileFailed'))
                if not row.get('compileFailed'):
                    try:
                        record['genuineLink'] = validate(row, qualified_bindings(row), directory / 'link')
                    except Exception as error:
                        record['genuineLink'] = error.args[0] if error.args and isinstance(error.args[0], dict) else dict(failure=str(error))
                attempt['rows'].append(record)
        except Exception as error:
            attempt['failure'] = str(error)
            objects = []
            for path in c.WORK.glob('objects/*.o'):
                with path.open('rb') as stream:
                    elf = ELFFile(stream)
                    table = elf.get_section_by_name('.symtab')
                    found = table and any(symbol.name == target and symbol['st_size'] > 0 for symbol in table.iter_symbols())
                    if found and elf.elfclass == 32 and elf['e_machine'] == 'EM_ARM':
                        objects.append(dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)))
            attempt['compilerOnlyObjects'] = objects
            attempt['compilerOnlyObserved'] = bool(objects)
        attempts.append(attempt)
    return attempts


def one(index):
    import draft_runtime as D
    import qualified_call_contexts_20261031 as Q
    from sweep_overlay_signed_remainder565_20261101 import repaired
    queue = read_json(BASE / 'queue.json')
    if sha256(ROOT / 'draft_runtime.py') != queue['originalFrontendSha256']:
        raise ValueError('835 frozen frontend differs')
    entry = queue['functions'][index]
    directory = ROOT / entry['directory']
    for item in entry['inputFiles']:
        if sha256(ROOT / item['path']) != item['sha256']:
            raise ValueError('835 preparation input changed')
    D.OPTIONS = options()
    D.FUNCTION_ADDRESSES[entry['original']] = f"{int(entry['address'], 0):08x}"
    D.FUNCTION_INPUTS[entry['original']] = ((directory / 'input.s').read_text(), '')
    results = []
    for profile in entry['profiles']:
        variant = directory / profile
        variant.mkdir(parents=True, exist_ok=True)
        context = directory / ('physical7-context.c' if profile == 'physical7' else 'context.c')
        command = [sys.executable, str(D.M2C), '--target', 'arm-mwcc-c', '--comment-style', 'none', '--no-cache', '--valid-syntax', '--context', str(context), '-f', entry['original'], str(directory / 'input.s')]
        output = subprocess.run(command, cwd=ROOT, env=dict(os.environ, PYTHONPATH=str(ROOT / 'tools/m2c-python')), capture_output=True, text=True, timeout=120)
        (variant / 'generated-output.txt').write_text(output.stdout)
        (variant / 'generated-errors.txt').write_text(output.stderr)
        item = dict(profile=profile, command=command, frontendExitCode=output.returncode, sourceCredit=0)
        try:
            if output.returncode:
                raise ValueError('835 m2c failed')
            combined, fixes = repaired(unrestricted_source_text(D, output.stdout, entry['original']))
            contracts = []
            for contract in Q.catalogue():
                contract = dict(contract)
                for key in ['alias', 'contextPrototype']:
                    contract[key] = contract[key].replace('func_', 'native_fn_')
                contracts.append(contract)
            combined, compilerEdits = Q.apply(combined, 'ov006', contracts)
            combined, compilerWordEdits = measured_word_views(combined, 'native_fn_')
            combined, compilerSourceWordEdits, compilerSkipped = source_word_hypotheses(combined)
            target = f"native_ov006_{int(entry['address'], 0):08x}"
            match = re.search(r'(?m)^[^\n;]*\b' + target + r'\(', combined)
            if not match:
                raise ValueError('835 target definition absent')
            body = combined[match.start():]
            header = variant / 'context.h'
            header.write_text(combined[:match.start()])
            source = variant / 'source.c'
            fragments = []
            if len(body.splitlines()) <= 480:
                source.write_text('#include "context.h"\n' + body)
            else:
                first, last = body.index('{') + 1, body.rindex('}')
                middle = body[first:last].splitlines()
                for offset in range(0, len(middle), 350):
                    fragment = variant / f'body_{offset // 350:02d}.inc'
                    fragment.write_text('\n'.join(middle[offset:offset + 350]) + '\n')
                    fragments.append(fragment)
                source.write_text('#include "context.h"\n' + body[:first] + '\n' + '\n'.join('#include "' + p.name + '"' for p in fragments) + '\n' + body[last:])
            closure = [source, header] + fragments
            if any(len(path.read_text().splitlines()) > 500 for path in closure):
                raise ValueError('835 formatted source closure exceeds500 lines')
            item.update(materialized=True, unresolvedSavedRegisters=sorted(set(re.findall(r"\bsaved_reg_(r\d+)\b", body))), compilerContextEdits=compilerEdits, compilerWordViews=compilerWordEdits, compilerSourceWordHypotheses=compilerSourceWordEdits, signedRemainderRepairs=fixes, sourceClosure=[dict(path=p.relative_to(ROOT).as_posix(), sha256=sha256(p)) for p in closure])
            item['compilerAttempts'] = compile_hypothesis(source, entry, profile)
        except Exception as error:
            item['failure'] = str(error)
        results.append(item)
    write_json(directory / 'draft-results.json', dict(identity=entry, results=results, sourceCredit=0))
    print(entry['original'], [(item['profile'], item.get('materialized', False), item.get('failure')) for item in results], flush=True)


def run():
    functions = read_json(BASE / 'queue.json')['functions']
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        pending = [pool.submit(subprocess.run, [sys.executable, __file__, '--one', str(index)], cwd=ROOT, capture_output=True, text=True) for index in range(len(functions))]
        for future in concurrent.futures.as_completed(pending):
            result = future.result()
            print(result.stdout, result.stderr[:1500], flush=True)
            if result.returncode:
                raise ValueError('835 isolated draft worker failed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--one', type=int)
    args = parser.parse_args()
    if args.prepare:
        prepare()
    if args.one is not None:
        one(args.one)
    if args.run:
        run()
