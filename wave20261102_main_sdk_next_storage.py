import re

from elftools.elf.elffile import ELFFile
from project import ROOT


def normalize_alignment(text):
    pattern = r'(?m)^([^\n;{}]+?)\s+(__attribute__\s*\(\(\s*aligned\([^)]*\)\s*\)\))\s*;'
    return re.sub(pattern, lambda m: m[2] + ' ' + m[1].strip() + ';', text)


def lift_statics(text, row, functions, declaration_name):
    seed = next(r for r in functions(text) if r['name'] == row['referenceFunction'])
    body = text[seed['opening']:seed['end']]
    declarations = []
    local_names = {}
    with (ROOT / row['object']).open('rb') as stream:
        symbols = list(ELFFile(stream).get_section_by_name('.symtab').iter_symbols())
    for match in list(re.finditer(r'(?m)^\s*static\s+[^;{}]*;', body))[::-1]:
        declaration = match[0].strip()
        name = declaration_name(declaration)
        candidates = [s.name for s in symbols if s.name.startswith(name + '$') and s['st_info']['type'] == 'STT_OBJECT']
        if len(candidates) != 1:
            raise ValueError('Local static SDK identity is ambiguous: ' + str(name))
        newname = 'native_static_' + name
        local_names[candidates[0]] = newname
        declarations.append(re.sub(r'\b' + re.escape(name) + r'\b', newname, declaration))
        body = body[:match.start()] + body[match.end():]
        body = re.sub(r'\b' + re.escape(name) + r'\b', newname, body)
    return text[:seed['start']] + '\n'.join(declarations) + '\n' + text[seed['start']:seed['opening']] + body + text[seed['end']:], local_names


def storage_groups(text, row, bases, aliases, entities, local_names):
    records = entities(text)
    declarations = [r for r in records if r['kind'] == 'declaration']
    remove = set()
    groups = []
    insertions = {}
    layouts = []
    with (ROOT / row['object']).open('rb') as stream:
        elf = ELFFile(stream)
        symbols = list(elf.get_section_by_name('.symtab').iter_symbols())
        for section, base in sorted(bases.items()):
            objects = sorted((s for s in symbols if s['st_shndx'] == section and s['st_info']['type'] == 'STT_OBJECT'), key=lambda s:s['st_value'])
            typename = 'NativeStorage_' + format(base, '08x')
            globalname = 'native_data_main_' + format(base, '08x')
            fields = []
            checks = []
            members = []
            section_declarations = []
            cursor = 0
            for symbol in objects:
                offset, size = symbol['st_value'], symbol['st_size']
                if offset < cursor:
                    raise ValueError('Measured SDK storage has overlapping objects')
                if offset > cursor:
                    fields.append('unsigned char padding_' + format(cursor, '04x') + '[' + str(offset - cursor) + '];')
                name = symbol.name
                sourcename = local_names.get(name, name)
                candidates = [d for d in declarations if re.search(r'\b' + re.escape(sourcename) + r'\b', d['text']) and not d['text'].strip().startswith('typedef')]
                candidates = [d for d in candidates if re.fullmatch(r'[A-Za-z_]\w*', sourcename)]
                field = 'field_' + format(offset, '04x')
                if candidates:
                    declaration = candidates[-1]
                    fragment = declaration['text'].strip().split('=', 1)[0].rstrip().removesuffix(';').rstrip()
                    fragment = re.sub(r'\b(?:static|extern)\s+', '', fragment)
                    fragment = re.sub(r'\b' + re.escape(sourcename) + r'\b', field, fragment)
                    fields.append(fragment + ';')
                    for item in candidates:
                        remove.add(id(item))
                        section_declarations.append(records.index(item))
                    aliases[sourcename] = globalname + '.' + field
                    checks.append('typedef char StorageCheck_' + format(base, '08x') + '_' + field + '[(sizeof(((' + typename + ' *)0)->' + field + ') == ' + str(size) + ' && (unsigned int)&((' + typename + ' *)0)->' + field + ' == ' + str(offset) + ') ? 1 : -1];')
                    members.append(dict(name=name, field=field, offset=offset, bytes=size))
                else:
                    fields.append('unsigned char ' + field + '[' + str(size) + '];')
                    members.append(dict(name=name, field=field, offset=offset, bytes=size, opaqueUncredited=True))
                cursor = offset + size
            group = 'typedef struct {\n' + '\n'.join(fields) + '\n} ' + typename + ';\nextern ' + typename + ' ' + globalname + ';\n' + '\n'.join(checks)
            if not section_declarations:
                raise ValueError('No typed declarations for SDK storage section')
            insertions.setdefault(max(section_declarations), []).append(group)
            layouts.append(dict(section=section, nativeBase=hex(base), members=members, storageCredit=0))
    pieces = []
    for index, record in enumerate(records):
        if id(record) not in remove:
            pieces.append(record['text'])
        pieces.extend(insertions.get(index, []))
    return '\n'.join(pieces) + '\n', layouts
