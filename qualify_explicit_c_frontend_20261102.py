import hashlib
import os
import subprocess
import match_runtime
from elftools.elf.elffile import ELFFile
from project import ROOT, sha256
from link_runtime_unit import relocation_rows


def signature(path, name):
    with path.open('rb') as stream:
        elf = ELFFile(stream)
        symbols = [s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name == name]
        assert len(symbols) == 1
        symbol = symbols[0]
        assert symbol['st_info']['type'] == 'STT_FUNC'
        start, size = symbol['st_value'] & ~1, symbol['st_size']
        body = elf.get_section(symbol['st_shndx']).data()[start:start + size]
        assert len(body) == size and size
    return dict(bytes=size, bodySha256=hashlib.sha256(body).hexdigest(),
        relocations=relocation_rows(path, name))


def qualify(row, directory):
    source, original = ROOT / row['source'], ROOT / row['object']
    compiler_name = row.get('compiler') or row['compilerPath']
    compiler = ROOT / compiler_name
    assert source.suffix == '.c'
    assert sha256(source) == row['sourceSha256']
    assert sha256(original) == row['objectSha256']
    assert sha256(compiler) == row['compilerSha256']
    flags = row.get('compilerFlags') or []
    assert '-lang' not in flags
    assert all(flag not in flags for flag in ['-c', '-o'])
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / 'explicit-c99.o'
    command = [str(compiler), *flags, '-lang', 'c99', '-c', str(source), '-o', str(output)]
    run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120,
        env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')))
    assert run.returncode == 0, (run.returncode, run.stdout, run.stderr)
    before, after = signature(original, row['name']), signature(output, row['name'])
    assert before == after, (before, after)
    return dict(source=row['source'], sourceSha256=sha256(source), compiler=compiler_name,
        compilerSha256=sha256(compiler), originalObject=row['object'], originalObjectSha256=sha256(original),
        explicitC99Object=output.relative_to(ROOT).as_posix(), explicitC99ObjectSha256=sha256(output),
        command=command, exitCode=run.returncode, stdout=run.stdout, stderr=run.stderr,
        completeFunctionBytesAndOriginalRelocationsEqual=True, signature=after,
        sourceCredit=0, sourceLanguage='C', productionObjectAndFlagsChanged=False)
