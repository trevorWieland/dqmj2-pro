import argparse
import hashlib
import json
import os
import re
import struct
import subprocess
from pathlib import Path
import match_lowlevel
import arm7_runtime
import utility_runtime
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
from elftools.elf.elffile import ELFFile
from elf_units import split_symbol
from link_runtime_unit import binding_object, relocation_rows

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work/arm7-bulk-20261030'
LINKER = ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwldarm.exe'
LINKER_HASH = 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def namespace(program):
    if program:
        if program != utility_runtime.PROGRAM:
            raise ValueError('Unknown ARM7 program namespace')
        layout, unused = utility_runtime.derive()
        inventory = json.loads((ROOT / 'evidence/utility/ghidra-arm7.json').read_text())
    else:
        layout = arm7_runtime.derive((ROOT / 'extract/arm7/arm7.bin').read_bytes())
        inventory = json.loads((ROOT / 'evidence/arm7/ghidra-runtime-inventory.json').read_text())
    modules = {row['id']: row for row in layout['modules'] if row.get('processor') == 'arm7'}
    functions = {}
    for row in inventory['functions']:
        if row.get('mode') in ('arm', 'thumb') and row['module'] in modules:
            address = int(row['address'], 0)
            binding = {'program': program, 'processor': 'arm7', 'module': row['module'], 'mode': row['mode'],
                'kind': 'function', 'address': hex(address), 'boundarySource': 'measured-runtime-map-Ghidra-entry; caller-boundary-audit-separate'}
            if address in functions and functions[address] != binding:
                raise ValueError('Conflicting same-program ARM7 function modes')
            functions[address] = binding
    return modules, functions


REGION_REPORT='evidence/arm7/lane-lock-bitmap-region-v2-20261031.json'
REGION_SHA='792cd8367e38b29bc9a43bf57e9a3d195b47a2fdd2bf41d2988abc9186a1aadb'
ROM_SHA='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'
BASE_SHA='f9afd9a3b5142dbb2f5bec561a8a4f3d725ec4b52faba9f9d7aa7837a540922c'
REGION_REFERENCE=dict(report=REGION_REPORT,sha256=REGION_SHA)
REGION_VIEWS={
    0x027fffb8:dict(symbol='native_utility_child_arm7_bitmap_word_027fffb8',address='0x27fffb8',bytes=4,kind='native32 bitmap word0'),
    0x027fffbc:dict(symbol='native_utility_child_arm7_bitmap_word_027fffbc',address='0x27fffbc',bytes=4,kind='native32 bitmap word1'),
    0x027ffff0:dict(symbol='native_utility_child_arm7_data_027ffff0',address='0x27ffff0',bytes=8,kind='partial handshake view',ownerOffset=4,ownerBytes=2,extensionOffset=6,extensionBytes=2,originalObjectExtentProved=False)}


def qualified_shared_runtime_view(entry,target):
    import gzip
    identity=tuple(entry.get(k) for k in ('program','processor','module','mode','address','bytes','romSha256'))
    if identity!=('dwc/utility.bin/move/child.srl','arm7','utility-child-arm7-wram','arm','0x37fc0b8',136,ROM_SHA):raise ValueError('Shared-region qualification is restricted to one full child initializer identity/build')
    if entry.get('qualifiedSharedRuntimeRegions')!=REGION_REFERENCE or entry.get('qualifiedSharedRuntimeViews')!=list(REGION_VIEWS.values()):raise ValueError('Explicit measured shared-window/type views differ')
    if target not in REGION_VIEWS:raise ValueError('Address is not one of the three measured typed relocation starts')
    if digest((ROOT/'link_arm7_bulk_20261030.py').read_bytes())!=BASE_SHA:raise ValueError('Original linker guard policy changed')
    report_path=ROOT/REGION_REPORT
    if digest(report_path.read_bytes())!=REGION_SHA:raise ValueError('Measured shared-window report changed')
    report=json.loads(report_path.read_text())
    if digest((ROOT/report['generator']).read_bytes())!=report['generatorSha256'] or report.get('romSha256')!=ROM_SHA:raise ValueError('Current shared-window generator/build pin differs')
    if any(report.get(k)!=0 for k in ('sourceCredit','assemblySourceCredit','functionMatchedBytes','originalDataSourceCredit','providerCalls','actualWaitThunkOrBiosExecutions')) or report['actualNormalReturns']!=604 or report['totals']['unreadyBoundaryStops']!=6:raise ValueError('Native return/boundary/zero-credit scope differs')
    context=next(r for r in report['nativeInputNamespaces'] if r['program']=='dwc/utility.bin/move/child.srl')
    if context['processor']!='arm7' or context['module']!='utility-child-arm7-wram' or context['mode']!='arm' or context['init']!=0x037fc0b8 or entry.get('inputModuleSha256')!=context['sha256'] or digest((ROOT/context['binary']).read_bytes())!=context['sha256']:raise ValueError('Current native input namespace differs')
    function=next(r for r in context['functions'] if r['kind']=='init')
    if function!=dict(address='0x37fc0b8',bytes=136,mode='arm',kind='init'):raise ValueError('Measured initializer extent differs')
    role=next(r for r in report['nativeRoleQualifications'] if r['program']==context['program'])
    if any(role.get(k)!=v for k,v in dict(mode='arm',bitmapBase='0x27fffb8',bitmapBytes=8,handshake='0x27ffff0',handshakeBytes=8,ownerReadBytes=2,ownerReadOffset=4,extensionStoreBytes=2,extensionOffset=6,initializerEntry='0x37fc0b8').items()):raise ValueError('Measured typed windows/field roles differ')
    trace=report['traceProduct'];packed=(ROOT/trace['path']).read_bytes();raw=gzip.decompress(packed)
    if digest(packed)!=trace['compressedSha256'] or digest(raw)!=trace['rawSha256'] or len(json.loads(raw))!=trace['records'] or packed[4:8]!=bytes(4):raise ValueError('Current shared-window actual native records missing or changed')
    return dict(program=context['program'],processor='arm7',module='external-shared-runtime-view',kind='data',mode='data',address=hex(target),region='measured-runtime-view-no-module-ownership',
        qualifiedSharedRuntimeRegions=REGION_REFERENCE,typedMinimumView=REGION_VIEWS[target],originalObjectExtentProved=False,sourceDataCredit=0)


def data_binding(entry, target, modules):
    ranges = []
    for module in modules.values():
        base = int(module.get('base', module['runtimeBase']), 0)
        if base <= target < base + module['bytes']:
            ranges.append((module['id'], 'initialized'))
        if int(module['bssStart'], 0) <= target < int(module['bssEnd'], 0):
            ranges.append((module['id'], 'bss'))
    if len(ranges) > 1:
        raise ValueError('Data target ambiguously overlaps ARM7 modules')
    if ranges:
        module, region = ranges[0]
    elif 0x02000000 <= target < 0x02400000:
        module, region = 'external-shared-main-ram', 'not-owned-by-initialized-ARM7-module'
    elif 0x04000000 <= target < 0x05000000:
        module, region = 'external-mmio', 'address-region-only-no-register-meaning'
    elif 0x027fffb8 <= target < 0x027fffc0 or 0x027ffff0 <= target < 0x027ffff8:
        return qualified_shared_runtime_view(entry,target)
    else:
        raise ValueError('Unqualified external ARM7 data target: ' + hex(target))
    return {'program': entry.get('program', ''), 'processor': 'arm7', 'module': module,
        'kind': 'data', 'mode': 'data', 'address': hex(target), 'region': region}


def derive_bindings(entry, native, functions, modules):
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB if entry['mode'] == 'thumb' else CS_MODE_ARM)
    decoder.detail = True
    address = int(entry['address'], 0)
    source = (ROOT / entry['source']).read_text()
    bindings = {}
    for rel in entry['relocations']:
        name, offset, kind = rel['symbol'], rel['offset'], rel['type']
        if kind == 2:
            addend = rel['explicitAddend'] if rel['format'] == 'SHT_RELA' else int.from_bytes(bytes.fromhex(rel['originalEncodedWord']), 'little')
            target = (struct.unpack_from('<I', native, offset)[0] - addend) & 0xFFFFFFFF
            function = bool(re.search(r'\b' + re.escape(name) + r'\s*\(', source)) or '_fn_' in name or '_thumb_' in name or '_arm_' in name
        elif kind in (1, 10, 15, 28, 29):
            instruction = next(decoder.disasm(native[offset:offset + 4], address + offset), None)
            if instruction is None or not instruction.operands or instruction.operands[0].type != 2:
                raise ValueError('Original relocated call/jump has no immediate native target')
            target, function = instruction.operands[0].imm & 0xFFFFFFFF, True
        else:
            raise ValueError('Unsupported unmodified ARM7 relocation')
        if function:
            canonical = target & ~1
            if canonical not in functions:
                raise ValueError('Unqualified ARM7 native function/alternate entry: ' + name + ' ' + hex(target))
            binding = functions[canonical]
            if kind == 2 and bool(target & 1) != (binding['mode'] == 'thumb'):
                raise ValueError('Function-pointer native tag/mode disagrees')
        else:
            binding = data_binding(entry, target, modules)
            if binding.get('typedMinimumView',{}).get('symbol',name)!=name:raise ValueError('Qualified typed view symbol differs from its actual relocation')
        encoded = re.search(r'_([0-9a-fA-F]{8})$', name)
        if encoded and (int(encoded[1], 16) & (~1 if function else 0xFFFFFFFF)) != (target & (~1 if function else 0xFFFFFFFF)):
            raise ValueError('Address-labelled source symbol conflicts with measured native binding')
        if name in bindings and bindings[name] != binding:
            raise ValueError('One source symbol has conflicting native identities')
        bindings[name] = binding
    return bindings


def validate(entry, directory):
    if entry.get('processor') != 'arm7' or digest(LINKER.read_bytes()) != LINKER_HASH:
        raise ValueError('Pinned ARM7-only linker contract differs')
    modules, functions = namespace(entry.get('program', ''))
    metadata = modules[entry['module']]
    path = ROOT / metadata['binary']
    binary = path.read_bytes()
    if digest(binary) != metadata['sha256'] or entry['inputModuleSha256'] != metadata['sha256']:
        raise ValueError('ARM7 source module input changed')
    address, size = int(entry['address'], 0), entry['bytes']
    base = int(metadata.get('base', metadata.get('runtimeBase')), 0)
    native = binary[address - base:address - base + size]
    if len(native) != size or digest(native) != entry['targetSha256'] or address not in functions or functions[address]['mode'] != entry['mode']:
        raise ValueError('Complete candidate span or canonical ARM7 entry differs')
    source, original = ROOT / entry['source'], ROOT / entry['object']
    if digest(source.read_bytes()) != entry['sourceSha256'] or digest(original.read_bytes()) != entry['objectSha256']:
        raise ValueError('Candidate source/immutable object changed')
    bindings = derive_bindings(entry, native, functions, modules)
    directory = Path(directory).resolve()
    directory.relative_to(WORK.resolve())
    directory.mkdir(parents=True, exist_ok=True)
    caller = directory / 'caller.o'
    with original.open('rb') as stream:
        elf = ELFFile(stream)
        flags = elf['e_flags']
        split_symbol(elf, entry['name'], caller)
    before, after = relocation_rows(original, entry['name']), relocation_rows(caller, entry['name'])
    if before != after:
        raise ValueError('Function split modified a relocation/addend/encoded instruction')
    required = set()
    with caller.open('rb') as stream:
        elf = ELFFile(stream)
        for section in elf.iter_sections():
            if section['sh_type'] in ('SHT_REL', 'SHT_RELA'):
                table = elf.get_section(section['sh_link'])
                for rel in section.iter_relocations():
                    symbol = table.get_symbol(rel['r_info_sym'])
                    if symbol['st_shndx'] == 'SHN_UNDEF':
                        required.add(symbol.name)
    if required - set(bindings):
        raise ValueError('Unbound ARM7 caller externs')
    memories, sections, objects, probes, assignments = [f'CALL: ORIGIN = {address:#x} > caller.bin'], ['.caller: { caller.o(.text) } > CALL'], [caller], [], []
    for index, name in enumerate(sorted(required)):
        binding = bindings[name]
        target = int(binding['address'], 0)
        if binding['kind'] == 'function':
            anchor = directory / ('anchor' + str(index) + '.o')
            binding_object(name, binding['mode'], flags, anchor)
            objects.append(anchor)
            memories.append(f'BIND{index}: ORIGIN = {target:#x} > anchor{index}.bin')
            sections.append(f'.binding{index}: {{ anchor{index}.o(.text) }} > BIND{index}')
            probes.append({'symbol': name, **binding, 'object': anchor.relative_to(ROOT).as_posix(), 'objectSha256': digest(anchor.read_bytes()),
                'initializedCodeBytes': 0, 'calleeSourceCredit': 0})
        else:
            assignments.append(name + ' = ' + hex(target) + ';')
    lcf = directory / 'unit.lcf'
    lcf.write_text('MEMORY {\n' + '\n'.join(memories) + '\n}\nSECTIONS {\n' + '\n'.join(sections + assignments) + '\n}\n')
    linked = directory / 'linked.elf'
    command = [str(LINKER), '-nostdlib', '-nodeadstrip', '-interworking', '-proc', 'arm7tdmi', '-main', entry['name'], str(lcf), *map(str, objects), '-o', str(linked)]
    result = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=30,
        env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')))
    if result.returncode:
        raise ValueError('Real ARM7 link failed: ' + result.stdout + result.stderr)
    output = (directory / 'caller.bin').read_bytes()
    if output != native:
        raise ValueError({'nativeBytes': size, 'linkedBytes': len(output), 'matchingBytes': sum(a == b for a, b in zip(output, native))})
    with linked.open('rb') as stream:
        elf = ELFFile(stream)
        symbols = list(elf.get_section_by_name('.symtab').iter_symbols())
        own = next(row for row in symbols if row.name == entry['name'])
        if own['st_value'] != address or own['st_size'] != size:
            raise ValueError('Linked ARM7 function symbol extent differs')
        for probe in probes:
            target = int(probe['address'], 0)
            symbol = next(row for row in symbols if row.name == probe['symbol'])
            if symbol['st_value'] != target or symbol['st_size'] != 0:
                raise ValueError('ARM7 zero-code callee binding changed extent')
            if not any(row.name == ('$t' if probe['mode'] == 'thumb' else '$a') and row['st_value'] == target for row in symbols):
                raise ValueError('ARM7 binding lost canonical instruction-mode mapping')
            output_path = (ROOT / probe['object']).with_suffix('.bin')
            if output_path.exists() and output_path.stat().st_size:
                raise ValueError('ARM7 binding acquired initialized callee code')
    proof = {'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()), 'processor': 'arm7',
        'program': entry.get('program', ''), 'module': entry['module'], 'address': entry['address'], 'mode': entry['mode'], 'bytes': size,
        'exactLinkedBytes': True, 'linkedCallerSha256': digest(output), 'targetSha256': entry['targetSha256'], 'sourceSha256': entry['sourceSha256'],
        'sourceObjectSha256': entry['objectSha256'], 'splitObjectSha256': digest(caller.read_bytes()), 'unchangedRelocations': before,
        'bindings': bindings, 'zeroCodeAnchors': probes, 'linkerSha256': LINKER_HASH, 'linkCommand': command, 'cwd': str(directory),
        'lcf': lcf.relative_to(ROOT).as_posix(), 'lcfSha256': digest(lcf.read_bytes()), 'linkedElfSha256': digest(linked.read_bytes()),
        'boundaryAndAbiAndNativeExecutionStillRequired': True, 'wholeModuleLinked': False, 'currentSourceCredit': 0, 'calleeSourceCredit': 0}
    (directory / 'proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    return proof


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('report', type=Path)
    parser.add_argument('--batch', required=True)
    args = parser.parse_args()
    report = json.loads(args.report.read_text())
    results = []
    for index, entry in enumerate(report['relocationOnlyCandidates']):
        try:
            proof = validate(entry, WORK / args.batch / entry['module'] / (entry['address'][2:] + '-' + entry['objectSha256'][:12]))
            results.append({'entry': entry, 'proof': proof})
        except Exception as error:
            results.append({'entry': entry, 'failure': type(error).__name__ + ': ' + str(error)})
        print(json.dumps({'processed': index + 1, 'address': entry['address'], 'module': entry['module'], 'realLinkExact': 'proof' in results[-1]}), flush=True)
    output = WORK / args.batch / 'results.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({'results': results, 'currentSourceCredit': 0}, indent=2) + '\n')


if __name__ == '__main__':
    main()
