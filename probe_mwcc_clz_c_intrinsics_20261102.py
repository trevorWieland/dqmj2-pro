import os
import subprocess
import match_runtime
from elftools.elf.elffile import ELFFile
from project import ROOT, write_json, sha256


def main():
    work = ROOT / 'work/mwcc-clz-c-intrinsic-probes-20261102'
    work.mkdir(parents=True, exist_ok=True)
    compiler = ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
    flags = ['-lang', 'c99', '-O4,p', '-proc', 'arm946e', '-interworking', '-gccinc']
    results = []
    for index, expression in enumerate(['__builtin_clz(value)', '__clz(value)']):
        source, obj = work / f'probe-{index}.c', work / f'probe-{index}.o'
        source.write_text('unsigned int probe(unsigned int value) { return ' + expression + '; }\n', encoding='utf-8')
        run = subprocess.run([str(compiler), *flags, '-c', str(source), '-o', str(obj)], cwd=ROOT,
            capture_output=True, text=True, timeout=60,
            env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')))
        row = dict(expression=expression, sourceSha256=sha256(source), exitCode=run.returncode,
            stdout=run.stdout, stderr=run.stderr)
        if run.returncode == 0:
            with obj.open('rb') as stream:
                elf = ELFFile(stream)
                symbol = next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name == 'probe')
                start = symbol['st_value'] & ~1
                row['codeHex'] = elf.get_section(symbol['st_shndx']).data()[start:start + symbol['st_size']].hex()
                row['undefinedSymbols'] = [s.name for s in elf.get_section_by_name('.symtab').iter_symbols()
                    if s['st_shndx'] == 'SHN_UNDEF' and s.name]
                row['intrinsicRecognized'] = not row['undefinedSymbols']
        results.append(row)
    write_json(ROOT / 'evidence/attempts/mwcc-clz-c-intrinsic-probes-20261102.json',
        dict(sourceCredit=0, compilerSha256=sha256(compiler), results=results, nativeFunctionReturns=0,
            externalUnknownClzSymbolsMustNotBeBoundAsCompilerIntrinsics=True))
    print(dict(probes=len(results), compiling=sum(r['exitCode'] == 0 for r in results), sourceCredit=0))


if __name__ == '__main__':
    main()
