import argparse
import hashlib
import json
import os
import re
import struct
import subprocess
from pathlib import Path

import match_runtime as C
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from elftools.elf.elffile import ELFFile
from project import ROOT, configuration, sha256
from slice_reference_sdk_entities_v3_20261102 import functions, slice_closed, declaration_name
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from wave20261102_main_sdk_next_storage import normalize_alignment, storage_groups, lift_statics
from slice_reference_sdk_entities_v3_20261102 import NONCODE

LANE = ROOT / 'evidence/lanes/parallel-wave20261102/main-sdk-next'
WORK = ROOT / 'work/parallel-wave20261102/main-sdk-next'
SOURCE = ROOT / 'src/runtime/parallel_wave20261102/main-sdk-next'
INPUT = ROOT / 'evidence/attempts/main-nitrosdk-masked-candidates-20261102.json'


def dump(name, value):
    LANE.mkdir(parents=True, exist_ok=True)
    (LANE / name).write_text(json.dumps(value, indent=2) + '\n')


def claim():
    if (LANE / 'claim.json').exists():
        raise ValueError('Main SDK next already claimed')
    ledger = [json.loads(line) for line in (ROOT / 'ledger/functions.jsonl').read_text().splitlines()]
    accepted = {(row['module'], int(row['address'], 0)) for row in ledger if row['states']['moduleLinked']}
    pending = set()
    for cohort in range(147, 151):
        for path in ROOT.glob(f'cohort{cohort}-*-specification.json'):
            body = json.loads(path.read_text())
            pending.update((r.get('module'), int(str(r['address']), 0)) for r in body.get('expectedAdditions', []) if r.get('address'))
    selected = {}
    for row in json.loads(INPUT.read_text())['candidates']:
        identity = row['identity']
        address = int(identity['address'], 0)
        if row['sourceOwner'] == 'root' and row['referenceFunction'].startswith('MB') and identity['bytes'] > 128 and ('main', address) not in accepted | pending:
            selected.setdefault(address, row)
    module, image, unused = measured_module('main')
    claims = [dict(**row['identity'], id=f'{configuration()["romSha256"]}/arm9/main/arm/{address:08x}', moduleSha256=module['sha256'], targetSha256=hashlib.sha256(image[address - 0x02000000:address - 0x02000000 + row['identity']['bytes']]).hexdigest(), referenceFunction=row['referenceFunction'], sourceTarget=f'src/runtime/parallel_wave20261102/main-sdk-next/{address:08x}/native_main_{address:08x}.c') for address, row in selected.items()]
    dump('claim.json', dict(schemaVersion=1, owner='ds_tooling_research/main-sdk-next', acceptedBaselineCohort=146, status='reconstructing', claimedFunctions=claims, nativeOpportunityBytes=sum(r['bytes'] for r in claims), sourceCredit=0, scope='Larger measured MB runtime/file/beacon/wireless control units; no save mechanics or prepared aggregate identities.'))
    dump('reference-selection.json', dict(schemaVersion=1, input=INPUT.relative_to(ROOT).as_posix(), inputSha256=sha256(INPUT), rows=list(selected.values()), sourceCredit=0))
    print(dict(claimed=len(claims), bytes=sum(row['bytes'] for row in claims)), flush=True)


def clean_flags(flags):
    result = []
    index = 0
    while index < len(flags):
        if flags[index] == '-i':
            index += 2
        elif flags[index].startswith('-D'):
            index += 1
        else:
            result.append(flags[index])
            index += 1
    return result


def entities(text):
    records = functions(text)
    mapping = {row['start']: row for row in records}
    mask = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', lambda m:' ' * len(m[0]), text)
    output = []
    start = index = depth = 0
    while index < len(text):
        if index in mapping:
            row = mapping[index]
            output.append(dict(kind='function', name=row['name'], text=text[start:row['end']]))
            start = index = row['end']
            continue
        if mask[index] == '{':
            depth += 1
        elif mask[index] == '}':
            depth -= 1
        elif mask[index] == ';' and depth == 0:
            fragment = text[start:index + 1]
            output.append(dict(kind='declaration', name=declaration_name(fragment), text=fragment))
            start = index + 1
        index += 1
    if depth or text[start:].strip():
        raise ValueError('Entity splitter left unbalanced or trailing source')
    return output


def mapped_symbols(row, image):
    address = int(row['identity']['address'], 0)
    original = image[address - 0x02000000:address - 0x02000000 + row['identity']['bytes']]
    aliases = {row['referenceFunction']: f'native_main_{address:08x}'}
    sectionBases = {}
    usedData = set()
    directData = {}
    with (ROOT / row['object']).open('rb') as stream:
        elf = ELFFile(stream)
        table = elf.get_section_by_name('.symtab')
        symbols = {s.name:s for s in table.iter_symbols()}
        decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
        decoder.detail = True
        for relocation in row['relocations']:
            name = relocation['symbol']
            symbol = symbols[name]
            offset = relocation['offset']
            kind = relocation['type']
            function = kind in [1, 28, 29] or symbol['st_info']['type'] == 'STT_FUNC'
            if kind == 2:
                addend = relocation['explicitAddend'] if relocation['format'] == 'SHT_RELA' else int.from_bytes(bytes.fromhex(relocation['originalEncodedWord']), 'little')
                target = (struct.unpack_from('<I', original, offset)[0] - addend) & 0xFFFFFFFF
            else:
                instruction = next(decoder.disasm(original[offset:offset + 4], address + offset))
                if instruction.operands[0].type != 2:
                    raise ValueError('Reference branch is not an immediate measured call')
                target = instruction.operands[0].imm & 0xFFFFFFFF
            if function:
                alias = f'native_fn_{target & ~1:08x}'
                if name == row['referenceFunction']:
                    if target & ~1 != address:
                        raise ValueError('Self callback points to a different native entry')
                    alias = f'native_main_{address:08x}'
                if name in aliases and aliases[name] != alias:
                    raise ValueError('Reference function requires contradictory addresses')
                aliases[name] = alias
            elif symbol['st_info']['type'] == 'STT_SECTION':
                section = symbol['st_shndx']
                if section in sectionBases and sectionBases[section] != target:
                    raise ValueError('Reference storage section requires contradictory bases')
                sectionBases[section] = target
                within = addend
                for candidate in symbols.values():
                    if candidate['st_shndx'] == section and candidate['st_info']['type'] == 'STT_OBJECT' and candidate['st_value'] <= within < candidate['st_value'] + candidate['st_size']:
                        usedData.add(candidate.name)
            else:
                aliases[name] = f'native_data_main_{target:08x}'
                directData[name] = target
                usedData.add(name)
                if isinstance(symbol['st_shndx'], int) and symbol['st_info']['type'] == 'STT_OBJECT' and not name.startswith('@'):
                    section = symbol['st_shndx']
                    inferred = target - symbol['st_value']
                    if section in sectionBases and sectionBases[section] != inferred:
                        raise ValueError('Named SDK object contradicts section base')
                    sectionBases[section] = inferred
        for symbol in symbols.values():
            if symbol['st_info']['type'] == 'STT_OBJECT' and isinstance(symbol['st_shndx'], int) and symbol['st_shndx'] in sectionBases:
                target = (sectionBases[symbol['st_shndx']] + symbol['st_value']) & 0xFFFFFFFF
                aliases[symbol.name] = f'native_data_main_{target:08x}'
                directData[symbol.name] = target
    return aliases, usedData, directData, sectionBases


def external_literals(text, row, aliases):
    declarations = []
    evidence = []
    referenced = {relocation['symbol'] for relocation in row['relocations']}
    with (ROOT / row['object']).open('rb') as stream:
        elf = ELFFile(stream)
        symbols = {s.name:s for s in elf.get_section_by_name('.symtab').iter_symbols()}
        for name, alias in aliases.items():
            if name not in referenced or not name.startswith('@') or not alias.startswith('native_data_main_'):
                continue
            symbol = symbols[name]
            data = elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value'] + symbol['st_size']]
            if not data.endswith(b'\0') or any(value < 32 or value > 126 for value in data[:-1]):
                raise ValueError('Anonymous SDK literal is not a plain ASCII string')
            literal = json.dumps(data[:-1].decode('ascii'))
            if literal not in text:
                raise ValueError('Anonymous SDK string has no unique source expression')
            text = text.replace(literal, alias)
            declarations.append('extern const char ' + alias + '[' + str(len(data)) + '];')
            evidence.append(dict(referenceSymbol=name, nativeAlias=alias, bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), storageCredit=0))
    return text + '\n' + '\n'.join(declarations) + '\n', evidence


def preprocessing(row):
    label = Path(row['referenceSource']).stem + '-' + row['profile']
    directory = WORK / 'preprocessed' / label
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / 'expanded.i'
    if output.exists():
        return output
    executable = ROOT / row['compiler']
    if sha256(executable) != row['compilerSha256'] or sha256(ROOT / row['referenceSource']) != row['sourceSha256']:
        raise ValueError('Reference source/compiler differs from fingerprint')
    command = [str(executable), *row['compilerFlags'], '-E', str(ROOT / row['referenceSource']), '-o', str(output)]
    process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')))
    if process.returncode:
        raise ValueError(('Reference preprocessing failed', process.stdout, process.stderr))
    return output


def materialize(row, image):
    address = int(row['identity']['address'], 0)
    seed = row['referenceFunction']
    aliases, usedData, directData, sectionBases = mapped_symbols(row, image)
    expanded = preprocessing(row)
    text = expanded.read_text(encoding='utf-8')
    text = NONCODE.sub(lambda match: (' ' + '\n' * match[0].count('\n')) if match[0].startswith('/') else match[0], text)
    text = '\n'.join(line for line in text.splitlines() if not line.lstrip().startswith('#')) + '\n'
    text = normalize_alignment(text)
    text, local_names = lift_statics(text, row, functions, declaration_name)
    for record in sorted(functions(text), key=lambda r:r['start'], reverse=True):
        header = text[record['start']:record['opening']]
        if record['name'] == seed:
            header = re.sub(r'\bstatic\s+', '', header)
            text = text[:record['start']] + header + text[record['opening']:]
        elif not re.search(r'\binline\b', header) or record['name'] in aliases:
            header = re.sub(r'\b(?:static|asm|__asm|__asm__)\s+', '', header)
            text = text[:record['start']] + header.rstrip() + ';\n' + text[record['end']:]
    for name in aliases.keys() - directData.keys():
        text = re.sub(r'\bstatic\s+(?=[^;{}]*\b' + re.escape(name) + r'\s*\()', '', text)
    text, literals = external_literals(text, row, aliases)
    text, layouts = storage_groups(text, row, sectionBases, aliases, entities, local_names)
    pieces = []
    externalized = []
    for entity in entities(text):
        fragment = entity['text']
        if entity['kind'] == 'declaration' and entity['name'] in usedData:
            fragment = fragment.split('=', 1)[0].rstrip().removesuffix(';').rstrip()
            fragment = re.sub(r'\bstatic\s+', '', fragment)
            if not re.search(r'\bextern\b', fragment):
                fragment = 'extern ' + fragment.strip()
            fragment += ';\n'
            externalized.append(entity['name'])
        pieces.append(fragment)
    text = '\n'.join(pieces)
    for name in sorted(aliases, key=len, reverse=True):
        if re.fullmatch(r'[A-Za-z_]\w*', name):
            text = re.sub(r'\b' + re.escape(name) + r'\b', aliases[name], text)
    text, closure = slice_closed(text, [f'native_main_{address:08x}'])
    text = re.sub(r'\b(?:asm|__asm|__asm__)\s+(?=[^{};]*;)', '', text)
    forbidden = re.findall(r'\b(?:asm|__asm|__asm__|J2pUnknownVaList|va_list|size_t)\b', text)
    if forbidden or '#include' in text or '/*' in text or '//' in text:
        raise ValueError(('Not ordinary closed C', sorted(set(forbidden))))
    records = entities(text)
    selected = next(record for record in records if record['kind'] == 'function' and record['name'] == f'native_main_{address:08x}')
    if len(selected['text'].splitlines()) > 490:
        raise ValueError(('Selected C body exceeds readable file policy', len(selected['text'].splitlines())))
    groups = []
    current = []
    for entity in records:
        if entity is selected:
            continue
        fragment = entity['text'].strip() + '\n'
        if len(fragment.splitlines()) > 480:
            raise ValueError('Single complete declaration exceeds header policy')
        if sum(len(piece.splitlines()) for piece in current) + len(fragment.splitlines()) > 480:
            groups.append(''.join(current))
            current = []
        current.append(fragment)
    if current:
        groups.append(''.join(current))
    directory = SOURCE / f'{address:08x}'
    directory.mkdir(parents=True, exist_ok=True)
    headers = []
    for index, group in enumerate(groups):
        path = directory / f'context_{index:02d}.h'
        path.write_text(group, encoding='utf-8')
        headers.append(dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)))
    source = directory / f'native_main_{address:08x}.c'
    source.write_text(''.join(f'#include "context_{index:02d}.h"\n' for index in range(len(groups))) + selected['text'].strip() + '\n', encoding='utf-8')
    return source, headers, dict(referenceSource=row['referenceSource'], referenceSourceSha256=row['sourceSha256'], referenceFunction=seed, profile=row['profile'], expandedSha256=sha256(expanded), lexicalClosure=closure, externalizedStorageNames=externalized, measuredAliases=aliases, measuredStorageObjects=directData, measuredSectionBases={str(k):v for k,v in sectionBases.items()}, typedStorageLayouts=layouts, externalLiteralReferences=literals, originalStorageSourceCredit=0)


def run():
    rows = json.loads((LANE / 'reference-selection.json').read_text())['rows']
    metadata, image, unused = measured_module('main')
    attempts, exact = [], []
    for row in rows:
        address = int(row['identity']['address'], 0)
        result = dict(identity=row['identity'], referenceFunction=row['referenceFunction'], sourceCredit=0, actualNativeFunctionReturns=0)
        try:
            if sha256(ROOT / row['object']) != row['objectSha256']:
                raise ValueError('Reference original object changed')
            source, headers, provenance = materialize(row, image)
            flags = clean_flags(row['compilerFlags'])
            C.FLAGS = flags
            C.WORK = WORK / f'compile/{address:08x}'
            compiled, unused = C.compare(source, 'main', flags[0][2:], flags[flags.index('-inline') + 1], compiler=ROOT / row['compiler'])
            if len(compiled) != 1 or compiled[0].get('compileFailed'):
                raise ValueError(('Closed compilation failed', compiled))
            entry = compiled[0]
            entry['sourceDependencies'] = headers
            proof = validate(entry, qualified_bindings(entry), WORK / f'link/{address:08x}')
            entry['manualRelocationComparison'] = dict(exact=entry['exactAfterDeclaredRelocation'], matchingBytes=entry['matchingBytes'])
            entry['exactAfterDeclaredRelocation'] = proof['exactCallerBytes']
            entry['matchingBytes'] = entry['bytes']
            entry['matchingBytesScope'] = 'Complete genuinely linked caller extent'
            result.update(exact=True, sourceEntry=entry, genuineLink=proof, provenance=provenance, flags=flags, source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source))
            exact.append(result)
            print('EXACT', hex(address), entry['bytes'], row['referenceFunction'], flush=True)
        except Exception as error:
            result.update(exact=False, errorType=type(error).__name__, refusal=str(error))
            print('rejected', hex(address), row['referenceFunction'], str(error)[:180], flush=True)
        attempts.append(result)
        dump('campaign.json', dict(schemaVersion=1, moduleSha256=metadata['sha256'], attempts=attempts, exact=exact, sourceCredit=0, actualNativeFunctionReturns=0))
    print(dict(exactFunctions=len(exact), exactBytes=sum(r['identity']['bytes'] for r in exact)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['claim', 'run'])
    globals()[parser.parse_args().action]()
