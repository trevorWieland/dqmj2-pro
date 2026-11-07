import re
from project import ROOT
import match_runtime
from elftools.elf.elffile import ELFFile
from link_runtime_unit import validate, relocation_rows
from recover_linked_runtime import qualified_bindings, relocation_only_candidate
from wave20261106_dwc_main_friend_next_second_compiler import compare
from wave20261106_dwc_main_friend_next_second_bindings import qualify
from closed_c_compiler_inputs_20261105 import compiler_inputs


def dependencies(source):
    seen, pending = set(), [source.resolve()]
    while pending:
        path = pending.pop().resolve()
        if path in seen:
            continue
        if not path.is_relative_to(source.parent.resolve()):
            raise ValueError('Closed friend include escaped selected unit')
        seen.add(path)
        text = path.read_text()
        if re.search(r'^\s*#\s*include\s*<', text, re.M):
            raise ValueError('Implicit system include in selected friend source')
        pending.extend(path.parent / name for name in re.findall(r'^\s*#\s*include\s*"([^"<>]+)"', text, re.M))
    from project import sha256
    return [dict(path=p.relative_to(ROOT).as_posix(), sha256=sha256(p)) for p in sorted(seen) if p != source.resolve()]


def build(source, directory):
    rows, unused = compare(source, directory / 'c')
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError(('Selected friend caller compile failed', rows))
    row = rows[0]
    row.update(program='', sourceDependencies=dependencies(source))
    row['closedCCompilerInputs'] = compiler_inputs(row)
    relocation_only_candidate(row)
    bindings = qualified_bindings(row)
    for binding in bindings.values():
        binding['program'] = ''
    row['originalNamespaceWitnesses'] = qualify(row, bindings)
    proof = validate(row, bindings, directory / 'l')
    body = (directory / 'l/caller.bin').read_bytes()
    with (directory / 'l/linked.elf').open('rb') as stream:
        elf = ELFFile(stream)
        symbols = list(elf.get_section_by_name('.symtab').iter_symbols())
        entry = next(symbol for symbol in symbols if symbol.name == row['name'])
        if entry['st_value'] != int(row['address'], 0) or entry['st_size'] != row['bytes'] or len(body) != row['bytes']:
            raise ValueError('Genuine friend caller extent changed')
        if not any(symbol.name == '$t' and symbol['st_value'] == entry['st_value'] for symbol in symbols):
            raise ValueError('Real Thumb caller mapping absent')
    if relocation_rows(ROOT / row['object'], row['name']) != relocation_rows(directory / 'l/caller.o', row['name']):
        raise ValueError('Friend split altered original source relocations')
    row.update(nativeSymbolEntries=bindings, realLink=proof, compiler=row['compilerPath'],
        prelinkMatchingBytes=row['matchingBytes'], prelinkExactAfterDeclaredRelocation=row['exactAfterDeclaredRelocation'],
        matchingBytes=row['bytes'], exactAfterDeclaredRelocation=True, outputSha256=proof['linkedCallerSha256'],
        realLinkInterworkingRequired=True, sourceLanguage='C', ordinaryCBytes=row['bytes'], justifiedAssemblyBytes=0)
    return row, body
