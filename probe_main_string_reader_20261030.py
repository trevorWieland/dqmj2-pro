import os
import subprocess
from project import ROOT, configuration, native_dependencies, write_json, sha256
native_dependencies(configuration())
from elftools.elf.elffile import ELFFile
import match_runtime as compiler
from link_runtime_unit import measured_module


def main():
    original = (ROOT / 'nonmatching/main-runtime/20261030/string-reader/native_main_0201d618.c').read_text()
    old = "        if (reader->eof != 0) reader->eof = 0;\n        else reader->cursor--;\n        return value;"
    forms = [
        ('early_return', "        if (reader->eof != 0) { reader->eof = 0; return value; }\n        reader->cursor--;\n        return value;"),
        ('goto_return', "        if (reader->eof != 0) { reader->eof = 0; goto value_return; }\n        reader->cursor--;\nvalue_return:\n        return value;"),
        ('switch_break', "        if (reader->eof != 0) { reader->eof = 0; break; }\n        reader->cursor--;\n        break;"),
        ('inverted', "        if (reader->eof == 0) { reader->cursor--; return value; }\n        reader->eof = 0;\n        return value;")]
    metadata, binary, config = measured_module('main')
    target = binary[0x1d618:0x1d69c]
    work = ROOT / 'work/main-runtime-20261030/string-reader/shapes'
    work.mkdir(parents=True, exist_ok=True)
    rows = []
    for tag, form in forms:
        text = original.replace(old, form)
        if tag == 'switch_break':
            text = text.rsplit('    }\n}', 1)[0] + '    }\n    return value;\n}\n'
        source = work / (tag + '.c')
        source.write_text(text, encoding='utf-8')
        obj = source.with_suffix('.o')
        result = subprocess.run([str(compiler.COMPILER), *compiler.FLAGS, '-opt', 'speed', '-c', str(source), '-o', str(obj)],
            capture_output=True, timeout=60,
            env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')))
        assert result.returncode == 0, (result.stdout + result.stderr).decode(errors='replace')
        with obj.open('rb') as stream:
            elf = ELFFile(stream)
            symbol = elf.get_section_by_name('.symtab').get_symbol_by_name('native_main_0201d618')[0]
            body = elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value'] + symbol['st_size']]
        rows.append({'shape': tag, 'bytes': len(body), 'sameOffsetBytes': sum(a == b for a, b in zip(body, target)),
            'exact': body == target, 'source': source.relative_to(ROOT).as_posix(), 'sourceSha256': sha256(source),
            'object': obj.relative_to(ROOT).as_posix(), 'objectSha256': sha256(obj)})
    write_json(ROOT / 'evidence/attempts/main-string-reader-shapes-20261030.json',
        {'sourceCredit': 0, 'initialProbeSetupFailure': 'Imported elftools before initializing explicit repository-local dependencies; no compilation or source changes occurred', 'rows': rows})
    print([{key: value for key, value in row.items() if key in ['shape', 'bytes', 'sameOffsetBytes', 'exact']} for row in rows])


if __name__ == '__main__':
    main()
