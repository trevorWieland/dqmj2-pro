import contextlib
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/goal-resume-20261106/child-snd-alias-v1'
sys.dont_write_bytecode = True
sys.path[:0] = [str(ROOT), str(ROOT / 'deps/native')]
from elftools.elf.elffile import ELFFile
from link_runtime_unit import relocation_rows
from project import sha256
import utility_runtime


CONTRACT_PATH = ROOT / 'provenance/utility-child-snd-alias-v1-20261106-contract.json'
CONTRACT_SHA256 = 'fa4b1c02d4f16b8988fa658bb4a2bb9269f593d59371aa3fb409b87e824be84c'
if sha256(CONTRACT_PATH) != CONTRACT_SHA256:
    raise ValueError('Exact promoted child alias contract changed')
CONTRACT = json.loads(CONTRACT_PATH.read_bytes())
EXPECTED = CONTRACT['row']
PROGRAM = 'dwc/utility.bin/move/child.srl'
NAME = 'native_utility_child_arm9_main_02006eb8'
KEYS = ['name', 'program', 'processor', 'module', 'mode', 'address', 'bytes', 'size', 'compiledBytes',
    'source', 'sourceSha256', 'sourceDependencies', 'object', 'objectSha256', 'compiler', 'compilerSha256',
    'compilerFlags', 'targetSha256', 'inputModuleSha256', 'relocations', 'nativeSymbolEntries', 'sectionIndex', 'sectionOffset']


def pins():
    if sha256(CONTRACT_PATH) != CONTRACT_SHA256:
        raise ValueError('Exact promoted child alias contract changed')
    for pin in CONTRACT['pins']:
        path = ROOT / pin['path']
        if path.suffix.lower() in ('.py', '.exe', '.dll') and (Path(pin['path']).parts[0] == 'work' or path.resolve() != path.absolute()):
            raise ValueError('Executable input escapes the exact pinned original root/tool chain')
        if sha256(path) != pin['sha256']:
            raise ValueError('Frozen child alias input changed: ' + pin['path'])


def executable(name):
    allowed = {EXPECTED['compiler']: EXPECTED['compilerSha256'], CONTRACT['linker']: CONTRACT['linkerSha256']}
    if name not in allowed:
        raise ValueError('Executable is outside the exact original compiler/linker chain')
    path = ROOT / name
    if path.resolve() != path.absolute() or not path.resolve().is_relative_to(ROOT / 'tools/mwccarm/mwccarm/2.0/base') or sha256(path) != allowed[name]:
        raise ValueError('Pinned original compiler/linker identity or location differs')
    return path


def validate_entry(row):
    if any(row.get(key) != EXPECTED.get(key) for key in KEYS):
        raise ValueError('Exact196-byte child caller/source/object/compiler/eight-alias contract differs')
    if '-lang' not in row['compilerFlags'] or row['compilerFlags'][row['compilerFlags'].index('-lang') + 1] != 'c99':
        raise ValueError('Fresh child alias qualification requires the exact C99 recipe')
    aliases = row['nativeSymbolEntries']
    if len(aliases) != 8 or {rel['symbol'] for rel in row['relocations']} != set(aliases):
        raise ValueError('The exact eight actual relocation imports are required')
    for name, item in aliases.items():
        if (item['program'], item['processor'], item['module'], item['mode'], item['kind']) != (PROGRAM, 'arm9', 'utility-child-arm9-main', 'arm', 'function'):
            raise ValueError('Original entry alias has an unqualified namespace/mode/kind')
        if name != 'native_fn_utility_child_arm9_main_%08x' % int(item['address'], 0):
            raise ValueError('Original-entry alias name/address identity differs')
    return aliases


def source_policy(row):
    paths = {row['source']: row['sourceSha256'], **{item['path']: item['sha256'] for item in row['sourceDependencies']}}
    included = set()
    for name, digest in paths.items():
        path = ROOT / name
        if path.suffix not in ('.c', '.h') or path.is_symlink() or not path.resolve().is_relative_to((ROOT / 'src/utility/parallel_wave20261106/child-snd-resume-next').resolve()) or sha256(path) != digest:
            raise ValueError('Frozen closed C/header input differs')
        text = path.read_text()
        if len(text.splitlines()) > 500 or '/*' in text or '//' in text or re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b', text) or re.search(r'^\s*#\s*include\s*<', text, re.M):
            raise ValueError('Child alias input violates the existing ordinary-C-only policy')
        included.update((path.parent / item).resolve() for item in re.findall(r'^\s*#\s*include\s*"([^"<>]+)"', text, re.M))
    if included != {(ROOT / item['path']).resolve() for item in row['sourceDependencies']}:
        raise ValueError('Actual child C include closure differs')


def function_payload(path):
    with path.open('rb') as stream:
        elf = ELFFile(stream)
        symbol = elf.get_section_by_name('.symtab').get_symbol_by_name(NAME)[0]
        if (elf['e_machine'], symbol['st_info']['type'], symbol['st_size']) != ('EM_ARM', 'STT_FUNC', 196):
            raise ValueError('Actual raw compiler ARM function type/extent differs')
        section = elf.get_section(symbol['st_shndx'])
        if (section['sh_type'], section['sh_flags']) != ('SHT_PROGBITS', 6):
            raise ValueError('Actual raw compiler caller section differs')
        start = symbol['st_value'] & ~1
        markers = [item for item in elf.get_section_by_name('.symtab').iter_symbols() if item['st_shndx'] == symbol['st_shndx'] and item.name in ('$a', '$t')]
        if not any(item.name == '$a' and item['st_value'] == start for item in markers) or any(item.name == '$t' and start <= item['st_value'] < start + 196 for item in markers):
            raise ValueError('Actual raw compiler function is not entirely ARM mapped')
        return section.data()[start:start + 196]


def original_namespace(row):
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
    layout, files = utility_runtime.derive()
    if layout['program'] != PROGRAM:
        raise ValueError('Actual derived child program differs')
    module = next(item for item in layout['modules'] if item['id'] == 'utility-child-arm9-main')
    native = files[ROOT / module['binary']]
    if module['processor'] != 'arm9' or hashlib.sha256(native).hexdigest() != row['inputModuleSha256']:
        raise ValueError('Actual original child CPU/module image differs')
    begin = int(row['address'], 0) - int(module['base'], 0)
    span = native[begin:begin + 196]
    if hashlib.sha256(span).hexdigest() != row['targetSha256']:
        raise ValueError('Actual original196-byte child span differs')
    inventory = json.loads((ROOT / 'evidence/utility/ghidra-arm9.json').read_bytes())
    if (inventory['program'], inventory['processor']) != (PROGRAM, 'arm9'):
        raise ValueError('Original imported-function inventory program/CPU differs')
    canonical = {}
    for rel in row['relocations']:
        binding = row['nativeSymbolEntries'][rel['symbol']]
        target = int(binding['address'], 0)
        found = [item for item in inventory['functions'] if int(item['address'], 0) == target]
        if len(found) != 1 or (found[0]['module'], found[0]['processor'], found[0]['mode']) != ('utility-child-arm9-main', 'arm9', 'arm') or int(found[0]['ranges'][0][0], 0) != target:
            raise ValueError('Original-child alias is not an exact same-namespace ARM function entry')
        instruction = list(Cs(CS_ARCH_ARM, CS_MODE_ARM).disasm(span[rel['offset']:rel['offset'] + 4], int(row['address'], 0) + rel['offset']))
        if len(instruction) != 1 or (instruction[0].mnemonic, instruction[0].op_str, rel['type'], rel['addend'], rel['targetMode']) != ('bl', '#' + hex(target), 1, -8, 'arm'):
            raise ValueError('Actual original child BL/type/addend/mode differs')
        canonical['arm9', target] = dict(binding, address=target)
    return canonical


def qualify():
    pins()
    report = json.loads((ROOT / CONTRACT['report']).read_bytes())
    if sha256(ROOT / CONTRACT['report']) != CONTRACT['reportSha256'] or len(report['matches']) != 1:
        raise ValueError('Frozen canonical child report differs')
    row = report['matches'][0]
    validate_entry(row)
    source_policy(row)
    canonical = original_namespace(row)
    WORK.mkdir(parents=True, exist_ok=True)
    directory = WORK / ('fresh-' + str(time.time_ns()))
    directory.mkdir()
    obj = directory / 'fresh.o'
    command = [str(executable(row['compiler'])), *row['compilerFlags'], '-c', str(ROOT / row['source']), '-o', str(obj)]
    process = subprocess.run(command, cwd=ROOT, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')), capture_output=True, text=True, timeout=30)
    attempt = dict(command=command, exitCode=process.returncode, stdout=process.stdout, stderr=process.stderr)
    (directory / 'compile.json').write_text(json.dumps(attempt, indent=2) + '\n')
    if process.returncode:
        raise ValueError('Actual fresh pinned C99 child compilation failed')
    original = ROOT / row['object']
    if function_payload(obj) != function_payload(original) or relocation_rows(obj, NAME) != relocation_rows(original, NAME):
        raise ValueError('Actual fresh C99 raw bytes/relocation type/addend/encoding differ from the pinned object')
    spec = importlib.util.spec_from_file_location('child_alias_original_link', ROOT / 'wave20261102_child_link.py')
    linker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(linker)
    if linker.LINKER.absolute() != executable(CONTRACT['linker']):
        raise ValueError('Original native link helper escaped the pinned linker')
    previous = linker.canonical
    fresh = dict(row, object=obj.relative_to(ROOT).as_posix(), objectSha256=sha256(obj))
    try:
        linker.canonical = lambda: canonical
        proof = linker.validate(fresh, directory / 'native-link')
    finally:
        linker.canonical = previous
    if not proof['exactCallerBytes'] or len(proof['bindings']) != 8 or any(item['initializedCodeBytes'] or item['nativeCalleeBytesUsed'] or item['calleeSourceCredit'] for item in proof['bindings']):
        raise ValueError('Genuine native caller link/zero-code anchor proof differs')
    for item in proof['bindings']:
        with (ROOT / item['anchorObject']).open('rb') as stream:
            elf = ELFFile(stream)
            section = elf.get_section_by_name('.text')
            symbol = elf.get_section_by_name('.symtab').get_symbol_by_name(item['name'])[0]
            if (section['sh_type'], section['sh_size'], section['sh_flags'], section['sh_addralign']) != ('SHT_NOBITS', 4, 6, 4) or (symbol['st_value'], symbol['st_size'], symbol['st_info']['type']) != (0, 0, 'STT_FUNC') or any(section['sh_type'] == 'SHT_PROGBITS' and section['sh_size'] for section in elf.iter_sections()):
                raise ValueError('Original-entry anchor acquired initialized code')
    pins()
    result = dict(proposalOnly=True, acceptedSourceCredit=0, aliasCodeCredit=0, aliases=copy.deepcopy(row['nativeSymbolEntries']),
        freshObject=fresh['object'], freshObjectSha256=fresh['objectSha256'], rawBytesAndRelocationsIdentical=True,
        actualFreshC99Compile=attempt, genuineNativeCallerLink=proof, frozenInputsUnchanged=True)
    (directory / 'qualification.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


def project(plan, qualified, program, processor):
    selected, symbols, bindings, metadata = plan
    targets = [item for item in selected if item.get('name') == NAME]
    if not targets:
        return plan
    if (program, processor) != (PROGRAM, 'arm9') or len(targets) != 1:
        raise ValueError('Child alias adaptation may target only the exact ARM9 child plan')
    validate_entry(targets[0])
    if qualified['aliases'] != EXPECTED['nativeSymbolEntries']:
        raise ValueError('Live qualification aliases differ from the exact frozen eight entries')
    updated_symbols, updated_bindings = dict(symbols), copy.deepcopy(bindings)
    for name, item in qualified['aliases'].items():
        if name in updated_symbols and int(updated_symbols[name], 0) != int(item['address'], 0):
            raise ValueError('Legacy child plan contains a conflicting alias address')
        duplicates = [entry for entry in updated_bindings if entry['name'] == name]
        expected = dict(item, name=name)
        if duplicates and (len(duplicates) != 1 or duplicates[0] != expected):
            raise ValueError('Legacy child plan contains a conflicting full namespace binding')
        updated_symbols[name] = item['address']
        if not duplicates:
            updated_bindings.append(expected)
    return selected, updated_symbols, updated_bindings, metadata


@contextlib.contextmanager
def factory(module):
    if Path(getattr(module, '__file__', '')).absolute() != ROOT / 'link_utility.py':
        raise ValueError('Factory may wrap only the pinned original root utility linker')
    qualified = qualify()
    previous = module.accepted
    def accepted(program, processor=None):
        return project(previous(program, processor), qualified, program, processor)
    try:
        module.accepted = accepted
        yield qualified
    finally:
        module.accepted = previous
        pins()


if __name__ == '__main__':
    result = qualify()
    print(dict(proposalOnly=True, actualFreshC99NativeLink=True, aliases=len(result['aliases']), initializedAliasBytes=0, sourceCredit=0, object=result['freshObject']))
